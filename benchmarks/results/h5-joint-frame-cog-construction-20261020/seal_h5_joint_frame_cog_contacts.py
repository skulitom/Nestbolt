"""Seal the eight new candidate sets, joint models and all returned layout checks."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-joint-frame-cog-construction-20261020'
OUT=ROOT/'benchmarks/results'/PREFIX
CONTACTS=ROOT/'output/h5-joint-frame-cog-contacts-20261020'
SOLVE=ROOT/'output/h5-joint-frame-cog-completion-20261020'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=ROOT)

def write(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,indent=2)
        f.write('\n')

def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as f:
        f.write(text)

def main():
    OUT.mkdir()
    head=git('rev-parse','HEAD').decode().strip()
    assert head=='8351f39a4b481d12a0be20fe0b5eac8f95a7d909'
    core=source_digest()
    assert core=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    generated=load(CONTACTS/'results.json')
    ca=load(CONTACTS/'audit/checks.json')
    results=load(SOLVE/'results.json')
    la=load(SOLVE/'audit/checks.json')
    assert len(generated)==len(results)==8 and ca['passed'] and la['passed']
    assert all(r['queries_completed']==10 and r['pending_queries']==0 and not r['generation_limit_reached']
               and not r['new_pose_cap_reached'] and not r['clique_limit_reached'] for r in generated)
    assert all(r['status']=='OPTIMAL' and r['cogs']==9 and r['best_bound']==9 and r['seconds']<20 for r in results)
    assert la['all_returned_layouts_checked']==16 and la['fresh_frozen_CLI_calls']==12
    assert la['exact_frozen_CLI_results_reused']==4 and not la['full_target_witness']
    assert all(r['incumbents']==1 for r in results)
    assert all(abs(r['charged_material_mm2']-4985103.45)<1e-6 and
               abs(r['filled_area_mm2']-4181364.4704418452)<1e-6 and
               not r['new_frame_contact_used'] and r['new_cog_contacts_used']==0 for r in la['records'])
    totals={name:sum(r[name] for r in generated) for name in ['new_frames','new_cogs','events','conflict_edges','compressed_cliques']}
    totals.update({name:sum(r[name] for r in ca['records']) for name in [
        'old_filter_pairs_checked','proposal_fixed_pairs_checked','all_eligible_pair_checks','rejected_proposals_verified']})
    prior=load(ROOT/'benchmarks/results/h5-single-frame-continuous-regions-20261020/source-review.json')
    readmes={p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']}
    assert readmes==prior['current_readmes']
    remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
    assert remote=='7c47f4989d40a6ba81e7022457f175b3965c4e7d'
    ci=json.loads(subprocess.check_output(
        ['gh','run','view','39461163256','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==remote
    if ci['conclusion']=='success':
        assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    write(OUT/'main-ci-7c47f498.json',ci)
    inputs={}
    for root in [CONTACTS,SOLVE]:
        for name,h in load(root/'plan.json')['inputs'].items():
            assert digest(ROOT/name)==h
            if name in inputs:
                assert inputs[name]==h
            inputs[name]=h
    for p in (SOLVE/'audit').rglob('validation-reuse-*.json'):
        reuse=load(p)
        assert reuse['rerun'] is False and reuse['exact_layout_match']
        for name,h in reuse['source_files'].items():
            assert digest(ROOT/name)==h
            inputs[name]=h
    next_step=('Do not rerun these eight joint single-frame models unchanged or resume the expired spatial tree. '
               'Their complete finite-pool optima remain nine cogs, and none of the new contact poses improves the returned count. '
               'Next investigate a coordinated whole-group construction: review the already audited complete frame groups, '
               'then allow bracket, insert and cog positions to be selected together instead of keeping either the51 non-cog set or one of the four old cog arrangements fixed. '
               'Choose a changed group or candidate construction from the original geometry after checking prior group results, '
               'declare its finite generation/solve limits, retain a valid partial baseline where available and independently recompute all relevant conflicts. '
               'An original66-copy witness, native margins and unchanged H5 material/cutting gates remain required; no single-part finite optimum proves unrestricted impossibility.')
    write(OUT/'source-review.json',{
        'verified_utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'production_digest':core,
        'current_readmes':readmes,'README_change_needed':False,'remote_main':remote,
        'remote_main_CI_status':ci['status'],'remote_main_CI_conclusion':ci['conclusion'],
        'original_geometry_layout_audits':16,'fresh_frozen_CLI_calls':12,'exact_CLI_results_reused':4,
        'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
        'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,
        'completion_percent':60,'H2_complete':False,'H5_complete':False,'next_investigation':next_step})
    for p,name in [(CONTACTS/'results.json','generation-results.json'),(CONTACTS/'audit/checks.json','candidate-and-graph-audit.json'),
                   (SOLVE/'results.json','solver-results.json'),(SOLVE/'audit/checks.json','layout-audit.json')]:
        shutil.copyfile(p,OUT/name)
    model_audits=[]
    for r in results:
        p=SOLVE/f"frame-{r['removed_frame']}"/'model-audit.json'
        audit=load(p)
        assert audit['all_model_fields_independently_reconstructed'] and audit['complete_feasible_seed_verified']
        assert digest(p.parent/'model.pbtxt')==audit['model_sha256']
        model_audits.append({'removed_frame':r['removed_frame'],**audit})
    write(OUT/'model-audits.json',model_audits)
    members={}
    for root in [CONTACTS,SOLVE]:
        for p in sorted(root.rglob('*')):
            if p.is_file():
                members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for name in inputs:
        p=ROOT/name
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    original=ROOT/'output/h5-coordinated-placement-selection-20261018'
    for name in ['job.json','library.json','request.json','conditional-target.json']:
        p=original/name
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['build_h5_joint_frame_cog_contacts.py','audit_h5_joint_frame_cog_contacts.py',
                                      'solve_h5_joint_frame_cog_contacts.py','audit_h5_joint_frame_cog_layouts.py','ccd1.py']]
    visited=set()
    while pending:
        p=pending.pop()
        if p in visited:
            continue
        visited.add(p)
        members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module
                  else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for module in mods:
                other=ROOT/'output'/(module+'.py')
                if other.is_file():
                    pending.append(other)
    manifest=[]
    archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name)
            manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:
            assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{
        'passed':True,'all_inputs_hash_verified':True,'cases_verified':8,'totals':totals,
        'all_models_independently_reconstructed':True,'solver_reported_cog_optima':[r['cogs'] for r in results],
        'unrestricted_infeasibility_claimed':False,'returned_layouts_verified':16,
        'fresh_frozen_CLI_calls':12,'exact_CLI_results_reused':4,'no_improvement_over_seed':True,
        'full_target_witness':False,'new_release_qualified':False,'completion_percent':60,
        'archive_members':len(manifest),'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    by_removed={r['removed_frame']:r for r in generated}
    table='\n'.join(f"| {r['removed_frame']} | {by_removed[r['removed_frame']]['frame_choices']} | "
                    f"{by_removed[r['removed_frame']]['cog_choices']} | {r['seconds']:.9f} | {r['cogs']} |"
                    for r in results)
    ci_note=('All six checks on remote 7c47f498 pass in the saved snapshot.' if ci['conclusion']=='success'
             else 'The remote 7c47f498 checks are still running in the saved snapshot. A complete pass is not inferred.')
    report=f'''# H5: joint frame and cog constructions — 2026-10-20

**All eight changed joint models still place nine cogs, six short of the
original requirement.** They finish below their declared limits and report
optimality for their finite candidate sets. All sixteen returned layouts
pass original geometry and fail the frozen CLI only for the cog quantity.
No improved partial, full witness or new release is established.
H2/H5 remain open at 60%.

## New constructions from unresolved frame regions

The [continuous-region audit](h5-single-frame-continuous-regions-20261020.md)
leaves eight single-frame choices unresolved. Each case holds the other fifty
non-cog poses fixed and allows a frame and all cogs to be selected together.
The original frame plus nine cogs remains a complete feasible starting point.
Every compatible old frame/cog candidate is retained, including old positions
outside the pending regions as additional valid finite choices.

The source pool's 9736 entries remain unchanged. New frame proposals come from
the remaining center cells, unioned by axis-size class and eroded by 0.001 mm
for positive construction margin. The canonical 0°/90° frame transforms cover
the two rectangular size classes; retained original poses keep their actual
rotations. New cog translation contacts use phases 0°, 4.5°, 9° and 13.5°
around the fifty fixed parts on both sheets.

Each case declares 120 seconds for generation, at most 600 new frame poses and
1000 new cog poses. Every polygon representative point, boundary vertex and
edge midpoint is processed in a recorded round-robin order. All **80 queries**
and **{totals['events']:,} proposals** complete without a generation limit or
pending query. Across the eight conditional sets, **{totals['new_frames']} frame
and {totals['new_cogs']} cog poses** are added. These are case totals, not a
deduplicated count across cases. All **{totals['rejected_proposals_verified']:,} rejected proposals**
remain recorded under the original geometry rules.

The independent audit checks **{totals['old_filter_pairs_checked']:,} old-candidate/fixed-part pairs**
and **{totals['proposal_fixed_pairs_checked']:,} proposal/fixed-part pairs**. It
reconstructs the frame regions and every sampling order, checks every accepted
and rejected proposal, and retains all eight original feasible seeds.

## Recompute every relevant conflict

No graph conditional on the old 51 fixed parts is reused. Original geometry
independently checks all **{totals['all_eligible_pair_checks']:,} eligible same-sheet
frame/cog and cog/cog pairs**, reproducing **{totals['conflict_edges']:,} conflicts**.
The **{totals['compressed_cliques']:,} verified cliques** cover every conflict;
no residual pair or compression limit remains.

Frame/frame geometry edges are intentionally omitted because every later model
requires exactly one frame. Those omitted pairs are never treated as geometric
clique evidence. All other pair conflicts are retained.

## Joint models and returned layouts

Each model fixes the fifty retained non-cog poses, requires exactly one frame,
and maximizes cogs from the known feasible nine through the original fifteen.
Every protobuf field, quantity constraint, objective and complete hint is
independently reconstructed before solving. Each case gets one 20-second
maximum, eight workers and seed zero, with no retry.

| Released frame | Frame choices | Cog choices | Seconds | Reported cog optimum |
| --- | ---: | ---: | ---: | ---: |
{table}

All eight runs return `OPTIMAL`, each with one callback and a distinct final
selection. The final count remains nine in every case. This is solver-reported
finite-pool optimality; it does not certify arbitrary continuous layouts or
prove that multiple non-cog moves are necessary.

All **16 layouts** receive independent original-outline, rotation, stock,
clearance and quantity checks. Twelve frozen CLI calls are fresh; four reuse
the exact original layout and hash-recorded result. Every CLI result fails
only with `part cog: expected 15, found 9`.

Every layout retains all 18 frames, 12 brackets and 21 inserts. Material charge
remains **4,985,103.45 mm²**, but the missing cogs invalidate the original job.
Filled area remains **4,181,364.4704 mm²**, with no improvement over this seed
or the previously documented better partials. Minimum clearances include
0.200100 mm; no native-margin qualification is claimed. The returned optima
use retained source poses rather than the new contacts.

## Source and next work

Core source and all three README hashes remain unchanged. The README accurately
describes the published preview and remaining work; no new release is qualified.
No native packing, quality run or reserved held-out evaluation occurs.

{ci_note}

{next_step}

[Checks]({PREFIX}/checks.json), [generation]({PREFIX}/generation-results.json),
[independent candidates and graphs]({PREFIX}/candidate-and-graph-audit.json),
[model audits]({PREFIX}/model-audits.json), [solver results]({PREFIX}/solver-results.json),
[all layout checks]({PREFIX}/layout-audit.json), [source review]({PREFIX}/source-review.json),
[remote checks]({PREFIX}/main-ci-7c47f498.json), [raw evidence]({PREFIX}/raw.zip)
and [manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 joint frame/cog constructions, 2026-10-20:** [all eight changed models and audits](../benchmarks/results/{PREFIX}.md)
combine one movable frame with free cog choices around the other 50 fixed
non-cog poses. The 80 queries add {totals['new_frames']} frame and {totals['new_cogs']} cog poses across the conditional
sets; every proposal, filter and relevant pair conflict is independently checked.
All eight finite-pool models report an optimum of nine cogs, without hitting
their 20-second limits. All 16 returned layouts pass original geometry and
retain the six-missing-cog CLI failure; 12 CLI calls are fresh and four exact
results are reused. No partial improves and no unrestricted impossibility is
claimed. Next investigate coordinated whole groups with all small-part families
free, after reviewing prior frame-group results; do not repeat these models.
Core source, README and releases remain unchanged. H2/H5 stay open at 60%.
'''
    assert (ROOT/'BENCHMARKS.md').read_bytes()==git('show','HEAD:BENCHMARKS.md')
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
        append(ROOT/name,'\n'+note)
    path=ROOT/'docs/STATUS.md'
    text=path.read_text(encoding='utf-8')
    marker='**N4 continuous single-frame regions, 2026-10-20:**'
    assert text.count(marker)==1
    path.write_text(text.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
                      'new_frames':totals['new_frames'],'new_cogs':totals['new_cogs'],'completion_percent':60}))

if __name__=='__main__':
    main()
