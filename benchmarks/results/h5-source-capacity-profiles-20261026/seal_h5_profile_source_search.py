"""Preserve exact source-capacity profiles and the closed staged necessary search."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-source-capacity-profiles-20261026';OUT=ROOT/'benchmarks/results'/NAME
GEO=ROOT/'output/h5-strip-capacity-profiles-20261026';SEARCH=ROOT/'output/h5-profile-source-cuts-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-cog-source-strips-and-timing-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head==main=='ff5036af94ff497284da7eae31a623cb98088695'
assert source_digest()==previous['production_digest']
assert {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40393931732','--json','databaseId,status,conclusion,headSha,jobs,url']))
assert ci['headSha']==main and len(ci['jobs'])==6
success=sum(j['conclusion']=='success' for j in ci['jobs'])
ready=ci['status']=='completed' and ci['conclusion']=='success' and success==6
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
    'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
    'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
    'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
profile=load(GEO/'audit/checks.json');response=load(SEARCH/'result-audit/checks.json')
assert profile['passed'] and response['passed'] and response['status']=='UNKNOWN' and response['closed']
assert response['source_candidates_returned']==0 and response['source_pair_cuts_added']==0
assert response['variables_verified']==114 and response['constraints_verified']==1400
assert response['fj_worker_excluded_verified'] and response['algorithm_60_second_budget_met'] and response['shared_90_second_budget_met']
OUT.mkdir()
for p,n in [(GEO/'audit/checks.json','profile-checks.json'),(GEO/'prepared.json','profile-summary.json'),
            (GEO/'profiles.json','source-profiles.json'),(SEARCH/'checks.json','initial-model-checks.json'),
            (SEARCH/'result-audit/checks.json','response-checks.json'),(SEARCH/'search/result.json','closed-result.json')]:shutil.copyfile(p,OUT/n)
receipt=load(ROOT/'output/h5-cog-strip-main-sync-20261026/receipt.json')
assert receipt['head']==main and receipt['pushed_commits']==3 and receipt['previous_successful_jobs']==6 and receipt['remote_main_verified']
write(OUT/'previous-checkpoint-push.json',receipt);write(OUT/'main-ci-ff5036af-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,
    'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],
    'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,
    'main_ci':40393931732,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,
    'push_qualified_now':ready,'previous_ci':40386947038,'previous_ci_successful_jobs':6,
    'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,
    'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'all57_first_originals_required':True,'all9_short_originals_fixed':True,
    'whole_stock_coordinates':True,'fixed_source_modes':True,'first_originals_fixed':0,
    'exact_781_rectangle_strip_capacities_retained':True,'additional_781_rectangle_nonoverlap_removed':True,
    'initial_detailed_source_cuts':0,'new_detailed_source_cuts':0,'source_candidates_returned':0,
    'solver_status':'UNKNOWN','unrestricted_exclusion':False,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The profile pipeline is CLOSED UNKNOWN after its first30-second call; do not extend, repeat or reseed it. Exact source-strip capacity profiles are verified and remain reusable. No infeasibility of this allocation or any source layout is established. All recent models retain a fixed9-part short sheet and fixed source modes. A materially different next investigation should permit the short-sheet composition to vary across the previously proved surviving count frontier, while retaining every one of66 originals and the actual target sheet height. Inspect the existing allocation/frontier evidence and derive an allocation-aware necessary capacity model before opening any new solver; verify every source footprint/orientation used, preserve the fixed-mode results and both older64-source partials, and use full original-ring readback before native validation. The fj worker was explicitly excluded in this closed call; any future search needs its own declared timing boundary and no unchanged retry. H2 remains unchanged and22 reserved vectors stay unopened. Main ff5036af CI40393931732 must pass all6 checks before the next normal push. No new release qualifies.',
    'completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs={}
for folder in [GEO,SEARCH,ROOT/'output/h5-cog-strip-main-sync-20261026']:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=[ROOT/'output'/n for n in ['prepare_h5_strip_capacity_profiles.py','audit_h5_strip_capacity_profiles.py',
    'h5_profile_source_model.py','h5_profile_source_model_audit.py','prepare_h5_profile_source_search.py',
    'h5_profile_source_round.py','run_h5_profile_source_search.py','audit_h5_profile_source_search.py',
    'ccd1.py','pack_h5_evidence_archive.py']];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p
    for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else
              [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'profile_audit_passed':True,'serialized_model_and_response_audit_passed':True,
    'original_axis_profiles_verified':114,'exact_integer_profile_slabs_verified':2315,
    'model_profile_intervals_verified':1218,'variables_verified':114,'constraints_verified':1400,
    'closed_status':'UNKNOWN','source_candidates':0,'new_source_cuts':0,'fj_worker_excluded_verified':True,
    'solver_soft_overrun_seconds':response['solver_soft_overrun_seconds'],'algorithm_budget_met':True,
    'shared_budget_met':True,'native_calls':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text=('All six checks pass; the next normal push is qualified.' if ready else
         f'{success} of six checks pass. Preserve the remaining live checks before the next push.')
report=f'''# H5: exact source capacity profiles — 2026-10-26

**The smaller staged model preserves the source-strip capacity information,
but returns UNKNOWN without a candidate.** Its first and only solve returns in
30.043256 seconds; the pipeline closes after 32.950780 shared seconds. H2/H5
remain open at 60% by completed gate weights.

## Exact capacity with fewer intervals

The previous geometry audit verified 781 disjoint source-contained rectangles,
including 728 cog strips. Their cumulative height and width demands can be
represented independently of the expensive additional 781-rectangle NoOverlap2D.
For every original and axis, the preparation sweeps all integer rectangle
endpoints, sums perpendicular demand and merges adjacent equal-demand slabs.

The resulting piecewise profiles contain 1,498 X intervals and 437 Y intervals.
Splitting overlapping X intervals increases that representation's size, so the
model retains the original 781 X intervals and uses the compact 437 Y profile
intervals: **1,218 instead of 1,562 projection intervals**. Both representations
measure exactly the same occupied source-strip capacity for arbitrary whole-part
translations. They do not replace two-dimensional collision checking.

An independent reader checks all 114 original/axis profiles through **2,315
integer event slabs**, with direct active-rectangle summation rather than the
producer's sweep. It also checks all 114 integrated source areas and interval
merging. The source rings and strip containment are unchanged.

## A different staged model

The new initial model has **114 whole-stock coordinates and 1,400 constraints**.
It keeps the older 65-rectangle non-overlap, its two cumulative constraints and
47 equivalent-copy orders, then adds the 1,218 exact strip intervals and two
capacity constraints. All 57 first-sheet originals remain mandatory, together
with the verified short nine. Ninety non-cog hints fix no coordinate.

The additional global strip non-overlap and all initial detailed source-cell
selectors are absent. After a returned candidate, the pipeline would inspect
all 66 original rings and add complete cell disjunctions for every newly failing
first-sheet pair. Each later round must change the constraints. The declared
limits are four rounds, 30 seconds for the first solve and eight for later
solves, all within 60 algorithm/90 shared seconds. UNKNOWN stops immediately.

An independent protobuf reader checks every initial and round-zero constraint,
both profile representations, all hints and unchanged whole-stock domains. The
model SHA-256 is `8bc5e5e3bfb19b669821c12ade47c31e7ad621857041e76e0916781e487076f6`.

## Closed result and timing

Only round zero runs. It returns **UNKNOWN**, with **155,233 branches and
22,875 conflicts**, no assignment, no source candidate and no new source cut.
The `fj` worker that overran the previous different model is explicitly excluded;
the serialized parameters and log confirm this, with `fs_random_no_lp` as the
first-solution worker. This does not establish a universal timing guarantee.

Solver time is **30.041647 seconds**, returned solve **30.043256**, algorithm
**32.720068** and shared process **32.950780**. The 0.041647/0.043256 second soft
overruns are recorded. The total algorithm and process boundaries are met. The
call remains CLOSED without extension, reseeding or unchanged-model retry.

The profile audit and complete serialized-model/response audit pass. No native
validation, full quality run, source-fit claim or unrestricted exclusion occurs.
The next distinct investigation can vary the short-sheet allocation across the
already proved surviving count frontier, instead of preserving the same fixed
nine-part short sheet and fixed source modes. That investigation has not opened
a search here and must keep every original and the target material boundary.

## Repository and evidence

The preceding three checkpoints were pushed normally as ff5036af at
{receipt['utc']}, after all six db4d2309 checks passed; remote main was verified.
At {review['utc']}, [ff5036af checks](https://github.com/skulitom/Nestbolt/actions/runs/40393931732):
{ci_text} Production, READMEs and upstream heads/releases remain unchanged.
All 22 reserved H2 vectors are unopened, and no new release is qualified.

[Checks]({NAME}/checks.json), [profile audit]({NAME}/profile-checks.json),
[initial model]({NAME}/initial-model-checks.json), [response]({NAME}/response-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json) and
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 exact source capacity profiles, 2026-10-26:** [the evidence]({link})
verifies all 114 original/axis profiles on 2,315 integer slabs and preserves both
781-rectangle source-strip capacities using 1,218 projection intervals. A different
staged model has 114 whole-stock coordinates/1,400 constraints, 90 non-cog hints,
no first part fixed, and no initial source-cell selectors or additional global
strip non-overlap. Its only round closes UNKNOWN: 155,233 branches, 22,875 conflicts,
30.043256 returned/32.950780 shared seconds, no candidate or new source cut.
Small soft overruns remain recorded; the 60/90-second total boundaries are met.
The previously overlong fj worker is explicitly excluded. Profile and complete
model/response audits pass without a full-source claim. All prior three
checkpoints were pushed normally as ff5036af after six successful main checks;
preserve its live CI 40393931732 before the next push. H2/H5 remain open at 60%;
no native/full-quality run or release qualifies, and all 22 reserved H2 vectors
remain unopened.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'main_ci_successful_jobs':success,'push_qualified_now':ready})
