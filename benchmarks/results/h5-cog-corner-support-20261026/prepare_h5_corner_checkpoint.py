"""Freeze the next evidence checkpoint without changing the CI-tested tree."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess
from pack_h5_evidence_archive import pack,digest
ROOT=Path(__file__).resolve().parents[1];NAME='h5-cog-corner-support-20261026';OUT=ROOT/'output'/f'{NAME}-checkpoint'
CAP=ROOT/'output/h5-corrected49-cog-capacity-20261026';CORNER=ROOT/'output/h5-cog-corner-support-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
assert load(CAP/'audit-bitset/checks.json')['passed'] and load(CORNER/'audit/checks.json')['passed']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='babe73b661efe8ac84c4f73c5823a7178274ec00'
assert not subprocess.check_output(['git','diff','HEAD','--name-only'],cwd=ROOT).strip()
OUT.mkdir()
for p,n in [(CAP/'result.json','capacity-result.json'),(CAP/'audit-bitset/checks.json','capacity-checks.json'),(CAP/'audit/interrupted.json','interrupted-reader.json'),
 (CORNER/'proof.json','corner-proof.json'),(CORNER/'audit/checks.json','corner-checks.json'),(CORNER/'audit/necessity-proof.json','necessity-proof.json'),
 (CORNER/'cog-cell-table.json','cog-cell-table.json'),(CORNER/'prepared.json','corner-prepared.json')]:shutil.copyfile(p,OUT/n)
members={};queue=[];bindings={}
for folder in [CAP,CORNER]:
    for p in folder.rglob('*'):
        if p.is_file():
            members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
            if p.name=='plan.json':queue.append(p)
seen=set()
while queue:
    p=queue.pop()
    if p in seen:continue
    seen.add(p)
    for n,h in load(p).get('inputs',{}).items():
        q=ROOT/n;assert digest(q)==h,n;bindings[n]=h;members['source-inputs/'+n]=q
        if q.name=='plan.json':queue.append(q)
for n,h in load(CORNER/'audit/inputs.json').items():
    q=ROOT/n;assert digest(q)==h,n;bindings[n]=h;members['source-inputs/'+n]=q
write(OUT/'source-bindings.json',bindings)
for name in ['prove_h5_corrected49_cog_capacity.py','audit_h5_corrected49_cog_capacity.py','repair_h5_capacity_reader_cost.py',
 'audit_h5_corrected49_cog_capacity_bitset.py','prepare_h5_cog_corner_support.py','audit_h5_cog_corner_support.py','pack_h5_evidence_archive.py','ccd1.py']:
    members['helpers/'+name]=ROOT/'output'/name
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'utc':datetime.now(timezone.utc).isoformat(),'source_head':'babe73b661efe8ac84c4f73c5823a7178274ec00',
 'capacity_graph_pairs_verified':9420646,'capacity_certificate_nodes_replayed':199989,'first_sheet_capacity_unresolved':True,'short_sheet_upper_bound':3,
 'all_angle_corner_boxes_verified':1116,'additional_cells_excluded':34,'remaining_cells':4514,'prior15_cells_retained':True,
 'closed_capacity_searches_not_repeated':True,'interrupted_reader_preserved_and_bitset_reader_passed':True,
 'additional_external_solver_calls':0,'native_calls':0,'full66_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive})
write(OUT/'next-step.json',{'action':'The current tracked tree is still exactly babe73b6. Hosted Checks40412648984 is validating that head; preserve the live run and push babe73b6 normally to main only after all six jobs succeed and remote main remains36f162d0. Then capture its main CI handle and do not cancel that run. This prepared evidence bundle is not yet installed under benchmarks/results or committed: after a safe checkpoint, copy it to benchmarks/results/h5-cog-corner-support-20261026, write its report and append BENCHMARKS/plan/research/status. Preserve the200000-node closed capacity probe, its199989 checked partial certificate nodes, the interrupted slow reader and repaired88.2633-second reader. First13 capacity is UNKNOWN;14/15 consumed zero nodes after the shared cap. The only proved count is short<=3. The new actual-tooth corner theorem adds1116 certified boxes and removes only34 cells; do not treat that modest reduction as a full placement or sufficient reason to repeat an unchanged feasibility search. Next seek a materially stronger geometric decomposition or different source construction with all66 mandatory. H2 unchanged;22 reserved vectors unopened; no release qualifies.','completion_percent':60,'H2_complete':False,'H5_complete':False})
shutil.copyfile(__file__,OUT/Path(__file__).name)
print({'prepared_checkpoint':str(OUT),**archive})
