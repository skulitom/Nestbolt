"""Preserve the compact mandatory model and a different original nine-insert core."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-compact-joint-model-and-nine-insert-core-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'geometry':'h5-compact-joint-geometry-20261026','model':'h5-compact-joint-model-20261026','core':'h5-central-nine-insert-core-20261026','review':'h5-compact-joint-nine-core-review-20261026'};base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==review['source_head']==review['main_head']=='32282158178d201e95c4c3defa028e06579e7bec';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('geometry','audit/checks.json'),('model','model-audit/checks.json'),('model','response-audit/checks.json'),('core','checks.json'),('core','audit/checks.json')];assert all(load(base[k]/n)['passed'] for k,n in audits)
response=load(base['model']/'response-audit/checks.json');r=load(base['model']/'search/000/result.json');proc=load(base['model']/'search/process.json');assert response['status']=='UNKNOWN' and not response['stopped_after_presolve'] and response['solver_branches']==288549 and r['solver_calls']==1 and proc['exit_code']==0 and not proc['timeout'] and proc['seconds']<=90 and len(list((base['model']/'search').rglob('opened.json')))==1
core=load(base['core']/'audit/checks.json');assert core['originals_verified']==42 and core['remaining_first_filled_area_reduction_mm2']==19000 and core['mandatory_remaining_counts']=={'bracket':6,'insert':3,'cog':15}
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('geometry','audit/necessity-proof.json','moving-component-necessity-proof.json'),('model','model-audit/necessity-proof.json','complete-model-necessity-proof.json'),('model','search/000/result.json','closed-call-result.json'),('model','search/process.json','closed-call-process.json'),('model','search/000/solver.log','closed-call-solver.log'),('core','placements.json','changed-core42-placements.json'),('core','anchors.json','central-insert-anchors.json'),('core','audit/next-neighborhood.json','next-fixed27-neighborhood.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-32282158-observed.json')]:shutil.copyfile(base[k]/n,OUT/d)
next_action='The complete compact fixed24/short15 joint model is CLOSED UNKNOWN after288549 branches; no source positive or neighborhood exclusion is claimed. Do not retry, reseed or extend it or the prior finite graph call. Its geometry proof covers every allowed non-cog quarter turn/mirror and every continuous translation after conservative flooring, with all27 movers explicit. A changed source construction puts nine inserts38..46 in the central opening, preserving all18 frame poses and15 short originals. It increases notch filled content from159200 to178200mm2 and reduces remaining first-sheet filled demand by19000mm2. This42-original core is not an improvement over the retained64-original partial. Next use next-fixed27-neighborhood.json:27 fixed first originals,15 fixed short originals, and all24 mandatory movers(six brackets18/19/20/23/24/27,three inserts47/48/49,all15 cogs51..65). Rebuild every source domain/owner transform for this changed obstacle set; no old fixed24 domain, unknown-model conclusion or cog seed feasibility transfers. Prefer a declared original-cog phase/contact construction coupled to every remaining non-cog, or a materially different independently audited necessary formulation, over variants of either closed fixed24 call. Source component certificates may be reused only for unchanged original geometry and allowed modes; current fixed geometry must be reverified. Full66 original source angles, native/material checks, production60-second integration and fullH5 matrix remain. Main32282158 CI40336537934 has four successful jobs at the source review and is still running; queue the evidence checkpoint until all six pass, then normal fast-forward push with ancestry checks. H2 retains its original gate;22 reserved vectors untouched; no new release qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'closed_compact_status':'UNKNOWN','fixed24_short15_excluded':False,'all_previous27_movers_required':True,'new_fixed_first_originals':27,'new_fixed_short_originals':15,'new_core_originals':42,'new_mandatory_moving_counts':{'bracket':6,'insert':3,'cog':15},'remaining_first_filled_area_reduction_mm2':19000,'old64_partial_preserved':True,'old_fixed24_domains_transferred':False,'part_in_hole_used':False,'all66_originals_required':True,'full66_target_witness':False,'H5_complete':False})
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
for n in ['h5-joint-source-graph-and-compact-domains-20261026','h5-original-cog-pool-and-central-notch-core-20261026','h5-full-circle-cog-spacing-and-fifteen-part-strip-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pattern in ['*h5_compact_joint*.py','*h5_central_nine_insert*.py'] for p in (ROOT/'output').glob(pattern)]+[ROOT/'output/h5_rational_geometry_helpers.py',ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)]
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
write(OUT/'checks.json',{'passed':True,'checks_passed':5,'source_geometry_profiles_verified':12,'fractional_anchor_corner_checks':112,'exact_component_edge_tests':448,'model_variables_verified':6658,'model_constraints_verified':8244,'old_mandatory_noncogs':12,'old_mandatory_cogs':15,'closed_solver_calls':1,'status':'UNKNOWN','solver_branches':288549,'solver_conflicts':12571,'stopped_after_presolve':False,'solver_reported_wall_seconds':response['solver_reported_wall_seconds'],'returned_solve_call_seconds':response['returned_solve_call_seconds'],'shared_process_seconds':response['shared_process_seconds'],'shared_budget_honored':True,'reported_soft_overrun_seconds':response['reported_soft_overrun_seconds'],'returned_call_soft_overrun_seconds':response['returned_call_soft_overrun_seconds'],'new_core_originals':42,'new_fixed_first_originals':27,'new_fixed_short_originals':15,'new_mandatory_moving_counts':core['mandatory_remaining_counts'],'new_original_pair_checks':456,'new_stock_edge_checks':168,'new_cutouts_preserved':54,'new_cutout_vertices_preserved':4464,'remaining_first_filled_area_reduction_mm2':19000,'main_ci_pending_at_review':True,'production_and_readmes_unchanged':True,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'full66_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: compact joint geometry and a nine-insert central core — 2026-10-26

**The complete compact model retains all twelve moving non-cogs and fifteen
cogs, covers every allowed non-cog orientation and continuous anchor, and leaves
cog angles unrestricted. Its sole call explores 288,549 branches but ends
UNKNOWN. There is no source layout or neighborhood exclusion.** A different
source construction puts nine inserts into the central opening, reducing the
remaining first-sheet filled demand by 19,000 mm². Its 42-original subassembly
passes independent original-geometry checks. All remaining six brackets, three
inserts and fifteen cogs stay mandatory. H2/H5 remain open at 60%.

## Necessary geometry for every original placement

Decompose the original orthogonal filled outers at their vertex coordinates:
three rectangles per bracket and one per insert. Enumerate all eight bracket
quarter-turn/mirror profiles and all four insert quarter turns. Exact grid
coverage and filled area are checked independently.

For an arbitrary continuous source placement, floor the translated ideal outer
minimum to integer micrometres. The fractional anchor is in [0,1)² micrometres.
Exact rational trigonometric intervals prove every corner of each model component,
inset by four micrometres, strictly inside its true source component throughout
the larger closed [0,1]² box. The audit covers **28 profile components, 112
corners and 448 exact edge tests**. Convexity contains each complete inner box.
The verified coordinate error is below 0.000001 mm, so the 20-micrometre outward
stock relaxation safely covers both that error and flooring.

The model includes all twenty moving component boxes and 28 independently
certified fixed boxes in a global two-dimensional nonoverlap constraint. All
fifteen cog centers choose from the complete 38-domain map. Exact occupancies
retain every checked capacity and cross-domain conflict. All 105 cog pairs
must lie outside a verified 32-sided polygon strictly inside the forbidden
254.297 mm rounded-separation disk.

Every cog/moving-component pair avoids both necessary support-exclusion
rectangles. The original inner disk and support tips establish those exclusions
for every cog angle. A two-micrometre inset accounts for floor-rounded centers.
Each of the **600 support-box exclusions** chooses one outside direction.
All twelve non-cog mode tables, continuous anchors and 27 original identities
remain in the model. Clearance is deliberately omitted only in this necessary
relaxation; original guards remain required for any eventual source solution.

## One closed complete-model call

An independent audit reconstructs all **6,658 variable roles**, **8,244
constraints**, every mapping field and the actual solver import/export. It
checks every profile table, stock row, component coordinate and size, interval,
nonoverlap box, domain choice, occupancy, symmetry row and pair exclusion.
The largest absolute linear activity bound is 314,621,244,000, below the checked
integer arithmetic limit. There is no objective, hint, fixed cog angle or
omitted mover.

The sole call uses four workers, seed zero and a 60-second soft solver limit
inside a 90-second shared process limit. It reports **UNKNOWN** after **288,549
branches** and **12,571 conflicts**. It progresses beyond presolve but returns
no solution. Internal solver time is **60.065567 seconds**, returned-call time
**60.068638 seconds**, and shared-process time **60.876190 seconds**. Both small
soft overruns are recorded; the shared limit is honored. This is diagnostic
evidence, not proof of meeting the production 60-second requirement.

The saved model, parameters, response, log and timing scopes pass their audit.
This call and the earlier finite graph call are **closed**: no retry, reseed or
extension. UNKNOWN does not exclude the fixed 24-original neighborhood, and
neither call provides a complete original layout.

## Different opening contents: nine original inserts

Keep all eighteen frame poses and all fifteen short-sheet originals unchanged.
Put inserts 38–46 in three rows of three at the center opening, using 0.225 mm
gaps. The first insert begins at (456.75, 1807.65) mm; column spacing is
180.225 mm and row spacing is 110.225 mm.

The former opening held two brackets and four inserts, occupying 159,200 mm²
of filled area. Nine inserts occupy 178,200 mm². The remaining first-sheet
filled demand falls by exactly **19,000 mm²**. This changes the remaining mix
and the cog obstacles; it does not itself prove a material improvement for a
complete layout.

Construction and independent direct-vertex readback verify **42 originals**,
**456 same-sheet filled-outer pairs**, **168 stock edges**, **54 cutouts** and
**4,464 cutout vertices**. Minimum pair distance is 0.225 mm against
0.211708673 mm required, with 0.025 mm minimum extra stock margin. Every frame
and short-sheet transform is unchanged. Part-in-hole remains off.

The next inventory fixes 27 first-sheet originals and fifteen short-sheet
originals. All **24 movers** are explicit: brackets 18/19/20/23/24/27, inserts
47/48/49 and cogs 51–65. This is an alternative starting core, not an improvement
over the retained 64-original partial. No old fixed-24 domain, unknown result
or cog-seed feasibility transfers to the changed arrangement.

Rebuild current geometry before any next search. Prefer a declared original-cog
phase/contact construction coupled to all nine remaining non-cogs, or a
materially different independently audited formulation. Actual source angles,
all 66 original/native/material checks, production integration within the
original budget and the complete H5 matrix remain required.

## Repository and evidence

At {review['utc']}, local HEAD and main are 32282158. Four jobs in
[CI 40336537934](https://github.com/skulitom/Nestbolt/actions/runs/40336537934)
have passed, with checks still running. Queue this checkpoint until all six
pass so the push does not cancel the active run. Production and README digests
and upstream stop-rule state are unchanged. H2 retains its original gate and
all 22 reserved vectors remain untouched. No new release is qualified.

The geometry audit, model audit, response audit, source construction and
independent original readback all pass.
[Checks]({NAME}/checks.json),
[component necessity]({NAME}/moving-component-necessity-proof.json),
[complete model necessity]({NAME}/complete-model-necessity-proof.json),
[closed result]({NAME}/closed-call-result.json),
[changed core]({NAME}/changed-core42-placements.json),
[next inventory]({NAME}/next-fixed27-neighborhood.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']:,} canonical files and
{archive['verified_aliases']:,} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 compact joint model and nine-insert core, 2026-10-26:** [the evidence]({link})
proves necessary inner-component geometry for every allowed quarter turn/mirror
and continuous non-cog anchor, using 112 corners and 448 exact edge tests.
All twelve non-cogs and fifteen cogs remain mandatory in the audited 6,658-variable,
8,244-constraint model. Its sole call explores 288,549 branches and closes UNKNOWN
in 60.068638 returned-call / 60.876190 shared seconds, with soft overruns recorded.
No source witness or neighborhood exclusion is claimed. A different checked core
puts nine inserts in the central opening, reducing remaining first-sheet filled
demand by 19,000 mm². Its 42 originals pass 456 pair checks, 168 stock edges and
54 cutouts/4,464 hole vertices. All six remaining brackets, three inserts and
fifteen cogs stay mandatory; rebuild domains for the new 27-fixed first sheet.
The prior 64-original partial is preserved. Main 32282158 CI is still running
at review, so the next push is queued until all six checks pass. H2/H5 remain
open at 60%; production, READMEs, releases and all 22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
