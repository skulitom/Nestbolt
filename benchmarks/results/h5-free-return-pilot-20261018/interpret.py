from pathlib import Path
from hashlib import sha256
import json
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-free-return-pilot-20261018'
r=json.loads((out/'results.json').read_bytes());pairs=r['summary']['pairs'];failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
assert len(failed)==5 and all(p['complete'] for p in pairs)
mechanical=[p for p in pairs if p['job'].startswith('m-mechanical-')]
assert sum(p['arms']['candidate']['exchanges'] for p in mechanical)==8
assert sum(p['arms']['candidate']['exchange_attempts'] for p in mechanical)==75
followup=('Reject integration and a full H5 run for this candidate. All four mechanical comparisons remain above the original +1% material limit, and the 1.5 mm bracket comparison also fails. '
 'The candidate accepts eight of 75 mechanical exchange attempts, but aggregate counters cannot identify which physical members moved, the return-seed choices, the accepted height reductions or the remaining rejection causes. '
 'The authored gains therefore do not establish a useful final development improvement. The next step is a separately qualified observation-only diagnostic of this exact failed candidate: both mechanical jobs, both kerfs, seed zero and the original 60-second budget, serially on CCD0 CPU 8. '
 'Capture the actual returned poses before and after free-space seeding, source repair loss, charged work and actual whole-job material outcomes, including accepted trials. Do not recompute a former seed formula as if it were the actual new seed. '
 'Prove that removing instrumentation recovers the candidate exactly, retain all 137 tests, qualify the reader with actual authored outcomes and malformed records, and independently validate saved original geometry. Logging may perturb wall trajectories, so the diagnostic must make no quality claim. '
 'Use that evidence before selecting another search change; do not repeat this unchanged quality pilot, relax limits, integrate it or open reserved inputs.')
record={'failed_material_pairs':len(failed),'results_sha256':sha256((out/'results.json').read_bytes()).hexdigest(),'quality_claim':False,'followup':followup}
(out/'interpretation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'failed_material_pairs':len(failed),'mechanical_accepted':8,'mechanical_attempts':75,'next':'Qualified observation-only return-seed and acceptance diagnosis'}))
