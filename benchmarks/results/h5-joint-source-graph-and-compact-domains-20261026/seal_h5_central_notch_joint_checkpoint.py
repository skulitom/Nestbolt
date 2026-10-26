"""Preserve the complete finite joint search and rebuilt geometric domains without claiming completion."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-joint-source-graph-and-compact-domains-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'pool':'h5-central-notch-joint-pool-20261026','failed-graph':'h5-central-notch-joint-graph-20261026','graph':'h5-central-notch-joint-graph-recovered-20261026','selection':'h5-central-notch-joint-selection-20261026','inventory':'h5-fixed24-joint-neighborhood-20261026','screen':'h5-fixed24-joint-cog-space-20261026','support':'h5-fixed24-joint-support-domains-20261026','failed-domains':'h5-fixed24-joint-combined-domains-20261026','domains':'h5-fixed24-joint-combined-domains-repaired-20261026','initial-review':'h5-central-notch-joint-review-20261026','review':'h5-central-notch-joint-final-review-20261026'}
base={k:ROOT/'output'/v for k,v in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==review['source_head']==review['main_head']=='4e1549adddd0e1f399265a5301140a685718146e';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items());assert review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6
audits=[('graph','audit/checks.json'),('graph','reduced/checks.json'),('selection','model-audit/checks.json'),('selection','response-audit-timing-repaired/checks.json'),('inventory','checks.json'),('support','audit/checks.json'),('domains','audit/checks.json')];assert len(audits)==7 and all(load(base[k]/n)['passed'] for k,n in audits)
response=load(base['selection']/'response-audit-timing-repaired/checks.json');assert response['status']=='UNKNOWN' and response['stopped_after_presolve'] and response['solver_branches']==0
result=load(base['selection']/'search/000/result.json');proc=load(base['selection']/'search/process.json');assert result['solver_calls']==1 and proc['exit_code']==0 and not proc['timeout'] and proc['seconds']<=90 and len(list((base['selection']/'search').rglob('opened.json')))==1
graph=load(base['graph']/'audit/checks.json');red=load(base['graph']/'reduced/checks.json');domains=load(base['domains']/'audit/checks.json');assert graph['all_unordered_candidate_pairs_verified']==199990000 and domains['merged_domains_verified']==38
failures=[('graph','failed-graph','failure-review.json'),('response-timing','selection','response-audit/failure-review.json'),('domain-owners','failed-domains','failure-review.json')]
assert not(base['failed-graph']/'result.json').exists() and not(base['selection']/'response-audit/checks.json').exists() and not(base['failed-domains']/'result.json').exists()
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('pool','result.json','pool-result.json'),('graph','result.json','graph-recovery-result.json'),('selection','search/000/result.json','closed-call-result.json'),('selection','search/process.json','closed-call-process.json'),('selection','search/000/solver.log','closed-call-solver.log'),('inventory','next-neighborhood.json','next-joint-neighborhood.json'),('support','audit/necessity-proof.json','fixed24-support-proof.json'),('domains','audit/necessity-proof.json','fixed24-domain-proof.json'),('domains','merged-domain-rectangles.json','complete-cog-center-domains.json'),('domains','audit/cell-capacities.json','cog-domain-capacities.json'),('domains','audit/incompatible-presence-pairs.json','cog-domain-presence-conflicts.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-4e1549ad-success.json')]:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'preserved-failures.json',[{'attempt':kind,**load(base[k]/n)} for kind,k,n in failures])
next_action='The sole finite joint solver is CLOSED UNKNOWN after presolve with zero branches. Do not repeat, reseed or extend it. Its20000 original candidates, complete30557608-edge graph,4835 certified substitutions, exact4-bracket/8-insert/15-cog model, imported protobuf and clocks remain preserved. No positive or finite/unrestricted exclusion is claimed. Next use a compact necessary geometric model for the same24 fixed first originals,15 fixed short originals and all27 mandatory movers. Fresh exact cog-center coverage now has38 domains, source separation254300/rounded254297 and309 unit-capacity cross-domain conflicts. Every current fixed owner transform and used source-point disk is verified; old world circles were rejected and rebuilt. The12 moving non-cogs must enter the joint formulation explicitly: their allowed quarter-turn/mirror source components and pair exclusions must cover all original continuous anchors under conservative rounding. Couple them to all15 free-angle cogs with independently audited support/rectangle necessities, while preserving every original and PIH OFF. Do not treat a necessary-model positive as source placements. Full66 source angles, original/native/material validation, production60-second integration and fullH5 matrix remain required. Prior64 and alternative63 partials remain preserved. Main4e1549ad CI40330371817 passes all six checks, allowing a normal checkpoint push after staged bytes and ancestry checks. H2 retains its original gate, all22 reserved vectors are untouched, and no new release is qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'all27_movers_mandatory':True,'mandatory_counts':{'bracket':4,'insert':8,'cog':15},'fixed_first_originals':24,'fixed_short_originals':15,'finite_pool_candidates':20000,'closed_solver_status':'UNKNOWN','stopped_after_presolve':True,'solver_branches':0,'no_positive_or_exclusion':True,'source_cog_center_domains':38,'moving_noncogs_omitted_only_from_necessary_preprocessing':12,'moving_noncogs_required_in_joint_model':12,'old_world_circle_transforms_reused':False,'old64_partial_preserved':True,'alternative63_partial_preserved':True,'part_in_hole_used':False,'full66_target_witness':False,'H5_complete':False})
members={};inputs={}
for folder in base.values():
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for field in ['inputs','input_hashes','additional_inputs']:
            for n,h in load(p).get(field,{}).items():
                if n in inputs:assert inputs[n]==h,n
                inputs[n]=h
for n,h in inputs.items():
    p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
for n in ['h5-original-cog-pool-and-central-notch-core-20261026','h5-full-circle-cog-spacing-and-fifteen-part-strip-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pattern in ['*h5_central_notch*joint*.py','*h5_central_notch*recovered*.py','*h5_central_notch*timing*.py','*h5_fixed24*.py'] for p in (ROOT/'output').glob(pattern)]+[ROOT/'output/audit_h5_central_notch_joint_graph.py',ROOT/'output/recover_h5_central_notch_joint_graph.py',ROOT/'output/h5_rational_geometry_helpers.py',ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)]
seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p;s=p.read_text(encoding='utf-8')
    for n in re.findall(r"['\"](?:output/)?([A-Za-z0-9_.-]+\.py)['\"]",s):
        q=ROOT/'output'/n
        if q.is_file():helpers.append(q)
    for node in ast.walk(ast.parse(s)):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
print({'archive_input_members':len(members)},flush=True);archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'audits_passed':7,'failed_attempts_preserved':3,'original_candidate_poses':20000,'original_pair_combinations_verified':199990000,'original_conflicts_verified':30557608,'certified_substitutions':4835,'remaining_candidate_variables':15165,'closed_solver_calls':1,'closed_solver_status':'UNKNOWN','stopped_after_presolve':True,'solver_branches':0,'solver_reported_wall_seconds':response['solver_reported_wall_seconds'],'returned_solve_call_seconds':response['solver_seconds'],'shared_process_seconds':response['shared_seconds'],'shared_budget_honored':True,'reported_solver_soft_overrun_seconds':response['solver_reported_soft_overrun_seconds'],'returned_call_soft_overrun_seconds':response['soft_overrun_seconds'],'reduction_soft_overrun_seconds':max(0,red['reduction_seconds']-30),'compression_soft_overrun_seconds':max(0,red['compression_seconds']-20),'complete_cog_center_domains':38,'mandatory_moving_noncogs':12,'mandatory_moving_cogs':15,'all66_originals_required':True,'native_calls':0,'quality_runs':0,'main_ci_successful_jobs':6,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full66_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: complete joint source graph and compact geometric domains — 2026-10-26

**The new joint source model requires all four remaining brackets, eight inserts
and fifteen cogs. Its single bounded call ends UNKNOWN during presolve, with
zero branches. It provides neither a complete layout nor an exclusion.**
The next formulation will use continuous geometric constraints around the same
verified frame arrangement. Fresh exact coverage reduces cog-center choices
to 38 conservative regions. All twelve moving non-cogs remain mandatory in
that joint formulation. H2/H5 remain open at 60%.

## Complete original-shape pool and graph

The fixed core has 24 first-sheet originals and fifteen unchanged short-sheet
originals. The fresh pool contains 20,000 poses: 8,336 cogs, 6,294 inserts and
5,370 brackets. It adds 3,960 staggered cog-lattice poses and retains 16,040
compatible historical poses. Generation takes 8.179028 seconds. Its 20,000-pose
cap is reached before boundary proposals are added: all seventeen translation
regions were built, but their seventeen proposal lists and 2,621 remaining
historical proposals stay explicitly pending. No continuous or all-angle pool
completeness is claimed.

The first graph builder reaches its declared 300-second cap after writing
10,494 complete adjacency rows. Its failure, inputs and partial graph remain.
A separate recovery preserves those row bytes exactly and computes only the
remaining 9,506 rows in 96.192462 seconds, using conservative boxes and proposed
contained disks to avoid unnecessary polygon distances. None of these proposed
pruning conditions is accepted without the independent audit.

That audit directly reconstructs all 20,000 original polygons, their provenance
and allowed transformations, **480,000 fixed-original pairs** and **80,000 stock
edges**. Exact integer winding and finite-segment distances verify 724,276
contained-disk edge conditions. Outward boxes use exact rational rounding.
Across **199,990,000 unordered pairs**, the audit proves 162,698,057 separated
boxes and 13,638,680 overlapping contained-disk pairs, then evaluates 23,653,263
remaining original polygon distances. Every saved graph row and its symmetry
pass. The full graph has **30,557,608 conflicts**. Minimum fixed-owner distance
is 0.212600 mm against 0.211708673 mm required. The audit takes 140.004232 seconds.

## Lossless reduction and one mandatory-count call

A candidate may be replaced only by a retained pose of the same family that
conflicts with it and has no additional conflict with any other original pose.
This preserves independent sets and exact family counts. The bounded reduction
removes 4,835 candidates, checks 11,103,634 source-neighbor memberships and retains
15,165 candidates with 20,301,732 induced conflicts. The 30-second reduction ends
after 30.000054 seconds; the 20-second compression ends after 20.020937 seconds.
Both small soft overruns are recorded. All unprocessed candidates and every
residual edge remain.

The model has 632 verified cliques, 15,083 conditional conflict rows and three
exact quantity constraints: four brackets, eight inserts, fifteen cogs. It has
15,165 Boolean variables and 15,718 constraints, with no relaxed quantity or
objective. A separate audit rechecks every substitution, the exact induced graph,
all model fields and the solver's actual import/export.

The sole call uses four workers, seed zero, a 60-second soft solver limit and
a 90-second shared process limit. Its status is **UNKNOWN**. The saved log says
it stopped after presolve; there are zero branches and no solution values.
The internal solver timer reports **60.515847 seconds**, the returned call takes
**61.015893 seconds**, and the shared process takes **63.909778 seconds**.
Both solver soft-limit overruns are disclosed; the shared limit is honored.
This diagnostic does not demonstrate the production 60-second requirement.

The first response audit incorrectly required two different clock scopes to
differ by less than 0.2 seconds. It failed and remains preserved. The repaired
audit verifies the internal timer against the saved log, checks chronological
ordering through the returned call and shared process, and records the actual
0.500046-second return overhead. It keeps the original limits and response;
the solver is never rerun. This call is closed: no retry, reseed or extension.

## Fresh geometry for the next joint model

All 27 moving identities remain explicit: brackets 20/23/24/27, inserts 42–49,
and cogs 51–65. Together with 24 fixed first originals and fifteen fixed short
originals they account for all 66 exactly once. The previous 64-original partial
and alternative 63-original partial remain preserved.

Rebuild cog-center coverage around only the 24 fixed originals. The source
support proof checks 28 contained rectangles, 112 corners and 448 exact interval
edge tests. Its 56 forbidden boxes partition the stock root into 2,025 closed
cells, retaining 180 cells with all boundaries covered.

The initial disk refinement rejects an assumption that these frame transforms
match the old arrangement. Its guard fails before any stale world circle is
used. The corrected construction reprojects all 5,476 local source points with
the current owner transformations. Independent exact membership and trigonometric
bounds verify every one of the 26 used disks. A 628-node refinement retains
273 atomic cells and merges them into **38 complete domains**. Exact containment,
area and single-use membership verify every merge. The allowed bounding box is
[145.750, 2212.844, 1354.250, 2854.250] mm; its area is 703,889.492759 mm².
Every capacity and all 309 cross-domain conflicts are rederived from the proved
254.300 mm source / 254.297 mm rounded cog-center separation. All conflict
endpoints have independently checked capacity one.

These domains deliberately ignore the twelve moving non-cogs during necessary
preprocessing. They do not permit omitting those parts from the actual joint
model. Next represent every allowed quarter-turn/mirror non-cog component and
every continuous anchor under conservative rounding, then couple those components
to all fifteen free-angle cogs with audited necessary geometric constraints.
A positive relaxation still needs actual source angles, all 66 original/native
and material checks, production integration and the complete H5 matrix.

## Repository and evidence

At {review['utc']}, local HEAD and main are 4e1549ad, and
[CI 40330371817](https://github.com/skulitom/Nestbolt/actions/runs/40330371817)
passes all six checks. Production and README digests and upstream stop-rule state
are unchanged. H2 retains its original gate; all 22 reserved vectors remain
untouched. No new release is qualified.

All **seven audits pass**, with three failed attempts preserved.
[Checks]({NAME}/checks.json), [closed call]({NAME}/closed-call-result.json),
[timing audit]({NAME}/selection-response-audit-timing-repaired-checks.json),
[preserved failures]({NAME}/preserved-failures.json),
[complete domains]({NAME}/complete-cog-center-domains.json),
[next inventory]({NAME}/next-joint-neighborhood.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']:,} canonical files and
{archive['verified_aliases']:,} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 joint source graph and compact domains, 2026-10-26:** [the evidence]({link})
independently verifies 20,000 original poses, all 199,990,000 candidate pairs and
30,557,608 conflicts around the changed 24-original first-sheet core. Certified
substitutions retain exact feasibility with 15,165 poses. The sole model requires
all four remaining brackets, eight inserts and fifteen cogs; it closes UNKNOWN
after presolve with zero branches. Internal solver / returned-call / shared
times are 60.515847 / 61.015893 / 63.909778 seconds. Soft overruns and the failed
clock-scope assertion are preserved; no retry or exclusion is claimed. Fresh
exact cog-center coverage has 38 domains, with all twelve moving non-cogs still
required in the next joint geometric model. Old world-circle coordinates were
rejected and reprojected through current owners before independent verification.
All seven audits pass, with three failed attempts preserved. Main 4e1549ad now
passes all six checks, permitting a normal checkpoint push. H2/H5 remain open
at 60%; production, READMEs, releases and all 22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
