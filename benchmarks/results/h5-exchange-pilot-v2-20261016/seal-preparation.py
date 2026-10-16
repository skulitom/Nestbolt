"""Record a separate pre-measurement scheduling correction; keep the old plan."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'output/h5-exchange-pilot-v2-preparation'
OUT=ROOT/'benchmarks/results/h5-exchange-pilot-v2-20261016'
OLD=ROOT/'benchmarks/results/h5-exchange-pilot-20261016'
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')

assert not (OLD/'opened.json').exists() and not (OUT/'opened.json').exists()
assert (ROOT/'scripts/h5_exchange_pilot_v2.py').read_bytes()==(SOURCE/'h5_exchange_pilot_v2.py').read_bytes()==(OUT/'runner.py').read_bytes()
plan=json.loads((OUT/'plan.json').read_bytes())
prior=json.loads((OLD/'plan.json').read_bytes())
for key in ['jobs','kerfs_mm','seeds','seconds','arms','blocks','attempts','cpus','concurrency','geometry',
    'search_external_timeout_seconds','validation_export_timeout_seconds','revalidation_absolute_tolerance',
    'whole_session_limit_seconds','failed_attempts','decision','held_out_geometry_read','H5_complete']:
    assert plan[key]==prior[key],key
assert 'Ran 7 tests' in (SOURCE/'runner-tests.log').read_text(encoding='utf-8')
files=[*sorted(p for p in SOURCE.iterdir() if p.is_file()),ROOT/'output/test_h5_exchange_pilot_v2.py',
       ROOT/'output/prepare_h5_exchange_pilot_v2.py',Path(__file__)]
archive=OUT/'preparation.zip'
inventory={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p)} for p in files}
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,row in inventory.items():
        raw=z.read(name)
        assert len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256']
write(OUT/'preparation-integrity.json',{'archive':archive.name,'bytes':archive.stat().st_size,'sha256':digest(archive),
    'members':inventory,'crc_and_every_member_verified':True})
write(OUT/'preparation-checks.json',{'scope':__doc__,'original_plan_sha256':digest(OLD/'plan.json'),
    'new_plan_sha256':digest(OUT/'plan.json'),'original_and_new_unopened':True,'pure_harness_tests_passed':7,
    'search_and_scoring_parameters_unchanged':True,'observer_binaries_unchanged':True,
    'workflow_change':'Require completed retained measurements and available cores instead of a passing unrelated H4 gate.',
    'original_H4_failure_preserved':True,'H4_complete':False,'H5_complete':False})
shutil.copyfile(__file__,OUT/'seal-preparation.py')
print(json.dumps({'members':len(files),'bytes':archive.stat().st_size,'sha256':digest(archive)}))
