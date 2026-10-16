"""Retain isolated source/build proofs before any chunks8 measurement opens."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PROBE=ROOT/'output/h4-score-granularity-probe'
WORK=PROBE/'workspace'
OUT=ROOT/'benchmarks/results/h4-score-chunks-preparation-20261016'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v): p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')

build=load(PROBE/'build-v3.json')
assert build['all_passed'] and build['root_baseline_unchanged']
assert not OUT.exists()
OUT.mkdir()
files={}
def add(p,name=None):
    assert p.is_file()
    name=name or p.relative_to(ROOT).as_posix()
    assert name not in files
    files[name]=p

for row in load(PROBE/'plan.json')['baseline_files']:
    source=WORK/row['path']
    assert digest(ROOT/row['path'])==row['sha256']
    if row['path']!='crates/core/src/separate/score.rs': assert digest(source)==row['sha256']
    add(source)
add(ROOT/'crates/core/src/separate/score.rs','baseline/score.rs')
for p in sorted(PROBE.iterdir()):
    if p.is_file():add(p)
for name in filter(None,subprocess.check_output(['git','ls-files','-z','--','web'],cwd=ROOT).decode().split('\0')):
    assert digest(ROOT/name)==digest(WORK/name)
    add(WORK/name)
for folder in ['web/src/pkg','web/dist']:
    for p in sorted((WORK/folder).rglob('*')):
        if p.is_file():add(p)
for name in ['scripts/h4_score_chunks_probe.py','output/prepare_h4_score_granularity.py',
    'output/check_h4_score_granularity.py','output/check_h4_score_long_rows.py',
    'output/build_h4_score_granularity.py','output/finish_h4_score_chunks_build.py','output/seal_h4_score_chunks_preparation.py']:
    add(ROOT/name)
archive=OUT/'raw.zip'
inventory={name:{'bytes':p.stat().st_size,'sha256':digest(p)} for name,p in sorted(files.items())}
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,p in sorted(files.items()):z.write(p,name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,row in inventory.items():
        raw=z.read(name)
        assert len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256']
write(OUT/'integrity.json',{'archive':archive.relative_to(ROOT).as_posix(),'sha256':digest(archive),
    'bytes':archive.stat().st_size,'members':inventory,'crc_and_every_member_verified':True})
checks={'scope':__doc__,'all_passed':True,'production_change':'Score-bound check granularity only',
    'fixture_pole_counts':[16,15],'multiple_and_partial_chunks_covered':True,
    'debug_tests':3,'optimized_tests':3,'reference_bound_combinations':5760,
    'one_filtered_test_is_unrelated_near_zero_arc_regression':True,
    'strict_core_library_clippy':True,'format_native_wasm_types_bundle':True,
    'candidate_score_sha256':build['candidate_score_sha256'],'cli_sha256':build['cli_sha256'],
    'wasm_sha256':build['wasm_sha256'],'root_product_unchanged':True,'unique_cargo_target':True,
    'measured_search_started':False,'performance_gain_established':False,
    'integrated':False,'H4_complete':False,'held_out_geometry_read':False}
write(OUT/'checks.json',checks)
shutil.copyfile(PROBE/'build-v3.json',OUT/'build.json')
shutil.copyfile(__file__,OUT/'seal.py')
print(json.dumps({'archive_sha256':digest(archive),'members':len(files),'bytes':archive.stat().st_size,
    'checks':checks},indent=2))
