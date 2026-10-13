"""Freeze the N0 corpus once, before N1, with a metadata-only held-out draw.

Never reads labels when selecting the split. Lineages unite native derivatives,
same-source DXF/SVG stems, and byte-identical originals. Writer quotas use largest
remainders for 20% real files, plus exactly 20% native files. A seeded SHA-256
ordering and first-feasible subset DP make the grouped allocation reproducible.
"""
import argparse
from collections import Counter
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from shop_sources import ROOT,CORPUS,ALLOWED,load_lock
from shop_reference_labels import write_json

SEED='nestbolt-v1.1-h1-110113'


def allocation(files):
    pool=[r for r in files if r['set'] in ['real','lightburn-native']]
    by_path={r['path']:r for r in pool};parent={p:p for p in by_path}
    def find(p):
        while parent[p]!=p:parent[p]=parent[parent[p]];p=parent[p]
        return p
    def union(a,b):parent[find(b)]=find(a)
    hashes={};stems={}
    for r in pool:
        p=r['path']
        if r.get('derived_from') in by_path:union(p,r['derived_from'])
        if r['sha256'] in hashes:union(p,hashes[r['sha256']])
        hashes[r['sha256']]=p
        if r['set']=='real':
            # Collection prefixes the original filename with eight hash digits.
            stem=(str(Path(p).parent),Path(p).stem.split('-',1)[1].lower())
            if stem in stems:union(p,stems[stem])
            stems[stem]=p
    components={}
    for r in pool:components.setdefault(find(r['path']),[]).append(r)
    totals=Counter(r['writer']['name'] for r in pool if r['set']=='real')
    real_target=round(sum(totals.values())*.2)
    quotas={k:int(n*.2) for k,n in totals.items()}
    for k in sorted(totals,key=lambda k:(-(totals[k]*.2-quotas[k]),k))[:real_target-sum(quotas.values())]:quotas[k]+=1
    names=sorted(totals);target=tuple(quotas[k] for k in names)+(round(sum(r['set']=='lightburn-native' for r in pool)*.2),)
    groups=[]
    for rows in components.values():
        paths=sorted(r['path'] for r in rows);key=sha256((SEED+'\n'+'\n'.join(paths)).encode()).hexdigest()
        vector=tuple(sum(r['set']=='real' and r['writer']['name']==k for r in rows) for k in names)+(sum(r['set']=='lightburn-native' for r in rows),)
        groups.append({'id':key,'paths':paths,'counts':vector})
    groups.sort(key=lambda g:g['id']);dp={tuple(0 for _ in target):[]}
    for i,g in enumerate(groups):
        for current,selected in list(dp.items()):
            nxt=tuple(a+b for a,b in zip(current,g['counts']))
            if all(a<=b for a,b in zip(nxt,target)) and nxt not in dp:dp[nxt]=selected+[i]
    if target not in dp:raise ValueError('No grouped allocation meets the writer quotas; do not silently relax them')
    selected=set(dp[target]);held={p for i in selected for p in groups[i]['paths']}
    return held,{'seed':SEED,'fraction':.2,'real_writer_population':dict(totals),
        'real_writer_held_out_quotas':quotas,'real_held_out_count':real_target,
        'native_held_out_count':target[-1],'dimensions':names+['native LightBurn'],
        'method':'SHA-256 ordered lineage components; first-feasible dynamic-programming subset with exact largest-remainder writer quotas. Labels, warnings, geometry and product results are not inputs.',
        'lineage_rule':'Native derivatives and their real parent, same source-repository original filename stem across formats, and byte-identical originals stay in one partition.',
        'groups':[{**g,'split':'held_out' if i in selected else 'training'} for i,g in enumerate(groups)]}


