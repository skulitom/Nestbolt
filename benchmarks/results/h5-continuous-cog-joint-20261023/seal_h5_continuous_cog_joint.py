"""Seal the complete new-contact conditional model and original 64-part outcomes."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-continuous-cog-joint-20261023';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME;REG=ROOT/'output/h5-one-cog-continuous-regions-20261023-v2'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    data={k:load(BASE/v) for k,v in [('graph','result.json'),('audit','audit/checks.json'),('provenance','provenance-audit.json'),('reduction','reduced/checks.json'),('hints','hints/checks.json'),('encoding','solve/encoding-audit.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json'),('retention','retention/checks.json')]}
    assert all(data[k]['passed'] for k in ['audit','provenance','reduction','hints','encoding','model','layouts','retention'])
    g,a,p,r,h,e,m,s,l,t=[data[k] for k in ['graph','audit','provenance','reduction','hints','encoding','model','solver','layouts','retention']]
    assert p['derived_maximum_variable_cogs']==m['derived_cog_clique_requires_original_cog_cap']==1 and m['seed_score']==865862719 and m['full_score']==945862719 and m['cp_model_presolve'] is False
    assert s['status']=='FEASIBLE' and not l['full_target_witness'];nextstep=load(BASE/'next-step.json');assert not nextstep['full_target_witness']
    priorroot=ROOT/'benchmarks/results/h5-one-cog-continuous-regions-20261023';prior=load(priorroot/'source-review.json');assert source_digest()==prior['production_digest'] and {path:digest(ROOT/path) for path in prior['current_readmes']}==prior['current_readmes'];previous=load(priorroot/'raw-manifest.json');hashes={row['path']:row['sha256'] for row in previous['files']+previous['aliases']};original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        path=original/name;assert digest(path)==hashes['source-inputs/'+path.relative_to(ROOT).as_posix()]
    OUT.mkdir()
    for k,v in data.items():write(OUT/(k+'.json'),v)
    for path,name in [(BASE/'plan.json','plan.json'),(BASE/'reduced/plan.json','reduction-plan.json'),(BASE/'hints/plan.json','hint-plan.json'),(BASE/'retention/plan.json','retention-plan.json'),(BASE/'retention/review-cores.json','review-cores.json'),(BASE/'next-step.json','next-step.json'),(REG/'audit/checks.json','source-geometry-audit.json')]:shutil.copyfile(path,OUT/name)
    best=max(l['records'],key=lambda v:v['filled_area_mm2'])
    for stem in ['layout','public']:
        shutil.copyfile(BASE/f"layout-audit/{stem}-{best['incumbent']}.json",OUT/f'best-{stem}.json');shutil.copyfile(BASE/f'layout-audit/{stem}-final.json',OUT/f'final-{stem}.json')
    ci=json.loads(subprocess.check_output(['gh','run','view','39984899040','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']=='facf0f388f865768ab60d7a8549eef67198ae714';write(OUT/'main-ci-facf0f38.json',ci)
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'main_head':subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'best_checked_parts':64,'best_checked_missing':{'bracket':2},'full_target_witness':False,'native_margin_qualified':False,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':nextstep['action']};write(OUT/'source-review.json',review)
    members={};inputs={}
    for path in BASE.rglob('*'):
        if path.is_file():members[BASE.name+'/'+path.relative_to(BASE).as_posix()]=path
    for path in BASE.rglob('*.json'):
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
    pending=[ROOT/'output'/name for name in ['build_h5_continuous_cog_joint.py','audit_h5_continuous_cog_joint.py','audit_h5_continuous_cog_provenance.py','prepare_h5_continuous_cog_selection.py','reduce_h5_continuous_cog_joint.py','seed_h5_continuous_cog_joint.py','solve_h5_continuous_cog_joint.py','audit_h5_continuous_cog_layouts.py','audit_h5_continuous_cog_retention.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
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
    checks={'passed':True,'all_original_inputs_match_previous_manifest':True,'all_input_hashes_verified':True,'reused_inputs_match_committed_evidence':True,'geometric_and_count_derived_conflicts_separately_verified':True,'every_model_and_parameter_field_independently_reconstructed':True,'all_30_original_baselines_preserved':True,'all_returned_original_layouts_checked':True,'retained_new_pose_and_review_core_audits_pass':True,'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    links=', '.join(f"[part {i}]({NAME}/{v['path']})" for i,v in enumerate(manifest['archives'],1))
    report=f'''# H5: joint selection with continuous cog contacts — 2026-10-23

**Best checked result remains 64/66, missing two brackets.** One fresh
conditional model includes all 4,000 verified new cog poses together with the
16,058 old variable choices and the same 30 fixed cores. The 60-second search
returns `{s['status']}` at the original area floor; the full upper bound remains
unresolved. No returned layout uses a new cog pose. This is neither an
optimality proof nor H5 acceptance. H2/H5 remain open at **60%** completed weight.

## Complete constraints and provenance

All 20,058 choices are retained before fresh reduction. Eleven source members
match their committed evidence manifests, including the unchanged unreduced
old graph and independently audited new geometry. Original pool records, core
positions, compatibility and all 30 mapped 64-part baselines remain intact.

The old graph contributes **{g['old_original_geometric_edges']:,} geometric edges**.
A fresh spatial-tree construction adds **{g['new_cog_non_cog_geometric_edges']:,}**
new cog/bracket or cog/insert conflicts. An independent sequential bounds scan
checks {a['new_pose_non_cog_same_sheet_possibilities']:,} same-sheet possibilities
and {a['independent_new_pose_exact_distances']:,} exact distances, finding the
same new conflicts. Construction and serialization take {g['seconds']:.6f}
seconds; the independent graph audit takes {a['seconds']:.6f} seconds.

The original job requires 15 cogs and each of the 30 fixed cores already has
14. The variable cog cap is therefore exactly one. An explicitly declared
complete clique on **5,462** variable cog choices is already implied by that
unchanged count cap. Its **{g['complete_derived_cog_clique_edges']:,}** edges are
count-derived mutual exclusions, including geometrically disjoint and
different-sheet pairs; they are not reported as measured collisions.
Of these, {g['original_old_cog_cog_geometric_edges']:,} old geometric edges
already existed; **{g['additional_derived_cog_edges']:,}** are additional
constraint edges. The total graph has **{g['total_constraint_graph_edges']:,}**
edges, and every row independently reconstructs. Zero variable cogs remain
permitted when the original area floor is met.

## Fresh reduction and bounded search

Same-family substitutions require an adjacent retained replacement, inclusion
of every verified constraint neighbor and a superset of compatible cores.
The pass completes in **{r['seconds']:.6f} seconds** and {r['comparisons']:,}
comparisons within its 30-second / 50-million allowance. It removes
{r['removed_candidates']:,} choices and retains **{r['kept_candidates']:,}**.
Independent certificates enumerate {r['certificate_neighbors_independently_verified']:,}
neighbor relationships and {r['compatible_group_memberships_independently_certified']:,}
core memberships. All 30 baselines keep their counts and area.

The exact induced graph has **{r['induced_edges']:,}** constraint edges.
Compression first records the verified clique on the retained
**{r['seeded_derived_cog_clique_size']}** cogs, then performs first-fit expansion.
It completes in **{r['compression_seconds']:.6f} seconds**, including the seeded
clique, within the 20-second limit. All {r['compressed_cliques']:,} cliques
reconstruct every edge; **no residual edges remain**. No additional greedy
hint search occurs, and no earlier reduction or capped proposal list is resumed.

Every binary model and parameter field independently reconstructs. The model
has **{m['variables']:,}** variables ({m['variable_poses']:,} pose choices and
30 core choices) and **{m['constraints']:,}** constraints. The original variable
area floor is 865,862,719 and full inventory requires 945,862,719. A single
seed-zero, eight-worker solve uses a 60-second allowance with CP model presolve
disabled, as previously diagnosed. It runs for **{s['seconds']:.6f} wall seconds**;
the soft overrun is preserved. The baseline appears at 0.237882 seconds and
search starts at 0.30 seconds. Worker logs record active search, including
1,045,013 branches for the core worker; zero aggregate counters do not mean
there was no search.

One callback and a distinct final layout retain the same score. The final
chooses core 15 and original cog 17355; it uses none of the new cog poses.
The bound remains 945,862,719. This completed call is not repeated or extended.

## Original layouts and next geometry to inspect

All **{l['layouts_checked_including_hint']}** layouts, including the starting hint,
pass original geometry, transform, stock and all 1,521 same-sheet pair checks.
Each has 18 frames, 15 cogs, 10 brackets and 21 inserts. There are
{l['fresh_frozen_CLI_calls']} fresh frozen-CLI calls and
{l['exact_CLI_results_reused']} exact-layout reuse; each result fails only the
original two-bracket quantity requirement. Best checked filled area is
{best['filled_area_mm2']:.9f} mm² and material is
{best['material_mm2']:.9f} mm². Hint/callback separation is 0.2001 mm and final
separation is 0.201 mm; none is native-margin qualified.

The retained pool still contains **{t['new_poses_retained']} new cog poses** and
{t['old_poses_retained']:,} old poses. Of the 3,803 removed new poses,
2,082 have a certified old replacement and 1,721 a certified new replacement;
10 old poses have certified new replacements. The retained families are
2,660 brackets, 3,158 inserts and 990 cogs. **172** retained new cogs expose old
bracket choices, but none has a positive net count of gained minus lost old
bracket candidates in its generating core. These counts reflect the old
candidate pool, not geometric capacity or achievable part quantities.

A transparent recorded ranking selects at most one such pose per generating
core, up to six; **five** distinct review cores exist. Each fixes 18 frames
and all 15 cogs. All **{t['review_core_original_geometry_pairs']:,}** original
same-sheet pairs pass. Their net old-bracket candidate changes are -24, -28,
-72, -615 and -694. They are explicit choices for inspecting new bracket and
insert contact positions, not improved or qualified layouts. The ranking,
all selected poses and both failed quantity checks remain preserved.

{nextstep['action']}

No native packing, production-budget qualification, complete H5 matrix or
held-out evaluation occurs. All 66 copies, the original material target,
native guard, production budget and all 13 jobs at both kerfs remain required.
Source and all three accurate READMEs remain unchanged; preview v0.2.0-alpha.1
and stable Latest v0.1.0 remain current. Main facf0f38 run 39984899040 is saved
as `{ci['status']}` / `{ci['conclusion'] or 'pending'}`; 5e88ac91 is committed
locally and waits for main's remaining checks before the next normal push.

Evidence: [graph]({NAME}/graph.json), [independent audit]({NAME}/audit.json),
[provenance]({NAME}/provenance.json), [reduction]({NAME}/reduction.json),
[encoding]({NAME}/encoding.json), [model]({NAME}/model.json), [solver]({NAME}/solver.json),
[original layouts]({NAME}/layouts.json), [best layout]({NAME}/best-layout.json),
[final layout]({NAME}/final-layout.json), [retained geometry]({NAME}/retention.json),
[review cores]({NAME}/review-cores.json), [source review]({NAME}/source-review.json),
raw evidence {links}, and [manifest]({NAME}/raw-manifest.json). All
{archive['archive_members']} canonical members and {archive['verified_aliases']}
aliases are byte-verified, with archive CRCs and SHA-256 hashes checked.
Every ZIP part is independently readable and below 50 MiB.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 continuous-cog joint selection, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
checks all 20,058 choices, 6,917,176 new geometric conflicts and a separately
justified count-derived cog clique. Fresh substitutions retain 6,808 choices,
including 197 new cogs, with all 30 baselines preserved. Complete compression
and every model/parameter field verify. One bounded solve reaches active
search and returns `FEASIBLE`; all three original layouts remain 64/66,
missing two brackets, with the full bound unresolved. Five new 33-part cores
are checked for a fresh bracket/insert contact investigation; their old
candidate-count rankings are not inventory gains. Main facf0f38 checks are
pending and 5e88ac91 is committed locally. Source, READMEs, releases and gate
requirements remain unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
