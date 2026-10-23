"""Seal one new conditional repair solve without promoting a partial layout to H5 acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-one-cog-release-joint-20261023';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME;COVER=ROOT/'output/h5-one-cog-release-coverage-20261023'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    data={k:load(BASE/v) for k,v in [('graph','audit/checks.json'),('reduction','reduced/checks.json'),('hints','hints/checks.json'),('encoding','solve/encoding-audit.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json')]}
    assert all(data[k]['passed'] for k in ['graph','reduction','hints','encoding','model','layouts'])
    g,r,h,e,m,s,l=[data[k] for k in ['graph','reduction','hints','encoding','model','solver','layouts']]
    assert m['seed_score']==865862719 and m['full_score']==945862719 and m['cp_model_presolve'] is False and s['status']=='FEASIBLE' and not l['full_target_witness']
    nextstep=load(BASE/'next-step.json');assert nextstep['full_target_witness']==l['full_target_witness']
    priorroot=ROOT/'benchmarks/results/h5-individual-frame-joint-20261023';prior=load(priorroot/'source-review.json');assert source_digest()==prior['production_digest'] and {p:digest(ROOT/p) for p in prior['current_readmes']}==prior['current_readmes']
    previous=load(priorroot/'raw-manifest.json');hashes={v['path']:v['sha256'] for v in previous['files']+previous['aliases']}
    for p in COVER.rglob('*'):
        if p.is_file():assert digest(p)==hashes[COVER.name+'/'+p.relative_to(COVER).as_posix()]
    original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;assert digest(p)==hashes['source-inputs/'+p.relative_to(ROOT).as_posix()]
    OUT.mkdir()
    for k,v in data.items():write(OUT/(k+'.json'),v)
    for p,name in [(BASE/'plan.json','plan.json'),(BASE/'reduced/plan.json','reduction-plan.json'),(BASE/'hints/plan.json','hint-plan.json'),(BASE/'next-step.json','next-step.json'),(COVER/'checks.json','core-coverage.json')]:shutil.copyfile(p,OUT/name)
    best=max(l['records'],key=lambda v:v['filled_area_mm2'])
    for stem in ['layout','public']:
        shutil.copyfile(BASE/f"layout-audit/{stem}-{best['incumbent']}.json",OUT/f'best-{stem}.json')
        shutil.copyfile(BASE/f'layout-audit/{stem}-final.json',OUT/f'final-{stem}.json')
    ci=json.loads(subprocess.check_output(['gh','run','view','39976658315','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']=='752b1c60e38adfaa554d9220382177b935eabf72';write(OUT/'main-ci-752b1c60.json',ci)
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'main_head':subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'best_checked_parts':sum(best['counts'].values()),'best_checked_missing':best['missing'],'full_target_witness':False,'native_margin_qualified':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':nextstep['action']};write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [BASE,COVER]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('*.json'):
            if p.name not in ['plan.json','model-audit.json']:continue
            value=load(p)
            for name,hsh in value.get('inputs',value.get('input_hashes',{})).items():
                if name in inputs:assert inputs[name]==hsh
                inputs[name]=hsh
    for name,hsh in inputs.items():
        p=ROOT/name;assert digest(p)==hsh;members['source-inputs/'+name.replace('\\','/')]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-expanded-frame-joint-20261023',['mapping.json','layout-audit/layout-hint.json','layout-audit/public-hint.json','layout-audit/command-hint.json']),('h5-individual-frame-bracket-gaps-20261023',['checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/name for name in ['build_h5_one_cog_release_joint.py','prepare_h5_one_cog_release_selection.py','reduce_h5_one_cog_release_joint.py','seed_h5_one_cog_release_joint.py','solve_h5_one_cog_release_joint.py','audit_h5_one_cog_release_layouts.py','audit_h5_one_cog_release_coverage.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            modules=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [v.name.split('.')[0] for v in node.names] if isinstance(node,ast.Import) else [])
            for module in modules:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    checks={'passed':True,'all_core_coverage_bytes_match_committed_manifest':True,'all_original_inputs_match_previous_manifest':True,'all_input_hashes_verified':True,'every_projected_and_reduced_conflict_verified':True,'all_30_mapped_baselines_preserved':True,'model_and_parameters_independently_reconstructed':True,'all_original_layouts_checked':l['layouts_checked_including_hint'],'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    links=', '.join(f"[part {i}]({NAME}/{v['path']})" for i,v in enumerate(manifest['archives'],1))
    report=f'''# H5: one-cog release with all brackets and inserts — 2026-10-23

**Best checked result remains 64/66, missing two brackets.** A distinct
conditional repair model frees one cog together with every bracket and insert.
It returns `{s['status']}` with its original 60-second allowance. It neither
improves the checked layout nor proves the finite pool optimal. The original
66-copy inventory and material target remain unchanged; H2/H5 stay open at
**60%** completed milestone weight.

## New repair model and independent checks

The preceding [coverage audit](h5-individual-frame-joint-20261023.md) supplies
30 cores from two checked layouts: each fixes 18 frames and 14 cogs. Every
core pair and all 989,670 candidate/core memberships were independently checked.
All coverage bytes match that committed manifest. The new model chooses
exactly one core and up to 12 brackets, 21 inserts and one additional cog.
A zero-cog choice remains permitted if it reaches the area floor. Original
reserved frame holes, transforms, stock limits and quantities are unchanged.

All **16,058** eligible variable poses are retained before fresh reduction.
The complete original graph is projected into this neighborhood, with every
projected row reconstructed back to original global indices. All
**{g['projected_conflicts']:,}** conflicts agree. Projection, serialization and
independent row verification take {g['seconds']:.6f} seconds. All 30 original
64-part baselines preserve full-graph feasibility. The 572 variable count
combinations are a subset of the previously verified original-area ordering;
the variable floor is **865,862,719**, and full inventory requires
**945,862,719**.

Fresh same-family substitutions require an adjacent retained replacement,
inclusion of every original neighbor and a superset of compatible cores.
The pass completes in {r['seconds']:.6f} seconds and {r['comparisons']:,}
comparisons within its 30-second / 50-million limits. It removes
{r['removed_candidates']:,} choices and retains **{r['kept_candidates']:,}**.
Independent certificates enumerate {r['certificate_neighbors_independently_verified']:,}
neighbor relationships and {r['compatible_group_memberships_independently_certified']:,}
core memberships. Every mapped baseline preserves quantities and score.

The reduced graph has **{r['induced_edges']:,}** conflicts. First-fit compression
completes in {r['compression_seconds']:.6f} seconds within its 20-second allowance,
yielding {r['compressed_cliques']:,} cliques and **{r['residual_edges']}** residual
edges. Every edge reconstructs independently. There is no extra greedy search;
all 30 mapped baselines are checked, and the first best baseline is the hint.

The final graph encoding, every binary model field and all solver parameters
are independently reconstructed. The model has **{m['variables']:,}** variables
({m['variable_poses']:,} poses and {m['core_choices']} core choices), with
**{m['constraints']:,}** constraints. Original family caps, conditional core
membership and the area floor are explicit. One seed-zero, eight-worker call
uses a 60-second allowance and disabled CP model presolve, following the
previous recorded diagnosis. It runs for **{s['seconds']:.6f} wall seconds**;
the soft overrun is preserved. Search starts at 0.34 seconds, after recovering
the baseline at 0.268763 seconds. The complete worker log records active
search; zero aggregate counters do not mean search was absent.

There is one callback and a distinct final result, selecting core 7. Both
return variable area 865,862,719; the reported upper bound remains 945,862,719.
This is **not an optimality or impossibility certificate**. This completed
solve is not repeated or extended.

## Original geometry and gate status

All {l['layouts_checked_including_hint']} layouts, including the starting hint,
pass independent original geometry, transform, stock and pair checks. Each
contains 18 frames, 15 cogs, 10 brackets and 21 inserts. Every layout checks
1,521 same-sheet pairs. The frozen CLI is run {l['fresh_frozen_CLI_calls']} times,
with {l['exact_CLI_results_reused']} exact-layout reuse; each result fails only
the original two-bracket quantity requirement. Filled area is
{best['filled_area_mm2']:.9f} mm², charged material is
{best['material_mm2']:.9f} mm², and minimum separation is
{best['minimum_distance_mm']:.12f} mm. These gaps are not native-margin qualified.

No native packing, production-budget qualification, complete H5 quality matrix
or held-out evaluation occurs. The full original target, native guard,
production budget and all 13 jobs at both kerfs remain required. This evidence
does not add a completed milestone or qualify a new release. Source and all
three accurate READMEs remain unchanged; preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain current.

## Next action and repository state

{nextstep['action']}

Main remains 752b1c60 after a fresh fetch with no incoming changes. Its six-job
run 39976658315 is saved as `{ci['status']}` / `{ci['conclusion'] or 'pending'}`.
The preceding d49d0ff6 evidence checkpoint is committed locally; pushing later
checkpoints waits for the remaining main check. No unobserved success is claimed.

Evidence: [projection]({NAME}/graph.json), [reduction]({NAME}/reduction.json),
[baselines]({NAME}/hints.json), [encoding]({NAME}/encoding.json),
[model]({NAME}/model.json), [solver]({NAME}/solver.json),
[original layouts]({NAME}/layouts.json), [best checked layout]({NAME}/best-layout.json),
[distinct final layout]({NAME}/final-layout.json), [source review]({NAME}/source-review.json),
raw evidence {links}, and [manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']} canonical members and {archive['verified_aliases']}
aliases are byte-verified, with archive CRCs and SHA-256 hashes checked. Each
independent ZIP part is below 50 MiB, and every original path remains represented.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 one-cog repair selection, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
selects one of 30 checked 18-frame/14-cog cores and jointly relocates a cog,
all brackets and all inserts. Every original conflict, core membership,
substitution, model field and parameter is verified. Fresh reduction completes
at 6,641 variable poses; complete first-fit compression preserves all 4,686,314
reduced conflicts with no residual edges. One 60-second solve reaches search
and returns `FEASIBLE`; all three original layouts remain 64/66, missing two
brackets. The full bound is unresolved. No native or production qualification
is inferred. Main 752b1c60 awaits its last Windows check, with d49d0ff6 committed
locally. Source, READMEs and releases remain unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
