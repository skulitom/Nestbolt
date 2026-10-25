"""Preserve complete single-core relocation domains and conditional exclusion."""
from pathlib import Path
from datetime import datetime, timezone
import ast, json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack, digest
NAME='h5-single-core-relocation-exclusion-20261025'
OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-core-relocation-regions-20261025'
load=lambda p:json.loads(p.read_bytes())

def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')

def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    result=load(BASE/'result.json'); audit=load(BASE/'audit/checks.json')
    model=load(BASE/'solve/model-audit.json'); solved=load(BASE/'solve/result.json')
    prior=load(ROOT/'benchmarks/results/h5-source-inventory-and-proxy-slot-coverage-20261025/source-review.json')
    assert audit['passed'] and model['passed']
    assert result['queries_completed']==result['queries_planned']==576
    assert result['cases_completed']==result['cases_planned']==33
    assert not result['pending_queries'] and not load(BASE/'pending.json') and not result['cell_cap_reached']
    assert audit['excluded_cases']==28 and audit['surviving_cases']==audit['surviving_allocations']==5
    assert solved['status']=='INFEASIBLE' and solved['solver_calls']==1 and not solved['incumbents']
    assert not solved['has_full_proxy_solution'] and not (BASE/'solve/positions.json').exists()
    log=(BASE/'solve/solver.log').read_text(encoding='utf-8')
    assert 'Starting search at 0.08s' in log and '#Done    0.13s probing' in log and 'LRAT_status: NA' in log
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('a8809268') and mainhead.startswith('247e823a')
    assert source_digest()==prior['production_digest']
    assert all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    ci=json.loads(subprocess.check_output(['gh','run','view','40233299884','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT))
    assert ci['headSha']==mainhead
    action='Stop single-core relocation attempts around this fixed64-part source: all33 recorded neighborhoods are excluded. A distinct next construction may move two of the33 frame/cog parts together while restoring both originals and both missing brackets:62 fixed plus4 mandatory equals66. First declare a bounded complete census of all528 unordered core pairs, their complete integer proxy free regions, every allowed sheet allocation and exact necessary occupied-area bounds for all nonempty role subsets. Retain the source orientation inventory, original area charges, material cap, all orientations for both extra brackets and all-angle cog proxies. Record caps and pending cases; do not silently extend them or infer impossibility from unfinished work. Only then consider a separately declared bounded four-part model for complete surviving cases after independent coverage/area auditing. No repeated unchanged solver call, smaller inventory, original clearance/native-guard reduction, reserved-vector access or new release. A positive proxy still needs full original shapes/angles, native checks, the production budget and all13 jobs/two kerfs. Poll existing main CI40233299884 and push accumulated commits normally after it is terminal.'
    OUT.mkdir()
    for rel,name in [('plan.json','region-plan.json'),('result.json','region-result.json'),
                     ('audit/checks.json','region-audit.json'),('audit/case-checks.json','case-audit.json'),
                     ('audit/surviving-neighborhoods.json','surviving-neighborhoods.json'),
                     ('solve/plan.json','solver-plan.json'),('solve/model-audit.json','model-audit.json'),
                     ('solve/result.json','solver-result.json')]:shutil.copyfile(BASE/rel,OUT/name)
    write(OUT/'main-ci.json',ci)
    write(OUT/'next-step.json',{'action':action,'H5_complete':False,'full_target_witness':False})
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,
            'production_digest':source_digest(),'current_readmes':prior['current_readmes'],
            'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,
            'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
            'solver_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
            'full_target_witness':False,'native_margin_qualified':False,'current_main_ci_id':40233299884,
            'next_investigation':action}
    write(OUT/'source-review.json',review)
    members={BASE.name+'/'+p.relative_to(BASE).as_posix():p for p in BASE.rglob('*') if p.is_file()}
    inputs={}
    for p in BASE.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for row in load(BASE/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['build_h5_core_relocation_regions.py',
             'audit_h5_core_relocation_regions.py','solve_h5_core_relocation_neighborhoods.py',
             'pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module
                  else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    checks={'passed':True,'complete33_case576_query_census':True,'nothing_capped_or_pending':True,
            'all73683_integer_obstacles_and3462_free_cells_independently_verified':True,
            'all33_original_source_poses_covered':True,'all1152_allocation_inequalities_independently_verified':True,
            '28_cases_excluded_by_necessary_occupied_area_or_original_area_bounds':True,
            'remaining5_cases_have_complete_exact_three_part_proxy_model':True,
            'all1111_variables2118_constraints_and_parameters_verified':True,
            'one_bounded_call_infeasible_without_incumbent':True,'lrat_certificate_available':False,
            'all66_original_counts_retained_in_every_case':True,
            'conclusion_only_for33_recorded_neighborhoods':True,'unrestricted_infeasibility_claimed':False,
            'production_source_and_readmes_unchanged':True,'full_target_witness':False,
            'native_margin_qualified':False,'H5_complete':False,'completion_percent':60,**archive}
    write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: all 33 single-core relocation neighborhoods excluded — 2026-10-25

**Moving one recorded frame or cog cannot make room for the two missing brackets
while the other 63 source poses stay fixed.** Complete necessary area bounds
exclude 28 neighborhoods. A separately audited exact integer-proxy model returns
`INFEASIBLE` for the other five in {solved['seconds']:.6f} seconds. This is a
conditional result for the recorded orientation inventory and fixed poses, not
an unrestricted packing impossibility claim. H2/H5 remain open at **60%**.

## Complete free regions and occupied-area bounds

The committed 64-part source still lacks two brackets. Each of its 18 frames
and 15 cogs is released in turn, with every component of that original part
removed from the fixed obstacles. The model must restore that part and add
both brackets: **63 + 1 + 2 = 66**. The 18 released frames retain their source
horizontal orientation inventory; cogs use the existing all-angle inscribed
disk's five coupled inner rectangles. Both extra brackets retain all eight
original orientation/reflection options and both allowed sheets. Sheet bounds,
the material target and full original area charges remain unchanged.

Construction completes all **576 queries** in **{result['seconds']:.6f} seconds,
within its declared 120-second limit and 500,000-cell cap. It returns **3,462**
free inclusive integer anchor cells, with no cap reached and nothing pending.
At 100 coordinate units/mm, strict rectangle overlap produces exact clipped
integer forbidden rectangles. Their complement includes touching boundaries
and isolated integer rows or columns; these are complete regions, not a sample
of candidate poses.

For every free anchor cell, sweep each moving component over the cell's
continuous bounding rectangle. The resulting occupied rectangle is an outward
cover of all attainable occupied component positions. Exact union areas bound
the physical proxy area available on each sheet. Every allowed sheet allocation
is checked against bracket-only, restored-part-only and combined occupied
covers, plus the original filled-area capacity. Proxy areas use coordinate
units squared; original area charges use their separate audited units. These
two unit systems are never mixed. A surviving area allocation is not a layout.

An independent two-dimensional prefix-sum audit reconstructs all **73,683**
integer forbidden rectangles, verifies the **3,462** cells partition their
complements without overlap, and checks **6,010,396** critical integer cells.
These represent **9,833,243,193,495** mode/anchor combinations, of which
**22,331,274,719** are free. The audit independently reconstructs all **7,840**
outward occupied rectangles and measures their unions with a two-dimensional
array method, separate from construction's vertical interval sweep.

All **33** released source poses are still represented in their restored-part
domains. Nine source files match committed evidence. Every one of **1,152**
allocation inequalities is independently checked. This audit completes in
**{audit['seconds']:.6f} seconds**. All 18 frame cases and ten cog cases are
excluded. The five surviving cog cases are 22, 23, 24, 29 and 31, releasing
items 55, 56, 57, 62 and 64 respectively. Each has exactly one remaining
allocation: the cog and both brackets share sheet 0 in the first four cases
or sheet 1 in case 31.

## Joint three-part feasibility

One model selects exactly one surviving case. In that case the cog and both
brackets are mandatory. Each chooses one of its complete audited free cells,
and all components share the part's position and orientation. A disjunction
of four exact integer separation inequalities handles each of **24** cross-part
component pairs per case. Touching is allowed; no positive original clearance
is added to this necessary proxy check. The fixed63 obstacles are already
represented by the complete free regions. Original area charges are retained.
There are no hints, objectives, copy-order restrictions or optional original
parts.

Construction takes **{model['construction_seconds']:.6f} seconds**. A separate
protobuf oracle reconstructs every field of **1,111 variables and 2,118
constraints**, all **416** free-cell options, **120** component pairs, ten
original-area inequalities and every solver parameter in
**{model['audit_seconds']:.6f} seconds**. It re-reads original cell files instead
of using the model mapping as its expected geometry.

The single declared 60-second, eight-worker, seed-zero call starts search at
0.08 seconds and records `#Done 0.13s probing`. It returns **`INFEASIBLE` in
{solved['seconds']:.6f} seconds**, with 664 branches, 130 conflicts and no
incumbent. The solver reports `LRAT_status: NA`; no separate formal LRAT
certificate is claimed. The entire model and log are preserved. No completed
call is retried or extended.

Combined with the 28 necessary area exclusions, this closes all 33 recorded
single-core relocation neighborhoods. It does not exclude moving additional
parts, changing the finite frame orientation inventory or using another
starting arrangement. No original-outline target witness, native validation,
production-budget qualification or H5 matrix result is produced.

## Next work and repository state

{action}

Production source, all three accurate READMEs and release versions are
unchanged. Main 247e823a's existing run **40233299884** is captured as
`{ci['status']}` / `{ci['conclusion'] or 'pending'}`. No unfinished run is
called a pass. This evidence checkpoint starts at {head[:8]}; accumulated
commits remain local while that run finishes. No held-out file is evaluated
and no release is qualified by these diagnostic results.

Evidence: [region plan]({NAME}/region-plan.json), [complete results]({NAME}/region-result.json),
[independent region audit]({NAME}/region-audit.json), [case audit]({NAME}/case-audit.json),
[solver plan]({NAME}/solver-plan.json), [full model audit]({NAME}/model-audit.json),
[solver result]({NAME}/solver-result.json), [source review]({NAME}/source-review.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']}** canonical members and **{archive['verified_aliases']}**
identical-content aliases retain exact bytes with CRC and SHA-256 verification.
The archive includes every query, every case/allocation, all independent checks,
the complete model and log, source inputs, plans and executed helpers.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 complete single-core relocation exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) covers all33 recorded frame/cog
releases, with63 source poses fixed and the released part plus two brackets
mandatory. All576 queries and3,462 integer free cells audit completely;1,152
exact allocation inequalities exclude28 cases. The other five cog cases have
an independently reconstructed1,111-variable/2,118-constraint model, including
all416 cell options and120 component pairs. One bounded call returns
INFEASIBLE in0.150878 seconds with no incumbent; no LRAT certificate is claimed.
All66 original counts are retained. These33 conditional neighborhoods are
closed; broader coordinated moves remain unresolved. No unrestricted
impossibility, target witness or H5 qualification is claimed. Source, accurate
READMEs and releases are unchanged; H2/H5 remain open at60%.
'''
    # Keep prose readable while preserving compact machine labels above.
    for old,new in [('all33','all 33'),('with63','with 63'),('All576','All 576'),('and3,462','and 3,462'),
                    (';1,152','; 1,152'),('exclude28','exclude 28'),('reconstructed1,111','reconstructed 1,111'),
                    ('all416','all 416'),('and120','and 120'),('in0.150878','in 0.150878'),('All66','All 66'),
                    ('These33','These 33'),('at60%','at 60%')]:note=note.replace(old,new)
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print(checks,flush=True)

if __name__=='__main__':main()
