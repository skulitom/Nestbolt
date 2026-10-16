"""Verify and seal the completed integrated-preview H4 measurement without rerunning searches."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import psutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h4-preview-score-release-20261016'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()

def write(path,data):
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')

assert (OUT/'results.json').exists(), 'Original measurement still incomplete'
assert not (OUT/'interruption.json').exists(), 'Preserve and investigate the original interruption'
opened=load(OUT/'opened.json')
if psutil.pid_exists(opened['pid']):
    command=psutil.Process(opened['pid']).cmdline()
    assert not any('h4_preview_matrix.py' in part for part in command), 'Original measurement is still running'
plan=load(OUT/'plan.json')
assert digest(OUT/'plan.json')==opened['plan_sha256']
assert subprocess.check_output(['git','show','HEAD:benchmarks/results/h4-preview-score-release-20261016/plan.json'],cwd=ROOT)==(OUT/'plan.json').read_bytes()
sys.path.insert(0,str(ROOT/'scripts'))
import h4_full_matrix as full
import h4_quality as quality
import h4_preview_matrix as preview
rows,development,subset=preview.cases()
assert rows==plan['cases'] and preview.guards(rows)==plan['guards']
result=load(OUT/'results.json')
assert result['records']==load(OUT/'records.json')
assert result['wall_seconds']<4*60*60
selected=lambda ids:{k:[r for r in v if r['job'] in ids] for k,v in result['records'].items()}
summary=json.loads(json.dumps(full.summarize(selected(plan['full_ids']),plan['full_ids'])))
subset_summary=json.loads(json.dumps(quality.summarize(selected(plan['subset_ids']),subset,[0,1,2],60)))
assert summary==result['full_summary'] and subset_summary==result['subset_summary']
assert result['guards_unchanged'] and result['all_quality_checks_pass']==bool(summary['all_quality_checks_pass'] and subset_summary['passes_subset'])
assert result['records']['v1']==preview.baseline(development)
assert all(summary['attempt_coverage_complete'].values())
assert not any(summary['failed_attempts'].values())
source_inventory=load(preview.PRIOR/'integrity.json')
assert digest((preview.PRIOR/'raw.zip'))==source_inventory['sha256']
jobs={r['id']:load(ROOT/r['path']) for r in rows}
checked=[]
with zipfile.ZipFile((preview.PRIOR/'raw.zip')) as previous:
    for engine,records in result['records'].items():
        assert len(records)==(195 if engine=='v1' else 201)
        for record in records:
            def read(name):
                member=record['directory']+'/'+name
                if record['reused']:
                    raw=previous.read(member)
                    assert sha256(raw).hexdigest()==source_inventory['members'][member]['sha256']
                else:
                    target=(ROOT/member).resolve()
                    assert OUT.resolve() in target.parents
                    raw=target.read_bytes()
                return raw
            layout_raw=read('layout.json')
            assert sha256(layout_raw).hexdigest()==record['layout_sha256']
            layout=json.loads(layout_raw)
            validation=json.loads(read('validate-stdout.json'))
            output=json.loads(read('search-stdout.json' if engine in ['v1','native'] else 'result.json'))
            assert validation['valid'] and output['validation']['valid'] and record['status']=='valid'
            delta=quality.equivalent(validation['metrics'],output['validation']['metrics'])
            assert delta==record['maximum_metric_json_roundtrip_difference']==0
            assert len(layout['placements'])==sum(p['quantity'] for p in jobs[record['job']]['parts'])
            assert validation['metrics']['normalized_material']==record['material']
            assert validation['metrics']['sheets_used']==record['sheets']
            case=json.loads(read('case.json'))
            assert all(case.get(k)==v for k,v in record.items() if k not in ['reused','source_archive'])
            assert record['reused']==(engine=='v1')
            if engine!='v1' and 'library' in next(r for r in rows if r['id']==record['job']):
                public=json.loads(read('public-validate-stdout.json'))
                assert public['valid'] and quality.equivalent(public['metrics'],validation['metrics'])==0
            checked.append({'engine':engine,'job':record['job'],'seed':record['seed'],
                'reused':record['reused'],'layout_sha256':record['layout_sha256'],'metrics_identical':True,
                'all_requested_parts_present':True})
batches=[]
for engine in ['chrome','firefox']:
    for seed in [0,1,2]:
        folder=OUT/engine/f's{seed}'
        execution=load(folder/'execution.json')
        info=load(folder/'browser.json')
        config=load(folder/'plan.json')
        assert execution['exit_code']==0 and execution['affinity_errors']==[]
        assert execution['cpus']==[0,2,4,6,8,10,12,14]
        assert len(config['jobs'])==67 and config['concurrency']==8 and config['seconds']==60
        batches.append({'browser':engine,'seed':seed,'version':info['version'],
            'new_jobs':len(config['jobs']),'wall_seconds':execution['wall_seconds'],
            'affinity_deviations':len(execution['affinity_errors']),'exit_code':execution['exit_code']})
write(OUT/'verification.json',{'all_artifact_checks_passed':True,'full_quality_pass':summary['all_quality_checks_pass'],'subset_quality_pass':subset_summary['passes_subset'],
    'total_attempts':len(checked),'new_attempts':sum(not r['reused'] for r in checked),
    'reused_attempts':sum(r['reused'] for r in checked),'plan_sha256':digest(OUT/'plan.json'),
    'results_sha256':digest(OUT/'results.json'),'baseline_binary_sha256':digest(full.BASELINE),
    'product_digest':plan['guards']['product'],'production_guards_unchanged':True,
    'scale_and_complete_requirement_audit_separate':True,'H4_complete':False,
    'held_out_geometry_read':False,'browser_batches':batches,'records':checked})
shutil.copyfile(__file__,OUT/'finalize.py')
# Retain the exact measured engines/site before any integration or rebuild.
for source,relative in [(quality.CLI,'engines/nestbolt.exe'),(full.BASELINE,'engines/nestbolt-final-75cbb32.exe')]:
    target=OUT/'snapshots'/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)
for source in (ROOT/'web/dist').rglob('*'):
    if source.is_file():
        target=OUT/'snapshots/site'/source.relative_to(ROOT/'web/dist')
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
archive=OUT/'raw.zip'
assert not archive.exists()
files=sorted(p for p in OUT.rglob('*') if p.is_file())
inventory={p.relative_to(ROOT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in files}
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:
        z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for member,expected in inventory.items():
        raw=z.read(member)
        assert len(raw)==expected['bytes'] and sha256(raw).hexdigest()==expected['sha256']
write(OUT/'integrity.json',{'archive':archive.relative_to(ROOT).as_posix(),'sha256':digest(archive),
    'bytes':archive.stat().st_size,'members':inventory,'crc_and_every_member_verified':True})
# Consolidation is a separate step; leave every loose file until the report has
# reviewed this inventory and selected the summaries that should stay readable.
print(json.dumps({'artifact_checks_passed':True,'quality_checks_pass':result['all_quality_checks_pass'],
    'archive_sha256':digest(archive),'archive_bytes':archive.stat().st_size,'members':len(inventory),
    'new_attempts':603,'reused_attempts':195},indent=2))
