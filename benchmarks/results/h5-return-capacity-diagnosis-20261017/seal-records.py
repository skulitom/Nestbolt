"""Retain complete large trace records in a verified archive plus a compact index."""
from pathlib import Path
from hashlib import sha256
import json,shutil,zipfile
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-return-capacity-diagnosis-20261017'
digest=lambda p:sha256(p.read_bytes()).hexdigest()
names=['records.json','results.json']
inventory={name:{'bytes':(out/name).stat().st_size,'sha256':digest(out/name)} for name in names}
archive=out/'original-records.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in names:z.write(out/name,name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(names)
    for name,row in inventory.items():
        data=z.read(name);assert len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256']
integrity={'archive':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'members':inventory,'all_members_and_crc_verified':True}
(out/'records-integrity.json').write_text(json.dumps(integrity,indent=2)+'\n',encoding='utf-8',newline='\n')
summary=json.loads((out/'results.json').read_bytes())
for row in summary['records']:
    del row['diagnosis']['traces']
    row['diagnosis']['complete_traces']={'archive':row['archive'],'member':'search-stderr.log','prefix':'OBSTRUCTION_DIAG '}
summary['complete_original_records']=integrity
summary['reproduction']='Extract records.json and results.json from original-records.zip here before running the retained finish/audit/render helpers. Those exact large files remain locally and are ignored by Git; no original data is discarded.'
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'seal-records.py')
ignore='\n# Complete capacity traces are retained in the verified original-records.zip.\n'
ignore+='\n'.join('/benchmarks/results/h5-return-capacity-diagnosis-20261017/'+name for name in names)+'\n'
with (root/'.gitignore').open('a',encoding='utf-8',newline='\n') as f:f.write(ignore)
print(json.dumps(integrity))
