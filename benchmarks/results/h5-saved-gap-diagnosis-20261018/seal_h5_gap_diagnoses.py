"""Independently audit and preserve four completed saved-layout diagnoses."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from datetime import datetime,timezone
import itertools,json,math,shutil,subprocess,sys,zipfile
from shapely.geometry import Polygon
import shapely
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h5-saved-gap-diagnosis-20261018'
PRIOR=ROOT/'benchmarks/results/h5-source-frontier-pilot-20261018'
PHASES={'hulls':'h5-saved-gap-diagnosis-20261018','concave':'h5-concave-gap-diagnosis-20261018',
        'direct-target':'h5-source-gap-diagnosis-20261018','incremental':'h5-incremental-gap-diagnosis-20261018'}
digest=lambda p:sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_bytes())
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest


def write(p,value):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n')


def append(p,value):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(value)


def check(job,layout,original,report):
    parts={p['id']:p for p in job['parts']};stocks={p['id']:p for p in job['stocks']}
    sheets={p['id']:stocks[p['stock_id']] for p in layout['sheets']}
    key=lambda p:(p['part_id'],p['copy_index'])
    assert set(map(key,layout['placements']))==set(map(key,original['placements']))
    assert len(set(map(key,layout['placements'])))==len(layout['placements'])
    assert layout['sheets']==original['sheets']
    assert Counter(p['part_id'] for p in layout['placements'])==Counter({p['id']:p['quantity'] for p in job['parts']})
    groups={};tops={}
    for p in layout['placements']:
        part=parts[p['part_id']];t=p['transform'];c=math.cos(t['rotation_radians']);s=math.sin(t['rotation_radians'])
        if t['mirrored']:assert part['allow_mirror']
        if part['rotations']['kind']=='list':
            assert any(abs(math.remainder(t['rotation_radians']-math.radians(a),math.tau))<1e-9 for a in part['rotations']['degrees'])
        assert len(part['geometry'])==1
        points=[]
        for x,y in part['geometry'][0]['outer']:
            if t['mirrored']:x=-x
            points.append((c*x-s*y+t['translation'][0],s*x+c*y+t['translation'][1]))
        poly=Polygon(points);assert poly.is_valid and poly.area>0
        x0,y0,x1,y1=poly.bounds;st=sheets[p['sheet_id']];m=st['margins'];e=job['edge_clearance']
        assert not st['outline'] and not st['defects']
        assert x0>=m['left']+e-1e-7 and y0>=m['bottom']+e-1e-7
        assert x1<=st['width']-m['right']-e+1e-7 and y1<=st['height']-m['top']-e+1e-7
        groups.setdefault(p['sheet_id'],[]).append(poly);tops[key(p)]=y1
    pairs=0;minimum=math.inf
    for shapes in groups.values():
        for a,b in itertools.combinations(shapes,2):
            pairs+=1;assert a.disjoint(b);slack=a.distance(b)-job['clearance'];minimum=min(minimum,slack)
            assert slack>=-1e-7
    heights={sid:min(sheets[sid]['height'],max(p.bounds[3] for p in shapes)+sheets[sid]['margins']['top']+job['edge_clearance']) for sid,shapes in groups.items()}
    sid=report['metrics']['last_sheet_id'];measured=report['metrics']['last_sheet_used_height']
    assert abs(heights[sid]-measured)<=2e-6
    full=sum(s['width']*s['height'] for s in sheets.values())
    area=full-sheets[sid]['width']*(sheets[sid]['height']-measured)
    assert abs(area-report['metrics']['material_area'])<=1e-6
    return {'filled_outer_pairs':pairs,'minimum_clearance_slack_mm':minimum,'tops':tops}


def main():
    OUT.mkdir()
    prior=load(PRIOR/'results.json');rows={Path(r['archive']).stem:r for r in prior['records'] if r['arm']=='candidate' and r['seed']==0 and r['job'].startswith('m-mechanical')}
    expected='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    assert source_digest()==expected
    records=[];unique={};commands=0;summaries=[];phase_rows={};file_manifest=[]
    for phase,name in PHASES.items():
        folder=ROOT/'output'/name;plan=load(folder/'plan.json');results=load(folder/'results.json')
        assert results['complete'] and results['production_unchanged'] and results['original_inputs_unchanged']
        assert plan['production_digest']==expected and digest(folder/'diagnose.py')==plan['script_sha256']
        assert plan['results_sha256']==digest(PRIOR/'results.json')
        phase_rows[phase]=[]
        for result in results['cases']:
            case=folder/result['case'];row=rows[result['case']]
            assert digest(PRIOR/row['archive'])==row['archive_sha256']
            assert digest(case/'original.json')==row['layout_sha256']
            with zipfile.ZipFile(PRIOR/row['archive']) as z:
                for member,local in [('library.json','library.json'),('request.json','request.json'),('nested/job.json','job.json')]:
                    assert z.read(member)==(case/local).read_bytes()
            job=load(case/'job.json');original=load(case/'original.json');before=original;previous_tops=None
            stages=['baseline']+[f'transfer-{i+1:03d}' for i in range(len(result['transfers']))]
            assert len(list(case.glob('*-stdout.json')))==len(stages)
            assert load(case/'attempts.json') and len(load(case/'attempts.json'))==result['orientation_attempts']
            for stage in stages:
                layout=load(case/(stage+'.json'));report=load(case/(stage+'-stdout.json'));command=load(case/(stage+'-command.json'))
                assert report['valid'] and command['exit_code']==0
                assert '--library' in command['command'] and '--request' in command['command']
                commands+=1
                key=sha256(json.dumps([job,layout],sort_keys=True).encode()).hexdigest()
                if key not in unique:unique[key]=check(job,layout,original,report)
                checked=unique[key]
                changed=[(a,b) for a,b in zip(before['placements'],layout['placements']) if a!=b]
                if stage=='baseline':assert not changed and report['metrics']==row['metrics']
                else:
                    assert len(changed)==1
                    old,new=changed[0];part_key=(new['part_id'],new['copy_index'])
                    assert (old['part_id'],old['copy_index'])==part_key
                    assert old['sheet_id']==new['sheet_id']==row['metrics']['last_sheet_id']
                    assert checked['tops'][part_key]<previous_tops[part_key]
                    if phase=='direct-target':
                        target=load(case/'conditional-target.json')
                        assert checked['tops'][part_key]<target['required_outline_top_mm']
                    if phase=='incremental':assert previous_tops[part_key]-checked['tops'][part_key]>=.001-1e-7
                records.append({'phase':phase,'case':result['case'],'stage':stage,'layout_sha256':digest(case/(stage+'.json')),
                    'geometry_hash':key,'material_mm2':report['metrics']['material_area'],'changed_copies':len(changed)})
                before=layout;previous_tops=checked['tops']
            assert result['after']['metrics']==report['metrics']
            summary={'case':result['case'],'copies_considered':result['copies_considered'],
                'orientation_attempts':result['orientation_attempts'],'region_constructions':result['region_constructions'],
                'moves':len(result['transfers']),'material_gain_mm2':result['material_gain_mm2']}
            if phase=='incremental':
                b=load(case/'conditional-target.json');old=result['before']['metrics'];new=result['after']['metrics']
                summary.update(height_reduction_mm=old['last_sheet_used_height']-new['last_sheet_used_height'],
                    remaining_excess_mm2=new['material_area']-b['target_material_mm2'],
                    fraction_of_required_gain=result['material_gain_mm2']/(old['material_area']-b['target_material_mm2']))
                summaries.append(summary)
            phase_rows[phase].append(summary)
        for p in sorted(folder.rglob('*')):
            if p.is_file():file_manifest.append({'path':phase+'/'+p.relative_to(folder).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p),'source':p})
    assert commands==33 and len(unique)==21
    assert sum(r['moves'] for r in phase_rows['hulls'])==0 and sum(r['moves'] for r in phase_rows['concave'])==0
    assert sum(r['moves'] for r in phase_rows['direct-target'])==1 and all(r['material_gain_mm2']==0 for r in phase_rows['direct-target'])
    assert all(r['moves']==4 and r['material_gain_mm2']>0 and r['remaining_excess_mm2']>0 for r in summaries)
    archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in file_manifest:z.write(f['source'],f['path'])
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={r['path'] for r in file_manifest}
        for f in file_manifest:assert sha256(z.read(f['path'])).hexdigest()==f['sha256']
    for f in file_manifest:del f['source']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':file_manifest})
    check_record={'verified_utc':datetime.now(timezone.utc).isoformat(),'all_checks_passed':True,'public_CLI_checks':commands,
        'unique_layouts':len(unique),'independent_filled_outer_pairs':sum(r['filled_outer_pairs'] for r in unique.values()),
        'minimum_clearance_slack_mm':min(r['minimum_clearance_slack_mm'] for r in unique.values()),
        'clearance_tolerance_mm':1e-7,'height_rounding_tolerance_mm':2e-6,
        'quantities_orientations_stock_margins_preserved':True,'one_selected_copy_changed_per_step':True,
        'all_holes_reserved':True,'original_sources_and_results_unchanged':True,'production_digest':source_digest(),
        'source_results_sha256':digest(PRIOR/'results.json'),'raw_archive_sha256':digest(archive),'raw_members':len(file_manifest),
        'phase_summaries':phase_rows,'records':records,'shapely_version':shapely.__version__,
        'posthoc_geometry_searches':4,'new_solver_searches':0,'runtime_quality_claim':False,'H5_complete':False}
    write(OUT/'checks.json',check_record)
    for name in ['seal_h5_gap_diagnoses.py','prepare_h5_concave_gap_diagnosis.py','prepare_h5_source_gap_diagnosis.py','prepare_h5_incremental_gap_diagnosis.py']:
        shutil.copyfile(ROOT/'output'/name,OUT/name)
    followup=('Do not integrate a new gap-placement policy or repeat the rejected pilot on this evidence. '
        'The fixed earlier-sheet diagnoses yield no constructed transfer; the four-step source sequences recover only '
        '0.0348–0.7374% of the remaining material gap. This supports small missed local opportunities, not a route to H5. '
        'Before another runtime candidate, inspect the original part geometry for generic multi-part arrangements that '
        'could reduce the larger assignment/packing loss, and construct an independently validated whole-job layout '
        'under the unchanged no-hole, kerf, orientation and stock constraints. An unbounded offline construction would '
        'show feasibility only; it would still require a bounded implementation, all prior qualifications and a new matched pilot. '
        'Do not increase the four-step cap or budgets, relax material limits, use reserved inputs, or claim infeasibility '
        'from these finite-angle greedy diagnostics.')
    interpretation={'followup':followup,'production_changed':False,'H5_complete':False,'completion_percent':60,
        'maximum_fraction_of_required_gain':max(r['fraction_of_required_gain'] for r in summaries),
        'limitations':['Four seed-0 saved candidate layouts only; not representative quality or speed evidence.',
            'Free rotations use original plus four quadrant angles; choices are finite and greedy.',
            'Mitred buffer and positive construction margin can remove true narrow round-clearance regions.',
            'The first hull pass uses a nominal circumscribed polygonal round buffer; its nominal arc angle is not an exact guarantee for every arbitrary corner. No witness was produced there. The later concave passes use mitred over-approximations and all constructed layouts pass independent exact polygon-distance checks.',
            'Zero fixed-neighbour transfers does not prove global infeasibility; smaller gains do not prove a good runtime tradeoff.']}
    write(OUT/'interpretation.json',interpretation)
    table='\n'.join(f"| {r['case'].replace('m-mechanical-','').replace('-s0-candidate','')} | {r['material_gain_mm2']:.6f} | {r['height_reduction_mm']:.6f} | {100*r['fraction_of_required_gain']:.4f}% |" for r in summaries)
    doc=f'''# Saved-layout gap diagnosis — 2026-10-18

Four seed-0 mechanical outputs from the rejected [source-frontier pilot](h5-source-frontier-pilot-20261018.md)
were reused byte-for-byte for deterministic, post-hoc geometry construction on CCD1.
No solver, quality comparison or full gate was rerun. The original 72 results remain intact.

The first convex-hull pass and second pass preserving concave outer contours each
consider 216 source copies and 1,144 orientation attempts across 168 unique region
constructions. Neither constructs an earlier-sheet transfer with every neighbour fixed.
The second pass decomposes each original filled outer ring into convex pieces and
checks exact union coverage before using their Minkowski sums. Holes stay reserved.
Absence of a witness is limited by finite free angles and conservative clearance buffers.

A third pass tries moving source copies directly below their saved +1% material
target. It constructs one valid insert move, with no material gain. A fourth pass
allows smaller height reductions, considers high source copies first and stops at
four moves per case. Each move lowers its own outline top by at least 0.001 mm;
all other placements remain exact. The actual total improvements are:

| Saved case | Material saved (mm²) | Height saved (mm) | Fraction of still-needed saving |
| --- | ---: | ---: | ---: |
{table}

All four remain above the original target. These local geometric opportunities
recover at most **0.7374% of the remaining material gap**, so they do not justify
another runtime candidate or quality pilot by themselves.

The frozen public CLI performs **33 checks across 21 unique layouts**, using each
original library and cutting request. A separate vertex-transform audit covers
**{check_record['independent_filled_outer_pairs']:,} filled-outer pairs**, quantities, rotations,
mirrors, stock margins, unchanged neighbours and the original material calculation.
All checks pass at the unchanged 1e-7 mm clearance tolerance. The raw archive's
{len(file_manifest)} members, CRCs and byte hashes verify. No production code changed.

[Checks](h5-saved-gap-diagnosis-20261018/checks.json),
[original plans, attempted layouts, geometry regions and validator output](h5-saved-gap-diagnosis-20261018/raw.zip),
[archive manifest](h5-saved-gap-diagnosis-20261018/raw-manifest.json),
[limitations and next investigation](h5-saved-gap-diagnosis-20261018/interpretation.json).

{followup}

H2/H5 remain open at **60%**. The published preview and all three READMEs remain
accurate; this diagnostic work does not create a new release candidate.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 saved-gap diagnosis, 2026-10-18:** [four saved mechanical layouts](../benchmarks/results/h5-saved-gap-diagnosis-20261018.md)
produce no fixed-neighbour transfers into earlier sheets in the tested convex-hull
or concave constructions. A direct-target source pass moves one insert without
material gain. Four smaller source moves per case save 0.054057–1.572117 mm of
height, recovering only 0.0348–0.7374% of the remaining material gap. All 33 public
CLI checks (21 unique layouts) and independent filled-outer checks pass. These are
post-hoc finite-angle geometry diagnostics, not quality/speed evidence or a proof
of infeasibility. Preserve them and investigate validated multi-part constructions
before proposing another runtime change. Production, budgets, four-step cap,
material limits and the published preview remain unchanged; completion stays 60%.
'''
    prior_bench=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==prior_bench
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 source-frontier outcome, 2026-10-18:**'
    assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-saved-gap-diagnosis-20261018/** -text -whitespace\n')
    print(json.dumps({k:check_record[k] for k in ['all_checks_passed','public_CLI_checks','unique_layouts','independent_filled_outer_pairs','raw_members']}),flush=True)


if __name__=='__main__':main()
