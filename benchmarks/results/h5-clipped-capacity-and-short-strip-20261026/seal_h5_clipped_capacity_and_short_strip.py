"""Preserve the stricter occupancy model and the distinct finite short-strip attempt."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-clipped-capacity-and-short-strip-20261026';OUT=ROOT/'benchmarks/results'/NAME;CAP=ROOT/'output/h5-paired-strip-clipped-capacity-20261026';STRIP=ROOT/'output/h5-six-insert-cog-short-sheet-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-paired-strip-clearance-capacity-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0];assert head==main=='cb7f7b1f414c9ebeccc61873f7046bae8b024f66'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40359411459','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main
ci_pass=ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
audits={'clipped-geometry':CAP/'audit/checks.json','clipped-model':CAP/'model/checks.json','clipped-response':CAP/'response-audit/checks.json','short-source-readback':STRIP/'audit/checks.json'};assert all(load(p)['passed'] for p in audits.values())
geometry=load(audits['clipped-geometry']);response=load(audits['clipped-response']);short=load(audits['short-source-readback'])
assert geometry['additional_geometric_conflicts']==139 and response['status']=='UNKNOWN' and response['closed'] and short['accepted_13_part_candidates']==0 and short['saved_finite_queries_read_back']==144
OUT.mkdir()
for label,p in audits.items():shutil.copyfile(p,OUT/(label+'-checks.json'))
for p,name in [(CAP/'audit/necessity-proof.json','clipped-necessity-proof.json'),(CAP/'audit/new-edge-certificates.json','139-new-edge-certificates.json'),(CAP/'search/result.json','closed-capacity-result.json'),(CAP/'search/process.json','closed-capacity-process.json'),(CAP/'search/solver.log','closed-capacity-solver.log'),(CAP/'response-audit/worker-stats.json','worker-stats.json'),(STRIP/'plan.json','short-strip-plan.json'),(STRIP/'result.json','closed-short-strip-result.json'),(STRIP/'variants.json','short-strip-fixed-variants.json'),(ROOT/'output/h5-paired-strip-clearance-main-sync-20261026/receipt.json','previous-main-push-receipt.json')]:shutil.copyfile(p,OUT/name)
write(OUT/'main-ci-cb7f7b1f-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,'upstream_state_reference':'benchmarks/results/h5-paired-strip-clearance-capacity-20261026/source-review.json','upstream_rechecked_this_seal':False,'main_ci':40359411459,'main_ci_status':ci['status'],'main_ci_successful_jobs':sum(j['conclusion']=='success' for j in ci['jobs']),'main_ci_all_six_passed':ci_pass,'next_push_queued_until_all_six_pass':not ci_pass,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
next_action='The clipped occupancy call is CLOSED UNKNOWN and the144 finite short-strip queries are CLOSED without a candidate. Do not repeat, reseed or extend either. Keep all34 paired-strip first-sheet originals and all15 short originals as an optional source-checked core; all15 cogs and both inserts remain mandatory for any full layout. The1045 clipped cell hulls retain all source floor-rounded centers and certify139 new conflicts, but the necessary model still relaxes away both inserts and original cog angles. A useful next materially changed formulation must jointly include the two inserts with the cog geometry and rebuild exact current-owner coupling, or move the frame/bracket core. Do not continue merely strengthening an unchanged search clock. The attempted six-bracket/six-insert/cog short strip supplied no13-part candidate; its saved empty conservative regions are not an independent impossibility proof. Preserve the existing short12/partial64 and short15 alternatives exactly. Full66 source/native/material validation, production60-second integration and the completeH5 matrix remain required. Wait for all six checks on maincb7f7b1f before any next push. H2 retains the original gate and22 reserved vectors stay unopened; no new release qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'fixed_first_originals':34,'fixed_short_originals':15,'mandatory_first_movers':{'cog':15,'insert':2},'all66_required':True,'prior66_whole_cell_exclusions_preserved':True,'clipped_cells':1045,'new_pair_conflicts':139,'cell_model_status':'UNKNOWN','fixed34_neighborhood_excluded':False,'attempted_short_counts':{'bracket':6,'insert':6,'cog':1},'short_candidate_found':False,'finite_source_query_only':True,'independent_negative_short_geometry_proof':False,'source_short_query_helper_recomputed':False,'full66_target_witness':False,'H5_complete':False})
members={};inputs={}
for folder in [CAP,STRIP]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
helpers=list((ROOT/'output').glob('*h5_paired_strip_clipped*.py'))+list((ROOT/'output').glob('*h5_six_insert_cog_short_sheet.py'))+[ROOT/'output/prepare_h5_clipped_capacity_tools.py',ROOT/'output/prepare_h5_paired_strip_capacity_model.py',ROOT/'output/run_h5_paired_strip_capacity_model.py',ROOT/'output/audit_h5_paired_strip_clearance_response.py',ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p
    for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members)
checks={'passed':True,'audits_passed':4,'failed_checker_attempts':0,'integer_partition_atoms':1313,'hull_corner_checks':4268,'full_cell_pair_checks':545490,'full_vertex_pair_checks':8782205,'additional_conflicts':139,'total_conflicts':112596,'cliques':1746,'model_variables':1045,'model_constraints':1747,'solver_calls':1,'status':'UNKNOWN','returned_solve_seconds':response['returned_solve_seconds'],'shared_process_seconds':response['shared_process_seconds'],'returned_soft_overrun_seconds':response['returned_soft_overrun_seconds'],'short_fixed_pair_checks':264,'short_stock_edge_checks':192,'closed_short_queries':144,'short_candidate_found':False,'independent_negative_short_geometry_proof':False,'full66_target_witness':False,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text='All six checks pass, allowing a normal checkpoint push after staging and ancestry verification.' if ci_pass else f"{review['main_ci_successful_jobs']} of six jobs pass; the run is {ci['status']}. Queue this checkpoint until all six pass, preserving the running checks."
report=f'''# H5: clipped cell capacity and a different short-strip allocation — 2026-10-26

**Exact clipping proves 139 additional conflicts between cog regions, but the
stronger necessary model still closes UNKNOWN.** A separate attempt to place
another insert beside the short-sheet cog finds no candidate in its declared
finite queries. Neither result closes H5. H2/H5 remain open at 60%.

## Exact occupancy footprints

The preceding model retained each whole cell unless a single proof excluded it
entirely. This model instead subtracts every certified oblique-support and
required-clearance support box from each surviving integer cell. It preserves
the prior 66 whole-cell exclusions and all potentially valid floor-rounded
centers, including integer endpoints. The 1,794 boxes change 93 nonempty cell
footprints; none becomes empty. The remaining 1,045 cells contain 1,067 lattice
rectangles. Their convex hulls are outer relaxations, not source poses.

Independent atomic partitioning checks **1,313 integer regions** and exact
retained/removed lattice counts. It verifies **4,268 corners** against their
convex hulls. For every cell pair, the farthest hull vertices bound the greatest
possible center separation. The audit checks **545,490 cell pairs and 8,782,205
vertex pairs**, proving **139 additional conflicts** while preserving every old
edge among retained cells. All **112,596 conflicts** are covered by **1,746
verified cliques**, with no residual edges.

Any original fifteen-cog layout must select fifteen distinct compatible cells:
each cell's diameter is below the certified 254.297 mm rounded separation, and
the new exclusions preserve every source-feasible center at every angle. The
two inserts remain mandatory for a full layout and are omitted only from this
necessary test. The model cannot establish source feasibility from a positive.

## Single closed model call

The complete **1,045-variable, 1,747-constraint** model is independently
reconstructed from the inventory and exact graph, without objectives or hints.
It closes **UNKNOWN** after actual search in **20.044475 returned-call seconds**
and **21.306630 shared-process seconds**. The internal solver time is
20.037539 seconds. Internal/returned soft overruns of 0.037539/0.044475 seconds
are preserved; the 30-second shared limit is honored. There is no retry,
reseed or extension. The returned worker records 12,561 branches and
378 conflicts; separate worker counters remain in the raw evidence. No
selection, source layout, neighborhood exclusion or formal unsat proof exists.

## Different short-sheet allocation

The known six-bracket/five-insert/cog short strip has one compact bracket pair.
The new construction widens that pair to hold an insert, then proposes three
more inserts in a stack at the right stock edge. A successful cog placement
would make **six brackets, six inserts and one cog**, moving insert38 from the
main sheet. Four stack variants use left/right alignment and vertical reflection.
The target stock height and all original quantities and clearances stay fixed.

Independent direct-vertex readback validates all twelve fixed originals in each
variant: **264 pair checks, 192 stock edges, 96 cutouts and 11,712 hole vertices**
across the four variants. Minimum gap is 0.225 mm and extra stock margin 0.025 mm.
The bracket/insert block retains the source-checked nine-part construction.

The finite proposal procedure queries 36 actual half-degree angles from 0 to
17.5 degrees against each of the four variants, with no exact rotational-symmetry
assumption. All **144 conservative free-translation regions are empty**, producing
no proposals or thirteen-part candidate in **36.235296 seconds**, within the
declared 60-second generation allowance. No solver is opened. The audit reads
back all saved queries and verifies their provenance; it does **not** independently
recompute the conservative region helper. These records show no candidate from
this procedure, not an independent impossibility proof or all-angle exclusion.

## Remaining work and repository state

All four audits pass. Both attempts are closed. A materially changed next model
should jointly include both remaining inserts with the cog geometry, or move the
frame/bracket core; these calls may not be resumed. Preserve the existing
short12/partial64 and short15 alternatives. Full66 original source/native/material
validation, production integration within 60 seconds and the complete H5 matrix
remain required.

At {review['utc']}, main is cb7f7b1f and its
[CI40359411459](https://github.com/skulitom/Nestbolt/actions/runs/40359411459)
is checked. {ci_text}
Production and READMEs remain unchanged. Upstream state is referenced to the
preceding recorded review; it was not rechecked during this seal. H2 retains
its original gate and all 22 reserved vectors remain untouched. No new release
is qualified.

[Checks]({NAME}/checks.json), [geometry]({NAME}/clipped-geometry-checks.json),
[necessity proof]({NAME}/clipped-necessity-proof.json),
[new edges]({NAME}/139-new-edge-certificates.json),
[model]({NAME}/clipped-model-checks.json),
[response]({NAME}/clipped-response-checks.json),
[short source/readback]({NAME}/short-source-readback-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 clipped capacity and short-strip allocation, 2026-10-26:** [the evidence]({link})
clips all certified forbidden integer points from the surviving cog cells.
Independent checks cover 1,313 atomic regions, 4,268 hull corners and all
545,490 cell pairs, proving 139 new conflicts. The stronger 1,045-variable,
1,747-constraint model closes UNKNOWN after search in 20.044475 returned/
21.306630 shared seconds; its 0.044475-second soft overrun is recorded.
A distinct six-bracket/six-insert/cog short-strip attempt checks four fixed
variants and144 finite translation queries, finding no candidate. Fixed source
geometry is independently validated; empty conservative query records are read
back, not promoted to an independent exclusion. Both attempts are closed.
All four audits pass. H2/H5 remain open at60%; production, READMEs, releases
and all22 reserved H2 vectors are unchanged. Preserve main's CI40359411459
and wait for all six checks before the next push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'audits_passed':4,'main_all_six_passed':ci_pass})
