"""Seal the cog-only finite optimum and an audited coordinated relocation hypothesis."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import ast,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
NAME='h5-dense-cog-limit-20261023';OUT=ROOT/'benchmarks/results'/NAME
COG=ROOT/'output/h5-dense-cog-completion-20261023';BLOCK=ROOT/'output/h5-dense-group-blockers-20261023'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();gen=load(COG/'result.json');graph=load(COG/'audit/checks.json');model=load(COG/'solve/model-audit.json');solved=load(COG/'solve/result.json');layouts=load(COG/'layout-audit/checks.json');census=load(BLOCK/'checks.json');audit=load(BLOCK/'audit/checks.json')
    assert all(r['passed'] for r in [graph,model,layouts,census,audit])
    assert gen['old_eligible']==1346 and gen['new_candidates']=={'cog':1500} and gen['retained_candidates']==2846 and gen['pending_proposal_lists']==8
    assert solved['status']=='OPTIMAL' and solved['objective']==solved['best_bound']==model['seed_score'] and solved['counts']['cog']==13
    assert layouts['layouts_checked_including_hint']==3 and layouts['fresh_frozen_CLI_calls']==2 and layouts['exact_CLI_results_reused']==1 and not layouts['full_target_witness']
    assert census['cases_checked']==audit['all_declared_cases_reconstructed']==165 and not census['pending_cases'] and census['minimum_required_moves_in_declared_cases']==8
    assert audit['missing']=={'bracket':3,'insert':5} and not audit['original_CLI_valid']
    previous=load(ROOT/'benchmarks/results/h5-dense-wide-progress-20261023/source-review.json')
    assert source_digest()==previous['production_digest'] and previous['current_readmes']=={p:digest(ROOT/p) for p in previous['current_readmes']}
    ci=json.loads(subprocess.check_output(['gh','run','view','39950507182','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']=='2333dd2c590750fa44a3170b34827c25320fe755';write(OUT/'main-ci-2333dd2c.json',ci)
    next_step=('Do not repeat this fixed-non-cog model or resume the eight capped lists. The existing 64-part layout remains the best retained partial. For a changed coordinated construction, use output/h5-dense-group-blockers-20261023/best-subassembly.json: case 20, saved group 96 with member 3 omitted plus the original last-sheet cog. All 18 frames and all 15 cogs coexist with nine brackets and 16 inserts. Exactly three original brackets and five inserts remain to place. First check the original remaining-area/stock constraints, then declare a finite completion of those two families against the exact 58 retained poses. Reuse only compatible old poses, generate new actual-outline contacts for every allowed bracket orientation/reflection and both insert size classes, independently check the complete conflict model, and keep all attempts and limits. The 165-case blocker minimum is conditional on those arrangements, not a global move bound. This construction is not yet a production repair mechanism; the unchanged repair limits, native margins, original 66-copy validity, production budget and complete H5 gates remain requirements before integration. H2 retains Artem’s unchanged gate.')
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'production_digest':source_digest(),'current_readmes':previous['current_readmes'],
      'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','completion_percent':60,'H2_complete':False,'H5_complete':False,
      'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':next_step}
    write(OUT/'source-review.json',review)
    for p,name in [(COG/'plan.json','plan.json'),(COG/'result.json','generation.json'),(COG/'audit/checks.json','graph-audit.json'),(COG/'solve/model-audit.json','model-audit.json'),
      (COG/'solve/result.json','solver-result.json'),(COG/'layout-audit/checks.json','layout-audit.json'),(BLOCK/'checks.json','blocker-census.json'),(BLOCK/'audit/checks.json','blocker-audit.json'),
      (BLOCK/'best-case.json','best-case.json'),(BLOCK/'best-subassembly.json','subassembly.json'),(BLOCK/'audit/public.json','subassembly-public.json')]:shutil.copyfile(p,OUT/name)
    members={};inputs={}
    for root in [COG,BLOCK]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for name,h in load(root/'plan.json')['inputs'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name,h in model['input_hashes'].items():assert digest(ROOT/name)==h;inputs[name]=h
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder,names in [('h5-coordinated-placement-selection-20261018',['job.json','library.json','request.json','conditional-target.json']),('h5-dense-insert-gap-20261023',['layout.json','checks.json','public.json','command.json'])]:
        for name in names:
            p=ROOT/'output'/folder/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for p in (COG/'layout-audit').glob('validation-reuse-*.json'):
        for name,h in load(p)['source_files'].items():
            other=ROOT/name;assert digest(other)==h;members['validation-sources/'+other.relative_to(ROOT).as_posix()]=other
    pending=[ROOT/'output'/n for n in ['build_h5_dense_cog_completion.py','audit_h5_dense_cog_completion.py','solve_h5_dense_cog_completion.py','audit_h5_dense_cog_layouts.py','census_h5_dense_group_blockers.py','audit_h5_dense_group_blockers.py','ccd1.py']];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'all_input_hashes_verified':True,'all_geometry_graph_model_and_census_audits_pass':True,'best_retained_parts':64,'finite_cog_optimum':13,'new_subassembly_is_not_an_improvement':True,
      'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,'completion_percent':60,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    passing=sum(j['conclusion']=='success' for j in ci['jobs']);ci_text=('All six checks on main `2333dd2c` pass.' if ci['conclusion']=='success' else f'The saved main `2333dd2c` snapshot is {ci["status"]}, with {passing} successful checks; no complete pass is inferred.')
    report=f'''# H5: fixed-part cog limit and coordinated relocation — 2026-10-23

**The best retained layout remains 64 of 66 parts, missing two cogs.** A new
cog-only model proves an optimum of 13 cogs within its finite pool when all
51 non-cogs stay fixed. This is not a continuous impossibility result. A separate
audit identifies a checked complete-cog subassembly for coordinated small-part
relocation. H2/H5 remain open at **60%**.

## New cog-only pool

The [improved64-part layout](h5-dense-wide-progress-20261023.md) supplies the exact
18 frame, 12 bracket and 21 insert poses. Its necessary continuous cog bound of
19 is inconclusive for 15. The changed construction preserves the whole prior
pool and maps every seed placement exactly, appending only the newly added fixed
insert. All 1,346 compatible old cog poses remain, including applicable denser
groups and the complete 13-cog seed.

Sixteen conservative translation-region queries use the exact current cog angles
plus four sampled phases on both target sheets. All queries complete. Round-robin
proposal processing adds 1,500 cog poses in 8.351362300 seconds. The fresh pose cap
leaves eight recorded lists pending; they are not resumed. The candidate total is
2,846. The eight last-sheet construction regions are empty under the positive
padding; original valid last-sheet seed positions remain available.

Independent checks cover 242,894 old/fixed pairs, 61,360 proposal/fixed pairs,
every actual proposal, its origin and original stock bounds. No proposal is
geometrically rejected. Among 3,944,502 same-sheet candidate pairs, 1,432,196 exact
distances establish 1,169,914 conflicts. All are covered by 3,621 verified cliques,
with no residual edge or compression expiry. The full seed is preserved.

## Finite optimum and original validation

Every protobuf model field is independently reconstructed before one eight-worker,
seed-zero call with a 30-second limit. It finishes in 3.845595200 seconds with
`OPTIMAL`: the objective and bound both equal 13 cogs. The current fixed-part pool
therefore cannot supply the two missing cogs. No additional solver call is made.

The starting hint, one callback and a different final layout all pass original
geometry checks. The hint exactly matches the retained 64-part layout, so its
frozen-CLI result is reused with verified source bytes. Two fresh frozen-CLI calls
for the different outputs fail only for two missing cogs. Their 4,381,615.346194 mm²
filled area and 4,988,890.203495 mm² charged material do not improve. Minimum
clearance remains about 0.2011 mm; native construction margins are unqualified.
The finite phase/pose cap and conservative regions do not justify a claim about
all continuous positions or rotations.

## Which existing parts block complete cog groups?

A separately declared 165-case census considers every saved first-sheet group
of 15 cogs, each possible one-cog omission paired with the original last-sheet
cog, and every saved 14-cog group paired with that last cog. All cases contain
exactly 15 original cogs and retain the 18 frame poses.

The independent reconstruction checks all 15,155 cog pairs, 41,760 cog/frame
pairs and 52,745 cog/small-part pairs. Every case completes within the declared
30-second allowance. At least eight of the current small-part poses must move
for each of these particular cog arrangements. This is a conditional statement
about the 165 cases, not a global lower bound on moves.

Ranking by removed filled area, count and case index selects case 20: group 96,
member 3 omitted, plus the original last-sheet cog. It leaves three brackets and
five inserts to relocate, total 219,000 mm². The exact checked subassembly contains
18 frames, 15 cogs, nine brackets and 16 inserts: 58 parts. All 1,101 pairs and
original stock bounds pass; a fresh frozen-CLI result reports precisely the three
missing brackets and five missing inserts. Its 4,262,740.784070 mm² filled area is
below the retained 64-part result. It is a construction hypothesis, not a new best
layout or a qualified production repair.

{next_step}

## Repository and release status

The preceding checkpoints were pushed normally to main as `2333dd2c` after all
six checks on `37edb1d2` passed. {ci_text} Core source and all three README hashes
are unchanged. The existing preview remains accurately described; no new build
qualifies for release. No native packing, quality matrix or reserved-input
evaluation occurs. Original gates, release authorization and H2's reviewed
denominator decision remain unchanged.

Evidence: [generation]({NAME}/generation.json), [graph audit]({NAME}/graph-audit.json),
[model audit]({NAME}/model-audit.json), [solver result]({NAME}/solver-result.json),
[layout audit]({NAME}/layout-audit.json), [blocker census]({NAME}/blocker-census.json),
[independent reconstruction]({NAME}/blocker-audit.json), [exact subassembly]({NAME}/subassembly.json),
[original CLI failure]({NAME}/subassembly-public.json), [source review]({NAME}/source-review.json),
[raw evidence]({NAME}/raw.zip), and [manifest]({NAME}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    report=report.replace('improved64','improved 64')
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 fixed-part cog limit, 2026-10-23:** [the complete audit](../benchmarks/results/{NAME}.md)
preserves the best 64/66 partial. Sixteen new queries and all compatible prior
poses give 2,846 cog choices. All 1,169,914 conflicts and model fields are checked;
one bounded solve proves a finite-pool optimum of 13 cogs with all 51 non-cogs
fixed. The two-cog CLI shortfall remains. No unrestricted impossibility is claimed.
An independent 165-case complete-cog census finds that these particular groups
require at least eight small-part moves. The selected checked 58-part subassembly
contains all frames/cogs and needs three brackets plus five inserts; it does not
improve the retained partial. Next test a newly bounded completion of those eight
parts, preserving original geometry, production repair limits and full H5 scope.
Prior checkpoints are pushed as 2333dd2c. Source, accurate READMEs and releases
remain unchanged; H2/H5 stay open at 60%.
'''
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/name,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'CI_status':ci['status'],'finite_cog_optimum':13,'next_missing':audit['missing']})
if __name__=='__main__':main()
