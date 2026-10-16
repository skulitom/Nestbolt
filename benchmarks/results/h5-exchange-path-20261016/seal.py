"""Seal two diagnostic observations before integrating an unrelated score change."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h5-exchange-path-20261016'
sys.path.insert(0,str(ROOT/'scripts'))
import h5_exchange_path_diagnostic as diagnostic
load,write,digest=diagnostic.load,diagnostic.write,diagnostic.digest
result=load(OUT/'results.json')
assert result['guards_unchanged'] and diagnostic.guards()==load(OUT/'plan.json')['guards']
assert len(result['records'])==2 and {r['job'] for r in result['records']}==set(diagnostic.JOBS)
for record in result['records']:
    assert record['status']=='valid' and record['timers_observed']
    assert not record['exchange_timed_call_observed']
    folder=OUT/record['job']
    assert load(folder/'case.json')==record
    search=load(folder/'nested/search.json')
    validation=load(folder/'validate-stdout.json')
    assert validation['valid'] and search['validation']['valid']
    assert diagnostic.pilot.equivalent(validation['metrics'],search['validation']['metrics'])==record['maximum_metric_difference']
write(OUT/'verification.json',{'all_original_records_verified':True,'valid':2,
    'exchange_call_observed':False,'quality_gate_evidence':False,'speed_claim':False,
    'interpretation':'Neither observed trajectory reached timed(exchange). This does not prove it is unreachable for every seed/job; it explains why these two runs cannot demonstrate exchange benefit.',
    'next_hypothesis':'Consider the already bounded initial relocation opportunity in a new isolated experiment; preserve global budgets, incumbents and original failures.'})
shutil.copyfile(__file__,OUT/'seal.py')
archive=OUT/'raw.zip';assert not archive.exists()
files=sorted(p for p in OUT.rglob('*') if p.is_file())
inventory={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p)} for p in files}
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,row in inventory.items():
        raw=z.read(name);assert len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256']
write(OUT/'integrity.json',{'archive':archive.name,'bytes':archive.stat().st_size,'sha256':digest(archive),
    'members':inventory,'crc_and_every_member_verified':True})
lines=['# Exchange path diagnostic — 2026-10-16','',
    '**Neither diagnostic reached the exchange call.** Both outputs validate.',
    'These are two separately planned, debug-enabled observations of the unchanged',
    'candidate, not repeat quality attempts or a speed comparison. The original',
    '[72-attempt pilot](h5-exchange-pilot-v2-20261016.md) remains unchanged.','',
    'Existing timers record separator work in both mechanical jobs; panel-hardware',
    'also records ordinary relocation. Neither contains an `exchange` timer.',
    'That timer surrounds the call even when it returns without a proposal, so',
    'its absence identifies a call-path issue on these observed trajectories.',
    'Source inspection places exchange only after three consecutive failed',
    'separation returns, while ordinary relocation also has an earlier opportunity.',
    'A separation call may consume the remaining exploration budget. This does',
    'not prove exchange unreachable on every job or seed.','',
    'Keep this candidate unintegrated. A future isolated experiment can test the',
    'existing bounded initial relocation opportunity while preserving the whole',
    'search deadline, independent acceptance and failed incumbent. H5 still needs',
    'its original material and cutting conditions; neither limit changes.','',
    'The committed plan uses kerf 0.2 mm, seed 0, 60 seconds, physical CCD0 CPUs',
    '8/10 and `NESTBOLT_DEBUG=1` in the two child processes only. All source/input/',
    'binary guards pass; the parent and original pilot have no environment override.',
    'Both saved layouts independently validate with identical metrics.','',
    '[Results and exact timers](h5-exchange-path-20261016/results.json),',
    '[verification](h5-exchange-path-20261016/verification.json),',
    '[fixed plan](h5-exchange-path-20261016/plan.json).','',
    f"The verified raw archive retains {len(files)} members, {archive.stat().st_size:,} bytes,",
    f"SHA-256 `{digest(archive)}`. CRC, every member size and hash were checked.",
    'All original logs and outputs remain preserved. No milestone is completed.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'members':len(files),'bytes':archive.stat().st_size,'sha256':digest(archive)}))
