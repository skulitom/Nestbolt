"""Seal both closed formulations and their full original-source readbacks."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-bounded-source-search-20261026';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
OUTER=ROOT/'output/h5-outer-original-search-20261026';OMODEL=ROOT/'output/h5-outer-original-model-20261026';MODEL=ROOT/'output/h5-bounded-source-model-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    oa=load(OUTER/'search-audit/checks.json');geometry=load(OUTER/'original-proposal-audit-repaired/checks.json');om=load(OMODEL/'audit/checks.json');ma=load(MODEL/'audit/checks.json');timing=load(BASE/'search-audit/checks.json');solved=load(BASE/'shared-search/solve/result.json');actual=load(BASE/'shared-search/solve/model-audit.json');prep=load(MODEL/'result.json')
    assert all(r['passed'] for r in [oa,geometry,om,ma,timing,actual]) and oa['failed_original_clauses']==6 and geometry['originally_valid_proposals']==0 and solved['status']=='UNKNOWN' and timing['shared_budget_honored']
    prior=load(ROOT/'benchmarks/results/h5-direct-original-search-20261025/source-review.json');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head=='de7b71fe043966ee853078e60d9e2997ed31ef8e' and mainhead=='728b2db2e86c2d123920fdceb8e3e2c1bcf1f66e'
    ci=json.loads(subprocess.check_output(['gh','run','view','40246226212','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead;write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Both calls remain closed. The necessary outer-cover positive fails six full original source clauses and six original pair-clearance checks, including four large/real overlaps; it is not a native candidate. '
        'The distinct full-source-clause formulation, with every pair rule retained and only exact rectangle-extrema simplification, ends UNKNOWN in 45.471545 seconds, shared 48.583887 seconds. Preserve the 0.471545-second soft-cap overshoot. No feasibility or impossibility claim is justified. '
        'Next investigate whole-domain completion of the independently verified six-cog witness: check all original bracket/insert inward domains against the full original guarded clauses with those six witness positions fixed, using exact rational polygon clipping or independently replayable interval/branch certificates. '
        'The previous finite pose census is not a continuous impossibility proof. Preserve all residual domains, lower-dimensional cases, caps, and unresolved branches. Any proof is conditional on those six positions, source orientations, fixed 57 and source integer domains; it must never exclude those domains in a model where cogs are movable. '
        'If those positions cannot admit both remaining brackets and the insert, identify which source poses or angles must change before another full search. Do not restart, extend or reseed either closed model. Full 66-original geometry/native validation, production-budget integration and the 13-job/two-kerf H5 matrix remain necessary. '
        'H2 remains open under the original gate and 22 reserved vectors remain untouched. Keep main newer work intact; finish its existing CI before the next normal push. No new release is qualified.')
    OUT.mkdir();copies={OMODEL/'result.json':'outer-model-result.json',OMODEL/'audit/checks.json':'outer-model-audit.json',OUTER/'shared-search/budget.json':'outer-search-budget.json',OUTER/'shared-search/result.json':'outer-search-result.json',OUTER/'shared-search/solve/model-audit.json':'outer-search-model-audit.json',OUTER/'shared-search/solve/result.json':'outer-solver-result.json',OUTER/'search-audit/checks.json':'outer-search-audit.json',OUTER/'search-audit/original-clause-failures.json':'outer-original-clause-failures.json',OUTER/'original-proposal-audit-repaired/checks.json':'outer-original-geometry-audit.json',OUTER/'original-proposal-audit-repaired/candidate/pair-failures.json':'outer-original-pair-failures.json',OUTER/'original-proposal-audit-repaired/candidate/area-checks.json':'outer-original-area-checks.json',OUTER/'original-proposal-audit/failure.txt':'outer-initial-geometry-audit-failure.txt',OUTER/'geometry-audit-repair.json':'outer-geometry-audit-repair.json',MODEL/'result.json':'source-model-result.json',MODEL/'transformation.json':'source-model-transformation.json',MODEL/'audit/checks.json':'source-model-audit.json',BASE/'shared-search/budget.json':'source-search-budget.json',BASE/'shared-search/result.json':'source-search-result.json',BASE/'shared-search/solve/model-audit.json':'source-search-model-audit.json',BASE/'shared-search/solve/result.json':'source-solver-result.json',BASE/'search-audit/checks.json':'source-search-audit.json',BASE/'main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(a,OUT/b)
    original_transform=OMODEL/'transformation.json';transform=load(original_transform)
    write(OUT/'outer-model-transformation.json',{'full_record_archive_member':'h5-outer-original-model-20261026/transformation.json','full_record_sha256':digest(original_transform),**{k:len(v) if isinstance(v,list) else v for k,v in transform.items()}})
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','outer_cover_solver_calls':1,'full_source_solver_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,'pushed':False,'current_main_ci_id':40246226212,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for base in [OMODEL,OUTER,MODEL,BASE]:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h,(n,inputs[n],h)
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for previous in ['h5-direct-original-search-20261025','h5-all-original-cell-search-20261025','h5-six-cog-guided-search-20261025']:
        p=ROOT/'benchmarks/results'/previous/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_outer_original_model.py','audit_h5_outer_original_model.py','solve_h5_outer_original_model.py','run_h5_outer_original_search.py','audit_h5_outer_original_search.py','prepare_h5_outer_geometry_audit.py','audit_h5_outer_original_geometry.py','repair_h5_outer_geometry_audit.py','audit_h5_outer_original_geometry_repaired.py','diagnose_h5_lazy_original_proposals.py','prepare_h5_bounded_source_model.py','audit_h5_bounded_source_model.py','run_h5_bounded_source_search.py','prepare_h5_bounded_source_readback.py','audit_h5_bounded_source_search.py','pack_h5_evidence_archive.py','ccd1.py']
    pending=[ROOT/'output'/n for n in names];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'outer_cover_full_transformation_verified':True,'invalid_outer_candidate_preserved_and_rejected':True,'all66_originals_and90_cutouts_reconstructed':True,'failed_no_cutouts_assertion_and_separate_repair_preserved':True,'full_source_clause_equivalence_independently_verified':True,'source_model_unknown_not_infeasible':True,'both_shared_search_budgets_honored':True,'source_solver_soft_cap_overrun_preserved':True,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: rejected outer-cover candidate and complete source-clause search — 2026-10-26

**The relaxed candidate is invalid; the complete source-clause model ends
UNKNOWN.** Neither result establishes a valid 66-original target layout or
packing impossibility. All original counts, material limits and clearance
guards remain unchanged. H2/H5 remain open at **60%** completed milestone weight.

## Complete replacement and relaxed candidate

The preceding checkpoint's necessary outer cover is installed in the audited
table-free model. Remove all **21,819** old safe-cell variables and **116,237**
cell constraints, including **54 empty-cell sums** which otherwise would still
forbid their pair modes. Preserve exactly **10,255 original variables / 57,577
constraints**, all nine movable originals, 57 fixed originals, domains, counts,
areas, coordinates, capacities and proved exclusions. Add all 394 explicit
query-difference bounds and **60,671** outer-box flags. The result has
**70,926 variables / 180,101 constraints**, with 79 advisory hints.

The independent **{om['seconds']:.6f}s** audit reconstructs every removed old
cell equation from its source, inverse-verifies the retained parent fields,
checks every added box and activation, restores the exact complete parent
protobuf, and verifies the actual solver import/export. Every integer
displacement satisfying the original guarded source clauses remains available.
The relaxation is deliberately not a safety certificate.

One eight-worker, seed-zero call, capped at 45 seconds with a ten-second
shutdown reserve inside a shared 60-second budget, returns a candidate in
**{oa['actual_solver_seconds']:.6f}s**, shared **{oa['actual_shared_seconds']:.6f}s**.
No cap overrun occurs. All calls terminate and remain closed.

Readback verifies all nine selected identities and inward domains, copy
ordering, all 394 pair activations and 16 chosen boxes. It checks **633 full
original guarded clauses / 27,362 inequalities**. Six clauses fail for six
different original pairs. Box membership is not accepted as safe geometry.

A separate reconstruction retains all **66 original copies**, checks
**1,540 same-sheet pairs / 264 stock edges**, and reconstructs all **90 original
cutouts / 10,026 cutout vertices** under the original transforms. Maximum
profile disagreement is **5.09e-13 mm**. Both original area constraints pass;
charges are 4,051,952,616 and 429,788,154 lower-area units. Fixed-original
clearances and all stock margins pass. Six moving-original pairs fail:

| Original items | Failure |
|---|---|
| Brackets 28 / 29 | 39,799.450801 mm² filled-outline overlap |
| Bracket 28 / cog 65 | 20,458.099742 mm² filled-outline overlap |
| Bracket 29 / cog 65 | 20,324.858527 mm² filled-outline overlap |
| Insert 50 / cog 57 | 12.686744 mm² filled-outline overlap |
| Cogs 57 / 62 | 0.188978 mm gap; required guard is 0.211709 mm |
| Cogs 64 / 65 | 0.209214 mm gap; required guard is 0.211709 mm |

Filled outer polygons are intentional because part-in-hole remains off. All
internal cutouts are retained in the original library and their transformed
geometry is separately checked. The first new audit incorrectly asserted that
the original shapes had no holes and stopped immediately. Its source, plan and
failure remain preserved; the separate repaired readback removes that false
assumption and verifies the actual cutouts. No source shape, placement, model
or gate is changed by that repair. No invalid candidate is sent to the native
validator.

## Complete source-clause formulation

Replace every outer box and appended pair-cover constraint with the complete
original guarded separation clauses. Preserve the same original variable and
constraint prefix and **72 non-box hints**. For each of the 164 query cases,
derive the full signed displacement rectangle directly from original domain
bounds and evaluate every source halfplane at its four integer corners:

- A face is always satisfied only if one outside edge holds over the whole rectangle.
- An edge is removed only when it cannot hold anywhere in that rectangle.
- A face with no possible edge forbids its active pair; one live edge is imposed directly.
- Otherwise all live edges remain in its conditional OR. Identical directions are shared only within the same physical pair and query mode.

This is exactly equivalent to all original guarded source clauses inside the
recorded source domains. It adds no padding or clearance relaxation. The model
retains all **394 physical pair/mode uses**, covering **8,238 source faces**:
3,818 are proved whole-rectangle tautologies, 2 impossible faces forbid their
pair modes, 5 require one direction, and 4,413 retain full disjunctions.
The result has **167,044 variables / 376,363 constraints**, including 156,789
shared directional flags. No faster runtime is presumed from this formulation.

Preparation takes **{prep['seconds']:.6f}s**. Independent audit takes
**{ma['seconds']:.6f}s**, checking **103 committed source files**,
**218,048 exact corner evaluations**, every retained prefix field, every added
variable/constraint/mapping entry and all hints. Restoring verified additions
to the parent reproduces its full protobuf exactly. Actual solver parsing,
validation and export also agree. Offline preparation/auditing is explicitly
not production-budget qualification.

This differs from the previously closed 181,160-variable full-source call:
it incorporates the subsequently proved domain and regional capacity
exclusions, original copy ordering, explicit difference bounds, exact
whole-rectangle simplification and the independently verified six-cog hints.
It neither restarts nor extends that earlier call.

The new single eight-worker, seed-zero call is capped at 45 seconds, with a
ten-second shutdown reserve in a fresh shared 60-second loading, verification
and search budget. Actual model loading takes **{actual['loading_seconds']:.6f}s**,
equality/parameter verification **{actual['audit_seconds']:.6f}s**. The call
ends **UNKNOWN in {solved['seconds']:.6f}s**; shared elapsed time is
**{timing['actual_shared_seconds']:.6f}s**. The solver exceeds its soft cap by
**{timing['solver_soft_limit_overshoot_seconds']:.6f}s**, preserved explicitly;
the shared budget is honored. There is no incumbent, retry, continuation,
native validation or H5 quality run. UNKNOWN is not an impossibility result.

## Next investigation and repository state

Check whether the verified six-cog witness admits continuous completion by the
missing original brackets and insert across all recorded original domains.
The earlier finite pose census cannot prove that it does not. Use exact rational
clipping or independently replayable interval/branch certificates; retain
lower-dimensional cases, residual domains and caps. Any conclusion is conditional
on those six positions, source angles, fixed 57 and source integer domains, and
must never exclude a domain in a model where the cogs can move. Use that evidence
to choose which source positions or orientations to change before another full
search. Both new calls stay closed.

All H5 requirements remain: 66 original shapes, unchanged material/native
guards, a native-valid layout, production-budget integration and the complete
13-job/two-kerf matrix. H2's original gate and 22 reserved vectors remain intact.

Main 728b2db2 remains preserved. Its own
[CI 40246226212]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful
jobs at this snapshot. The two preceding local checkpoints and this checkpoint
await its terminal outcome before a normal push, reconciling newer remote work
first. Production source, all three accurate READMEs, preview v0.2.0-alpha.1 and
stable Latest v0.1.0 are unchanged. No new release is qualified.

Evidence: [outer transformation]({NAME}/outer-model-audit.json),
[candidate rejection]({NAME}/outer-original-geometry-audit.json),
[full source-model audit]({NAME}/source-model-audit.json),
[closed call readback]({NAME}/source-search-audit.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']} canonical files / {archive['verified_aliases']}
exact-content aliases** have size, SHA-256 and CRC verification, retaining both
models, source files, parameters, logs, candidates, all failures and audits.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 complete source-clause search and rejected relaxation, 2026-10-26:** [the evidence]({link})
verifies complete replacement of all strict safe cells, including 54 empty-cell
sums, by the necessary integer outer cover. Its sole call finds a candidate in
16.162402s, shared 18.195138s; independent full-source and 66-original geometry
readback rejects six moving-pair failures, including four overlaps. All 90
cutouts, original copies/areas, 1,540 same-sheet pairs and 264 stock edges are
checked. The initial false no-cutouts assertion and separate repair are retained.
A distinct complete source-clause model replaces all outer boxes, retains every
original domain/count/area/capacity rule and applies only exact rectangle-bound
simplifications. Its 167,044 variables/376,363 constraints and all 394 pair modes
pass independent reconstruction, 218,048 exact corner evaluations and actual
solver import/export. One 45s-cap call ends UNKNOWN in 45.471545s, shared 48.583887s;
the 0.471545s soft-cap overrun is preserved, the shared 60s budget holds, and no
feasibility/impossibility or native qualification is claimed. Both calls remain
closed. Next test whole-domain completion against the verified six-cog positions
with replayable exact certificates; the previous finite pose census is not a
continuous proof. Any exclusion must remain conditional on fixed witness poses.
H2/H5 stay open at 60%; production, READMEs, releases and 22 reserved H2 vectors
remain unchanged. Main 728b2db2's existing CI is allowed to finish before pushing.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    assert (ROOT/'docs/STATUS.md').read_text(encoding='utf-8').startswith('# Status — 2026-10-26\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
