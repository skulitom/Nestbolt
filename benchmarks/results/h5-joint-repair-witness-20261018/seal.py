"""Preserve the unchanged-runtime joint-repair witness and its first audit failure."""
from pathlib import Path
from hashlib import sha256
import difflib,json,shutil,subprocess,sys,zipfile
root=Path(__file__).resolve().parents[1];probe=root/'output/h5-joint-repair-probe-20261018'
out=root/'benchmarks/results/h5-joint-repair-witness-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
plan=load(probe/'preparation.json');native=load(probe/'initial-witness/checks.json');audit=load(probe/'initial-geometry/checks.json')
assert native['witness_passed'] and audit['all_saved_outcome_checks_passed'] and audit['actual_useful_joint_repair_observed']
assert audit['public_CLI_checks']==5 and audit['valid_outputs']==3 and audit['filled_outer_pairs']==8
assert digest(probe/'initial-witness/witness.log')==native['log_sha256']==audit['native_log_sha256']
assert digest(probe/'initial-witness/authored-tests.exe')==native['binary_sha256']
failure=load(probe/'initial-geometry-first-check-failure/failure.json')
assert digest(probe/'initial-geometry-first-check-failure/failed-check.py')==failure['failed_checker_sha256']
assert native['log_sha256']==failure['native_log_sha256']
sys.path.insert(0,str(root/'scripts'));from h2_import_audit import source_digest
assert source_digest()==plan['production_digest']
rel='crates/core/src/sheets/vstrip/exchange.rs';old=Path(plan['old_probe'])
before=(old/'candidate'/rel).read_text(encoding='utf-8');after=(probe/'candidate'/rel).read_text(encoding='utf-8')
assert after.startswith(before[:before.rindex('\n}')])
assert before.count('#[test]')+1==after.count('#[test]')
assert after.split('#[cfg(test)]\nmod tests',1)[0]==before.split('#[cfg(test)]\nmod tests',1)[0]
out.mkdir()
patch=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
(out/'witness.patch').write_text(patch,encoding='utf-8',newline='\n')
files={p.relative_to(probe).as_posix():p for p in sorted(probe.rglob('*')) if p.is_file()}
for name in ['prepare_h5_joint_repair.py','check_h5_joint_repair_initial.py','check_h5_joint_repair_initial_geometry.py','seal_h5_joint_repair_witness.py']:
 files['helpers/'+name]=root/'output'/name
inventory={n:{'bytes':p.stat().st_size,'sha256':digest(p)} for n,p in files.items()}
archive=out/'raw.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in files.items():z.write(p,n)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None and set(z.namelist())==set(inventory)
 for n,row in inventory.items():
  b=z.read(n);assert len(b)==row['bytes'] and sha256(b).hexdigest()==row['sha256']
write(out/'integrity.json',{'archive':'raw.zip','bytes':archive.stat().st_size,'sha256':digest(archive),'all_members_and_crc_verified':True,'members':inventory})
for src,dst in [('preparation.json','preparation.json'),('initial-witness/checks.json','native-checks.json'),
                ('initial-geometry/checks.json','independent-checks.json'),('initial-geometry-first-check-failure/failure.json','first-audit-failure.json')]:
 shutil.copyfile(probe/src,out/dst)
checks={'authored_native_witness_passed':True,'runtime_unchanged':True,'prior_test_bodies_unchanged':156,
 'prior_tests_rerun':False,'new_test_count':1,'public_CLI_checks':5,'valid_outputs':3,'expected_invalid_outputs':2,
 'filled_outer_pairs':8,'original_frozen_prefix_preserved_exactly':True,'first_audit_failure_preserved':True,
 'same_saved_native_search_used_for_corrected_audit':True,'production_unchanged':True,'benchmark_searches':0,
 'new_policy_implemented':False,'quality_claim':False,'H5_complete':False,'completed_weight_percent':60}
