from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,subprocess,shutil,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-dominated-poses-and-seeds-20261020';OUT=ROOT/'benchmarks/results'/PREFIX
PARENT=ROOT/'output/h5-joint-frames-brackets-20261020'
RED=ROOT/'output/h5-dominated-pose-reduction-20261020'
SMALL=ROOT/'output/h5-reduced-joint-frames-brackets-20261020'
SUB=ROOT/'output/h5-substituted-partials-20261020'
ADAPT=ROOT/'output/h5-substituted-completion-adapter-20261020'
COMP=ROOT/'output/h5-substituted-insert-completion-20261020'
SEED=ROOT/'output/h5-certified-partial-seeds-20261020'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir()
    original=load(PARENT/'results.json');reduced=load(SMALL/'results.json');subs=load(RED/'audit.json')
    completed=load(COMP/'result-audit/checks.json');seeds=load(SEED/'checks.json')
    assert all(r['status']=='UNKNOWN' and not r['feasible'] for r in original+reduced)
    assert subs['all_substitutions_verified_with_sets']
    assert completed['all_returned_layouts_checked']==6 and completed['best_insert_count']==13
    assert seeds['all_four_joint_hints_exactly_feasible']
    assert [r['seed_inserts'] for r in seeds['cases']]==[12,12,13,13]
    core=source_digest();assert core=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    old=load(ROOT/'benchmarks/results/h5-frame-bracket-diagnosis-20261020/source-review.json')
    readmes={p:digest(ROOT/p) for p in old['current_readmes']};assert readmes==old['current_readmes']
    inputs={}
    for root in [PARENT,RED,SMALL,SUB,COMP,SEED]:
        for p,h in load(root/'plan.json')['inputs'].items():
            assert digest(ROOT/p)==h
            if p in inputs:assert inputs[p]==h
            inputs[p]=h
    ci=json.loads(subprocess.check_output(['gh','run','view','39439565169','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']=='f6edfb7149e2ac03ad221a033e00c45be2ed38bb'
    write(OUT/'main-ci-f6edfb7.json',ci)
    next_step=('All eight unseeded joint searches expire without a candidate, although direct certified substitution now supplies '
        'an exact feasible whole-frame/bracket hint for every reduced case. Do not repeat those cold starts or the six fixed-group '
        'insert completions unchanged. Next build a changed reduced model selecting whole frames, brackets and inserts together: '
        'retain the certified frame/bracket survivors, all compatible original insert poses, original conflicts, quantities and '
        'frame exclusions; maximize the actual insert count up to 21, rather than the blocked-pose heuristic. Supply a complete '
        'feasible zero/one hint from the audited 12, 12, 13 and 13-insert partials. Declare finite limits before solving and preserve '
        'every incumbent, including an unchanged seed. Partial quantities receive no full-job credit. Any complete original 66-copy '
        'layout still needs original filled-outer geometry, frozen CLI, native-margin qualification and unchanged H5 material/cutting '
        'gates. H2 remains open under Artem’s original-denominator decision.')
    write(OUT/'source-review.json',{'production_digest':core,'current_readmes':readmes,
        'last_pushed_commit':ci['headSha'],'last_pushed_CI_status':ci['status'],'last_pushed_CI_conclusion':ci['conclusion'],
        'local_base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'runtime_changed':False,'native_packing_calls':0,'quality_runs':0,'frozen_CLI_calls':12,
        'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,
        'completion_percent':60,'H2_complete':False,'H5_complete':False,'next_investigation':next_step})
    for p,name in [(PARENT/'result-audit.json','joint-results.json'),(RED/'results.json','reduction-results.json'),
        (RED/'audit.json','substitution-audit.json'),(SMALL/'model-audit.json','reduced-model-audit.json'),
        (SMALL/'result-audit.json','reduced-results.json'),(SUB/'result-audit.json','substituted-partial-audit.json'),
        (COMP/'result-audit/checks.json','completion-audit.json'),(SEED/'checks.json','seed-audit.json')]:
        shutil.copyfile(p,OUT/name)
    members={}
    for root in [PARENT,RED,SMALL,SUB,ADAPT,COMP,SEED]:
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helpers=['build_h5_joint_frames_brackets.py','audit_h5_joint_frames_brackets_model.py',
        'solve_h5_joint_frames_brackets.py','audit_h5_joint_frames_brackets_results.py',
        'prepare_h5_joint_insert_completion.py','solve_h5_joint_insert_completion.py',
        'reduce_h5_dominated_poses.py','audit_h5_pose_substitutions.py','prepare_h5_reduced_joint_model.py',
        'run_h5_reduced_joint_model.py','check_h5_substituted_partials.py','audit_h5_substituted_partials.py',
        'adapt_h5_substituted_completion.py','prepare_h5_substituted_insert_completion.py',
        'solve_h5_substituted_insert_completion.py','audit_h5_substituted_completion_results.py',
        'verify_h5_partial_seeds.py','audit_h5_cog_lattices.py']
    for name in helpers:members['helpers/'+name]=ROOT/'output'/name
    src=ROOT/'output/h5-skeleton-contact-selection-20261020'
    for name in ['library.json','request.json','selected-layout.json']:
        members['source-inputs/'+src.relative_to(ROOT).as_posix()+'/'+name]=src/name
    archive=OUT/'raw.zip';manifest=[]
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for r in manifest:assert sha256(z.read(r['path'])).hexdigest()==r['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    removed=[r['removed_joint_variables'] for r in load(RED/'results.json')['cases']]
    write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'all_inputs_hash_verified':True,
        'preserved_expired_joint_searches':8,'substitutions_independently_verified':sum(removed),
        'safe_substitutions_by_case':removed,'new_substituted_partials_geometry_checked':6,
        'completed_partials_geometry_checked':6,'full_original_CLI_checks':12,'complete_feasible_joint_hints':4,
        'full_target_witness':False,'completion_percent':60,'archive_members':len(manifest),'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/'seal_h5_dominated_poses_and_seeds.py')
    reduction_rows=load(RED/'results.json')['cases']
    table='\n'.join(f"| {r['case']} | {r['original_joint_variables']} | {r['kept_joint_variables']} | {100*r['removed_joint_variables']/r['original_joint_variables']:.2f}% | {original[r['case']]['seconds']:.6f} | {reduced[r['case']]['seconds']:.6f} |" for r in reduction_rows)
    completion_lines=[]
    for r in load(COMP/'results.json'):
        cog_case=load(COMP/('case-'+str(r['case']))/'mapping.json')['cog_case']
        completion_lines.append(f"| {r['case']} | {cog_case} | {r['seconds']:.9f} | {r['inserts']} | {r['missing_inserts']} |")
    completion_table='\n'.join(completion_lines)
    ci_line=(f"All six hosted checks on pushed **f6edfb7** pass ([exact-checkpoint evidence]({PREFIX}/main-ci-f6edfb7.json))."
        if ci['conclusion']=='success' else f"The hosted checks on pushed **f6edfb7** are still in progress in the [saved snapshot]({PREFIX}/main-ci-f6edfb7.json).")
    report=f'''# H5: certified pose reduction and feasible starting layouts — 2026-10-20

**No improved partial or complete layout is found.** The useful result is a
certified reduction of 26–30% of frame/bracket choices, plus concrete feasible
starting layouts for all four reduced models. These now allow a changed search
to optimize actual insert count from a known layout. H2/H5 remain open at 60%.

## Joint frames and brackets

The [bracket-capacity diagnosis](h5-frame-bracket-diagnosis-20261020.md) requires
selecting frames and brackets together. Four models therefore fix one complete
cog arrangement, require all 18 frames and 12 brackets simultaneously, retain
every projected original conflict, and exclude the 26 reviewed exact frame
sets. A blocked-insert-pose score ranks these choices but has no physical fit
guarantee. All models and costs are independently reconstructed.

Each case declares one **30-second limit**, eight workers and seed zero.
All four return `UNKNOWN` with no incumbent. The saved logs retain thousands of
search branches and many interchangeable positions; no failure is erased.

## Certified substitutions

For each fixed cog case, a same-family pose A may replace B only when:

1. A and B conflict, so a feasible selection of B cannot already contain A.
2. Apart from the compared pair, every eligible neighbor of A is already a
   neighbor of B, including **all eligible insert positions**.
3. A belongs to no additional excluded-frame-set constraint.
4. A is a final survivor, so no replacement chain is required.

Replacing B preserves family quantity and introduces no new conflict or
forbidden frame set. Its blocked-insert cost cannot increase. This preserves
completion existence within the original finite pose pool; it does not alter
geometry or assert anything about unrestricted continuous arrangements.

The reduction declares a 60-second total bound and ten million comparisons per
case, retaining unprocessed positions if either limit is reached. All four cases
finish without reaching either limit. Independent explicit-set checks verify
**{sum(removed)} substitutions** against the original cliques and exclusions.
Original source candidates remain intact.

The follow-up rule is declared before reduction: only cases removing at least
25% of joint variables receive one reduced-model solve. All four qualify. Each
reduced model is reconstructed against its parent with removed variables fixed
to zero, retaining exact quantities and objective and dropping only false
literals and tautological constraints.

| Cog case | Original joint variables | Retained | Removed | Original solve seconds | Reduced solve seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
{table}

All four reduced calls also return `UNKNOWN` without an incumbent at their
declared 30-second limits. The smaller models do **not** demonstrate a measured
search-speed improvement. All eight failures and soft cleanup overruns remain.
No expired process or suffix is restarted.

## Direct substitution succeeds where unseeded search did not

Applying the audited substitutions once to the six previously validated
whole-group partial layouts yields six new exact frame sets outside the old
exclusions, while retaining all existing inserts and cogs. The changes include
equivalent rectangular orientations, tiny translations and, in two cases,
frame movements of about **86.3248 mm**. Original filled-outline Hausdorff
distances are saved so coordinate changes are not confused with shape movement.

All six substituted partials pass original geometry, rotation, margins, clearance
and target-material checks. The frozen CLI rejects them only for their original
insert shortfall. They are construction starting points, not full jobs.

Six separately declared insert-only models fix the 18 frames, 12 brackets and
15 cogs, retain every surviving original insert pose and conflict, and maximize
the insert count up to 21. Every model is reconstructed before its single
20-second-maximum solve. All finish `OPTIMAL` quickly:

| Source case | Cog case | Seconds | Inserts | Missing |
| --- | ---: | ---: | ---: | ---: |
{completion_table}

The six returned layouts also pass original geometry and the frozen validator's
geometry checks, failing only the unchanged insert quantity. Counts match the
prior fixed-group optima; none improves the known 58-part partial, and no native
margin qualification or quality run is attempted.

From these outputs, each reduced joint model receives a complete zero/one hint.
Exact arithmetic checks every variable domain, conflict, family equality,
excluded frame set and objective: **57,374 constraints across four hints**.
Their insert counts are **12, 12, 13 and 13**. These witnesses establish that
the four reduced frame/bracket models are feasible despite their earlier
unseeded timeouts. They do not establish feasibility of the full 21-insert job.

## Next work and repository state

{next_step}

{ci_line}
The previous local checkpoint and this evidence remain local until a subsequent
recorded push. Core source and the three current README hashes are unchanged.
There is no held-out evaluation, native packing, quality run, new release or
milestone credit.

[Checks]({PREFIX}/checks.json), [substitution audit]({PREFIX}/substitution-audit.json),
[reduced models]({PREFIX}/reduced-model-audit.json), [completed partials]({PREFIX}/completion-audit.json),
[feasible hints]({PREFIX}/seed-audit.json), [source review]({PREFIX}/source-review.json),
[all raw models, failures, layouts and certificates]({PREFIX}/raw.zip), and
[verified manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 certified reduction and starting layouts, 2026-10-20:** [joint construction and safe pose substitution](../benchmarks/results/{PREFIX}.md)
preserve eight bounded searches without incumbents. Independent set checks
verify 4,105 same-family substitutions across four cases, preserving future
insert compatibility and frame exclusions while removing 26–30% of joint
variables. Direct substitution of known partials produces six valid new exact
frame sets. Their bounded insert completions retain 12, 12, 10, 11, 13 and 13
inserts; all twelve original CLI checks fail only the required insert quantity.
Exact checks across 57,374 constraints establish complete feasible starting
hints for all four reduced joint models. Next optimize actual whole-insert
count with these hints, retaining all conflicts and original acceptance rules.
No full layout or improvement is claimed; H2/H5 remain open at 60%.
'''
    previous=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==previous
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 frame/bracket capacity, 2026-10-20:**'
    assert s.count(marker)==1;s=s.replace(marker,note+'\n'+marker)
    if ci['conclusion']=='success':
        assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
        ci_note=f'All six hosted checks on pushed `f6edfb7` pass, including Windows, Linux, browsers, benchmark smoke and both maker rebuilds. [Exact-checkpoint evidence](../benchmarks/results/{PREFIX}/main-ci-f6edfb7.json). Subsequent local evidence commits require their own hosted result.'
        s=s.replace('**Hosted preview and repository reconciliation, 2026-10-20:**',ci_note+'\n\n**Hosted preview and repository reconciliation, 2026-10-20:**')
        append(ROOT/'BENCHMARKS.md','\n'+ci_note.replace('../benchmarks/','benchmarks/')+'\n')
    p.write_text(s,encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
        'substitutions_verified':sum(removed),'feasible_joint_hints':4,'completion_percent':60,
        'pushed_CI_status':ci['status'],'pushed_CI_conclusion':ci['conclusion']}),flush=True)
if __name__=='__main__':main()
