"""Read the sealed archive, all aliases/bindings and every local report link."""
from pathlib import Path
from hashlib import sha256
import json,re,zipfile
ROOT=Path(__file__).resolve().parents[3];NAME='h5-finite-source-poses-and-equivalent-graph-reduction-20261029';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes());digest=lambda b:sha256(b).hexdigest()
manifest=load(OUT/'raw-manifest.json');files={r['path']:r for r in manifest['files']};blobs={};jsons=0
for a in manifest['archives']:
    p=OUT/a['path'];assert p.stat().st_size==a['bytes'] and digest(p.read_bytes())==a['sha256']
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
        for n in z.namelist():
            r=files[n];data=z.read(n);assert r['archive']==a['path'] and len(data)==r['bytes'] and digest(data)==r['sha256'];blobs[n]=data
            if n.endswith('.json'):json.loads(data);jsons+=1
assert set(blobs)==set(files)
for r in manifest['aliases']:
    data=blobs[r['canonical']];assert len(data)==r['bytes'] and digest(data)==r['sha256'];blobs[r['path']]=data
bindings=load(OUT/'source-bindings.json')
for n,h in bindings.items():assert digest(blobs['source-inputs/'+n])==h==digest((ROOT/n).read_bytes())
report=OUT.with_suffix('.md');links=[]
for target in re.findall(r'\]\(([^)]+)\)',report.read_text(encoding='utf-8')):
    if '://' in target:continue
    p=(report.parent/target).resolve();assert p.is_file() or p==(OUT/'archive-checks.json').resolve(),target;links.append(target)
for p in OUT.glob('*.json'):load(p)
result={'passed':True,'archive_parts':len(manifest['archives']),'canonical_members_verified':len(files),
    'identical_aliases_verified':len(manifest['aliases']),'source_bindings_verified':len(bindings),'archived_json_files_parsed':jsons,
    'local_report_links_verified':len(links),'archive_bytes':sum(a['bytes'] for a in manifest['archives']),'verifier_sha256':digest(Path(__file__).read_bytes()),'report_sha256':digest(report.read_bytes()),'own_output_link_deferred_until_output_written':True}
with (OUT/'archive-checks.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
for target in links:assert (report.parent/target).resolve().is_file(),target
assert load(OUT/'archive-checks.json')['passed']
print(result)
