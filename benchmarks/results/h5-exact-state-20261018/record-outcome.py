"""Record exact-state results without inferring benefit from equal inventory."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exact-state-20261018'
load=lambda p:json.loads(p.read_bytes())
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
v=load(out/'verification.json');audit=load(out/'layout-checks.json');ex=load(out/'observed-exchanges.json');r=load(out/'results.json')
assert v['all_original_archives_verified'] and v['all_traces_verified'] and v['valid']==2 and audit['all_checks_passed']
assert audit['neutral_pairs']==ex['summary']['outcomes'].get('neutral_inventory_rejected',0)
exact=audit['internal_exact_pairs'];total=audit['neutral_pairs'];public=audit['public_exact_pairs']
if exact:
    conclusion=f'{exact} of {total} neutral trials exactly preserve the complete internal physical state.'
    next_step='''An exact-state early rejection now has an observed target, but its impact on
search quality is unproven. A separate candidate may reject only a complete
exact-state match before repeated validation, preserving shared container and
original-item identity, full transform bits, reflection and multiplicity.
Every changed state and every accepted exchange must retain the original
full geometry/material checks. Qualify the predicate and early branch with
authored regressions, preserve expired/disabled behavior and rollback, and
repeat the existing paired development protocol only for that changed build.
Do not infer a quality gain or promote it from these diagnostic timings.'''
else:
    conclusion=f'None of the {total} neutral trials has an exact internal state match.'
    next_step='''Do not implement the proposed exact-state early rejection on this evidence:
it has no observed target in the failing panel case. A false bitwise result
alone does not establish a meaningful geometry difference; public exactness
is reported separately. Do not broaden equality with tolerances or skip the
validator on equal inventory/material. The remaining material problem still
requires a packing/search change, with full independent checks and the
original paired quality protocol. The existing failed pilot remains the
quality evidence; these observations neither close H5 nor justify integration.'''
source=root/'output/h5-exact-state-20261018/workspace/crates/core/src/sheets/vstrip/exchange.rs'
write(out/'source-review.json',{'source':str(source.relative_to(root)),'source_sha256':sha256(source.read_bytes()).hexdigest(),
    'conclusion':conclusion,'next_step':next_step,'exact_internal_neutral_pairs':exact,'neutral_pairs':total,
    'exact_public_pairs':public,'production_changed':False,'quality_claim':False,'new_searches':0})
lines=['# Exact-state observations on panel hardware — 2026-10-18','',f'**{conclusion}**','',
    'Two serial seed-zero, 60-second panel-hardware diagnostics use kerfs 0.2',
    'and 1.5 mm on physical CCD0 CPU 8. All original decisions, repairs, full',
    'validation and strict material guards remain. Logging can alter wall-clock',
    'trajectories; this is neither a quality comparison nor a speedup claim.','',
    f"Both final layouts and all {audit['saved_layouts']} saved intermediate layouts validate.",
    f"Independent filled-outer checks cover {audit['same_sheet_pairs']:,} same-sheet pairs",
    'with the unchanged 1e-7 mm clearance tolerance. Every original quantity,',
    'archive member/hash, trace counter, metric and source/binary/input guard',
    f"verifies. The session takes {r['wall_seconds']/60:.3f} minutes.",'',
    '| Kerf mm | Attempts | Neutral rejections | Exact internal state | Neutral validation seconds | Identity check seconds |',
    '| --- | ---: | ---: | ---: | ---: | ---: |']
for t in audit['timings']:
    lines.append(f"| {t['kerf_mm']} | {t['all_attempts']} | {t['neutral_rejections']} | {t['exact_state_true']} | {t['neutral_validation_seconds']:.7f} | {t['identity_seconds']:.7f} |")
lines += ['',f'{public} of {total} saved neutral pairs have exactly equal public pose multisets.',
    'The comparison ignores copy indices only within the same original part ID,',
    'retaining sheet, full pose and multiplicity. The internal predicate also',
    'requires the same immutable model/container objects and exact f32 bits.',
    'Signed zero and equivalent angles may therefore yield a conservative false',
    'result. Equal public poses are not substituted for the internal predicate.','',
    '| Kerf mm | Attempt | Exact internal | Exact public | Unmatched incumbent/trial public poses |',
    '| --- | ---: | --- | --- | ---: |']
for p in audit['pairs']:
    lines.append(f"| {p['kerf_mm']} | {p['attempt']} | {p['internal_exact_state']} | {p['public_pose_multisets_exact']} | {p['public_incumbent_unmatched_poses']} / {p['public_trial_unmatched_poses']} |")
lines += ['',next_step,'',
    '[Committed plan](h5-exact-state-20261018/plan.json),',
    '[archive and metric verification](h5-exact-state-20261018/verification.json),',
    '[every saved layout and independent check](h5-exact-state-20261018/layout-checks.json),',
    '[all attempts](h5-exact-state-20261018/observed-exchanges.json),',
    '[source review](h5-exact-state-20261018/source-review.json).','',
    '**H2/H5 remain open; completed weight stays 60%.** Production, reserved',
    'inputs and earlier failed results remain unchanged. No new release is',
    'warranted by this diagnostic; the existing preview and READMEs stay current.','',
    'The first independent-audit helper looked up before-material on an attempt',
    'instead of its enclosing trace and stopped before checking any saved layout.',
    'Its failed source and result remain preserved. The corrected helper uses',
    'the same recorded inputs and tolerances; no search was rerun. See',
    '[audit repair](h5-exact-state-20261018/audit-repair.json).','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
note=f'''**N4 exact-state diagnosis, 2026-10-18:** [both final and all {audit['saved_layouts']} saved layouts validate](../benchmarks/results/h5-exact-state-20261018.md).
{conclusion}
Independent filled-outer checks cover {audit['same_sheet_pairs']:,} same-sheet pairs.
Public pose multisets match in {public}/{total} pairs; exact internal comparison also
requires shared model/container identity and full float bits. All original
validators and decisions remain. This diagnostic establishes no quality gain;
the five failed pilot comparisons remain authoritative. H2/H5 stay open at 60%.
'''
status=root/'docs/STATUS.md';text=status.read_text(encoding='utf-8');begin=text.index('**N4 exact-state diagnosis preparation, 2026-10-18:**');end=text.index('**N4 larger-return diagnosis, 2026-10-18:**',begin)
status.write_text(text[:begin]+note+'\n'+text[end:],encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note+'\n'+next_step+'\n')
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Observe exact physical states of neutral panel trials\n\n'+note.replace('../benchmarks/','benchmarks/')+'\n'+next_step+'\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-outcome.py')
print(json.dumps({'conclusion':conclusion,'public_exact_pairs':public,'saved_layouts':audit['saved_layouts'],'filled_outer_pairs':audit['same_sheet_pairs']}))
