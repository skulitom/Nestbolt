"""Read saved summaries and source history only; do not reopen reserved inputs."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tomllib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h2-requirements-review-20261016'
OUT.mkdir()
load=lambda p:json.loads((ROOT/p).read_bytes())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
manifest=load('benchmarks/datasets/shop/manifest.json')
groups=Counter((r['split'],Path(r['path']).suffix.lower()) for r in manifest['files'])
training_vector=sum(groups[('training',suffix)] for suffix in ['.svg','.dxf'])
training_native=sum(groups[('training',suffix)] for suffix in ['.lbrn','.lbrn2'])
assert (training_vector,training_native)==(257,56)
vector=load('benchmarks/results/h2-export-replay-20261015/review.json')
native=load('benchmarks/results/h2-native-warning-probe-20261016-v3/checks.json')
current=load('benchmarks/results/preview-integration-20261016/verification.json')
robust=load('benchmarks/results/h2-import-robustness-20261014T015959Z.json')
assert vector['fidelity_bridge_passes'] and vector['current_import_geometry_matches']==246
assert native['all_checks_passed'] and native['accepted']==45 and native['original_clear_rejections']==11
assert current['all_checks_passed'] and robust['counts']=={'imported':36,'rejected':147}
assert len(robust['files'])==183 and max(r['elapsed_s'] for r in robust['files'])<10
changed=subprocess.check_output(['git','diff','--name-only','465f994','HEAD','--',
    'crates/core/src','crates/validator/src','crates/cli/src','crates/mcp/src','crates/wasm/src'],cwd=ROOT,text=True).splitlines()
assert set(changed)=={'crates/core/src/holes.rs','crates/core/src/lightburn.rs','crates/core/src/lightburn/path.rs',
    'crates/core/src/lightburn/units.rs','crates/core/src/project/lightburn.rs'}
old_lock=tomllib.loads(subprocess.check_output(['git','show','465f994:Cargo.lock'],cwd=ROOT).decode())
new_lock=tomllib.loads((ROOT/'Cargo.lock').read_text(encoding='utf-8'))
external=lambda lock:[p for p in lock['package'] if not p['name'].startswith('nestbolt-')]
assert external(old_lock)==external(new_lock)
for relative,expected in native['source_files'].items():
    assert sha256((ROOT/'crates/core/src'/relative).read_bytes()).hexdigest()==expected['candidate']
refs=['benchmarks/results/h2-export-replay-20261015/review.json',
    'benchmarks/results/h2-native-warning-probe-20261016-v3/checks.json',
    'benchmarks/results/preview-integration-20261016/verification.json',
    'benchmarks/results/h2-import-robustness-20261014T015959Z.json',
    'benchmarks/results/h3-complete-20261015/checks.json',
    'benchmarks/results/h2-habit-fuzz-20261014T015256Z.md',
    'benchmarks/results/h2-warning-audit-20261014T015958Z.md',
    'benchmarks/results/h2-lightburn-20261013T195848Z.md']
write(OUT/'checks.json',{'scope':'Saved-evidence/source review, not a new corpus run or acceptance result',
    'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'all_review_checks_passed':True,'H2_complete':False,'held_out_geometry_read':False,
    'held_out_labels_read':False,'new_searches':0,'new_imports':0,
    'training_files':313,'accepted_training_libraries':291,'clear_original_rejections':22,
    'R43_approved_hash_scoped_exception_retained':True,
    'changed_product_sources_since_vector_replay':changed,'third_party_lock_records_identical':True,
    'current_core_identical_to_native_training_audit':True,
    'historical_robustness_files':183,'historical_max_import_seconds':max(r['elapsed_s'] for r in robust['files']),
    'reserved_vector_evaluation_pending':22,'reserved_native_results_reused_without_reopening':3,
    'pending_denominator_clarification_unchanged':True,
    'evidence_sha256':{p:sha256((ROOT/p).read_bytes()).hexdigest() for p in refs}})
(OUT/'review.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps({'training_files':313,'accepted':291,'clear_rejections':22,'unchanged_external_dependencies':True,'H2_complete':False}))
