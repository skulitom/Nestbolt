"""Publish the changed construction and reconciliation with exact evidence bytes."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
RUN=ROOT/'output/h5-group-choice-20261023'
REFRESH=ROOT/'output/h5-group-choice-20261023-refresh'
NAME='h5-group-choice-20261023'
OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,obj):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,indent=2);f.write('\n')
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
def main():
    OUT.mkdir();gen=load(RUN/'generation.json');graph=load(RUN/'graph-audit/checks.json');model=load(RUN/'solve/model-audit.json')
    result=load(RUN/'solve/result.json');audit=load(RUN/'layout-audit/checks.json');refresh=load(REFRESH/'checks.json')
    assert graph['passed'] and model['passed'] and audit['passed']
    assert result['status']=='FEASIBLE' and result['incumbents']==3 and 60<=result['seconds']<62
    assert audit['all_returned_layouts_checked']==4 and audit['fresh_frozen_CLI_calls']==4 and not audit['full_target_witness']
    assert audit['best']['counts']=={'frame':18,'insert':19,'cog':13,'bracket':12}
    assert audit['best']['missing']=={'cog':2,'insert':2} and result['best_bound']==model['full_score']
    assert gen['retained_small_poses']==5302 and gen['edges']==1173136
    assert source_digest()==refresh['production_digest']=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    assert refresh['readmes']=={p:digest(ROOT/p) for p in refresh['readmes']}
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT).decode().split()[0]
    assert head==remote==refresh['merged_head']
    ci=json.loads(subprocess.check_output(['gh','run','view','39940832610','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==head
    write(OUT/'main-ci-44ff9cc4.json',ci)
    next_step=('Do not retry the expired group-choice model unchanged. Inspect the saved 62-part geometry and its free regions to identify '
       'the obstruction for the two missing cogs and two missing inserts, then construct changed contacts with coordinated small-part moves. '
       'Before fixing additional parts, check that the resulting conditional free space has enough capacity. Declare finite generation and solver limits, '
       'retain the 62-part seed and every result, and independently recompute all changed conflicts. Native construction margins and an original 66-copy '
       'witness are still required before a quality pilot; retain all original H5 savings/material and full-scope requirements. H2 stays open under Artem’s decision.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':remote,
      'production_digest':source_digest(),'current_readmes':refresh['readmes'],'README_change_needed':False,
      'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
      'completion_percent':60,'H2_complete':False,'H5_complete':False,'next_investigation':next_step,
      'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
      'current_main_CI_status':ci['status'],'current_main_CI_conclusion':ci['conclusion']}
    write(OUT/'source-review.json',review)
    for p,name in [(RUN/'generation.json','generation.json'),(RUN/'graph-audit/checks.json','graph-audit.json'),
                   (RUN/'solve/model-audit.json','model-audit.json'),(RUN/'solve/result.json','solver-result.json'),
                   (RUN/'layout-audit/checks.json','layout-audit.json'),(REFRESH/'checks.json','reconciliation.json')]:shutil.copyfile(p,OUT/name)
    members={};inputs=load(RUN/'plan.json')['inputs']
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    # Preserve the exact original CLI inputs and seed geometry used by the independent audit.
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),
                         ('h5-skeleton-contact-selection-20261020',['audit/layout-0.json','audit/public-0.json','audit/command-0.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for root in [RUN,REFRESH,ROOT/'output/h5-group-choice-sealing-failure-20261023']:
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['build_h5_group_choice.py','audit_h5_group_choice_graph.py','solve_h5_group_choice.py',
       'audit_h5_group_choice_layouts.py','refresh_h5_release_20261023.py','ccd1.py']];visited=set()
    while pending:
        p=pending.pop()
        if p in visited:continue
        visited.add(p);members['helpers/'+p.name]=p
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
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'all_graph_and_model_checks_pass':True,
       'all_returned_layouts_checked':4,'original_CLI_calls':4,'missing_original_copies':4,'full_target_witness':False,
       'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,
       'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    table='\n'.join(f"| {r['incumbent']} | {r['counts']['bracket']} | {r['counts']['cog']} | {r['counts']['insert']} | {r['filled_area_mm2']:,.6f} | {r['material_mm2']:,.6f} |" for r in audit['records'])
    ci_note=('All six checks on merge 44ff9cc4 pass.' if ci['conclusion']=='success' else 'Checks on merge 44ff9cc4 are still running in the saved snapshot; a complete pass is not inferred.')
    report=f'''# H5: joint frame-group and small-part selection — 2026-10-23

**A new 62-part partial places more filled area within the original material allowance,
but still lacks two cogs and two inserts.** All 18 frames and 12 brackets are present.
H2/H5 remain open and completed milestone weight stays 60%. No product code changes
or new release are qualified by this experiment.

## Repository and release refresh

Incoming main `e9046d53` adds the comparison index and metadata. Merge `44ff9cc4`
preserves all six incoming files and all 30 local evidence/doc files from the two
previous unpushed checkpoints, byte for byte. Both raw archives (466 and 362
members) pass SHA and CRC checks again. The merge is pushed to main. The previous
7c47f498 checks, incoming e9046d53 checks and its Pages deployment all pass.
{ci_note}

Core source and all three READMEs retain their reviewed hashes. The existing
README accurately identifies the v0.2.0-alpha.1 preview, stable v0.1.0, hosted
preview from main, 60% milestone completion and incomplete import/material gates.
No README revision or another application release is justified by these offline
diagnostics. Artem’s release authorization remains recorded; no registry is published.

The [current Studio README](https://github.com/JeroenGar/sparrow-studio/blob/{refresh['studio_head']}/README.md)
identifies its new app as unpublished. The [published app description](https://sparrowstudio.app/)
still states strip packing without multiple fixed sheets or part-in-hole.
The October 21 upstream commit changes its API specification; these sources do
not trigger the plan’s shipped-feature stop rule. Read-only source snapshots are
preserved. H2 retains Artem’s original-denominator decision; no reserved input is evaluated.

## Changed construction

The earlier [whole-group tests](h5-whole-group-diagnosis-20261020.md) fixed both
frames and cogs. This model jointly chooses one of all 26 audited complete
18-frame groups and all three small-part families. It starts from the whole
11,319-pose source pool, including 900 later bracket and 900 later insert contacts,
with every original cog choice restored. It creates no new coordinates.

Filtering only for compatibility with at least one frame group retains 5,302
small poses: 1,579 bracket, 1,393 insert and 2,330 cog. The graph is recomputed from
original filled outlines, without reusing conflicts conditional on fixed cogs.
Generation completes in {gen['seconds']:.9f} seconds; all 1,173,136 edges fit into
8,779 checked cliques before the 30-second compression limit, with no residual edges.

An independent full-pair audit checks 743,589 frame/small pairs, 3,978 within-group
frame pairs and 8,715,150 small-pair possibilities. Bounding-box lower bounds
avoid unnecessary exact distances; all 1,375,283 remaining distances and complete
clique edge coverage agree. Every retained transform, stock bound and quantity
in the complete 58-part starting hint passes. All 4,576 possible small-family count
combinations have the same ordering under original filled areas and the model’s
integer area weights. The complete protobuf model, including group implications,
family caps, objective, area floor and full hint, is independently reconstructed.

## One bounded search and all returned layouts

One 60-second call, eight offline workers and seed 0 ends `FEASIBLE` after
{result['seconds']:.9f} seconds. Three callbacks and a different final placement
all use frame group 2. The reported upper bound still permits the full inventory;
this is neither an optimum nor a finite-pool infeasibility certificate. The
expired search is not extended or restarted.

Every layout below has 18 original frames. Areas are mm².

| Return | Brackets | Cogs | Inserts | Filled area | Charged material |
| --- | ---: | ---: | ---: | ---: | ---: |
{table}

The best partial has 4,342,015.346194 mm² of filled area, 18,674.562124 more than
its 58-part seed and 10,462.718938 more than the earlier 63-part partial recorded in
[the prior comparison](h5-coordinated-contact-selection-20261020.md). It places
62 rather than 63 copies and uses 3,786.903495 mm² more charged material than its
58-part seed, reaching the original 4,988,890.353495 mm² allowance exactly. This is
progress in filled area within the allowance, not complete-job material evidence.

All four returns pass independent original geometry, clearance, rotations and
stock checks. All four fresh calls to the hash-pinned original CLI fail **only**
their missing-copy quantities; the final two lack two cogs and two inserts each.
Minimum clearance for those two is 0.201 mm, and their target material has no
remaining headroom. Native construction margins are not qualified. No search
engine integration, native packing, quality rerun or held-out evaluation occurs.

## Preserved packaging correction

The first evidence sealer wrote a valid ZIP but looked up one archive member
using Windows backslashes; ZIP normalized its name to forward slashes. That
verification stopped with a missing-member KeyError. The failed helper, its raw
archive and partial output files are preserved together. The repaired sealer
uses normalized archive paths and verifies every member hash and CRC. No model,
search, geometry audit or CLI call is repeated for this packaging correction.

## Next investigation

{next_step}

Evidence: [reconciliation]({NAME}/reconciliation.json), [graph audit]({NAME}/graph-audit.json),
[model audit]({NAME}/model-audit.json), [solver result]({NAME}/solver-result.json),
[all-layout audit]({NAME}/layout-audit.json), [source review]({NAME}/source-review.json),
[raw inputs, graphs, models, outputs and upstream snapshots]({NAME}/raw.zip),
and [verified manifest]({NAME}/raw-manifest.json). All {len(manifest)} archive members,
CRCs and byte hashes verify.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 joint frame-group selection, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
chooses among 26 complete frame groups while all bracket, cog and insert poses
remain free. A recomputed 5,302-pose graph and complete model pass independent
checks. One 60-second search returns a 62-part partial: all 18 frames and 12
brackets, 13 cogs and 19 inserts. Filled area reaches 4,342,015.346194 mm² within
the original material allowance, but two cogs and two inserts remain missing.
All four returned layouts pass original geometry and retain quantity-only CLI
failures. The final bound is unresolved; no optimum or full-job pass is claimed.
Next diagnose free regions and construct changed contacts, preserving the new
seed; do not repeat the expired model. Incoming e9046d53’s comparison index and
both pending evidence commits are merged and pushed as 44ff9cc4. Its checks are
recorded separately. Core source and all three READMEs remain unchanged; the
published preview is still accurate and no new release is qualified. H2/H5
remain open at 60%, with original gates and held-out isolation preserved.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    status=ROOT/'docs/STATUS.md';text=status.read_text(encoding='utf-8');assert text.startswith('# Status — 2026-10-20')
    status.write_text(text.replace('# Status — 2026-10-20','# Status — 2026-10-23',1),encoding='utf-8',newline='\n')
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print(json.dumps({'report':str(OUT.parent/(NAME+'.md')),'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'checks':True,'main_CI':ci['status']}))
if __name__=='__main__':main()
