"""Verify the four saved stage-diagnostic attempts; never run another search."""
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json, shutil, sys, zipfile
import psutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'benchmarks/results/h5-exchange-diagnosis-20261016'
sys.path.insert(0,str(ROOT/'scripts'))
import h5_exchange_diagnosis as diag
load,write,digest=diag.load,diag.write,diag.digest

# Stats intentionally omits zero-valued counters. Preserve the original reader
# and its failed outcomes; only this post-processing reader supplies that zero.
source=(diag.PROBE/'workspace/crates/core/src/sheets.rs').read_text(encoding='utf-8')
for field in ['directed_exchange_attempts','directed_exchanges']:
    assert '#[serde(skip_serializing_if = "is_zero")]\n    pub '+field+': u64' in source
assert 'fn is_zero(n: &u64) -> bool {\n    *n == 0\n}' in source

def corrected_trace(archive,record):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        for name,expected in case['artifacts'].items():assert sha256(z.read(name)).hexdigest()==expected
        traces=[json.loads(line.removeprefix('EXCHANGE_DIAG '))
            for line in z.read('search-stderr.log').decode('utf-8').splitlines()
            if line.startswith('EXCHANGE_DIAG ')]
    attempts=[a for t in traces for a in t['attempts']]
    counts=Counter(a['outcome'] for a in attempts)
    assert not counts['unfinished']
    if record['status']=='valid':
        assert len(attempts)==record['stats'].get('directed_exchange_attempts',0)
        assert counts['accepted']==record['stats'].get('directed_exchanges',0)
    return {'invocations':len(traces),'attempts':len(attempts),'outcomes':dict(counts),
        'receivers':sum(t['receivers'] for t in traces),'proposals':sum(t['proposals'] for t in traces),
        'expired_before_attempt':sum(t['expired_before_attempt'] for t in traces),'traces':traces}

result=load(OUT/'results.json');plan=load(OUT/'plan.json');opened=load(OUT/'opened.json')
try:arguments=psutil.Process(opened['pid']).cmdline()
except psutil.NoSuchProcess:arguments=[]
assert not any('h5_exchange_diagnosis.py' in a for a in arguments)
assert result['guards_unchanged'] and diag.guards()==plan['guards']
assert digest(OUT/'plan.json')==opened['plan_sha256']
assert len(result['records'])==4
assert {(r['job'],r['kerf_mm'],r['seed']) for r in result['records']}=={(j,k,0) for j in diag.JOBS for k in [0.2,1.5]}
verified=[];total=Counter();rechecked=[]
for row in result['records']:
    archive=OUT/row['archive'];assert digest(archive)==row['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        assert case=={k:v for k,v in row.items() if k not in ['archive','archive_sha256','diagnosis','trace_error']}
        assert set(z.namelist())==set(case['artifacts'])|{'case.json'}
        for name,expected in case['artifacts'].items():assert sha256(z.read(name)).hexdigest()==expected
        if row['status']=='valid':
            saved=json.loads(z.read('nested/search.json'));validation=json.loads(z.read('validate-stdout.json'))
            assert saved['validation']['valid'] and validation['valid']
            assert saved['stats']==row['stats'] and row['riders']==0
            diag.prior.equivalent(validation['metrics'],saved['validation']['metrics'])
    trace=corrected_trace(archive,row)
    if 'diagnosis' in row:assert trace==row['diagnosis']
    else:assert "KeyError: 'directed_exchanges'" in row['trace_error'] and trace['outcomes'].get('accepted',0)==0
    rechecked.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'diagnosis':trace,'original_trace_error':row.get('trace_error')})
    total.update(trace['outcomes'])
    verified.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'valid':row['status']=='valid',
        'archive':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,
        'invocations':trace['invocations'],'attempts':trace['attempts'],'outcomes':trace['outcomes']})