def inventory(files):
    known={r['path']:{'licence':r['licence'],'source':r['source']} for r in files}
    native=json.loads((CORPUS/'native/manifest.json').read_text(encoding='utf-8'))
    for r in native['files']:known[r['path']]={'licence':r['licence'],'source':r.get('derived_from',r.get('source','Original Nestbolt MIT probe'))}
    generated=json.loads((CORPUS/'generated/manifest.json').read_text(encoding='utf-8'))
    for r in generated['bases']:known[r['path']]={'licence':'MIT','source':r['source']}
    for r in files:
        for k in ['label','reference_render']:
            if r.get(k):known[r[k] if isinstance(r[k],str) else r[k]['path']]={'licence':r['licence'],'source':r['path']}
    lock=load_lock(CORPUS/'sources.lock.json')
    for source in lock['sources']:
        for e in source['evidence']:known[e['path']]={'licence':source['licence'],'source':e['source_url']}
    refs=json.loads((CORPUS/'references/public/manifest.json').read_text(encoding='utf-8'))
    warning=refs['font_warning_image'];known[warning['path']]={'licence':warning['licence'],'source':warning['derived_from']}
    for row in refs['rows']:
        for r in row['files']:known[r['path']]={'licence':r['licence'],'source':row['source']}
    result=[]
    for p in sorted(CORPUS.rglob('*')):
        if not p.is_file() or p.name in ['manifest.json.sha256'] or p==CORPUS/'manifest.json':continue
        relative=p.relative_to(CORPUS).as_posix()
        info=known.get(relative)
        if info is None:
            # Explicit directories of original Nestbolt metadata/probes/bases;
            # source geometry must have been covered by the maps above.
            allowed=(relative.startswith(('probes/','oracle-tool/')) or
                     p.suffix in ['.json','.md','.txt'] or relative=='oracle-tool/LICENSE')
            if not allowed:raise ValueError('Unattributed file: '+relative)
            info={'licence':'MIT','source':'Original Nestbolt authoring metadata/probe; repository LICENSE, except oracle-tool third-party MIT notice'}
        if info['licence'] not in ALLOWED:raise ValueError('Non-permissive '+relative)
        result.append({'path':relative,'sha256':sha256(p.read_bytes()).hexdigest(),**info})
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    target=CORPUS/'manifest.json'
    if args.check:
        manifest=json.loads(target.read_text(encoding='utf-8'))
        for r in manifest['corpus_inventory']:
            assert sha256((CORPUS/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
        digest=sha256(target.read_bytes()).hexdigest();assert (CORPUS/'manifest.json.sha256').read_text().split()[0]==digest
        print(json.dumps({'H1_frozen_integrity':True,'inventory_files':len(manifest['corpus_inventory']),'manifest_sha256':digest}));return
    if target.exists():raise ValueError('Already frozen; only --check is allowed')
    draft=json.loads((CORPUS/'manifest.draft.json').read_text(encoding='utf-8'))
    files=draft['files'];held,split=allocation(files)
    write_json(ROOT/'output/shop-split-candidate.json',split)
    print(json.dumps({k:v for k,v in split.items() if k!='groups'}))
    if not args.write:return
    for r in files:
        assert sha256((CORPUS/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
        if r['set'] in ['real','lightburn-native','public-lightburn','generated']:
            assert r.get('label') and sha256((CORPUS/r['label']).read_bytes()).hexdigest()==r['label_sha256'],r['path']
        r['split']='held_out' if r['path'] in held else 'robustness' if r['set']=='robustness' else 'reference' if r['set']=='oracle-svg' else 'training'
    counts=Counter(r['set'] for r in files)
    assert counts['real']>=60 and counts['lightburn-native']==50 and counts['public-lightburn']>=40 and counts['robustness']>=150 and counts['generated']>=100
    assert split['real_writer_population'].get('Fusion 360',0)>=25
    assert len({Path(r['path']).parts[1] for r in files if r['set']=='real'})>=8
    authored=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    scripts={p.relative_to(ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in (ROOT/'scripts').glob('shop_*') if p.is_file()}
    frozen={'schema_version':1,'state':'frozen','frozen_at':datetime.now(timezone.utc).isoformat(),
        'authoring_commit':authored,'implementation_started':False,'counts':dict(counts),
        'split':split,'files':files,'corpus_inventory':inventory(files),'authoring_scripts_sha256':scripts,
        'held_out_policy':'Never read held-out geometry/labels for tuning after this freeze. Gate-only evaluation; report failures without changing these expectations or allocation.',
        'negative_fixture_policy':'Malformed/empty/incomplete negative fixtures do not earn successful H2 imports. Labels and actionable failures remain visible in the denominator; no result-dependent split selection.',
        'licence':'MIT for original manifest metadata; original/derived file licences remain as recorded per inventory row.'}
    write_json(target,frozen);digest=sha256(target.read_bytes()).hexdigest()
    (CORPUS/'manifest.json.sha256').write_text(digest+'  manifest.json\n',encoding='utf-8',newline='\n')
    print(json.dumps({'frozen':True,'manifest_sha256':digest,'held_out_real':split['real_held_out_count'],'held_out_native':split['native_held_out_count']}))


if __name__=='__main__':main()
