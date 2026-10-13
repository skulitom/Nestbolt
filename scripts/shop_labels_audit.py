"""Check pre-freeze label/provenance completeness without invoking Nestbolt."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from shop_sources import CORPUS, ROOT


def main():
    manifest=json.loads((CORPUS/'manifest.draft.json').read_text(encoding='utf-8'))
    counts=Counter(); negative=[]; pending=[]; rendered=set(); errors=[]
    required={'real','lightburn-native','public-lightburn','generated'}
    for row in manifest['files']:
        def check(condition,message):
            if not condition: errors.append(row['path']+': '+message)
        check(sha256((CORPUS/row['path']).read_bytes()).hexdigest()==row['sha256'],'source hash')
        if row['set'] not in required: continue
        if not row.get('label'): pending.append(row['path']); continue
        data=(CORPUS/row['label']).read_bytes(); label=json.loads(data)
        check(sha256(data).hexdigest()==row['label_sha256'],'label hash')
        check(label['sha256']==row['sha256'] and label['file']==row['path'],'label source identity')
        for key in ['cut_parts','cut_layers','expected_warnings','derivation','import_options']:
            check(key in label,'missing '+key)
        for part in label['cut_parts']:
            b=part['outer_bounds_mm']; size=part['outer_size_mm']
            check(len(b)==4 and b[2]>b[0] and b[3]>b[1],'degenerate part bounds')
            check(max(abs(a-c) for a,c in zip([b[2]-b[0],b[3]-b[1]],size))<1e-7,'inconsistent part sizes')
            check(isinstance(part['holes'],int) and part['holes']>=0,'invalid hole count')
        if label.get('negative_fixture'):
            check(bool(label.get('expected_failure')),'negative fixture lacks actionable failure')
            negative.append(row['path'])
        if row['set']!='generated':
            r=row.get('reference_render');check(bool(r),'missing reviewed render')
            if r:
                check(sha256((CORPUS/r['path']).read_bytes()).hexdigest()==r['sha256'],'render hash')
                check(r['licence']==row['licence'],'render licence')
                rendered.add(r['path'])
        counts[row['set']]+=1
    result={'recorded_at':datetime.now(timezone.utc).isoformat(),
            'scope':'N0 authoring/provenance only; no Nestbolt import or quality claim',
            'label_counts':dict(counts),'total_labels':sum(counts.values()),
            'unique_reviewed_renders':len(rendered),'negative_fixtures':negative,
            'negative_fixture_policy':'These do not earn an H2 successful-import result; malformed, empty or ambiguous inputs require clear actionable rejection.',
            'pending_labels':pending,'integrity_checks_pass':not errors,'errors':errors,
            'H1':False,'H2':False,'completed_milestone_weight_percent':0}
    (ROOT/'benchmarks/results/n0-labels-20261013.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['pending_labels','negative_fixtures','scope','negative_fixture_policy']}))
    print('Remaining labels:',len(pending))
    if errors: raise SystemExit(1)


if __name__=='__main__':main()
