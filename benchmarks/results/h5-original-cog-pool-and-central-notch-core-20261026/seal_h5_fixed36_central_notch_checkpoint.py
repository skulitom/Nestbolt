"""Seal the fixed36 finite source search and independently checked central-notch core."""
from pathlib import Path
import ast, json, re, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-original-cog-pool-and-central-notch-core-20261026'
OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
names={'screen':'h5-fixed36-cog-space-20261026','support':'h5-fixed36-support-domains-20261026','domains':'h5-fixed36-combined-domains-20261026','map':'h5-fixed36-space-inspection-20261026','pool':'h5-fixed36-source-cog-pool-20261026','selection':'h5-fixed36-source-selection-20261026','frames':'h5-central-notch-frame-core-20261026','notch':'h5-notch-four-brackets-20261026','mixed':'h5-central-notch-mixed-core-20261026','review':'h5-fixed36-central-notch-review-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()}
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==review['source_head']==review['main_head']=='07c17806fbef00d9911cb74c02354baf7d8f7d9d'
assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
assert review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6
audits=[('support','audit/checks.json'),('domains','audit/checks.json'),('pool','audit-segment-circles/checks.json'),('selection','model-audit/checks.json'),('selection','response-audit/checks.json'),('selection','original-readback/checks.json'),('frames','checks.json'),('notch','model-audit/checks.json'),('notch','response-audit/checks.json'),('mixed','checks.json'),('mixed','audit/checks.json')]
assert len(audits)==11 and all(load(base[k]/n)['passed'] for k,n in audits)
calls=[]
for k in ['selection','notch']:
    r=load(base[k]/'search/000/result.json');p=load(base[k]/'search/process.json');a=load(base[k]/'response-audit/checks.json')
    assert r['solver_calls']==1 and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and len(list((base[k]/'search').rglob('opened.json')))==1
    calls.append({'formulation':k,**r,'shared_seconds':p['seconds'],'scope':'Finite 4770-pose original cog pool only; all15 required for target.' if k=='selection' else 'Four-bracket positive-construction model only; 1-micrometre grid and axis component gap. Negative does not exclude unrestricted placements.'})
assert [r['status'] for r in calls]==['OPTIMAL','INFEASIBLE']
pool=load(base['pool']/'audit-segment-circles/checks.json');partial=load(base['selection']/'original-readback/checks.json');mixed=load(base['mixed']/'audit/checks.json')
assert pool['original_cog_candidates_verified']==4770 and pool['all_unordered_candidate_pairs_verified']==11374065
assert partial['originals_placed']==63 and partial['missing_original_cogs']==[63,64,65]
assert mixed['originals_verified']==39 and mixed['mandatory_moving_family_counts']=={'bracket':4,'insert':8,'cog':15}
failures=[]
for n in ['audit','audit-repaired']:
    p=base['pool']/n;f=load(p/'failure-review.json');assert not (p/'checks.json').exists() and not f['checks_json_emitted'];failures.append({'attempt':n,**f})
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('domains','audit/necessity-proof.json','fixed36-domain-proof.json'),('selection','original-readback/placements.json','fixed36-partial63-placements.json'),('selection','original-readback/missing-originals.json','fixed36-missing-originals.json'),('frames','notch-container.json','notch-container.json'),('mixed','placements.json','changed-core39-placements.json'),('mixed','anchors.json','mixed-core-anchors.json'),('mixed','audit/next-neighborhood.json','next-joint27-neighborhood.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-07c17806-success.json')]:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'closed-calls.json',calls);write(OUT/'preserved-failed-audits.json',failures)
next_action='Both solver calls are CLOSED. The finite4770 original-cog pose pool has optimum12, not an unrestricted15-cog exclusion. The four-bracket axis-gap notch construction is INFEASIBLE only within its declared1-micrometre-grid construction. Do not repeat, reseed or extend either call. Keep the earlier64-original partial and the alternative63-original fixed36/short15 partial. The independently audited changed central-notch core has24 first-sheet originals and15 unchanged short originals, with all27 remaining originals mandatory: brackets20/23/24/27, inserts42..49 and cogs51..65. Use next-joint27-neighborhood.json to build a fresh joint original-geometry candidate space. No previous36-fixed domain restriction, finite-pool optimum or old cog seed feasibility transfers. Retain every original, cutout, original stock target and PIH OFF. Any complete source-positive still needs independent66-original readback, native/material validation, production60-second integration and the complete H5 matrix. Main07c17806 CI40323092414 now passes all six checks; normal fast-forward checkpoint push is permitted after staged-byte and ancestry checks. H2 retains its original gate, all22 reserved vectors remain untouched, and no new release is qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'fixed36_finite_pool_optimum_cogs':12,'all15_cogs_required_for_target':True,'fixed36_unrestricted_exclusion_claimed':False,'four_bracket_notch_unrestricted_exclusion_claimed':False,'changed_core_first_originals':24,'changed_core_short_originals':15,'changed_core_total_originals':39,'mandatory_moving_originals':27,'mandatory_moving_family_counts':mixed['mandatory_moving_family_counts'],'old64_partial_preserved':True,'old_fixed36_partial63_preserved':True,'old_domains_or_pool_limits_transferred':False,'part_in_hole_used':False,'all66_originals_required':True,'full66_target_witness':False,'H5_complete':False})
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
for n in ['h5-full-circle-cog-spacing-and-fifteen-part-strip-20261026','h5-frame-compound-limits-20261023','h5-individual-frame-joint-20261023']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json'
    if p.exists():members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pattern in ['*h5_fixed36*.py','*h5_central_notch*.py','*h5_notch_four*.py'] for p in (ROOT/'output').glob(pattern)]+[ROOT/'output/h5_rational_geometry_helpers.py',ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)]
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
print({'archive_input_members':len(members)},flush=True)
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'audits_passed':11,'failed_audit_attempts_preserved':2,'closed_solver_calls':2,'all_shared_budgets_honored':True,'maximum_solver_soft_overrun_seconds':max(r['solver_soft_overshoot_seconds'] for r in calls),'original_cog_candidates':4770,'all_candidate_pairs_verified':11374065,'complete_conflicts_verified':3016663,'finite_pool_cog_optimum':12,'fixed36_partial_originals':63,'fixed36_missing_cogs':[63,64,65],'changed_core_originals':39,'changed_core_original_pair_checks':381,'changed_core_stock_edge_checks':156,'changed_core_cutouts_preserved':55,'changed_core_hole_vertices_preserved':4586,'mandatory_moving_originals':27,'mandatory_moving_family_counts':mixed['mandatory_moving_family_counts'],'all66_originals_required':True,'native_calls':0,'quality_runs':0,'main_ci_successful_jobs':6,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full66_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: original cog pool and central-notch frame core — 2026-10-26

