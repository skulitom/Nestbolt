"""Continue a frozen queue in bounded chunks within one declared time allowance."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
import uuid

import comparison_session as sessions
from svgnest import digest, write


def select_chunk(pending, remaining_seconds, remaining_attempts, tool):
    # Reserve one minute for final evidence and release. Each native runner has
    # its own process deadlines; the 400-second allowance covers preparation,
    # validation and teardown. Anode also has its external desktop-job timeout.
    allowance = min(remaining_seconds-60, 27*60 if tool=='deepnest' else 3*3600)
    selected = []
    for slot in pending[:min(30,remaining_attempts)]:
        cost = slot['seconds']+400
        if cost>allowance:break
        selected.append(slot)
        allowance-=cost
    return selected


def continue_queue(name, tool, seconds, max_attempts):
    if not 600<=seconds<=10800 or not 1<=max_attempts<=2000:
        raise ValueError('Use a 600..10800-second envelope and 1..2000 attempts')
    if tool=='deepnest' and seconds>27*60:
        raise ValueError('Desktop envelopes must remain below the Anode job lifetime')
    directory=sessions.session_dir(name)
    manifest=json.loads((directory/'manifest.json').read_bytes())
    if tool not in manifest['settings']:raise ValueError('Tool absent from frozen session')
    sessions.verify_sources(manifest)
    record={'started_at':datetime.now(timezone.utc).isoformat(),'pid':os.getpid(),
        'name':name,'tool':tool,'maximum_seconds':seconds,'maximum_attempts':max_attempts,
        'manifest_sha256':digest(directory/'manifest.json'),'controller_sha256':digest(Path(__file__)),
        'chunks':[],'completed_attempts':0}
    folder=directory/'envelopes'/str(uuid.uuid4())
    folder.mkdir(parents=True,exist_ok=False)
    write(folder/'started.json',record)
    start=time.monotonic()
    try:
        while record['completed_attempts']<max_attempts:
            pending=sessions.pending(directory,manifest,tool)
            if not pending:
                record['status']='queue_complete'
                break
            chosen=select_chunk(pending,seconds-(time.monotonic()-start),max_attempts-record['completed_attempts'],tool)
            if not chosen:
                record['status']='time_allowance_exhausted'
                break
            sessions.execute(name,tool,len(chosen))
            entry={'slots':[s['id'] for s in chosen],'finished_at':datetime.now(timezone.utc).isoformat()}
            with (folder/'chunks.jsonl').open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(entry)+'\n')
            record['chunks'].append(entry)
            record['completed_attempts']+=len(chosen)
        else:record['status']='attempt_limit_reached'
    except Exception as error:
        record.update(status='failed',error=f'{type(error).__name__}: {error}')
        raise
    finally:
        record.update(finished_at=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start)
        write(folder/'finished.json',record)
        print(json.dumps({'envelope':str(folder),'status':record['status'],
                          'completed_attempts':record['completed_attempts']}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name',required=True)
    parser.add_argument('--tool',choices=sessions.MODULES,required=True)
    parser.add_argument('--seconds',type=int,default=3600)
    parser.add_argument('--max-attempts',type=int,default=100)
    args=parser.parse_args()
    continue_queue(args.name,args.tool,args.seconds,args.max_attempts)
