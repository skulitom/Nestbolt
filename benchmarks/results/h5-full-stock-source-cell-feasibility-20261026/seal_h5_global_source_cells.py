"""Preserve the first full-stock source-cell feasibility call and its complete audits."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-full-stock-source-cell-feasibility-20261026';OUT=ROOT/'benchmarks/results'/NAME;GEO=ROOT/'output/h5-global-source-cells-20261026';MODEL=ROOT/'output/h5-global-source-cells-model-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-frame-blocks-source-cells-and-displacement-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0];assert head==main=='db4d23092464cb79fb2dcfb96e60f798f8cae8f8';assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40386947038','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and len(ci['jobs'])==6;success=sum(j['conclusion']=='success' for j in ci['jobs']);ready=ci['status']=='completed' and ci['conclusion']=='success' and success==6
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))};assert all(upstream[k]==previous[k] for k in upstream)
audits={'source-cells':GEO/'geometry-audit/checks.json','source-rectangles':GEO/'inner-rectangles/audit/checks.json','model':MODEL/'model-audit/checks.json','response':MODEL/'response-audit/checks.json'};assert all(load(p)['passed'] for p in audits.values());response=load(audits['response']);model=load(audits['model']);assert response['status']=='UNKNOWN' and response['closed'] and response['search_started'] and not response['has_assignment'] and model['entire_stock_domains_verified'] and model['all57_required'] and model['variables_verified']==38401 and model['constraints_verified']==138177
OUT.mkdir()
for n,p in audits.items():shutil.copyfile(p,OUT/(n+'-checks.json'))
for p,n in [(GEO/'prepared.json','prepared-source-cells.json'),(GEO/'domains.json','whole-stock-domains.json'),(GEO/'inner-rectangles/rectangles.json','source-contained-rectangles.json'),(GEO/'inner-rectangles/identical-source-groups.json','equivalent-source-copy-groups.json'),(MODEL/'built.json','model-summary.json'),(MODEL/'search/result.json','closed-result.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-db4d2309-snapshot.json',ci);receipt=load(ROOT/'output/h5-frame-block-main-sync-20261026/receipt.json');assert receipt['head']==head and receipt['previous_successful_jobs']==6 and receipt['remote_main_verified'];write(OUT/'previous-checkpoint-push.json',receipt)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40386947038,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,'push_qualified_now':ready,'previous_main_f2322ccd_ci':40381684665,'previous_main_ci_successful_jobs':6,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'all57_first_originals_required':True,'all9_short_originals_fixed':True,'coordinate_domains':'entire legal stock','local_displacement_bounds_removed':True,'source_modes_fixed':True,'conservative_cell_subset':True,'necessary_source_rectangle_constraints':True,'solver_status':'UNKNOWN','search_started':True,'no_assignment_returned':True,'no_exclusion_claimed':True,'native_calls':0,'quality_runs':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The full-stock38401-variable/138177-constraint call is CLOSED UNKNOWN after real search. Do not extend or reseed it. A materially different next algorithm can generate source constraints only when a proposed full57-part assignment violates them: begin with the114 full-stock coordinates,65 source-contained rectangles, NoOverlap2D, both necessary cumulative strip constraints and source-copy ordering. Keep the fixed9 short originals and all57 first originals mandatory. Use one declared60-second total search/90-second shared budget with at most6 rounds, a first-call cap of15 seconds and later caps of8 seconds. After each returned necessary-model assignment, inspect all1596 original source pairs and add the complete existing cell disjunction for every newly violating pair. Every subsequent solver model must contain new constraints; stop on UNKNOWN/INFEASIBLE or if no new valid cut exists, never repeat an unchanged model. Preserve each model/response/candidate and independently verify the final all66 original rings before any native call. This is a proposed different algorithm, not permission to resume the closed call. No complete source/native/material witness exists; integration, fullH5 matrix and release stay unqualified. Keep H2 original gate and22 reserved vectors unopened. Main db4d2309 CI40386947038 must finish all6 checks before the next normal push.','completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs={}
for folder in [GEO,MODEL,ROOT/'output/h5-frame-block-main-sync-20261026']:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=list((ROOT/'output').glob('*h5_global_source_cells*.py'))+list((ROOT/'output').glob('*h5_global_inner_rectangles*.py'))+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':4,'all57_first_originals_mandatory':True,'all9_short_originals_fixed':True,'whole_stock_domains_verified':114,'all_source_pairs_verified':1596,'source_cells_verified':38287,'integer_halfplanes_verified':136401,'source_geometry_samples':174688,'source_contained_rectangles_verified':65,'serialized_constraints_verified':138177,'solver_status':'UNKNOWN','search_started':True,'returned_branches':179798,'returned_conflicts':5060,'no_assignment_or_exclusion':True,'native_calls':0,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text=('All six checks pass; the next normal checkpoint push is qualified.' if ready else f'{success} of six checks pass; the remaining jobs are still live. Preserve CI40386947038 and wait for all six before the next push.')
report=f'''# H5: full-stock source-cell feasibility — 2026-10-26

**The new model removes every local movement limit, but its bounded search
returns UNKNOWN without a layout or an impossibility proof.** All 57 first-sheet
originals may use the entire legal stock; the verified nine-part short sheet is
retained. H2/H5 remain open at 60% by completed gate weights.

## Beyond the proved local obstruction

The preceding source certificate rules out the mixed candidate's five-part
configuration within 180 mm vertically. This experiment therefore discards
every local anchor bound. It keeps the original source modes and the checked
short-sheet allocation, but fixes no first-sheet position. An independent model
reader checks that all 114 coordinate bounds equal the full legal stock domains.
This is a different global-domain feasibility model, not a continuation of the
closed local solver or any source-sliding run.

All **1,596 first-sheet pair domains** are reconstructed. Their conservative
configuration-space complements yield **38,287 convex cells** and **136,401
exact integer halfplanes**. The same additional 0.002 mm obstacle expansion
precedes nearest-micrometre rounding; 456 rounded cells are discarded by the
conservative checks and no pair has an empty disjunction. Preparation takes
45.060182 seconds. The minimum retained cell distance to its already conservative
obstacle is 0.001355144 mm.

Independent geometry checking covers all cells, all pairs, 912 stock-edge corner
checks and **174,688 original-source clearance samples**. This takes 15.189268
seconds. The retained cells remain a sufficient subset: full-stock coordinate
bounds do not turn the rounded conservative representation into an exact
enumeration of every source layout. No exclusion is inferred from UNKNOWN.

## Source-based strip constraints

The model also uses **65 rectangles contained in the 57 source filled outlines**:
one inset outer rectangle for each frame and insert, two disjoint stem/foot
rectangles per bracket, and a 153 mm square about each cog's source-center
anchor. Each rectangle is inset in micrometres and independently checked against
the original transformed outer ring. Components of the same original remain
disjoint. Holes remain reserved under part-in-hole off.

These source-contained rectangles provide necessary NoOverlap2D constraints
and cumulative width/height limits across the usable stock. They strengthen
propagation without replacing any detailed source-pair constraint. Eight groups
of identical-source, identical-mode copies with equal stock domains add 47
nondecreasing-Y ordering constraints. No prior positions are supplied as hints.

The serialized model has **38,401 variables and 138,177 constraints**: 114
coordinates, 38,287 cell selectors, 1,596 exactly-one choices, 136,401 cell
halfplanes, 130 interval constraints, one NoOverlap2D, two cumulative constraints
and 47 source-copy ordering constraints. An independent reader reconstructs
every variable domain and serialized constraint, confirms whole-stock coverage,
all 57 mandatory first originals, and the absence of objectives and hints.

## One closed call

The sole 60-second search within 90 shared seconds returns **UNKNOWN** after
search begins. It records **179,798 branches and 5,060 conflicts** in the returned
response. Solver time is **60.078208 seconds**, returned solve time **60.089808
seconds**, and shared process time **61.906913 seconds**. The 0.078208/0.089808
second soft overruns are preserved. There is no assignment, native call or full
quality run. The search is CLOSED without retry, extension or reseeding.

Four independent audits pass. The next distinct hypothesis is constraint
generation: begin with the smaller necessary source-rectangle model, inspect
every pair in each returned candidate, and add complete source-cell disjunctions
only for newly violated pairs. Every original must stay mandatory, every later
solver model must contain new constraints, and total work must have a declared
bound. UNKNOWN or an unchanged model must stop that pipeline. No such run has
opened in this checkpoint, and no necessary-model candidate may be called a
valid source layout without full independent readback.

## Repository and evidence

All six checks on prior main f2322ccd passed, allowing the normal one-commit push
of db4d2309 at {receipt['utc']}. The push and remote main were verified. At
{review['utc']}, [db4d2309 checks](https://github.com/skulitom/Nestbolt/actions/runs/40386947038):
{ci_text}

Production, READMEs, upstream heads/releases and all 22 reserved H2 vectors
remain unchanged. No release is qualified. [Checks]({NAME}/checks.json),
[source geometry]({NAME}/source-cells-checks.json),
[source rectangles]({NAME}/source-rectangles-checks.json),
[model audit]({NAME}/model-checks.json), [response]({NAME}/response-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json) and
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 full-stock source feasibility, 2026-10-26:** [the evidence]({link})
removes every local movement bound and retains all 57 first originals plus the
verified short nine. All 1,596 source pairs yield 38,287 conservative free cells
and 136,401 exact integer halfplanes; independent checking covers 174,688 source
samples. Another 65 source-contained rectangles provide necessary non-overlap
and cumulative strip constraints. Every one of the 38,401 variables and 138,177
serialized constraints is checked, with whole-stock domains and no position
hints. The sole call closes UNKNOWN after search: 179,798 returned branches,
5,060 conflicts, 60.089808 returned/61.906913 shared seconds. Its soft overrun is
preserved; there is no assignment or exclusion. Four independent audits pass.
Prior main f2322ccd passed all six checks and checkpoint db4d2309 was pushed
normally. Preserve its live CI40386947038 before the next push. H2/H5 remain
open at 60%; no native/full-quality run or new release qualifies, and all 22
reserved H2 vectors remain unopened.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'independent_audits_passed':4,'main_ci_successful_jobs':success,'push_qualified_now':ready})
