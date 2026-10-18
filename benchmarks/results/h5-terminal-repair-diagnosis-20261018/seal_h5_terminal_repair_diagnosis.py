"""Seal the unchanged failed repair observation and its rejected geometry follow-ups."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from collections import Counter
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];OBS=ROOT/'output/h5-terminal-repair-observer-20261018'
FREE=ROOT/'output/h5-terminal-cog-regions-20261018';RELAX=ROOT/'output/h5-terminal-contact-relaxation-20261018'
OUT=ROOT/'benchmarks/results/h5-terminal-repair-diagnosis-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();plan=load(OBS/'plan.json');native=load(OBS/'run/checks.json');audit=load(OBS/'audit/checks.json');follow=load(RELAX/'audit/checks.json');free=load(FREE/'checks.json');relax=load(RELAX/'checks.json')
    assert native['original_failure_reproduced_exactly'] and native['same_work_counts_stats_and_expiry'] and audit['all_runtime_and_prior_tests_unchanged'] and follow['complete']
    assert plan['prior_tests_unchanged']==173 and native['accepted_layouts']==follow['accepted_layouts']==0
    assert source_digest()==audit['production_digest']==follow['production_digest']=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    assert digest(OBS/'terminal-tests.exe')=='ec04a28d449908e8231ee8a28c927141d24c457df8c4633b61bba5f4359482cc'
    moves=load(OBS/'audit/moves.json');families=Counter(p['part_id'] for p in moves);assert families=={'cog':15,'bracket':3,'insert':3}
    best=load(OBS/'audit/best/checks.json');initial=load(OBS/'audit/initial/checks.json')
    assert len(best['physical_conflicts'])==10 and all('cog' in p['parts'] for p in best['physical_conflicts'])
    ci=json.loads(subprocess.check_output(['gh','run','view','39137371817','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']=='cb5e23cb698ab81c59b14b51bb008399688183c1' and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    write(OUT/'main-ci-cb5e23c.json',ci)
    next_step=('The fixed-seed repair and every terminal state are now observed. Do not repeat the same repair, '
        'spacing adjustment or one-cog relocation grid. The local collective LP also fails actual geometry and '
        'must not be treated as a feasible rearrangement. The native separator moves all cogs but leaves the '
        'noncolliding frame block fixed; the closest beam construction likewise commits to that block early. '
        'Next investigate a discrete placement-selection construction that chooses several compatible part '
        'placements together from actual-outline contact candidates, with exact inventory constraints, '
        'rather than committing each part greedily. Include alternative frame allocations already present '
        'in the retained catalog, retain candidate/coverage failures and declare a finite offline limit '
        'before running. Do not alter the original stock, filled holes, quantities, rotations or material '
        'target. An independently validated whole-job target witness is still required before proposing '
        'bounded runtime changes or another matched quality pilot. These restricted failures are not '
        'global infeasibility evidence. Normal-mode hole riders cannot be reused under the common-line '
        'reserved-hole requirement.')
    review={'next_investigation':next_step,'original_failure_reproduced_exactly':True,'production_and_runtime_unchanged':True,
        'all_prior_173_tests_unchanged':True,'full_regression_suite_run':False,'instrumented_replays':1,'new_native_search_inputs':0,
        'quality_runs':0,'accepted_target_layouts':0,'budgets_guards_and_gate_limits_unchanged':True,
        'frozen_cli_sha256':'97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b',
        'terminal_observer_binary_sha256':digest(OBS/'terminal-tests.exe'),'production_digest':source_digest(),
        'readmes_unchanged':{p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']},'H5_complete':False,'completion_percent':60}
    write(OUT/'source-review.json',review)
    helpers=['prepare_h5_terminal_repair_observer.py','build_h5_terminal_repair_observer.py','run_h5_terminal_repair_observer.py',
        'audit_h5_terminal_repair_state.py','plot_h5_terminal_repair_state.py','relocate_h5_terminal_cogs.py','relax_h5_terminal_contacts.py',
        'audit_h5_terminal_followups.py','diagnose_h5_concave_gaps.py']
    members=[]
    for p in sorted(OBS.iterdir()):
        if p.is_file() and p.name!='terminal-tests.exe':members.append((p,OBS.name+'/'+p.name))
    for name in ['run','audit']:
        for p in sorted((OBS/name).rglob('*')):
            if p.is_file():members.append((p,OBS.name+'/'+p.relative_to(OBS).as_posix()))
    for phase in [FREE,RELAX]:
        for p in sorted(phase.rglob('*')):
            if p.is_file():members.append((p,phase.name+'/'+p.relative_to(phase).as_posix()))
    for row in plan['source_files']:members.append((OBS/'candidate'/row['path'],'observer-source/'+row['path']))
    for name in helpers:members.append((ROOT/'output'/name,'helpers/'+name))
    inputroot=ROOT/'output/h5-pattern-joint-probe-20261018/inputs'/plan['case']
    for name in ['library.json','request.json']:members.append((inputroot/name,'original-public-inputs/'+name))
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p,name in members:
            assert '.claude' not in p.parts
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    shutil.copyfile(OBS/'terminal-layouts.png',OUT/'terminal-layouts.png')
    checks={'verified_utc':datetime.now(timezone.utc).isoformat(),'all_stated_scope_checks_passed':True,
        'observational_replay':native,'terminal_geometry_audit':audit,'moved_families':dict(families),
        'physical_overlap_reduction_percent':100*(1-best['filled_overlap_mm2']/initial['filled_overlap_mm2']),
        'free_region_followup':free,'collective_followup':relax,'followup_audit':follow,
        'archive_sha256':digest(archive),'archive_members':len(manifest),'production_digest':source_digest(),
        'main_cb5e23c_all_six_CI_jobs_passed':True,'runtime_changed':False,'H5_complete':False,'completion_percent':60}
    write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/'seal_h5_terminal_repair_diagnosis.py')
    doc=f'''# H5: retained repair state and residual cog conflicts — 2026-10-18

The observed repair reduces physical overlap by **78.8441%**, but still fails.
Its retained best state has **ten pair overlaps and one cog extending 47.7152 mm
beyond the original stock edge**. All remaining overlaps involve cogs. No expired
state or geometry follow-up becomes an accepted layout; H5 remains open.

The [native-margin investigation](h5-native-collision-diagnosis-20261018.md) produced
four partial layouts with exactly zero native loss, yet restoring their missing
parts still expired the unchanged repair. This checkpoint instruments one fixed
replay of the closest case, large plates / 0.2 mm, to retain both its initial
proposal and its best state immediately before the original expiry return.

The test-only observer runs in a fresh source copy and build target on logical
CPU 8. Seed 0, the 12-work-second allowance, hard limit, runtime decisions and
charged work remain unchanged. It reproduces the previous failure's **exact work
counts, statistics, initial losses and expiry**, finishing at 12.03904728 charged
seconds (14.8567 real seconds). No quality run is repeated and the expired result
is still rejected. All 173 prior test bodies and all runtime source remain exact
after removing the observer; this does not claim a fresh full regression run.

Stable tracker identity is matched uniquely to all **66 original copies**, then
carried through the retained best state. Independent original-vertex transforms
and filled-outer checks examine **2,953 physical pairs** across the two states.
Both original public CLI checks reject their layouts. Original quantities and
copy identities are preserved; holes stay reserved.

| Retained state | Native loss score | Filled overlap (mm²) | Parts on first / second sheet | Accepted |
| --- | ---: | ---: | ---: | :---: |
| Initial proposal | 175,938.3125 | 39,022.751975 | 53 / 13 | no |
| Best before expiry | 83,827.648438 | 8,255.630840 | 54 / 12 | no |

Native loss scores are not overlap areas. The best state has eleven native pair
collisions and one wall collision: the additional pair contact crosses the joined
virtual sheet boundary because the out-of-stock cog straddles it. Its second-sheet
height is 325.788154 mm, below the original 325.926902 mm target, but the other
violations still invalidate the layout. All 15 cogs, three brackets and three
inserts move; three copies change sheets. **No frame moves.**

![The initial and rejected best states, with failed physical contacts highlighted](h5-terminal-repair-diagnosis-20261018/terminal-layouts.png)

A separate fixed-neighbour free-space construction removes one conflicting cog
at a time. It tests its retained angle plus integer angles 0–17°, on both original
target sheets: **380 queries over ten cogs**. Exact covering convex pieces build
Minkowski obstacles with a conservative mitred clearance envelope and a positive
0.0001 mm construction margin. Every saved free region is empty; no move is
accepted. It finishes in 34.114 seconds under its declared 120-second geometry
ceiling. This finite-angle, conservative query is not a proof that no single-cog
move exists under arbitrary rotation, and says nothing about global feasibility.

One bounded offline collective experiment then lets every non-frame part
translate together, including currently noncolliding neighbours. Rotations,
reflections, sheet assignments and the frame block stay fixed. Closest obstacle
boundaries define a local linear problem with nonnegative separation slacks,
original stock bounds and 60 mm coordinate trust steps. Every constraint and the
objective recheck: its predicted slack sum is **120.539379 mm**. However, the actual
conservative penetration measure rises from **249.971424 mm** to **468.483502 mm**
at the full step. Fractions 1/2, 1/4, 1/8 and 1/16 also worsen that measure.
The method stops at its first local stall after 8.591 seconds; it accepts no move.

Independent original-shape checks replay all five collective proposals, covering
another **7,485 physical pairs**. They contain 22–23 pair conflicts, compared with
ten initially. The full step brings the protruding cog inside stock but has
34,468.544080 mm² overlap and fails the original public CLI check. The smallest
step slightly lowers overlap area to 8,193.476867 mm² while increasing the conflict
count to 22 and retaining the stock violation; it is still rejected. No linear
prediction is substituted for geometric acceptance. Both follow-ups retain the
original rejected terminal layout unchanged as their final output.

[Checks](h5-terminal-repair-diagnosis-20261018/checks.json),
[all raw source, states, regions, proposals, logs and audits](h5-terminal-repair-diagnosis-20261018/raw.zip),
[manifest](h5-terminal-repair-diagnosis-20261018/raw-manifest.json),
[next investigation](h5-terminal-repair-diagnosis-20261018/source-review.json).
All {len(manifest)} archive members, CRCs and byte hashes verify. The saved failed
proposals, original work limit, conversion guard and material target are unchanged.

{next_step}

All six hosted checks on main commit `cb5e23c` pass, including both native
platforms and the Chromium/Firefox web job ([record](h5-terminal-repair-diagnosis-20261018/main-ci-cb5e23c.json)).
That is the previous pushed revision, not a claim about this evidence commit.
Production source, preview assets and all three accurate README descriptions
remain unchanged. H2/H5 are still open at **60%**; this diagnostic work does not
create a newly qualified release.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 terminal repair diagnosis, 2026-10-18:** [one fixed observational replay](../benchmarks/results/h5-terminal-repair-diagnosis-20261018.md)
reproduces the previous failure's exact work, statistics and expiry. The retained
best state reduces physical overlap 78.8441%, but has ten pair overlaps and one cog
47.7152 mm outside stock. All residual overlaps involve cogs; all 15 cogs move and
no frame moves. Original identities/quantities, budgets and rejection remain.
All 380 sampled fixed-neighbour cog free regions are empty. A collective local
linear step also fails actual geometry at all five tested fractions and accepts
no move. Independent original-shape checks cover 2,953 terminal-state pairs plus
7,485 collective-trial pairs; the original CLI rejects both terminal states and
the full collective proposal. Preserve these restricted failures, then investigate
joint selection of compatible actual-outline placements and alternative frame
allocations before another runtime proposal. All six prior main `cb5e23c` hosted
checks pass. Runtime, release assets and accurate READMEs remain unchanged;
H2/H5 stay open at 60%.
'''
    prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==prior
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 native-margin diagnosis, 2026-10-18:**';assert s.count(marker)==1
    p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-terminal-repair-diagnosis-20261018/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'accepted_target_layouts':0,'H5_complete':False}),flush=True)
if __name__=='__main__':main()
