"""Prepare a matched source-frontier pilot without starting measurements."""
from pathlib import Path
from hashlib import sha256
import ast,importlib,json,shutil,subprocess,sys,unittest
root=Path(__file__).resolve().parents[1];probe=root/'output/h5-frontier-probe-20261018'
digest=lambda p:sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
parent=root/'scripts/h5_joint_repair_pilot.py';target=root/'scripts/h5_source_frontier_pilot.py'
assert not target.exists()
text=parent.read_text(encoding='utf-8')
a=text.index('"""');b=text.index('"""',a+3)+3
text=text[:a]+'''"""Matched development pilot of joint repair with an exposed source boundary.

The four original jobs, both kerfs, seeds 0-2, three arms and 60-second wall
allowance remain. The candidate derives a nonempty remaining-source boundary
before returns are added, charges the scan and retains the original crop for
empty sources. The short phase, total deadline, validation reserve, four-step
cap, exact container checks, strict final material guard and rollback remain.
All 171 native tests, 139 exact earlier witnesses, six public outcomes and
independent geometry checks qualify this isolated implementation. This pilot
cannot close H5 or establish a comparative product claim.
"""'''+text[b:]
text=text.replace("PROBE = ROOT/'output/h5-joint-repair-probe-20261018'", "import h5_joint_repair_pilot as previous_pilot\n\nPROBE = ROOT/'output/h5-frontier-probe-20261018'")
text=text.replace("CLI = PROBE/'public-checks/nestbolt-validator.exe'",'CLI = previous_pilot.CLI')
text=text.replace("'normal': PROBE/'baseline-observer.exe'", "'normal': previous_pilot.ENGINES['normal']")
text=text.replace("'baseline': PROBE/'baseline-observer.exe'", "'baseline': previous_pilot.ENGINES['baseline']")
text=text.replace("'candidate': PROBE/'candidate-observer.exe'", "'candidate': PROBE/'frontier-candidate.exe'")
a=text.index('def guards():');b=text.index('\n\ndef blocks():',a)
text=text[:a]+'''def guards():
    prior = ROOT/'benchmarks/results/h5-joint-repair-pilot-20261018'
    observer = ROOT/'benchmarks/results/h5-joint-observer-20261018'
    assert load(prior/'verification.json')['valid'] == 72
    assert load(observer/'verification.json')['all_original_archives_verified']
    require_runner_stopped(load(prior/'opened.json'), 'h5_joint_repair_pilot.py')
    require_runner_stopped(load(observer/'opened.json'), 'h5_joint_observer.py')
    paths = [Path(__file__), ROOT/'scripts/h5_joint_repair_pilot.py',
        ROOT/'output/finish_h5_source_frontier_pilot.py', ROOT/'output/audit_h5_source_frontier_pilot.py',
        PROBE/'policy-plan.json', PROBE/'policy-checks/build.json',
        PROBE/'policy-native-audit/checks.json', PROBE/'public-checks/checks.json',
        PROBE/'frontier-pilot-harness-tests.log', PROBE/'frontier-paired-method-review.json',
        ROOT/'benchmarks/results/h5-frontier-preparation-20261018/checks.json',
        ROOT/'benchmarks/results/h5-frontier-preparation-20261018/integrity.json',
        ROOT/'benchmarks/results/h5-frontier-witness-20261018/integrity.json',
        prior/'verification.json', prior/'source-review.json', observer/'verification.json',
        observer/'interpretation.json', observer/'source-frontiers.json', *set(ENGINES.values())]
    return {'production': source_digest(), 'previous_qualification_guards': previous_pilot.guards(),
        'candidate_source': tree_hash(PROBE/'candidate'),
        'files': {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}}
'''+text[b:]
a=text.index('    assert load(PROBE/',text.index('def prepare(out):'));b=text.index('    out.mkdir()',a)
text=text[:a]+'''    assert load(PROBE/'public-checks/checks.json')['all_passed']
    assert load(PROBE/'policy-checks/build.json')['binary_sha256'] == digest(ENGINES['candidate'])
    assert load(previous_pilot.PROBE/'build.json')['binaries']['baseline'] == digest(ENGINES['baseline'])
    assert digest(ENGINES['baseline']) != digest(ENGINES['candidate'])
    assert load(ROOT/'benchmarks/results/h5-frontier-preparation-20261018/checks.json')['qualified_for_matched_pilot']
'''+text[b:]
text=text.replace("'Isolated joint-repair candidate, common-line search bonus on'", "'Isolated source-frontier joint-repair candidate, common-line search bonus on'")
text=text.replace("'benchmarks/results/h5-assignment-bridge-pilot-20261018/results.json'", "'benchmarks/results/h5-joint-repair-pilot-20261018/results.json'")
target.write_text(text,encoding='utf-8',newline='\n')
# Preserve the independent archive verification and all previous counter audits.
p=root/'output/finish_h5_source_frontier_pilot.py';s=(root/'output/finish_h5_joint_repair_pilot.py').read_text(encoding='utf-8')
s=s.replace('h5-joint-repair-pilot-20261018','h5-source-frontier-pilot-20261018').replace('h5_joint_repair_pilot','h5_source_frontier_pilot')
s=s.replace('# Joint-repair exchange pilot','# Source-frontier joint-repair pilot')
old='''    'the candidate repairs only the selected receiver/source pair jointly, checks',
    'both exact containers and lowers source parts using existing bounded sampling.',
'''
new='''    'the candidate derives a target from the remaining source after selection.',
    'It charges the scan and keeps the original crop when no member remains.',
    'The joint helper repairs only the selected pair, checks both exact containers',
    'and lowers source parts using the existing bounded sampling.',
'''
assert old in s;s=s.replace(old,new)
old='''    '[Qualification](h5-joint-repair-preparation-20261018.md) retains all 165 passing',
    'native tests, including 157 unchanged prior bodies and eight new policy tests.',
    'Thirty-two independent saved-layout checks and 93 filled-outer pairs pass,',
    'with every prior witness exact, public replay, reconstruction, lint and build.','',
'''
new='''    '[Qualification](h5-frontier-preparation-20261018.md) retains all 171 passing',
    'native tests, including 166 unchanged prior bodies and five new policy tests.',
    'All 139 prior recorded outputs remain exact. Seven new-policy saved-layout',
    'checks and 34 filled-outer pairs pass, plus six public outcomes, six public',
    'CLI checks and 856 public filled-outer pairs. Strict lint and build pass.','',
'''
assert old in s;s=s.replace(old,new)
needle="(OUT.parent/(OUT.name+'.md')).write_text"
pos=s.index(needle)
extra='''frontier_rows=[]
for row in result['records']:
    stats=row.get('stats',{});count=stats.get('source_frontier_attempts',0)
    assert type(count) is int and 0<=count<=stats.get('extended_exchange_attempts',0)
    if row['arm']!='candidate':assert count==0
    frontier_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | {'attempted':count})
write(OUT/'frontier-counters.json',{'attempted':sum(r['attempted'] for r in frontier_rows),'records':frontier_rows})
lines += ['## Exposed source targets','',
    '| Job | Kerf mm | Proposals with a tighter crop |', '| --- | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in frontier_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {sum(r['attempted'] for r in selected)} |")
lines += ['', 'This counter identifies proposed joint calls with a tighter source crop,',
    'including a helper that declines an expired call. It does not identify which',
    'targeted calls completed, measure time, or establish final material benefit.','']
'''
s=s[:pos]+extra+s[pos:];p.write_text(s,encoding='utf-8',newline='\n')
q=root/'output/audit_h5_source_frontier_pilot.py'
q.write_text((root/'output/audit_h5_joint_repair.py').read_text(encoding='utf-8').replace('h5-joint-repair-pilot-20261018','h5-source-frontier-pilot-20261018'),encoding='utf-8',newline='\n')
# Compare executable methods, not just labels or prose.
def functions(path):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef)}
old,new=functions(parent),functions(target)
same=['blocks','summarize','case','measure','require_runner_stopped','require_measurements_finished']
for name in same:assert old[name]==new[name],name
sys.path.insert(0,str(root/'scripts'));pilot=importlib.import_module('h5_source_frontier_pilot');previous=importlib.import_module('h5_joint_repair_pilot')
for name in ['JOBS','ARMS','SEEDS','KERFS','CPUS','CLI','H4']:assert getattr(pilot,name)==getattr(previous,name),name
for arm in ['normal','baseline']:assert pilot.ENGINES[arm]==previous.ENGINES[arm]
tests=importlib.import_module('test_h5_early_exchange_pilot');tests.pilot=pilot
names=['test_original_material_failures_stay_failures_despite_improvement',
    'test_missing_duplicate_and_failed_seeds_never_get_complete_comparison',
    'test_nonfinite_invalid_scores_and_missing_cut_savings_are_not_scored',
    'test_each_block_keeps_all_arms_and_balances_order_across_seeds',
    'test_expired_session_preserves_failure_without_starting_a_process']
suite=unittest.TestSuite(tests.PilotSummaryTests(name) for name in names)
with (probe/'frontier-pilot-harness-tests.log').open('x',encoding='utf-8',newline='\n') as log:
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
assert result.wasSuccessful() and result.testsRun==5
write(probe/'frontier-paired-method-review.json',{'parent':str(parent.relative_to(root)),'parent_sha256':digest(parent),
    'runner_sha256':digest(target),'AST_identical_functions':same,'five_adversarial_tests_passed':True,
    'normal_and_common_baseline_binaries_unchanged':True,'cases_kerfs_seeds_cpus_budgets_unchanged':True,
    'new_searches':0,'finish_sha256':digest(p),'geometry_audit_sha256':digest(q)})
shutil.copyfile(__file__,probe/'prepare-frontier-pilot-tools.py')
print(json.dumps({'runner_ready':True,'AST_identical_functions':same,'adversarial_tests_passed':5,'new_searches':0}))
