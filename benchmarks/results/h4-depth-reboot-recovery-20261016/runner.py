"""Recover the missing Firefox phase after the recorded Windows servicing restart.

Keep all 402 completed current-build native/Chrome outcomes and all 195 frozen-v1
outcomes. Preserve the interrupted original phase with zero Firefox outputs.
Run the 201 missing Firefox outcomes once with the original jobs/seeds/budgets.
This does not relabel the interrupted original session as a completed run.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback
import zipfile
import psutil

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'benchmarks/results/h4-preview-depth-release-20261016'
OLD_SEQUENCE=ROOT/'benchmarks/results/h4-preview-depth-scale-plan-20261016'
OUT=ROOT/'benchmarks/results/h4-depth-reboot-recovery-20261016'
sys.path.insert(0,str(ROOT/'scripts'))
import h4_preview_matrix as preview
import h4_quality as quality
import h4_full_matrix as full
from g5_browser import serve

load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def relative(p):return p.relative_to(ROOT).as_posix()
def utc(t):return datetime.fromtimestamp(t,timezone.utc).isoformat()

def require_original_stopped():
    for folder,script in [(OLD,'h4_preview_matrix.py'),(OLD_SEQUENCE,'continue_preview_depth_checks.py')]:
        marker=load(folder/'opened.json')
        try:arguments=psutil.Process(marker['pid']).cmdline()
        except psutil.NoSuchProcess:arguments=[]
        assert not any(script in arg for arg in arguments), 'Original process is still live'
    assert not (OLD/'results.json').exists(), 'Original already completed; do not start recovery'
    assert not (OLD_SEQUENCE/'completed.json').exists()
    assert not list(OLD_SEQUENCE.glob('stage-*.log')), 'Scale sequence already started; review it'

def original_files():
    return sorted([p for p in OLD.rglob('*') if p.is_file()]+
                  [p for p in OLD_SEQUENCE.rglob('*') if p.is_file()])

def unchanged_original():
    expected=load(OUT/'original-files.json')
    files=original_files()
    assert {relative(p) for p in files}==set(expected)
    assert all(digest(p)==expected[relative(p)]['sha256'] and p.stat().st_size==expected[relative(p)]['bytes'] for p in files)

def validate_saved(records,rows):
    known={r['id']:r for r in rows}
    checked=[]
    for engine in ['native','chrome','firefox']:
        for record in records.get(engine,[]):
            if record['status']!='valid':
                checked.append({'engine':engine,'job':record['job'],'seed':record['seed'],'valid':False})
                continue
            folder=ROOT/record['directory']
            layout_raw=(folder/'layout.json').read_bytes()
            assert sha256(layout_raw).hexdigest()==record['layout_sha256']
            validation=load(folder/'validate-stdout.json')
            result=load(folder/('search-stdout.json' if engine=='native' else 'result.json'))
            assert validation['valid'] and result['validation']['valid']
            assert quality.equivalent(validation['metrics'],result['validation']['metrics'])==0
            assert record['maximum_metric_json_roundtrip_difference']==0
            assert validation['metrics']['normalized_material']==record['material']
            assert validation['metrics']['sheets_used']==record['sheets']
            row=known[record['job']]
            assert len(json.loads(layout_raw)['placements'])==sum(p['quantity'] for p in load(ROOT/row['path'])['parts'])
            case=load(folder/'case.json')
            assert all(case.get(k)==v for k,v in record.items() if k not in ['reused','source_archive'])
            if 'library' in row:
                public=load(folder/'public-validate-stdout.json')
                assert public['valid'] and quality.equivalent(public['metrics'],validation['metrics'])==0
            checked.append({'engine':engine,'job':record['job'],'seed':record['seed'],
                'valid':True,'layout_sha256':record['layout_sha256'],'metrics_identical':True,
                'all_requested_parts_present':True})
    return checked

def archive(paths,target):
    inventory={name:{'sha256':digest(p),'bytes':p.stat().st_size} for name,p in paths}
    assert len(inventory)==len(paths)
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,p in paths:z.write(p,name)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None and set(z.namelist())==set(inventory)
        for name,row in inventory.items():
            data=z.read(name)
            assert len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256']
    return {'archive':relative(target),'sha256':digest(target),'bytes':target.stat().st_size,
        'members':inventory,'crc_and_every_member_verified':True}

def summaries(records,plan,subset):
    selected=lambda ids:{k:[r for r in v if r['job'] in ids] for k,v in records.items()}
    return (full.summarize(selected(plan['full_ids']),plan['full_ids']),
        quality.summarize(selected(plan['subset_ids']),subset,[0,1,2],60))

def prepare():
    require_original_stopped()
    rows,development,subset=preview.cases();old=load(OLD/'plan.json')
    assert old['cases']==rows and preview.guards(rows)==old['guards']
    retained=load(OLD/'records.json')
    assert {k:len(v) for k,v in retained.items()}=={'v1':195,'native':201,'chrome':201,'firefox':0}
    assert retained['v1']==preview.baseline(development)
    expected={(r['id'],s) for r in rows for s in [0,1,2]}
    for engine in ['native','chrome']:
        assert {(r['job'],r['seed']) for r in retained[engine]}==expected
        assert all(r['status']=='valid' for r in retained[engine])
    assert {relative(p).removeprefix(relative(OLD)+'/firefox/') for p in (OLD/'firefox').rglob('*') if p.is_file()}=={
        's0/browser.json','s0/plan.json','s0/stdout.log','s0/stderr.log'}
    assert load(OLD/'firefox/s0/browser.json')['version']=='157.0'
    batches=[]
    for seed in [0,1,2]:
        folder=OLD/'chrome'/f's{seed}';execution=load(folder/'execution.json');config=load(folder/'plan.json')
        assert execution['exit_code']==0 and not execution['affinity_errors'] and execution['cpus']==quality.CPUS
        assert config['seed']==seed and config['seconds']==60 and config['concurrency']==8 and len(config['jobs'])==67
        batches.append({'seed':seed,'execution_sha256':digest(folder/'execution.json'),
            'browser':load(folder/'browser.json'),'wall_seconds':execution['wall_seconds']})
    checked=validate_saved(retained,rows);assert len(checked)==402 and all(r['valid'] for r in checked)
    OUT.mkdir(exist_ok=False)
    event_command="Get-WinEvent -FilterHashtable @{LogName='System';Id=12,13,1074;StartTime=[datetime]'2026-10-16T05:50:00Z';EndTime=[datetime]'2026-10-16T06:10:00Z'} | Where-Object { $_.ProviderName -eq 'Microsoft-Windows-Kernel-General' -or $_.ProviderName -eq 'User32' } | Select-Object @{Name='utc';Expression={$_.TimeCreated.ToUniversalTime().ToString('o')}},Id,ProviderName,RecordId,Message | ConvertTo-Json -Depth 3"
    raw_events=subprocess.check_output(['powershell','-NoProfile','-Command',event_command],cwd=ROOT)
    (ROOT/'output/h4-depth-restart-system-events.local.json').write_bytes(raw_events)
    events=json.loads(raw_events.decode('utf-8-sig'))
    assert {e['Id'] for e in events}=={12,13,1074}
    update=next(e for e in events if e['Id']==1074)
    assert 'MoUsoCoreWorker.exe' in update['Message'] and '0x80020010' in update['Message']
    restart={'observed_boot_utc':utc(psutil.boot_time()),'events':[{k:e[k] for k in ['utc','Id','ProviderName','RecordId']} for e in events],
        'restart_initiator':'Windows servicing / MoUsoCoreWorker.exe','reason_code':'0x80020010',
        'original_processes_absent':True,'original_Firefox_outputs':0,'original_Firefox_errors':0,
        'first_Firefox_batch_started':True,'precise_number_of_started_worker_jobs':'Not recorded; do not infer zero attempts from zero outputs.',
        'original_scale_sequence_started':False,'original_session_disposition':'Interrupted by servicing restart; never claimed complete or passing.'}
    write(OUT/'restart-evidence.json',restart)
    version_code="import {firefox} from './web/node_modules/playwright/index.mjs';import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';const executable=firefox.executablePath();const b=await firefox.launch({headless:true});console.log(JSON.stringify({version:b.version(),executable,sha256:createHash('sha256').update(readFileSync(executable)).digest('hex')}));await b.close();"
    browser=json.loads(subprocess.check_output(['node','--input-type=module','-e',version_code],cwd=ROOT))
    assert browser['version']=='157.0'
    files=original_files();write(OUT/'original-files.json',{relative(p):{'sha256':digest(p),'bytes':p.stat().st_size} for p in files})
    paths=[(relative(p),p) for p in files]
    paths.append(('qualified-build/nestbolt.exe',quality.CLI))
    paths.extend(('qualified-build/web/dist/'+p.relative_to(ROOT/'web/dist').as_posix(),p) for p in sorted((ROOT/'web/dist').rglob('*')) if p.is_file())
    inventory=archive(paths,OUT/'interrupted-session.zip');write(OUT/'interrupted-integrity.json',inventory)
    write(OUT/'retained-records.json',retained)
    native,subset_quality=summaries(retained,old,subset)
    write(OUT/'retained-verification.json',{'all_completed_current_records_verified':True,'records':checked,
        'retained_native':201,'retained_chrome':201,'retained_v1':195,'Chrome_batches':batches,
        'native_comparison':native['native_vs_v1'],'Chrome_full':native['browsers_vs_native']['chrome'],
        'Chrome_subset':subset_quality['comparisons']['chrome'],'H4_complete':False})
    plan={'scope':__doc__,'prepared_utc':datetime.now(timezone.utc).isoformat(),'commit':old['commit'],
        'cases':rows,'full_ids':old['full_ids'],'subset_ids':old['subset_ids'],'guards':old['guards'],
        'seeds':[0,1,2],'seconds':60,'cpus':quality.CPUS,'concurrency':8,'gates':old['gates'],
        'retained_completed_current_build':{'native':201,'chrome':201},'retained_frozen_v1':195,
        'new_attempts':{'firefox':201},'original_directory':relative(OLD),'original_plan_sha256':digest(OLD/'plan.json'),
        'original_archive_sha256':inventory['sha256'],'retained_records_sha256':digest(OUT/'retained-records.json'),
        'original_file_inventory_sha256':digest(OUT/'original-files.json'),'restart_evidence_sha256':digest(OUT/'restart-evidence.json'),
        'runner_sha256':digest(Path(__file__)),'firefox':browser,'recovery_session_cap_seconds':3600,
        'environment':{'platform':platform.platform(),'boot_utc':utc(psutil.boot_time()),'logical_cpus':psutil.cpu_count(),'physical_cpus':psutil.cpu_count(logical=False)},
        'restart_policy':'Only the interrupted/missing Firefox phase is recovered. No completed outcome is replaced or selected by score; no change to build, jobs, seeds, budgets or bounds.',
        'original_interrupted_session_never_relabelled':True,'held_out_geometry_read':False,
        'source_build_and_measurement_freeze_until_recovery_and_scale_sequence_finish':True,
        'scale_and_full_requirement_audit_still_separate':True}
    write(OUT/'plan.json',plan);shutil.copyfile(__file__,OUT/'runner.py')
    print(json.dumps({'prepared':relative(OUT),'retained_current_outcomes':402,'missing_Firefox_outcomes':201,'interrupted_archive_sha256':inventory['sha256']}))

def guard(plan,rows):
    assert preview.guards(rows)==plan['guards']
    assert digest(Path(__file__))==plan['runner_sha256']
    assert digest(Path(plan['firefox']['executable']))==plan['firefox']['sha256']
    assert digest(OUT/'interrupted-session.zip')==plan['original_archive_sha256']
    assert digest(OUT/'retained-records.json')==plan['retained_records_sha256']
    assert digest(OUT/'original-files.json')==plan['original_file_inventory_sha256']
    assert digest(OUT/'restart-evidence.json')==plan['restart_evidence_sha256']

def run():
    require_original_stopped();plan=load(OUT/'plan.json');rows,_,subset=preview.cases()
    assert subprocess.check_output(['git','show','HEAD:'+relative(OUT/'plan.json')],cwd=ROOT)==(OUT/'plan.json').read_bytes()
    guard(plan,rows);unchanged_original()
    with (OUT/'opened.json').open('x',encoding='utf-8') as f:
        json.dump({'pid':os.getpid(),'utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':digest(OUT/'plan.json')},f,indent=2)
    records=load(OUT/'retained-records.json');started=time.perf_counter()
    def progress():
        write(OUT/'records.json',records)
        write(OUT/'progress.json',{k:{'done':len(v),'valid':sum(r['status']=='valid' for r in v)} for k,v in records.items()})
    progress();server=serve(ROOT/'web/dist')
    try:
        url=f'http://127.0.0.1:{server.server_address[1]}/bench.html'
        for seed in [0,1,2]:
            assert time.perf_counter()-started<plan['recovery_session_cap_seconds']
            guard(plan,rows)
            batch=quality.browser('firefox',seed,rows,SimpleNamespace(seconds=60,concurrency=8),OUT,url)
            assert load(OUT/'firefox'/f's{seed}'/'browser.json')['version']==plan['firefox']['version']
            records['firefox'].extend({**r,'reused':False} for r in batch);progress()
            print(json.dumps({'firefox_seed':seed,'valid':sum(r['status']=='valid' for r in batch),'attempts':len(batch)}),flush=True)
        assert time.perf_counter()-started<plan['recovery_session_cap_seconds']
        guard(plan,rows);unchanged_original()
        full_result,subset_result=summaries(records,plan,subset)
        write(OUT/'results.json',{'records':records,'full_summary':full_result,'subset_summary':subset_result,
            'all_quality_checks_pass':bool(full_result['all_quality_checks_pass'] and subset_result['passes_subset']),
            'guards_unchanged':True,'wall_seconds':time.perf_counter()-started,'finished_utc':datetime.now(timezone.utc).isoformat(),
            'retained_completed_current_build':402,'new_recovery_outcomes':201,'retained_frozen_v1':195,
            'original_interruption_preserved':True,'original_session_claimed_complete':False,'H4_complete':False})
        print('Firefox recovery complete; original interruption remains preserved.',flush=True)
    except BaseException:
        write(OUT/'interruption.json',{'error':traceback.format_exc(),'wall_seconds':time.perf_counter()-started});raise
    finally:server.shutdown()

def verify():
    plan=load(OUT/'plan.json');result=load(OUT/'results.json');rows,development,subset=preview.cases()
    opened=load(OUT/'opened.json')
    try:arguments=psutil.Process(opened['pid']).cmdline()
    except psutil.NoSuchProcess:arguments=[]
    assert not any(a.endswith('h4_depth_reboot_recovery.py') and 'run' in arguments for a in arguments)
    assert not (OUT/'interruption.json').exists()
    guard(plan,rows);unchanged_original()
    assert digest(OUT/'plan.json')==opened['plan_sha256']
    assert result['records']==load(OUT/'records.json')
    assert {k:len(v) for k,v in result['records'].items()}=={'v1':195,'native':201,'chrome':201,'firefox':201}
    retained=load(OUT/'retained-records.json')
    assert all(result['records'][e]==retained[e] for e in ['v1','native','chrome'])
    assert retained['v1']==preview.baseline(development)
    checked=validate_saved(result['records'],rows)
    full_result,subset_result=summaries(result['records'],plan,subset)
    assert json.loads(json.dumps(full_result))==result['full_summary']
    assert json.loads(json.dumps(subset_result))==result['subset_summary']
    assert result['all_quality_checks_pass']==bool(full_result['all_quality_checks_pass'] and subset_result['passes_subset'])
    assert result['wall_seconds']<plan['recovery_session_cap_seconds']
    batches=[]
    for seed in [0,1,2]:
        folder=OUT/'firefox'/f's{seed}';execution=load(folder/'execution.json');config=load(folder/'plan.json')
        batches.append({'seed':seed,'exit_code':execution['exit_code'],'affinity_errors':execution['affinity_errors'],
            'cpus':execution['cpus'],'version':load(folder/'browser.json')['version']})
        assert config['seconds']==60 and config['seed']==seed and len(config['jobs'])==67 and config['concurrency']==8
    write(OUT/'verification.json',{'all_artifact_checks_passed':True,'completed_current_build_outcomes':603,
        'retained_current_build_outcomes':402,'new_recovery_outcomes':201,'frozen_v1_outcomes':195,
        'completed_scored_outcomes':798,'original_infrastructure_interruption_preserved':True,
        'all_quality_checks_pass':result['all_quality_checks_pass'],'records':checked,'Firefox_batches':batches,
        'product_digest':plan['guards']['product'],'scale_and_requirement_review_separate':True,'H4_complete':False})
    paths=[(relative(p),p) for p in sorted(OUT.rglob('*')) if p.is_file()]
    inventory=archive(paths,OUT/'raw.zip');write(OUT/'integrity.json',inventory)
    print(json.dumps({'verified_and_sealed':True,'all_quality_checks_pass':result['all_quality_checks_pass'],
        'archive_sha256':inventory['sha256'],'archive_bytes':inventory['bytes'],'members':len(inventory['members'])}),flush=True)

assert len(sys.argv)==2 and sys.argv[1] in ['prepare','run','verify']
{'prepare':prepare,'run':run,'verify':verify}[sys.argv[1]]()
