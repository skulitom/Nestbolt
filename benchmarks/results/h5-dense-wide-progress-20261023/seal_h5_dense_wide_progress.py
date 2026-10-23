"""Seal the improved64-part partial and the next conditional capacity evidence."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,math,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-dense-wide-progress-20261023';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-dense-wide-contacts-20261023';GAP=ROOT/'output/h5-dense-insert-gap-20261023';BOUND=ROOT/'output/h5-dense-fixed-cog-capacity-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();gen=load(BASE/'result.json');graph=load(BASE/'audit/checks.json');red=load(BASE/'reduced/checks.json');hint=load(BASE/'group-hints/checks.json');model=load(BASE/'solve/model-audit.json')
    solved=load(BASE/'solve/result.json');layouts=load(BASE/'layout-audit/checks.json');gap=load(GAP/'checks.json');bound=load(BOUND/'audit/checks.json')
    assert all(r['passed'] for r in [graph,red,hint,model,layouts,gap,bound])
    assert gen['new_candidates']=={'cog':488,'bracket':1200,'insert':800} and gen['completed_queries']==gen['planned_queries']==750
    assert graph['conflicts']==7910375 and red['kept_candidates']==9183 and hint['completed_cases']==3000 and hint['pending_cases']==0
    assert solved['status']=='FEASIBLE' and solved['incumbents']==4 and solved['counts']=={'frame':18,'bracket':12,'cog':13,'insert':20}
    assert layouts['layouts_checked_including_hint']==6 and layouts['fresh_frozen_CLI_calls']==5 and layouts['exact_CLI_results_reused']==1
    assert gap['counts']=={'frame':18,'bracket':12,'cog':13,'insert':21} and gap['queries_completed']==4 and gap['full_layout_pairs']==1392
    assert bound['records'][0]['sheet_bounds']==[18,1] and not bound['records'][0]['fifteen_cogs_ruled_out']
    prior=max(load(ROOT/'output/h5-group-choice-20261023/layout-audit/checks.json')['records'],key=lambda r:r['filled_area_mm2'])
    gain=gap['filled_area_mm2']-prior['filled_area_mm2'];assert abs(gain-39600)<1e-7
    previous=load(ROOT/'benchmarks/results/h5-wide-small-selection-20261023/source-review.json')
    assert source_digest()==previous['production_digest'] and previous['current_readmes']=={p:digest(ROOT/p) for p in previous['current_readmes']}
    # Recompute material from all original transformed vertices, including the added insert.
    job=load(ROOT/'output/h5-skeleton-contact-selection-20261020/job.json');parts={p['id']:p for p in job['parts']};stock=job['stocks'][0];target=load(ROOT/'output/h5-skeleton-contact-selection-20261020/conditional-target.json')
    tops={s:0 for s in ['sheet-0','sheet-1']};final=load(GAP/'layout.json')
    assert final['placements'][:-1]==load(BASE/'layout-audit/layout-final.json')['placements'] and final['placements'][-1]==gap['appended_insert']
    for p in final['placements']:
        t=p['transform'];c,s=math.cos(t['rotation_radians']),math.sin(t['rotation_radians']);mirror=-1 if t['mirrored'] else 1
        top=max(mirror*x*s+y*c+t['translation'][1] for x,y in parts[p['part_id']]['geometry'][0]['outer'])+stock['margins']['top']+job['edge_clearance'];tops[p['sheet_id']]=max(tops[p['sheet_id']],top)
    material=stock['width']*(stock['height']+tops['sheet-1']);assert material<=target['target_material_mm2']+1e-6 and abs(material-4988890.203494999)<1e-6
    ci=json.loads(subprocess.check_output(['gh','run','view','39945225743','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']=='37edb1d2cf11afed380a5c355a1ba0396a65e6ae';write(OUT/'main-ci-37edb1d2.json',ci)
    next_step=('Use the exact 64-part layout in output/h5-dense-insert-gap-20261023/layout.json as the retained seed. Its 51 fixed non-cogs allow at most 19 cogs under the checked continuous relaxation: 18 on the first sheet and 1 on the last. This is inconclusive for 15, not evidence of attainability. Next construct a changed cog-only pool against those exact 51 poses, retaining every compatible old cog and all 13 seed cogs. Include current actual cog angles and the declared sampled phases on both sheets, with original-outline free-region contacts and the applicable audited denser groups. Declare finite generation and solver bounds, check every new transform/conflict, and solve only after independent model review. Do not retry the expired all-small model or resume capped lists. If the finite cog pool cannot complete 15, keep the failure and investigate coordinated non-cog moves instead of claiming continuous impossibility. A full 66-copy original witness, native margins, production-budget qualification and all unchanged H5 gates are required before integration. H2 stays open under Artem’s retained-denominator decision.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),
      'current_readmes':previous['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
      'completion_percent':60,'H2_complete':False,'H5_complete':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    copies=[(BASE/'plan.json','plan.json'),(BASE/'result.json','generation.json'),(BASE/'audit/checks.json','graph-audit.json'),(BASE/'reduced/checks.json','reduction-audit.json'),
      (BASE/'group-hints/checks.json','group-hints-audit.json'),(BASE/'solve/model-audit.json','model-audit.json'),(BASE/'solve/result.json','solver-result.json'),(BASE/'layout-audit/checks.json','layout-audit.json'),
      (GAP/'checks.json','insert-gap-audit.json'),(GAP/'layout.json','layout-64.json'),(GAP/'public.json','public-64.json'),(GAP/'partial-layout.png','partial-layout.png'),(BOUND/'audit/checks.json','capacity-audit.json')]
    for p,name in copies:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [BASE,GAP,BOUND]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for plan in [BASE/'plan.json',BASE/'reduced/plan.json',BASE/'group-hints/plan.json',GAP/'plan.json',BOUND/'plan.json']:
        for name,h in load(plan)['inputs'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name,h in model['input_hashes'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),
      ('h5-group-choice-20261023',['layout-audit/checks.json','layout-audit/layout-final.json','layout-audit/public-final.json','layout-audit/command-final.json','mapping.json']),
      ('h5-wide-small-pool-20261023',['layout-audit/layout-final.json','layout-audit/public-final.json','layout-audit/command-final.json']),
      ('h5-wide-catalogue-coverage-20261023',['placements.json','new-poses.json','checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    # Every exact-result reuse is bound to the actual source bytes retained here.
    for p in (BASE/'layout-audit').glob('validation-reuse-*.json'):
        for name,h in load(p)['source_files'].items():
            other=ROOT/name;assert digest(other)==h;members['validation-sources/'+other.relative_to(ROOT).as_posix()]=other
    pending=[ROOT/'output'/n for n in ['build_h5_dense_wide_contacts.py','audit_h5_dense_wide_contacts.py','reduce_h5_dense_wide_contacts.py','seed_h5_dense_wide_groups.py','solve_h5_dense_wide_contacts.py',
      'audit_h5_dense_wide_layouts.py','check_h5_dense_insert_gap.py','bound_h5_dense_fixed_cogs.py','audit_h5_dense_fixed_cogs.py','plot_h5_dense_wide_contacts.py','plot_h5_dense_insert_gap.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
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
    write(OUT/'checks.json',{'passed':True,'all_source_hashes_verified':True,'all_geometry_graph_model_and_capacity_audits_pass':True,'retained_parts':64,'missing':{'cog':2},'filled_area_mm2':gap['filled_area_mm2'],
      'filled_area_gain_over_previous_best_mm2':gain,'original_material_mm2':material,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,
      'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    passing=sum(j['conclusion']=='success' for j in ci['jobs']);ci_text=('All six checks on main `37edb1d2` pass.' if ci['conclusion']=='success' else f'The saved main `37edb1d2` snapshot has {passing} passing checks; Windows remains running. The queued evidence checkpoint has not been pushed over that live run.')
    report=f'''# H5: denser cog groups improve the partial to 64 parts — 2026-10-23

**The retained partial now places 64 of the original 66 parts.** All frames,
brackets and inserts fit; two cogs are still missing. Filled area rises to
**4,381,615.346194 mm²**, a **39,600 mm²** gain over the previous best, within
the same material allowance. This is still an incomplete job. H2/H5 remain
open at **60%**, and no native quality or release claim follows.

![Improved64-part partial; frame holes remain reserved]({NAME}/partial-layout.png)

## Changed contacts and complete collision checks

The [previous coverage audit](h5-wide-small-selection-20261023.md) supplied 488
absent cog poses from denser, already checked groups. The changed pool retains
all 10,066 old choices before any old reduction; a previous substitution could
cease to be valid against a newly added position. All 488 cog poses are added.

Seventy-five placed groups with at least nine cogs produce 750 bracket/insert
queries. Groups propose positions only; all small families remain free in the
final selection. Cached zero-translation original-outline Minkowski obstacles
are translated for each neighbor. All queries finish. The fresh caps add 1,200
bracket and 800 insert poses, leaving 626 recorded proposal lists pending.
Generation takes 6.811821100 seconds; no old capped list is resumed.

Independent checks reconstruct all 750 free regions and compare all 40 cache
entries with direct absolute-position calculations; maximum translation error
is 4.69×10⁻¹³ mm. All 303,804 frame pairs and 69,123 proposal/group pairs pass,
with no geometric rejection. Exact transform deduplication records 4,248 duplicates.
Among 54,495,448 same-sheet possibilities, 9,460,375 exact distances establish
7,910,375 conflicts. Bounded compression retains 2,022 cliques and 1,477,496
explicit residual edges. The independent audit proves complete coverage.

Fresh same-family substitution certificates remove 3,371 poses, checking
2,985,531 replacement-neighbor relations. The ten-million-comparison cap stops
further reductions after 4.452257200 seconds; remaining choices stay present.
All 9,183 retained variables and 927,875 projected conflict constraints are checked.

## Better starts and one bounded solve

The original wider-frame 62-part result survives the changed graph and fresh
substitutions. Forty greedy scans do not improve it. A separately declared
finite enumeration then starts from each of the 75 denser cog groups, with or
without the optional insert strip, using 20 ordering rules. All 3,000 cases
complete in 20.267838900 seconds, below 30 seconds; every final mask is checked.
The best starting layout contains 63 parts, missing three cogs.

Every protobuf model field is independently reconstructed before solving.
Binary model export uses the installed exporter's documented format and avoids
parsing a large text model; it changes no constraint or solver parameter.
One eight-worker, seed-zero call uses the declared 60-second limit and returns
`FEASIBLE` after 61.654028900 seconds. The measured soft overrun is preserved.
Four callbacks and a distinct final selection are saved. The bound still permits
full inventory; neither optimality nor unrestricted impossibility is established.

The best selection has 18 frames, 12 brackets, 13 cogs and 20 inserts. Its filled
area is 4,361,815.346194 mm², 19,800 mm² above the previous best. The starting
hint and all five returned layouts pass independent original stock, rotation,
mirror, pair-distance and material checks. Five fresh frozen-CLI calls fail only
for their recorded missing quantities. The first callback exactly matches the
checked hint, so its result is reused with source-byte verification.

## One more insert fits without moving the other parts

Four new conservative free-region queries test the two rectangular orientations
on both sheets while preserving every one of the final 63 placements. Three
regions are empty. The fourth supplies 23 valid positions, all checked against
the original neighbors (1,173 pairs). One insert is appended deterministically.
The original 63 placements remain byte-for-byte equal.

All 1,392 pairs in the resulting 64-part layout pass. A fresh frozen-CLI check
reports exactly two missing cogs and no other violation. Charged material remains
4,988,890.203495 mm² against the unchanged 4,988,890.353495 mm² target. Minimum
clearance remains about 0.2011 mm; native construction margins are unqualified.
The conservative insertion queries are not a general impossibility test.

## Continuous capacity and next investigation

With the new 51 non-cog placements fixed, a necessary all-angle cog relaxation
allows at most 18 cogs on the first sheet and one on the second, total 19.
The independent exact-rational audit checks 75 strictly interior rectangles,
two components, four diameter covers, every complement and reachable-area
calculation, and retention of all 13 current cogs. This bound is inconclusive
for the required 15; it does not assert that they can be packed.

{next_step}

## Repository and release

{ci_text} Core source and all three README hashes remain unchanged. The existing
v0.2.0-alpha.1 preview and hosted browser preview are still accurately described;
no new application build is qualified. Stable v0.1.0 and registry versions remain
unchanged. No reserved inputs, native packing runs or quality matrices are used.
Artem’s H2 denominator decision and release authorization remain in force.

Evidence: [generation]({NAME}/generation.json), [geometry/graph audit]({NAME}/graph-audit.json),
[substitution audit]({NAME}/reduction-audit.json), [starting layouts]({NAME}/group-hints-audit.json),
[model audit]({NAME}/model-audit.json), [solver result]({NAME}/solver-result.json),
[returned-layout audit]({NAME}/layout-audit.json), [insert addition]({NAME}/insert-gap-audit.json),
[retained64-part layout]({NAME}/layout-64.json), [original CLI failure]({NAME}/public-64.json),
[capacity audit]({NAME}/capacity-audit.json), [source review]({NAME}/source-review.json),
[raw evidence]({NAME}/raw.zip), and [manifest]({NAME}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    report=report.replace('Improved64','Improved 64').replace('retained64','retained 64')
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 denser-cog progress, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
improves the retained partial to 64/66 original parts, missing two cogs. Filled
area is 4,381,615.346194 mm², 39,600 mm² above the previous best, under the same
material target. All 750 new contact queries, 7,910,375 conflicts, fresh safe
substitutions and 3,000 group-based starting layouts are checked. One bounded
solve reaches 63 parts; a new gap query appends an insert without moving any
of them. All original geometry checks pass and the frozen CLI retains the two-cog
quantity failure. Native margins remain unqualified. The new fixed-non-cog
continuous capacity bound is 19 (18 first sheet, one last), inconclusive for 15.
Next construct and audit a changed cog-only pool against those exact 51 non-cogs;
do not retry the expired all-small model or capped lists. Original requirements,
source, accurate READMEs and release assets remain; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'CI_status':ci['status'],'best_parts':64,'gain_mm2':gain})
if __name__=='__main__':main()
