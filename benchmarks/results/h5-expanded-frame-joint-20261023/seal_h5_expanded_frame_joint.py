"""Seal the enlarged whole-frame selection and any separately checked coverage follow-up."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-expanded-frame-joint-20261023';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output'/NAME;COVER=ROOT/'output/h5-expanded-frame-group-coverage-20261023';NEXT=ROOT/'output/h5-all-pose-coverage-20261023'
COMPACT=ROOT/'output/h5-expanded-frame-implications-20261023'
FIRST=ROOT/'output/h5-expanded-frame-first-fit-cover-20261023'
FAST=ROOT/'output/h5-expanded-frame-first-fit-selection-20261023'
DIRECT=ROOT/'output/h5-expanded-frame-direct-search-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    data={name:load(BASE/path) for name,path in [('graph','result.json'),('audit','audit/checks.json'),('reduction','reduced/checks.json'),('hints','hints/checks.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json')]}
    assert all(data[k]['passed'] for k in ['audit','reduction','hints','model','layouts'])
    assert data['audit']['conflicts']==data['graph']['conflicts'] and data['model']['seed_score']>=1566740785 and data['model']['full_score']==1646740785
    assert data['solver']['status'] in ['FEASIBLE','OPTIMAL','UNKNOWN']
    assert not data['layouts']['full_target_witness'],'A full witness requires native/production follow-up before this partial-only checkpoint.'
    compact={name:load(COMPACT/path) for name,path in [('encoding','solve/encoding-audit.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json')]}
    assert all(compact[k]['passed'] for k in ['encoding','model','layouts']) and not compact['layouts']['full_target_witness']
    assert compact['encoding']['edges']==data['reduction']['induced_edges'] and compact['model']['seed_score']==data['model']['seed_score'] and compact['model']['full_score']==data['model']['full_score']
    assert compact['model']['constraints']<data['model']['constraints']/100
    assert compact['solver']['status'] in ['UNKNOWN','FEASIBLE','OPTIMAL']
    first=load(FIRST/'checks.json');assert first['passed'] and first['original_edges']==data['reduction']['induced_edges']
    fast={name:load(FAST/path) for name,path in [('encoding','solve/encoding-audit.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json')]}
    assert all(fast[k]['passed'] for k in ['encoding','model','layouts']) and not fast['layouts']['full_target_witness']
    assert fast['encoding']['edges']==first['original_edges'] and fast['model']['seed_score']==data['model']['seed_score'] and fast['model']['full_score']==data['model']['full_score']
    direct={name:load(DIRECT/path) for name,path in [('parameters','parameter-delta-audit.json'),('encoding','solve/encoding-audit.json'),('model','solve/model-audit.json'),('solver','solve/result.json'),('layouts','layout-audit/checks.json')]}
    assert all(direct[k]['passed'] for k in ['parameters','encoding','model','layouts']) and not direct['layouts']['full_target_witness']
    assert direct['model']['model_sha256']==fast['model']['model_sha256'] and direct['solver']['status']=='FEASIBLE'
    coverage=load(NEXT/'checks.json');assert coverage['passed']
    priorroot=ROOT/'benchmarks/results/h5-wide-core-compound-limits-20261023';prior=load(priorroot/'source-review.json')
    assert source_digest()==prior['production_digest'] and {p:digest(ROOT/p) for p in prior['current_readmes']}==prior['current_readmes']
    original=ROOT/'output/h5-coordinated-placement-selection-20261018';oldmanifest=load(priorroot/'raw-manifest.json');oldhashes={r['path']:r['sha256'] for r in oldmanifest['files']+oldmanifest.get('aliases',[])}
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name;assert digest(p)==oldhashes['source-inputs/'+p.relative_to(ROOT).as_posix()]
    OUT.mkdir()
    for name,value in data.items():write(OUT/f'{name}.json',value)
    for name,value in compact.items():write(OUT/f'compact-{name}.json',value)
    shutil.copyfile(COMPACT/'plan.json',OUT/'compact-plan.json')
    for name,value in fast.items():write(OUT/f'first-fit-{name}.json',value)
    write(OUT/'first-fit-cover.json',first)
    shutil.copyfile(FIRST/'plan.json',OUT/'first-fit-cover-plan.json');shutil.copyfile(FAST/'plan.json',OUT/'first-fit-selection-plan.json')
    for name,value in direct.items():write(OUT/f'direct-{name}.json',value)
    shutil.copyfile(DIRECT/'plan.json',OUT/'direct-plan.json')
    for source,name in [(BASE/'plan.json','plan.json'),(BASE/'reduced/plan.json','reduction-plan.json'),(BASE/'hints/plan.json','hint-plan.json'),(NEXT/'plan.json','all-pose-plan.json'),(NEXT/'checks.json','all-pose-audit.json')]:shutil.copyfile(source,OUT/name)
    best=max(direct['layouts']['records'],key=lambda r:r['filled_area_mm2']);index=best['incumbent']
    assert best['missing']=={'bracket':2},'Update the outcome and next-step narrative for a newly improved partial.'
    for source,name in [(DIRECT/f'layout-audit/layout-{index}.json','checked-partial-layout.json'),(DIRECT/f'layout-audit/public-{index}.json','checked-partial-public.json')]:shutil.copyfile(source,OUT/name)
    cis=[]
    for run,head in [('39964600029','7cd00432e81324e1c2d8a006147ca5fa3ba5bbb5'),('39969515541','955cc87eb3c5910e5b575f519676b44197fe3492')]:
        ci=json.loads(subprocess.check_output(['gh','run','view',run,'--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==head;write(OUT/f'main-ci-{head[:8]}.json',ci);cis.append(ci)
    assert cis[0]['conclusion']=='success' and len(cis[0]['jobs'])==6 and all(j['conclusion']=='success' for j in cis[0]['jobs'])
    next_step=('Do not rerun or extend this bounded group-choice solve or resume capped comparisons. Preserve the complete graph, residual edges, mapped original 64-part floor and every returned result. The new all-pose coverage audit identifies a distinct relaxation: release the requirement to choose one of 29 complete frame sets. Allow individually chosen original frame poses, all cogs, brackets and inserts under their original caps, retaining the original best partial as the floor. Use output/h5-all-pose-coverage-20261023/mapping.json. Build a fresh complete four-family graph; the 29-group graph omits small poses that were incompatible with those specific frame sets and does not contain frame/frame or frame/small edges. Audit every edge and use fresh same-family substitutions only with original neighbor inclusion. Preserve every residual constraint, declare fresh finite limits and independently reconstruct the entire model. This is an enlarged pose-selection problem, not an unchanged solver retry. No new geometry or unrestricted packing proof is claimed by the coverage audit. A complete original 66-copy target witness must precede native-margin qualification, a repair within the original production budget and the full H5 matrix. H2 retains Artem\'s unchanged gate; keep all 22 reserved vectors unopened.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,'best_original_partial_parts':64,'best_original_partial_missing':{'bracket':2},'bounded_group_model_status':data['solver']['status'],'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    review['compact_encoding_status']=compact['solver']['status']
    review['first_fit_encoding_status']=fast['solver']['status']
    review['direct_search_status']=direct['solver']['status']
    next_step='All three preceding encodings returned UNKNOWN during presolve. A separately declared strategy intervention changes only cp_model_presolve to false on the byte-identical first-fit model; its exact parameter delta is independently verified and search now reaches the baseline after 4.2047213 seconds. Preserve all four outcomes and every soft overrun. Do not repeat any unchanged model/strategy, extend any solve or resume capped work. Use the verified first-fit cover and explicit residual implications, with the measured no-presolve strategy, as the starting representation for a genuinely enlarged candidate model. Retain full edge, model and parameter audits; this is not a production speed claim. '+next_step
    review['next_investigation']=next_step
    write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [BASE,COVER,NEXT,COMPACT,FIRST,FAST,DIRECT]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('*.json'):
            if p.name not in ['plan.json','model-audit.json']:continue
            value=load(p)
            for name,h in value.get('inputs',value.get('input_hashes',{})).items():
                if name in inputs:assert inputs[name]==h
                inputs[name]=h
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name.replace('\\','/')]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-latest-wide-joint-20261023',['mapping.json','layout-audit/layout-final.json','layout-audit/public-final.json','layout-audit/command-final.json','layout-audit/checks.json']),('h5-whole-frame-census-20261020',['groups.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/name for name in ['build_h5_expanded_frame_joint.py','audit_h5_expanded_frame_joint.py','reduce_h5_expanded_frame_joint.py','seed_h5_expanded_frame_joint.py','solve_h5_expanded_frame_joint.py','audit_h5_expanded_frame_joint_layouts.py','prepare_h5_expanded_frame_joint.py','prepare_h5_expanded_frame_selection.py','audit_h5_all_pose_coverage.py','prepare_h5_expanded_frame_implications.py','solve_h5_expanded_frame_implications.py','audit_h5_expanded_frame_implication_layouts.py','compress_h5_expanded_frame_first_fit.py','prepare_h5_expanded_frame_first_fit_selection.py','solve_h5_expanded_frame_first_fit.py','audit_h5_expanded_frame_first_fit_layouts.py','prepare_h5_expanded_frame_direct_search.py','solve_h5_expanded_frame_direct.py','audit_h5_expanded_frame_direct_layouts.py','audit_h5_expanded_frame_direct_parameters.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [n.name.split('.')[0] for n in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    # Canonicalize identical bytes, retaining every original path as a verified alias.
    canonical={};aliases=[];files=[];staging=ROOT/'output'/f'{NAME}-raw-staging.zip'
    with zipfile.ZipFile(staging,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            row={'path':name,'bytes':p.stat().st_size,'sha256':digest(p)};key=(row['bytes'],row['sha256'])
            if key in canonical:aliases.append({**row,'canonical':canonical[key]})
            else:canonical[key]=name;z.write(p,name);files.append(row)
    # Independent complete ZIP parts stay below GitHub's recommended 50 MiB/file.
    archives=[];lookup={r['path']:r for r in files}
    with zipfile.ZipFile(staging) as source:
        assert source.testzip() is None;groups=[];group=[];size=0
        for info in source.infolist():
            assert info.compress_size<44*1024*1024
            if group and size+info.compress_size>44*1024*1024:groups.append(group);group=[];size=0
            group.append(info.filename);size+=info.compress_size
        if group:groups.append(group)
        for number,group in enumerate(groups,1):
            path=OUT/f'raw-{number:03d}.zip'
            with zipfile.ZipFile(path,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
                for name in group:
                    data_bytes=source.read(name);assert len(data_bytes)==lookup[name]['bytes'] and sha256(data_bytes).hexdigest()==lookup[name]['sha256'];z.writestr(name,data_bytes);lookup[name]['archive']=path.name
            assert path.stat().st_size<50*1024*1024
            with zipfile.ZipFile(path) as z:
                assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(group)
                for name in group:assert sha256(z.read(name)).hexdigest()==lookup[name]['sha256']
            archives.append({'path':path.name,'bytes':path.stat().st_size,'sha256':digest(path)})
    for r in aliases:
        target=lookup[r['canonical']];assert target['bytes']==r['bytes'] and target['sha256']==r['sha256'];r['archive']=target['archive']
    write(OUT/'raw-manifest.json',{'archives':archives,'files':files,'aliases':aliases,'format':'Each complete ZIP part is independently readable. Files name their archive. Byte-identical inputs are stored once; every alias names its canonical member, archive, exact byte length and SHA-256. All original paths and evidence are retained.'})
    checks={'passed':True,'all_input_hashes_verified':True,'original_job_library_request_target_match_previous_manifest':True,'all_geometry_reduction_model_layout_audits_pass':True,'layouts_checked':data['layouts']['layouts_checked_including_hint'],'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,'archive_parts':len(archives),'archive_members':len(files),'verified_aliases':len(aliases),'archive_bytes':sum(r['bytes'] for r in archives)}
    checks['compact_encoding_exact']=True;checks['compact_constraints']=compact['model']['constraints'];checks['compact_layouts_checked']=compact['layouts']['layouts_checked_including_hint']
    checks['first_fit_cover_and_encoding_exact']=True;checks['first_fit_layouts_checked']=fast['layouts']['layouts_checked_including_hint']
    checks['direct_parameter_delta_exact']=True;checks['direct_layouts_checked']=direct['layouts']['layouts_checked_including_hint'];checks['direct_search_status']=direct['solver']['status']
    checks['total_original_layouts_checked']=sum(v['layouts']['layouts_checked_including_hint'] for v in [data,compact,fast,direct])
    write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    g,a,r,h,m,s,l=[data[k] for k in ['graph','audit','reduction','hints','model','solver','layouts']]
    archive_links=', '.join(f"[part {i}]({NAME}/{v['path']})" for i,v in enumerate(archives,1))
    report=f'''# H5: enlarged frame-group joint selection — 2026-10-23

**The best original partial remains 64 of 66 parts, missing two brackets.**
The enlarged model chooses among all 29 checked complete frame arrangements
while moving cogs, brackets and inserts together. The first encoding returns
`{s['status']}` during presolve. A changed exact implication encoding returns
`{compact['solver']['status']}` under its separately declared 60-second allowance.
A faster, independently audited clique cover then returns
`{fast['solver']['status']}` under its own unchanged 60-second allowance.
Finally, an explicit no-presolve strategy change on the byte-identical audited
model reaches search and returns `{direct['solver']['status']}`.
No full original-job target witness or H5 completion is claimed;
H2/H5 remain open at **60%** completed milestone weight.

## Complete geometry and preserved baseline

The entire 35,488-entry accumulated source pool is preserved. All 29,631 eligible
small poses enter a fresh graph: 11,202 brackets, 13,272 inserts and 5,157 cogs.
This preserves all 5,302 old 26-group choices and all 21,468 latest wide-only
choices. All three small families move freely; exactly one complete 18-frame
group is selected. The original 64-part layout maps exactly to group 26.

Graph construction takes {g['graph_seconds']:.6f} seconds and checks
{g['bounds_candidates_exactly_checked']:,} expanded-bound pairs, yielding
**{g['conflicts']:,} conflicts**. A separate sequential bounds scan covers
{a['small_pair_possibilities']:,} same-sheet possibilities and
{a['small_pair_exact_distances']:,} exact distances, independently reconstructing
every saved adjacency row. The two distance counts differ because the builder
uses expanded rectangles while the auditor uses Euclidean bounding-box distance;
their complete conflict graphs agree exactly.

All 32,989 small poses and 141 used frame poses pass original stock/transform
checks. All 4,437 within-group frame pairs pass. Independent distances to each
whole group's polygon union recheck 765,513 distances and all 956,681 group
memberships. All 1,521 same-sheet pairs in the exact original seed pass.
All 4,576 original small-family count combinations preserve filled-area ordering
under the integer objective. Original job and target are unchanged.

## Bounded reduction, hints and selection

Fresh substitution retains {r['kept_candidates']:,} choices and removes
{r['removed_candidates']:,} only with a retained adjacent same-family replacement,
original neighbor inclusion and a superset of compatible frame groups.
The bounded search performs {r['comparisons']:,} comparisons in {r['seconds']:.6f}
seconds; limit reached: `{r['limit_reached']}`. Every unprocessed choice remains.
Independent certificates check {r['certificate_neighbors_independently_verified']:,}
original neighbors and {r['compatible_group_memberships_independently_certified']:,}
group memberships. The full 64-part score and exact family counts survive mapping.

The exact induced graph has {r['induced_edges']:,} conflicts. Its 20-second
compression allowance produces {r['compressed_cliques']:,} cliques and preserves
all {r['residual_edges']:,} residual edges. Every edge is reconstructed from the
saved constraints. No conflict is discarded. Timers for reduction/compression
exclude additional certificate checking, graph projection, serialization and
independent reconstruction; these are development diagnostics, not a production
budget measurement.

The 30-second hint allowance completes {h['completed_cases']:,}/1,508 deterministic
group/order starts, preserving {h['pending_cases']:,} pending cases. Every result
is independently checked against the graph, group membership, original caps and
score. The original 64-part baseline remains a feasible floor.

Every binary protobuf field is independently reconstructed: {m['variables']:,}
variables ({m['small_pose_variables']:,} small poses and 29 frame groups),
{m['constraints']:,} constraints, a minimum score of {m['seed_score']:,} and full
inventory score {m['full_score']:,}. One eight-worker, seed-zero call has a
60-second allowance and records {s['seconds']:.6f} wall seconds, status
`{s['status']}`, {s['incumbents']} callbacks and reported bound {s['best_bound']}.
The full log and any limit overrun are retained. No retry or extension occurs.

All {l['layouts_checked_including_hint']} layouts, including the mapped starting
hint and every returned distinct final result, receive original-geometry and
frozen-CLI checks: {l['fresh_frozen_CLI_calls']} fresh calls and
{l['exact_CLI_results_reused']} exact-layout reuses. Each partial keeps its missing
quantity violations. The detailed results remain linked below; a feasible partial
is not an original-job acceptance result. Native margins remain unqualified.

## Exact encoding follow-up

The first call stops after presolve with zero callbacks, branches and searched
solutions. Its reported zero bound is **not** an infeasibility certificate and
does not replace the independently checked feasible baseline. The saved log
identifies the cost of processing over 12 million separate pair constraints.

The changed encoding groups residual conflicts by lower-index endpoint:
selecting pose `i` implies that every listed conflicting pose `j` is absent.
It retains all larger at-most-one cliques. This is an exact representation
change, with no candidate, edge, quantity, group or objective relaxation.
Independent reconstruction matches all {compact['encoding']['edges']:,} induced
edges exactly. The {compact['encoding']['original_pair_rows']:,} pair rows become
{compact['encoding']['implication_rows']:,} enforced conjunctions, plus
{compact['encoding']['retained_larger_cliques']:,} retained larger cliques.

Every field of the changed model is independently reconstructed. Its constraint
count falls from {m['constraints']:,} to {compact['model']['constraints']:,} while
the complete hint and score floor remain identical. This new encoding makes
one eight-worker, seed-zero call with a 60-second allowance; the prior call is
not extended or overwritten. It returns `{compact['solver']['status']}` in
{compact['solver']['seconds']:.6f} wall seconds with
{compact['solver']['incumbents']} callbacks and reported bound
{compact['solver']['best_bound']}. All
{compact['layouts']['layouts_checked_including_hint']} original layout checks
pass geometry, preserving every missing-quantity failure:
{compact['layouts']['fresh_frozen_CLI_calls']} fresh frozen-CLI calls and
{compact['layouts']['exact_CLI_results_reused']} exact-layout reuses.
Neither encoding proves unrestricted packing impossible. No unchanged solve
is repeated. This syntax-only change also stops before search; its observed
73.635199-second soft overrun is retained and it is not a demonstrated runtime
improvement.

## Fresh first-fit clique cover

A new cover starts from the full original reduced graph. It chooses the lowest
available common neighbor directly, avoiding the prior 16-candidate scoring at
every clique extension. Its fresh 20-second allowance yields
{first['cliques']:,} cliques and retains every one of
{first['residual_edges']:,} residual edges. All {first['original_edges']:,}
original edges are independently reconstructed; the complete original hint
satisfies every resulting constraint. This is a changed compression algorithm,
not a continuation of the earlier capped cover.

The exact cover has {first['total_constraints']:,} rows and
{first['total_literals']:,} literals, versus 12,129,544 rows in the original
cover. Its larger cliques plus aggregated residual implications produce
{fast['model']['constraints']:,} final model constraints. Every protobuf field
and all original edges are checked again. One separately planned eight-worker,
seed-zero call has the same 60-second allowance and returns
`{fast['solver']['status']}` after {fast['solver']['seconds']:.6f} wall seconds,
with {fast['solver']['incumbents']} callbacks and reported bound
{fast['solver']['best_bound']}. All
{fast['layouts']['layouts_checked_including_hint']} original layouts are checked:
{fast['layouts']['fresh_frozen_CLI_calls']} fresh CLI calls and
{fast['layouts']['exact_CLI_results_reused']} exact-layout reuses. Full logs,
failed results and soft overruns remain preserved. No production performance
or native-margin claim follows from these finite diagnostic models.

## Explicit search-strategy intervention

Before enlarging the candidate set, a separately declared diagnostic intervention
changes **only** `cp_model_presolve` to false on the byte-identical first-fit
model. A protobuf parameter comparison independently verifies this single change;
the 60-second allowance, eight workers and seed zero stay unchanged. All original
constraints, complete hint and objectives remain identical. The previous three
presolve failures are retained, not replaced by this result.

This strategy reaches the checked baseline after 4.2047213 seconds and returns
`{direct['solver']['status']}` in {direct['solver']['seconds']:.6f} wall seconds,
with {direct['solver']['incumbents']} callbacks and final reported bound
{direct['solver']['best_bound']}. All
{direct['layouts']['layouts_checked_including_hint']} original layouts pass their
geometry checks and preserve the missing-quantity failures:
{direct['layouts']['fresh_frozen_CLI_calls']} fresh CLI calls and
{direct['layouts']['exact_CLI_results_reused']} exact-layout reuses.
This reaches search but does not supply a full 66-copy target witness or prove
the finite model optimal. No further unchanged call or allowance extension is made.

The log starts search at 4.64 seconds and records actual branch, LP and local
search work; the aggregate response's zero branch counters are not used to
claim no search. The 65.892903-second wall time exceeds the solver's soft
60-second allowance and is retained as observed. The distinct final layout
selects six small poses absent from the prior wide-only model, but its original
filled area stays 4,401,740.784070 mm², with two brackets missing and a roughly
0.2001 mm minimum gap. This is no improvement in the required full-job result.

## Future coverage: individual frame choices

A separate coverage audit directly reconstructs all {coverage['complete_source_pool']:,}
source poses from original vertices and checks original stock/transform rules.
It retains {coverage['eligible_candidates']:,}, with {coverage['rejected_candidates']:,}
explicit rejections. All {coverage['previous_group_model_small_choices_preserved']:,}
small choices and {coverage['previous_group_frame_choices_preserved']:,} frame
choices from the group model remain. Removing the whole-group restriction exposes
{coverage['additional_individual_frame_choices']:,} additional individual frame
poses and {coverage['additional_small_choices']:,} additional small poses.
All 86,944 original four-family count combinations preserve area ordering;
the best original partial maps and passes geometry. This audit generates no new
poses and runs no solver; the full four-family mutual graph remains pending.

{next_step}

## Repository and evidence

Main 7cd00432 now passes all six hosted jobs. The previous reviewed checkpoint
955cc87e was pushed normally to main; its run 39969515541 is captured as
`{cis[1]['status']}` / `{cis[1]['conclusion'] or 'pending'}`. Only observed passes
are claimed. Production source, original library/request/target and all three
READMEs remain unchanged. The published preview remains v0.2.0-alpha.1 and stable
Latest v0.1.0. These diagnostic changes do not qualify a new application release.
No registry publication, reserved-input evaluation, native packing or full H5
quality run occurs.

Evidence: [graph audit]({NAME}/audit.json), [reduction]({NAME}/reduction.json),
[hints]({NAME}/hints.json), [model]({NAME}/model.json),
[solve]({NAME}/solver.json), [original layouts]({NAME}/layouts.json),
[compact encoding]({NAME}/compact-encoding.json),
[compact model]({NAME}/compact-model.json), [compact solve]({NAME}/compact-solver.json),
[compact layouts]({NAME}/compact-layouts.json),
[first-fit cover]({NAME}/first-fit-cover.json),
[first-fit model]({NAME}/first-fit-model.json), [first-fit solve]({NAME}/first-fit-solver.json),
[first-fit layouts]({NAME}/first-fit-layouts.json),
[strategy parameter audit]({NAME}/direct-parameters.json),
[direct search]({NAME}/direct-solver.json), [direct layouts]({NAME}/direct-layouts.json),
[individual-pose coverage]({NAME}/all-pose-audit.json),
[source review]({NAME}/source-review.json), raw evidence {archive_links},
and [manifest]({NAME}/raw-manifest.json). All {len(files)} canonical members,
{len(aliases)} aliases, archive CRCs and byte hashes verify. The complete ZIP
parts stay below 50 MiB each; identical input bytes are stored once with explicit,
verified aliases. Every original source path remains represented.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 expanded frame-group selection, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
checks a fresh 29,631-pose graph with {g['conflicts']:,} conflicts across all 29
whole frame groups. Group-preserving substitutions retain the 64-part baseline;
all residual edges and pending work remain. The first bounded solve returns
`{s['status']}` during presolve. A changed exact implication encoding preserves
every edge, reduces constraints from {m['constraints']:,} to
{compact['model']['constraints']:,}, and returns `{compact['solver']['status']}`
during presolve. A fresh, cheaper clique cover retains all edges, reduces
residuals to {first['residual_edges']:,}, and its separately bounded changed
model returns `{fast['solver']['status']}`. Every original layout is audited;
an independently verified no-presolve strategy then reaches search on the
byte-identical model and returns `{direct['solver']['status']}`.
No full 66-copy witness is found. A separate coverage audit exposes {coverage['additional_individual_frame_choices']:,}
additional individual frame poses and {coverage['additional_small_choices']:,}
additional small poses by removing the whole-frame-group restriction. The next
model needs a fresh complete four-family graph. Previous checkpoint 955cc87e is
pushed after all six 7cd00432 checks pass. Product source, accurate READMEs and
releases remain unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print(checks,flush=True)
if __name__=='__main__':main()
