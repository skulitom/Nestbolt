"""Preserve full-circle cog spacing, all closed calls and the new fifteen-part strip."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-full-circle-cog-spacing-and-fifteen-part-strip-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={
 'support':'h5-fixed40-support-domains-20261026','combined':'h5-fixed40-combined-domains-20261026',
 'coordinates':'h5-fixed40-fourteen-cog-model-20261026','occupancy':'h5-fixed40-capacity-projection-20261026',
 'unions':'h5-fixed40-union-capacities-20261026','union-projection':'h5-fixed40-union-projection-20261026',
 'union-coordinates':'h5-fixed40-union-coordinate-model-20261026','rotation-screen':'h5-cog-pair-rotation-screen-20261026',
 'rotation-proof':'h5-cog-pair-rotation-certificate-20261026','strong-domains':'h5-fixed40-strong-domains-20261026',
 'strong-unions':'h5-fixed40-strong-union-capacities-20261026','strong-coordinates':'h5-fixed40-strong-coordinate-model-20261026',
 'linear-geometry':'h5-fixed40-linear-distance-geometry-20261026','linear-coordinates':'h5-fixed40-linear-distance-model-20261026',
 'short':'h5-nine-insert-short-sheet-20261026','next':'h5-fixed36-cog-neighborhood-20261026',
 'initial-review':'h5-fixed40-review-20261026','review':'h5-fixed40-final-review-20261026'}
base={k:ROOT/'output'/v for k,v in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==review['source_head']==review['main_head']=='5ab344f5819ba4daa7c9e335cfb31f097e44eac1';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('support','audit/checks.json'),('combined','audit/checks.json'),('unions','audit/checks.json'),('rotation-proof','audit/checks.json'),('strong-domains','audit/checks.json'),('strong-unions','audit/checks.json'),('short','checks.json'),('short','audit/checks.json'),('next','checks.json')]
callkeys=['coordinates','occupancy','union-projection','union-coordinates','strong-coordinates','linear-coordinates']
for key in callkeys:audits.extend([(key,'model-audit/checks.json'),(key,'response-audit/checks.json')])
assert len(audits)==21 and all(load(base[k]/n)['passed'] for k,n in audits);calls=[]
for k in callkeys:
    r=load(base[k]/'search/000/result.json');p=load(base[k]/'search/process.json');assert r['solver_calls']==1 and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and len(list((base[k]/'search').rglob('opened.json')))==1;calls.append({'formulation':k,**r,'shared_seconds':p['seconds']})
assert [r['status'] for r in calls]==['UNKNOWN','OPTIMAL','OPTIMAL','UNKNOWN','UNKNOWN','UNKNOWN'];proof=load(base['rotation-proof']/'audit/checks.json');assert proof['original_all_angle_center_separation_units1000']==254300 and proof['ordered_phase_pairs_verified']==518400;short=load(base['short']/'audit/checks.json');assert short['originals_verified']==63 and short['short_originals_verified']==15 and short['mandatory_first_sheet_additions']==[63,64,65]
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('rotation-proof','audit/necessity-proof.json','all-angle-cog-spacing-proof.json'),('combined','audit/necessity-proof.json','complete-fixed40-domain-proof.json'),('unions','audit/necessity-proof.json','domain-union-capacity-proof.json'),('strong-domains','audit/necessity-proof.json','strong-domain-proof.json'),('linear-coordinates','model-audit/necessity-proof.json','linear-distance-model-proof.json'),('short','partial63-placements.json','partial63-placements.json'),('short','short-sheet-placements.json','original-short-fifteen.json'),('short','short-sheet-anchors.json','short-sheet-anchors.json'),('next','next-neighborhood.json','next-fixed36-neighborhood.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-5ab344f5-pending.json')]:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'closed-calls.json',calls)
next_action='All six solver calls in this checkpoint are CLOSED: four complete-coordinate formulations UNKNOWN, two occupancy projections OPTIMAL with counts only. None excludes the fixed40/short12 neighborhood and none may be retried, reseeded or extended. The independent full-circle cog proof establishes source center separation254300 micrometres at all original rotations; relative flooring conservatively yields254297. It may be reused only for this exact original cog geometry after hash checks. A distinct original short sheet now fits15 non-cogs: six brackets21/22/25/26/28/29 and nine inserts30/31/32/33/34/35/36/37/50. The previous short cog65 returns to first-sheet obligations; four first inserts30/31/33/50 move to short, freeing29137.28106202mm2 net first filled area. Keep the old64-original partial as well as this63-original changed allocation. New first48/short15 checks pass, with cogs63/64/65 mandatory. Next use h5-fixed36-cog-neighborhood-20261026/next-neighborhood.json:36 fixed first non-cogs, all15 moving first cogs and15 fixed short originals. Rebuild complete source-support/disk coverage and recheck all12 existing cog seeds. Recompute every individual/union capacity and conflict at254297 and with15 mandatory cogs; do not inherit40-fixed domain restrictions or the old14-count cap. Prefer original-cog contact construction or a materially different independently audited spatial decomposition over more variants of the closed coordinate model. Any positive still requires actual source angles, all66 native/material validation, production60-second integration and the full H5 matrix. Main5ab344f5 CI40317475504 had five successful jobs and Windows checks running at the final review; queue this evidence commit until all six pass, then normal fast-forward push with ancestry checks. H2 stays open under the original gate;22 reserved vectors untouched; no new release qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'old_fixed40_neighborhood_excluded':False,'closed_complete_coordinate_calls':4,'complete_coordinate_terminal_statuses':['UNKNOWN']*4,'closed_occupancy_only_positive_calls':2,'universal_original_cog_center_distance_mm':254.3,'new_short_originals':15,'new_short_family_counts':{'bracket':6,'insert':9},'new_first_originals_placed':48,'new_originals_placed':63,'previous_partial64_preserved':True,'mandatory_first_cogs_unplaced':[63,64,65],'new_fixed_first_noncogs':36,'new_moving_first_cogs':15,'old_domain_restrictions_transferred':False,'part_in_hole_used':False,'all66_originals_required':True,'full66_target_witness':False,'H5_complete':False})
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
for n in ['h5-fourteen-cog-exclusion-and-twelve-part-strip-20261026','h5-exact-cog-coverage-and-two-insert-strip-20261026','h5-complete-composition-selection-and-support-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pattern in ['*h5_fixed40*.py','*h5_fixed36*.py','*h5_nine_insert*.py','*h5_cog_pair_rotation*.py'] for p in (ROOT/'output').glob(pattern)]+[ROOT/'output/audit_h5_occupancy_projection_response.py',ROOT/'output/h5_rational_geometry_helpers.py',ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
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
write(OUT/'checks.json',{'passed':True,'audits_passed':21,'closed_solver_calls':6,'complete_coordinate_unknown_calls':4,'occupancy_only_positive_calls':2,'all_shared_budgets_honored':True,'maximum_solver_soft_overrun_seconds':max(r['solver_soft_overshoot_seconds'] for r in calls),'full_circle_angle_cells':720,'robust_segment_certificates':28840,'exact_capsule_edge_checks':2307200,'ordered_phase_pairs_verified':518400,'original_cog_all_angle_spacing_mm':254.3,'strong_rounded_center_spacing_units1000':254297,'new_originals_placed':63,'new_short_originals':15,'original_pair_checks':1233,'stock_edge_checks':252,'cutouts_preserved':87,'cutout_vertices_preserved':9426,'remaining_first_cogs':[63,64,65],'next_fixed_first_noncogs':36,'next_mandatory_first_cogs':15,'all66_originals_required':True,'native_calls':0,'quality_runs':0,'main_ci_pending':True,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full66_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
rows='\n'.join(f"| {r['formulation']} | {r['status']} | {r['seconds']:.6f} | {r['shared_seconds']:.6f} |" for r in calls)
report=f'''# H5: full-circle cog spacing and a fifteen-part short sheet — 2026-10-26

**Every pair of the original cogs requires at least 254.3 mm between centers,
at arbitrary rotations. A complete independent exact audit establishes this
stronger bound. A changed short sheet fits fifteen originals: six brackets and
nine inserts. It frees a net 29,137.281062 mm² of first-sheet filled area, while
returning one cog to the first sheet. This changed partial places 63 originals
and leaves cogs63/64/65 mandatory. The previous 64-original partial is preserved.
H2/H5 remain open at 60%; no full66 target witness or exclusion is claimed.**

## Complete domains for the previous40-fixed neighborhood

Rebuild the source-support grid after removing inserts32/34/35 from the old43
owner set. All40 non-cog transforms are checked against the original placements.
The52 source rectangles have208 inset world corners, verified by832 exact
interval edge tests. Their77 forbidden support boxes partition the center-stock
root into3,060 closed cells. Retain579 cells; remove only wholly certified
forbidden cells. A2,211-node collision-disk refinement preserves every unresolved
boundary and leaves1,040 atomic rectangles. Exact containment, equal area and
single-use membership verify their185 merged domains. All43 used source-point
disks and all12 existing cog seed centers pass independent checks.

The initial247.441mm rounded-separation model has3,167 variables and9,476
constraints; its complete coordinate call is UNKNOWN. A distinct185-variable
occupancy projection returns counts only. Its apparent14-count allocation
violates630 independently derived whole-union capacity bounds, so it is not a
center witness. The2,791 union bounds follow from exact bounding boxes: if
transverse span t<D, integer longitudinal separation is at least
ceil(sqrt(D²-t²)), bounding the total count across the entire union. This remains
valid for cells with capacity above one. Separate countA+countB<=1 conflicts
are used only where both endpoints individually have capacity one.

The union-strengthened occupancy projection is positive, but the complete
coordinate-plus-union call remains UNKNOWN. Both results are preserved.

## Exact254.3mm separation at every original rotation

A floating screen over the full circle suggests a stronger tooth-aware bound;
the screen is not used as proof. The certificate covers all360degrees with
720 overlapping half-degree angle cells. No exact tooth symmetry is assumed.
For each needed phase and horizontal level, construct a candidate segment from
X0 toward the original cog boundary. Its endpoints are proposed by erosion,
rounded inward to micrometres and mapped back to a nanometre source grid.

The independent audit proves **28,840 complete segments** robust for every angle
in their respective cells. Exact integer intersection and segment-distance
checks establish a0.615mm capsule strictly inside the source outer polygon:
**2,307,200 capsule/edge checks**. Exact rational Taylor sine/cosine intervals
bound inverse endpoint rounding below0.000001mm. Every segment point has norm
at most140.001mm, and140.001×0.004364+0.000001<0.615. The capsule therefore covers
the entire inverse rotation variation within the cell, not just sampled angles.

Exact Machin arctangent series bounds certify pi and verify closed-cell coverage
of[0,2pi]. For all **518,400 ordered phase-cell pairs**, a common horizontal level
has rightA-leftB at least254.385mm. At any positive center distance below254.3mm,
the two certified horizontal segments overlap. Coincident centers intersect by
the independently proved inner disks. Rotating the whole scene aligns any
center displacement with positive X without restricting either cog angle.
Thus every nonintersecting original cog pair has center distance at least
**254.3mm**. A conservative3micrometre loss under relative coordinate flooring
gives the necessary integer bound **254297**.

Recompute every domain capacity and conflict from this new bound. The185
immutable geometric domains remain byte-identical, but all3,729 conflicts and
2,846 useful union capacities are independently derived afresh. The resulting
complete3,167-variable/12,409-constraint coordinate call is UNKNOWN.

A separate linear formulation replaces squared-distance operations with a
32-facet polygon strictly inside the forbidden distance disk. Every vertex
norm, supporting edge, strict convexity, variable and constraint is rebuilt
independently. All91 pairs must choose an outward facet; all domain and union
constraints remain. This necessary relaxation has5,715 variables and14,970
constraints. Its call is also UNKNOWN. A positive would still require checking
the full distance and actual source-cog angles.

## Six closed calls

Every call was separately declared and used four workers, seed zero and a
20-second solver limit inside a30-second shared process limit. All shared limits
were honored. The largest solver soft overrun was
{max(r['solver_soft_overshoot_seconds'] for r in calls):.6f}seconds; it is recorded.
Every saved model, actual import, parameter set, terminal response and timing
passes its audit. No call is retried, reseeded or extended.

| Formulation | Status | Solver seconds | Shared seconds |
|---|---|---:|---:|
{rows}

The two positives contain occupancies only. None of the four UNKNOWN results
excludes the40-fixed neighborhood, and no source-feasible14-cog positions were
produced. These distinctions remain explicit in the saved scope and next step.

## Fifteen originals on the unchanged short-sheet target

Widen all three bracket pairs and raise their upper-arm partners toY19mm.
Insert one180×110mm original between each pair's separate filled outers. Place
four110×180mm inserts side by side to the right, and two180×110mm inserts above
them. The six brackets are21/22/25/26/28/29; the nine inserts are
30/31/32/33/34/35/36/37/50. Part-in-hole remains disabled.

This moves four more inserts30/31/33/50 off the first sheet and returns short
cog65 to the first-sheet obligation. Four inserts occupy79,200mm², exceeding
the removed cog's50,062.718938mm² by29,137.281062mm². All48 remaining first-sheet
placements are unchanged. The new partial contains63 originals, with63/64/65
still mandatory cogs; this is an alternative allocation, not a complete layout
or an increase over the prior64 placed originals.

Construction and independent direct-vertex readback pass **1,233 same-sheet
filled-outer pair checks**, **252 stock edges**, **87 cutouts** and **9,426 hole
vertices**. Minimum pair distance is0.212500mm against0.211708673mm required;
extra stock margin remains0.012500mm. The short sheet reachesX1439.225mm and
Y319mm within the unchanged target. No native full-job validation is run on a
partial layout.

The next inventory accounts for every original exactly once: **36 fixed first
non-cogs** (18 frames, six brackets, twelve inserts), **15 mandatory first cogs**,
and **15 fixed short originals**. All12 previous first-cog poses remain available
as diagnostic seeds only. Rebuild full domains and recompute capacities for this
changed owner set and15-cog obligation. The newly proved254.3mm separation applies
to the same original cog geometry; old40-fixed domains and14-count caps do not.
Actual source angles, all66 native/material checks, production integration
within60seconds and the full H5 matrix remain required.

## Repository and evidence

At{review['utc']}, local HEAD and main are5ab344f5. Production and README digests
and upstream stop-rule state are unchanged. Main
[CI40317475504](https://github.com/skulitom/Nestbolt/actions/runs/40317475504)
has five successful jobs, with Windows checks still running. Queue this evidence
checkpoint until all six pass so a push does not cancel the active run.
H2 retains its original gate; all22 reserved vectors remain untouched. No new
release is qualified.

All **21 audits pass**. [Checks]({NAME}/checks.json),
[full-circle proof]({NAME}/all-angle-cog-spacing-proof.json),
[closed calls]({NAME}/closed-calls.json),
[original short fifteen]({NAME}/original-short-fifteen.json),
[partial63]({NAME}/partial63-placements.json),
[next inventory]({NAME}/next-fixed36-neighborhood.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']:,} canonical files and{archive['verified_aliases']:,}
aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 full-circle cog spacing and fifteen-part strip, 2026-10-26:** [the evidence]({link})
proves a254.3mm minimum original cog-center distance at every rotation, improving
the prior247.444mm bound. Independent exact checks cover720 angle cells,
28,840 robust horizontal segments,2,307,200 capsule/edge tests and all518,400
ordered angle-cell pairs without assuming rotational symmetry. Six separately
bounded calls are closed: four complete-coordinate formulations UNKNOWN and two
occupancy-only projections positive. No40-fixed exclusion or full target witness
is claimed. A changed short sheet fits six brackets and nine inserts, freeing
29,137.281062mm² net first-sheet area while returning cog65 to first obligations.
This alternative places63 originals and leaves cogs63/64/65 mandatory; the earlier
64-original partial is preserved. Independent checks pass1,233 pairs,252 stock
edges and87 cutouts/9,426 hole vertices. The next inventory has36 fixed first
non-cogs, all15 first cogs mandatory, and15 fixed short originals. Rebuild domains
and capacities for that changed allocation. All21 audits pass. Main5ab344f5 has
five successful jobs and Windows checks pending, so the next push is queued until
all six pass. H2/H5 remain open at60%; production, READMEs, release assets and
all22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
