"""Prepare the unchanged matched method for the qualified joint-repair policy."""
from pathlib import Path
from hashlib import sha256
import ast
import json
import shutil

root=Path(__file__).resolve().parents[1]
probe=root/'output/h5-joint-repair-probe-20261018'
parent=root/'scripts/h5_assignment_bridge_pilot.py'
target=root/'scripts/h5_joint_repair_pilot.py'
assert not target.exists()
def write(p,s):p.write_text(s,encoding='utf-8',newline='\n')
def adapt(s):return s.replace('h5-assignment-bridge','h5-joint-repair').replace('h5_assignment_bridge','h5_joint_repair').replace('Assignment-bridge','Joint-repair')
s=adapt(parent.read_text(encoding='utf-8'))
end=s.index('"""',3)+3
s='''"""Paired development pilot of bounded joint repair of a selected sheet pair.

Four frozen H5 jobs, both kerfs, seeds 0-2 and matched 60-second wall budgets.
The isolated candidate retains the original short exchange phase. Within the
remaining original allowance it repairs receiver/source membership jointly,
rechecks both exact containers and lowers source members with existing bounded
sampling. Material-flat steps need canonical source-area descent; sequences
commit only after strict whole-job improvement, otherwise layout, tracker and
accepted counts roll back. The original four-step cap, deadline, validation
reserve and geometry guards remain. All 165 native tests, unchanged prior
witnesses, public replay and independent geometry checks qualify this candidate.
This descriptive pilot cannot close H5 or establish a comparative quality claim.
"""'''+s[end:]
s=s.replace("previous = ROOT/'benchmarks/results/h5-extended-repair-pilot-20261018'", "previous = ROOT/'benchmarks/results/h5-assignment-bridge-pilot-20261018'")
s=s.replace("require_runner_stopped(load(previous/'opened.json'), 'h5_extended_repair_pilot.py')", "require_runner_stopped(load(previous/'opened.json'), 'h5_assignment_bridge_pilot.py')")
s=s.replace("PROBE/'preparation.json'", "PROBE/'policy-preparation.json'")
s=s.replace("PROBE/'bridge-checks/checks.json'", "PROBE/'joint-checks/checks.json'")
s=s.replace(", PROBE/'reconstruction.json'", "")
s=s.replace("'Isolated assignment-bridge candidate, common-line search bonus on'", "'Isolated joint-repair candidate, common-line search bonus on'")
s=s.replace("'previous_failed_pilot': 'benchmarks/results/h5-extended-repair-pilot-20261018/results.json'", "'previous_failed_pilot': 'benchmarks/results/h5-assignment-bridge-pilot-20261018/results.json'")
needle="    paths.extend(ROOT/row['path'] for row, _ in load_cases())"
assert s.count(needle)==1
s=s.replace(needle,"""    paths.extend([previous/'verification.json', previous/'interpretation.json',
                  previous/'fixed-inventory-area.json',
                  PROBE/'public-checks/filled-outer-audit.json',
                  PROBE/'pilot-harness-tests.log', PROBE/'paired-method-review.json',
                  PROBE/'counter-audit-method.json',
                  ROOT/'output/finish_h5_joint_repair_pilot.py',
                  ROOT/'output/audit_h5_joint_repair.py'])
"""+needle)
compile(s,str(target),'exec');write(target,s)
def funcs(text):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
old,new=funcs(parent.read_text(encoding='utf-8')),funcs(s)
names=['blocks','summarize','case','measure','require_runner_stopped','require_measurements_finished']
assert all(old[n]==new[n] for n in names)
write(probe/'paired-method-review.json',json.dumps({'parent':parent.relative_to(root).as_posix(),
    'parent_sha256':sha256(parent.read_bytes()).hexdigest(),'runner_sha256':sha256(target.read_bytes()).hexdigest(),
    'AST_identical_functions':names,'jobs_kerfs_seeds_arms_cpus_seconds_unchanged':True,
    'new_searches':0},indent=2)+'\n')

