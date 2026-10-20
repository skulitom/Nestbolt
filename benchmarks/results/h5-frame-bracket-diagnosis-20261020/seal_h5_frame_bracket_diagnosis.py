from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,subprocess,shutil,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-frame-bracket-diagnosis-20261020';OUT=ROOT/'benchmarks/results'/PREFIX
MIX=ROOT/'output/h5-novel-whole-frames-20261020'
FRAME=ROOT/'output/h5-frame-availability-20261020'
ADAPT=ROOT/'output/h5-availability-completion-adapter-20261020'
COMP=ROOT/'output/h5-availability-completion-20261020'
BOUND=ROOT/'output/h5-frame-bracket-capacity-20261020'
SRC=ROOT/'output/h5-skeleton-contact-selection-20261020'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir()
    mixed=load(MIX/'result-audit.json');frames=load(FRAME/'result-audit.json')
    completion=load(COMP/'result-audit/checks.json');bounds=load(BOUND/'results.json')
    assert mixed['new_frame_cog_pairs']==0 and mixed['statuses']=={'1':4}
    assert frames['all_returned_frame_layouts_checked']==19 and frames['final_cases']==4
    assert all(c['solver_status']=='INFEASIBLE' for c in completion['cases'])
    assert completion['all_returned_layouts_checked']==0
    assert all(r['original_12_brackets_ruled_out'] and r['certificate']['independent_fraction_reconstruction_matches'] for r in bounds)
    assert [r['certificate']['integer_bracket_upper_bound'] for r in bounds]==[7,7,10,10]
    core=source_digest();assert core=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    old=load(ROOT/'benchmarks/results/h5-whole-group-diagnosis-20261020/source-review.json')
    readmes={p:digest(ROOT/p) for p in old['current_readmes']};assert readmes==old['current_readmes']
    inputs={}
    for root in [MIX,FRAME,COMP,BOUND]:
        for p,h in load(root/'plan.json')['inputs'].items():
            assert digest(ROOT/p)==h
            if p in inputs:assert inputs[p]==h
            inputs[p]=h
    ci=json.loads(subprocess.check_output(['gh','run','view','39439565169','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']=='f6edfb7149e2ac03ad221a033e00c45be2ed38bb'
    write(OUT/'main-ci-f6edfb7.json',ci)
    next_step=('The four heuristic frame arrangements fail the exact 12-bracket quantity even when all inserts are removed: '
        'their independently certified integer bracket upper bounds are 7, 7, 10 and 10. Reject this additive pose-availability '
        'score as a sufficient construction criterion. Next build a bounded construction that selects all 18 frames and 12 '
        'brackets simultaneously with one full cog arrangement, preserving their original conflict cliques and exact quantities. '
        'Insert availability may guide ranking but cannot replace a separate exact 21-insert completion test. Exclude the 26 '
        'previously reviewed exact frame sets and retain all failed cases and any returned groups. Declare limits before solving; '
        'do not extend the four expired mixed models or rerun these rejected fixed groups unchanged. Any full original 66-copy '
        'layout still needs the frozen CLI, independent filled-outer geometry, native margins and unchanged full H5 material/cutting '
        'gates. H2 remains open under Artem’s original-denominator decision.')
    write(OUT/'source-review.json',{'production_digest':core,'current_readmes':readmes,
        'current_main_commit':ci['headSha'],'current_main_CI_status':ci['status'],'current_main_CI_conclusion':ci['conclusion'],
        'runtime_changed':False,'native_packing_calls':0,'quality_runs':0,'frozen_CLI_calls':0,
        'full_target_witness':False,'native_margin_qualified':False,'new_release_qualified':False,
        'H2_complete':False,'H5_complete':False,'completion_percent':60,'next_investigation':next_step})
    for p,name in [(MIX/'model-audit.json','mixed-model-audit.json'),(MIX/'result-audit.json','mixed-results.json'),
        (FRAME/'model-audit.json','frame-model-audit.json'),(FRAME/'result-audit.json','frame-results.json'),
        (COMP/'model-audit.json','completion-model-audit.json'),(COMP/'result-audit/checks.json','completion-results.json'),
        (BOUND/'results.json','bracket-bounds.json')]:shutil.copyfile(p,OUT/name)
    members={}
    for root in [MIX,FRAME,ADAPT,COMP,BOUND]:
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for p in inputs:
        path=ROOT/p;members['source-inputs/'+path.relative_to(ROOT).as_posix()]=path
    for name in ['prepare_h5_novel_whole_frames.py','audit_h5_novel_frame_model.py','solve_h5_novel_whole_frames.py',
        'audit_h5_novel_frame_results.py','build_h5_frame_availability.py','audit_h5_frame_availability_model.py',
        'solve_h5_frame_availability.py','audit_h5_frame_availability_results.py','adapt_h5_availability_completion.py',
        'prepare_h5_availability_completion.py','audit_h5_availability_completion_model.py','solve_h5_availability_completion.py',
        'audit_h5_availability_completion_results.py','diagnose_h5_bracket_capacity.py','solve_h5_area_relaxations.py','audit_h5_cog_lattices.py']:
        members['helpers/'+name]=ROOT/'output'/name
    archive=OUT/'raw.zip';manifest=[]
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for r in manifest:assert sha256(z.read(r['path'])).hexdigest()==r['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'all_input_hashes_verified':True,
        'mixed_cases_preserved':4,'frame_only_models_independently_reconstructed':4,'frame_proposals_geometry_checked':19,
        'completion_models_independently_reconstructed':4,'completion_layouts_returned':0,
        'exact_bracket_bounds_reconstructed':[7,7,10,10],'full_target_witness':False,'completion_percent':60,
        'archive_members':len(manifest),'archive_sha256':digest(archive)})
    shutil.copyfile(__file__,OUT/'seal_h5_frame_bracket_diagnosis.py')
    mixed_table='\n'.join(f"| {r['case']} | {r['seconds']:.9f} | Time limit, no incumbent |" for r in load(MIX/'results.json'))
    frames_table='\n'.join(f"| {r['case']} | {r['seconds']:.9f} | {r['incumbents']} | {r['heuristic_cost']:.0f} |" for r in load(FRAME/'results.json'))
    bounds_table='\n'.join(f"| {r['case']} | {r['bracket_candidates']} | {r['certificate']['upper_bound_brackets']:.12f} | **{r['certificate']['integer_bracket_upper_bound']}** |" for r in bounds)
    report=f'''# H5: new frame arrangements and bracket capacity — 2026-10-20

**Four new complete frame arrangements fail because too few brackets can
coexist.** Exact rational certificates bound their bracket counts at **7, 7, 10
and 10**, below the original 12. No complete layout or improved partial is found.
The next construction must choose frames and brackets together. H2/H5 remain
open at 60%; no release or product change is qualified.

## Whole frames with fractional smaller parts

Following the [previous diagnosis](h5-whole-group-diagnosis-20261020.md), four
mixed-integer feasibility models fix one original complete cog arrangement,
require 18 whole frames, and retain the exact 12-bracket and 21-insert sums while
relaxing those smaller parts to fractions. All original conflicts and audited
local area capacities remain. The 26 reviewed exact frame sets are excluded:
nine receive explicit sum-at-most-17 rows and seventeen already contain a pose
absent from the model. Only the 2,213 frame variables are integral, among 6,786
variables. Every row, bound, exclusion and integrality change is independently
checked before solving.

Each case has one declared **30-second limit**, eight workers and seed zero.
All four expire without an incumbent; slight solver cleanup overruns are
preserved. No suffix is retried and no fractional or physical layout is returned.

| Cog case | Seconds | Outcome |
| --- | ---: | --- |
{mixed_table}

These are bounded failed constructions, not infeasibility proofs.

## A changed frame-only construction

A separate declared model selects exactly 18 whole frames compatible with the
fixed cog arrangement, retaining all frame conflicts and excluding all 26 old
sets. It ranks frames by how few existing smaller-part poses each blocks. The
integer cost is proportional to the sum of normalized blocked bracket and
insert fractions. Shared blocked positions may be counted more than once;
this is explicitly a heuristic, with no area or completion guarantee.

All four Boolean models and every cost are independently reconstructed from the
original conflict cliques. Each case declares **10 seconds**, eight workers and
seed zero, without a retry. All four reach the heuristic optimum:

| Cog case | Seconds | Returned incumbents | Heuristic cost |
| --- | ---: | ---: | ---: |
{frames_table}

All **19 returned frame/cog proposals** pass original filled-outer geometry,
allowed rotation, stock, margin and clearance checks. Each has all 18 frames and
15 cogs. Each case's final frame set is new, and the four final sets are distinct.
Only those four final sets proceed to completion. This stage places no brackets
or inserts and has no full-job credit.

## Exact completion and the reason for failure

Four new completion models fix those final frame/cog groups, require 12 whole
brackets and maximize inserts up to 21. Their surviving candidate counts are
308, 452, 695 and 754. Every model is independently reconstructed, and 46,017
original same-sheet pairs between fixed parts and surviving candidates are
checked before solving. The adapter starts from hash-verified sealed scripts;
every scope change is retained explicitly.

Each completion has one declared **20-second limit**, eight workers and seed
zero. All four return `INFEASIBLE` in 0.0183, 0.0176, 0.1979 and 0.3066 seconds.
They return no incumbent, so no new frozen CLI validation is claimed.

To identify the obstructing quantity, a further necessary relaxation removes
every insert and maximizes the simultaneous bracket sum, retaining every
bracket conflict and unit variable bound. Four declared ten-second LPs finish
in under 0.01 seconds each. Their saved duals are converted into exact rational
upper bounds and independently reconstructed using Python `Fraction`:

| Cog case | Individually available bracket poses | Exact bound, decimal display | Integer bracket upper bound |
| --- | ---: | ---: | ---: |
{bounds_table}

For minimization of minus the bracket sum, any nonpositive inequality
multipliers give a lower bound from their row totals plus the minimum reduced
cost over each unit interval. All coefficients and right-hand sides are integers;
binary64 multipliers are interpreted as exact dyadic rationals. This avoids
rounding a solver objective into a proof. Exact numerators and denominators,
all primal/dual vectors and both arithmetic reconstructions are saved.

Thus these fixed frame/cog groups cannot fit the required 12 brackets **from
their finite original pose pools**, even without inserts. The certificates do
not bound arbitrary continuous arrangements. Counting individual available
poses had concealed their mutual conflicts; the frame-only ranking is rejected
as a sufficient construction criterion.

## Next work and repository state

{next_step}

The original candidate geometry, stock, targets and all gate thresholds remain
unchanged. There is no held-out access, native packing, quality run, full new
layout, runtime change or new release. All three README hashes still match the
current hosted-preview description. Main remains at pushed **f6edfb7**, with its
separate [hosted check snapshot]({PREFIX}/main-ci-f6edfb7.json) retained. This
diagnostic checkpoint is local until a subsequent recorded push.

[Checks]({PREFIX}/checks.json), [mixed outcomes]({PREFIX}/mixed-results.json),
[frame audit]({PREFIX}/frame-results.json), [completion audit]({PREFIX}/completion-results.json),
[exact bounds]({PREFIX}/bracket-bounds.json), [source review]({PREFIX}/source-review.json),
[raw models, certificates and bounded results]({PREFIX}/raw.zip), and
[verified manifest]({PREFIX}/raw-manifest.json).
All {len(manifest)} archive members, CRCs and byte hashes verify.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 frame/bracket capacity, 2026-10-20:** [four new frame constructions and exact bracket bounds](../benchmarks/results/{PREFIX}.md)
follow four preserved 30-second mixed-model timeouts. A changed frame-only
heuristic finds four new final frame sets; all 19 returned frame/cog proposals
pass original geometry checks. Four independently reconstructed completion
models reject these sets without a layout. Removing inserts and reconstructing
exact rational dual bounds proves that their surviving finite poses allow at
most 7, 7, 10 and 10 brackets, below the required 12. This does not prove the
unrestricted job impossible. Individual pose availability is insufficient;
next select all 18 frames and 12 brackets together before exact insert
completion. No expired model is extended, no quality run occurs and no gate
changes. H2/H5 remain open at 60%; runtime and README contents are unchanged.
'''
    previous=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==previous
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 whole-group diagnosis, 2026-10-20:**'
    assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
        'exact_integer_bracket_bounds':[7,7,10,10],'completion_percent':60,'current_main_CI_status':ci['status']}),flush=True)
if __name__=='__main__':main()
