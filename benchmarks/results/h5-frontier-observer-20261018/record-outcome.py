"""Record verified choice coverage and the resulting bounded ranking hypothesis."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-frontier-observer-20261018'
load=lambda p:json.loads(p.read_bytes())
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
v=load(out/'verification.json');a=load(out/'layout-checks.json');e=load(out/'observed-exchanges.json');r=load(out/'results.json')
assert v['valid']==2 and v['all_traces_verified'] and v['all_original_archives_verified'] and a['all_checks_passed']
assert a['baseline_layouts']==2 and a['attempts_with_height_family']==0 and a['all_credited_sheets_are_source']
assert e['summary']['attempts']==25
assert all(x['height_families']==['insert'] and len(x['height_owners'])==2 and x['all_visited_indices']==[0,1,12] for x in a['baselines'])
assert all(not x['matching_visited_indices'] and x['matching_choice_indices'][0]==6 for x in a['baselines'])
next_step='''The actual search reaches only choice indices 0, 1 and 12 in both
diagnostics: a frame pair, its mixed frame/cog alternative, and the first
frame single. The insert pair is present at index 6; insert singles start at
73. Neither is visited. Both height-setting copies are inserts on the same
last sheet that receives the material offcut credit. Removing repeated
neutral validation increased attempts but did not reach that family.

The next isolated candidate should rank incoming members by proximity to the
last sheet's upper edge before forming the existing bounded pair and single
choices. In the solver's rotated strip frame this is the placed shape's
rightmost extent. Keep area as a tie-breaker and retain stable equal ties,
the six same-item and six mixed-pair limits, sampling, repair caps, all work
budgets and full geometry/material acceptance checks. Prove that a smaller
part at the boundary outranks a larger interior part, that ties are stable,
and that disabled/expired behavior and useful existing exchanges remain.
Only after those checks should the unchanged paired quality pilot run.
This is a ranking hypothesis, not evidence of feasible improvement or a
reason to relax any H5 requirement.'''
source=root/'output/h5-material-profile-probe-20261018/candidate/crates/core/src/sheets/vstrip/exchange.rs'
s=source.read_text(encoding='utf-8');start=s.index('        incoming_keys.sort_by(');end=s.index('        let mut fill',start)
model=root/'output/h5-material-profile-probe-20261018/candidate/crates/core/src/sheets.rs'
review={'source':source.relative_to(root).as_posix(),'source_sha256':sha256(source.read_bytes()).hexdigest(),
    'current_sort':s[start:end],'model_source_sha256':sha256(model.read_bytes()).hexdigest(),
    'invocations':2,'attempts':25,'height_family_attempts':0,'height_family_visited_choices':0,
    'next_step':next_step,'production_changed':False,'quality_claim':False,'new_searches':0}
(out/'source-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
lines=['# Exchange coverage of height-setting parts — 2026-10-18','',
    '**None of 25 attempts selects the insert family that sets the credited sheet height.**','',
    'Two serial panel-hardware diagnostics use both kerfs, seed zero, 60 seconds',
    'and physical CCD0 CPU 8. The observer changes no decision, work charge or',
    'budget. Logging can change wall trajectories; these are diagnostic results,',
    'not a quality comparison with earlier runs.','',
    f"Both final layouts and both saved baselines validate. The independent",
    f"filled-outer audit checks {a['same_sheet_pairs']:,} same-sheet pairs at the unchanged",
    '1e-7 mm clearance tolerance. All original quantities, metrics, archive',
    'members/hashes, counters and source/binary/input guards verify. The separate',
    'rectangular-stock height calculation reproduces both baseline material',
    f"values exactly. The session takes {r['wall_seconds']/60:.3f} minutes.",'',
    '| Kerf mm | Attempts | Visited choice indices | First insert-pair index | Insert attempts | Credited sheet height mm |',
    '| --- | ---: | --- | ---: | ---: | ---: |']
for b in a['baselines']:
    lines.append(f"| {b['kerf_mm']} | {b['all_attempts']} | 0, 1, 12 | {b['matching_choice_indices'][0]} | {b['attempts_with_height_family']} | {b['credited_height']:.6f} |")
lines += ['', 'Outcomes: one exact-state rejection, eleven material-profile rejections',
    'and thirteen source-repair-or-expiry stops. Seventeen attempts are paired,',
    'including five mixed-item attempts. No exchange is accepted. The combined',
    'source outcome preserves the original short-circuit condition; it does not',
    'separate repair infeasibility from a time limit.','',next_step,'',
    'Coverage is by original part family. Zero insert-family attempts excludes',
    'the two height-setting insert copies; a positive family count would not',
    'by itself prove that those particular copies were chosen.','',
    '[Committed plan](h5-frontier-observer-20261018/plan.json),',
    '[archive verification](h5-frontier-observer-20261018/verification.json),',
    '[independent layouts and coverage](h5-frontier-observer-20261018/layout-checks.json),',
    '[all observed attempts](h5-frontier-observer-20261018/observed-exchanges.json),',
    '[source review](h5-frontier-observer-20261018/source-review.json).','',
    'Production, frozen inputs, the published preview and README claims remain',
    'unchanged. The failed 72-outcome pilot remains the quality evidence.',
    '**H2/H5 remain open; completed milestone weight is 60%.**','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
note=f'''**N4 height-setting part diagnosis, 2026-10-18:** [both final and baseline layouts validate](../benchmarks/results/h5-frontier-observer-20261018.md).
None of 25 attempts selects the insert family defining the credited sheet
height. Both traces visit only choices 0, 1 and 12; the insert pair at index
6 and insert singles from 73 are never visited. Twelve trials are rejected
early and thirteen stop at source repair or expiry. The independent audit
checks {a['same_sheet_pairs']:,} filled-outer pairs and reconstructs both material values
exactly. This supports qualifying a boundary-first member ranking under the
existing choice limits, budgets and full acceptance guards. It proves no
quality gain; H2/H5 remain open at 60%.
'''
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');start=s.index('**N4 height-setting part observation, 2026-10-18:**');end=s.index('**N4 material-profile rejection outcome, 2026-10-18:**',start)
p.write_text(s[:start]+note+'\n'+s[end:],encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note+'\n'+next_step+'\n')
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Diagnose untouched height-setting parts\n\n'+note.replace('../benchmarks/','benchmarks/')+'\n'+next_step+'\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-outcome.py');shutil.copyfile(root/'output/prepare_h5_frontier_finish.py',out/'prepare-finish.py')
print(json.dumps({'attempts':25,'height_family_attempts':0,'same_sheet_pairs':a['same_sheet_pairs'],'next':'Qualify boundary-first member ranking'}))