The complete checked pool of 4,770 cog poses fits at most twelve cogs around
the previous 36 fixed first-sheet parts. All fifteen are still required.
That finite result motivates a changed frame arrangement: sixteen turned
frames followed by two wide frames at opposite stock edges. Its central opening
holds two brackets and four inserts. Independent source checks verify this
39-original core, including the unchanged fifteen-original short sheet.
The remaining four brackets, eight inserts and fifteen cogs are mandatory.
**H2/H5 remain open at 60%; no complete 66-original layout is claimed.**

## Complete domains and finite original cog pool

Rebuild coverage for the changed 36-owner neighborhood. The 48 source rectangles
have 192 inset world corners checked by 768 exact interval edge tests. Their
72 forbidden support boxes partition the center-stock root into 2,291 closed
cells. Retain 425 cells and remove only wholly certified forbidden cells.
A 1,981-node source-point disk refinement leaves 887 atomic rectangles, merged
into 178 domains with exact coverage and area checks. All twelve existing cog
seeds survive. Recompute capacities for fifteen required cogs using the proved
254.300 mm source separation and conservative 254.297 mm rounded separation.
All 3,625 incompatible domain pairs have separately verified capacity-one
endpoints. No coordinate solver is run on these domains.

The original-shape construction retains 3,438 compatible historical and seed
poses, then adds 1,332 new contact poses at eight declared angles. All eight
free-translation queries and proposal lists finish. Generation takes 7.221464
seconds; the complete graph and compression bring total construction time to
134.586215 seconds. The 120-second generation allowance applies to generation,
with a separate 15-second compression allowance. This is diagnostic work, not
evidence of meeting the production 60-second budget.

Two failed audit attempts remain preserved. The first opened its input manifest
before graph construction finished and exceeded its 120-second distance-audit
cap; it emitted no passing check. The second attempted an unnecessarily strong
infinite-edge-halfplane condition for the cog's inner disk, which fails because
the disk is inside the polygon but outside its convex kernel. It also emitted
no passing check. The corrected audit starts after all graph files are final
and uses exact distances to finite boundary segments, including endpoint cases.

For every candidate, the independent audit checks every original transformed
vertex, 36 fixed owners and four guarded stock edges. Exact integer winding and
finite-segment distances certify a 109.1 mm inner disk; original vertex bounds
certify a 140.01 mm outer disk. Integer center distances settle 2,040,174 near
and 8,282,043 far pairs; the remaining 1,051,848 pairs use original polygon
distances. **All 11,374,065 unordered pairs** reproduce the entire 3,016,663-edge
conflict graph. All 117,579 clique rows and 984,700 members preserve every edge.
The corrected audit passes in 26.107016 seconds. It does not change the earlier
independent full-circle cog-spacing proof, which already used finite segments.

## Two closed solver calls

Both calls use four workers, seed zero and a 20-second solver limit inside a
30-second shared process limit. Saved model fields, actual imports, parameters,
responses and timings pass their separate audits. Neither call is retried,
reseeded or extended.

