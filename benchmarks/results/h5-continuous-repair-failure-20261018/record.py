"""Archive the failed functional candidate and its independently checked saved outcomes."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess,sys,zipfile
root=Path(__file__).resolve().parents[1];probe=root/'output/h5-continuous-repair-probe-20261018';out=root/'benchmarks/results/h5-continuous-repair-failure-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
plan=load(probe/'preparation.json');failure=load(probe/'failed-long-source/checks.json');source=load(probe/'reconstruction.json');repair=load(probe/'repair-checks/checks.json');regress=load(probe/'regression-checks/checks.json');red=load(probe/'before-continuous-repair/checks.json')
assert failure['passed_tests']==142 and failure['failed_tests']==3 and not failure['candidate_qualification_passed']
assert source['all_checks_passed'] and source['prior_tests_unchanged']==141 and source['unchanged_other_files']==154
assert repair['all_checks_passed'] and repair['public_CLI_checks']==2 and repair['independent_final_filled_outer_pairs']==300
assert regress['all_saved_output_checks_passed'] and regress['public_CLI_validations']==6 and regress['filled_outer_pairs']==54
assert red['expected_runtime_failure']
for name,checks in [('before-continuous-repair',red),('failed-long-source',failure)]:
 log='expected-failure.log' if name.startswith('before') else 'core-tests.log'
 assert digest(probe/name/log)==checks['log_sha256']
 assert digest(probe/name/'authored-tests.exe')==checks.get('binary_sha256',checks.get('test_binary_sha256'))
assert digest(probe/'core-tests.log')==failure['log_sha256']==repair['core_log_sha256']==regress['candidate_log_sha256']
for rel,expected in failure['source_sha256'].items():assert digest(probe/'candidate'/rel)==expected
sys.path.insert(0,str(root/'scripts'));from h2_import_audit import source_digest
assert source_digest()==plan['production_digest']
for arm,rows in plan['old_source_files'].items():
 for row in rows:
  assert digest(Path(plan['old_probe'])/arm/row['path'])==row['sha256']
  if not (arm=='candidate' and row['path'] in plan['changed_files']):assert digest(probe/arm/row['path'])==row['sha256']
assert not (probe/'build.json').exists() and not (probe/'candidate-observer.exe').exists()
followup=('Reject the direct-long-source allocation before any quality pilot. Preserve all three old assertions and their failed outputs. '
 'Giving the first attempted source repair the rest of its paired/single phase changes which opportunities remain reachable: the preceding candidate accepts the three saved authored swaps in three paired attempts, while this candidate stops with two paired and two single attempts and no acceptance. '
 'The original valid incumbent is retained in every failed case; the independent material totals are equal to the preceding accepted outcome. This is an opportunity regression, not observed geometry corruption or a worse material result on these authored cases. '
 'The source and counters are consistent with early proposals consuming the available paired phase, but exact per-proposal loss/time trajectories were not captured. Do not claim those unobserved details or soften the tests. '
 'Next retain the original short exchange phase and its accepted incumbent, then use any remaining existing relocation allowance for a bounded continuous repair phase. Additional accepted exchanges should require a strict material decrease relative to that incumbent. Keep the original total search deadline, validation reserve, filled-hole reservation, exact quantities, orientations, frozen sheets and rollback. '
 'Qualify both successful and unsuccessful fast phases, actual extended whole-job acceptance, rejection/expiry retaining the fast incumbent, and no acceptance after the deadline. Retain existing regressions, record stage counters honestly, and require complete functional qualification before a newly committed matched comparison. This is a new policy to test, not proof that H5 can pass.')
out.mkdir();files={p.relative_to(probe).as_posix():p for p in probe.rglob('*') if p.is_file()}
helpers=['prepare_h5_continuous_repair.py','check_h5_continuous_repair_red.py','apply_h5_continuous_repair.py','prepare_h5_continuous_repair_build.py','build_h5_continuous_repair.py','check_h5_continuous_repair_source.py','check_h5_continuous_repair_witness.py','freeze_h5_continuous_repair_failure.py','check_h5_continuous_repair_failed_source.py','check_h5_continuous_repair_failed_witness.py','check_h5_continuous_repair_regressions.py','record_h5_continuous_repair_failure.py']
for name in helpers:files['helpers/'+name]=root/'output'/name
inventory={n:{'bytes':p.stat().st_size,'sha256':digest(p)} for n,p in files.items()}
with zipfile.ZipFile(out/'raw.zip','x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in files.items():z.write(p,n)
with zipfile.ZipFile(out/'raw.zip') as z:
 assert z.testzip() is None and set(z.namelist())==set(inventory)
 for n,row in inventory.items():
  b=z.read(n);assert len(b)==row['bytes'] and sha256(b).hexdigest()==row['sha256']
write(out/'integrity.json',{'archive':'raw.zip','bytes':(out/'raw.zip').stat().st_size,'sha256':digest(out/'raw.zip'),'all_members_and_crc_verified':True,'members':inventory})
checks={'candidate_qualification_passed':False,'optimized_tests_passed':142,'optimized_tests_failed':3,'prior_test_bodies_unchanged':141,'new_tests':4,'new_tests_passed':4,'old_behavior_expected_failures':2,'old_behavior_preservation_passes':2,'all_original_sources_logs_and_binaries_preserved':True,'source_reconstruction_passed':True,'formatted_files_reconstructed':156,'unchanged_other_files':154,'saved_source_repair_CLI_checks':2,'regression_saved_output_CLI_checks':6,'independent_filled_outer_pairs':354,'source_proposal_expected_invalid':True,'source_repaired_output_valid':True,'three_regressions_keep_valid_exact_native_incumbents':True,'parent_and_candidate_material_equal_in_all_three_regressions':True,'prior_delay_explicitly_simulated':True,'no_authored_search_reruns':True,'no_quality_measurement_started':True,'no_strict_lint_or_observer_build_started':True,'production_unchanged':True,'H5_complete':False,'completed_weight_percent':60,'followup':followup}
write(out/'checks.json',checks)
for name in ['preparation.json','progress.json','build-failure.json','reconstruction.json','source-checks.json','candidate.patch']:shutil.copyfile(probe/name,out/name)
for sub,name in [('before-continuous-repair','expected-failure'),('failed-long-source','failed-candidate'),('repair-checks','repair-checks'),('regression-checks','regression-checks')]:shutil.copyfile(probe/sub/'checks.json',out/(name+'.json'))
write(out/'source-review.json',{'source_sha256':failure['source_sha256'],'old_exchange_cap_seconds':1.2,'new_exchange_deadline':'Existing ten-percent relocation deadline','receiver_allowance_formula_unchanged':True,'old_source_deadline':'Short pair end, capped at 0.4 seconds and half remaining phase','new_source_deadline':'Existing paired/single phase end less validation reserve','per_proposal_loss_and_time_observed':False,'followup':followup})
doc='''# Continuous source repair — failed functional qualification, 2026-10-18

**142 tests pass; three existing regressions fail. No quality benchmark starts.**

The [preceding continuation pilot](h5-exchange-chain-pilot-20261018.md) exercises
multiple exchanges but still fails all four mechanical material comparisons.
This isolated candidate uses the existing ten-percent relocation allowance
instead of capping the exchange window at 1.2 seconds. Receiver repair retains
its short allowance; one source repair can use the rest of the existing paired
or single phase, excluding the unchanged validation reserve. Overall search
time, proposal order, per-exchange acceptance and geometry guards are unchanged.
The internal source deadline is deliberately changed; this is not an unchanged
internal-budget experiment.

All 141 prior test bodies remain unchanged, with four new regressions. Against
the old allocation, the two new behavior tests fail and both preservation tests
pass. After applying the allocation, all four new tests pass, but three existing
tests fail: the larger-return positive case at seed 3, mixed-original-item positive
case at seed 0, and mixed-original-item frozen-prefix case at seed 0. The saved
preceding candidate accepts each required swap in three paired attempts. The new
candidate accepts none after two paired and two single attempts. Native exact
rollback assertions pass before the later opportunity assertions fail.

Six frozen-CLI checks and 54 independent filled-outer pair checks validate both
the current and preceding outputs of those three cases. Material is unchanged
between the accepted preceding result and current retained incumbent: 19,699.9994,
19,699.9994 and 22,300 mm² respectively. This is loss of required swap opportunities,
not observed geometry corruption or greater material use in these authored cases.

The new useful repair fixture starts with 25 overlapping 17 mm squares. A delay
of 300,000 charged evaluations explicitly simulates earlier receiver work; it is
not a wall-time observation or measured geometry work. Source repair starts at
0.541741 work seconds, after the former 0.401741 deadline, and actually clears the
overlaps by 0.588720848, before the full phase ends at 3.001741. The proposed input
is intentionally invalid and preserved. Its repaired output passes the frozen
CLI and all 300 filled-outer pair checks. The invalid-input CLI result also remains.
This qualifies the extended-time policy and an actual geometric repair only.

All 156 formatted source files reconstruct exactly; 154 are unchanged. Reversing
the two deadline adapters restores the preceding runtime exactly. The original
failed and expected-failure sources, binaries and logs remain. No assertion is
relaxed, no native search is repeated, and strict lint, experimental executable
build, public workflow checks and a quality pilot are not reached.

'''+followup+'''

Production, published preview and README claims remain unchanged. H2/H5 remain
open and completed milestone weight remains **60%**.

[Checks](h5-continuous-repair-failure-20261018/checks.json),
[three saved regressions](h5-continuous-repair-failure-20261018/regression-checks.json),
[actual source repair](h5-continuous-repair-failure-20261018/repair-checks.json),
[source reconstruction](h5-continuous-repair-failure-20261018/reconstruction.json),
[raw evidence](h5-continuous-repair-failure-20261018/raw.zip),
[archive integrity](h5-continuous-repair-failure-20261018/integrity.json).
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
prior=(root/'BENCHMARKS.md').read_bytes();assert prior==subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
note='''**N4 continuous-repair qualification failure, 2026-10-18:** the [isolated allocation](../benchmarks/results/h5-continuous-repair-failure-20261018.md)
passes 142 tests and fails three unchanged exchange regressions. It uses the
existing relocation allowance and lets each source repair use its phase remainder.
The new source-repair witness validates, but the old larger-return and mixed-item
examples lose required swaps. Six independent validations confirm valid retained
incumbents with the same material as the preceding accepted results. The authored
delay is explicitly simulated; no wall-time or quality claim follows. All failures
remain, no assertions change, and no quality pilot starts. Next preserve the
original short phase, then allow strictly improving continuous repairs with the
remaining allowance. Production is unchanged; H2/H5 remain open at 60%.
'''
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Continuous source repair fails functional qualification\n\n'+note.replace('../benchmarks/','benchmarks/'))
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');at=s.index('**N4 exchange-continuation outcome');p.write_text(s[:at]+note+'\n'+s[at:],encoding='utf-8',newline='\n')
append(root/'.gitattributes','\nbenchmarks/results/h5-continuous-repair-failure-20261018/** -text -whitespace\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record.py')
print(json.dumps({'preserved':True,'passed':142,'failed':3,'raw_members':len(inventory),'archive_bytes':(out/'raw.zip').stat().st_size,'new_quality_runs':0}))
