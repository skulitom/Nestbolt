"""Wait for the identified tagless build, then check its actual downloads once."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys
import time
import traceback

root = Path(__file__).resolve().parents[1]
out = root/'output/depth-package-sequence-20261016'
out.mkdir(exist_ok=False)
run = '38854620093'
commit = '23442be38ee2e881669e753bc405ab3269ff1b39'
helpers = ['prepare_depth_dryrun_verification.py', 'report_preview_depth_dryrun.py']
hashes = {name: sha256((root/'output'/name).read_bytes()).hexdigest() for name in helpers}

def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')

write(out/'opened.json', {'workflow_run':run, 'commit':commit,
    'started':datetime.now(timezone.utc).isoformat(), 'helper_hashes':hashes,
    'dry_run_only':True, 'release_or_registry_publication':False})
stages = []
try:
    expires = time.monotonic()+3600
    while True:
        raw = subprocess.check_output(['gh','run','view',run,'--json',
            'status,conclusion,headSha,event,url'], cwd=root, timeout=90)
        workflow = json.loads(raw)
        assert workflow['headSha'] == commit and workflow['event'] == 'workflow_dispatch'
        if workflow['status'] == 'completed':
            (out/'workflow.json').write_bytes(raw)
            assert workflow['conclusion'] == 'success', 'Preserve failed workflow; do not rerun automatically'
            break
        assert time.monotonic() < expires, 'Package wait expired; original workflow remains untouched'
        time.sleep(60)
    assert all(sha256((root/'output'/name).read_bytes()).hexdigest() == value
               for name,value in hashes.items())
    for name in [helpers[0], 'verify_preview_depth_dryrun.py', helpers[1]]:
        log = out/(name+'.log')
        with log.open('wb') as stream:
            result = subprocess.run([sys.executable, str(root/'output/ccd1.py'),
                sys.executable, '-X', 'utf8', str(root/'output'/name)],
                cwd=root, stdout=stream, stderr=subprocess.STDOUT, timeout=900)
        stage = {'helper':name, 'exit_code':result.returncode,
            'log_sha256':sha256(log.read_bytes()).hexdigest()}
        stages.append(stage)
        write(out/'progress.json',stages)
        print(json.dumps(stage),flush=True)
        assert result.returncode == 0, 'Preserve original verification failure; investigate without rerunning'
    write(out/'completed.json', {'stages':stages, 'dry_run_only':True,
        'release_created':False, 'milestone_closed':False})
except BaseException:
    write(out/'interruption.json', {'error':traceback.format_exc(), 'stages':stages})
    raise
