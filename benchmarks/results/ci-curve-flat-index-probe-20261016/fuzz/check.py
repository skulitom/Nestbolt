"""Broaden the isolated candidate check with pinned dependencies and 128 curves."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import psutil

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'output/ci-curve-probe'
CANDIDATE=BASE/'candidate-core'
OUT=ROOT/'benchmarks/results/ci-curve-flat-index-probe-20261016/fuzz'
sys.path.insert(0,str(ROOT/'scripts'))
import h4_full_matrix as full
from h6_material_cost import run as validate_run, equivalent
OUT.mkdir(exist_ok=False)
before=full.guards(full.cases())
assert before==full.load(ROOT/'benchmarks/results/h4-full-development-20261015/plan.json')['guards']
tests=CANDIDATE/'tests'
(tests/'support').mkdir(parents=True,exist_ok=False)
source=(ROOT/'crates/core/tests/search_fuzz.rs').read_text(encoding='utf-8')
assert source.count('ProptestConfig::with_cases(24)')==1
source=source.replace('ProptestConfig::with_cases(24)','ProptestConfig::with_cases(128)')
(tests/'search_fuzz.rs').write_text(source,encoding='utf-8',newline='\n')
shutil.copyfile(ROOT/'crates/core/tests/support/shop_habits.rs',tests/'support/shop_habits.rs')
shutil.copyfile(ROOT/'Cargo.lock',BASE/'Cargo.lock')
shutil.copyfile(tests/'search_fuzz.rs',OUT/'search_fuzz.rs')
shutil.copyfile(tests/'support/shop_habits.rs',OUT/'shop_habits.rs')
shutil.copyfile(__file__,OUT/'check.py')
env=os.environ.copy()
env['CARGO_TARGET_DIR']=str(ROOT/'target')
env['RUST_BACKTRACE']='1'
env['PROPTEST_RNG_SEED']='20261016'
def run(command,name):
    with (OUT/(name+'-stdout.txt')).open('xb') as out,(OUT/(name+'-stderr.txt')).open('xb') as err:
        p=subprocess.Popen(command,cwd=ROOT,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        psutil.Process(p.pid).cpu_affinity(list(range(16,32)))
        try: code=p.wait(timeout=900)
        except subprocess.TimeoutExpired:
            p.kill(); p.wait(); code='timeout'
    return {'command':[str(c) for c in command],'exit_code':code}
record={'created_utc':datetime.now(timezone.utc).isoformat(),'cases':128,'generation_seed':20261016,
        'scope':'Functional generated-curve cases on isolated candidate, no corpus/held-out inputs; no performance claim.',
        'steps':{}}
record['steps']['curves']=run(['cargo','test','--offline','--manifest-path',str(BASE/'Cargo.toml'),'-p','nestbolt-core','--test','search_fuzz','random_curved_svg_parts_nest_validly','--','--exact','--nocapture','--test-threads=1'],'curves')
old=tomllib.loads((ROOT/'Cargo.lock').read_text(encoding='utf-8'))['package']
new=tomllib.loads((BASE/'Cargo.lock').read_text(encoding='utf-8'))['package']
key=lambda p:(p['name'],p['version'],p.get('source'),p.get('checksum'))
record['third_party_lock_entries_match']=all(key(p) in {key(q) for q in old} for p in new if p.get('source'))
assert record['third_party_lock_entries_match']
shutil.copyfile(BASE/'Cargo.lock',OUT/'probe-Cargo.lock')
record['steps']['binary']=run(['cargo','build','--offline','--manifest-path',str(BASE/'Cargo.toml')],'binary')
if record['steps']['binary']['exit_code']==0:
    record['steps']['exact_case']=run([ROOT/'target/debug/nestbolt-ci-curve-probe.exe','search',OUT/'exact'],'exact')
    if record['steps']['exact_case']['exit_code']==0:
        expected=ROOT/'benchmarks/results/release-readiness-20261016/search'
        assert (OUT/'exact/input.svg').read_bytes()==(expected/'input.svg').read_bytes()
        assert (OUT/'exact/job.json').read_bytes()==(expected/'job.json').read_bytes()
        result=full.load(OUT/'exact/result.json')
        (OUT/'exact/layout.json').write_text(json.dumps(result['layout'],indent=2)+'\n',encoding='utf-8',newline='\n')
        record['independent_validation']=validate_run([ROOT/'target/release/nestbolt.exe','validate','--job',OUT/'exact/job.json','--layout',OUT/'exact/layout.json'],OUT,'validate',16,60)
        if record['independent_validation']['exit_code']==0:
            checked=full.load(OUT/'validate-stdout.json')
            record['valid']=checked['valid']
            record['metric_delta']=equivalent(result['validation']['metrics'],checked['metrics'])
            record['placements']=len(result['layout']['placements'])
record['guards_unchanged']=full.guards(full.cases())==before
assert record['guards_unchanged']
for p in tests.glob('*.proptest-regressions'):
    shutil.copyfile(p,OUT/p.name)
(OUT/'checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(record,indent=2))