| Model | Result | Solver seconds | Shared seconds | Valid scope |
|---|---|---:|---:|---|
| 4,770 original cog poses | OPTIMAL, twelve cogs | 16.919967 | 18.000306 | This finite pool only |
| Four brackets in the central opening | INFEASIBLE | 0.036713 | 0.741638 | Declared grid and axis-gap construction only |

The first model has 4,770 Boolean variables and 7,057 constraints. Full graph
equivalence, all residual implications and the twelve-cog hint are independently
verified. Its positive response satisfies every active constraint. Assigning
the selected poses to original cog identities gives 63 placed originals and
leaves cogs 63/64/65 missing. Source readback passes 1,233 same-sheet pairs,
252 stock edges and all 87 cutouts with 9,426 hole vertices. Minimum pair gap
is 0.212500 mm against 0.211708673 mm required. The finite optimum is not a
continuous or all-angle exclusion of the previous neighborhood.

The second model uses eight original quarter-turn/mirror bracket profiles,
each with two exact rectangular components. Its 148 variables and 135 constraints
require all four brackets within a 586.5 × 349.55 mm container, with 0.225 mm
axis separation between cross-original components. The one-micrometre grid and
axis-separation construction are sufficient conditions for a checked positive;
its negative does **not** exclude unrestricted placements in that opening.

## Changed source construction and remaining work

Sixteen turned 350 × 450 mm frames form four rows of four; two unturned
450 × 350 mm frames occupy opposite edges above them. Historical groups already
used this orientation count, so no first-ever orientation claim is made.
This particular central-opening arrangement is checked with the changed short
allocation. Place brackets 18/19 and inserts 38/39/40/41 in that opening.

Independent direct-vertex reconstruction verifies all eighteen frame anchors,
the six added anchors, all allowed transformations and the unchanged short-sheet
placements. It passes **381 same-sheet original pairs**, **156 stock edges**,
**55 cutouts** and **4,586 cutout vertices**. Minimum pair distance is 0.225 mm;
minimum extra stock margin is 0.025 mm. Filled outer polygons reserve cutouts,
so part-in-hole remains off.

The next inventory fixes 24 first-sheet originals and fifteen short-sheet
originals. Mandatory first-sheet movers are brackets 20/23/24/27, inserts 42–49
and cogs 51–65. All 66 original identities occur exactly once in this partition.
The 39-original core is a new search starting point, not an improvement over
the preserved 64-original partial. Old fixed-owner domains and the finite
twelve-cog limit do not transfer to this different geometry.

Next build a fresh joint original-geometry candidate space for all 27 movers.
A complete positive still needs independent source readback, full native and
material validation, production integration within 60 seconds and the full
H5 matrix. No native validator is called on these partial layouts.

## Repository and evidence

At {review['utc']}, local HEAD and main are 07c17806. All six checks in
[CI 40323092414](https://github.com/skulitom/Nestbolt/actions/runs/40323092414)
pass, permitting a normal checkpoint push after staged-byte and ancestry checks.
Production, README digests and upstream stop-rule state are unchanged. H2
retains its original gate; all 22 reserved vectors remain untouched. No new
release is qualified.

All **eleven audits pass**, with two earlier failed audit attempts retained.
[Checks]({NAME}/checks.json),
[closed calls]({NAME}/closed-calls.json),
[preserved failures]({NAME}/preserved-failed-audits.json),
[63-original partial]({NAME}/fixed36-partial63-placements.json),
[changed core]({NAME}/changed-core39-placements.json),
[next inventory]({NAME}/next-joint27-neighborhood.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']:,} canonical files and
{archive['verified_aliases']:,} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 original cog pool and central-notch core, 2026-10-26:** [the evidence]({link})
checks all 4,770 source cog poses and all 11,374,065 pair combinations in a fresh
36-fixed neighborhood. The sole selection call is OPTIMAL at twelve cogs;
this finite pool does not exclude unrestricted placements of the required fifteen.
The 63-original readback preserves all cutouts and leaves cogs 63/64/65 mandatory.
Two failed audits and their final finite-segment repair are preserved. A changed
frame arrangement creates a central opening holding two brackets and four inserts.
Its independently checked 39-original core fixes 24 first-sheet parts and the
unchanged fifteen short-sheet parts; all remaining four brackets, eight inserts
and fifteen cogs are mandatory movers. Checks pass 381 original pairs, 156 stock
edges and 55 cutouts/4,586 hole vertices. The separate four-bracket notch model
is INFEASIBLE only within its declared grid/axis-gap construction. Both calls
are closed; old domains and finite limits do not transfer to the changed core.
All eleven audits pass. The earlier 64-original partial is preserved. Main
07c17806 now passes all six checks, permitting a normal checkpoint push.
H2/H5 remain open at 60%; production, READMEs, releases and all 22 reserved H2
vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive},flush=True)
