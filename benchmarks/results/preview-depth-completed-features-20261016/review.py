"""Bind completed H3/H6 evidence to the preview without reopening reserved inputs."""
from pathlib import Path
from hashlib import sha256
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/preview-depth-completed-features-20261016'
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
H3='5fb6b5a6620ae63c4d4fb431f2c235c7ea547056'
H6='77dfa55ceabc7680ce5d332dc7682bc25f6b5ab6'
product=source_digest()
assert product=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
assert not OUT.exists()
evidence=[
 'benchmarks/results/h3-complete-20261015/checks.json',
 'benchmarks/results/h6-material-recheck-20261015/verification.json',
 'benchmarks/results/h6-material-recheck-20261015/reconciled.json',
 'benchmarks/results/h6-complete-20261015.md',
 'benchmarks/results/h2-native-warning-probe-20261016-v3/checks.json',
 'benchmarks/results/h2-depth-applicability-20261016/checks.json',
 'benchmarks/results/h4-depth-integration-20261016/checks.json',
 'benchmarks/results/preview-depth-features-20261016/checks.json']
records={name:load(ROOT/name) for name in evidence if name.endswith('.json')}
assert records[evidence[0]]['H3'] and records[evidence[1]]['H6_complete']
assert records[evidence[4]]['all_checks_passed'] and records[evidence[4]]['accepted']==45 and records[evidence[4]]['original_clear_rejections']==11
assert records[evidence[5]]['all_review_checks_pass']
assert records[evidence[6]]['all_checks_passed'] and records[evidence[6]]['product_digest']==product
assert records[evidence[7]]['all_checks_pass'] and records[evidence[7]]['production_digest']==product
assert records[evidence[7]]['repeat_export_byte_identical_both_surfaces']
identities=[]
for base,paths in [(H3,['crates/core/src/lightburn/writer.rs','crates/core/src/project/lightburn/cutting.rs']),
                   (H6,['crates/core/src/lead_in.rs','crates/core/src/lead_in/source.rs','crates/core/src/lead_in/layout.rs',
                        'crates/core/src/export.rs','crates/core/src/export/ordered.rs'])]:
    for name in paths:
        original=git('show',base+':'+name);current=git('show','HEAD:'+name)
        assert original==current and (ROOT/name).read_bytes().replace(b'\r\n',b'\n')==current
        identities.append({'source':name,'unchanged_since':base,'git_blob_sha256':sha256(current).hexdigest()})
H3paths=['crates/core/src/lightburn.rs','crates/core/src/lightburn','crates/core/src/project/lightburn.rs','crates/core/src/project/lightburn']
changed=git('diff','--name-only',H3,'HEAD','--',*H3paths).decode().splitlines()
assert set(changed)=={'crates/core/src/lightburn.rs','crates/core/src/lightburn/path.rs','crates/core/src/lightburn/units.rs','crates/core/src/project/lightburn.rs'}
OUT.mkdir()
(OUT/'h3-diagnostic-only.diff').write_bytes(git('diff',H3,'HEAD','--',*H3paths))
(OUT/'h6-integration-adapters.diff').write_bytes(git('diff',H6,'HEAD','--','crates/core/src/project/cutting.rs','crates/core/src/project/lightburn/cutting.rs','crates/core/src/lead_in/tests.rs'))
(OUT/'review.py').write_bytes(Path(__file__).read_bytes())
result={'scope':__doc__,'all_review_checks_pass':True,'product_digest':product,
    'current_commit':git('rev-parse','HEAD').decode().strip(),'H3_evidence_commit':H3,'H6_material_evidence_commit':H6,
    'source_identities':identities,'H3_changed_import_paths':changed,
    'H3_diff_review':'Warnings for cached text, missing controls and bounding rectangles; warning-list de-duplication. Source geometry operations and preserving writer unchanged.',
    'H6_adapter_review':'Quick-start propagation and optional common-line bonus route were added. Native mixed-group checks moved into nesting_units; layer-cut classification uses the common scene method. Lead construction/validation/export implementation remains unchanged; integration and downloaded CLI/MCP checks cover the current adapters.',
    'evidence_sha256':{name:digest(ROOT/name) for name in evidence},
    'current_functional_counts':records[evidence[6]]['counts'],
    'actual_downloaded_CLI_MCPB_feature_checks_pass':True,
    'historical_material_costs_not_relabelled_as_current_search_results':True,
    'historical_H6_costs_percent':{'laser':1.0696,'plasma':6.0951},
    'new_imports':0,'new_searches':0,'new_native_sessions':0,'held_out_geometry_read':False,
    'gate_weights_changed':False,'release_created':False}
(OUT/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'all_review_checks_pass':True,'unchanged_core_sources':len(identities),'historical_measurement_scope_preserved':True}))
