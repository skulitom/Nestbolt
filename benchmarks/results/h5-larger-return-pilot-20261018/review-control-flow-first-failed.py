"""Read-only source/counter review; does not infer quality from accepted swaps."""
from pathlib import Path
from hashlib import sha256
import json,shutil
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-larger-return-pilot-20261018'
probe=root/'output/h5-larger-return-probe-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert load(out/'verification.json')['all_original_archives_verified']
assert load(out/'filled-outer-audit.json')['all_holes_reserved']
result=load(out/'results.json');rows=[r for r in result['records'] if r['arm']=='candidate'];assert len(rows)==24
summary=[{k:r[k] for k in ['job','kerf_mm','seed','stats','material']} for r in rows]
assert sum(r['stats'].get('directed_exchanges',0) for r in rows)==13
assert max(r['stats'].get('directed_exchanges',0) for r in rows)==1
assert all(r['stats'].get('eliminated_sheets',0)==0 for r in rows)
sources={}
for rel,first,last in [
 ('crates/core/src/sheets/vstrip.rs','            let mut filled = false;','                        filled = false;'),
 ('crates/core/src/sheets/vstrip/exchange.rs','                    let after = report.metrics.as_ref().expect("valid exchange");','                    return Ok(1);')]:
    p=probe/'candidate'/rel;expected=load(probe/'build.json')['source_sha256'].get(rel)
    if expected:assert digest(p)==expected
    else:
        old=next(x for x in load(probe/'preparation.json')['old_source_files']['candidate'] if x['path']==rel)
        assert digest(p)==old['sha256']
    s=p.read_text(encoding='utf-8');start=s.index(first);end=s.index(last,start)+len(last)
    sources[rel]={'sha256':digest(p),'start_line':s[:start].count('\n')+1,'snippet':s[start:end]}
text='''The 24 candidate searches accept at most one directed exchange each;
13 accept one and none eliminate a sheet. The source returns immediately after
the first accepted exchange. The window call is guarded by `filled`, which is
reset on sheet elimination or a new window. The current source therefore does
not spend the remaining part of that same opportunity on consecutive accepted
exchanges. This is a source observation, not proof that time remained or that
another exchange was feasible or beneficial.

Removing the area filter enables ten accepted pairs, including one mixed pair,
but panel-hardware still records no mixed attempts. The completed material
comparison fails five pairs, so broader eligibility alone is insufficient.
Before choosing another runtime change, observe accepted before/after material,
actual returned inventories, post-fill material and remaining phase time, plus
where panel-hardware exhausts or rejects its pair choices. Preserve the failed
quality run and existing budgets. Any later consecutive-exchange experiment
must prevent cycles, retain an independently valid incumbent after every step,
respect all original time/material/geometry checks and undergo a new matched
comparison. Current counters establish none of those possible benefits.
'''
record={'production_changed':False,'new_searches':0,'candidate_cases':24,'accepted':13,'maximum_per_search':1,
 'eliminated_sheets':0,'source':sources,'records':summary,'interpretation_and_next_step':text,
 'H5_complete':False,'integrated':False}
(out/'control-flow-review.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
with (out.parent/(out.name+'.md')).open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n\n## Read-only follow-up\n\n'+text+'\n[Source and counter review](h5-larger-return-pilot-20261018/control-flow-review.json).\n')
shutil.copyfile(__file__,out/'review-control-flow.py')
print(json.dumps({'accepted':13,'maximum_per_search':1,'new_searches':0,'production_changed':False}))
