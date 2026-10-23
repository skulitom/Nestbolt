"""Seal the unrestricted-within-pool four-family construction and original checks."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-individual-frame-joint-20261023';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME;COVER=ROOT/'output/h5-all-pose-coverage-20261023'
GAP=ROOT/'output/h5-individual-frame-bracket-gaps-20261023';REPAIR=ROOT/'output/h5-one-cog-release-coverage-20261023'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    data={name:load(BASE/path) for name,path in [('graph','result.json'),('audit','audit/checks.json'),('reduction','reduced/checks.json'),('hints','hints/checks.json'),('encoding','solve/encoding-audit.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json')]}
    assert all(data[k]['passed'] for k in ['audit','reduction','hints','encoding','model','layouts'])
    assert data['model']['seed_score']>=4401740785 and data['model']['full_score']==4481740785 and data['model']['cp_model_presolve'] is False
    assert data['solver']['status'] in ['FEASIBLE','OPTIMAL','UNKNOWN']
    gap=load(GAP/'checks.json');repair=load(REPAIR/'checks.json');comparison=load(REPAIR/'seed-comparison.json')
    assert gap['passed'] and gap['queries_completed']==16 and gap['empty_regions']==16 and gap['pending_queries']==0 and not gap['full_target_witness']
    assert repair['passed'] and repair['distinct_fixed_cores']==30 and repair['mapped_complete_64_seeds']==30 and repair['fixed_poses_explicitly_excluded_from_variables']
    assert all(r['nearest_matches_form_bijection'] for r in comparison)
    next_step=load(BASE/'next-step.json');assert next_step['full_target_witness']==data['layouts']['full_target_witness']
    priorroot=ROOT/'benchmarks/results/h5-expanded-frame-joint-20261023';prior=load(priorroot/'source-review.json')
    assert source_digest()==prior['production_digest'] and {p:digest(ROOT/p) for p in prior['current_readmes']}==prior['current_readmes']
    previous=load(priorroot/'raw-manifest.json');hashes={r['path']:r['sha256'] for r in previous['files']+previous['aliases']};original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;assert digest(p)==hashes['source-inputs/'+p.relative_to(ROOT).as_posix()]
    OUT.mkdir()
    for name,value in data.items():write(OUT/f'{name}.json',value)
    for source,name in [(BASE/'plan.json','plan.json'),(BASE/'reduced/plan.json','reduction-plan.json'),(BASE/'hints/plan.json','hint-plan.json'),(BASE/'next-step.json','next-step.json'),(COVER/'checks.json','source-coverage.json')]:shutil.copyfile(source,OUT/name)
    for root,prefix in [(GAP,'bracket-gap'),(REPAIR,'one-cog-coverage')]:
        for name in ['plan.json','checks.json']:shutil.copyfile(root/name,OUT/(prefix+'-'+name))
    shutil.copyfile(REPAIR/'seed-comparison.json',OUT/'seed-comparison.json')
    best=max(data['layouts']['records'],key=lambda r:r['filled_area_mm2']);index=best['incumbent']
    for stem in ['layout','public']:shutil.copyfile(BASE/f'layout-audit/{stem}-{index}.json',OUT/f'best-{stem}.json')
    for stem in ['layout','public']:shutil.copyfile(BASE/f'layout-audit/{stem}-final.json',OUT/f'alternate-final-{stem}.json')
    cis=[]
    for run,head in [('39969515541','955cc87eb3c5910e5b575f519676b44197fe3492'),('39976658315','752b1c60e38adfaa554d9220382177b935eabf72')]:
        ci=json.loads(subprocess.check_output(['gh','run','view',run,'--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==head;write(OUT/f'main-ci-{head[:8]}.json',ci);cis.append(ci)
    assert cis[0]['conclusion']=='success' and len(cis[0]['jobs'])==6 and all(j['conclusion']=='success' for j in cis[0]['jobs'])
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'best_checked_parts':sum(best['counts'].values()),'best_checked_missing':best['missing'],'best_checked_filled_area_mm2':best['filled_area_mm2'],'full_target_witness':data['layouts']['full_target_witness'],'native_margin_qualified':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step['action']}
    write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [BASE,COVER,GAP,REPAIR]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('*.json'):
            if p.name not in ['plan.json','model-audit.json']:continue
            v=load(p)
            for name,h in v.get('inputs',v.get('input_hashes',{})).items():
                if name in inputs:assert inputs[name]==h
                inputs[name]=h
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name.replace('\\','/')]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-expanded-frame-joint-20261023',['mapping.json','layout-audit/layout-hint.json','layout-audit/public-hint.json','layout-audit/command-hint.json']),('h5-expanded-frame-direct-search-20261023',['parameter-delta-audit.json','solve/result.json','layout-audit/layout-final.json','layout-audit/public-final.json','layout-audit/command-final.json','layout-audit/checks.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/name for name in ['build_h5_individual_frame_joint.py','audit_h5_individual_frame_joint.py','reduce_h5_individual_frame_joint.py','seed_h5_individual_frame_joint.py','solve_h5_individual_frame_joint.py','audit_h5_individual_frame_layouts.py','prepare_h5_individual_frame_selection.py','prepare_h5_individual_frame_layout_audit.py','prepare_h5_individual_frame_bracket_gaps.py','check_h5_individual_frame_bracket_gaps.py','audit_h5_one_cog_release_coverage.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            modules=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [n.name.split('.')[0] for n in node.names] if isinstance(node,ast.Import) else [])
            for module in modules:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    checks={'passed':True,'all_original_inputs_match_previous_manifest':True,'all_input_hashes_verified':True,'complete_four_family_graph_and_induced_encoding_verified':True,'model_and_parameters_independently_reconstructed':True,'all_original_layouts_checked':data['layouts']['layouts_checked_including_hint'],'all_16_conservative_bracket_queries_completed_empty':True,'all_30_one_cog_release_cores_and_memberships_verified':True,'seed_geometry_comparison_verified':True,'one_cog_group_model_pending':True,'full_target_witness':data['layouts']['full_target_witness'],'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,**archive}
    write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    g,a,r,h,e,m,s,l=[data[k] for k in ['graph','audit','reduction','hints','encoding','model','solver','layouts']]
    archive_links=', '.join(f"[part {i}]({NAME}/{v['path']})" for i,v in enumerate(manifest['archives'],1))
    report=f'''# H5: individual frames and all small families — 2026-10-23

**Best checked result: {sum(best['counts'].values())}/66 original parts, missing
{json.dumps(best['missing'],sort_keys=True)}.** One new bounded model frees every
original frame pose individually while selecting cogs, brackets and inserts
together. The original target and full inventory are unchanged. It returns
`{s['status']}`; full original target witness: `{l['full_target_witness']}`.
Native margins, production-budget qualification and the complete H5 matrix
remain required. H2/H5 remain open at **60%** completed milestone weight.

## Changed scope and independent geometry

The prior model selected one of 29 complete frame groups. This model removes
that construction restriction and retains all **35,488** independently checked
source poses: 2,499 frames, 12,317 brackets, 13,968 inserts and 6,704 cogs.
It adds 2,358 individual frame choices and 3,358 small choices relative to the
previous group model. Both original 64-part layouts map exactly by pose identity.
No new geometry is generated. All original reserved frame holes remain filled
for spacing checks; the 22 reserved evaluation vectors are not opened.

The fresh graph checks all family pair types, including frame/frame and
frame/small edges absent from the earlier group-filtered graph. Construction
takes {g['graph_seconds']:.6f} seconds and checks {g['bounds_candidates_exactly_checked']:,}
expanded-bound pairs. An independent sequential bounds scan covers
{a['small_and_frame_pair_possibilities']:,} same-sheet possibilities and
{a['exact_pair_distances']:,} exact distances. Both methods agree on all
**{g['conflicts']:,} edges** and every binary adjacency row. All 35,488 original
poses reconstruct directly from source vertices with zero distance and area
error; stock bounds, permitted rotations and mirror flags pass. Both seeds'
3,042 same-sheet pairs pass independently.

All 86,944 original four-family count combinations preserve true filled-area
ordering under the integer objective. The seed floor is **4,401,740,785** and
full inventory requires **4,481,740,785**. Even all other families plus 17 frames
reach only **4,324,240,785**, so exactly 18 frames is already implied by the
original floor. The explicit frame equality strengthens propagation without
excluding any qualifying count combination. Original job, library, request,
target and family caps remain unchanged.

## Fresh reduction and bounded selection

The new same-family substitution pass performs {r['comparisons']:,} comparisons
in {r['seconds']:.6f} seconds, with its original 30-second / 50-million limits;
limit reached: `{r['limit_reached']}`. It retains {r['kept_candidates']:,} choices
and removes {r['removed_candidates']:,} only with original neighbor inclusion
and a retained adjacent replacement. Independent certificates enumerate
{r['certificate_neighbors_independently_verified']:,} neighbor relationships.
Both complete 64-part counts and area scores survive mapping. Every unprocessed
choice remains; no earlier reduction or capped list is resumed.

The exact induced graph has {r['induced_edges']:,} conflicts. A fresh 20-second
first-fit cover yields {r['compressed_cliques']:,} cliques and retains every
one of {r['residual_edges']:,} residual edges. Full graph reconstruction passes.
The hint pass completes {h['completed_cases']:,}/1,960 new four-family relocation
starts in its 30-second allowance, retaining {h['pending_cases']:,} pending
cases. Each completed case passes full-graph, count and objective checks; the
original score floor remains feasible.

Every model and parameter field is independently reconstructed. Larger cliques
and {e['implication_rows']:,} aggregated residual implications retain every edge.
The final model has {m['variables']:,} variables and {m['constraints']:,}
constraints, no frame-group restriction, and explicit original family caps.
One eight-worker, seed-zero call has a **60-second allowance**, with CP model
presolve disabled as motivated by the preceding recorded diagnosis. It returns
`{s['status']}` after **{s['seconds']:.6f} wall seconds**, with {s['incumbents']}
callbacks and reported bound {s['best_bound']}. Every soft overrun and full log
is preserved. This model is not repeated or extended.

All {l['layouts_checked_including_hint']} original layouts are checked, including
the starting hint and each returned distinct final result. Original filled
outlines, permitted transforms, target stock, all pair distances, quantities
and the frozen CLI are verified: {l['fresh_frozen_CLI_calls']} fresh CLI calls
and {l['exact_CLI_results_reused']} exact-layout reuses. The detailed layout
table retains every missing-quantity violation. The best checked filled area
is {best['filled_area_mm2']:.9f} mm², charged material {best['material_mm2']:.9f}
mm², and minimum separation {best['minimum_distance_mm']:.12f} mm.

Generation, reduction and solve timers are separate from graph serialization,
certificate enumeration and independent audits. These are development
diagnostics, not production-budget or full H5 quality measurements.

## Fixed-layout gap check and a different repair neighborhood

The distinct final layout also has 64 parts and minimum separation
{gap['minimum_distance_mm']:.12f} mm. Its frame poses differ from the original
wide seed by at most {repair['seed_geometry_comparison'][0]['maximum_distance_mm']:.12f}
mm; nearest matching is bijective. The cogs match within
{repair['seed_geometry_comparison'][1]['maximum_distance_mm']:.3g} mm. These are
small placement changes, not evidence of a different packing arrangement.

A fresh conservative insertion check fixes this exact final layout and checks
all 16 bracket rotation/reflection/sheet combinations in
{gap['generation_seconds']:.6f} seconds. Every padded region is empty, with
no pending queries, proposals or added brackets. All original 1,521 pairs pass
and the exact unchanged CLI result is reused. Conservative padding makes this
a failed insertion diagnostic, not an impossibility proof.

The next repair neighborhood releases one cog together with every bracket
and insert. Each of the two exact checked layouts supplies 15 fixed cores,
each with 18 frames and 14 cogs: 30 distinct cores in total. Every fixed-core
pair passes. All {repair['group_memberships_independently_checked']:,} variable/core
memberships agree between the complete original graph and independent
distances to the filled core unions. Fixed poses are explicitly excluded from
variable choices, because graph diagonals are zero. This retains
{repair['eligible_variable_poses']:,} choices: 6,176 brackets, 8,420 inserts and
1,462 cogs. All 30 complete 64-part starting layouts map back exactly.

The variable-area floor is 865,862,719; full quantities require 945,862,719.
The future conditional model must select exactly one core, retain all
compatible choices and conflicts, and cap variable counts at 12 brackets,
21 inserts and one cog. A zero-cog choice must remain allowed when it meets
the area floor. Coverage took {repair['seconds']:.6f} seconds; no conditional
graph reduction or solver call is included yet. The full original 66-copy
requirement, material target and native/production qualifications remain.

## Next action

{next_step['action']}

## Repository and evidence

All six hosted checks pass for main 955cc87e. The queued 752b1c60 checkpoint
was then pushed normally to main; its run 39976658315 is saved as
`{cis[1]['status']}` / `{cis[1]['conclusion'] or 'pending'}`. No unobserved pass
is inferred. Production source and all three READMEs remain unchanged, with
preview v0.2.0-alpha.1 and stable Latest v0.1.0 still accurately described.
No new release, registry publication, held-out evaluation, native packing or
full H5 quality run occurs in this diagnostic checkpoint.

Evidence: [geometry and graph]({NAME}/audit.json), [reduction]({NAME}/reduction.json),
[hints]({NAME}/hints.json), [encoding]({NAME}/encoding.json), [model]({NAME}/model.json),
[solver]({NAME}/solver.json), [original layouts]({NAME}/layouts.json),
[best checked layout]({NAME}/best-layout.json), [original validation]({NAME}/best-public.json),
[distinct final layout]({NAME}/alternate-final-layout.json),
[fixed-layout gaps]({NAME}/bracket-gap-checks.json),
[one-cog coverage]({NAME}/one-cog-coverage-checks.json),
[seed comparison]({NAME}/seed-comparison.json),
[source review]({NAME}/source-review.json), raw evidence {archive_links},
and [manifest]({NAME}/raw-manifest.json). All {archive['archive_members']} canonical
members, {archive['verified_aliases']} aliases, archive CRCs and byte hashes
verify. Complete ZIP parts remain below 50 MiB each; all original paths remain
represented through explicit verified aliases for identical input bytes.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 individual-frame joint selection, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
frees every original frame pose and all three small families across the full
35,488-pose pool. All {g['conflicts']:,} new four-family conflicts, original
transforms/stock bounds and both 64-part seeds are independently checked.
Fresh substitutions and first-fit constraints preserve every induced edge;
all model and parameter fields are verified. One unchanged-allowance solve
returns `{s['status']}`. Best checked inventory: {sum(best['counts'].values())}/66;
missing {json.dumps(best['missing'],sort_keys=True)}. Native and complete H5
qualification remain open. All 16 conservative bracket insertion regions for
the distinct final layout are empty. Thirty fresh repair cores, each freeing
one cog plus all brackets and inserts, preserve both 64-part layouts and all
989,670 independently checked memberships; their conditional selection is
pending. The earlier 752b1c60 checkpoint is pushed after
all six 955cc87e checks pass. Source, accurate READMEs and releases remain
unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
