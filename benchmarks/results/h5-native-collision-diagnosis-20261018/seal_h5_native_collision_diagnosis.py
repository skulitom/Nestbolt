"""Record exact native collision causes, verified zero-loss partials and bounded failed completion attempts."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from collections import Counter
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];OBS=ROOT/'output/h5-native-collision-observer-20261018'
FAIL=ROOT/'output/h5-native-partial-spacing-20261018';SPACE=ROOT/'output/h5-native-partial-spacing-recovery-20261018'
JOINT=ROOT/'output/h5-spaced-joint-repair-20261018';OUT=ROOT/'benchmarks/results/h5-native-collision-diagnosis-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();audit=load(OBS/'audit-recovery/checks.json');verified=load(SPACE/'verification/checks.json');joint=load(JOINT/'checks.json');nativeplan=load(OBS/'plan.json')
    assert audit['source_and_geometry_reconstruction_verified'] and verified['complete'] and joint['complete']
    assert verified['native_zero_loss_partials']==4 and joint['complete_target_layouts']==0
    assert all(c['partial_native_loss_zero'] and c['expired']==1 and c['completed']==0 for c in joint['cases'])
    assert source_digest()==audit['production_digest']=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    recovery=load(OBS/'audit-recovery-plan.json')
    for name,h in recovery['completed_geometry_files'].items():
        assert digest(OBS/'audit'/name)==h and digest(OBS/'audit-recovery'/name)==h
    case_records=[];all_counts=Counter();table=[]
    for case in audit['cases']:
        r=load(OBS/'audit-recovery'/(case+'.json'));v=next(x for x in verified['cases'] if x['case']==case);j=next(x for x in joint['cases'] if x['case']==case)
        by_input={}
        for ob in r['observations']:
            counts=sum((Counter(s['counts']) for s in ob['sheets']),Counter());all_counts+=counts
            for key in ['reported_but_disjoint','polygon_overlap_without_report','static_false_positive','static_missing','requires_roundtrip_or_collision_precision_review']:assert counts[key]==0,(case,key)
            pairs=[p for s in ob['sheets'] for p in s['positive_pairs']];items=[p for s in ob['sheets'] for p in s['items_detail']]
            by_input[ob['input']]={'counts':dict(counts),'native_pair_overlap_mm2':sum(p['native_overlap_mm2'] for p in pairs),
                'native_outside_area_mm2':sum(p['outside_container_mm2'] for p in items),'reported_pairs_requiring_guard_beyond_chord_compensation':sum(p['ideal_native_offset_overlap_mm2']>1e-7 and p['offset_without_guard_overlap_mm2']<=1e-7 for p in pairs)}
        record={'case':case,'observations':by_input,'adjusted_partial':v,'bounded_completion':j};case_records.append(record)
        table.append(f"| {case.removeprefix('m-mechanical-').removesuffix('-s0-candidate')} | {by_input['partial']['counts']['reported_pairs']} | {by_input['partial']['counts']['static_positive']} | {v['max_coordinate_translation_mm']:.6f} | 0 / 0 / 0 | expired |")
    followup=('The saved adjusted partials now start at exactly zero native loss, so do not repeat spacing correction '
        'or treat its extra-cushion shortfall as a native collision failure. Restoring the same missing copies still '
        'expires all four unchanged repair calls. The helper discards its best snapshot on expiry, leaving the '
        'remaining bottleneck unobserved. Next add a test-only terminal-snapshot observer to a fresh isolated source '
        'and target, starting with the closest large-plates / 0.2 mm case (three missing cogs). Replay that fixed '
        'adjusted input once with the same seed 0 and 12-work-second allowance solely to capture the retained best '
        'snapshot, remaining losses, per-part collision partners and sheet assignments before the existing expiry '
        'return. Preserve expiry and every original failed outcome; do not accept an expired snapshot or increase '
        'any budget. Independently validate its physical geometry even if rejected, so the next constructor or '
        'repair proposal addresses the observed obstructions. This is observational diagnosis, not another quality '
        'attempt or evidence that the +1% material target is impossible.')
    review={'followup':followup,'all_production_and_runtime_source_unchanged':True,'prior_172_tests_unchanged':True,
        'native_observer_calls':8,'new_bounded_repair_calls':4,'new_quality_runs':0,'full_layouts_found':0,
        'native_zero_loss_partials':4,'original_quantity_requirements_still_fail':True,
        'collision_guard_or_threshold_changed':False,'native_collision_disagreement_found':False,
        'native_coordinate_roundtrip_max_mm':audit['max_pose_roundtrip_mm'],
        'H5_complete':False,'completion_percent':60,'production_digest':source_digest(),
        'readmes':{p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']},
        'native_observer_binary_sha256':digest(OBS/'observer-tests.exe')}
    write(OUT/'source-review.json',review)
    helpers=['prepare_h5_native_collision_observer.py','build_h5_native_collision_observer.py','run_h5_native_collision_observer.py',
        'audit_h5_native_collision_geometry.py','recover_h5_native_collision_audit.py','audit_h5_native_collision_geometry_recovery.py',
        'space_h5_native_partials.py','recover_h5_native_partial_spacing.py','space_h5_native_partials_recovery.py',
        'check_h5_spaced_native_partials.py','run_h5_spaced_joint_repair.py']
    members=[]
    for p in sorted(OBS.iterdir()):
        if p.is_file() and p.name!='observer-tests.exe':members.append((p,OBS.name+'/'+p.name))
    for name in ['runs','audit','audit-recovery']:
        for p in sorted((OBS/name).rglob('*')):
            if p.is_file():members.append((p,OBS.name+'/'+p.relative_to(OBS).as_posix()))
    for phase in [FAIL,SPACE,JOINT]:
        for p in sorted(phase.rglob('*')):
            if p.is_file():members.append((p,phase.name+'/'+p.relative_to(phase).as_posix()))
    for row in nativeplan['source_files']:members.append((OBS/'candidate'/row['path'],'observer-source/'+row['path']))
    for name in helpers:members.append((ROOT/'output'/name,'helpers/'+name))
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p,name in members:
            assert '.claude' not in p.parts
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    summary={'verified_utc':datetime.now(timezone.utc).isoformat(),'all_stated_scope_checks_passed':True,
        'cases':case_records,'native_polygon_pairs_checked':audit['all_pairs_checked'],
        'adjusted_original_geometry_pairs':sum(c['geometry_pairs'] for c in verified['cases']),
        'native_zero_loss_partials':4,'zero_loss_sheet_and_joined_checks':12,'expired_completion_attempts':4,
        'completed_target_layouts':0,'collision_counts':dict(all_counts),'runtime_changed':False,
        'production_digest':source_digest(),'raw_archive_sha256':digest(archive),'raw_members':len(manifest),
        'H5_complete':False,'completion_percent':60}
    write(OUT/'checks.json',summary);shutil.copyfile(__file__,OUT/'seal_h5_native_collision_diagnosis.py')
    doc=f'''# H5: native collision margins and adjusted partial inputs — 2026-10-18

The native collision discrepancy is explained and corrected in the saved partial
inputs. **All four adjusted partials have exactly zero native loss**, on each sheet
and in the joined strip. Restoring their missing parts still expires four bounded
repair attempts. No complete target layout is found, and H5 remains open.

A new test-only observer exports actual native inflated polygons, original item
templates, container bounds, transforms and tracker entries. It observes the four
saved complete controls, partials and deliberately overlapping proposals without
running separation. Independent Shapely checks reconstruct every transform and
examine **51,175 pairs**. Every reported pair collision has actual native polygon
overlap; every significant native overlap is reported. Every static loss matches
an actual native polygon extending beyond its container. No collision detection
disagreement is found at the recorded 1e-7 geometric comparison scale.

All originally legal pairs with positive native loss are explained by the native
inflation margins. Native pose round-trip error is at most **0.000128 mm**;
independent offset reconstruction differs by at most **0.001168 mm**, within the
unchanged conversion guard. These loss scores include shape penalties and are not
overlap areas. The actual partial pair overlaps total 186–268 mm² per job, despite
the much larger numerical loss scores.

The native model uses `(clearance + conversion_guard) / cos(0.05)` for separation.
The geometric constructor used only 0.0011 mm extra spacing and 0.0001 mm edge
insets. At 0.2 mm, the guard explains the new pair contacts; at 1.5 mm, the chord
compensation alone already exceeds most of that extra spacing. The saved complete
controls also become colliding native inputs: their physically legal gaps can be
as tight as kerf + 0.000001 mm. The guards and physical acceptance criteria stay
unchanged.

A local linear construction then minimizes the largest translation, preserving
every original size, rotation, reflection, copy and sheet assignment. It keeps
the original target containers and seeks an additional 0.001 mm native cushion.
The first linear solution breaks another physical contact; that failure and its
solution are retained. A continuation reuses that solution, backtracks against
all original outer contours, and adds newly active contact constraints. All four
stop at the predeclared 20-iteration limit with predicted native gaps of
0.000622–0.000906 mm. **Their extra-cushion criterion remains failed.**

Those saved outputs are independently evaluated by the unchanged native engine.
Actual native loss is zero in all twelve sheet/joined checks. The original public
library/request checks reject only the unchanged missing quantities. Another
**13,566** filled-outer pair checks confirm physical clearances and original stock
targets. All other control inputs reproduce their earlier observations exactly.

| Case | Initial native pair collisions | Initial boundary collisions | Largest coordinate move (mm) | Adjusted native losses: first / last / joined | Completion repair |
| --- | ---: | ---: | ---: | ---: | --- |
{chr(10).join(table)}

The same missing original copies are restored at their already-saved deliberate
poses; pose selection is not repeated. Each new complete proposal passes the
original quantity/bounds checks and is rejected for its retained overlaps.
The original repair binary then runs once per changed input on logical CPU 8,
with seed 0 and the unchanged 12-work-second allowance. All four expire at
12.036–12.091 charged seconds (13.385–17.295 real seconds), returning no layout.
These are mechanism tests, not quality runs or proof of infeasibility.

The first geometry audit added native f32 tracker entries using Python binary64
and failed its approximate total check on the last case. The recovery reproduces
the native f32 accumulation order and requires exact totals for every item and
sheet. It reuses the first three completed geometry audits byte-for-byte and
finishes only the missing fourth. No native observation or repair was repeated
to repair that audit. Original failures and extra-cushion shortfalls remain.

[Checks](h5-native-collision-diagnosis-20261018/checks.json),
[all raw geometry, attempts, outputs and source](h5-native-collision-diagnosis-20261018/raw.zip),
[manifest](h5-native-collision-diagnosis-20261018/raw-manifest.json),
[next investigation](h5-native-collision-diagnosis-20261018/source-review.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.

{followup}

Production source and all 172 prior test bodies remain unchanged. The added
observer passes on eight fixed inputs; this does not claim a new regression suite
or full H5 acceptance run. Published preview assets and all three accurate READMEs
remain unchanged; H2/H5 are still open at **60%**.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 native-margin diagnosis, 2026-10-18:** [exact native polygons and tracker entries](../benchmarks/results/h5-native-collision-diagnosis-20261018.md)
agree on all 51,175 checked pairs. The saved physical gaps are too tight for the
unchanged native inflation/edge margins. Translations below 0.18 mm produce four
partials with exactly zero native loss on each sheet and the joined strip; all
original sizes, rotations, assignments and stock targets remain. The extra
0.001 mm construction cushion still misses its declared limit and is preserved
as failed. Original public checks reject only the unchanged missing quantities;
13,566 additional filled-outer pairs pass. Restoring the same missing poses still
expires all four original-budget repair calls. Next observe the retained best
snapshot on expiry for the closest case, without accepting it or changing limits.
The f32 audit correction, original linearization failure and all failed repairs
remain preserved. Runtime/release assets stay unchanged; H2/H5 remain open at 60%.
'''
    prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==prior
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 saved-partial joint repair, 2026-10-18:**';assert s.count(marker)==1
    p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-native-collision-diagnosis-20261018/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'native_zero_loss_partials':4,'full_target_layouts':0,'raw_members':len(manifest),'archive_bytes':archive.stat().st_size}),flush=True)
if __name__=='__main__':main()
