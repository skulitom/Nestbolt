"""Connect retained panel traces to original part families; no new solver run."""
from pathlib import Path
from hashlib import sha256
import json,shutil,zipfile
root=Path(__file__).resolve().parents[1];old=root/'benchmarks/results/h5-exact-state-20261018'
out=root/'output/h5-neutral-frontier-review-20261018';assert (out/'checks.json').exists()
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
dependency=Path('C:/Users/artem/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/jagua-rs-1.1.0/src')
files=[root/'output/h5-exact-state-20261018/workspace/crates/core/src/sheets.rs',
    root/'output/h5-exact-state-20261018/workspace/crates/core/src/sheets/vstrip/exchange.rs',
    dependency/'probs/spp/io/import.rs',dependency/'io/import.rs',dependency/'probs/spp/entities/instance.rs']
sources={str(p):digest(p) for p in files}
model=files[0].read_text(encoding='utf-8');importer=files[2].read_text(encoding='utf-8');instance=files[4].read_text(encoding='utf-8')
assert 'for (id, part) in job.parts.iter().enumerate()' in model
assert 'part.push(usize::try_from(item.external_id())?);' in model
assert '.filter(|item| item.demand > 0)' in importer and '.enumerate()' in importer
assert 'importer.import_item(&item.base, idx)?' in importer
assert 'instance_item_indices_correct(&items)' in instance and 'Self { items, base_strip }' in instance
verification=load(old/'verification.json');assert verification['all_traces_verified']
rows=[]
for record in verification['archives']:
    p=old/record['path'];assert digest(p)==record['sha256']
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        job=json.loads(z.read('nested/job.json'));assert all(p['quantity']>0 for p in job['parts'])
        # The imported index is enumeration of positive-demand items. Here all
        # demands are positive, so it matches the original job part index.
        names=[p['id'] for p in job['parts']]
        traces=[json.loads(line[len('LARGER_DIAG '):]) for line in z.read('search-stderr.log').decode().splitlines() if line.startswith('LARGER_DIAG ')]
        assert len(traces)==1;trace=traces[0]
        choices=[[names[i] for i in choice] for choice in trace['pair_choices']]
        attempts=[]
        for attempt in trace['attempts']:
            proposal=trace['proposals'][attempt['proposal_index']]
            attempts.append({'incoming':[names[i] for i in proposal['incoming_ids']],
                'returned':[names[i] for i in proposal['returned_ids']],
                'paired':proposal['paired'],'outcome':attempt['outcome']})
        rows.append({'archive':record['path'],'sha256':record['sha256'],
            'index_to_original_part':names,'available_source_families':sorted({names[i] for i in trace['available_source_items']}),
            'pair_choices':choices,'first_insert_pair_zero_based':next((i for i,c in enumerate(choices) if 'insert' in c),None),
            'attempts':attempts,'attempts_selecting_insert':sum('insert' in a['incoming'] for a in attempts)})
checks={'all_checks_passed':True,'archived_diagnostics':len(rows),
    'attempts':sum(len(r['attempts']) for r in rows),
    'attempts_selecting_insert':sum(r['attempts_selecting_insert'] for r in rows),
    'records':rows,'source_sha256':sources,
    'mapping_basis':'Input job parts are enumerated as external IDs; all have positive demand. The pinned importer enumerates those entries, retains the external ID, and SPInstance checks index-to-position equality.',
    'limits':'These two earlier diagnostics predate the material-profile branch. Their selection coverage must not be attributed to the new pilot. No new geometry, search, quality claim or global packing bound.',
    'new_searches':0,'production_changed':False}
(out/'choices.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'inspect-choices.py')
print(json.dumps({k:v for k,v in checks.items() if k not in ['records','source_sha256']}))
