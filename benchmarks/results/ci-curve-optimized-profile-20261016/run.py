"""Recheck the isolated hole-index repair with the production engine optimization profile."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'benchmarks/results/ci-curve-optimized-profile-20261016'
PROBE = ROOT/'output/ci-curve-probe'
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()

def write(path, data):
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')

def guards():
    sys.path.insert(0,str(ROOT/'scripts'))
    import h4_full_matrix as full
    value = full.guards(full.cases())
    assert value==load(ROOT/'benchmarks/results/h4-full-development-20261015/plan.json')['guards']
    return value

def run(command, stem, environment=None):
    result = subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),*map(str,command)],cwd=ROOT,
        env=environment,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=900)
    (OUT/(stem+'-stdout.log')).write_bytes(result.stdout)
    (OUT/(stem+'-stderr.log')).write_bytes(result.stderr)
    record = {'command':list(map(str,command)), 'exit_code':result.returncode}
    write(OUT/(stem+'.json'),record)
    assert result.returncode==0, record

before=guards()
OUT.mkdir()
shutil.copyfile(__file__,OUT/'run.py')
candidate = load(ROOT/'benchmarks/results/h2-native-warning-probe-20261016-v2/checks.json')
for name,record in candidate['source_files'].items():
    assert digest(PROBE/'candidate-core/src'/name)==record['candidate']
shutil.copyfile(PROBE/'Cargo.toml',OUT/'probe-Cargo.toml')
shutil.copyfile(PROBE/'Cargo.lock',OUT/'probe-Cargo.lock')
shutil.copyfile(PROBE/'candidate-core/tests/search_fuzz.rs',OUT/'search_fuzz.rs')
write(OUT/'started.json',{'utc':datetime.now(timezone.utc).isoformat(),
    'candidate_warning_audit_sha256':digest(ROOT/'benchmarks/results/h2-native-warning-probe-20261016-v2/checks.json'),
    'production_guards':before,'cpu_affinity':'CCD1 logical 16-31; functional checks only',
    'profile':'nestbolt-core, nestbolt-validator and third-party crates opt-level=3; debug assertions enabled',
    'timing_or_quality_measurement':False,'held_out_geometry_read':False})
binary=PROBE/'target/debug/nestbolt-ci-curve-probe.exe'
run([binary,'exact',OUT/'exact'],'exact')
original=ROOT/'benchmarks/results/release-readiness-20261016'
# Locate the retained original by its known content hash without reading unrelated inputs.
job=OUT/'exact/job.json'
assert digest(job)=='cb3a509cba4751e1e4992a7391264bbffb312a21cd8324e25232e14fbafe564e'
env=os.environ.copy()
env['PROPTEST_RNG_SEED']='20261016'
run(['cargo','test','--offline','--manifest-path',PROBE/'Cargo.toml','-p','nestbolt-core',
    '--test','search_fuzz','random_curved_svg_parts_nest_validly','--','--exact'], 'curves-128',env)
assert guards()==before
result=load(OUT/'exact/result.json')
write(OUT/'checks.json',{'all_checks_passed':True,'exact_job_sha256':digest(job),
    'exact_placements':len(result['layout']['placements']), 'exact_independent_validation':result['validation'],
    'generated_cases':128,'generation_seed':20261016,'test':'random_curved_svg_parts_nest_validly',
    'binary_sha256':digest(binary),'production_guards_unchanged':True,'production_integration_pending':True,
    'quality_or_timing_claim':False,'held_out_geometry_read':False,
    'limitation':'Isolated workspace and generated functional cases; full production regression checks and measured performance remain required.'})
write(OUT/'integrity.json',{p.relative_to(OUT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size}
    for p in sorted(OUT.rglob('*')) if p.is_file()})
print(json.dumps(load(OUT/'checks.json'),indent=2))
