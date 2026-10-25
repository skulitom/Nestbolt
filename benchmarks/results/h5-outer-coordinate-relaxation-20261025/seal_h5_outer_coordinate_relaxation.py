"""Seal continuous coverage, the single outer-model result and a guarded alternate core."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-outer-coordinate-relaxation-20261025';BASE=ROOT/'output'/NAME;ALT=ROOT/'output/h5-guarded-alternate-core-20261025';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    generation=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');model=load(BASE/'solve/model-audit.json');result=load(BASE/'solve/result.json');alternate=load(ALT/'checks.json');aa=load(ALT/'audit/checks.json');prior=load(ROOT/'benchmarks/results/h5-direct-coordinate-selection-20261025/source-review.json');assert audit['passed'] and model['passed'] and alternate['passed'] and aa['passed'];assert generation['completed_queries']==24 and not load(BASE/'pending.json');assert result['status']=='INFEASIBLE' and result['solver_calls']==1 and not result['has_full_model_solution'] and not result['incumbents'];log=(BASE/'solve/solver.log').read_text(encoding='utf-8');done=re.findall(r'^#Done\s+([0-9.]+)s\s+([^\s]+)',log,re.M);assert done==[('13.78','no_lp')] and 'Starting search at 1.85s' in log and 'LRAT_status: NA' in log;assert not (BASE/'solve/relaxed-layout.json').exists()
    correction=load(BASE/'plan-correction.json');assert digest(BASE/'plan-original.json')==correction['original_plan_sha256'] and digest(BASE/'plan.json')==correction['corrected_plan_sha256'];assert all(digest(BASE/'queries'/n)==h for n,h in correction['query_geometry_hashes'].items())
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items());head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head.startswith('cc9e8702') and mainhead.startswith('8f941426');ci=json.loads(subprocess.check_output(['gh','run','view','40229962984','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==mainhead
    action='Evaluate the independently checked guarded alternative in output/h5-guarded-alternate-core-20261025/fixed-core.json. It preserves32 placements from saved core5 and moves its one changed cog by(+0.0125,-0.0125)mm to repair the stock margin while preserving the cog orientation. First construct and audit complete zero-clearance outer translation regions for this new fixed arrangement, retaining every original bracket/insert orientation, both original stock domains, all12 brackets and21 inserts, and the same outward quantization proof. The prior source regions cannot be reused unchanged because a cog moved; reconstruct its Minkowski obstacle and the complete affected unions. Declare fresh bounded construction and a single outer feasibility call before execution. Reuse checked encoding only after independently verifying every new model/input field. If this generous fixed-core relaxation is feasible, diagnose it against all original filled polygons; never accept its overlaps or expanded bounds. If it is infeasible with verified continuous coverage, preserve that conditional exclusion and investigate more substantial frame/cog rearrangement rather than retrying completed small-part searches. Do not extend the completed core0 calls, resume capped pose lists, lower native guards, change H2 or claim a new release. Any accepted outcome still needs all66 original parts, the material target, actual native checks, original production budget and the complete13-job/two-kerf matrix.'
    write(BASE/'next-step.json',{'action':action,'H5_complete':False,'full_target_witness':False})
    interpretation={'status':result['status'],'fixed_core':0,'original_fixed_parts':33,'original_variable_counts':{'bracket':12,'insert':21},'source_continuous_regions_covered':24,'permitted_orientation_reflection_cases':12,'outward_domain_count':953,'known_original_compatible_poses_covered':14734,'continuous_coverage_checked':True,'solver_completion_seconds':13.78,'solver_elapsed_seconds':result['seconds'],'conditional_conclusion':'Within the recorded original polygon and allowed-rotation model, the audited outer relaxation excludes the complete original inventory while all33 placements of core0 remain fixed at the original two-sheet material target. Further small-part pose sampling with that unchanged fixed core is not a useful direction. Different frame/cog arrangements are not excluded.','proof_limit':'CP-SAT reports INFEASIBLE for the fully checked model; no independently verified LRAT proof is available. The geometric implication relies on the committed original-outline zero-clearance translation-region audit and the new exact outward-coverage/encoding checks. This is not unrestricted infeasibility with freely moving fixed parts.','new_layout_returned':False,'unrestricted_problem_infeasibility_claimed':False,'native_margin_qualified':False,'H5_complete':False};write(BASE/'interpretation.json',interpretation)
    OUT.mkdir()
    for source,name in [(BASE/'plan.json','plan.json'),(BASE/'result.json','generation.json'),(BASE/'audit/checks.json','coverage-audit.json'),(BASE/'audit/provenance.json','provenance.json'),(BASE/'solve/plan.json','model-plan.json'),(BASE/'solve/model-audit.json','model-audit.json'),(BASE/'solve/result.json','solver.json'),(BASE/'interpretation.json','interpretation.json'),(BASE/'plan-correction.json','plan-correction.json'),(BASE/'next-step.json','next-step.json'),(ALT/'plan.json','alternate-core-plan.json'),(ALT/'projection.json','alternate-core-projection.json'),(ALT/'checks.json','alternate-core-screen.json'),(ALT/'audit/checks.json','alternate-core-audit.json')]:shutil.copyfile(source,OUT/name)
    write(OUT/'main-ci.json',ci);review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,'conditionally_excluded_fixed_core':0,'next_investigation':action};write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [BASE,ALT]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for row in load(BASE/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['build_h5_outer_coordinate_domains.py','audit_h5_outer_coordinate_domains.py','prepare_h5_outer_coordinate_solver.py','solve_h5_outer_coordinates.py','solve_h5_direct_coordinates.py','prepare_h5_guarded_alternate_core.py','audit_h5_guarded_alternate_core.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'all_original_continuous_source_regions_covered':True,'all_known_core0_poses_and_baseline_represented':True,'every_outward_inequality_and_model_field_verified':True,'one_outer_solver_call_only':True,'conditional_core0_exclusion_recorded':True,'all_other_arrangements_not_excluded':True,'alternate_core_original_geometry_independently_checked':True,'native_margin_qualified':False,'full_target_witness':False,'production_source_and_readmes_unchanged':True,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: continuous-coverage outer coordinate relaxation — 2026-10-25

**The audited outer relaxation reports `INFEASIBLE` with fixed core 0.**
Unlike the earlier inward-safe grid model, this construction covers the
recorded original continuous placement regions and deliberately permits extra
space and small overlaps. Within that original polygon/rotation model, keeping
these 18 frames and 15 cogs unchanged cannot accommodate all 12 brackets and
21 inserts at the original two-sheet material target. Different frame/cog
arrangements remain open. H2/H5 remain open at **60%** completed milestone weight.

## Coverage before the solver

Reuse the committed, independently checked zero-clearance translation regions
for core 0. All **24** queries retain all **12** permitted orientation/reflection
cases and both sheets. Their 953 outer hulls cover the complete source regions,
including unsampled positions. Normalize each orientation by its exact
quarter-turn bounding-box minimum, then add the full floor-quantization square
from -0.01 to 0 mm on each axis and 0.001 mm extra outward numerical padding.
Construction finishes in **{generation['seconds']:.6f} seconds**, within the
declared 120 seconds, with nothing pending.

The independent audit verifies 32 inherited input/query files against committed
manifests. Exact rational tests show that all **19,808** required shifted-source
and quantization vertices lie inside the expanded hulls. Convexity extends
that coverage to every continuous point. All **4,952** expanded-hull vertices
satisfy every outward-rounded halfspace and outward integer bound. The same
4,952 edge inequalities are independently re-derived with their complete
coefficient error allowances.

All **14,734** known original poses compatible with core 0 have encoded grid
representatives. The original 64-part baseline is retained as a partial
sanity check; all 500 of its cross-part rectangle-component pairs satisfy the
relaxed separation rule. It does not satisfy the model's required 66 parts.
Original floating quarter-turn transforms differ from their exact normalized
rectangles by at most 5.69e-14 mm; known translated polygons differ by at most
1.15e-13 mm, far below the original 0.2 mm clearance.

Review caught duplicated vertices in the plan's descriptive quantization-square
field. The actual construction and stated per-axis range already used the full
two-dimensional square. The field was corrected before the independent audit;
the original plan/builder and hashes of all 24 unchanged geometry files remain.
No geometry phase was regenerated or extended.

## Complete exact-count outer encoding

All 66 original parts remain mandatory: 33 fixed and 33 small parts. The model
retains **17,178** per-copy domain choices and **360** orientation/sheet modes.
Every bracket has two coupled original rectangular arms. All **978** component
pairs from distinct physical parts are constrained; a bracket's own arms
are never separated from each other.

Original nonoverlap gives an x or y order between axis-aligned rectangle
components. Their dimensions and offsets are exact grid multiples, so flooring
the two anchors preserves zero-gap order. Allowing an additional one-grid-unit
overlap only enlarges the model. Expanded stock, dropped positive clearance,
outward domains and that overlap are relaxation parameters, never acceptable
cutting settings. The original material target remains the source of the
second-sheet height limit.

Independent reconstruction checks every field of the **22,290-variable**,
**128,377-constraint** model and every solver parameter. The generated encoding
retains the previous independent checker; all template changes and hashes are
recorded. There is no objective, missing-part allowance or arbitrary pruning.

## Result and its limit

One declared 60-second, eight-worker, seed-zero call reaches search at
**1.85 seconds**. The log records `#Done 13.78s no_lp`; total elapsed time is
**{result['seconds']:.6f} seconds**. Status is `INFEASIBLE`, with no incumbent,
170,621 branches and 32,789 conflicts. The call is neither repeated nor extended.

This is CP-SAT's result for the fully checked model, without a separately
verified LRAT proof. The conditional geometric implication relies on the
committed original-outline translation-region audit and the exact outward
coverage/encoding checks above. It excludes continuing to hold **core 0**
unchanged within that recorded geometry model. It does not establish
unrestricted impossibility when the frame/cog placements may change, close H5,
or justify different quantities, clearances or material limits.

## A guarded alternative to investigate

Saved core 5 differs from core 0 in one rotated cog. Its pair distances pass
the guarded screen, but that cog lies too close to the left and top stock
edges. A single deterministic nearest-point projection moves it by
**(+0.0125, -0.0125) mm**, preserving its rotation and every other 32 placement.
This is a new arrangement, not resumed sampling from a capped proposal list.

An independent affine-transform audit verifies all **438** same-sheet original
polygon pairs and **132** stock boundaries. Minimum pair gap is 0.2126 mm and
minimum extra stock margin is 0.0126 mm, above the source-derived compensated
separation 0.21170867250963943 mm and conversion guard 0.011444091796875 mm.
This passes a sufficient distance screen only. There is no 66-part layout or
actual native transformed-collision qualification yet.

{action}

## Repository and evidence

Engine source, all three accurate READMEs and releases are unchanged. Main
8f941426's hosted checks are captured as `{ci['status']}` /
`{ci['conclusion'] or 'pending'}`; the two newer domain/model checkpoints remain
local at source head {head[:8]}. No native packing, production-budget run,
full H5 matrix or held-out evaluation occurs. A new release is not qualified.

Evidence: [construction plan]({NAME}/plan.json), [coverage audit]({NAME}/coverage-audit.json),
[complete model audit]({NAME}/model-audit.json), [solver]({NAME}/solver.json),
[conditional interpretation]({NAME}/interpretation.json),
[alternate projection]({NAME}/alternate-core-projection.json),
[independent alternate-core audit]({NAME}/alternate-core-audit.json),
[source review]({NAME}/source-review.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All {archive['archive_members']} canonical
members and {archive['verified_aliases']} aliases retain exact bytes with
CRC and SHA-256 checks, including every region, model, source plan and solver log.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 continuous-coverage outer result, 2026-10-25:** [the complete audit](../benchmarks/results/{NAME}.md)
checks 24 source regions, all twelve permitted orientation/reflection cases,
953 outward domains and all 14,734 known compatible core-0 poses. Exact rational
containment and rounding cover the full source regions, not just saved samples.
Every field of the 22,290-variable/128,377-constraint exact-count model verifies.
One bounded outer search reports INFEASIBLE in 13.950743 seconds. Within the
recorded geometry/coverage model this excludes the full inventory with core 0
unchanged; it does not exclude different frame/cog arrangements. A single
projected cog in saved core 5 yields a new arrangement passing all 438 original
pair and 132 stock-boundary screens, with the other 32 placements unchanged.
Next check its complete outer regions and exact-count feasibility before any
accepted-layout claim. Actual native qualification and all H5 requirements
remain. Source, accurate READMEs and releases are unchanged; H2/H5 stay open
at 60% completed milestone weight.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
