from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-balanced-stage-20261018'
load=lambda p:json.loads(p.read_bytes())
v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json');data=load(out/'observed-exchanges.json');s=data['summary']
assert v['all_original_archives_verified'] and v['all_traces_verified'] and v['valid']==4
assert audit['all_holes_reserved'] and audit['cases']==4
accepted=s['outcomes'].get('accepted',0)
source=root/'output/h5-balanced-group-probe-20261018/candidate/crates/core/src/sheets/vstrip.rs'
callsite=source.read_text(encoding='utf-8')
fragment='''                        if exchanged > 0
                            || (gaps
                                && timed("fill", || self.fill_gaps(&strip, &mut sep, shape)) > 0)
                            || timed("relocate", || {
                                self.relocate(&strip, &mut sep, shape, budget)
                            })? > 0'''
assert callsite.count(fragment)==1
followup='''Source inspection also confirms that accepting an exchange short-circuits
the following gap-fill and relocation calls in that window. The next isolated
change should test whether gap filling after an accepted exchange can use its
new arrangement, while preserving the total search limit and normal-mode
behavior. This identifies a missed execution path, not a measured quality gain.
'''
note=f'''**N4 pair-identity diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-balanced-stage-20261018.md).
There are {s['attempts']} attempts and {accepted} accepted exchanges, including
{s['paired_accepted']} pairs. {s['neutral_accepted']} accepted exchanges return the
same original part types and quantities as they take; per-sheet inventory is
unchanged in those cases, although poses may change. Immediate material falls
in {s['accepted_material_decreases']} accepted exchanges and last-sheet occupied
extent falls in {s['accepted_extent_decreases']}. These traces do not reconstruct
the earlier pilot or prove a later benefit/harm from rearrangement. Retained
proposal identities, losses, material and extent are preserved. The independent
filled-outer audit checks {audit['same_sheet_pairs']:,} pairs. No gate relaxation,
production change, reserved-file access or H5 credit. H2/H5 remain open at 60%.
{followup}
'''
marker='**N4 pair-identity diagnosis, 2026-10-18:**'
paths=[root/n for n in ['docs/STATUS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']]
assert all(marker not in p.read_text(encoding='utf-8') for p in paths)
assert not (out/'record-outcome.py').exists()
assert not (out/'control-flow-review.json').exists()
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
status=paths[0];text=status.read_text(encoding='utf-8');at=text.index('**N4 balanced-pair outcome, 2026-10-18:**')
status.write_text(text[:at]+note+'\n'+text[at:],encoding='utf-8',newline='\n')
for p in paths[1:]:append(p,'\n\n'+note)
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Balanced-pair identity diagnosis

[All four outputs validate](benchmarks/results/h5-balanced-stage-20261018.md).
{s['attempts']} attempts produce {accepted} accepted exchanges, including
{s['paired_accepted']} pairs. {s['neutral_accepted']} accepted exchanges preserve
the original part-type multiset on each sheet. Immediate material decreases in
{s['accepted_material_decreases']} accepted exchanges; last-sheet occupied extent
decreases in {s['accepted_extent_decreases']}. Same inventory does not imply same
poses, and these observations neither replay the failed pilot nor establish
the later benefit or harm of a rearrangement.

All source/input/binary guards, archive CRCs/member hashes, trace references,
four solver counters, original quantities, public exports and independently
recomputed metrics pass. The independent filled-outer audit verifies
{audit['same_sheet_pairs']:,} same-sheet pairs, with minimum clearance slack
{audit['minimum_clearance_slack_mm']:.12g} mm at the original 1e-7 mm tolerance.
Every failure and original limit remains; no production change or reserved
input access. H2/H5 remain open at 60%.

{followup}
''')
append(out.parent/(out.name+'.md'),f'''

The independent filled-outer audit additionally checks all
{audit['same_sheet_pairs']:,} same-sheet pairs, keeping hole interiors reserved.
Minimum clearance slack is {audit['minimum_clearance_slack_mm']:.12g} mm,
within the unchanged 1e-7 mm audit tolerance. No new searches are run.

## Next implementation question

{followup}
The [source review](h5-balanced-stage-20261018/control-flow-review.json) records
the exact call site and source hash. The original experiment is preserved.
''')
review={'source':source.relative_to(root).as_posix(),'source_sha256':sha256(source.read_bytes()).hexdigest(),
    'line':callsite[:callsite.index(fragment)].count('\n')+1,'exact_source':fragment,
    'finding':'Rust short-circuit OR skips gap filling and relocation when exchanged > 0. The filled flag is already set for this window.',
    'inference':'A separate candidate can test continuing gap filling after successful exchange. No claim that it will improve measured quality.',
    'production_changed':False,'new_searches':0}
(out/'control-flow-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps(s))
