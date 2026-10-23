"""Seal changed sheet-group selection, fixed-layout gaps and the next frame geometry."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-two-sheet-cog-progress-20261023';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-two-sheet-cog-group-choice-20261023';GAP=ROOT/'output/h5-two-sheet-final-gaps-20261023';TALL=ROOT/'output/h5-tall-frame-cog-subassembly-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();gen=load(BASE/'result.json');graph=load(BASE/'audit/checks.json');red=load(BASE/'reduced/checks.json');hints=load(BASE/'hints/checks.json');model=load(BASE/'solve/model-audit.json');solved=load(BASE/'solve/result.json');layouts=load(BASE/'layout-audit/checks.json');gaps=load(GAP/'checks.json');tall=load(TALL/'checks.json')
    assert all(r['passed'] for r in [graph,red,hints,model,layouts,gaps,tall])
    assert gen['completed_queries']==gen['planned_queries']==500 and gen['new_candidates']=={'insert':1200,'bracket':1600} and gen['retained_candidates']==12960 and gen['pending_lists']==322
    assert graph['all_365_groups_reconstructed'] and graph['no_prior_query_repeated'] and gen['conflicts']==6603323 and gen['residual_edges']==541132
    assert red['kept_candidates']==9022 and red['removed_candidates']==3938 and red['comparisons']==10000000 and red['limit_reached']
    assert hints['completed_cases']==hints['planned_cases']==7300 and not hints['pending_cases']
    assert solved['status']=='FEASIBLE' and solved['objective']==796000000 and solved['best_bound']==model['full_score']==895800000
    assert layouts['layouts_checked_including_hint']==4 and layouts['fresh_frozen_CLI_calls']==4 and not layouts['full_target_witness']
    assert gaps['queries_completed']==gaps['empty_regions']==20 and not gaps['selected_additions'] and not gaps['pending_queries'] and not gaps['pending_proposal_lists']
    assert tall['component_counts']==[8,4,3] and tall['original_geometry_pairs']==438 and not tall['original_CLI_valid']
    oldbest=load(ROOT/'output/h5-dense-insert-gap-20261023/checks.json');best=layouts['best'];improvement=best['filled_area_mm2']-oldbest['filled_area_mm2'];assert 325.43<improvement<325.44
    prior_root=ROOT/'benchmarks/results/h5-complete-cog-group-choice-20261023';prior=load(prior_root/'source-review.json');assert source_digest()==prior['production_digest'] and prior['current_readmes']=={p:digest(ROOT/p) for p in prior['current_readmes']}
    previous_manifest={r['path']:r['sha256'] for r in load(prior_root/'raw-manifest.json')['files']};original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;assert digest(p)==previous_manifest['source-inputs/'+p.relative_to(ROOT).as_posix()]
    for name in ['job.json','conditional-target.json']:assert (original/name).read_bytes()==(ROOT/'output/h5-skeleton-contact-selection-20261020'/name).read_bytes()
    ci=json.loads(subprocess.check_output(['gh','run','view','39955078136','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']=='37b671d3763b7804d605ab123a54cfe3c26cfac7';write(OUT/'main-ci-37b671d3.json',ci)
    next_step=('Do not repeat the 365-group solve, extend its limit, resume its 322 capped lists, or rerun the unchanged empty-gap queries. Preserve both useful partials: the new 63-part layout has higher filled area, while output/h5-dense-insert-gap-20261023/layout.json retains the highest part count of 64. The concrete next construction is output/h5-tall-frame-cog-subassembly-20261023/layout.json: all 18 quarter-turned frames in columns 4/4/5/5, eight dense cogs above the shorter pair of columns, four above the taller pair, and three on the last sheet. All 33 original pieces pass geometry and the frozen CLI reports only the 12 missing brackets and 21 missing inserts. This is not itself a partial improvement. Declare a fresh bounded completion against those exact 33 poses. Preserve the full current source pool before any old frame/cog filtering, append absent fixed poses by exact identity, and generate all bracket orientation/reflection and insert-class contacts. Inspect the already saved bracket/insert compound components and include compatible actual-outline compound contacts under explicit new caps when useful; do not repeat the earlier whole-bounding-rectangle searches. Audit original member geometry, stock, all conflicts and model fields before at most one newly declared selection call. The historical four-tall-column frame pattern already exists; the exact coordinates and 8+4+3 cog subassembly are the changed construction. Native margins, original production repair limits/budget, the complete 66-part target and all H5 jobs/kerfs remain required. H2 retains Artem\'s unchanged gate decision.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'highest_part_count_partial':64,'highest_filled_area_partial_parts':63,'filled_area_improvement_mm2':improvement,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(BASE/'plan.json','plan.json'),(BASE/'result.json','generation.json'),(BASE/'audit/checks.json','graph-audit.json'),(BASE/'reduced/checks.json','reduction-audit.json'),(BASE/'hints/checks.json','hint-audit.json'),(BASE/'solve/model-audit.json','model-audit.json'),(BASE/'solve/result.json','solver-result.json'),(BASE/'layout-audit/checks.json','layout-audit.json'),(BASE/'layout-audit/layout-final.json','partial-layout.json'),(BASE/'layout-audit/public-final.json','partial-public.json'),(BASE/'partial-layout.png','partial-layout.png'),(GAP/'checks.json','gap-audit.json'),(TALL/'plan.json','tall-plan.json'),(TALL/'checks.json','tall-audit.json'),(TALL/'layout.json','tall-subassembly.json'),(TALL/'components.json','tall-components.json'),(TALL/'public.json','tall-public.json')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [BASE,GAP,TALL]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for name,h in load(root/'plan.json')['inputs'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for source in [load(BASE/'reduced/plan.json')['inputs'],load(BASE/'hints/plan.json')['inputs'],model['input_hashes']]:
        for name,h in source.items():assert digest(ROOT/name)==h;inputs[name]=h
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-dense-insert-gap-20261023',['layout.json','checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['build_h5_two_sheet_cog_group_choice.py','audit_h5_two_sheet_cog_group_choice.py','reduce_h5_two_sheet_cog_group_choice.py','seed_h5_two_sheet_cog_group_choice.py','solve_h5_two_sheet_cog_group_choice.py','audit_h5_two_sheet_cog_group_layouts.py','check_h5_two_sheet_final_gaps.py','check_h5_tall_frame_cog_subassembly.py','plot_h5_two_sheet_cog_group_choice.py','plot_h5_dense_insert_gap.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'frozen_original_job_library_request_target_match_prior_manifest':True,'all_geometry_compatibility_graph_reduction_model_and_layout_audits_pass':True,'highest_part_count_partial':64,'highest_filled_area_partial_parts':63,'filled_area_improvement_mm2':improvement,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: two-sheet cog progress and changed frame construction — 2026-10-23

**The new 63-part partial improves filled area by 325.437876 mm².** It contains
all 18 frames and 15 cogs, ten brackets and 20 inserts, missing two brackets and
one insert. The earlier 64-part partial, missing two cogs, remains preserved as
the highest-count result. Neither completes the original 66-copy job. H2/H5
remain open at **60%**.

## Changed complete-group model

This construction combines the previous 165 complete-cog cases with the 200
newly audited sheet distributions. Only new neighborhoods absent from the prior
query set are queried. All 500 queries finish; the 980 previously capped lists
are not resumed. The full source pool is retained before fresh filtering.

Generation takes 4.790236600 seconds, adding 1,600 bracket and 1,200 insert poses
under fresh family caps. All 7,326 events are retained, including 4,526 duplicates
and no geometric rejection. All queries finish; 322 new capped lists remain
pending. Forty Minkowski caches pass absolute-coordinate comparisons with maximum
error 4.687×10⁻¹³ mm, and every query region reconstructs with zero area difference.

Independent checks reconstruct all 365 complete groups, including their 200
new source combinations, and cover 168,910 within-group geometry pairs,
219,150 old/frame pairs and 158,477 proposal/neighbor pairs. All original stock
bounds, allowed transforms and every compatibility list pass. Of 3,481,472
cog/small-part possibilities, 599,372 exact distances establish 502,701 conflicts.

The 12,960 retained choices have 54,714,544 same-sheet pair possibilities.
Independent checks of 7,753,291 exact distances establish 6,603,323 conflicts.
The bounded compression produces 3,711 cliques and retains all 541,132 residual
edges when its allowance expires. Full coverage is checked; no edge is dropped.

## Safe reduction and bounded selection

Fresh substitution certificates require the same family, adjacency, a subset of
other original neighbors, and a superset of compatible complete groups. This
preserves original counts, filled area and group choice. The 10-million-comparison
cap is reached in 2.562611700 seconds; all unprocessed candidates remain. The
3,938 certificates receive 2,908,867 independent neighbor checks and 505,345
group-membership checks. The 9,022 retained choices and 306,217 projected
constraints exactly preserve the induced graph. The previous 63-part seed is
mapped only through these new certificates and checked.

All 7,300 declared starting-layout cases finish in 21.380736700 seconds. The
200 new groups are visited first, followed by the earlier 165. Every selected
set passes graph, group, count and score checks. The best hint has ten brackets
and 19 inserts with all frames/cogs, using group 258.

All fields of the 9,387-variable, 315,243-constraint model are independently
reconstructed. One eight-worker, seed-zero solve with a 60-second allowance takes
62.378406200 seconds; this soft overrun is preserved. It returns `FEASIBLE` with
score 796,000,000 and full-inventory upper bound 895,800,000. The gap remains
unresolved; no optimum or infeasibility is claimed. No call is repeated or extended.

The hint, two callbacks and a different final layout receive four fresh frozen
CLI checks. Every original filled-outer geometry check passes; only the recorded
missing quantities fail. The better layouts use group 259, splitting cogs 12+3
across sheets, and fill 4,381,940.784070 mm². The previous highest filled area was
4,381,615.346194 mm². Charged material is 4,988,890.203495 mm², within the unchanged
target. Minimum clearance is about 0.2001 mm; native margins are unqualified.

![New 63-part diagnostic partial]({NAME}/partial-layout.png)

## Fixed-layout gaps and the next geometry

A separately declared insertion check keeps all 63 final placements exactly
fixed. All 20 bracket/insert orientation queries finish in 8.896743200 seconds;
every conservative padded region is empty. There are no new proposals, capped
lists or pending queries. No solver is called. The unchanged prefix and all
1,467 same-sheet original pairs pass; the recorded fresh CLI check still reports
two missing brackets and one missing insert. Empty conservative regions do not
prove unrestricted impossibility.

A different checked subassembly prepares a new construction: all 18 frames are
quarter-turned in four columns of 4/4/5/5. The two shorter columns leave room
for eight aligned cogs; the two taller columns leave room for four; a saved
three-cog row occupies the last sheet. The eight- and four-cog components are
specified subsets of the previously audited aligned lattice, preserving their
original members before translation normalization.

All 438 original same-sheet pairs and all stock/transform checks pass, with
minimum distance about 0.225 mm. The frozen CLI reports only the twelve missing
brackets and 21 missing inserts. This 33-part subassembly is not a partial
improvement, complete job, or native qualification. Historical four-tall-column
patterns already exist at source indices 22–24, including balanced 5/5/4/4;
the new evidence concerns these exact coordinates and the 8+4+3 cog construction,
not a claim that this frame orientation was never tried.

{next_step}

## Repository and scope

Main remains at pushed `37b671d3`; the prior `356c8523` checkpoint is local and
queued behind its live checks. The saved run `39955078136` is `{ci['status']}`
with conclusion `{ci['conclusion'] or 'pending'}`. No unobserved pass is inferred.
Frozen original job, library, request and target bytes match the preceding raw
manifest. Core source and all three README hashes remain unchanged. The published
preview is accurate, and no new application release qualifies. No production
packing, full quality matrix or reserved-input evaluation occurs.

Evidence: [plan]({NAME}/plan.json), [generation]({NAME}/generation.json),
[graph audit]({NAME}/graph-audit.json), [reduction]({NAME}/reduction-audit.json),
[starting layouts]({NAME}/hint-audit.json), [model]({NAME}/model-audit.json),
[solve]({NAME}/solver-result.json), [original layouts]({NAME}/layout-audit.json),
[gap checks]({NAME}/gap-audit.json), [new subassembly plan]({NAME}/tall-plan.json),
[subassembly audit]({NAME}/tall-audit.json), [subassembly]({NAME}/tall-subassembly.json),
[source review]({NAME}/source-review.json), [raw evidence]({NAME}/raw.zip), and
[manifest]({NAME}/raw-manifest.json). All {len(manifest)} archive members, CRCs and
byte hashes verify.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 two-sheet cog progress, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
improves retained filled area by 325.437876 mm² with a checked 63-part layout,
missing two brackets and one insert. The previous 64-part result remains the
highest-count partial. All 365 groups, 500 new contact queries, 6,603,323 conflicts,
fresh group-preserving substitutions and 7,300 starting layouts are checked.
One bounded solve and all four original layouts retain quantity-only failures;
the full-inventory bound remains unresolved. All 541,132 residual edges and 322
capped lists are preserved. Twenty new fixed-layout gap queries are empty under
positive padding. A separate 18-frame/15-cog subassembly in four tall columns
with 8+4+3 cogs passes original geometry and the expected CLI quantity failure.
Next complete its brackets/inserts under fresh limits; it is not a new best
partial or production repair. Source, accurate READMEs and releases remain
unchanged. H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'filled_area_improvement_mm2':improvement,'new_partial_parts':63,'highest_part_count':64,'CI_status':ci['status']})
if __name__=='__main__':main()
