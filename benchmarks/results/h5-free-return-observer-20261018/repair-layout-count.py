"""Retain the old two-case terminal assertion; reuse already validated four-case baselines."""
from pathlib import Path
from hashlib import sha256
import json,shutil
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-free-return-observer-20261018';p=root/'output/check_h5_free_return_observer_layouts.py'
failure=json.loads((out/'layout-check-failure.json').read_bytes());assert len(failure['completed'])==4
shutil.copyfile(p,out/'failed-two-case-layout-checker.py');original=p.read_text(encoding='utf-8');s=original
assert s.count('len(finals)==2')==1;s=s.replace('len(finals)==2','len(finals)==4')
a="folder=out/'baseline-layouts';folder.mkdir();records=[];finals=[]";b="folder=out/'baseline-layouts';assert folder.is_dir();records=[];finals=[]"
assert s.count(a)==1;s=s.replace(a,b)
a='case.mkdir()';assert s.count(a)==1;s=s.replace(a,'assert case.is_dir()')
a="            write(case/'job.json',job);write(case/'layout.json',layout)";b="            assert load(case/'job.json')==job and load(case/'layout.json')==layout"
assert s.count(a)==1;s=s.replace(a,b)
a="""            r=subprocess.run(args,capture_output=True,timeout=60)
            (case/'stdout.json').write_bytes(r.stdout);(case/'stderr.log').write_bytes(r.stderr);write(case/'command.json',{'command':args,'exit_code':r.returncode})"""
b="""            command=load(case/'command.json');assert command['command']==args and command['exit_code']==0
            cache=load(out/'layout-terminal-count-repair.json')['cached_baselines']
            for file in case.iterdir():assert digest(file)==cache[file.relative_to(out).as_posix()]
            r=subprocess.CompletedProcess(args,0,(case/'stdout.json').read_bytes(),(case/'stderr.log').read_bytes())"""
assert s.count(a)==1;s=s.replace(a,b)
record={'reason':'The copied audit inspected all four cases, then its inherited final assertion still required two. Correct only the expected count; reuse every already captured frozen-CLI validation and retain the original failure.',
 'failure_sha256':sha256((out/'layout-check-failure.json').read_bytes()).hexdigest(),
 'failed_checker_sha256':sha256((out/'failed-two-case-layout-checker.py').read_bytes()).hexdigest(),
 'cached_baselines':{f.relative_to(out).as_posix():sha256(f.read_bytes()).hexdigest() for f in (out/'baseline-layouts').rglob('*') if f.is_file()},
 'new_searches':0,'new_CLI_runs':0,'geometry_assertions_unchanged':True}
(out/'layout-terminal-count-repair.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');compile(s,str(p),'exec');p.write_text(s,encoding='utf-8',newline='\n');shutil.copyfile(__file__,out/'repair-layout-count.py')
print('Corrected the four-case terminal assertion; original failure and all cached validations retained.')
