"""Seal complete-cog group choice, all returned layouts, and two-sheet coverage."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-complete-cog-group-choice-20261023';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output'/NAME;COVER=ROOT/'output/h5-cog-sheet-group-coverage-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();gen=load(BASE/'result.json');graph=load(BASE/'audit/checks.json');hints=load(BASE/'hints/checks.json');model=load(BASE/'solve/model-audit.json');solved=load(BASE/'solve/result.json');layouts=load(BASE/'layout-audit/checks.json');coverage=load(COVER/'checks.json')
    assert all(v['passed'] for v in [graph,hints,model,layouts,coverage])
    assert gen['completed_queries']==gen['planned_queries']==1670 and gen['new_candidates']=={'bracket':1600,'insert':1200} and gen['retained_candidates']==9089 and gen['pending_lists']==980
    assert gen['conflicts']==3051661 and graph['all_165_groups_reconstructed'] and graph['complete_graph_coverage']
    assert hints['completed_cases']==hints['planned_cases']==3300 and hints['best_hint']['objective']==756000000
    assert solved['status']=='FEASIBLE' and solved['objective']==775800000 and solved['best_bound']==model['full_score']==895800000
    assert layouts['layouts_checked_including_hint']==4 and layouts['fresh_frozen_CLI_calls']==4 and not layouts['full_target_witness']
    assert coverage['checked_combinations']==210 and coverage['new_complete_groups']==200 and not coverage['pending_combinations']
    previous=load(ROOT/'benchmarks/results/h5-complete-cog-small-relocation-20261023/source-review.json')
    assert source_digest()==previous['production_digest'] and previous['current_readmes']=={p:digest(ROOT/p) for p in previous['current_readmes']}
    passed=load(BASE/'main-ci-2333dd2c.json');assert passed['conclusion']=='success' and len(passed['jobs'])==6 and all(j['conclusion']=='success' for j in passed['jobs']);shutil.copyfile(BASE/'main-ci-2333dd2c.json',OUT/'main-ci-2333dd2c.json')
    ci=json.loads(subprocess.check_output(['gh','run','view','39955078136','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']=='37b671d3763b7804d605ab123a54cfe3c26cfac7';write(OUT/'main-ci-37b671d3.json',ci)
    assert subprocess.check_output(['git','rev-list','--left-right','--count','origin/main...HEAD'],cwd=ROOT).decode().split()==['0','0']
    next_step=('Do not repeat the expired 165-group solve or resume its 980 capped proposal lists. The saved 64-part layout remains the best retained partial by both part count and filled area. Use output/h5-cog-sheet-group-coverage-20261023/new-cases.json for 200 independently checked additional complete-cog arrangements: 75 with five cogs on the last sheet, 75 with three, and 50 with one at catalogue poses different from the exact old last-sheet seed. Combine these with the existing 165 cases in a fresh declared 365-group construction, preserving every source/global candidate index and the new checked 63-part case-144 seed. Begin from the complete current source pool before group-compatibility filtering. Generate new small-part contacts only for the additional case neighborhoods under freshly declared time/family caps; reconstruct all compatibility, actual geometry and the complete changed graph before at most one newly declared selection call. Preserve all failures, caps and pending work. Merely combining the already checked components is not a full-job witness, a new production repair, or proof that two-sheet cog distributions have never been tried elsewhere. Original native margins, production repair limits and budget, 66-part validity and all H5 jobs/kerfs still apply. H2 retains Artem\'s unchanged gate.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':previous['current_readmes'],
      'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,
      'prior_commits_pushed':'37b671d3763b7804d605ab123a54cfe3c26cfac7','native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(BASE/'plan.json','plan.json'),(BASE/'result.json','generation.json'),(BASE/'audit/checks.json','graph-audit.json'),(BASE/'hints/checks.json','hint-audit.json'),(BASE/'solve/model-audit.json','model-audit.json'),(BASE/'solve/result.json','solver-result.json'),(BASE/'layout-audit/checks.json','layout-audit.json'),(BASE/'layout-audit/layout-final.json','partial-layout.json'),(BASE/'layout-audit/public-final.json','partial-public.json'),(BASE/'partial-layout.png','partial-layout.png'),(COVER/'plan.json','coverage-plan.json'),(COVER/'checks.json','coverage-audit.json'),(COVER/'new-cases.json','new-cases.json')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [BASE,COVER]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for name,h in load(root/'plan.json')['inputs'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for source in [load(BASE/'hints/plan.json')['inputs'],model['input_hashes']]:
        for name,h in source.items():assert digest(ROOT/name)==h;inputs[name]=h
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-complete-cog-small-pool-20261023',['layout-audit/layout-final.json','layout-audit/public-final.json','layout-audit/command-final.json']),('h5-dense-insert-gap-20261023',['layout.json','checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['build_h5_complete_cog_group_choice.py','audit_h5_complete_cog_group_choice.py','seed_h5_complete_cog_group_choice.py','solve_h5_complete_cog_group_choice.py','audit_h5_complete_cog_group_layouts.py','audit_h5_cog_sheet_group_coverage.py','plot_h5_complete_cog_group_choice.py','plot_h5_dense_insert_gap.py','record_h5_group_choice_ci.py','ccd1.py']];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'all_geometry_compatibility_graph_model_and_layout_audits_pass':True,'best_retained_parts':64,'new_partial_parts':63,'new_partial_improves_retained_filled_area':False,
      'new_two_sheet_groups':200,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: complete-cog group choice and sheet coverage — 2026-10-23

**The best retained partial remains 64/66 parts.** A new choice among 165 complete
cog groups improves this branch to 63/66: all 18 frames, all 15 cogs, all 21
inserts, and nine of 12 brackets. Its filled area is still below the saved
64-part result. A separate audit identifies 200 additional complete-cog groups,
including distributions with three or five cogs on the last sheet. H2/H5 remain
open at **60%**.

## Construction and independent graph audit

The [previous experiment](h5-complete-cog-small-relocation-20261023.md) fixed one
complete-cog arrangement. This construction instead chooses one of all 165 saved
cases, each with the same 18 frames, while every bracket and insert may move.
Every original source candidate keeps its exact index. Old small parts excluded
by a former fixed cog arrangement are reconsidered against all cases.

Exact neighborhood deduplication gives 1,670 new translation-region queries.
All finish in 6.992402800 seconds. Thirty zero-origin Minkowski cache entries
are checked against absolute-position calculations; maximum coordinate error
is 4.619×10⁻¹³ mm. Every query region is reconstructed with zero area difference.
The new caps add 1,600 bracket and 1,200 insert poses. Generation takes
9.488442600 seconds. All 13,226 events are retained: 10,426 duplicates and no
geometry rejections. The family caps leave 980 recorded lists pending; none is
resumed. No query is unbuilt.

Independent checks reconstruct all 165 groups and cover 82,160 within-group
original geometry pairs, 169,794 old/frame pairs and 418,731 proposal/neighbor
pairs. Every allowed transform, stock bound and complete seed is checked.
Among 2,007,005 cog/small-part possibilities, 333,130 exact distances establish
277,611 conflicts. Every complete-group compatibility list is reconstructed.

The resulting 9,089 small-part choices have 28,654,006 same-sheet pair
possibilities. The independent audit checks 3,495,106 exact distances, finding
3,051,661 conflicts. All are covered by 13,632 verified cliques; there are no
residual edges or compression expiry. Old source coordinates and the original
61-part seed remain unchanged.

## Starting layouts and one bounded solve

A separately declared 30-second construction census checks 20 deterministic
small-part orderings for every group. All 3,300 cases finish in 15.958726700
seconds. Every result is checked against full compatibility, conflicts, quantity
caps and filled-area score. The best starting layout uses case 97 and contains
62 parts: nine brackets and 20 inserts alongside all frames and cogs.

All fields of the 9,254-variable, 22,725-constraint protobuf model are independently
reconstructed before one eight-worker, seed-zero solve. Its 60-second allowance
finishes in 60.296662800 seconds; the soft overrun is preserved. Two callbacks
and a different final result are retained. Status is `FEASIBLE`, with score
775,800,000 and upper bound 895,800,000, the full-inventory score. The bound
therefore remains unresolved; neither optimality nor finite infeasibility is
claimed. No extra call or limit extension occurs.

The best returned counts use case 144 and total 63 parts, missing three brackets.
Filled area is 4,361,740.784070 mm², below the saved 64-part result's
4,381,615.346194 mm². The second callback uses 4,985,157.064866 mm² of charged
material; the different final layout reaches the original target of
4,988,890.353495 mm². All four layouts, including the starting hint, receive
fresh frozen-CLI checks. Their only failures are the recorded missing quantities.
Original filled-outer geometry passes throughout. Minimum clearance is about
0.2001 mm, so native construction margins remain unqualified.

![Checked 63-part partial, missing three brackets]({NAME}/partial-layout.png)

The image shows the final diagnostic layout. Frame holes remain reserved; this
is not a complete cutting layout or an H5 pass.

## Additional distributions across sheets

The 165 cases put zero or one cog on the last sheet. A fresh finite coverage audit
combines every saved first-sheet catalogue group with every saved last-sheet
group (or no last group) whose counts total exactly 15. It preserves exact source
poses and checks all original stock, transform and pair constraints. This is
coverage of the present group-selection model, not a claim that earlier unrelated
algorithms never tried other sheet distributions.

All 210 declared combinations finish in 0.256266400 seconds, with none pending.
There are 6,930 stock/transform checks and 92,030 original same-sheet pair checks,
including exact reuse of 7,649 distinct pairs. Minimum distance is 0.2126 mm.
All component poses already exist in the full source pool.

Ten combinations match existing complete groups. The other 200 are new to this
165-case model: 75 split cogs 10+5 across sheets, 75 split them 12+3, and 50 split
them 14+1 using different last-sheet catalogue poses. These are valid frame/cog
subassemblies; no small-part completion or full original CLI pass is claimed.

{next_step}

## Repository and release status

All six checks on main `2333dd2c` passed. The two preceding checkpoints were
pushed normally together as `37b671d3`, with local and remote ancestry equal
after the push. Its new run `39955078136` is saved as `{ci['status']}` with
conclusion `{ci['conclusion'] or 'pending'}`; no unobserved pass is inferred.
Production source and all three README hashes remain unchanged. The existing
preview is accurate, and no new application build qualifies for release. No
production packing, quality matrix or reserved-input evaluation occurs.

Evidence: [plan]({NAME}/plan.json), [generation]({NAME}/generation.json),
[graph audit]({NAME}/graph-audit.json), [starting layouts]({NAME}/hint-audit.json),
[model audit]({NAME}/model-audit.json), [solver result]({NAME}/solver-result.json),
[original layouts]({NAME}/layout-audit.json), [coverage plan]({NAME}/coverage-plan.json),
[coverage audit]({NAME}/coverage-audit.json), [new cases]({NAME}/new-cases.json),
[source review]({NAME}/source-review.json), [raw evidence]({NAME}/raw.zip), and
[manifest]({NAME}/raw-manifest.json). All {len(manifest)} archive members, CRCs and
byte hashes verify.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 complete-cog group choice, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
preserves the best 64/66 partial. All 1,670 newly declared group/contact queries
and 3,300 starting layouts complete. The 9,089 choices, 165 group decisions,
3,051,661 conflicts and full model pass independent checks. One bounded solve
reaches 63 parts, missing three brackets; its filled area remains below the
retained result and its bound is unresolved. All four original layouts pass
geometry and retain quantity-only CLI failures. The 980 capped lists remain
pending. A new 210-combination coverage audit identifies 200 additional complete
cog groups, including 12+3 and 10+5 distributions across sheets. Next test those
changed group choices under fresh limits; do not repeat the expired model.
All six prior-main checks pass and both saved checkpoints are pushed as 37b671d3.
Source, accurate READMEs and releases remain unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'prior_commits_pushed':'37b671d3','CI_status':ci['status'],'best_retained_parts':64,'new_branch_parts':63,'new_group_cases':200})
if __name__=='__main__':main()
