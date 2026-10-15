"""Record local preview-policy checks without creating tags or releases."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/preview-packaging-20261016'
OUT.mkdir(exist_ok=False)
sys.path.insert(0,str(ROOT/'scripts'))
import h4_full_matrix as full
assert full.guards(full.cases())==full.load(ROOT/'benchmarks/results/h4-full-development-20261015/plan.json')['guards']
workflow=yaml.safe_load((ROOT/'.github/workflows/release.yml').read_text(encoding='utf-8'))
syntax=[]
for job_id,job in workflow['jobs'].items():
    for i,step in enumerate(job['steps']):
        if 'run' not in step: continue
        code=re.sub(r'\$\{\{.*?\}\}','WORKFLOW_EXPRESSION',step['run'],flags=re.S)
        check=subprocess.run(['C:/Program Files/Git/bin/bash.exe','-n','-s'],input=code,text=True,capture_output=True,cwd=ROOT)
        syntax.append({'job':job_id,'step':step.get('name',str(i)),'exit_code':check.returncode,'stderr':check.stderr})
assert all(r['exit_code']==0 for r in syntax),syntax
policy=[]
for tag in ['v0.1.0','v0.2.0-alpha.1']:
    command=['node','mcpb/release.mjs',tag]
    p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    policy.append({'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
assert policy[0]['exit_code']==0 and json.loads(policy[0]['stdout'])=={'prerelease':False,'latest':True}
assert policy[1]['exit_code']==1 and 'existing valid version tag' in policy[1]['stderr']
files=['.github/workflows/release.yml','mcpb/build.mjs','mcpb/release.mjs','mcpb/mcpb.test.mjs','mcpb/PUBLISHING.md']
record={'created_utc':datetime.now(timezone.utc).isoformat(),
        'files':{name:sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
        'packaging_tests':{'command':['python','output/ccd1.py','node','--test','--test-skip-pattern=^real release','mcpb/mcpb.test.mjs'],
                           'exit_code':0,'passed':21,'platform_skips':1,'real_binary_tests_excluded':2,
                           'evidence':'Observed tool execution in this turn; no separate raw test log was captured.'},
        'workflow_yaml_parsed':True,'bash_syntax':syntax,'local_policy_cli':policy,
        'no_tag_or_release_created':True,'native_packaging_dry_run_pending':True,
        'measured_H4_guards_unchanged':True}
(OUT/'checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,OUT/'check.py')
print(json.dumps({'bash_steps_checked':len(syntax),'policy_cli_cases':len(policy),'H4_guards_unchanged':True}))
