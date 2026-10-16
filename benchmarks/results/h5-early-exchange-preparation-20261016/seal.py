"""Seal functional preparation for a separately measured early exchange trial."""
from hashlib import sha256
from pathlib import Path
import json
import shutil
import zipfile

root = Path(__file__).resolve().parents[1]
probe = root/'output/h5-early-exchange-probe'
out = root/'benchmarks/results/h5-early-exchange-preparation-20261016'
out.mkdir(exist_ok=False)
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()
def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')

preparation = load(probe/'preparation.json')
for row in preparation['production_files']:
    assert digest(root/row['path']) == row['sha256'], row['path']
    assert (probe/'baseline'/row['path']).read_bytes().replace(b'\r\n', b'\n') == (root/row['path']).read_bytes().replace(b'\r\n', b'\n')
baseline = {p.relative_to(probe/'baseline').as_posix(): p for p in (probe/'baseline').rglob('*') if p.is_file()}
candidate = {p.relative_to(probe/'candidate').as_posix(): p for p in (probe/'candidate').rglob('*') if p.is_file()}
changed = sorted(name for name in set(baseline)|set(candidate)
    if name not in baseline or name not in candidate or baseline[name].read_bytes().replace(b'\r\n', b'\n') != candidate[name].read_bytes().replace(b'\r\n', b'\n'))
assert changed == ['crates/core/src/sheets.rs', 'crates/core/src/sheets/vstrip.rs', 'crates/core/src/sheets/vstrip/exchange.rs'], changed
stage_names = ['baseline-format-v1', 'baseline-observer-build', 'candidate-format-v1',
    'candidate-exchange-tests-v1', 'candidate-exchange-tests-v2', 'candidate-observer-build',
    'candidate-core-release-tests', 'candidate-clippy', 'candidate-format-check']
stages = []
for name in stage_names:
    row = load(probe/(name+'.json'))
    assert digest(probe/(name+'.log')) == row['log_sha256']
    assert row['exit_code'] == (101 if name == 'candidate-exchange-tests-v1' else 0)
    stages.append(row)
assert '82 passed; 0 failed' in (probe/'candidate-core-release-tests.log').read_text(encoding='utf-8')
assert '7 passed; 0 failed' in (probe/'candidate-exchange-tests-v2.log').read_text(encoding='utf-8')
assert 'window exchange enabled=true budget=20 attempts=1 accepted=1 valid=true' in (probe/'candidate-exchange-tests-v2.log').read_text(encoding='utf-8')
public = load(probe/'public-checks-v1/checks.json')
assert public['all_checks_passed'] and public['normal_full_result_exact_except_elapsed_wall']
assert public['common_candidate_replay_exact_except_elapsed_wall'] and public['independent_metrics_exact']
assert len(list((probe/'public-checks-v1').glob('*/search.json'))) == 10
assert len(list((probe/'public-checks-v1').glob('*/report.json'))) == 4
for name, expected in load(probe/'public-checks-v1/completed-before-repair.json').items():
    assert digest(probe/'public-checks-v1'/name) == expected
binaries = {arm: {'sha256': digest(probe/('nestbolt-'+arm+'-observer.exe')),
                 'bytes': (probe/('nestbolt-'+arm+'-observer.exe')).stat().st_size} for arm in ['baseline', 'candidate']}
assert binaries['baseline']['sha256'] != binaries['candidate']['sha256']
for arm in binaries:
    assert binaries[arm]['sha256'] == load(probe/(arm+'-observer-build.json'))['binary_sha256']
assert (probe/'baseline/crates/core/examples/exchange_probe.rs').read_bytes() == (probe/'candidate/crates/core/examples/exchange_probe.rs').read_bytes()
checks = {'all_functional_checks_pass': True, 'baseline_product_commit': preparation['baseline_product_commit'],
    'isolated_candidate_only': True, 'root_production_sources_unchanged': True,
    'changed_source_paths': changed, 'stages': stages, 'observer_binaries': binaries,
    'full_optimized_core_tests': 82, 'focused_debug_tests': 7,
    'window_search_reaches_and_accepts_authored_exchange': True,
    'disabled_and_expired_paths_do_not_exchange': True, 'public_checks': public,
    'retained_setup_failures': ['Missing unchanged authored validation-job.json at first compile',
        'Public checker wrongly expected a nested cutting-report validation field; completed outcomes were hash-verified and reused after correcting that assertion'],
    'performance_measurement': False, 'held_out_geometry_read': False,
    'H5_complete': False, 'completed_milestone_weight_percent': 45,
    'next_step': 'A new committed matched mechanical/control pilot after current H4 quality/scale measurements finish; no integration from functional evidence.'}
