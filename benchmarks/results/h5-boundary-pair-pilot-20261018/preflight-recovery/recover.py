"""Preserve a pre-measurement PID-reuse failure and qualify process identity checks."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
from unittest.mock import patch
import ast,importlib.util,json,shutil,subprocess,sys
import psutil
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-boundary-pair-pilot-20261018'
runner=root/'scripts/h5_boundary_pair_pilot.py';folder=out/'preflight-recovery';folder.mkdir()
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (out/'opened.json').exists() and not (root/'output'/out.name).exists()
assert sorted(p.name for p in out.iterdir() if p.is_file())==['plan.json','runner.py']
assert subprocess.check_output(['git','show','HEAD:'+(out/'plan.json').relative_to(root).as_posix()],cwd=root)==(out/'plan.json').read_bytes()
shutil.copyfile(runner,folder/'runner-before.py');shutil.copyfile(out/'plan.json',folder/'plan-before.json')
original=runner.read_text(encoding='utf-8');old_plan=load(out/'plan.json')
write(folder/'failure.json',{'exit_code':1,'exception':'psutil.AccessDenied','pid':96548,
    'origin':'require_measurements_finished: psutil.Process(old_diagnostic_pid).cmdline()',
    'old_opened':load(root/'benchmarks/results/h5-balanced-stage-20261018/opened.json'),
    'observed_current_process':{'pid':96548,'name':psutil.Process(96548).name(),'created':psutil.Process(96548).create_time()},
    'no_opened_marker':True,'no_measurement_work_directory':True,'started_searches':0,
    'original_plan_sha256':digest(out/'plan.json'),'original_runner_sha256':digest(runner)})
helper='''def require_runner_stopped(opened, runner):
    # A Windows PID is reusable. Establish identity before reading a command
    # line, which may be inaccessible for the unrelated replacement process.
    original_opened = datetime.fromisoformat(opened['utc']).timestamp()
    try:
        process = psutil.Process(opened['pid'])
        created = process.create_time()
        if created > original_opened:
            return {'pid': opened['pid'], 'state': 'reused_pid',
                    'original_opened': original_opened, 'current_created': created}
        arguments = process.cmdline()
    except psutil.NoSuchProcess:
        return {'pid': opened['pid'], 'state': 'absent'}
    assert not any(runner in arg for arg in arguments), 'Previous measurement runner is still active'
    return {'pid': opened['pid'], 'state': 'different_command', 'current_created': created}


'''
needle='def require_measurements_finished():';assert original.count(needle)==1;s=original.replace(needle,helper+needle)
before="""    try:
        arguments = psutil.Process(load(diagnostic/'opened.json')['pid']).cmdline()
    except psutil.NoSuchProcess:
        arguments = []
    assert not any('h5_balanced_stage.py' in arg for arg in arguments), 'Diagnostic is still running'"""
after="    process_checks = [require_runner_stopped(load(diagnostic/'opened.json'), 'h5_balanced_stage.py')]"
assert s.count(before)==1;s=s.replace(before,after)
before="""        opened = load(folder/'opened.json')
        try:
            arguments = psutil.Process(opened['pid']).cmdline()
        except psutil.NoSuchProcess:
            arguments = []
        assert not any(runner in arg for arg in arguments), 'Release measurements are still running'"""
after="        process_checks.append(require_runner_stopped(load(folder/'opened.json'), runner))"
assert s.count(before)==1;s=s.replace(before,after)
needle="    return {path.relative_to(ROOT).as_posix(): digest(path) for path in paths}"
assert s.count(needle)==1;s=s.replace(needle,needle+" | {'process_identity_checks': process_checks}")
needle="    paths = [Path(__file__), ROOT/'scripts/test_h5_early_exchange_pilot.py',"
assert s.count(needle)==1;s=s.replace(needle,"    paths = [Path(__file__), ROOT/'benchmarks/results/h5-boundary-pair-pilot-20261018/preflight-recovery/checks.json', ROOT/'scripts/test_h5_early_exchange_pilot.py',")
def fn(text,name):return next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
names=['blocks','summarize','case','measure']
for name in names:assert ast.dump(fn(original,name))==ast.dump(fn(s,name))
runner.write_text(s,encoding='utf-8',newline='\n')
sys.path.insert(0,str(root/'scripts'))
spec=importlib.util.spec_from_file_location('boundary_pair_recovery',runner);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
opened={'pid':999999,'utc':'2026-10-18T00:00:00+00:00'};timestamp=datetime.fromisoformat(opened['utc']).timestamp();tests=[]
class Fake:
    def __init__(self,created,args=None,denied_time=False):self.created=created;self.args=args;self.denied_time=denied_time
    def create_time(self):
        if self.denied_time:raise psutil.AccessDenied(999999)
        return self.created
    def cmdline(self):
        if self.args is None:raise psutil.AccessDenied(999999)
        return self.args
with patch.object(module.psutil,'Process',side_effect=psutil.NoSuchProcess(999999)):
    assert module.require_runner_stopped(opened,'runner.py')['state']=='absent';tests.append('absent process accepted')
with patch.object(module.psutil,'Process',return_value=Fake(timestamp+60)):
    assert module.require_runner_stopped(opened,'runner.py')['state']=='reused_pid';tests.append('new protected replacement accepted without reading its command')
with patch.object(module.psutil,'Process',return_value=Fake(timestamp-60,['python','runner.py'])):
    try:module.require_runner_stopped(opened,'runner.py')
    except AssertionError:tests.append('live original runner rejected')
    else:raise AssertionError('Accepted live original runner')
with patch.object(module.psutil,'Process',return_value=Fake(timestamp-60,['python','other.py'])):
    assert module.require_runner_stopped(opened,'runner.py')['state']=='different_command';tests.append('different command retains prior behavior')
for fake,label in [(Fake(timestamp-60), 'unknown original command fails closed'),(Fake(timestamp-60,denied_time=True),'unknown creation time fails closed')]:
    with patch.object(module.psutil,'Process',return_value=fake):
        try:module.require_runner_stopped(opened,'runner.py')
        except psutil.AccessDenied:tests.append(label)
        else:raise AssertionError('Ignored unresolved process identity')
prerequisites=module.require_measurements_finished()
checks={'all_checks_pass':True,'tests':tests,'actual_prerequisites':prerequisites,
        'runner_sha256':digest(runner),'original_runner_sha256':digest(folder/'runner-before.py'),
        'original_plan_sha256':digest(folder/'plan-before.json'),'unchanged_function_ASTs':names,
        'candidate_sources_and_binaries_changed':False,'search_budgets_inputs_scoring_changed':False,
        'measurement_started_before_recovery':False,'new_searches':0}
write(folder/'checks.json',checks)
new_plan=dict(old_plan);new_plan['guards']=module.guards()
new_plan['preflight_amendment']={'utc':datetime.now(timezone.utc).isoformat(),'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
    'reason':'Old diagnostic PID was reused by svchost.exe; compare creation time before reading command lines.',
    'original_plan_sha256':checks['original_plan_sha256'],'checks':'preflight-recovery/checks.json','started_searches_before_amendment':0}
write(out/'plan.json',new_plan);shutil.copyfile(runner,out/'runner.py');shutil.copyfile(__file__,folder/'recover.py')
print(json.dumps({'guard_tests':len(tests),'real_process_checks':prerequisites['process_identity_checks'],'new_searches':0,'plan_requires_commit':True}))
