"""Repair two report link targets altered by prose formatting; retain the failed text."""
from pathlib import Path
from hashlib import sha256
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];NAME='h5-cog-site-mask-and-rigid-component-searches-20261029';OUT=ROOT/'benchmarks/results'/NAME;report=OUT.with_suffix('.md')
before=report.read_bytes();(OUT/'report-before-link-correction.txt').write_bytes(before)
def prose(s):
    s=s.replace('Validshort11','Valid short11')
    def spaced(m):
        return m[0] if m[0].lower() in {'short','full','first','fixed','valid','partial'} else m[0]+' '
    s=re.sub(r'[A-Za-z]{2,}(?=\d)',spaced,s)
    s=re.sub(r',(?=\d)',', ',s)
    s=re.sub(r'(?<=\d)  +',' ',s)
    return s
def format_md(s):
    pieces=re.split(r'(\]\([^)]*\)|`[^`]*`)',s)
    return ''.join(piece if piece.startswith('](') or piece.startswith('`') else prose(piece) for piece in pieces)
text=before.decode('utf-8');badlinks=['all 105-area-bounds.json','all 105-capacity-bounds.json']
for name in badlinks:
    assert text.count(name)==1,name
    text=text.replace(name,name.replace('all 105','all105'))
report.write_text(format_md(text),encoding='utf-8',newline='\n')
for name in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    p=ROOT/name;s=p.read_text(encoding='utf-8');marker='**N4 cog-site masks, rigid components and occupied-area bounds, 2026-10-29:**';assert s.count(marker)==1
    pos=s.index(marker);p.write_text(s[:pos]+format_md(s[pos:]),encoding='utf-8',newline='\n')
baseline=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
assert (ROOT/'BENCHMARKS.md').read_bytes().startswith(baseline)
record={'stage':'first archive verifier report-link check','result':'failed','error':'AssertionError for all 105-area-bounds.json; two link targets had acquired a space during prose formatting','original_report_preserved':'report-before-link-correction.txt','original_report_sha256':sha256(before).hexdigest(),'correction':'Repair both link targets to their existing all105 filenames and format prose while protecting link destinations and code spans. Source evidence, solver results, hashes, ZIPs and prior benchmark text remain unchanged. Rerun the same verifier.','corrected_report_sha256':sha256(report.read_bytes()).hexdigest(),'BENCHMARKS_prior_prefix_preserved':True,'raw_archive_unchanged':True}
with (OUT/'publication-correction.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(record,f,indent=2);f.write('\n')
print(record)
