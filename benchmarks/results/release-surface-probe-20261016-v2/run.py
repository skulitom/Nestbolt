"""Actual CLI, stdio MCP and browser checks of the isolated release fixes."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PROBE=ROOT/'output/release-surface-probe'
OUT=ROOT/'benchmarks/results/release-surface-probe-20261016-v2'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()

def write(path,data):
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')

def guards():
    sys.path.insert(0,str(ROOT/'scripts'))
    import h4_full_matrix as full
    current=full.guards(full.cases())
    assert current==load(ROOT/'benchmarks/results/h4-full-development-20261015/plan.json')['guards']
    return current

OUT.mkdir()
shutil.copyfile(__file__,OUT/'run.py')
shutil.copyfile(ROOT/'output/prepare_release_surface_probe.py',OUT/'prepare.py')
before=guards()
write(OUT/'started.json',{'utc':datetime.now(timezone.utc).isoformat(),
    'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'production_guards':before,'held_out_geometry_read':False,'measured_searches':0,
    'workspace':str(PROBE),'cpu_affinity':'CCD1 logical 16-31',
    'isolated_server':'http://127.0.0.1:4185; no existing server reuse'})
stages=[]
def run(name,command,cwd=PROBE,timeout=1800):
    with (OUT/(name+'-stdout.log')).open('wb') as out, (OUT/(name+'-stderr.log')).open('wb') as err:
        result=subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),*map(str,command)],
            cwd=cwd,stdout=out,stderr=err,timeout=timeout)
    stages.append({'stage':name,'command':list(map(str,command)), 'cwd':str(cwd),'exit_code':result.returncode})
    write(OUT/'progress.json',stages)
    print(name,result.returncode,flush=True)
    assert result.returncode==0,name

run('native-diagnostics',['cargo','test','--locked','--offline','-p','nestbolt-cli','-p','nestbolt-mcp','lightburn_import_diagnostics'])
run('native-lint',['cargo','clippy','--locked','--offline','-p','nestbolt-cli','-p','nestbolt-mcp','--tests','--','-D','warnings'])
# Build scripts and Vite replace generated directories. Resolve these fixed
# targets before invoking either, and exclude the shared dependency/cache links.
for relative in ['web/src/pkg','web/dist','web/test-results']:
    target=(PROBE/relative).resolve()
    assert PROBE.resolve() in target.parents, target
run('web-build',[sys.executable,PROBE/'scripts/build_web.py'])
run('web-types',['node',ROOT/'web/node_modules/typescript/bin/tsc','-p','tsconfig.tests.json'],PROBE/'web')
run('web-diagnostics',['node',ROOT/'web/node_modules/@playwright/test/cli.js','test','lightburn.spec.ts',
    '--grep','LightBurn import diagnostics','--workers','2'],PROBE/'web',300)
assert guards()==before
paths=['crates/core/src/holes.rs','crates/core/src/lightburn.rs','crates/core/src/lightburn/path.rs',
    'crates/core/src/lightburn/units.rs','crates/core/src/project/lightburn.rs','crates/core/tests/lightburn.rs',
    'crates/core/tests/lightburn_diagnostics.rs','crates/core/tests/hole_index_regression.rs',
    'crates/core/tests/fixtures/ci-hole-curve.svg','crates/core/tests/fixtures/native-diagnostics.lbrn2',
    'crates/cli/tests/features.rs','crates/mcp/tests/connection.rs','web/tests/lightburn.spec.ts',
    'web/playwright.config.ts','web/package.json','Cargo.toml','Cargo.lock','.cargo/config.toml']
for relative in paths:
    target=OUT/'snapshots'/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(PROBE/relative,target)
for source in (PROBE/'web/test-results').rglob('*'):
    if source.is_file():
        target=OUT/'browser-artifacts'/source.relative_to(PROBE/'web/test-results')
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
write(OUT/'checks.json',{'all_checks_passed':True,'stages':stages,'production_guards_unchanged':True,
    'production_integration_pending':True,'held_out_geometry_read':False,
    'scope':'New diagnostic e2e tests through the actual CLI, stdio MCP server, Chromium and Firefox; strict native lint and browser build/type checks.',
    'limitations':'Isolated workspace; production integration, complete regression suite and hole-index performance remain required.',
    'candidate_cli_sha256':digest(PROBE/'target/debug/nestbolt.exe'),
    'candidate_mcp_sha256':digest(PROBE/'target/debug/nestbolt-mcp.exe'),
    'candidate_wasm_sha256':digest(PROBE/'web/src/pkg/nestbolt_wasm_bg.wasm'),
    'core_source':{p.relative_to(PROBE/'crates/core/src').as_posix():digest(p) for p in sorted((PROBE/'crates/core/src').rglob('*.rs'))}})
write(OUT/'integrity.json',{p.relative_to(OUT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size}
    for p in sorted(OUT.rglob('*')) if p.is_file()})
print(json.dumps(load(OUT/'checks.json'),indent=2))
