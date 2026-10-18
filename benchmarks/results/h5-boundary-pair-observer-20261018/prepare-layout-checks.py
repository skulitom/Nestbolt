"""Conditional exact-copy observer for a failed boundary-pair pilot."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,difflib,json,shutil,sys
root=Path(__file__).resolve().parents[1]
pilot=root/'benchmarks/results/h5-boundary-pair-pilot-20261018'
out=root/'output/h5-boundary-pair-observer-20261018';old=root/'output/h5-boundary-pair-probe-20261018/candidate';work=out/'workspace'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert load(pilot/'verification.json')['valid']==72 and load(pilot/'filled-outer-audit.json')['all_holes_reserved']
assert any(not p['candidate_within_original_material_limit'] for p in load(pilot/'results.json')['summary']['pairs'])
out.mkdir();shutil.copytree(old,work)
rel='crates/core/src/sheets/vstrip/exchange.rs';path=work/rel
original=path.read_text(encoding='utf-8');text=original
changes=load(root/'output/h5-boundary-observer-20261018/substitutions.json')
for before,after in changes:
    assert text.count(before)==1;text=text.replace(before,after)
reverse=text
for before,after in reversed(changes):
    assert reverse.count(after)==1;reverse=reverse.replace(after,before)
assert reverse==original and text.split('#[cfg(test)]',1)[1]==original.split('#[cfg(test)]',1)[1]
path.write_text(text,encoding='utf-8',newline='\n')
(out/'substitutions.json').write_text(json.dumps(changes,indent=2)+'\n',encoding='utf-8',newline='\n')
(out/'instrumentation.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='boundary-pair/'+rel,tofile='boundary-pair-observer/'+rel)),encoding='utf-8',newline='\n')
sys.path.insert(0,str(root/'scripts'));from h2_import_audit import source_digest
plan={'utc':datetime.now(timezone.utc).isoformat(),'purpose':__doc__,'old_source':str(old),
      'source_files':[{'path':p.relative_to(old).as_posix(),'sha256':digest(p)} for p in sorted(old.rglob('*')) if p.is_file()],
      'changed_file':rel,'changed_files':[rel],'production_digest':source_digest(),
      'target':str(root/'output/h5-boundary-pair-observer-target-20261018'),
      'all_130_prior_tests_unchanged':True,'exact_preformat_reversal':True,
      'decisions_budgets_work_charges_unchanged':True,'trace_overhead_can_change_wall_trajectory':True,'measured_search_started':False}
(out/'preparation.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8',newline='\n');shutil.copyfile(__file__,out/'prepare.py')
def adapt(s):
    return s.replace('h5-boundary-observer','h5-boundary-pair-observer').replace('h5_boundary_observer','h5_boundary_pair_observer').replace('h5-boundary-priority','h5-boundary-pair').replace('h5_boundary_priority','h5_boundary_pair')
def save(name,s):
    compile(s,name,'exec');(root/'output'/name).write_text(s,encoding='utf-8',newline='\n')
for name in ['build_h5_boundary_observer.py','check_h5_boundary_observer_source.py','check_h5_boundary_observer_reader.py','check_h5_boundary_observer_layouts.py','finish_h5_boundary_observer.py']:
    s=adapt((root/'output'/name).read_text(encoding='utf-8')).replace('all_126','all_130')
    save(name.replace('h5_boundary_observer','h5_boundary_pair_observer'),s)
reference=root/'scripts/h5_boundary_observer.py';before=reference.read_text(encoding='utf-8');s=adapt(before)
s=s.replace('boundary-priority candidate','boundary-pair candidate')
runner=root/'scripts/h5_boundary_pair_observer.py';assert not runner.exists();compile(s,str(runner),'exec');runner.write_text(s,encoding='utf-8',newline='\n')
def fn(text,name):return next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name==name)
for name in ['run','pose_key','check_traces','parse_log','read_trace']:
    assert ast.dump(fn(s,name))==ast.dump(fn(before,name))
method={'reference':reference.relative_to(root).as_posix(),'reference_sha256':digest(reference),
        'measurement_function_AST_exact':True,'case_method_reused_unchanged':True,'pose_reader_functions_AST_exact':True,'runner_sha256':digest(runner)}
(out/'runner-method.json').write_text(json.dumps(method,indent=2)+'\n',encoding='utf-8',newline='\n')
s=adapt((root/'output/seal_h5_boundary_observer.py').read_text(encoding='utf-8')).replace('126','130').replace('completed boundary-priority pilot','completed boundary-pair pilot')
start=s.index('for name in [');end=s.index("files['runner.py']",start)
s=s[:start]+'''for name in ['prepare_h5_boundary_pair_observer.py','build_h5_boundary_pair_observer.py',
             'check_h5_boundary_pair_observer_reader.py','check_h5_boundary_pair_observer_source.py',
             'seal_h5_boundary_pair_observer.py','record_h5_boundary_pair_observer_preparation.py']:
    files['helpers/'+name]=root/'output'/name
'''+s[end:]
save('seal_h5_boundary_pair_observer.py',s)
s=adapt((root/'output/record_h5_boundary_observer_preparation.py').read_text(encoding='utf-8')).replace('126','130')
s=s.replace('**N4 boundary-priority outcome, 2026-10-18:**','**N4 boundary-pair outcome, 2026-10-18:**')
s=s.replace('exact boundary-copy observation','boundary-pair observation').replace('Qualify exact boundary-copy observation','Qualify boundary-pair observation')
save('record_h5_boundary_pair_observer_preparation.py',s)
print(json.dumps({'isolated_observer_prepared':True,'unchanged_tests':130,'unchanged_pose_reader':True,'new_measurements':0}))