write(out/'checks.json',checks)
note='''**N4 joint-repair witness, 2026-10-18:** the [unchanged-runtime authored test](../benchmarks/results/h5-joint-repair-witness-20261018.md)
shows why repairing fixed sheet assignments can fail: two source rectangles cannot
fit together even in the full usable sheet. The existing separator finds a valid
joint rearrangement by moving the extra source part to the receiver. Material
drops from 29,699.9994 to 28,799.9993 mm², with the earlier sheet exactly fixed.
Five independent CLI checks retain three valid outputs and two expected invalid
proposals; eight filled-outer pairs pass. One audit error compared authored f64
and converted f32 coordinates as byte-identical; it is preserved, and the corrected
audit reuses the same saved outputs without changing tolerance or rerunning search.
All runtime code and 156 prior test bodies remain unchanged; only the new test ran.
This proves a constructed case, not policy selection or development-job quality.
Next qualify a bounded joint-repair policy before any new matched pilot. H2/H5
remain open at 60%.
'''
doc='''# Joint repair across two sheets — authored witness, 2026-10-18

The [assignment-bridge pilot](h5-assignment-bridge-pilot-20261018.md) misses all four
mechanical material limits. Some saved source inventories cannot meet the target
area without changing membership. This fixture tests one specific limitation of
repairing the receiver and source separately, using the existing separator.

## Construction and actual result

All stock is 100 × 100 mm, edge clearance is 1 mm, part clearance is 0.2 mm,
rotation is fixed at zero, and mirroring is forbidden. An earlier sheet is fixed.
The receiver initially holds a 20 × 94 mm filler and a 60 × 85 mm return part;
the source holds a 30 × 94 mm incoming part and a 40 × 50 mm extra part.

An authored proposal swaps incoming and return parts. Its receiver is valid, but
the source now contains two overlapping rectangles. Their widths plus clearance
total 100.2 mm and their heights plus clearance total 135.2 mm. Both exceed the
full sheet's 98 mm usable dimension. Two axis-aligned rectangles must separate
along at least one axis, so this fixed source inventory cannot fit. This is a
proof about these rectangles and this sheet, not about whole development jobs.

With seed 0 and a maximum 12 charged-work-second allowance per repair, the
source-only separator returns nonzero loss and an invalid layout. A hand-authored
joint rearrangement is valid. The actual joint separator also finds a valid
rearrangement: the extra part migrates to the receiver and the source retains the
return part. Material changes from **29,699.9994 to 28,799.9993 mm²**. The fixed
prefix is exactly unchanged; quantities, permitted poses and boundaries validate.
The joint call ends before its deadline. The allowance is a functional-test
bound, not a wall-time speed comparison or a new production budget.

The incoming/return proposal is deliberately constructed. This test does not
establish that current proposal selection would choose it, or that the current
exchange policy has no other route. The normal window separator already supports
cross-sheet sampling; the gap demonstrated here is fixed membership during
directed-proposal repair. No runtime policy has changed.

## Independent checks and retained failure

The frozen public CLI validates the before layout, hand-authored feasible layout
and actual joint output, and rejects the overlapping proposal and source-only
repair output. Shapely independently checks all eight same-sheet filled-outer
pairs across valid outputs, stock boundaries, quantities and allowed orientations.
All four runtime layouts retain an exactly identical earlier-sheet placement.
The hand-authored prefix is checked separately against its exact [2, 2] pose.

The first audit mistakenly required byte equality between that authored f64 pose
and the solver's f32 round-trip. Its failed checker, saved CLI outputs and failure
record remain in the raw archive. The corrected audit reuses the original native
outputs, retains exact equality among runtime poses, and changes no geometry
tolerance. There was no search rerun or changed fixture.

One optimized native test passes; 156 existing tests are filtered out and their
bodies are verified unchanged, together with every runtime source file. This
witness does not claim a new complete-suite qualification. The exact binary,
formatted sources, logs, helper scripts, original failure and corrected checks
are archived with member hashes and verified ZIP CRCs.

## Next decision

Qualify a distinct joint-repair policy while retaining the original short phase,
overall deadline, validation reserve and strict final whole-job acceptance.
Repair only the two selected sheets in a temporary two-sheet container so an
unselected active sheet cannot move. Preserve the original cropped source boundary,
stock walls/defects, original item models and all earlier sheets. Failure, expiry
or non-improvement must leave the incumbent intact. Proposal counters must not
claim that only the initially selected parts moved during joint repair.

Require positive and failed joint repairs, expiry, nonadjacent selected sheets,
fixed intervening sheets, quantities/poses, reserved holes, exact replay and old
fast-phase behavior before any new matched development comparison. A hand-authored
success is not evidence of improved real-job quality. Production, releases,
reserved inputs, thresholds and completed milestone weight remain unchanged.

[Native check](h5-joint-repair-witness-20261018/native-checks.json),
[independent checks](h5-joint-repair-witness-20261018/independent-checks.json),
[first audit failure](h5-joint-repair-witness-20261018/first-audit-failure.json),
[source patch](h5-joint-repair-witness-20261018/witness.patch),
[archive integrity](h5-joint-repair-witness-20261018/integrity.json).
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Joint-repair authored witness\n\n'+note.replace('../benchmarks/','benchmarks/'))
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 assignment-bridge outcome, 2026-10-18:**'
assert s.count(needle)==1 and '**N4 joint-repair witness, 2026-10-18:**' not in s
p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
p=root/'.gitattributes';line='benchmarks/results/h5-joint-repair-witness-20261018/** -text -whitespace\n'
assert line not in p.read_text(encoding='utf-8');append(p,line)
shutil.copyfile(__file__,out/'seal.py')
print(json.dumps({'sealed':True,'archive_members':len(inventory),'archive_bytes':archive.stat().st_size,
 'runtime_unchanged':True,'new_tests_passed':1,'quality_claim':False}))
