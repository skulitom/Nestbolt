"""Production regression checks for the authorized preview; no corpus evaluation."""
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/preview-integration-20261016'
OUT.mkdir()
shutil.copyfile(__file__,OUT/'run.py')
shutil.copyfile(ROOT/'output/preview-integration.json',OUT/'integration.json')
def write(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
write('started.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'working_tree_changes':True,'version':'0.2.0-alpha.1','affinity':'CCD1 logical CPUs 16-31','held_out_geometry_read':False,
    'scope':'Production workspace, optimized CLI and Sparrow tests, WASM builds, notices, schemas, real native packaging and browser tests. Frozen dataset/held-out evaluations are separate.'})
stages=[]
def run(name,args,cwd=ROOT,timeout=2400):
    with (OUT/(name+'-stdout.log')).open('wb') as out,(OUT/(name+'-stderr.log')).open('wb') as err:
        r=subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),*map(str,args)],cwd=cwd,stdout=out,stderr=err,timeout=timeout)
    stages.append({'name':name,'command':list(map(str,args)),'exit_code':r.returncode})
    write('progress.json',stages)
    print(name,r.returncode,flush=True)
    assert r.returncode==0,name
run('format',['cargo','fmt','--all','--check'])
run('lint',['cargo','clippy','--workspace','--all-targets','--locked','--','-D','warnings'])
run('workspace',['cargo','test','--workspace','--locked'])
run('optimized-cli',['cargo','test','--release','--locked','-p','nestbolt-cli','--test','features'])
run('optimized-sparrow',['cargo','test','--release','--locked','-p','nestbolt-core','--lib','sparrow_'])
run('stock-helper',['cargo','test','--locked','-p','nestbolt-validator','--example','stock_adapter'])
run('native-build',['cargo','build','--release','--locked','-p','nestbolt-cli','-p','nestbolt-mcp'])
run('wasm-core',['cargo','build','-p','nestbolt-wasm','--target','wasm32-unknown-unknown','--locked'])
run('wasm-validator',['cargo','build','-p','nestbolt-validator','--target','wasm32-unknown-unknown','--locked'])
run('notices',[sys.executable,'scripts/notices.py','--check'])
run('schemas',[sys.executable,'scripts/schemas.py','--check'])
run('packaging',['node','--test','mcpb/mcpb.test.mjs'])
# Vite/build scripts replace these generated directories; verify fixed targets.
for relative in ['web/dist','web/src/pkg','web/test-results']:
    assert ROOT in (ROOT/relative).resolve().parents
run('web-build-and-tests',[sys.executable,'scripts/build_web.py','--test'])
run('web-test-types',['node','node_modules/typescript/bin/tsc','-p','tsconfig.tests.json'],ROOT/'web')
for p in (ROOT/'web/test-results').rglob('*'):
    if p.is_file():
        dest=OUT/'browser-artifacts'/p.relative_to(ROOT/'web/test-results')
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,dest)
write('checks.json',{'all_checks_passed':True,'stages':stages,'version':'0.2.0-alpha.1','held_out_geometry_read':False,
    'performance_confirmation_pending':True,'completed_utc':datetime.now(timezone.utc).isoformat(),
    'binaries':{rel:sha256((ROOT/rel).read_bytes()).hexdigest() for rel in ['target/release/nestbolt.exe','target/release/nestbolt-mcp.exe','web/src/pkg/nestbolt_wasm_bg.wasm']}})
print('All preview integration checks passed',flush=True)
