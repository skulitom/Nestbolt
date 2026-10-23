"""Seal new small-part contacts, the single bounded search and original quantity failures."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-shifted-core-small-joint-20261023';BASE=ROOT/'output'/NAME;REG=ROOT/'output/h5-shifted-core-small-contacts-20261023';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    data={k:load(root/path) for k,root,path in [('generation',REG,'result.json'),('geometry',REG,'audit/checks.json'),('graph',BASE,'result.json'),('audit',BASE,'audit/checks.json'),('provenance',BASE,'provenance-audit.json'),('reduction',BASE,'reduced/checks.json'),('hints',BASE,'hints/checks.json'),('encoding',BASE,'solve/encoding-audit.json'),('model',BASE,'solve/model-audit.json'),('solver',BASE,'solve/result.json'),('layouts',BASE,'layout-audit/checks.json'),('retention',BASE,'selection-summary.json'),('gaps',BASE,'final-gaps/checks.json')]}
    assert all(data[k]['passed'] for k in ['geometry','audit','provenance','reduction','hints','encoding','model','layouts','retention','gaps'])
    gen,geo,g,a,p,r,h,e,m,s,l,t,gaps=[data[k] for k in ['generation','geometry','graph','audit','provenance','reduction','hints','encoding','model','solver','layouts','retention','gaps']]
    assert s['status']=='FEASIBLE' and s['objective']==816200000 and s['best_bound']==895800000 and not l['full_target_witness'] and m['seed_score']==815800000 and not m['cp_model_presolve']
    assert s['counts']=={'frame':18,'cog':15,'bracket':11,'insert':19} and gaps['completed_queries']==gaps['empty_regions']==40
    nextstep={'full_target_witness':False,'action':'Investigate a fresh bounded neighborhood of coordinated small-part moves in the two new 63-part layouts. First measure which adjacent bracket/insert pairs, when temporarily released together, expose continuous original-outline placements for the missing inventory; choose release pairs from recorded geometry rather than resuming capped proposal lists. Preserve all fixed-part, stock and mutual conflicts and every pending query. Any later selection must retain the two original 64-part baseline mappings and both new 63-part mappings, use the original area floor 815800000, and keep the full 12-bracket/21-insert inventory with all 18 frames and 15 cogs. Declare genuinely new generation and selection bounds before execution; do not retry or extend this completed 60-second solve, resume 1950 deferred member lists, or infer impossibility from the unresolved full bound or conservative empty regions. All 66 parts, the original material target, native guard, original production budget and full 13-job/two-kerf matrix remain required.'};write(BASE/'next-step.json',nextstep)
    priorroot=ROOT/'benchmarks/results/h5-continuous-cog-joint-20261023';prior=load(priorroot/'source-review.json');assert source_digest()==prior['production_digest'] and {path:digest(ROOT/path) for path in prior['current_readmes']}==prior['current_readmes']
    previous=load(priorroot/'raw-manifest.json');hashes={v['path']:v['sha256'] for v in previous['files']+previous['aliases']};original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        path=original/name;assert digest(path)==hashes['source-inputs/'+path.relative_to(ROOT).as_posix()]
    OUT.mkdir()
    for k,v in data.items():write(OUT/(k+'.json'),v)
    for path,name in [(REG/'plan.json','generation-plan.json'),(REG/'audit/plan.json','geometry-plan.json'),(BASE/'plan.json','plan.json'),(BASE/'reduced/plan.json','reduction-plan.json'),(BASE/'final-gaps/plan.json','gap-plan.json'),(BASE/'next-step.json','next-step.json'),(BASE/'layout-comparison.png','layout-comparison.png')]:shutil.copyfile(path,OUT/name)
    for index,name in [('hint','baseline'),('final','new')]:
        for stem in ['layout','public']:shutil.copyfile(BASE/f'layout-audit/{stem}-{index}.json',OUT/f'{name}-{stem}.json')
    ci=json.loads(subprocess.check_output(['gh','run','view','39984899040','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs']);write(OUT/'main-ci-facf0f38.json',ci)
    current=json.loads(subprocess.check_output(['gh','run','view','39991641757','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert current['headSha']=='0526421ede59de232edbf2979362e9641e749ee6';write(OUT/'main-ci-0526421e.json',current)
    best=max(l['records'],key=lambda v:v['filled_area_mm2']);baseline=l['records'][0];assert abs(best['filled_area_mm2']-baseline['filled_area_mm2']-400)<1e-6
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'main_head':subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'highest_checked_part_count':64,'preserved_64_part_missing':{'bracket':2},'new_highest_filled_area_part_count':63,'new_highest_filled_area_missing':{'bracket':1,'insert':2},'filled_area_gain_mm2':400,'full_target_witness':False,'native_margin_qualified':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':nextstep['action']};write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [BASE,REG]:
        for path in root.rglob('*'):
            if path.is_file():members[root.name+'/'+path.relative_to(root).as_posix()]=path
        for path in root.rglob('*.json'):
            if path.name not in ['plan.json','model-audit.json']:continue
            value=load(path)
            for name,hsh in value.get('inputs',value.get('input_hashes',{})).items():
                if name in inputs:assert inputs[name]==hsh
                inputs[name]=hsh
    for name,hsh in inputs.items():
        path=ROOT/name;assert digest(path)==hsh;members['source-inputs/'+name.replace('\\','/')]=path
    for row in p['source_members_matching_committed_evidence']:
        for path,hsh in [(ROOT/row['source'],row['sha256']),(ROOT/row['manifest'],row['manifest_sha256'])]:assert digest(path)==hsh;members['source-inputs/'+path.relative_to(ROOT).as_posix()]=path
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-expanded-frame-joint-20261023',['mapping.json','layout-audit/layout-hint.json','layout-audit/public-hint.json','layout-audit/command-hint.json'])]:
        for name in names:
            path=ROOT/'output'/folder/name;members['source-inputs/'+path.relative_to(ROOT).as_posix()]=path
    helpers=['build_h5_shifted_core_small_contacts.py','audit_h5_shifted_core_small_contacts.py','build_h5_shifted_core_small_joint.py','audit_h5_shifted_core_small_joint.py','audit_h5_shifted_core_provenance.py','prepare_h5_shifted_core_small_selection.py','reduce_h5_shifted_core_small_joint.py','seed_h5_shifted_core_small_joint.py','solve_h5_shifted_core_small_joint.py','audit_h5_shifted_core_small_layouts.py','summarize_h5_shifted_core_small_joint.py','check_h5_shifted_core_final_gaps.py','plot_h5_shifted_core_small_joint.py','reduce_h5_one_cog_release_joint.py','seed_h5_one_cog_release_joint.py','solve_h5_one_cog_release_joint.py','audit_h5_one_cog_release_layouts.py','pack_h5_evidence_archive.py','ccd1.py'];pending=[ROOT/'output'/name for name in helpers];seen=set()
    while pending:
        path=pending.pop()
        if path in seen:continue
        seen.add(path);members['helpers/'+path.name]=path
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            modules=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for module in modules:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    checks={'passed':True,'all_original_inputs_match_previous_manifest':True,'all_input_hashes_verified':True,'reused_inputs_match_committed_evidence':True,'all_regions_events_caps_and_memberships_audited':True,'complete_graph_reconstructed_independently':True,'every_model_and_parameter_field_independently_reconstructed':True,'both_original_64_baselines_preserved':True,'all_returned_original_layouts_checked':True,'new_63_part_geometry_and_quantity_failures_preserved':True,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    links=', '.join(f"[part {i}]({NAME}/{v['path']})" for i,v in enumerate(manifest['archives'],1))
    report=f'''# H5: small-part contacts around changed cog arrangements — 2026-10-23

**The new highest-area layout has 63/66 parts: one bracket and two inserts
remain missing.** It places 11 brackets and 19 inserts, with all 18 frames and
15 cogs, and fills **400 mm² more** than the preserved 64-part layouts.
Those layouts still contain 10 brackets and all 21 inserts, missing two brackets.
The extra area is a different partial arrangement, not an inventory or H5 pass.
H2/H5 remain open at **60%** completed milestone weight.

![Original-outline comparison]({NAME}/layout-comparison.png)

## Fresh contacts and independent geometry

Two original baseline cores and five previously checked changed-cog cores give
seven distinct fixed 33-part arrangements, each with 18 frames and 15 cogs.
Every one of the 39,488 source pool records is preserved. Fourteen reused input
members match their committed manifests, including the compound catalogues,
core choices and verified explicit 128-sided clearance construction.

The generator processes 268 specifications: ten individual orientations,
36 small-part compounds at four quarter turns, and 114 already transformed
reflected compounds. Each specification visits every core and both sheets
before the next. All **3,752 queries** complete in **{gen['query_seconds']:.6f}
seconds** within the 120-second limit; 1,773 regions are empty. All 92 cached
obstacle first uses independently agree with direct global constructions.
The compound bounding box restricts only stock translations; exclusions use
each original member outline, and members remain independently selectable.

A separate 90-second proposal phase ends after **{gen['proposal_seconds']:.6f}
seconds** at the declared caps of 2,000 new brackets and 2,000 new inserts.
There are 16,408 recorded events: 4,000 additions and 12,408 exact duplicates.
All **1,950 deferred member lists** and their exact cursors are preserved;
none is resumed. Original generation checks cover 320,709 fixed-part pairs.
The 0.0126 mm construction padding applies to new contacts with fixed parts
and stock. It does not change internal compound gaps or existing core gaps
and does not establish native-margin qualification.

Independent verification takes **{geo['seconds']:.6f} seconds**. It checks
all 268 specifications, 456 independent whole-shape affine comparisons,
990 internal compound pairs, every saved region and proposal list, and the
entire event/deferred-list sequence. It reconstructs 1,074,147 distinct
fixed-part distances and all **211,995** old/new-to-core memberships using
both individual part distances and complete filled core unions. All 3,066
core pairs and both original 64-part baselines pass. Minimum new construction
padding is {geo['minimum_construction_clearance_padding_mm']:.12f} mm.

## Complete graph, certified reduction and one search

All **14,046** eligible choices enter a new complete geometric graph:
6,197 brackets and 7,849 inserts, including 10,046 old and 4,000 new poses.
The graph has **{g['geometric_conflicts']:,}** original-geometry conflicts;
there are no count-derived cog edges. Construction and serialization take
{g['seconds']:.6f} seconds. A separate sequential bounds scan considers
{a['same_sheet_possibilities']:,} same-sheet pairs and checks
{a['independent_exact_distances']:,} exact distances in {a['seconds']:.6f}
seconds. Every row agrees, and both 64-part baselines remain valid.

Fresh same-family substitutions require an adjacent retained replacement,
inclusion of all conflict neighbors and a superset of compatible cores.
They complete in **{r['seconds']:.6f} seconds** and {r['comparisons']:,}
comparisons, within 30 seconds and 50 million comparisons. Independent
certificates enumerate {r['certificate_neighbors_independently_verified']:,}
neighbor relationships and {r['compatible_group_memberships_independently_certified']:,}
core memberships. The result retains **{r['kept_candidates']:,}** choices.
The exact induced {r['induced_edges']:,}-edge graph compresses to
{r['compressed_cliques']:,} cliques in {r['compression_seconds']:.6f} seconds,
within 20 seconds. No residual edges remain; all edges reconstruct independently.
Both baseline mappings retain counts and area. There is no extra greedy search.

Retained choices include **1,246 new poses** (555 brackets and 691 inserts)
and 3,493 old poses. Of the 2,754 removed new choices, 2,054 have certified old
replacements and 700 have certified new replacements. Another 422 old choices
have certified new replacements. Every one of the seven cores still has
compatible retained new geometry; per-core counts are saved.

Every binary model and parameter field independently reconstructs. The model
contains **{m['variables']:,} variables** ({m['variable_poses']:,} pose choices
plus seven cores) and **{m['constraints']:,} constraints**, with exactly one
core and unchanged 12-bracket/21-insert caps. Its original variable-area floor
is 815,800,000 and full-inventory score 895,800,000. One eight-worker, seed-zero,
presolve-disabled call has a 60-second allowance. Actual wall time is
**{s['seconds']:.6f} seconds**; the soft overrun is preserved.

The baseline arrives at 0.120241 seconds and search starts at 0.16 seconds.
At 51.928128 seconds a second callback finds the new 63-part layout in core 3.
The distinct final layout has the same score **816,200,000**. Status is
`{s['status']}` and the full 895,800,000 bound remains unresolved. Worker logs
show active search, including 2,465,405 branches for the core worker.
The completed solve is neither repeated nor extended.

## Original layouts and fixed-layout gap diagnosis

All **{l['layouts_checked_including_hint']}** layouts—hint, both callbacks and
distinct final—pass original transforms, stock, material and every same-sheet
geometry pair. The 64-part layouts each check 1,521 pairs; the 63-part layouts
each check 1,467. Three fresh frozen-CLI calls and one exact-layout reuse report
only the original missing quantities. Every failed quantity result is retained.

New filled area is **{best['filled_area_mm2']:.9f} mm²**, versus
{baseline['filled_area_mm2']:.9f} mm² for the preserved baseline. Material is
{best['material_mm2']:.9f} mm² in both. The new core's minimum separation is
{best['minimum_distance_mm']:.12f} mm, so native-margin qualification remains
absent. The second callback uses five new small poses; the final uses seven.

A fresh diagnosis fixes every placement in each distinct 63-part layout and
checks all ten permitted small-part orientations on both sheets. All **40
continuous insertion queries** complete in **{gaps['seconds']:.6f} seconds**
within 90 seconds. Every padded region is empty. All 150 cached obstacles agree
with independent direct calculations; there are no proposed additions,
pending queries or extra solver calls. These conservative empty regions do
not prove unrestricted impossibility. Further progress needs coordinated
movement rather than a simple padded insertion into these fixed arrangements.

{nextstep['action']}

No native packing, original-budget qualification, full H5 quality matrix or
held-out evaluation occurs. All original gate requirements remain intact.
Product source and all three accurate READMEs are unchanged. Preview
v0.2.0-alpha.1 and stable Latest v0.1.0 remain current; this diagnostic result
does not qualify another release. Main facf0f38 completed all six checks.
Checkpoints 5e88ac91 and 0526421e were pushed normally to main; the new main run
39991641757 is saved as `{current['status']}` / `{current['conclusion'] or 'pending'}`.

Evidence: [generation]({NAME}/generation.json), [geometry audit]({NAME}/geometry.json),
[graph]({NAME}/graph.json), [independent graph audit]({NAME}/audit.json),
[source provenance]({NAME}/provenance.json), [reduction]({NAME}/reduction.json),
[model]({NAME}/model.json), [solver]({NAME}/solver.json),
[original layouts]({NAME}/layouts.json), [new layout]({NAME}/new-layout.json),
[preserved baseline]({NAME}/baseline-layout.json), [retained geometry]({NAME}/retention.json),
[gap diagnosis]({NAME}/gaps.json), [source review]({NAME}/source-review.json),
raw evidence {links}, and [manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']} canonical members and {archive['verified_aliases']}
aliases are byte-verified, with archive CRCs and SHA-256 checked. Each ZIP part
is independently readable and below 50 MiB.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 changed-core small-part selection, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
checks 4,000 fresh small-part poses across seven fixed cores, all 211,995
memberships and a new complete 19,719,151-conflict graph. Certified reduction
retains 4,739 choices, including 1,246 new poses; every constraint and model
field verifies. One bounded solve finds a different 63/66 layout: 11 brackets,
19 inserts, all 18 frames and 15 cogs. It fills 400 mm² more but misses one
bracket and two inserts. Both original 64-part baselines remain preserved.
All four original layout audits pass geometry and fail only original missing
quantities. Forty fresh padded insertion regions are empty, without an
impossibility claim; coordinated small-part moves are the next investigation.
All 1,950 capped member lists and the unresolved full bound remain preserved.
Main facf0f38 passes all six checks, and checkpoints 5e88ac91/0526421e are pushed.
Source, READMEs and releases are unchanged; H2/H5 remain open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
