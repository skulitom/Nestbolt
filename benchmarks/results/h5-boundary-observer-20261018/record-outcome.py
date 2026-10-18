"""Record verified physical boundary-copy coverage without a quality claim."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-boundary-observer-20261018'
load=lambda p:json.loads(p.read_bytes())
v=load(out/'verification.json');a=load(out/'layout-checks.json')
e=load(out/'observed-exchanges.json');r=load(out/'results.json')
assert v['valid']==2 and v['all_traces_verified'] and v['all_original_archives_verified']
assert a['all_checks_passed'] and a['choice_poses_match_validated_baseline_exactly']
summary=e['summary'];any_outcomes=Counter();all_outcomes=Counter()
for b in a['baselines']:
    any_outcomes.update(b['attempt_outcomes_with_actual_height_copy'])
    all_outcomes.update(b['attempt_outcomes_with_all_height_copies'])
count=a['attempts_with_actual_height_copy'];complete=a['attempts_with_all_height_copies']
assert count==sum(any_outcomes.values()) and complete==sum(all_outcomes.values())
finding=(f"{count} of {summary['attempts']} attempts select at least one actual part defining the credited sheet height; "
         f"{complete} select every part defining that height. {any_outcomes['accepted']} of the first group "
         f"and {all_outcomes['accepted']} of the second group are accepted.")
assert count==summary['attempts']==19 and complete==0
assert all(len(b['height_owners'])==2 and b['height_families']==['insert'] and not b['all_height_copies_choice_indices'] for b in a['baselines'])
followup='The boundary ordering reaches a real height-setting copy on every attempt, but the generated pair lists never include both height-setting inserts together. The current pair generators use nearest-neighbour partners before applying their caps. The next isolated hypothesis is to include the two highest-ranked source members as the first pair in the appropriate same-item or mixed-item list, remove an equivalent duplicate, and retain the six-plus-six caps and existing nearby alternatives within those caps. Preserve original pair anchor order, allowed orientations, all repair/deadline/work limits and every full acceptance check. Authored cases must fail under the current selection when closer lower neighbours displace the upper pair, then pass for same-item and mixed-item boundary pairs, without duplicates or cap overruns. All existing 126 tests and public/rejection checks must remain. Only then prepare a matched quality pilot. This is a proposal-coverage hypothesis: it does not prove that jointly moving those copies is feasible, necessary for every improvement or sufficient to meet H5. Eighteen repair-or-expiry stops also remain unexplained by this selection result. The six failed pilot material comparisons remain authoritative.'
lines=['# Exact boundary-copy selection diagnosis — 2026-10-18','',f'**{finding}**','',
    'Two serial panel-hardware diagnostics retain both kerfs, seed zero,',
    '60 seconds and physical CCD0 CPU 8. The separately qualified observer',
    'changes no decision, budget or work charge. Logging may alter wall',
    'trajectories; these observations are not a quality or speed comparison.','',
    f"Both final layouts and {a['baseline_layouts']} saved baselines independently validate.",
    f"All original quantities, archive/member hashes and source guards pass. The",
    f"filled-outer audit checks {a['same_sheet_pairs']:,} same-sheet pairs at the unchanged",
    '1e-7 mm tolerance. A separate rectangular-stock calculation reproduces',
    'every saved baseline material value exactly. Every observed choice matches',
    'unique physical members of that validated baseline exactly; no approximate',
    'pose matching or part-family inference identifies the boundary copies.',
    f"The session takes {r['wall_seconds']/60:.3f} minutes.",'',
    '| Kerf mm | Invocation | All attempts | Any actual top copy | Every top copy | Accepted with any / every |',
    '| --- | ---: | ---: | ---: | ---: | ---: |']
for b in a['baselines']:
    x=b['attempt_outcomes_with_actual_height_copy'];y=b['attempt_outcomes_with_all_height_copies']
    lines.append(f"| {b['kerf_mm']} | {b['invocation']} | {b['all_attempts']} | {b['attempts_with_actual_height_copy']} | {b['attempts_with_all_height_copies']} | {x.get('accepted',0)} / {y.get('accepted',0)} |")
lines+=['','| Outcome | All attempts | Any actual top copy | Every top copy |','| --- | ---: | ---: | ---: |']
for name in sorted(set(summary['outcomes'])|set(any_outcomes)|set(all_outcomes)):
    lines.append(f"| {name} | {summary['outcomes'].get(name,0)} | {any_outcomes[name]} | {all_outcomes[name]} |")
lines+=['','The combined source-repair-or-expiry outcome preserves the original',
    'short-circuit condition; it does not distinguish repair failure from the',
    'remaining deadline. Accepted exchanges still pass full validation and the',
    'original material guard. Acceptance counts do not prove final quality.','',followup,'',
    '[Committed plan](h5-boundary-observer-20261018/plan.json),',
    '[archive verification](h5-boundary-observer-20261018/verification.json),',
    '[independent geometry and exact copy coverage](h5-boundary-observer-20261018/layout-checks.json),',
    '[all observed attempts](h5-boundary-observer-20261018/observed-exchanges.json).','',
    'Production, reserved inputs, release assets and README claims remain',
    'unchanged. **H2/H5 remain open; completed milestone weight is 60%.**','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
note=f'''**N4 exact boundary-copy diagnosis, 2026-10-18:** [both diagnostic outcomes and every saved baseline validate](../benchmarks/results/h5-boundary-observer-20261018.md).
{finding} The independent audit checks {a['same_sheet_pairs']:,} filled-outer
pairs and reconstructs every material value exactly. Every selected physical
pose matches its baseline exactly. This identifies copy coverage, without
establishing final quality or packing feasibility. The six failed pilot
comparisons remain authoritative. H2/H5 remain open at 60%.
'''
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8')
start=s.index('**N4 exact boundary-copy observation, 2026-10-18:**')
end=s.index('**N4 boundary-priority outcome, 2026-10-18:**',start)
assert '**N4 exact boundary-copy diagnosis, 2026-10-18:**' not in s
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(path,value):
    with path.open('a',encoding='utf-8',newline='\n') as stream:stream.write(value)
p.write_text(s[:start]+note+'\n'+s[end:],encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Diagnose exact boundary-copy selection\n\n'+note.replace('../benchmarks/','benchmarks/')+'\n'+followup+'\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
review={'all_attempts':summary['attempts'],'attempts_with_actual_top_copy':count,
        'attempts_with_every_top_copy':complete,'outcomes_with_actual_top_copy':dict(any_outcomes),
        'outcomes_with_every_top_copy':dict(all_outcomes),'physical_choice_mapping_exact':True,
        'followup':followup,'quality_claim':False,'production_changed':False,'new_searches':0}
source=root/'output/h5-boundary-priority-probe-20261018/candidate/crates/core/src/sheets/vstrip/exchange.rs'
code=source.read_text(encoding='utf-8')
selectors=code[code.index('fn incoming_pairs('):code.index('fn same_original_inventory(')]
assert selectors.count('neighbours.into_iter().take(2)')==2
assert selectors.count('if pairs.len() == 6')==2
review.update(source=source.relative_to(root).as_posix(),source_sha256=sha256(source.read_bytes()).hexdigest(),
              current_pair_selectors=selectors,both_height_copies_absent_from_all_available_choices=True,
              all_observed_height_owner_counts=[len(b['height_owners']) for b in a['baselines']])
(out/'source-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
shutil.copyfile(root/'output/prepare_h5_boundary_observer_layout_checks.py',out/'prepare-layout-checks.py')
shutil.copyfile(root/'output/prepare_h5_boundary_observer_seal.py',out/'prepare-finish.py')
print(json.dumps({'finding':finding,'same_sheet_pairs':a['same_sheet_pairs'],'outcomes_with_actual_top_copy':dict(any_outcomes)}))
