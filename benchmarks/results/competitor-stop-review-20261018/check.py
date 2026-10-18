"""Read public shipment descriptions only; no solver code or benchmark changes."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from html.parser import HTMLParser
import json,re,subprocess,urllib.request
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/competitor-stop-review-20261018';out.mkdir(exist_ok=False)
class Visible(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Nestbolt-shipment-review'}),timeout=30) as r:return r.read(),r.status,r.geturl()
site='https://sparrowstudio.app/';body,status,url=fetch(site);parser=Visible();parser.feed(body.decode('utf-8'));plain=' '.join(' '.join(parser.parts).split())
excerpts=['does not allocate parts across multiple fixed-size sheets','placing other parts inside holes is not supported'];assert all(q in plain for q in excerpts)
commit=subprocess.check_output(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha'],text=True,cwd=root).strip();assert re.fullmatch('[0-9a-f]{40}',commit)
readme_url=f'https://raw.githubusercontent.com/JeroenGar/sparrow-studio/{commit}/README.md';readme,rs,ru=fetch(readme_url);excerpt='in development and not published yet';assert excerpt in readme.decode('utf-8')
record={'utc':datetime.now(timezone.utc).isoformat(),'scope':__doc__,'site':{'url':site,'final_url':url,'status':status,'bytes':len(body),'sha256':sha256(body).hexdigest(),'short_excerpts':excerpts},'repository':{'url':f'https://github.com/JeroenGar/sparrow-studio/blob/{commit}/README.md','commit':commit,'raw_url':ru,'status':rs,'readme_bytes':len(readme),'readme_sha256':sha256(readme).hexdigest(),'short_excerpt':excerpt},'finding':'The published description continues to exclude automatic multi-sheet allocation and placing parts inside holes. The repository distinguishes the published web app from the unpublished new app.','shipment_stop_rule_triggered':False,'scope_limit':'Availability-description check only, not a new solver capability test, benchmark or claim about unpublished code.','production_or_frozen_competitors_changed':False}
(out/'review.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
doc=f'''# Competitor shipment check — 2026-10-18

The [published Sparrow Studio description]({site}) still excludes automatic
allocation across multiple fixed sheets and placing parts inside holes. Its
[repository README at the checked commit](https://github.com/JeroenGar/sparrow-studio/blob/{commit}/README.md)
distinguishes the published web app from the new, unpublished app.

The plan's shipment stop condition is not triggered by these sources. This is
an availability-description check, not a benchmark or a solver capability test.
No competitor code, dependency, production setting or frozen result changes.
[The review](competitor-stop-review-20261018/review.json) records response hashes,
the exact repository commit and short supporting excerpts.
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
print(json.dumps({'commit':commit,'shipment_stop_rule_triggered':False,'review':str(out/'review.json')}))
