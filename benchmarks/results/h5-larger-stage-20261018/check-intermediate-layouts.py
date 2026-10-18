"""Independently validate saved exchange/fill snapshots; run no new searches."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import itertools,json,math,shutil,subprocess,traceback,zipfile
import shapely
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-larger-stage-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
assert load(out/'verification.json')['all_original_archives_verified']
cli=root/'target/release/nestbolt.exe';expected='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b';assert digest(cli)==expected
folder=out/'intermediate-layouts';folder.mkdir();records=[];timings=[]
tolerance=1e-7
def filled_geometry(job,layout):
    parts={p['id']:p for p in job['parts']}
    assert Counter(p['part_id'] for p in layout['placements'])==Counter({p['id']:p['quantity'] for p in job['parts']})
    assert len({(p['part_id'],p['copy_index']) for p in layout['placements']})==len(layout['placements'])
    sheets={}
    for p in layout['placements']:
        part=parts[p['part_id']];assert len(part['geometry'])==1
        shape=Polygon(part['geometry'][0]['outer']);assert shape.is_valid and shape.area>0
        t=p['transform'];c=math.cos(t['rotation_radians']);s=math.sin(t['rotation_radians']);m=-1 if t['mirrored'] else 1
        transformed=affine_transform(shape,[m*c,-s,m*s,c,*t['translation']]);assert transformed.is_valid
        sheets.setdefault(p['sheet_id'],[]).append(transformed)
    count=0;minimum=math.inf
    for shapes in sheets.values():
        for a,b in itertools.combinations(shapes,2):
            count+=1;assert a.disjoint(b),'Filled outer polygons overlap'
            slack=a.distance(b)-job['clearance'];minimum=min(minimum,slack)
            assert slack>=-tolerance,slack
    return {'same_sheet_pairs':count,'minimum_clearance_slack_mm':minimum if count else None}
try:
    for row in load(out/'results.json')['records']:
        archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None;job=json.loads(z.read('nested/job.json'))
        assert job['clearance']==row['kerf_mm']
        for invocation,t in enumerate(row['diagnosis']['traces']):
            a=t['attempts'];phases={
                'baseline_validation':t['baseline_elapsed'] or 0,
                'choice_construction':sum(x['elapsed'] for x in t['choice_setup']),
                'paired_generation':sum(x['elapsed'] for x in t['generations']),
                'attempt_setup':sum(x['attempt_setup_elapsed'] or 0 for x in a),
                'receiver_repair':sum(x['receiver_elapsed'] or 0 for x in a),
                'source_repair':sum(x['source_elapsed'] or 0 for x in a),
                'reconstruction':sum(x['reconstruction_elapsed'] or 0 for x in a),
                'proposal_validation':sum(x['validation_elapsed'] or 0 for x in a),
            }
            assert sum(phases.values())<=t['total_elapsed']
            phases['other_and_observation_overhead']=t['total_elapsed']-sum(phases.values())
            timings.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'invocation':invocation,'total_elapsed_seconds':t['total_elapsed'],
                'seconds':phases,'choice_constructions':len(t['choice_setup']),'generation_calls':len(t['generations']),
                'pair_phase_remaining':t['pair_phase_remaining'],'exchange_remaining':t['exchange_remaining'],
                'accepted':[x for x in row['diagnosis']['attempt_rows'] if x['outcome']=='accepted' and x['before_material']==t['before_material']]})
            values=[]
            for view in t['layouts']:
                name=f"{row['job']}-k{row['kerf_mm']}-i{invocation}-{view['stage']}";case=folder/name;case.mkdir()
                write(case/'job.json',job);write(case/'layout.json',view['layout']);write(case/'observation.json',view)
                args=[str(cli),'validate','--job',str(case/'job.json'),'--layout',str(case/'layout.json')]
                result=subprocess.run(args,capture_output=True,timeout=60)
                (case/'stdout.json').write_bytes(result.stdout);(case/'stderr.log').write_bytes(result.stderr)
                write(case/'command.json',{'command':args,'exit_code':result.returncode});assert result.returncode==0
                checked=json.loads(result.stdout);assert checked['valid'];material=checked['metrics']['material_area']
                if view['stage']=='after_exchange':
                    accepted=next(x for x in a if x['outcome']=='accepted')
                    assert material==accepted['after_material'] and material<=t['before_material']
                geometry=filled_geometry(job,view['layout']);values.append(material)
                records.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'invocation':invocation,'stage':view['stage'],
                    'path':case.relative_to(out).as_posix(),'material':material,'exchange_before_material':t['before_material'],
                    'remaining':view['remaining'],'exchange_count':view['exchange_count'],**geometry})
            if values:
                assert len(values)==2
                timings[-1]['immediate_material']={'before_exchange':t['before_material'],'after_exchange':values[0],'after_fill':values[1],
                    'exchange_delta':values[0]-t['before_material'],'fill_delta':values[1]-values[0]}
    assert digest(cli)==expected
    expected_count=2*sum(r['stats'].get('directed_exchanges',0) for r in load(out/'results.json')['records'])
    assert len(records)==expected_count
    write(out/'intermediate-layout-checks.json',{'all_checks_passed':True,'layouts':len(records),'records':records,
        'same_sheet_pairs':sum(r['same_sheet_pairs'] for r in records),'absolute_clearance_tolerance_mm':tolerance,
        'shapely_version':shapely.__version__,'CLI_sha256':expected,'fill_material_nonincrease_assumed':False,'new_searches':0})
    write(out/'phase-timings.json',{'records':timings,'phases_are_disjoint_instrumented_scopes':True,
        'interpretation':'Observed duration under logging. Residual includes uninstrumented work and observation overhead; no minimum-time, speedup or counterfactual claim.', 'new_searches':0})
    shutil.copyfile(__file__,out/'check-intermediate-layouts.py')
    print(json.dumps({'validated_intermediate_layouts':len(records),'same_sheet_pairs':sum(r['same_sheet_pairs'] for r in records),'phase_timings':len(timings)}))
except BaseException:
    write(out/'intermediate-layout-failure.json',{'error':traceback.format_exc(),'completed_records':records});raise
