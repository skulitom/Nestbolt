"""Continue the standalone reproduction after removing a private-API probe."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'benchmarks/results/release-readiness-20261016'
PROBE = ROOT / 'output/ci-curve-probe'
sys.path.insert(0, str(ROOT / 'scripts'))
import h4_full_matrix as full

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(command, name, env):
    with (OUT/(name+'-stdout.txt')).open('xb') as out, (OUT/(name+'-stderr.txt')).open('xb') as err:
        proc = subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
        psutil.Process(proc.pid).cpu_affinity(list(range(16,32)))
        code=proc.wait(timeout=900)
    return {'command':[str(p) for p in command],'exit_code':code,
            'stdout_sha256':digest(OUT/(name+'-stdout.txt')),'stderr_sha256':digest(OUT/(name+'-stderr.txt'))}

before=full.guards(full.cases())
assert before==full.load(ROOT/'benchmarks/results/h4-full-development-20261015/plan.json')['guards']
source=(OUT/'probe.rs').read_text(encoding='utf-8')
source=source[source.index('use nestbolt_core'):]
begin=source.index('    if std::env::args()')
end=source.index('    let circles = ',begin)
source=source[:begin]+source[end:]
(PROBE/'src/main.rs').write_text(source,encoding='utf-8',newline='\n')
(OUT/'probe-v2.rs').write_text(source,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,OUT/'probe-v2.py')
env=os.environ.copy()
env['CARGO_TARGET_DIR']=str(ROOT/'target')
env['RUST_BACKTRACE']='1'
result={'scope':'Same exact CI input and public search; the earlier build failed only because the primitive trait is private. No product edit.',
        'before_guard_matches':True,'steps':{}}
result['steps']['build']=run(['cargo','build','--offline','--manifest-path',str(PROBE/'Cargo.toml')],'build-v2',env)
if result['steps']['build']['exit_code']==0:
    result['steps']['search']=run([ROOT/'target/debug/nestbolt-ci-curve-probe.exe','search',OUT/'search'],'search',env)
result['after_guard_matches']=full.guards(full.cases())==before
assert result['after_guard_matches']
(OUT/'probe-v2-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,indent=2))
