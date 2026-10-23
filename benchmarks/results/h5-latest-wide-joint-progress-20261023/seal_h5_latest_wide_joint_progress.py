"""Seal the improved 64-part joint result and exact-core next-step evidence."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-latest-wide-joint-progress-20261023';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-latest-wide-joint-20261023';GAP=ROOT/'output/h5-latest-wide-bracket-gaps-20261023';CORE=ROOT/'output/h5-latest-wide-compound-core-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();graph=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');red=load(BASE/'reduced/checks.json');hints=load(BASE/'hints/checks.json');model=load(BASE/'solve/model-audit.json');solved=load(BASE/'solve/result.json');layouts=load(BASE/'layout-audit/checks.json');gaps=load(GAP/'checks.json');core=load(CORE/'checks.json')
    assert all(x['passed'] for x in [audit,red,hints,model,layouts,gaps,core])
    assert graph['conflicts']==20223984 and graph['retained_candidates']==21468 and red['kept_candidates']==13315 and red['removed_candidates']==8153
    assert not red['limit_reached'] and red['residual_edges']==1877444 and red['every_induced_edge_reconstructed_from_constraints']
    assert hints['completed_cases']==416 and not hints['pending_cases'] and hints['best_original_seed_preserved']
    assert solved['status']=='FEASIBLE' and solved['objective']==1566740785 and solved['best_bound']==model['full_score']==1646740785
    assert layouts['layouts_checked_including_hint']==5 and layouts['fresh_frozen_CLI_calls']==4 and layouts['exact_CLI_results_reused']==1 and not layouts['full_target_witness']
    best=next(r for r in layouts['records'] if r['incumbent']=='final');assert best['counts']=={'bracket':10,'insert':21,'frame':18,'cog':15} and best['missing']=={'bracket':2}
    assert gaps['queries_completed']==gaps['empty_regions']==16 and not gaps['pending_queries'] and not gaps['selected_additions'] and gaps['exact_CLI_reuse'] and not gaps['fresh_frozen_CLI_calls']
    assert core['fixed_core_count']==33 and core['seed_count']==64 and core['core_cog_poses_absent_from_previous_63']==4
    previousbest=load(ROOT/'output/h5-two-sheet-cog-group-choice-20261023/layout-audit/checks.json')['best'];improvement=best['filled_area_mm2']-previousbest['filled_area_mm2'];assert abs(improvement-19800)<1e-6
    older64=load(ROOT/'output/h5-dense-insert-gap-20261023/checks.json');overolder=best['filled_area_mm2']-older64['filled_area_mm2'];assert 20125.43<overolder<20125.44
    priorroot=ROOT/'benchmarks/results/h5-frame-compound-limits-20261023';prior=load(priorroot/'source-review.json');assert source_digest()==prior['production_digest'] and prior['current_readmes']=={p:digest(ROOT/p) for p in prior['current_readmes']}
    previous_manifest={r['path']:r['sha256'] for r in load(priorroot/'raw-manifest.json')['files']};original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;assert digest(p)==previous_manifest['source-inputs/'+p.relative_to(ROOT).as_posix()]
    for name in ['job.json','conditional-target.json']:assert (original/name).read_bytes()==(ROOT/'output/h5-skeleton-contact-selection-20261020'/name).read_bytes()
    ci=json.loads(subprocess.check_output(['gh','run','view','39960579594','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']=='4592d97ccd03ae9127482b88ec197a864361d5a1';write(OUT/'main-ci-4592d97c.json',ci)
    next_step=('Do not repeat or extend the 60-second all-family solve, resume the bounded compression, or repeat the 16 unchanged fixed-64 bracket gap queries. Preserve the improved final layout at output/h5-latest-wide-joint-20261023/layout-audit/layout-final.json, its intermediate 64-part layout with one bracket and one cog missing, and both earlier best partials. The concrete next construction is output/h5-latest-wide-compound-core-20261023/layout.json: exactly the new 18 wide frames and 15 cogs, with all 31 small parts from source-seed.json retained as the baseline. Four cog poses differ from the previous 63-part core; its 12+3 sheet split passes 438 original pairs. Declare a fresh bounded actual-outline compound contact experiment against these 33 fixed poses, using all 36 saved two-to-four-member bracket/insert patterns under four whole-group quarter turns plus all allowed single-part classes on both sheets. These actual-compound contacts were checked on the inferior tall and mixed cores, not this new wide core; prior wide whole-bounding-rectangle probes and single-part complete-group queries are not resumed. Preserve the entire 29,838-pose source pool before fresh filtering, map the 64-part seed exactly, retain every pending event under fresh caps, and independently audit every original member, cache, region, mutual conflict and model field. Fresh substitutions must preserve the seed and original counts; use its 10 brackets and 21 inserts as a score floor. At most one newly declared solve may seek 12 brackets and 21 inserts. Native margins, unchanged production repair limits and the full original H5 jobs/kerfs remain required after a complete 66-part witness. H2 retains Artem\'s unchanged gate and the 22 reserved vectors remain unopened.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'highest_part_count_partial':64,'highest_filled_area_partial_parts':64,'filled_area_improvement_mm2':improvement,'improvement_over_earlier_64_mm2':overolder,'missing':{'bracket':2},'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(BASE/'plan.json','plan.json'),(BASE/'result.json','graph-generation.json'),(BASE/'audit/checks.json','graph-audit.json'),(BASE/'reduced/checks.json','reduction-audit.json'),(BASE/'hints/checks.json','hint-audit.json'),(BASE/'solve/model-audit.json','model-audit.json'),(BASE/'solve/result.json','solver-result.json'),(BASE/'layout-audit/checks.json','layout-audit.json'),(BASE/'layout-audit/layout-final.json','partial-layout.json'),(BASE/'layout-audit/public-final.json','partial-public.json'),(BASE/'partial-layout.png','partial-layout.png'),(GAP/'checks.json','gap-audit.json'),(CORE/'plan.json','next-core-plan.json'),(CORE/'checks.json','next-core-audit.json'),(CORE/'layout.json','next-core-layout.json')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [BASE,GAP,CORE]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for name,h in load(root/'plan.json')['inputs'].items():
            if name in inputs:assert inputs[name]==h
            inputs[name]=h
    for mapping in [load(BASE/'reduced/plan.json')['inputs'],load(BASE/'hints/plan.json')['inputs'],model['input_hashes'],load(GAP/'command.json')['source_files']]:
        for name,h in mapping.items():
            if name in inputs:assert inputs[name]==h
            inputs[name]=h
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-dense-insert-gap-20261023',['layout.json','checks.json']),('h5-two-sheet-cog-group-choice-20261023',['layout-audit/layout-final.json','layout-audit/checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['build_h5_latest_wide_joint.py','audit_h5_latest_wide_joint.py','reduce_h5_latest_wide_joint.py','seed_h5_latest_wide_joint.py','prepare_h5_latest_wide_joint_selection.py','solve_h5_latest_wide_joint.py','audit_h5_latest_wide_joint_layouts.py','prepare_h5_latest_wide_gaps.py','check_h5_latest_wide_bracket_gaps.py','check_h5_latest_wide_compound_core.py','plot_h5_latest_wide_joint.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive=OUT/'raw.zip';manifest=[]
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'original_inputs_match_previous_manifest':True,'complete_graph_reduction_model_and_original_layout_checks_pass':True,'highest_part_count_partial':64,'highest_filled_area_partial_parts':64,'filled_area_improvement_mm2':improvement,'missing':{'bracket':2},'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: improved joint wide-frame partial — 2026-10-23

**The new best partial fits 64 of 66 original parts and lacks only two brackets.**
All 18 frames, 15 cogs and 21 inserts are present. Filled area improves by
**19,800 mm²** over the previous best 63-part layout and by **20,125.437876 mm²**
over the older 64-part layout that lacked two cogs. Both older layouts and every
intermediate result remain preserved. This is not a complete job; H2/H5 remain
open at **60%**.

## Complete changed graph and safe reduction

The full 29,838-entry source pool is preserved before fresh filtering against
only the 18 exact wide frames. All 21,468 eligible cog/bracket/insert choices
are reconsidered together: 8,359 brackets, 8,588 inserts and 4,521 cogs.
This includes every previous all-family choice plus 8,914 compatible additions.
No new pose or old pending-list continuation is introduced here.

Graph construction takes {graph['graph_seconds']:.9f} seconds. A separate bounds
scan checks 149,735,398 same-sheet possibilities and 23,855,322 exact distances,
reconstructing **20,223,984 conflicts** and every saved adjacency row. The
original filter receives 404,658 pair checks; all stock bounds and transforms,
153 frame/frame pairs and both previous partial geometries pass. The graph is
stored as documented fixed-width binary rows with a verified byte hash.

Fresh substitutions consider the entire audited graph and require same family,
adjacency and a subset of all other neighbors. They finish all 43,417,456
comparisons in {red['seconds']:.9f} seconds, below the declared 30-second /
50-million-comparison limits. Independent enumeration checks 12,928,359
certificate neighbors. Removing 8,153 choices leaves 13,315, preserves both
seed counts and geometry feasibility, and retains an exact induced graph of
9,231,632 edges.

Constraint compression happens after reduction. Its 20-second allowance ends
at {red['compression_seconds']:.9f} seconds; 1,770 cliques and **all 1,877,444
residual edges** are saved. Independent reconstruction confirms complete
coverage by the 1,879,214 constraints. No edge is dropped to simplify the model.

## Bounded selection and original acceptance checks

All 416 fresh starting-layout cases finish in {hints['seconds']:.9f} seconds.
They cover both mapped original partials, each intact or with one small-part
family released, under 52 deterministic orders. Every result's graph, original
caps and score passes; none improves the saved 63-part seed.

Every field of the 13,315-variable, 1,879,218-constraint model is independently
reconstructed. Original integer area weights preserve all 4,576 original
quantity-combination orderings. One eight-worker, seed-zero call with a
60-second allowance takes **{solved['seconds']:.9f} seconds**; the soft overrun
is retained. It returns `FEASIBLE` with score 1,566,740,785 and full-inventory
upper bound 1,646,740,785. The gap is unresolved; no optimum or impossibility
is claimed. No call is repeated or extended.

The hint, three callbacks and different final selection receive five original
layout audits: four fresh frozen-CLI calls and one exact-layout reuse with
source hashes. All original geometry passes. Only expected missing quantities
fail. The intermediate 64-part layout lacking one bracket and one cog is also
preserved, before the better 64-part result lacking two brackets.

The final result fills **4,401,740.784070 mm²** and charges 4,988,890.203495 mm²,
within the unchanged material target. All 1,521 same-sheet original pairs pass.
Minimum clearance is about 0.2001 mm; native margins remain unqualified.

![Improved 64-part diagnostic partial]({NAME}/partial-layout.png)

## Fixed-layout gaps and the next construction

Sixteen fresh bracket orientation/reflection queries against the exact fixed
64-part layout finish in {gaps['generation_seconds']:.9f} seconds. Every padded
region is empty; no proposals or pending queries remain. The unchanged layout
and its 1,521 pairs pass. Its frozen CLI result is reused only by exact equality
and source hashes, with no repeated call. Conservative empty regions do not
prove unrestricted packing impossibility.

The next checked core extracts exactly the new 18 frames and 15 cogs while
retaining the original 64-part layout as its completion seed. It passes all
stock/transform checks and 438 original same-sheet pairs, with minimum gap
0.2126 mm. Cogs split 12+3 across sheets; four cog poses differ from the previous
63-part core. Every core and seed pose maps exactly to the full source pool.
This is a subset geometry check, not an additional full-job CLI acceptance.

{next_step}

## Repository and evidence

Remote main is still 4592d97c, with no incoming changes after fetch. The previous
abc464a2 audit is queued locally. Main run 39960579594 is saved as
`{ci['status']}` / `{ci['conclusion'] or 'pending'}`; no unobserved pass is inferred.
Queued commits will be pushed normally once those checks finish successfully.

Original job, library, request and target hashes match the preceding archive.
Production source and all three README hashes remain unchanged. The README's
published-preview wording remains accurate; this diagnostic work does not
qualify a new application release. No native packing, full quality matrix,
registry publication or reserved-input evaluation occurs.

Evidence: [plan]({NAME}/plan.json), [graph]({NAME}/graph-audit.json),
[reduction]({NAME}/reduction-audit.json), [hints]({NAME}/hint-audit.json),
[model]({NAME}/model-audit.json), [solve]({NAME}/solver-result.json),
[original layouts]({NAME}/layout-audit.json), [gap checks]({NAME}/gap-audit.json),
[next core]({NAME}/next-core-audit.json), [source review]({NAME}/source-review.json),
[raw evidence]({NAME}/raw.zip) and [manifest]({NAME}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 improved joint partial, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
places all frames, cogs and inserts: 64/66 parts, lacking two brackets. Filled
area improves by 19,800 mm² over the previous best; all older partials remain.
The complete 21,468-choice graph, 20,223,984 conflicts, fresh substitutions,
1,877,444 retained residual edges and every model field are checked. One bounded
solve returns feasible; all five original layouts pass geometry with expected
quantity-only failures. Sixteen new fixed-layout bracket regions are empty under
positive padding. The next checked 33-part core has four changed cog poses and
preserves the new 64-part seed for fresh actual-compound bracket/insert contacts.
No previous solve, capped list or unchanged gap check is resumed. Main's current
checks remain separately recorded; queued commits await their successful finish.
Source, accurate READMEs and releases remain unchanged. H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'best_parts':64,'filled_area_improvement_mm2':improvement,'main_CI_status':ci['status']},flush=True)
if __name__=='__main__':main()