write(OUT/'rechecked-traces.json',{'scope':'Saved-output reader correction only; original results and errors unchanged','records':rechecked,'all_trace_counts_match':True})
write(OUT/'verification.json',{'all_archives_and_members_verified':True,'trace_counters_recomputed':True,
    'guards_unchanged':True,'records':verified,'total_outcomes':dict(total),'quality_claim':False,'H5_complete':False,'posthoc_reader_correction':'Supply zero only for counters explicitly omitted by serde is_zero; original errors and outputs retained','original_trace_reader_failures':sum('trace_error' in r for r in result['records'])})
for name,expected in plan['guards']['files'].items():
    p=ROOT/name;assert digest(p)==expected;target=OUT/'snapshots'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
shutil.copyfile(ROOT/'output/finish_h5_exchange_diagnosis.py',OUT/'finish-original.py')
shutil.copyfile(__file__,OUT/'finish-rechecked.py')
files=sorted(p for p in (OUT/'snapshots').rglob('*') if p.is_file());archive=OUT/'snapshots.zip'
inventory={p.relative_to(OUT/'snapshots').as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in files}
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(OUT/'snapshots').as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,r in inventory.items():
        data=z.read(name);assert len(data)==r['bytes'] and sha256(data).hexdigest()==r['sha256']
write(OUT/'snapshot-integrity.json',{'sha256':digest(archive),'members':inventory,'crc_and_every_member_verified':True})
target=(OUT/'snapshots').resolve();assert target.is_relative_to(OUT.resolve()) and target!=OUT
for p in target.rglob('*'):
    if p.is_file():assert digest(p)==inventory[p.relative_to(target).as_posix()]['sha256']
shutil.rmtree(target)
lines=['# Directed-exchange repair-stage diagnosis — 2026-10-16','',
f"**{sum(r['valid'] for r in verified)}/4 diagnostic layouts validate.** These runs identify observed failure stages;",
'they do not establish material or speed improvement. The original report reader',
+'failed on omitted zero counters. The serde definition explicitly skips zero;',
+'the corrected reader rechecks the same saved outputs. Original errors and',
+'results remain unchanged, and no search was repeated. The earlier failed pilot',
'is retained and is not replaced or rescored.','',
'The [committed plan](h5-exchange-diagnosis-20261016/plan.json) fixes both mechanical',
'jobs, both kerfs, seed 0, 60 seconds and serial physical CCD0 CPU 8. Measurement',
'starts only after the H4 tree-depth pilot is terminal and sealed. The isolated',
'observer preserves the rejected algorithm and adds one aggregate trace per',
'invocation. Tracing can perturb deadlines; no quality comparison is claimed.','',
'| Job | Kerf mm | Invocations | Attempted exchanges | Recorded outcomes |',
'| --- | ---: | ---: | ---: | --- |']
for r in verified:
    outcomes=', '.join(f'{k}: {v}' for k,v in sorted(r['outcomes'].items())) or 'none'
    lines.append(f"| {r['job']} | {r['kerf_mm']} | {r['invocations']} | {r['attempts']} | {outcomes} |")
lines+=['','All attempt-level areas, blocker counts and repair losses remain in',
'[rechecked traces](h5-exchange-diagnosis-20261016/rechecked-traces.json), with the original stderr',
'traces in each immutable per-attempt archive. Counts agree with the solver',
'statistics. Independent public validation, original requested quantities,',
'zero hole riders and public exports are checked. CRC, all archive/member hashes',
'and source/binary/input guards pass. The complete session took',
f"{result['wall_seconds']/60:.3f} minutes. No candidate is integrated.",'',
'This identifies observed rejection stages, not geometric impossibility or',
'a reason to increase budgets. Choose any future change from these stage losses',
'and preserved geometry, then test it separately under the original H5 limits.',
'H5 remains open; completed milestone weight remains 45%.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'valid':sum(r['valid'] for r in verified),'outcomes':dict(total)}))
