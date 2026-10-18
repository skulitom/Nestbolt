"""Seal qualified joint repair, retaining unsuccessful implementations and audits."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess,sys,zipfile
root=Path(__file__).resolve().parents[1];probe=root/'output/h5-joint-repair-probe-20261018'
out=root/'benchmarks/results/h5-joint-repair-preparation-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
plan=load(probe/'policy-preparation.json');build=load(probe/'build.json');source=load(probe/'source-checks.json')
joint=load(probe/'joint-checks/checks.json');public=load(probe/'public-checks/checks.json');holes=load(probe/'public-checks/filled-outer-audit.json')
assert all(x['all_checks_passed'] for x in [build,source,joint,public,holes])
assert '165 passed; 0 failed' in (probe/'core-tests.log').read_text(encoding='utf-8')
assert source['all_157_prior_test_bodies_unchanged'] and source['new_policy_tests']==8
assert joint['saved_joint_pair_outcomes']==joint['saved_joint_policy_outcomes']==8 and joint['public_CLI_checks']==32
assert public['observer_outcomes']==10 and public['CLI_cross_checks']==4 and holes['holes_reserved'] and holes['common_outcomes']==6
assert load(probe/'before-joint-repair/checks.json')['expected_runtime_failure']
assert load(probe/'before-source-lowering/independent-checks/checks.json')['tests_still_fail_original_targets']
assert load(probe/'before-rollback-fixture-correction/independent-checks/checks.json')['actual_strict_material_gain_confirmed']
assert load(probe/'rollback-fixture-check/checks.json')['witness_passed']
sys.path.insert(0,str(root/'scripts'));from h2_import_audit import source_digest
assert source_digest()==plan['production_digest']
for rel,expected in build['source_sha256'].items():assert digest(probe/'candidate'/rel)==expected
for arm,expected in build['binaries'].items():assert digest(probe/(arm+'-observer.exe'))==expected
for path,expected in load(probe/'public-checks/plan.json')['guards'].items():assert digest(root/path)==expected
for row in build['stages']:assert digest(probe/(row['label']+'.log'))==row['log_sha256']
native=next(r for r in build['stages'] if r['label']=='core-tests');assert native['log_sha256']==joint['core_log_sha256']
binaries=list((Path(plan['target'])/'release/deps').glob('nestbolt_core-*.exe'));assert len(binaries)==1
shutil.copyfile(binaries[0],probe/'final-authored-tests.exe')
write(probe/'final-test-binary.json',{'sha256':digest(binaries[0]),'core_log_sha256':native['log_sha256']})
out.mkdir()
files={p.relative_to(probe).as_posix():p for p in sorted(probe.rglob('*')) if p.is_file()}
helpers=['prepare_h5_joint_repair.py','check_h5_joint_repair_initial.py','check_h5_joint_repair_initial_geometry.py',
 'prepare_h5_joint_repair_red.py','check_h5_joint_repair_red.py','apply_h5_joint_repair.py','apply_h5_joint_lowering.py',
 'build_h5_joint_repair.py','check_h5_joint_repair_source.py','check_h5_joint_unlowered_failure.py',
 'check_h5_joint_rollback_assumption.py','check_h5_joint_rollback_fixture.py','check_h5_joint_repair_witness.py',
 'check_h5_joint_repair_public.py','audit_h5_joint_repair_public.py','seal_h5_joint_repair.py']
for name in helpers:files['helpers/'+name]=root/'output'/name
inventory={n:{'sha256':digest(p),'bytes':p.stat().st_size} for n,p in files.items()};archive=out/'raw.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in files.items():z.write(p,n)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None and set(z.namelist())==set(inventory)
 for n,row in inventory.items():
  b=z.read(n);assert len(b)==row['bytes'] and sha256(b).hexdigest()==row['sha256']
write(out/'integrity.json',{'archive':'raw.zip','bytes':archive.stat().st_size,'sha256':digest(archive),'all_members_and_crc_verified':True,'members':inventory})
for src,dst in [('policy-preparation.json','preparation.json'),('build.json','build.json'),('source-checks.json','source-checks.json'),
 ('candidate.patch','candidate.patch'),('rollback-fixture-provenance.json','rollback-fixture-provenance.json'),('joint-checks/checks.json','joint-checks.json'),('public-checks/checks.json','public-checks.json'),
 ('public-checks/filled-outer-audit.json','public-filled-outers.json'),('before-source-lowering/independent-checks/checks.json','unlowered-failures.json'),
 ('before-rollback-fixture-correction/independent-checks/checks.json','rollback-assumption-failure.json'),('final-test-binary.json','final-test-binary.json')]:
 shutil.copyfile(probe/src,out/dst)
checks={'all_functional_checks_pass':True,'optimized_core_tests_passed':165,'prior_tests_unchanged':157,'new_policy_tests':8,
 'original_short_phase_and_total_deadline_retained':True,'only_selected_pair_can_move':True,'exact_source_crop_rechecked':True,
 'bounded_source_lowering_keeps_orientation_reflection_and_deadline':True,'joint_sequences_require_final_strict_gain':True,
 'joint_accepted_count_restored_on_rollback':True,'old_native_witnesses_exact':True,'source_reconstruction_passed':True,
 'native_CLI_checks':32,'native_filled_outer_pairs':joint['filled_outer_pairs'],'public_outcomes':10,'public_CLI_cross_checks':4,
 'public_common_hole_reservation_checks':6,'public_filled_outer_pairs':holes['filled_outer_pairs'],
 'strict_lint_passed':True,'observer_build_passed':True,'all_failures_preserved':True,'production_unchanged':True,
 'quality_measurement_started':False,'pilot_plan_and_harness_still_required':True,'H5_complete':False,'completed_weight_percent':60}
write(out/'checks.json',checks)
note=f'''**N4 joint-repair qualification, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-joint-repair-preparation-20261018.md)
retains the short phase, then repairs only the selected receiver/source pair
within the remaining original allowance. It rechecks the exact cropped source,
lowers parts into freed space with existing bounded sampling, and commits a joint sequence only
after strict final whole-job material improvement. Incomplete sequences restore
their layout, tracker and accepted counters. All 165 native tests pass, including
157 unchanged prior tests and eight new policy tests. Independent validation covers
32 saved native layouts and {joint['filled_outer_pairs']:,} filled-outer pairs;
ten public outcomes, four CLI comparisons and six common-mode hole-reservation
checks pass. Source reconstruction, exact prior witnesses, lint and build pass.
The two insufficient-gain repairs, one newly invalid flat-fixture assumption,
initial compile error and audit error remain preserved. The rollback fixture uses the previously validated compacted output and
retains every assertion; runtime, guards and earlier tests are unchanged
by that fixture correction. A new committed pilot plan and harness checks are
still required before quality measurement. Production is unchanged; H2/H5 remain
open at 60%.
'''
doc=f'''# Joint repair and source lowering — qualification, 2026-10-18

The [preceding 72-run pilot](h5-assignment-bridge-pilot-20261018.md) fails all four
mechanical material limits. The [authored witness](h5-joint-repair-witness-20261018.md)
establishes a fixed-assignment source that cannot fit, but permits an actual valid
joint repair when an extra part migrates. This candidate makes that repair
available to directed exchange proposals. It is isolated; production is unchanged.

## Behavior and guards

The original short exchange phase runs first. The remaining original relocation
allowance uses a temporary strip containing only the selected receiver and source.
Other active sheets are absent and cannot move; the earlier frozen prefix remains
untouched. Original item geometry, rotations, reflection, stock walls/defects and
the current source crop carry into that strip. Both outputs are then rechecked in
their exact single-sheet containers. This also enforces a crop too thin to create
the normal stable boundary blocker.

After both outputs validate, the existing bounded free-pose routine lowers source
members into newly freed space, highest first. It keeps each current orientation
and reflection, uses the same collision guards and stays within the original
deadline. Both before and after this step, charged geometry work and expiry are
checked. Final whole-job validation and material comparison remain authoritative.
Material-flat steps need canonical source-area descent and stay provisional until
a strict whole-job gain. Failure, expiry or the shared four-step cap restores the
last committed layout, matching tracker and accepted counts, including the new
joint accepted counter. Attempt/repair diagnostics remain visible.

Pair-selection counters describe the initial proposal; joint repair can move
additional members. Completed pair repair does not by itself mean the whole job
was accepted, or that each intermediate step improved material.

## Evidence and retained failures

The old-behavior contract run passes three tests and fails the five intended
missing-capability checks. The thin-crop failure guards the new helper API; it
does not establish a production crop bug, since the existing path already used
a cropped source container. An earlier attempt did not compile because two newly
authored fixture references used descriptive names; no search ran. Its logs and
sources remain. The harness also copied the prior witness executable on that
failed build; its separate notice identifies that executable as stale, never as
the failed compilation's output. Later harness records require actual test startup.

The first joint implementation passes 163/165 tests. Its two failed-target layouts
are valid and preserve the prefix/intervening sheet, but save only 29.4281 mm²:
the returned part remains raised. Four public CLI validations and ten filled-outer
pair checks preserve that diagnosis. Source lowering fixes those targets without
weakening their assertions.

The next run passes 164/165 tests. The remaining failure is a new rollback fixture
whose previously flat first move now saves 99.9452 mm² because source lowering
works. Committing that gain is correct. Two independent CLI checks and twelve
filled-outer pairs confirm it. An attempted hand-positioned lower-boundary fixture fails the internal collision
check and is retained. The corrected fixture uses the exact saved, independently
validated compacted output as its starting layout; its provenance is hashed.
All assertions and runtime code remain unchanged. The focused rollback test
passes, followed by all **165 optimized native tests**. All **157 prior test
bodies** are unchanged. The original authored-witness audit error is also retained.

Sixteen saved new outcomes receive **32 independent public CLI validations** and
**{joint['filled_outer_pairs']:,} filled-outer pair checks**. Coverage includes actual extra-member
migration, nonadjacent selected sheets with a fixed middle and prefix, failed
repairs, disabled/expired/tiny budgets, thin crop rejection, successful acceptance,
exact replay, provisional rollback and preservation of fast-phase gains. Every
previously checked native witness is present exactly before its earlier evidence
is reused. Source reconstruction verifies all 157 files, with 153 unrelated files
unchanged and one authored saved-layout fixture added. Strict lint and the isolated observer build pass.

Ten public fixed-work outcomes and four baseline CLI comparisons pass. Ordinary
mode is exact apart from elapsed wall time, and common candidate replay is exact.
Six common outputs with real source holes pass an independent filled-outer audit
of **{holes['filled_outer_pairs']:,} pairs**, at the unchanged 1e-7 mm numerical tolerance. The
public workflow actually reaches joint repair; no hole interior is used.

Original sources, binaries, logs, failures, corrected fixture, snapshots and
auditors are archived with verified member hashes and ZIP CRCs. These checks
establish functionality and preservation, not better development-job quality.

## Next decision

Prepare and commit a matched development-pilot plan, verify the unchanged scoring
and execution harness, and retain every outcome. Use the original 60-second
budget, job inputs, seeds and material limit. Only a passing pilot can justify
opening the full original 13-job H5 comparison. No production integration, new
release, held-out access, threshold change or H5 completion follows this report.

[Native/build checks](h5-joint-repair-preparation-20261018/build.json),
[saved-layout checks](h5-joint-repair-preparation-20261018/joint-checks.json),
[source audit](h5-joint-repair-preparation-20261018/source-checks.json),
[public checks](h5-joint-repair-preparation-20261018/public-checks.json),
[filled-outer audit](h5-joint-repair-preparation-20261018/public-filled-outers.json),
[archive integrity](h5-joint-repair-preparation-20261018/integrity.json).
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Joint repair qualification\n\n'+note.replace('../benchmarks/','benchmarks/'))
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 joint-repair witness, 2026-10-18:**'
assert s.count(needle)==1 and '**N4 joint-repair qualification, 2026-10-18:**' not in s
a=s.index(needle);b=s.index('**N4 ',a+1);p.write_text(s[:a]+note+'\n'+s[b:],encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
p=root/'.gitattributes';line='benchmarks/results/h5-joint-repair-preparation-20261018/** -text -whitespace\n';assert line not in p.read_text(encoding='utf-8');append(p,line)
shutil.copyfile(__file__,out/'seal.py')
print(json.dumps({'sealed':True,'members':len(inventory),'bytes':archive.stat().st_size,'core_tests':165,
 'native_CLI_checks':32,'public_outcomes':10,'quality_measurement_started':False}))
