"""Seal both changed frame completions and the next wider pooled comparison."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-frame-compound-limits-20261023';OUT=ROOT/'benchmarks/results'/NAME
TALL=ROOT/'output/h5-tall-small-compound-contacts-20261023';MIXED=ROOT/'output/h5-mixed-small-compound-contacts-20261023'
CORE=ROOT/'output/h5-mixed-frame-cog-subassembly-20261023';COVER=ROOT/'output/h5-latest-wide-pool-coverage-20261023';FAIL=ROOT/'output/h5-tall-small-compound-preflight-failure-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();records=[]
    for kind,base in [('tall',TALL),('mixed',MIXED)]:
        gen=load(base/'result.json');audit=load(base/'audit/checks.json');red=load(base/'reduced/checks.json');hint=load(base/'hints/checks.json');model=load(base/'solve/model-audit.json');solved=load(base/'solve/result.json');layouts=load(base/'layout-audit/checks.json')
        assert all(x['passed'] for x in [audit,red,hint,model,layouts]) and gen['completed_queries']==gen['planned_queries']==308 and not gen['pending_queries']
        assert solved['status']=='OPTIMAL' and solved['objective']==solved['best_bound']<model['full_score']==895800000
        assert hint['completed_cases']==20 and not hint['pending_cases'] and not layouts['full_target_witness']
        best=max(layouts['records'],key=lambda r:(r['filled_area_mm2'],str(r['incumbent'])=='final'))
        assert best['filled_area_mm2']<4381940.784069743
        records.append({'kind':kind,'generation':gen,'graph':audit,'reduction':red,'hints':hint,'model':model,'solver':solved,'layouts':layouts,'best':best})
        copies=[('plan.json','plan.json'),('result.json','generation.json'),('audit/checks.json','graph-audit.json'),('reduced/checks.json','reduction-audit.json'),('hints/checks.json','hint-audit.json'),('solve/model-audit.json','model-audit.json'),('solve/result.json','solver-result.json'),('layout-audit/checks.json','layout-audit.json'),(f"layout-audit/layout-{best['incumbent']}.json",'partial-layout.json'),(f"layout-audit/public-{best['incumbent']}.json",'partial-public.json'),('partial-layout.png','partial-layout.png')]
        for source,name in copies:shutil.copyfile(base/source,OUT/f'{kind}-{name}')
    tall,mixed=records;coverage=load(COVER/'checks.json');core=load(CORE/'checks.json')
    assert coverage['passed'] and core['passed'] and coverage['additional_candidates']==8914 and coverage['retained_candidates']==21468
    assert core['component_counts']==[9,1,5] and core['original_geometry_pairs']==388
    assert (FAIL/'failure.txt').is_file() and not (FAIL/'plan.json').exists() and "KeyError: 'passed'" in (FAIL/'failure.txt').read_text(encoding='utf-8')
    priorroot=ROOT/'benchmarks/results/h5-two-sheet-cog-progress-20261023';prior=load(priorroot/'source-review.json')
    assert source_digest()==prior['production_digest'] and prior['current_readmes']=={p:digest(ROOT/p) for p in prior['current_readmes']}
    manifestbefore={r['path']:r['sha256'] for r in load(priorroot/'raw-manifest.json')['files']};original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;assert digest(p)==manifestbefore['source-inputs/'+p.relative_to(ROOT).as_posix()]
    for name in ['job.json','conditional-target.json']:assert (original/name).read_bytes()==(ROOT/'output/h5-skeleton-contact-selection-20261020'/name).read_bytes()
    ciold=json.loads(subprocess.check_output(['gh','run','view','39955078136','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT))
    assert ciold['headSha']=='37b671d3763b7804d605ab123a54cfe3c26cfac7' and ciold['conclusion']=='success' and len(ciold['jobs'])==6 and all(j['conclusion']=='success' for j in ciold['jobs'])
    cinew=json.loads(subprocess.check_output(['gh','run','view','39960579594','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert cinew['headSha']=='4592d97ccd03ae9127482b88ec197a864361d5a1'
    write(OUT/'main-ci-37b671d3.json',ciold);write(OUT/'main-ci-4592d97c.json',cinew)
    next_step=('Do not rerun either fixed-core solver, extend their limits, or resume the 81 tall-core or 16 mixed-core pending member lists. Both finite models have a proven optimum below full inventory; no continuous/global impossibility is claimed. Preserve the highest-filled-area 63-part partial and the separate highest-count 64-part partial. The next concrete changed model is output/h5-latest-wide-pool-coverage-20261023/mapping.json: fix only its exact 18 wide frames, and let all cogs, brackets and inserts select together from the 21,468 freshly checked original poses. The source preserves the entire preceding 29,838-pose pool and all 12,554 choices from the earlier dense-wide all-family model. Its 8,914 additional compatible choices include 4,125 brackets, 4,766 inserts and 23 cogs. Both prior partials are mapped by exact identity and their full geometries checked. This is coverage only: declare fresh bounded graph compression, safe same-family substitutions, hint construction and at most one bounded solve before proceeding; audit every original conflict, all residual edges, the projected graph and every model field. Use the higher-area 63-part seed while preserving the 64-part alternative. Do not reuse prior reduced subsets or assume unchanged graph adjacency. Only an original complete 66-part target witness can advance to native margins and a production repair within the original budget; all H5 jobs and both kerfs remain required. H2 retains Artem\'s unchanged gate decision; the 22 reserved vectors stay unopened.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'both_changed_frame_models_finite_optimum_below_full_inventory':True,'previous_best_partials_preserved':True,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(CORE/'plan.json','mixed-core-plan.json'),(CORE/'checks.json','mixed-core-audit.json'),(CORE/'layout.json','mixed-core-layout.json'),(COVER/'plan.json','wide-coverage-plan.json'),(COVER/'checks.json','wide-coverage-audit.json'),(FAIL/'failure.txt','preflight-failure.txt')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [TALL,MIXED,CORE,COVER,FAIL]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        if (root/'plan.json').exists():inputs.update(load(root/'plan.json')['inputs'])
    for base in [TALL,MIXED]:
        for mapping in [load(base/'reduced/plan.json')['inputs'],load(base/'hints/plan.json')['inputs'],load(base/'solve/model-audit.json')['input_hashes']]:
            for name,h in mapping.items():
                if name in inputs:assert inputs[name]==h
                inputs[name]=h
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-dense-insert-gap-20261023',['layout.json','checks.json']),('h5-two-sheet-cog-group-choice-20261023',['layout-audit/layout-final.json','layout-audit/checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helpernames=['prepare_h5_tall_small_selection.py','prepare_h5_mixed_frame_core.py','prepare_h5_mixed_small_selection.py','check_h5_mixed_frame_cog_subassembly.py','audit_h5_latest_wide_pool_coverage.py','plot_h5_frame_compound_comparison.py','plot_h5_dense_insert_gap.py','ccd1.py']
    helpernames += [prefix+'_h5_'+kind+'_small_compound_'+suffix+'.py' for kind in ['tall','mixed'] for prefix,suffix in [('build','contacts'),('audit','contacts'),('reduce','contacts'),('seed','contacts'),('solve','contacts'),('audit','layouts')]]
    pending=[ROOT/'output'/n for n in helpernames];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'original_inputs_match_previous_manifest':True,'failed_preflight_preserved_no_search_started':True,'both_original_graphs_reductions_models_layouts_pass':True,'total_original_layout_checks':sum(r['layouts']['layouts_checked_including_hint'] for r in records),'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: alternate frame arrangements and actual compound contacts — 2026-10-23

**Neither changed frame arrangement improves the saved partial layouts.** Both
finite candidate models reach a proven optimum below the original 66-part job.
The 63-part layout still has the highest retained filled area; the separate
64-part layout still has the highest part count. H2/H5 remain open at **60%**.

## Construction and limits

The tall construction fixes the checked four frame columns (4/4/5/5) with cogs
split 8+4+3. A separate mixed construction fixes three columns of six frames,
two unturned and one quarter-turned, with cogs split 9+1+5. The mixed core passes
388 original same-sheet pairs, all stock and transform checks, and a frozen CLI
check whose only failures are the absent brackets/inserts. Historical mixed
frame patterns already exist; no first-ever orientation claim is made.

Each completion preserves the preceding complete source pool before fresh
filtering. It queries every bracket orientation/reflection and both insert
classes, plus 36 saved two-to-four-member bracket/insert compounds under four
whole-group rotations, on both sheets. Each of the 308 regions uses the union
of actual member exclusions; compound bounding rectangles only limit stock
translations. Internal compound gaps remain their saved values. Construction
padding applies to the fixed neighbors and stock, and is not native qualification.

The initial tall preparation failed on an absent `passed` field in an older
audit. The corrected reader checks its actual source-hash, transform and pair
fields. The original script and failure are retained separately; no search or
plan had started in that failed folder.

| Checked result | Tall frame core | Mixed frame core |
| --- | ---: | ---: |
| Queries finished | 308/308 | 308/308 |
| Added brackets / inserts | 642 / 1,600 | 103 / 1,600 |
| Retained choices | 4,960 | 3,592 |
| Complete conflicts | 2,454,670 | 883,219 |
| Pending capped member lists | 81 | 16 |
| Choices after certified substitution | 1,347 | 798 |
| Starting layouts checked | 20/20 | 20/20 |
| Solve wall seconds | {tall['solver']['seconds']:.9f} | {mixed['solver']['seconds']:.9f} |
| Finite optimum, original area × 1,000 | 617,000,000 | 495,800,000 |
| Full inventory would require | 895,800,000 | 895,800,000 |
| Best area counts: frames / cogs / brackets / inserts | 18 / 15 / 8 / 15 | 18 / 15 / 2 / 21 |
| Original layouts checked | 11 | 3 |

All regions, events, duplicate records, pending positions, original stock bounds,
allowed transformations and full conflict graphs reconstruct independently.
Tall/mixed audits check 6,173,201 / 6,049,581 same-sheet possibilities and
2,671,478 / 905,511 exact distances. The 36 / 54 cache translations agree within
6.636×10⁻¹³ / 9.113×10⁻¹³ mm; every reconstructed region has zero area difference.
All original cliques cover the complete graph, with no residual edge dropped.

Fresh same-family substitution requires adjacency and a subset of all other
original neighbors. Independent enumeration verifies 3,148,318 / 1,191,757
certificate neighbors and both projected graphs. Each model's every protobuf
field is independently reconstructed. Each makes exactly one call, with a
declared 60-second allowance, eight workers and seed zero. Both finish early
with `OPTIMAL`; neither call is extended or repeated. This proves a limit of
these finite pools with their fixed cores, not unrestricted packing impossibility.

All 14 original layout checks pass geometry and retain only expected quantity
failures from the frozen CLI. The highest-area results in these experiments each
contain 56 pieces: tall fills 4,202,940.784070 mm² and lacks four brackets/six
inserts; mixed fills 4,081,740.784070 mm² and lacks ten brackets. Some lower-area
tall intermediate results contain more pieces; count is not the area objective.
Their minimum gaps are about 0.2002 and 0.2011 mm. Neither is native-qualified.

![Tall-core diagnostic partial]({NAME}/tall-partial-layout.png)
![Mixed-core diagnostic partial]({NAME}/mixed-partial-layout.png)

## Fresh coverage for the next comparison

A read-only coverage audit fixes the 18 wide frames from the better 63-part
layout, then considers every cog/bracket/insert pose in the full 29,838-entry
accumulated pool. All 404,658 fixed-frame comparisons are checked. The earlier
19,834-entry source prefix is unchanged, and all 12,554 earlier all-family
choices remain eligible. The 21,468 eligible choices include **8,914 additions**:
4,125 bracket, 4,766 insert and 23 cog poses. Both best partials map by exact
identity and pass their full original geometries. This is useful coverage;
the new complete mutual conflict graph and selection remain pending.

{next_step}

## Repository, release and evidence

All six checks on main `37b671d3` passed. The queued `356c8523` and `4592d97c`
checkpoints were pushed normally to main, without force. Run `39960579594` for
`4592d97c` is saved as `{cinew['status']}` / `{cinew['conclusion'] or 'pending'}`;
no unobserved completion is inferred. This report's commit will follow the
same policy of allowing the current checks to finish before another push.

Original job, library, request and target hashes match the preceding archive.
Core source and all three READMEs are unchanged. Their current preview wording
remains accurate. These diagnostics do not qualify a new application release;
v0.2.0-alpha.1 and stable v0.1.0 remain as published. No production packing,
full quality run, registry publication or reserved-input evaluation occurs.

Evidence: [tall plan]({NAME}/tall-plan.json), [tall graph]({NAME}/tall-graph-audit.json),
[tall model]({NAME}/tall-model-audit.json), [tall layouts]({NAME}/tall-layout-audit.json),
[mixed plan]({NAME}/mixed-plan.json), [mixed graph]({NAME}/mixed-graph-audit.json),
[mixed model]({NAME}/mixed-model-audit.json), [mixed layouts]({NAME}/mixed-layout-audit.json),
[mixed core]({NAME}/mixed-core-audit.json), [coverage]({NAME}/wide-coverage-audit.json),
[preflight failure]({NAME}/preflight-failure.txt), [source review]({NAME}/source-review.json),
[raw evidence]({NAME}/raw.zip) and [manifest]({NAME}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 alternate-frame compound limits, 2026-10-23:** [the full audit](../benchmarks/results/{NAME}.md)
checks actual-outline bracket/insert compounds around the tall 8+4+3 and mixed
9+1+5 cog cores. Both fresh finite models reach optimal area below full inventory;
neither improves the saved 63-part area or 64-part count partials. All 616 queries,
3,337,889 conflicts, fresh reductions, model fields and 14 original layouts are
checked; only expected missing quantities fail. The original preflight reader
failure and 97 capped lists remain preserved. A new coverage audit retains every
earlier all-family choice plus 8,914 compatible additions around the 18 wide
frames. Next build its complete graph and select cogs/brackets/inserts together
under fresh limits, preserving both checked seeds. All six checks passed on
37b671d3, then queued checkpoints were pushed to main 4592d97c; its checks are
recorded separately. Source, accurate READMEs and releases remain unchanged.
H2/H5 stay open at 60%; no reserved files or production quality runs are used.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'layouts_checked':14,'next_compatible_additions':8914,'main_CI_status':cinew['status']},flush=True)
if __name__=='__main__':main()