write(out/'checks.json', checks)
shutil.copyfile(probe/'preparation.json', out/'preparation.json')
helpers = ['prepare_h5_early_exchange.py', 'run_h5_early_functional.py', 'check_h5_early_public.py',
           'repair_h5_early_public_checker.py', 'check_h5_early_public_v2.py', 'seal_h5_early_exchange.py']
(probe/'tools').mkdir()
for name in helpers:
    shutil.copyfile(root/'output'/name, probe/'tools'/name)
files = sorted(p for p in probe.rglob('*') if p.is_file())
inventory = {p.relative_to(root).as_posix(): {'sha256': digest(p), 'bytes': p.stat().st_size} for p in files}
archive = out/'raw.zip'
with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for path in files:
        z.write(path, path.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist()) == set(inventory)
    for name, record in inventory.items():
        data = z.read(name)
        assert len(data) == record['bytes'] and sha256(data).hexdigest() == record['sha256']
write(out/'integrity.json', {'archive': archive.relative_to(root).as_posix(), 'sha256': digest(archive),
    'bytes': archive.stat().st_size, 'members': inventory, 'crc_and_every_member_verified': True})
shutil.copyfile(__file__, out/'seal.py')
report = f'''# H5 early exchange: isolated functional preparation — 2026-10-16

**The new call path works on authored tests; material improvement is unmeasured.**
The [previous pilot](h5-exchange-pilot-v2-20261016.md) failed its material limits
and recorded no exchange proposals. [Two diagnostic paths](h5-exchange-path-20261016.md)
never reached its late hook. This candidate instead tries one exchange at the
first feasible window state, before gap filling can bypass relocation. It shares
the existing ten-percent relocation opportunity, capped at 1.2 seconds, and
removes the old late hook. No overall search budget increases.

The baseline is current product `7eba929`, including the finer exact score bound.
Only `sheets.rs`, `sheets/vstrip.rs` and the isolated `exchange.rs` differ.
Both workspaces and Cargo target directories are separate; neither release
source nor measured engines change. Identical observation drivers use the public
preparation/search API and write counters only after search.

[Checks](h5-early-exchange-preparation-20261016/checks.json) record seven focused
debug tests, all 82 optimized core tests, strict core/example lint and formatting.
The added full-window test has a small part that fits an earlier gap: enabled
exchange proposes and accepts once, while disabled and expired cases do neither.
All resulting incumbents independently validate without increasing material.
Existing tests retain frozen-sheet, reflection, stock-defect, refused larger
return, failed repair and nonmutation checks.

The public API checks preserve ten observer outcomes and four CLI comparisons
on the same authored two-sheet job, seeds 0/1 and a 20-unit fixed-work budget.
Normal full results match baseline except elapsed wall time. Candidate common
results repeat exactly on replay, and standalone metrics agree exactly. These
small public cases record zero exchange proposals; they establish API consistency,
not the mechanical pilot's improvement or reachability.

Two setup failures remain preserved: the first test compile lacked an unchanged
authored example fixture, and the first public checker used the wrong field in
the cutting report. The fixture was copied unchanged into both workspaces.
The checker repair verified all completed file hashes and exact successful
commands before reusing those outcomes; it did not rerun completed searches.
No product fix or scoring exception was made for either setup error.

Baseline observer SHA-256: `{binaries['baseline']['sha256']}`.
Candidate observer SHA-256: `{binaries['candidate']['sha256']}`.

The [raw archive](h5-early-exchange-preparation-20261016/raw.zip) retains both
source trees, drivers/binaries, all checks, original failures and helpers:
{len(inventory):,} members, {archive.stat().st_size:,} bytes,
SHA-256 `{digest(archive)}`. CRC, member sizes and every hash pass.

The candidate remains unintegrated. A separately committed matched pilot must
wait until the current release comparison and scale sequence finish. No H5
quality claim, held-out input, gate threshold, release content or milestone
weight changes; completion remains 45%.
'''
(out.parent/(out.name+'.md')).write_text(report, encoding='utf-8', newline='\n')
print(json.dumps({'all_functional_checks_pass': True, 'members': len(inventory),
    'bytes': archive.stat().st_size, 'sha256': digest(archive)}))
