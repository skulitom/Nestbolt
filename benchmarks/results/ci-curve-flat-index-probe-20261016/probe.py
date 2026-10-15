"""Test one isolated hole-index configuration without editing measured sources."""
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
OUT=ROOT/'benchmarks/results/ci-curve-flat-index-probe-20261016'
CANDIDATE=BASE/'candidate-core'
sys.path.insert(0,str(ROOT/'scripts'))
import h4_full_matrix as full

def digest(path): return sha256(path.read_bytes()).hexdigest()
def write(path,value): path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
def toml(value):
    if isinstance(value,dict): return '{ '+', '.join(k+' = '+toml(v) for k,v in value.items())+' }'
    if isinstance(value,list): return '['+', '.join(toml(v) for v in value)+']'
    if isinstance(value,bool): return str(value).lower()
    if isinstance(value,str): return json.dumps(value)
    return str(value)
def run(command,name,env):
    with (OUT/(name+'-stdout.txt')).open('xb') as out,(OUT/(name+'-stderr.txt')).open('xb') as err:
        process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=out,stderr=err,creationflags=subprocess.CREATE_NO_WINDOW)
        psutil.Process(process.pid).cpu_affinity(list(range(16,32)))
        code=process.wait(timeout=900)
    return {'command':[str(c) for c in command],'exit_code':code,
            'stdout_sha256':digest(OUT/(name+'-stdout.txt')),'stderr_sha256':digest(OUT/(name+'-stderr.txt'))}

OUT.mkdir(exist_ok=False)
CANDIDATE.mkdir(exist_ok=False)
before=full.guards(full.cases())
assert before==full.load(ROOT/'benchmarks/results/h4-full-development-20261015/plan.json')['guards']
shutil.copytree(ROOT/'crates/core/src',CANDIDATE/'src')
workspace=tomllib.loads((ROOT/'Cargo.toml').read_text(encoding='utf-8'))['workspace']
lines=[]
section=None
for line in (ROOT/'crates/core/Cargo.toml').read_text(encoding='utf-8').splitlines():
    if line.startswith('['): section=line
    if line.endswith('.workspace = true'):
        key=line.split('.')[0]
        value=workspace['package' if section=='[package]' else 'dependencies'][key]
        if isinstance(value,dict) and 'path' in value:
            value={**value,'path':(ROOT/value['path']).as_posix()}
        line=key+' = '+toml(value)
    elif section=='[lints]' and line=='workspace = true':
        line='rust.unsafe_code = "forbid"\nclippy.all = "warn"'
    lines.append(line)
(CANDIDATE/'Cargo.toml').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
path=CANDIDATE/'src/holes.rs'
original=path.read_text(encoding='utf-8')
old='let importer = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None)'
new='''// The small hole container uses a flat collision index. This avoids the
    // upstream f32 quadrant classification at near-corner intersections.
    let importer = Importer::new(jagua_rs::collision_detection::CDEConfig {
        quadtree_depth: 0, ..DEFAULT_SPARROW_CONFIG.cde_config
    }, None, None)'''
assert original.count(old)==1
path.write_text(original.replace(old,new),encoding='utf-8',newline='\n')
manifest=(BASE/'Cargo.toml').read_text(encoding='utf-8')
assert 'path = "../../crates/core"' in manifest
manifest=manifest.replace('path = "../../crates/core"','path = "candidate-core"')
manifest=manifest.replace('[workspace]\n','[workspace]\nmembers = ["candidate-core"]\n')
(BASE/'Cargo.toml').write_text(manifest,encoding='utf-8',newline='\n')
shutil.copyfile(path,OUT/'candidate-holes.rs')
shutil.copyfile(CANDIDATE/'Cargo.toml',OUT/'candidate-Cargo.toml')
shutil.copyfile(BASE/'src/main.rs',OUT/'probe.rs')
shutil.copyfile(__file__,OUT/'probe.py')
env=os.environ.copy()
env['CARGO_TARGET_DIR']=str(ROOT/'target')
env['RUST_BACKTRACE']='1'
record={'created_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Isolated configuration hypothesis in output/candidate-core; no production integration or performance claim.',
        'original_holes_sha256':digest(ROOT/'crates/core/src/holes.rs'),
        'candidate_holes_sha256':digest(path),'product_digest':before['product'],'steps':{}}
record['steps']['build']=run(['cargo','build','--offline','--manifest-path',str(BASE/'Cargo.toml')],'build',env)
write(OUT/'checks.json',record)
if record['steps']['build']['exit_code']==0:
    record['steps']['search']=run([ROOT/'target/debug/nestbolt-ci-curve-probe.exe','search',OUT/'search'],'search',env)
    if record['steps']['search']['exit_code']==0:
        result=full.load(OUT/'search/result.json')
        record['valid']=result['validation']['valid']
        record['placements']=len(result['layout']['placements'])
record['guards_unchanged']=full.guards(full.cases())==before
assert record['guards_unchanged']
write(OUT/'checks.json',record)
print(json.dumps(record,indent=2))
