"""Reconnect the unopened paired pilot to the preserved H4 recovery."""
from pathlib import Path
from hashlib import sha256
import ast
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h5-obstruction-set-recovered-pilot-20261016'
RUNNER=ROOT/'output/h5_obstruction_set_recovered_pilot.py'
old=(ROOT/'scripts/h5_obstruction_set_pilot.py').read_text(encoding='utf-8')
new=old.replace('h4-preview-depth-release-20261016','h4-depth-reboot-recovery-20261016').replace('h4-preview-depth-scale-plan-20261016','h4-depth-recovered-scale-plan-20261016')
new=new.replace('from cutting_development_set import ROOT,',"import sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))\n\nfrom cutting_development_set import ROOT,")
new=new.replace("(H4, 'h4_preview_matrix.py'), (sequence, 'continue_preview_depth_checks.py')", "(H4, 'h4_depth_reboot_recovery.py'), (sequence, 'continue_recovered_depth_checks.py')")
new=new.replace("assert verification['all_artifact_checks_passed'] and verification['new_attempts'] == 603", "assert verification['all_artifact_checks_passed']\n    assert verification['completed_current_build_outcomes'] == 603\n    assert verification['retained_current_build_outcomes'] == 402 and verification['new_recovery_outcomes'] == 201\n    assert verification['original_infrastructure_interruption_preserved']\n    assert verification['frozen_v1_outcomes'] == 195\n    if terminal.name == 'completed.json':\n        fidelity = load(sequence/'curve-export-fidelity/verification.json')\n        assert fidelity['all_checks_pass'] and fidelity['both_scale_workflows_pass']\n        for kind in ['curves','g5']:\n            scale = load(ROOT/fidelity[kind]/'summary.json')\n            assert scale['passes'] and scale['source_guards_passed']\n            assert scale['archive']['crc_and_member_hashes_verified']\n            assert digest(ROOT/fidelity[kind]/'raw.zip') == scale['archive']['sha256']\n        visual = load(sequence/'visual-review.json')\n        assert visual['reviewed'] and len(visual['screenshots']) == 4\n        assert all(r['reviewed'] and digest(ROOT/r['path'])==r['sha256'] for r in visual['screenshots'])")
new=new.replace("H4/'plan.json', CLI,", "H4/'plan.json', ROOT/'benchmarks/results/h4-depth-recovered-scale-plan-20261016/plan.json', CLI,")
new=new.replace("'requires_completed_current_preview_and_scale_sequence': True,", "'requires_completed_current_preview_and_scale_sequence': True,\n        'original_unopened_pilot_preserved': 'benchmarks/results/h5-obstruction-set-pilot-20261016',\n        'only_prerequisite_and_evidence_paths_changed': True,\n        'recovery_preserves_completed_current_outcomes': 402,\n        'recovery_new_Firefox_outcomes': 201,")
assert new!=old
before,after=ast.parse(old),ast.parse(new)
for name in ['blocks','summarize','case','measure']:
    a=next(n for n in before.body if isinstance(n,ast.FunctionDef) and n.name==name)
    b=next(n for n in after.body if isinstance(n,ast.FunctionDef) and n.name==name)
    assert ast.dump(a)==ast.dump(b),name
assert not RUNNER.exists() and not OUT.exists()
RUNNER.write_text(new,encoding='utf-8',newline='\n')
subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),'python',str(RUNNER),'prepare','--out',str(OUT)],cwd=ROOT,check=True)
finisher=(ROOT/'output/finish_h5_obstruction_set_pilot.py').read_text(encoding='utf-8')
finisher=finisher.replace('h5-obstruction-set-pilot-20261016','h5-obstruction-set-recovered-pilot-20261016').replace('h5_obstruction_set_pilot','h5_obstruction_set_recovered_pilot')
finisher=finisher.replace("sys.path.insert(0,str(ROOT/'scripts'))", "sys.path.insert(0,str(ROOT/'scripts'))\nsys.path.insert(0,str(ROOT/'output'))")
finisher=finisher.replace("'remains required, and no original acceptance limit changes. Completed',\n    'milestone weight remains 45%.',", "'remains required, and no original acceptance limit changes. This pilot',\n    'earns no completed H5 milestone weight.',")
ast.parse(finisher)
finish=ROOT/'output/finish_h5_obstruction_set_recovered_pilot.py'
assert not finish.exists()
finish.write_text(finisher,encoding='utf-8',newline='\n')
(OUT/'finish.py').write_bytes(finish.read_bytes())
(OUT/'prepare.py').write_bytes(Path(__file__).read_bytes())
oldplan=json.loads((ROOT/'benchmarks/results/h5-obstruction-set-pilot-20261016/plan.json').read_bytes())
newplan=json.loads((OUT/'plan.json').read_bytes())
for key in ['jobs','kerfs_mm','seeds','seconds','arms','blocks','attempts','cpus','concurrency','pairing','geometry','search_external_timeout_seconds','validation_export_timeout_seconds','revalidation_absolute_tolerance','whole_session_limit_seconds','failed_attempts','decision']:
    assert oldplan[key]==newplan[key],key
assert not (ROOT/'benchmarks/results/h5-obstruction-set-pilot-20261016/opened.json').exists()
evidence={'only_prerequisite_and_evidence_paths_changed':True,'same_AST_functions':['blocks','summarize','case','measure'],
    'original_plan_sha256':sha256((ROOT/'benchmarks/results/h5-obstruction-set-pilot-20261016/plan.json').read_bytes()).hexdigest(),
    'runner_sha256':sha256(RUNNER.read_bytes()).hexdigest(),'finisher_sha256':sha256(finish.read_bytes()).hexdigest(),
    'original_pilot_unopened':True,'measurement_started':False,'H5_complete':False}
(OUT/'derivation.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(evidence))
