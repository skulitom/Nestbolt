"""Seal the independently proved guarded displacement cells before solver use."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-cog-displacement-cells-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    raw=load(BASE/'result.json');fine=load(BASE/'refinement/result.json');coarse=load(BASE/'coarse-refinement/result.json');audit=load(BASE/'audit/checks.json')
    assert audit['passed'] and audit['retained_cells']==233 and audit['exact_whole_cell_failure_region_separations']==13531 and audit['previous_second_sheet_witnesses_retained']==5
    assert raw['solver_calls']==fine['solver_calls']==coarse['solver_calls']==audit['solver_calls']==0
    prior=load(ROOT/'benchmarks/results/h5-second-sheet-guided-search-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('b8c6dbff') and mainhead=='613594568fb49a71abf0248aec218a6b12f63319'
    ci=json.loads(subprocess.check_output(['gh','run','view','40242602102','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('The complete guarded displacement-cell representation is now independently prepared and proved safe, but no new solver has run. '
        'Use229 first-sheet cells plus4 unchanged second-sheet cells,831 inward halfplanes total. Every one of13531 whole-cell/nonempty-source-failure pairs has an exact rational strict separating-axis certificate, read back and checked. '
        'The source failure polygons are the full61 original guarded clauses clipped to each exact same-sheet difference box: failed integer outside projection>=bound means projection<=bound-1. '
        'All five verified second-sheet pair witnesses remain inside selected cells. First-sheet simplification tolerance0.005mm and outward forbidden padding0.01mm add a conservative construction restriction, not a relaxed acceptance guard; negatives cannot exclude the unrestricted geometry. '
        'Next replace the guided master\'s71-piece necessary raw-core disjunctions with sheet-conditional allowed displacement cells. Keep the full inherited domain/area/occupancy model and all140 new guarded/exact pair exclusions, all66 originals and fixed57 source. '
        'Bind every cog anchor to its complete selected inward domain and explicit query box. A same-sheet physical pair must choose one allowed displacement cell for that sheet; differing-sheet pairs must need no cell. Every chosen cell enforces its sufficient inward halfplanes on anchorB-anchorA, with exact query difference bounds. '
        'Verify all Boolean gating, model fields, signed difference-coordinate rounding and any optional witness hints before one distinct staged call. Preserve the shared60-second pipeline,45-second master cap and2-second shutdown reserve. '
        'A positive has full guarded cog separation but still needs all other original-pair coordinates, independent66-original stock/geometry/native checks, production-budget integration and the unchanged13-job/two-kerf H5 matrix. Do not continue any closed prior call. '
        'Main61359456 remains preserved; await terminal CI40242602102 before a normal push, reconciling any newer work first. H2 remains open under the unchanged gate with all22 reserved vectors untouched. No release is qualified.')
    OUT.mkdir()
    copies={'plan.json':'preparation-plan.json','result.json':'preparation-result.json','summary.json':'initial-representation.json','previous-witness-membership.json':'initial-witness-membership.json',
        'refinement/plan.json':'fine-refinement-plan.json','refinement/candidates.json':'fine-candidates.json','refinement/result.json':'fine-result.json',
        'coarse-refinement/plan.json':'coarse-refinement-plan.json','coarse-refinement/candidates.json':'coarse-candidates.json','coarse-refinement/result.json':'coarse-result.json','coarse-refinement/selection.json':'selected-representation.json',
        'audit/checks.json':'cell-audit.json','audit/query-checks.json':'cell-query-checks.json','audit/retained-witnesses.json':'retained-witnesses.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'new_solver_model_prepared':False,'new_solver_calls':0,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],
        'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,'pushed':False,
        'first_sheet_conservative_failure_padding_mm':.01,'current_main_ci_id':40242602102,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    oldmanifest=ROOT/'benchmarks/results/h5-original-core-search-20261025/raw-manifest.json';old=load(oldmanifest);known={r['path']:r['sha256'] for r in old['files']+old['aliases']}
    witness=ROOT/'output/h5-original-core-search-20261025/remaining-second-sheet-pairs/audit/verified-pair-witnesses.json'
    assert digest(witness)==known[witness.relative_to(ROOT/'output').as_posix()]
    members['source-inputs/'+oldmanifest.relative_to(ROOT).as_posix()]=oldmanifest
    pending=[ROOT/'output'/n for n in ['prepare_h5_cog_displacement_cells.py','refine_h5_cog_displacement_cells.py','refine_h5_cog_displacement_cells_coarse.py','audit_h5_cog_displacement_cells.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'complete_source_failure_polygons_reconstructed_exactly':True,'all233_retained_cells_imply_full_guarded_original_clauses':True,
        'all13531_exact_separation_certificates_read_back':True,'all_five_prior_second_sheet_witnesses_retained':True,'all_candidates_and_constructive_restrictions_preserved':True,
        'production_and_readmes_unchanged':True,'solver_calls':0,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: proved guarded cog displacement cells — 2026-10-25

**A smaller guarded separation representation is ready for a new full search.**
Independent exact proofs show that every retained allowed cell satisfies every
full original guarded cog/cog clause. No new solver runs in this checkpoint,
and no full target layout is found. H2/H5 remain open at **60%**.

## Exact source-clause complement

The previous fully guarded model used59 forbidden pieces and2,636 separating
directions per physical pair. Its simpler71-piece raw-core relaxation omitted
moving-pair clearance and still returned UNKNOWN. The alternative prepared here
represents allowed displacement regions directly, while proving full guarded
separation for every retained integer displacement.

For an integer relative position, failure of a source outside inequality
`A*dx + B*dy >= bound` is exactly `A*dx + B*dy <= bound - 1`.
For each of the61 complete guarded source clauses, exact rational clipping
constructs that clause's entire convex failure polygon inside each complete
same-sheet difference box. This accounts for **122 bounded failure regions**.
Outward dyadic vertex boxes enclose each rational polygon before geometric union
and complement operations. The first sheet has59 nonempty failure regions;
the second sheet has five.

The initial decomposition retains **1,245 first-sheet cells and four second-sheet
cells**, with11 explicitly retained inset/grid discards. It covers the complete
raw prepared free region but is too large for the intended reduction. All raw
faces and discarded records remain preserved.

## Conservative first-sheet simplification

Four declared sub-micrometre simplification candidates still leave at least
1,158 first-sheet cells. A separate bounded preparation measures five additional
representations. Each simplifies the whole failure union and pads it outward by
twice the tolerance; the complete original failure union must remain covered.
The second-sheet representation is copied unchanged.

| Simplification tolerance | Outward failure padding | First-sheet cells |
|---:|---:|---:|
| 0.001 mm | 0.002 mm | 464 |
| **0.005 mm** | **0.010 mm** | **229** |
| 0.010 mm | 0.020 mm | 183 |
| 0.025 mm | 0.050 mm | 143 |
| 0.050 mm | 0.100 mm | 112 |

The declared rule selects the smallest tolerance producing at most352 total
cells, including the unchanged four second-sheet cells. Thus the selected
representation has **229+4=233 cells and831 inward halfplanes**. No selected raw
face is discarded and both raw prepared free regions are fully covered. This
does not remove the explicit boundary loss from outward enclosure, first-sheet
simplification/padding, allowed-face insets and integer rounding.

The 0.010 mm first-sheet padding is a **conservative construction restriction**.
It can exclude feasible placements; a negative result cannot establish
unrestricted packing impossibility. It never weakens the original guard,
material target or66-part requirement. Selection concerns representation size,
not benchmark success. All nine measured candidates remain available as evidence.

## Independent whole-cell safety proof

The independent audit reconstructs every source failure polygon with rational
arithmetic and checks its complete vertex set and outward enclosure. It verifies
the selected complete free regions, all233 convex cells and all831 sufficient
inward halfplanes, including exact signed-coordinate coefficient-error bounds.

For every retained cell and every nonempty failure polygon, a strict separating
axis proves the **whole cell** disjoint from that source-clause failure region.
Floating calculations only nominate an axis; exact rational projections of all
vertices must verify its strictly positive gap. The audit then reads back and
rechecks all **13,531 certificates**. Integer displacement points in any retained
cell therefore satisfy every complete original guarded source clause, provided
the model enforces the declared same-sheet difference bounds.

All **five previously verified second-sheet pair witnesses** remain in retained
cells and satisfy their exact integer halfplanes. The independent audit takes
**{audit['seconds']:.6f}s**. Preparation times are **{raw['seconds']:.6f}s** for the
initial complement, **{fine['seconds']:.6f}s** for the first four candidates, and
**{coarse['seconds']:.6f}s** for the next five. Every declared120-second bound is met.

Across15 physical cog pairs, the new representation needs at most **3,495 cell
flags**, compared with **39,540 outside-direction variables** in the earlier full
guarded model, or5,280 in the weaker raw-core model. These counts do not establish
a runtime improvement; the new solver model is not constructed or run yet.

Next bind the full master to sheet-conditional allowed displacement cells,
retaining all original domain, area, occupancy and pair constraints. Same-sheet
pairs must choose a sufficient cell; different-sheet pairs require none. Verify
every model field and Boolean implication before one distinct shared60-second
pipeline with a45-second master cap and two-second shutdown reserve. Any positive
still needs the remaining full original-pair coordinates, all66-original/native
checks, production integration and unchanged13-job/two-kerf H5 matrix.

## Repository and evidence

Main61359456 and its offcut page remain preserved. Its own
[CI40242602102]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful jobs
at the saved snapshot. This checkpoint is local; the normal push awaits terminal
CI to avoid cancelling the Windows check. Production source and all three
accurate READMEs are unchanged. Preview v0.2.0-alpha.1 and stable Latest v0.1.0
remain unchanged; no release is qualified. No solver, native packing, quality
run or reserved H2 vector evaluation occurs. All22 reserved vectors stay untouched.

Evidence: [exact cell audit]({NAME}/cell-audit.json),
[per-sheet certificate counts]({NAME}/cell-query-checks.json),
[all coarse candidates]({NAME}/coarse-candidates.json),
[retained witnesses]({NAME}/retained-witnesses.json), [archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). The archive retains **{archive['archive_members']}**
canonical files and **{archive['verified_aliases']}** exact-content aliases, including
all source polygons, candidates, halfplanes and exact certificates, with verified
length, SHA-256 and ZIP CRC.
'''
    for a,b in {'used59':'used 59','and2,636':'and 2,636','simpler71':'simpler 71','the61':'the 61','has59':'has 59','with11':'with 11','most352':'most 352','and831':'and 831','or66':'or 66','all233':'all 233','all831':'all 831','declared120':'declared 120','Across15':'Across 15','or5,280':'or 5,280','shared60':'shared 60','a45-second':'a 45-second','all66':'all 66','unchanged13':'unchanged 13','Main61359456':'Main 61359456','All22':'All 22'}.items():report=report.replace(a,b)
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 exact guarded displacement cells, 2026-10-25:** [the evidence]({link})
prepares 229 first-sheet and four second-sheet allowed relative-position cells.
It reconstructs all 122 bounded source-clause failure regions exactly, then
independently proves all 233 whole cells safe with 13,531 rational separating-axis
certificates and 831 inward halfplanes. All five known second-sheet witnesses
remain represented. The selected first-sheet simplification uses 0.005 mm
tolerance and 0.010 mm outward failure padding, an explicit stricter construction
restriction; negative results cannot exclude unrestricted packing. All nine
measured candidates, initial faces and discards remain preserved. At most 3,495
cell flags replace the earlier guarded model's 39,540 direction variables, but
no new solver model or runtime improvement is claimed yet. Next integrate these
proved cells with all 66 originals and unchanged material/native/H5 requirements.
Production source, READMEs and releases are unchanged. H2/H5 stay open at 60%;
all 22 reserved H2 vectors remain untouched. Main CI40242602102 is still tracked
before the next normal push.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
