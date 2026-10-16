"""Check the isolated warning candidate on all 56 training native projects."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import ast
import difflib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'
BASE = ROOT/'benchmarks/results'
OUT = BASE/'h2-native-warning-probe-20261016-v3'
PROBE = ROOT/'output/ci-curve-probe'
EXE = PROBE/'target/debug/nestbolt-ci-curve-probe.exe'
REVIEW = BASE/'h2-native-warning-review-20261015'
ARCHIVE = BASE/'h3-missing-layer-native-20261015/raw.zip'
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')

def guards():
    sys.path.insert(0, str(ROOT/'scripts'))
    import h4_full_matrix as full
    current = full.guards(full.cases())
    assert current == load(BASE/'h4-full-development-20261015/plan.json')['guards']
    return current

def run(command, stem):
    p = subprocess.run([sys.executable, str(ROOT/'output/ccd1.py'), *command], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1800)
    (OUT/(stem+'-stdout.log')).write_bytes(p.stdout)
    (OUT/(stem+'-stderr.log')).write_bytes(p.stderr)
    return {'command': command, 'exit_code': p.returncode}

def package_set(path):
    data = tomllib.loads(path.read_text(encoding='utf-8'))
    return {(p['name'], p['version'], p.get('source'), p.get('checksum'))
            for p in data['package'] if 'source' in p}

assert digest(CORPUS/'manifest.json') == '02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
manifest = load(CORPUS/'manifest.json')
training = {r['path']: r for r in manifest['files'] if r['split']=='training'
            and Path(r['path']).suffix in ['.lbrn', '.lbrn2']}
previous = load(REVIEW/'checks.json')
assert set(training) == {r['path'] for r in previous['rows']} and len(training) == 56
assert digest(ARCHIVE) == previous['archive_sha256']
inventory = load(ARCHIVE.with_name('integrity.json'))
assert inventory['sha256'] == previous['archive_sha256']
assert package_set(PROBE/'Cargo.lock') <= package_set(ROOT/'Cargo.lock')
before = guards()
OUT.mkdir()
shutil.copyfile(__file__, OUT/'audit.py')
shutil.copyfile(ROOT/'output/native_warning_probe_audit_preflight_1.py', OUT/'preflight-1-audit.py')
write(OUT/'preflight-1.json', {
    'command':['python','output/native_warning_probe_audit.py'], 'exit_code':1,
    'failure':'Full third-party package-set equality failed before output creation or corpus imports.',
    'diagnosis':'Cargo pruned unused CLI/MCP packages from the isolated workspace lock. No candidate dependency has a different version, source or checksum.',
    'unused_production_packages':sorted([list(p[:2]) for p in package_set(ROOT/'Cargo.lock')-package_set(PROBE/'Cargo.lock')]),
    'repair':'Require every candidate dependency record to equal a production record; record unused production dependencies separately.'})
# Reuse exactly the reviewed category rules without executing the review's
# create-only audit or interpreting any reserved geometry.
tree = ast.parse((REVIEW/'review.py').read_text(encoding='utf-8'))
definition = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='covered')
namespace = {}
exec(compile(ast.Module(body=[definition], type_ignores=[]), 'reviewed-coverage', 'exec'), namespace)
covered = namespace['covered']

tests = run(['cargo','test','--offline','--manifest-path',str(PROBE/'Cargo.toml'),
    '-p','nestbolt-core','--test','lightburn','--test','project_lightburn','--test','lightburn_diagnostics'], 'authored-tests')
write(OUT/'authored-tests.json',tests)
assert tests['exit_code']==0
build = run(['cargo', 'build', '--offline', '--manifest-path', str(PROBE/'Cargo.toml'),
             '--bin', 'nestbolt-ci-curve-probe'], 'build')
write(OUT/'build.json', build)
assert build['exit_code'] == 0, build
assert package_set(PROBE/'Cargo.lock') <= package_set(ROOT/'Cargo.lock')
write(OUT/'started.json', {'utc':datetime.now(timezone.utc).isoformat(), 'binary_sha256':digest(EXE),
    'production_guards':before, 'held_out_geometry_read':False})

rows = []
counts = Counter()
with zipfile.ZipFile(ARCHIVE) as z:
    for index, old in enumerate(previous['rows']):
        source = training[old['path']]
        assert digest(CORPUS/source['path']) == source['sha256'] == old['source_sha256']
        assert digest(CORPUS/source['label']) == source['label_sha256'] == old['label_sha256']
        folder = OUT/f'{index:03}'
        folder.mkdir()
        target = folder/'library.json'
        command = [str(EXE), 'import', str(CORPUS/source['path']), str(target), '0.005']
        p = subprocess.run([sys.executable, str(ROOT/'output/ccd1.py'), *command], cwd=ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        (folder/'stdout.log').write_bytes(p.stdout)
        (folder/'stderr.log').write_bytes(p.stderr)
        row = {'path':old['path'], 'label':old['label'], 'source_sha256':source['sha256'],
               'label_sha256':source['label_sha256'], 'baseline_outcome':old['public_import'],
               'exit_code':p.returncode, 'command':command}
        if old['public_import']=='imported':
            raw = z.read(old['archive_member'])
            assert sha256(raw).hexdigest() == old['library_sha256'] == inventory['members'][old['archive_member']]['sha256']
            baseline = json.loads(raw)
            assert baseline['tolerance'] == 0.005 and baseline['imports'] == []
            if p.returncode == 0:
                candidate = load(target)
                # Only the documented top-level warning array may differ.
                unchanged = {k:v for k,v in baseline.items() if k!='warnings'} == {k:v for k,v in candidate.items() if k!='warnings'}
                old_warnings = iter(candidate['warnings'])
                original_distinct = list(dict.fromkeys(baseline['warnings']))
                kept = all(any(w == prior for w in old_warnings) for prior in original_distinct)
                unique = len(candidate['warnings']) == len(set(candidate['warnings']))
                row.update(geometry_xml_and_all_other_fields_identical=unchanged,
                    all_distinct_original_warnings_kept_in_order=kept, warnings=candidate['warnings'],
                    duplicate_free=unique,
                    original_duplicate_count=len(baseline['warnings'])-len(original_distinct),
                    added_warnings=[w for w in candidate['warnings'] if w not in baseline['warnings']],
                    library_sha256=digest(target), baseline_library_sha256=old['library_sha256'],
                    coverage={c:covered(c,candidate['warnings']) for c in old['expected_warnings']})
                row['passed'] = unchanged and kept and unique and all(row['coverage'].values())
                for category, ok in row['coverage'].items():
                    counts[category+(':covered' if ok else ':missing')] += 1
            else:
                row['passed'] = False
        else:
            error = p.stderr.decode('utf-8').replace('\r\n','\n')
            row.update(rejection_kind=old['rejection_kind'], error=error,
                original_error_identical=error==old['error'], no_partial_library=not target.exists())
            row['passed'] = p.returncode==1 and row['original_error_identical'] and row['no_partial_library']
        rows.append(row)
        write(folder/'check.json', row)
        write(OUT/'progress.json', {'done':len(rows),'passed':sum(r['passed'] for r in rows)})

core = ROOT/'crates/core/src'
candidate = PROBE/'candidate-core/src'
changed = []
patch = []
hashes = {}
for original in sorted(core.rglob('*.rs')):
    relative = original.relative_to(core)
    other = candidate/relative
    hashes[relative.as_posix()] = {'original':digest(original), 'candidate':digest(other)}
    if original.read_bytes()!=other.read_bytes():
        changed.append(relative.as_posix())
        patch.extend(difflib.unified_diff(original.read_text(encoding='utf-8').splitlines(True),
            other.read_text(encoding='utf-8').splitlines(True),
            fromfile='a/crates/core/src/'+relative.as_posix(), tofile='b/crates/core/src/'+relative.as_posix()))
assert set(changed) == {'holes.rs','lightburn.rs','lightburn/path.rs','lightburn/units.rs','project/lightburn.rs'}
(OUT/'candidate.patch').write_text(''.join(patch),encoding='utf-8',newline='\n')
for src, dst in [(PROBE/'Cargo.toml','probe-Cargo.toml'),(PROBE/'Cargo.lock','probe-Cargo.lock'),
                 (PROBE/'src/main.rs','probe-main.rs'),(PROBE/'candidate-core/Cargo.toml','candidate-core-Cargo.toml')]:
    shutil.copyfile(src, OUT/dst)
for name in ['lightburn.rs','project_lightburn.rs','lightburn_diagnostics.rs']:
    shutil.copyfile(PROBE/'candidate-core/tests'/name, OUT/('test-'+name))
after = guards()
assert after==before
summary = {'scope':__doc__, 'utc':datetime.now(timezone.utc).isoformat(),
    'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'production_changes':False, 'production_guards_unchanged':True,
    'production_integration_pending':True, 'H2_complete':False,'held_out_geometry_read':False,
    'new_searches':0, 'training_projects':len(rows),
    'prior_failed_audit':'benchmarks/results/h2-native-warning-probe-20261016/checks.json',
    'prior_failed_audit_sha256':digest(BASE/'h2-native-warning-probe-20261016/checks.json'),
    'prior_passing_audit':'benchmarks/results/h2-native-warning-probe-20261016-v2/checks.json',
    'prior_passing_audit_sha256':digest(BASE/'h2-native-warning-probe-20261016-v2/checks.json'),
    'change_since_prior_audits':'Public import now uses the complete nesting warning list once. Compare all distinct original messages in order and require no duplicated candidate messages. Geometry comparisons and coverage predicates unchanged.',
    'accepted':sum(r['baseline_outcome']=='imported' and r['exit_code']==0 for r in rows),
    'original_clear_rejections':sum(r.get('original_error_identical',False) for r in rows),
    'all_checks_passed':all(r['passed'] for r in rows), 'category_counts':dict(sorted(counts.items())),
    'source_files':hashes, 'changed_candidate_files':changed,
    'all_candidate_third_party_dependency_records_match_production':True,
    'unused_production_packages':sorted([list(p[:2]) for p in package_set(ROOT/'Cargo.lock')-package_set(PROBE/'Cargo.lock')]),
    'binary_sha256':digest(EXE), 'baseline_review_sha256':digest(REVIEW/'checks.json'),
    'baseline_archive_sha256':digest(ARCHIVE), 'rows':rows}
write(OUT/'checks.json',summary)
write(OUT/'integrity.json', {p.relative_to(OUT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size}
    for p in sorted(OUT.rglob('*')) if p.is_file()})
print(json.dumps({k:v for k,v in summary.items() if k not in ['source_files','rows','unused_production_packages']},indent=2))
assert summary['all_checks_passed']
