"""Read-only counter review of all previously retained H5 schedule trials."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'benchmarks/results/h5-schedule-probe-20261015T152046Z'
OUT=ROOT/'benchmarks/results/h5-relocation-inspection-20261016'
OUT.mkdir(exist_ok=False)
raw=(SOURCE/'results.json').read_bytes()
assert sha256(raw).hexdigest()=='433d28ed64c078f6b6de0a4605449e4cd716fba92dc89c0dfbdd95b2f287b973'
data=json.loads(raw)
assert len(data['rows'])==36 and data['held_out_geometry_read'] is False
groups=defaultdict(list)
rows=[]
for row in data['rows']:
    archive=SOURCE/row['archive']
    assert sha256(archive.read_bytes()).hexdigest()==row['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        member=z.read('nested/result.json')
    assert sha256(member).hexdigest()==row['artifacts']['nested/result.json']
    saved=json.loads(member)
    assert saved['stats']==row['stats'] and saved['history']==row['history']
    assert row['status']=='valid' and saved['validation']['valid']
    entry={k:row[k] for k in ['job','kerf_mm','seed','warm_fraction','material','warm_material','stats','history','archive','archive_sha256']}
    entry['result_sha256']=sha256(member).hexdigest()
    rows.append(entry)
    groups[row['warm_fraction']].append(entry)
summaries={}
for warm,group in sorted(groups.items()):
    assert len(group)==12
    counts=Counter()
    for row in group:
        counts.update(row['stats'])
    summaries[str(warm)]={'runs':len(group),'totals':dict(counts),
        'runs_with_no_counted_separated_insertion_outcome':sum(r['stats']['separated_insertions']+r['stats']['failed_insertions']==0 for r in group),
        'runs_with_direct_insertions':sum(r['stats']['direct_insertions']>0 for r in group)}
code=(ROOT/'crates/core/src/sheets/vstrip.rs').read_bytes()
old=subprocess.check_output(['git','show',data['product_commit']+':crates/core/src/sheets/vstrip.rs'],cwd=ROOT)
def section(source):
    return source[source.index(b'    fn relocate('):source.index(b'    /// Run one window')].replace(b'\r\n',b'\n')
assert section(code)==section(old)
record={'scope':'Read-only historical development evidence; no new searches, no product changes, no held-out evaluation.',
        'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),
        'results_sha256':sha256(raw).hexdigest(),'product_commit':data['product_commit'],
        'relocate_implementation_unchanged':True,'summaries':summaries,'rows':rows,
        'interpretation':'Zero separated/failed insertion counters mean no counted local separation outcome, not proof that relocate was never entered. Direct insertions short-circuit the initial relocate call; the later retry requires three stalled separation outcomes and available budget. Global disrupt swaps are not counted as these insertions.'}
(OUT/'checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,OUT/'inspect.py')
print(json.dumps(summaries,indent=2))
