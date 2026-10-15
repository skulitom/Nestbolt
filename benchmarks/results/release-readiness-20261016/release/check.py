"""Check the exact failure's behavior with the existing release executable."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import h4_full_matrix as full
from h6_material_cost import run, equivalent

out=ROOT/'benchmarks/results/release-readiness-20261016/release'
out.mkdir(exist_ok=False)
before=full.guards(full.cases())
assert before==full.load(ROOT/'benchmarks/results/h4-full-development-20261015/plan.json')['guards']
cli=ROOT/'target/release/nestbolt.exe'
job=out.parent/'search/job.json'
record={'scope':'Functional check on CCD1 CPU 16; no benchmark claim.',
        'cli_sha256':sha256(cli.read_bytes()).hexdigest(), 'job_sha256':sha256(job.read_bytes()).hexdigest()}
record['search']=run([cli,'sheets','--job',job,'--output',out/'layout.json','--seed','659','--seconds','2','--repeatable'],out,'search',16,60)
if record['search']['exit_code']==0:
    result=full.load(out/'search-stdout.json')
    record['validation']=run([cli,'validate','--job',job,'--layout',out/'layout.json'],out,'validate',16,60)
    if record['validation']['exit_code']==0:
        check=full.load(out/'validate-stdout.json')
        record['valid']=check['valid']
        record['metric_delta']=equivalent(result['validation']['metrics'],check['metrics'])
        record['placements']=len(full.load(out/'layout.json')['placements'])
record['guards_unchanged']=full.guards(full.cases())==before
assert record['guards_unchanged']
(out/'checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'check.py')
print(json.dumps(record,indent=2))
