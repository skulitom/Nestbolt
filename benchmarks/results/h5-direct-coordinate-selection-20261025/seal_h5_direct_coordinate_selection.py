"""Seal the sole exact-count coordinate solve and its precisely limited conclusion."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
BASE=ROOT/'output/h5-direct-coordinate-domains-20261025';RED=BASE/'reduced';SOLVE=BASE/'solve';NAME='h5-direct-coordinate-selection-20261025';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    reduction=load(RED/'result.json');ra=load(RED/'checks.json');model=load(SOLVE/'model-audit.json');result=load(SOLVE/'result.json');plan=load(SOLVE/'plan.json');prior=load(ROOT/'benchmarks/results/h5-direct-coordinate-domains-20261025/source-review.json');assert ra['passed'] and model['passed'] and result['status']=='INFEASIBLE' and result['solver_calls']==1 and not result['has_full_model_solution'] and not result['incumbents'];assert not (SOLVE/'layout.json').exists();log=(SOLVE/'solver.log').read_text(encoding='utf-8');done=re.findall(r'^#Done\s+([0-9.]+)s\s+([^\s]+)',log,re.M);assert done==[('59.73','no_lp')] and 'status: INFEASIBLE' in log and 'Starting search at 10.09s' in log
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items());head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head.startswith('7fa9fc18') and mainhead.startswith('8f941426');ci=json.loads(subprocess.check_output(['gh','run','view','40229962984','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==mainhead
    action='Investigate an independently checked outer coordinate relaxation for fixed core 0 before changing the fixed arrangement or repeating inner-domain search. Keep the full original 12-bracket/21-insert inventory and all 18 frames/15 cogs. Construct outer translation domains covering every original permitted continuous placement, with explicit allowances for grid quantization and numerical geometry, rather than reusing inward-safe domains as if exhaustive. For cross-part axis-aligned rectangle components, drop positive clearance and allow the grid-rounding displacement needed to cover every continuous nonoverlap; those are relaxation parameters only and can never qualify a cutting layout. Verify all orientation/reflection aliases, unchanged stock accounting, complete region coverage, every rounded inequality and every known original compatible placement. Declare a fresh construction and one solver limit before execution. A feasible relaxed solution is only diagnostic and must not be accepted as a layout. Any negative claim must be conditional on the recorded fixed core and full outward-coverage audit. Preserve the completed inner model and its infeasibility, the original counts, native guard and production budget; do not rerun or extend this solve, infer unrestricted impossibility, resume capped pose lists or change H2. Original geometry, actual native qualification and the full 13-job/two-kerf H5 matrix remain required for completion.'
    write(SOLVE/'next-step.json',{'action':action,'original_problem_resolved':False,'H5_complete':False})
    OUT.mkdir()
    for source,name in [(RED/'plan.json','reduction-plan.json'),(RED/'result.json','reduction.json'),(RED/'checks.json','reduction-audit.json'),(SOLVE/'plan.json','plan.json'),(SOLVE/'model-audit.json','model-audit.json'),(SOLVE/'result.json','solver.json'),(SOLVE/'next-step.json','next-step.json')]:shutil.copyfile(source,OUT/name)
    write(OUT/'main-ci.json',ci)
    interpretation={'solver_status':result['status'],'solver_done_seconds':float(done[0][0]),'solver_done_worker':done[0][1],'elapsed_seconds':result['seconds'],'search_started_seconds':10.09,'declared_limit_seconds':60,'soft_wall_overrun_preserved':result['seconds']>60,'original_required_counts':plan['required_counts'],'fixed_core':0,'coordinate_grid_mm':.01,'new_part_gap_mm':.22,'new_part_extra_stock_margin_mm':.02,'original_part_gap_mm':.2,'proof_scope':'The checked exact-count integer model only: its inward-rounded safe subdomains, fixed core 0, additional spacing, stock margin and axis-wise component separation. CP-SAT reports infeasibility; no separately checked LRAT proof is available.','unrestricted_original_infeasibility_claimed':False,'other_core_infeasibility_claimed':False,'new_layout_returned':False,'native_margin_qualified':False,'production_budget_qualified':False,'H5_complete':False};write(OUT/'interpretation.json',interpretation)
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,'next_investigation':action};write(OUT/'source-review.json',review)
    members={};inputs={}
    for root in [RED,SOLVE]:
        for p in root.rglob('*'):
            if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
        for p in root.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for n in ['plan.json','audit/checks.json','consolidated/plan.json','consolidated/audit/checks.json','consolidated/audit/integer-domains.json','fixed-core.json']:
        p=BASE/n;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    pending=[ROOT/'output'/n for n in ['reduce_h5_coordinate_domains.py','solve_h5_direct_coordinates.py','audit_h5_consolidated_coordinate_domains.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'all_input_hashes_match':True,'all_removed_domains_independently_certified':True,'every_model_variable_constraint_and_parameter_checked':True,'all_original_quantities_required':True,'no_same_part_arm_separation_imposed':True,'one_solver_call_only':True,'inner_model_infeasibility_preserved':True,'unrestricted_impossibility_not_claimed':True,'production_source_and_readmes_unchanged':True,'completion_percent':60,'H5_complete':False,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: exact-count direct-coordinate selection — 2026-10-25

**CP-SAT reports `INFEASIBLE` for the checked grid model with fixed core 0.**
It returns no layout. This closes this particular inner-domain search, but
does not prove the original continuous placement problem or another fixed
arrangement impossible. H2/H5 remain open at **60%** completed milestone weight.

## Certified removal of redundant domains

The previous independently checked domains remain preserved. Exact rational
clipping reconstructs all 3,703 domains. One predeclared 30-second/500,000-check
containment phase takes **{reduction['reduction_seconds']:.6f} seconds** and
7,268 comparisons. It removes **26** domains only when a retained domain in
the same orientation and sheet contains their entire bounded rational region.
All **3,677** retained domains remain eligible: 2,412 for brackets and 1,265
for inserts, giving **55,509** per-copy alternatives for the exact inventory.
No limit is reached and no incomplete comparison phase is resumed.

A separate boundary-line intersection oracle reconstructs every removed
source domain, independently of the clipping routine. It verifies 121 vertices
against 1,166 target inequalities. Each removal preserves every allowed grid
coordinate, orientation and sheet assignment. No arbitrary pose pruning occurs.

## Complete model verification

The model contains **60,537 variables** and **306,319 constraints**. It fixes
the original 18 frames and 15 cogs from core 0 and requires all **12 brackets
and 21 inserts**, with no objective or unplaced-part variable. Every physical
small part has shared anchor coordinates and exactly one orientation/sheet
mode. Its active mode selects one of the certified convex domains and applies
every inward-rounded halfspace and stock bound.

Each L bracket uses its exact two rectangular arms; their offsets share the
same mode and anchor. The model includes all **528** distinct physical-part
pairs and all **978** cross-part rectangle-component pairs. Same-sheet pairs
must have at least 0.22 mm separation along one axis. The arms belonging to the
same bracket are never separated from one another. Thirty-one ordering
constraints only permute identical copies by sheet/y/x. All permitted original
orientation/reflection aliases remain accounted for.

An independent protobuf reconstruction checks every variable, constraint and
parameter, including all 55,509 domain-choice booleans and 276 orientation/sheet
modes. No additional model fields or hidden objective are present. Model
preparation and that complete comparison take **{model['seconds']:.6f} seconds**.

## One bounded search and its actual scope

Exactly one 60-second, eight-worker, seed-zero call is made. Ordinary presolve
is enabled; presolve probing and automatic symmetry discovery are disabled.
The normal worker portfolio still includes a probing search worker. The log
reaches search at **10.09 seconds** and records `#Done 59.73s no_lp` before
returning `INFEASIBLE`. Actual elapsed time is **{result['seconds']:.6f} seconds**;
the soft overrun is preserved, without a retry or extension. The response
records 218,662 branches and 22,653 conflicts. There is no returned incumbent.
No separately checked LRAT proof is present; this is the solver's result for
the independently checked model.

This model is a conservative subset of original placements: it uses a 0.01 mm
grid, inward-rounded safe domains, 0.22 mm new-part gap, 0.02 mm additional
stock margin and axis-wise component separation. Original required part gap
is 0.2 mm. Those construction restrictions can exclude valid continuous
placements. Therefore the result does not establish that core 0 must move,
that the original target is impossible, or that H5 can be relaxed.

## Next continuous-coverage question

{action}

## Repository and evidence

The domain checkpoint 7fa9fc18 is preserved locally; earlier audits are pushed
to main 8f941426. Main's hosted checks are captured as
`{ci['status']}` / `{ci['conclusion'] or 'pending'}`. Engine source, accurate
READMEs and releases are unchanged. No new release is qualified. No original
geometry acceptance run, native packing, production-budget trial, full H5
quality matrix or held-out evaluation occurs because no layout was returned.
The original 66-part inventory, material target, native guard, production
budget and all 13 jobs at both kerfs remain required.

Evidence: [reduction]({NAME}/reduction.json), [independent containment audit]({NAME}/reduction-audit.json),
[model plan]({NAME}/plan.json), [complete model audit]({NAME}/model-audit.json),
[solver result]({NAME}/solver.json), [precise interpretation]({NAME}/interpretation.json),
[source review]({NAME}/source-review.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All {archive['archive_members']} canonical
members and {archive['verified_aliases']} aliases retain exact bytes with
CRC and SHA-256 verification, including the binary model and complete solver log.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 exact-count coordinate result, 2026-10-25:** [the complete model audit](../benchmarks/results/{NAME}.md)
certifies 26 domain-containment removals and preserves all 3,677 retained
domains. Every field of the 60,537-variable/306,319-constraint model verifies,
including exact original quantities and all 978 cross-part arm pairs. One
declared 60-second search reports INFEASIBLE for the restricted grid/domain
model with fixed core 0, finishing at 59.73 seconds with 60.354444 seconds
actual elapsed time. No layout is returned and no solve is repeated. This
does not prove the unrestricted continuous problem impossible or that the
fixed core must move. Next verify an outer coordinate relaxation covering
all original continuous placements before drawing any conditional negative
conclusion. Engine source, accurate READMEs and releases remain unchanged;
H2/H5 stay open at 60%, with all original counts and acceptance limits retained.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
