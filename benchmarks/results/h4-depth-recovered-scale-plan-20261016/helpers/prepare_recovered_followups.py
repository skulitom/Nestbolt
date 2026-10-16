"""Derive recovery-aware follow-ups without modifying original frozen runners."""
from pathlib import Path
import ast
import json
import subprocess
import sys
from hashlib import sha256

ROOT=Path(__file__).resolve().parents[1]
OLD='h4-preview-depth-scale-plan-20261016'
NEW='h4-depth-recovered-scale-plan-20261016'
MATRIX='h4-depth-reboot-recovery-20261016'

def replace(text,old,new):
    assert old in text, old
    return text.replace(old,new)

def save(name,text):
    ast.parse(text)
    p=ROOT/'output'/name
    assert not p.exists()
    p.write_text(text,encoding='utf-8',newline='\n')
    return p

report=(ROOT/'output/report_h4_preview_depth_release.py').read_text(encoding='utf-8')
report=replace(report,'h4-preview-depth-release-20261016',MATRIX)
report=replace(report,"'All 603 new layouts and 195 reused frozen-v1 layouts validate. These are',", "f\"{sum(r['status']=='valid' for e in ['native','chrome','firefox'] for r in result['records'][e])}/603 completed current-build layouts and 195 frozen-v1 layouts validate. These are\",")
report=replace(report,"'67 jobs. Native, Chrome and Firefox each run all 67 at 60 seconds and seeds',\n    '0–2, giving 201 outcomes per engine. Only the 195 sealed frozen-v1 outcomes',\n    'are reused. There are no held-out jobs, final seeds or competitor claims.',", "'67 jobs. Each engine covers all 67 at 60 seconds and seeds 0–2.',\n    'The 201 native and 201 Chrome outcomes completed before the servicing reboot',\n    'and are retained unchanged alongside 195 frozen-v1 outcomes. The recovery',\n    'runs only the 201 missing Firefox outcomes. The original Firefox batch had',\n    'started but saved no outcomes; its precise number of started jobs is unknown.',\n    'The interrupted session remains interrupted. There are no held-out jobs,',\n    'final seeds or competitor claims.',")
report=replace(report,"'and environment guards stay unchanged.',", "'and original environment-override guards stay unchanged. The new boot and OS',\n    'environment are recorded separately in the recovery plan.',")
report=replace(report,"f\"The complete run took {result['wall_seconds']/60:.3f} minutes, below its four-hour cap.\",", "f\"The Firefox recovery took {result['wall_seconds']/60:.3f} minutes, below its one-hour cap.\",\n    'This is not the elapsed time of all three engines; no continuous complete',\n    'session is claimed and the original four-hour session is not extended.',")
report=replace(report,"'validation of the public examples. All six browser batches succeed with',\n    'zero affinity deviations.',", "'validation of the public examples. Original Chrome and recovered Firefox',\n    'batch execution and affinity records are preserved in their respective archives.',")
report=replace(report,"'It preserves every new attempt, validation, original plan, browser/process',\n    'record and exact measured engine/site. CRC, member size and SHA-256 checks',\n    'all pass. Reused v1 bytes remain in their verified preceding archive.',", "'It preserves every recovery outcome, validation, plan and browser/process record,',\n    'including the original interrupted-session archive and exact measured build.',\n    'The nested original archive preserves every completed native/Chrome outcome',\n    'and the interrupted first Firefox batch. CRC, member sizes and SHA-256 checks',\n    'all pass. Frozen-v1 bytes remain in their verified preceding archive.',")
report=replace(report,"assert verified['all_artifact_checks_passed'] and inventory['crc_and_every_member_verified']", "assert verified['all_artifact_checks_passed'] and inventory['crc_and_every_member_verified']\nassert verified['retained_current_build_outcomes']==402 and verified['new_recovery_outcomes']==201\nassert verified['original_infrastructure_interruption_preserved']\nassert result['original_interruption_preserved'] and not result['original_session_claimed_complete']")
report=replace(report,'# Integrated tree-depth preview: full H4 comparison — 2026-10-16','# Integrated tree-depth preview: recovered full H4 comparison — 2026-10-16')
save('report_h4_recovered_depth.py',report)

check=(ROOT/'output/check_depth_scale_exports.py').read_text(encoding='utf-8')
save('check_recovered_depth_scale_exports.py',replace(check,OLD,NEW))
seal=(ROOT/'output/h4_depth_scale_report.py').read_text(encoding='utf-8')
save('h4_recovered_depth_scale_report.py',replace(seal,OLD,NEW))

sequence=(ROOT/'output/continue_preview_depth_checks.py').read_text(encoding='utf-8')
sequence=replace(sequence,OLD,NEW)
sequence=replace(sequence,'h4-preview-depth-release-20261016',MATRIX)
sequence=replace(sequence,'continue_preview_depth_checks.py','continue_recovered_depth_checks.py')
sequence=replace(sequence,"['python', 'output/finalize_h4_preview_depth_release.py']", "['python', 'output/h4_depth_reboot_recovery.py', 'verify']")
sequence=replace(sequence,'output/finalize_h4_preview_depth_release.py','output/h4_depth_reboot_recovery.py')
sequence=replace(sequence,'report_h4_preview_depth_release.py','report_h4_recovered_depth.py')
sequence=replace(sequence,'check_depth_scale_exports.py','check_recovered_depth_scale_exports.py')
sequence=replace(sequence,"active = any('h4_preview_matrix.py' in arg for arg in psutil.Process(pid).cmdline())", "arguments = psutil.Process(pid).cmdline()\n            active = 'run' in arguments and any(arg.endswith('h4_depth_reboot_recovery.py') for arg in arguments)")
sequence=replace(sequence,"'Original matrix interruption retained; investigate it'", "'Recovery interruption retained; investigate it'")
sequence=replace(sequence,"'exclusive_measurements_until_complete': True,", "'original_interrupted_session_preserved': True,\n        'recovery_retains_current_outcomes': 402,\n        'recovery_new_Firefox_outcomes': 201,\n        'original_sequence_never_started': True,\n        'exclusive_measurements_until_complete': True,")
sequence=replace(sequence,"'output/check_recovered_depth_scale_exports.py','output/h4_curve_export_check_v3.py']", "'output/check_recovered_depth_scale_exports.py','output/h4_curve_export_check_v3.py',\n            'output/h4_recovered_depth_scale_report.py','output/prepare_recovered_followups.py']")
sequence=replace(sequence,"(out/'runner.py').write_bytes(Path(__file__).read_bytes())", "(out/'runner.py').write_bytes(Path(__file__).read_bytes())\n    (out/'helpers').mkdir()\n    for name in plan['helpers']:\n        (out/'helpers'/Path(name).name).write_bytes((root/name).read_bytes())\n    (out/'recovery-preparation-report.md').write_bytes((matrix.parent/(matrix.name+'.md')).read_bytes())")
save('continue_recovered_depth_checks.py',sequence)
subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),'python','output/continue_recovered_depth_checks.py','prepare'],cwd=ROOT,check=True)
print(json.dumps({'prepared':NEW,'searches_started':0,'original_runners_changed':False}))
