"""Independently audit every saved repack round against its fixed assignment."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import itertools,json,math,shutil,subprocess,sys,zipfile
import shapely
from shapely.geometry import Polygon,box
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-assignment-repack-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')

def inspect(value,original):
    expected=Counter((p['item_index'],p['external_id']) for p in original['initial']['items'])
    assert Counter((p['item_index'],p['external_id']) for p in value['items'])==expected
    assert value['container']==original['initial']['container']
    boundary=Polygon(value['container']);assert boundary.is_valid and boundary.area>0
    collision=[Polygon(p['polygon']) for p in value['items']]
    assert all(p.is_valid and p.area>0 for p in collision)
    outside=[p.difference(boundary).area for p in collision]
    overlap=[(i,j,a.intersection(b).area) for (i,a),(j,b) in itertools.combinations(enumerate(collision),2)]
    original_job=original['job'];stock=original_job['stocks'][0];m=stock['margins'];e=original_job['edge_clearance']
    usable=box(m['left']+e,m['bottom']+e,stock['width']-m['right']-e,stock['height']-m['top']-e)
    public=[];placements=[];copies=Counter()
    for item in value['items']:
        part=original_job['parts'][item['external_id']];t=item['public_transform']
        assert item['orientation_allowed'] is True
        assert isinstance(t['mirrored'],bool) and (not t['mirrored'] or part['allow_mirror'])
        assert all(math.isfinite(v) for v in [*t['translation'],t['rotation_radians']])
        rotation=part['rotations']
        if rotation['kind']!='free':
            degrees=rotation['degrees'] if rotation['kind']=='list' else [i*rotation['degrees'] for i in range(math.ceil(360/rotation['degrees']))]
            assert min(abs(math.remainder(t['rotation_radians']-math.radians(a),2*math.pi)) for a in degrees)<1e-7
        assert len(part['geometry'])==1
        shape=Polygon(part['geometry'][0]['outer']);assert shape.is_valid
        c,s=math.cos(t['rotation_radians']),math.sin(t['rotation_radians']);mirror=-1 if t['mirrored'] else 1
        public.append(affine_transform(shape,[mirror*c,-s,mirror*s,c,*t['translation']]))
        placements.append({'part_id':part['id'],'copy_index':copies[part['id']],'sheet_id':'assignment','transform':t})
        copies[part['id']]+=1
    gaps=[a.distance(b)-original_job['clearance'] for a,b in itertools.combinations(public,2)]
    public_disjoint=all(a.disjoint(b) for a,b in itertools.combinations(public,2))
    public_outside=[p.difference(usable).area for p in public]
    job=deepcopy(original_job);job['parts']=[{**p,'quantity':copies[p['id']]} for p in job['parts'] if copies[p['id']]]
    layout={'version':1,'units':job['units'],'sheets':[{'id':'assignment','stock_id':stock['id']}],'placements':placements}
    summary={'parts':len(collision),'shortened_boundary_exact':True,'membership_exact':True,
        'source_polygon_outside_areas_mm2':outside,'source_positive_pair_intersections_mm2':[r for r in overlap if r[2]>0],
        'collision_clear':all(v==0 for v in outside) and all(r[2]==0 for r in overlap),
        'original_filled_outers_disjoint':public_disjoint,'full_stock_outside_areas_mm2':public_outside,
        'minimum_original_clearance_slack_mm':min(gaps) if gaps else None,
        'clearance_roundoff_tolerance_mm':1e-7,
        'original_filled_outer_clear':public_disjoint and all(v==0 for v in public_outside) and all(g>=-1e-7 for g in gaps),
        'original_orientations_and_reflections_checked':True}
    return summary,job,layout

if __name__=='__main__':
    sys.path.insert(0,str(root/'scripts'));import h5_assignment_repack as runner
    result=load(out/'results.json');plan=load(out/'plan.json')
    assert runner.guards()==plan['guards'] and result['guards_unchanged']
    assert result['all_four_completed'] and len(result['records'])==4
    audit=out/'validation';audit.mkdir();records=[]
    for row in result['records']:
        archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None and set(z.namelist())==set(row['members'])
            for name,expected in row['members'].items():
                data=z.read(name);assert len(data)==expected['bytes'] and sha256(data).hexdigest()==expected['sha256']
            original=json.loads(z.read('input.json'));output=json.loads(z.read('output.json'))
            assert sha256(z.read('input.json')).hexdigest()==row['sha256']
        assert output['exact_reconstruction'] and output['parts']==row['parts'] and output['seed']==0
        assert 1<=len(output['rounds'])<=6
        findings=[]
        for index,round in enumerate(output['rounds']):
            assert round['index']==index and round['initialization']==('saved_initial' if index==0 else 'all_items_random')
            checked,job,layout=inspect(round['geometry'],original)
            name=Path(row['input']).stem+'-round-'+str(index);folder=audit/name;folder.mkdir()
            write(folder/'job.json',job);write(folder/'layout.json',layout)
            command=[str(runner.prior.CLI),'validate','--job',str(folder/'job.json'),'--layout',str(folder/'layout.json')]
            p=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
            (folder/'stdout.json').write_bytes(p.stdout);(folder/'stderr.log').write_bytes(p.stderr)
            public=json.loads(p.stdout);assert isinstance(public['valid'],bool)
            checked.update(index=index,separator_best_loss=round['best_loss'],seconds=round['seconds'],
                CLI_valid=public['valid'],CLI_exit_code=p.returncode,command=command)
            checked['feasibility_witness']=checked['collision_clear'] and checked['original_filled_outer_clear'] and public['valid'] and p.returncode==0
            write(folder/'checks.json',checked);findings.append(checked)
        assert output['separator_clear_snapshot_found']==any(r['best_loss']==0 for r in output['rounds'])
        records.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'archive':row['archive'],'archive_sha256':row['archive_sha256'],
            'parts':row['parts'],'witness_rounds':[r['index'] for r in findings if r['feasibility_witness']],'rounds':findings})
    write(out/'independent-audit.json',{'all_original_archives_verified':True,'all_four_assignments_audited':True,
        'source_sha256':digest(Path(__file__)),'shapely_version':shapely.__version__,'records':records,
        'feasible_assignments':sum(bool(r['witness_rounds']) for r in records),'failed_search_proves_infeasibility':False,
        'global_or_material_quality_claim':False,'H5_complete':False})
    shutil.copyfile(__file__,out/'audit.py')
    print(json.dumps({'assignments':4,'feasible_assignments':sum(bool(r['witness_rounds']) for r in records),
        'rounds_audited':sum(len(r['rounds']) for r in records),'witness_rounds':[(r['job'],r['kerf_mm'],r['witness_rounds']) for r in records]}))
