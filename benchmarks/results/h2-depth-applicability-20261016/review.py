"""Bind existing import evidence to current sources without opening reserved files."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h2-depth-applicability-20261016'
prior_path=root/'benchmarks/results/h2-requirements-review-20261016/checks.json'
prior=json.loads(prior_path.read_bytes())
candidate='aba989e1173f64ca1f273af1c839bd990d8cea05'
git=lambda *a:subprocess.check_output(['git',*a],cwd=root)
digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(root/'scripts'))
from h2_import_audit import source_digest
product=source_digest()
assert product=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
scope=['crates','web/src','Cargo.toml','Cargo.lock']
changed=git('diff','--name-only',prior['commit'],candidate,'--',*scope).decode('utf-8').splitlines()
assert changed==['crates/core/src/separate/score.rs','crates/core/src/sheets/vstrip.rs']
names=git('ls-files','--',*scope).decode('utf-8').splitlines()
for name in names:
    assert (root/name).read_bytes().replace(b'\r\n',b'\n')==git('show',candidate+':'+name),name
assert git('show',prior['commit']+':Cargo.lock')==git('show',candidate+':Cargo.lock')
for name,expected in prior['evidence_sha256'].items():assert digest(root/name)==expected,name
manifest=root/'benchmarks/datasets/shop/manifest.json'
assert digest(manifest)=='02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
integration=json.loads((root/'benchmarks/results/h4-depth-integration-20261016/checks.json').read_bytes())
assert integration['all_checks_passed'] and integration['product_digest']==product
features=json.loads((root/'benchmarks/results/preview-depth-features-20261016/checks.json').read_bytes())
assert features['all_checks_pass'] and features['production_digest']==product
out.mkdir(exist_ok=False)
(out/'source-difference.patch').write_bytes(git('diff',prior['commit'],candidate,'--',*scope))
record={'all_review_checks_pass':True,'scope':__doc__,'candidate':candidate,'product_digest':product,
    'prior_review_commit':prior['commit'],'prior_review_sha256':digest(prior_path),
    'checked_tracked_product_files':len(names),'changed_product_sources':changed,
    'all_other_product_sources_unchanged':True,'complete_Cargo_lock_unchanged':True,
    'prior_evidence_hashes_unchanged':prior['evidence_sha256'],'frozen_manifest_sha256':digest(manifest),
    'current_integration':integration['counts'],'downloaded_windows_feature_checks_pass':True,
    'training_files':prior['training_files'],'accepted_training_libraries':prior['accepted_training_libraries'],
    'clear_original_rejections':prior['clear_original_rejections'],
    'reserved_vector_evaluation_pending':22,'reserved_native_results_reused_without_reopening':3,
    'pending_denominator_clarification_unchanged':True,'held_out_geometry_read':False,
    'held_out_labels_read':False,'new_imports':0,'new_searches':0,'new_timing_or_fidelity_claim':False,
    'H2_complete':False,'completed_milestone_weight_percent':45}
(out/'checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
(out/'review.py').write_bytes(Path(__file__).read_bytes())
report='''# Current preview: import evidence applicability — 2026-10-16

**The import/export code and prior evidence remain unchanged; H2 is still open.**
This read-only source review binds the existing
[complete training review](h2-requirements-review-20261016.md) to candidate
`aba989e` and the current release preview. It imports no drawing, runs no
search, and opens no reserved geometry or labels.

[Exact checks](h2-depth-applicability-20261016/checks.json) establish that only
`separate/score.rs` and `sheets/vstrip.rs` changed since the earlier `0a9fb44`
review. Those are the bounded collision-score traversal and collision-tree
depth changes under H4 measurement. Every other tracked product file, including
the readers, native warnings, preserving writer, SVG/DXF exporters, public
CLI/MCP/browser adapters and independent validator, is unchanged. The entire
Cargo lockfile is identical. The saved source difference is retained.

All prior review evidence hashes and the frozen shop manifest still match.
Its accounting remains 313 labelled training files: 291 accepted libraries and
22 original clear rejections. The approved hash-scoped R43 exception and all
original labels/failures remain intact. Historical robustness, property and
fidelity measurements retain their original dates and scopes.

[Current integration checks](h4-depth-integration-20261016.md) pass on the
changed solver. The [actual downloaded Windows CLI/MCPB workflow](preview-depth-features-20261016.md)
also verifies authored native repair instructions, preserved editable groups,
lead sidecars, independent layout validation and repeated exports. Neither
check substitutes for the unresolved reserved acceptance.

Twenty-two reserved vectors remain unopened. The three native projects' saved
results are retained without reopening them. The original denominator question
and 95% requirement are unchanged; H2 remains incomplete and completed milestone
weight remains 45%. No new import timing, geometric-fidelity or acceptance
claim follows from source equality.
'''
(out.parent/(out.name+'.md')).write_text(report,encoding='utf-8',newline='\n')
path=root/'BENCHMARKS.md';before=path.read_bytes()
assert before.startswith(git('show','HEAD:BENCHMARKS.md'))
with path.open('a',encoding='utf-8',newline='\n') as f:
    f.write('''

## 2026-10-16 — Import evidence applies to the current depth preview

[The current source review](benchmarks/results/h2-depth-applicability-20261016.md)
finds only the two H4 search files changed since the complete `0a9fb44` import
review. Every reader/exporter, public adapter and validator source and the full
Cargo lockfile are unchanged. All prior evidence and frozen-manifest hashes
match. Current integration and downloaded Windows feature checks pass. The
313-file training accounting stays 291 accepted / 22 clear rejections with
the approved R43 exception and original failures preserved. This review runs
no import/search and claims no new timing or fidelity measurement. Twenty-two
reserved vectors and the denominator clarification remain pending; H2 stays
open and completed milestone weight stays 45%.
''')
assert path.read_bytes().startswith(before)
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\nbenchmarks/results/h2-depth-applicability-20261016/** -text -whitespace\n')
print(json.dumps({'all_review_checks_pass':True,'unchanged_product_files':len(names)-len(changed),
    'changed_search_files':changed,'held_out_opened':False,'H2_complete':False}))
