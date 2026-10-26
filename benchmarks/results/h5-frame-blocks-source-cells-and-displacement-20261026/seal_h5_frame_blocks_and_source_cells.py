"""Archive coordinated frame searches, source-cell feasibility and a source width certificate."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-frame-blocks-source-cells-and-displacement-20261026';OUT=ROOT/'benchmarks/results'/NAME
MACRO=ROOT/'output/h5-frame-block-exchange-20261026';CELLS=ROOT/'output/h5-local-source-cells-20261026';MODEL=ROOT/'output/h5-local-source-cells-model-20261026';PROOF=ROOT/'output/h5-mixed-frame-displacement-proof-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-retained64-allocation-source-search-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0];assert head==main=='f2322ccd3b612d9d46bb77c065892ebc32294b65';assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40381684665','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and len(ci['jobs'])==6;success=sum(j['conclusion']=='success' for j in ci['jobs']);assert success>=5 and all(j['conclusion'] in ['',None,'success'] for j in ci['jobs']);ready=ci['status']=='completed' and ci['conclusion']=='success' and success==6
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))};assert all(upstream[k]==previous[k] for k in upstream)
audits={'frame-block-results':MACRO/'result-audit/checks.json','source-cell-geometry':CELLS/'geometry-audit-orientation-repaired/checks.json','source-cell-model':MODEL/'model-audit/checks.json','source-cell-response':MODEL/'response-audit/checks.json','source-width-certificate':PROOF/'audit/checks.json'};assert all(load(p)['passed'] for p in audits.values());mac=load(audits['frame-block-results']);cert=load(PROOF/'certificate.json');assert mac['patterns_verified']==4 and mac['actual_source_valid_patterns']==0 and cert['width_excess_um']==22990 and cert['vertical_radius_um']==180000
OUT.mkdir()
for n,p in audits.items():shutil.copyfile(p,OUT/(n+'-checks.json'))
for p,n in [(MACRO/'search/result.json','closed-block-search.json'),(CELLS/'prepared.json','source-cells.json'),(MODEL/'built.json','source-cell-model.json'),(PROOF/'certificate.json','source-width-certificate.json'),(PROOF/'rectangles.json','source-contained-rectangles.json'),(PROOF/'pair-overlap-proof.json','guaranteed-overlap-proof.json'),(CELLS/'geometry-audit/failure.json','preserved-distance-checker-failure.json'),(CELLS/'geometry-audit-distance-repaired/failure.json','preserved-distance-tolerance-checker-failure.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-f2322ccd-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40381684665,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,'push_qualified_now':ready,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'coordinated_frame_alternatives':4,'all66_source_identities_retained_each':True,'valid_full_results':0,'source_cell_model_status':'INFEASIBLE','cell_model_exclusion_is_finite_sufficient_subset_only':True,'independent_actual_source_certificate':True,'certificate_source_originals':[0,1,2,3,31],'certificate_vertical_radius_mm':180,'certificate_other61_originals_unconstrained':True,'certificate_horizontal_positions_unrestricted_within_stock':True,'certificate_fixed_source_modes_required':True,'whole_job_impossibility_claimed':False,'native_calls':0,'quality_runs':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'All four frame-block alternatives and the571-cell CP-SAT call are CLOSED. Do not retry, extend or reseed them. The independent source certificate proves that frames0..3 and insert original31 cannot all retain their current quarter-turn modes while staying within180mm vertically of the saved mixed candidate; their source-contained widths total1509.990mm versus1487mm stock. A next hypothesis must explicitly relocate side inserts or restructure frame rows beyond that obstruction, or change at least one of those five orientations. Simply expanding40mm to any radius<=180mm cannot repair this mixed candidate. The other61 originals and horizontal placement were not fixed in the proof; the whole job remains unresolved. Retain the checked9-part short sheet as an allocation option, both older64 partials, and all failures. No complete66 source/native/material witness qualifies integration, fullH5 matrix or release. Keep H2 original gate and22 reserved vectors untouched. Wait for all6 checks on main f2322ccd before a normal checkpoint push; do not cancel its live job.','completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs={}
for folder in [MACRO,CELLS,MODEL,PROOF]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=[]
for pattern in ['*h5_frame_block*.py','*h5_local_source_cells*.py','*h5_mixed_frame_displacement*.py']:helpers.extend((ROOT/'output').glob(pattern))
helpers.extend([ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py']);seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':5,'failed_checker_attempts_preserved':2,'coordinated_patterns_closed':4,'source_valid_patterns':0,'local_source_model_variables':685,'local_source_model_constraints':2212,'source_cells':571,'exact_integer_halfplanes':2056,'source_clearance_samples':9827,'solver_status':'INFEASIBLE','solver_closed_by_presolve':True,'source_width_certificate_originals':5,'exact_source_corner_edge_tests':80,'guaranteed_vertical_pairs':10,'vertical_displacement_neighborhood_excluded_mm':180,'width_excess_mm':22.99,'unrestricted_exclusion':False,'native_calls':0,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_sentence=('All six checks pass; a normal checkpoint push is qualified.' if ready else f'{success} of six checks pass; the Windows check is still running. Preserve that job and wait for all six before the next push.')
report=f'''# H5: coordinated frames, source cells and a displacement obstruction — 2026-10-26

**A source-geometry certificate explains why small translations cannot repair
the mixed-frame candidate.** Four frames and one insert require 1,509.990 mm of
cross-section width on 1,487 mm usable stock. At least one of those five originals
must change orientation or move vertically by more than 180 mm. The proof does
not exclude the whole job. No complete layout has passed; H2/H5 stay open at
60% by completed gate weights.

## Coordinated frame choices

Instead of extending a closed local run, a new compound search changes 12–18
frame orientations and their starting positions together. All57 first originals
can translate jointly; all9 verified short originals stay fixed. Four source-valid
frame constructions are assigned to original identities by minimum squared
center displacement. Their frame modes remain fixed within that alternative;
legal modes for the other39 originals may change. Every initial frame pattern
passes153 source pairs and72 stock edges. The other39 positions start from the
saved previous candidate, with no claim that the complete initial layouts fit.

Each alternative receives at most20 positive weight updates and12 seconds,
within one60-second search/90-second shared call. All four close ITERATION_LIMIT.
Total search time is23.804778 seconds; shared time is26.417979 seconds.

| Frame construction | Frames turned | Search seconds | Source pair failures | Stock failures |
| --- | ---: | ---: | ---: | ---: |
| 12 turned, 6 wide | 12 | 7.114317 | 72 | 20 |
| Central notch:16 turned,2 wide | 16 | 5.162431 | 96 | 26 |
| Three tall columns | 18 | 7.692661 | 84 | 14 |
| Four turned columns:5/5/4/4 | 18 | 3.727039 | 106 | 28 |

Each independent reader reconstructs all66 original identities,90 cutouts and
10,026 hole vertices, checks1,632 source pairs and264 stock edges, and replays
all20 positive weight updates. No original or constraint is removed. Lower
penalties are not valid part counts or material savings. No native call qualifies.

## Simultaneous source-clearance constraints

A different feasibility method fixes the mixed candidate's source modes and
allows every first anchor to move within40 mm, intersected with stock bounds.
All1,596 pair domains are examined. For1,440 pairs the whole relative-position
box is safe. The other156 pairs use **571 convex collision-free cells** and
**2,056 exact integer halfplanes** from original-source configuration obstacles.
An additional0.002 mm obstacle expansion precedes micrometre rounding;23 rounded
cells fail conservative checks and are discarded. The smallest retained cell
distance to the already conservative obstacle is0.001355144 mm.

Independent checking reconstructs all114 coordinate domains, every pair box,
every cell's exact integer halfplanes and9,827 original-source clearance samples.
Full native/source acceptance remains mandatory for any eventual assignment.
This is a finite sufficient subset, not an exact enumeration of every legal
source pose in the neighborhood.

The serialized model has **685 variables and2,212 constraints**, with all57
first originals mandatory, no overlap objective,114 position hints and156
exactly-one cell choices. A separate reader reconstructs every serialized
constraint. The one60/90-second call closes **INFEASIBLE in presolve**:
0.021436 solver /0.026760 returned /1.184046 shared seconds, zero returned branches
and conflicts. No assignment is returned. The finite-cell result alone does
not exclude the whole translation neighborhood or the job.

Two initial geometry readers failed on an auxiliary distance-equality check.
The saved distance was computed before a polygon's vertex order was reversed;
the equivalent reversed polygon differs by at most1.129565191382298e-14 mm in
the library's diagnostic reduction. Both failed readers are retained. The final
reader exactly reproduces the saved value using either vertex order, while
independently requiring source containment, strict disjointness and positive
distance. No physical tolerance, geometry or model cell is changed.

## Independent source proof: more than180 mm or an orientation change

This proof does not rely on the solver or the cell approximation. Originals0–3
are frames turned90°; original31 is a vertical insert. Exact quarter-turn source
geometry contains four349.998 mm-wide rectangles and one109.998 mm-wide rectangle.
An independent rational reader verifies all80 corner/edge inclusion tests.
Filled outer areas remain reserved, as required with part-in-hole off.

Enclose each saved binary64 vertical anchor outward in micrometres. Permit any
vertical movement up to **180 mm** and relax stock containment to these inner
rectangles alone. Exact interval bounds prove **all10 vertical interval pairs
must intersect**; the smallest guaranteed overlap margin is22 micrometres.
Pairwise-intersecting intervals on a line share a common point, so in every
permitted placement all five rectangles cross one common horizontal line.
Their disjoint horizontal intervals then require **1,509.990 mm**, exceeding
the stock's **1,487 mm** by **22.990 mm**, even with zero clearance.

Horizontal positions are unrestricted within stock and the other61 originals
are not fixed. Therefore a valid source layout must change at least one of
these five modes or move at least one vertically by more than180 mm from this
candidate. This excludes a real source neighborhood, not just the finite cells.
It does not exclude other modes, large rearrangements or the entire target job.
The next hypothesis must explicitly relocate side inserts or restructure frame
rows beyond this obstruction; widening40 mm to another radius at most180 mm
cannot repair this fixed-mode candidate.

## Repository and evidence

Five independent audits pass. All four frame alternatives and the cell-model
call are CLOSED, without retry or extension. No native call, full quality run
or release is qualified. Production, READMEs, upstream heads/releases and all22
reserved H2 vectors remain unchanged.

At {review['utc']}, [main f2322ccd checks](https://github.com/skulitom/Nestbolt/actions/runs/40381684665):
{ci_sentence}

[Checks]({NAME}/checks.json), [source certificate]({NAME}/source-width-certificate.json),
[rational source audit]({NAME}/source-width-certificate-checks.json),
[cell model audit]({NAME}/source-cell-model-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and{archive['verified_aliases']}
aliases by bytes,SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 coordinated frame blocks and source obstruction, 2026-10-26:** [the evidence]({link})
closes four joint frame-orientation alternatives; all66 source originals remain
mandatory, but each full result fails geometry. A separate685-variable model
uses571 verified source-clearance cells and2,056 exact integer halfplanes for
all57 first parts; its sole call closes INFEASIBLE in presolve in0.026760 returned/
1.184046 shared seconds, excluding only the finite sufficient cell subset.
An independent exact source certificate is stronger: four turned frames and one
vertical insert require1,509.990 mm of width versus1,487 mm stock. All10 vertical
interval pairs must intersect under any movement up to180 mm. At least one of
those five originals must change mode or move vertically more than180 mm;
horizontal positions and the other61 parts were not fixed. This is not a whole-job
exclusion. Five independent audits pass; two diagnostic-reader failures are
preserved and resolved without changing geometry or physical thresholds. H2/H5
remain open at60%; no native/full-quality run or release qualifies. Preserve
main f2322ccd's live checks and wait for all6 before the next push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'independent_audits_passed':5,'main_ci_successful_jobs':success,'push_qualified_now':ready})