h=adapt((root/'output/check_h5_assignment_bridge_harness.py').read_text(encoding='utf-8'))
write(root/'output/check_h5_joint_repair_harness.py',h)
f=adapt((root/'output/finish_h5_assignment_bridge_pilot.py').read_text(encoding='utf-8'))
a=f.index("    'The candidate retains the original short exchange phase")
b=f.index("    'Four jobs, two kerfs",a)
f=f[:a]+'''    'The original short phase runs first. Within the remaining original allowance,',
    'the candidate repairs only the selected receiver/source pair jointly, checks',
    'both exact containers and lowers source parts using existing bounded sampling.',
    'Material-flat steps require canonical source-area descent. A joint sequence',
    'commits only after strict whole-job material improvement; otherwise layout,',
    'tracker and accepted counts roll back. The original deadline, four-step cap,',
    'validation reserve and geometry guards remain.',
    '[Qualification](h5-joint-repair-preparation-20261018.md) retains all 165 passing',
    'native tests, including 157 unchanged prior bodies and eight new policy tests.',
    'Thirty-two independent saved-layout checks and 93 filled-outer pairs pass,',
    'with every prior witness exact, public replay, reconstruction, lint and build.','',
'''+f[b:]
needle='fill_rows=[]'
assert f.count(needle)==1
f=f.replace(needle,'''joint_rows=[]
for row in result['records']:
    stats=row.get('stats',{})
    names=['joint_repair_attempts','joint_repair_completed','joint_repair_failed','joint_repair_expired','joint_exchanges']
    counts={n:stats.get(n,0) for n in names}
    assert all(type(v)is int and v>=0 for v in counts.values())
    attempted,completed,failed,expired,accepted=[counts[n] for n in names]
    assert attempted==completed+failed+expired
    assert attempted<=stats.get('extended_exchange_attempts',0)
    assert accepted<=completed and accepted<=stats.get('directed_exchanges',0)
    assert accepted==stats.get('extended_exchanges',0)==stats.get('assignment_bridge_committed',0)
    assert stats.get('assignment_bridge_steps',0)<=completed
    assert accepted+stats.get('assignment_bridge_rolled_back',0)<=completed
    if row['arm']!='candidate':assert not any(counts.values())
    joint_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | counts)
joint={name:sum(r[name] for r in joint_rows) for name in names}
joint['records']=joint_rows;write(OUT/'joint-counters.json',joint)
lines += ['## Joint repairs','',
    '| Job | Kerf mm | Attempted | Completed | Failed | Expired | Committed steps |',
    '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in joint_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    values=[sum(r[name] for r in selected) for name in names]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {' | '.join(map(str,values))} |")
lines += ['', 'Attempts equal completed plus failed plus expired. Pair completion',
    'does not imply whole-job acceptance. Accepted counts include only committed',
    'sequences and exclude rolled-back provisional steps. Pair-selection counters',
    'refer to the initial proposal; joint repair can move additional members.',
    'These counts do not measure repair durations or final quality benefit.','']
'''+needle)
compile(f,'joint finisher','exec');write(root/'output/finish_h5_joint_repair_pilot.py',f)
audit=adapt((root/'output/audit_h5_assignment_bridge.py').read_text(encoding='utf-8'))
write(root/'output/audit_h5_joint_repair.py',audit)
write(probe/'counter-audit-method.json',json.dumps({
    'parent':'output/finish_h5_assignment_bridge_pilot.py',
    'parent_sha256':sha256((root/'output/finish_h5_assignment_bridge_pilot.py').read_bytes()).hexdigest(),
    'archive_metric_score_and_existing_counter_checks_retained':True,
    'new_counter_checks':['attempts equal completed plus failed plus expired',
        'attempts bounded by extended attempts','accepted bounded by completed and all accepted',
        'joint accepted equals extended accepted and committed bridge steps',
        'provisional steps bounded by completed repairs','rolled-back steps excluded from accepted',
        'baseline joint counters zero'],
    'finisher_sha256':sha256((root/'output/finish_h5_joint_repair_pilot.py').read_bytes()).hexdigest(),
    'new_searches':0},indent=2)+'\n')
print(json.dumps({'paired_AST_unchanged':names,'runner':str(target),'measurement_started':False}))
