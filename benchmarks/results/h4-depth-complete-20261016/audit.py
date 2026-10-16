"""Audit every H4 gate against completed recovery, original evidence and sealed scales."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import h4_preview_matrix as preview
import h4_quality as quality
import h4_full_matrix as full
import h4_scale as scale

M=ROOT/'benchmarks/results/h4-depth-reboot-recovery-20261016'
S=ROOT/'benchmarks/results/h4-depth-recovered-scale-plan-20261016'
P=ROOT/'benchmarks/results/h4-depth-requirement-preflight-20261016'
O=ROOT/'benchmarks/results/h4-preview-depth-release-20261016'
OUT=ROOT/'benchmarks/results/h4-depth-complete-20261016'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')

assert not OUT.exists()
rows,development,subset=preview.cases()
plan=load(M/'plan.json');result=load(M/'results.json');verified=load(M/'verification.json')
assert preview.guards(rows)==plan['guards']
assert result['guards_unchanged'] and result['all_quality_checks_pass']
assert not result['original_session_claimed_complete'] and result['original_interruption_preserved']
assert verified['all_artifact_checks_passed'] and verified['all_quality_checks_pass']
assert verified['completed_current_build_outcomes']==603 and verified['retained_current_build_outcomes']==402
assert verified['new_recovery_outcomes']==201 and verified['frozen_v1_outcomes']==195
assert len(verified['records'])==603 and all(r['valid'] and r['all_requested_parts_present'] and r['metrics_identical'] for r in verified['records'])
original=load(O/'plan.json');retained=load(M/'retained-records.json')
assert original['guards']==plan['guards']
assert all(result['records'][e]==retained[e] for e in ['v1','native','chrome'])
assert result['records']['v1']==preview.baseline(development)
assert plan['seconds']==60 and plan['seeds']==[0,1,2] and plan['cpus']==[0,2,4,6,8,10,12,14] and plan['concurrency']==8
assert len(plan['full_ids'])==65 and set(plan['full_ids'])=={r['id'] for r in development}
expected_subset={f'm-public-gear-{i}' for i in range(1,5)}|{f'm-sign-{i}' for i in range(1,5)}|{'m-mechanical-cog-washers','example-gears','example-letters'}
assert set(plan['subset_ids'])==expected_subset and len(plan['subset_ids'])==11
expected={(r['id'],s) for r in rows for s in [0,1,2]}
for engine in ['native','chrome','firefox']:
    records=result['records'][engine]
    assert len(records)==201 and {(r['job'],r['seed']) for r in records}==expected
    assert all(r['status']=='valid' for r in records)
select=lambda ids:{k:[r for r in v if r['job'] in ids] for k,v in result['records'].items()}
f=full.summarize(select(plan['full_ids']),plan['full_ids'])
q=quality.summarize(select(plan['subset_ids']),subset,[0,1,2],60)
assert json.loads(json.dumps(f))==result['full_summary'] and json.loads(json.dumps(q))==result['subset_summary']
assert f['all_quality_checks_pass'] and q['passes_subset']
assert f['native_vs_v1']['median_difference_percent']<=.5
for engine in ['chrome','firefox']:
    assert q['comparisons'][engine]['median_difference_percent']<=1
    assert all(v<=5 for v in q['comparisons'][engine]['per_job_difference_percent'].values())
    r=f['browsers_vs_native'][engine]
    assert r['median_difference_percent']<=2 and r['total_difference_percent']<=2
    assert all(s['median_difference_percent']<=2 and s['total_difference_percent']<=2 for s in r['per_seed'].values())
    for seed in [0,1,2]:
        folder=(O if engine=='chrome' else M)/engine/f's{seed}'
        execution=load(folder/'execution.json');configuration=load(folder/'plan.json')
        assert execution['exit_code']==0 and not execution['affinity_errors'] and execution['cpus']==quality.CPUS
        assert configuration['seed']==seed and configuration['seconds']==60 and len(configuration['jobs'])==67
        assert configuration['concurrency']==8

inventory=load(M/'integrity.json')
assert inventory['crc_and_every_member_verified'] and digest(M/'raw.zip')==inventory['sha256']
with zipfile.ZipFile(M/'raw.zip') as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory['members'])
    for name,row in inventory['members'].items():
        data=z.read(name);assert len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256']
assert digest(M/'interrupted-session.zip')==plan['original_archive_sha256']
for name,row in load(M/'original-files.json').items():
    p=ROOT/name;assert digest(p)==row['sha256'] and p.stat().st_size==row['bytes']
assert not (O/'results.json').exists()
assert not (M/'interruption.json').exists() and not (S/'interruption.json').exists()
terminal=load(S/'completed.json')
assert [s['index'] for s in terminal['stages']]==[0,1,2,3,4]
assert all(s['exit_code']==0 and digest(S/f"stage-{s['index']}.log")==s['log_sha256'] for s in terminal['stages'])
fidelity=load(S/'curve-export-fidelity/verification.json')
assert fidelity['all_checks_pass'] and fidelity['both_scale_workflows_pass'] and fidelity['every_curve_sheet_selected']
visual=load(S/'visual-review.json')
assert visual['reviewed'] and len(visual['screenshots'])==4
expected_screens={fidelity[k]+'/'+b+'/screen.png' for k in ['curves','g5'] for b in ['chrome','firefox']}
assert {r['path'] for r in visual['screenshots']}==expected_screens
assert all(r['reviewed'] and digest(ROOT/r['path'])==r['sha256'] for r in visual['screenshots'])
scale_records=[]
for kind in ['curves','g5']:
    folder=ROOT/fidelity[kind];summary=load(folder/'summary.json')
    assert summary['passes'] and summary['source_guards_passed']
    assert summary['fixture_kind']==kind and summary['quick_start']==(kind=='curves') and summary['workers_override'] is None
    assert scale.guards(Path(summary['pinned_validator']),kind)==summary['guards']
    archive=summary['archive']
    assert archive['crc_and_member_hashes_verified'] and digest(folder/'raw.zip')==archive['sha256']
    assert {r['browser'] for r in summary['results']}=={'chrome','firefox'}
    with zipfile.ZipFile(folder/'raw.zip') as z:
        assert z.testzip() is None and set(z.namelist())==set(archive['members'])
        for name,row in archive['members'].items():
            data=z.read(name);assert len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256']
        for r in summary['results']:
            assert r['status']=='valid' and r['passes'] and not r['affinity_errors']
            assert r['peak_rss_bytes']<1500000000 and r['peak_private_bytes']<1500000000
            assert r['app']['maximum_event_loop_gap_ms']<=200
            assert r['app']['maximum_long_task_ms'] is None or r['app']['maximum_long_task_ms']<=200
            for name,h in r['artifacts'].items():assert sha256(z.read(r['browser']+'/'+name)).hexdigest()==h
            layout=json.loads(z.read(r['browser']+'/layout.json'))
            assert len(layout['placements'])==2000
            if kind=='curves':
                checked=load(S/'curve-export-fidelity'/(r['browser']+'.json'))
                assert checked['all_checks_pass'] and checked['full_project_checked'] and checked['total_placements_checked']==2000
                assert checked['limit_mm']==.01 and checked['searches_run']==0 and not checked['exports_regenerated']
                assert sha256(z.read(r['browser']+'/project.zip')).hexdigest()==checked['project_zip_sha256']
            scale_records.append({'fixture':kind,'browser':r['browser'],'peak_rss_bytes':r['peak_rss_bytes'],
                'peak_private_bytes':r['peak_private_bytes'],'heartbeat_ms':r['app']['maximum_event_loop_gap_ms'],
                'long_task_ms':r['app']['maximum_long_task_ms'],'layout_sha256':r['layout_sha256'],'placements':2000})

preflight=load(P/'checks.json');integration=load(ROOT/'benchmarks/results/h4-depth-integration-20261016/checks.json')
assert preflight['product_digest']==plan['guards']['product']==integration['product_digest']
assert preflight['declared_subset_exact'] and preflight['physical_cores_and_original_budget_seed_method']
assert preflight['no_imported_or_shared_WASM_memory']
assert digest(ROOT/preflight['wasm_path'])==preflight['wasm_sha256']==integration['wasm_sha256']
assert integration['all_checks_passed'] and integration['actual_windows_bundle_verified'] and not integration['H5_exchange_integrated']
assert digest(ROOT/'benchmarks/datasets/shop/manifest.json')=='02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
OUT.mkdir()
(OUT/'audit.py').write_bytes(Path(__file__).read_bytes())
evidence=[M/'plan.json',M/'results.json',M/'verification.json',M/'integrity.json',M/'restart-evidence.json',M/'original-files.json',
    P/'checks.json',S/'plan.json',S/'completed.json',S/'visual-review.json',S/'curve-export-fidelity/verification.json',
    ROOT/'benchmarks/results/h4-depth-integration-20261016/checks.json']
evidence.extend(ROOT/fidelity[k]/'summary.json' for k in ['curves','g5'])
record={'scope':__doc__,'utc':datetime.now(timezone.utc).isoformat(),'all_explicit_H4_requirements_pass':True,
    'H4_complete':True,'completed_weight_percent':60,'product_digest':plan['guards']['product'],
    'current_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'native_valid':195,'native_median_percent':f['native_vs_v1']['median_difference_percent'],
    'subset':q['comparisons'],'full_development':f['browsers_vs_native'],'scales':scale_records,
    'no_previous_fitting_input_lost':True,'all_matrix_requested_quantities_validated':True,
    'unshared_WASM_memory_verified_for_exact_binary':True,'full_saved_curve_fidelity_in_both_browsers':True,
    'original_restart_and_failures_preserved':True,'retained_current_outcomes':402,'new_recovery_outcomes':201,
    'held_out_geometry_read':False,'remaining_gates':['H2','H5'],'new_competitor_claim':False,'release_created':False,
    'limits':'Memory is sampled process-tree RSS/private every 200 ms; responsiveness uses a 20 ms heartbeat and Long Tasks where supported. Firefox recovery is a separate post-reboot session. No universal resource or latency guarantee.',
    'evidence':{p.relative_to(ROOT).as_posix():digest(p) for p in evidence}}
write(OUT/'checks.json',record)
print(json.dumps({'H4_complete':True,'completed_weight_percent':60,'native_median_percent':record['native_median_percent'],'scales':scale_records}))
