"""Seal expanded contact geometry, equivalent conflict models, bounded solver outcomes and runtime diagnosis."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];RUN=ROOT/'output/h5-contact-placement-selection-20261018';CRASH=ROOT/'output/h5-contact-cpsat-20261018';CP=ROOT/'output/h5-contact-cpsat-cpython-20261018';OUT=ROOT/'benchmarks/results/h5-contact-selection-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();generation=load(RUN/'generation.json');model=load(RUN/'model.json');audit=load(RUN/'audit/checks.json');cp_audit=load(CP/'audit/checks.json');results={name:load(RUN/name/'result.json') for name in ['solve','solve-warm','solve-no-presolve']};cp_result=load(CP/'result.json')
    assert audit['complete'] and cp_audit['complete'] and not cp_audit['complete_target_witness'] and cp_result['status']=='UNKNOWN'
    assert generation['candidates']==8798 and generation['contact_additions']=={'bracket':900,'cog':900,'frame':900,'insert':900} and not generation['generation_expired']
    assert model['conflict_edges']==audit['conflict_edges_verified']==2517051 and model['all_conflict_constraints']==audit['equivalent_cliques_verified']==17097
    assert all(r['status']==1 and r['missing']=={'cog':3} for r in results.values())
    for phase in ['warm','no-presolve']:
        assert load(RUN/('audit-'+phase)/'checks.json')['selected_layout_bytes_unchanged']
        assert (RUN/('solve-'+phase)/'selected-layout.json').read_bytes()==(RUN/'solve/selected-layout.json').read_bytes()
    assert (CP/'model.pbtxt').read_bytes()==(CRASH/'model.pbtxt').read_bytes() and (CP/'requirements.txt').read_bytes()==(CRASH/'requirements.txt').read_bytes()
    assert load(CRASH/'runtime-diagnosis/result.json')['unsigned_windows_code']=='0xc0000005' and load(CP/'probe/result.json')['succeeded']
    assert source_digest()==audit['production_digest']==cp_audit['production_digest']=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    ci=json.loads(subprocess.check_output(['gh','run','view','39140860263','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']=='5743a321562422e838be8cfd2f7e70be3d5e7671' and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs']);write(OUT/'main-ci-5743a32.json',ci)
    next_step=('The expanded finite pool and its entire physical conflict graph are now audited. The original '
        'partial remains the only returned layout: no native or offline full target witness is established. '
        'Do not repeat these unchanged models or extend their declared limits. CP-SAT now has a working '
        'isolated standard-CPython runtime, but its full-inventory status is UNKNOWN, not infeasible. '
        'Next construct coherent multi-cog components directly from the original filled outer geometry: '
        'use two-phase alternating lattices with pitches derived from actual horizontal/vertical '
        'Minkowski contacts, verify every pair and allowed rotation, and record finite phase/offset choices '
        'before running. Try fitting these coordinated groups with the retained frame allocations and '
        'original bracket/insert inventory, preserving stock and the original material target. Component '
        'checks remain component checks; only all 66 original copies passing both original CLI and '
        'filled-outer validation constitute a witness for this case. Do not infer that a cog bounding-box '
        'or area improvement proves the whole job fits. Use exact-count selection with the working '
        'runtime only after a materially different construction supplies useful coordinated candidates. '
        'Native margins, production-budget qualifications, the four-step repair cap and the full H5 '
        'matrix still apply before integration or gate credit.')
    write(OUT/'source-review.json',{'next_investigation':next_step,'runtime_and_production_unchanged':True,'native_packing_calls':0,'quality_runs':0,'full_target_witnesses':0,
        'independent_candidate_geometry_and_graph_complete':True,'all_expired_and_failed_outcomes_preserved':True,'CP_SAT_status_is_not_infeasibility':True,'presolve_off_only_improves_root_relaxation_progress':True,
        'original_CPSAT_native_exit_unknown':'Original wrapper returned exit 1 after 6.086 seconds with no solver result or Python exception record. Do not invent its underlying native code; the independent two-variable probe records 0xc0000005.',
        'runtime_recovery_scope':'Standard CPython 3.13.9 with its corresponding official wheel passes the identical tiny probe; all package versions stay equal. This does not isolate whether the original interpreter build, Python ABI, wheel or their environment caused the access violation.',
        'production_digest':source_digest(),'readmes_unchanged':{p:digest(ROOT/p) for p in ['README.md','README.ja.md','README.zh-CN.md']},'H5_complete':False,'completion_percent':60})
    members={}
    def add(path,name):
        assert '.claude' not in path.parts
        if name in members:assert digest(members[name])==digest(path)
        else:members[name]=path
    for phase in [RUN,CRASH,CP]:
        for p in sorted(phase.rglob('*')):
            if p.is_file():add(p,phase.name+'/'+p.relative_to(phase).as_posix())
    for name in load(RUN/'plan.json')['sources']:
        p=ROOT/name;add(p,'source-inputs/'+p.relative_to(ROOT/'output').as_posix())
    helpers=['build_h5_contact_selection.py','solve_h5_contact_selection.py','audit_h5_contact_selection.py','prepare_h5_contact_warm_start.py','solve_h5_contact_selection_warm.py','audit_h5_contact_selection_warm.py',
        'check_h5_contact_followup.py','prepare_h5_contact_no_presolve.py','solve_h5_contact_selection_no_presolve.py','prepare_h5_contact_cpsat.py','solve_h5_contact_cpsat.py','diagnose_h5_cpsat_runtime.py',
        'prepare_h5_cpsat_cpython.py','solve_h5_contact_cpsat_cpython.py','audit_h5_contact_cpsat.py','diagnose_h5_concave_gaps.py']
    for name in helpers:add(ROOT/'output'/name,'helpers/'+name)
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'generation':generation,'model':model,'geometry_audit':audit,'MIP_outcomes':results,'CP_SAT_outcome':cp_result,'CP_SAT_audit':cp_audit,
        'runtime_probe_failure':load(CRASH/'runtime-diagnosis/result.json'),'runtime_probe_recovery':load(CP/'probe/result.json'),'archive_members':len(manifest),'archive_sha256':digest(archive),'main_5743a32_all_six_checks_pass':True,'runtime_changed':False,'production_digest':source_digest(),'H5_complete':False,'completion_percent':60})
    shutil.copyfile(__file__,OUT/'seal_h5_contact_selection.py')
    doc=f'''# H5: expanded contact placements and exact-inventory selection — 2026-10-18

The new contact pool is independently verified, but **no complete target layout
is found**. The retained valid partial still has 63 of 66 original parts, missing
three cogs. The full-inventory CP-SAT attempt ends **UNKNOWN** at its time limit;
that is not an infeasibility result. H5 remains open.

The [previous saved-pose selection](h5-saved-placement-selection-20261018.md)
suggested generating contact locations beyond the beam's three lowest choices.
This construction keeps its 2,614 candidates, adds 2,584 distinct half-turns about
their original target-sheet centres, and generates **3,600 new original-outline
contacts**, 900 per family. It uses the 63 selected old poses and their half-turns
as 126 anchors, with all applicable quarter-turn/reflection templates and cog
phases 0°, 4.5°, 9° and 13.5°. Conservative Minkowski boundaries and stock-domain
intersections provide points spread around entire contact rings. Unrounded
coordinates are retained; every admitted contact is clear of its generating
anchor. The result has **8,798 candidates**, below its declared 8,828 cap.

Generation completes in **18.965 seconds**, without its 120-second contact-query
limit firing. Actual filled-outer geometry defines **2,517,051 conflicting pairs**.
Pairwise verified cliques compress these into **17,097** binary exclusions in
16.051 seconds, below the 30-second compression ceiling. Every original conflict
edge is covered and every clique member pair is an actual edge, making the binary
model exactly equivalent. The known partial remains a feasible model certificate.

Independent source reconstruction checks all 8,798 unrounded poses, original
stock targets, allowed rotations/reflections and all 3,600 anchor contacts. An
independent bounding-box enumeration visits **29,902,803** same-sheet candidate
pairs and evaluates **2,822,033** original-polygon distances. It reproduces the
entire 2,517,051-edge graph exactly, without the producer's spatial index, then
checks every clique and complete edge coverage. All **1,303** selected-part pairs
of the retained partial pass; the original public CLI rejects only cog quantity.

Three serial, separately recorded MILP mechanism attempts use the same model and
120-second allowance. The first has no starting incumbent; the second explicitly
supplies the independently valid full binary vector; the third changes only
presolve from its default to off. The bundled HiGHS 1.12.0 model arrays are checked
against the same matrix, objective, bounds and integrality before solving.

| Attempt | Actual seconds | Solver outcome | Returned inventory |
| --- | ---: | --- | --- |
| SciPy interface, no incumbent input | 120.181630 | time limit, no incumbent | unchanged partial fallback |
| Explicit verified incumbent | 120.096101 | time limit, feasible incumbent retained | 63/66, three cogs missing |
| Same incumbent, presolve off | 124.519761 | time limit, feasible incumbent retained | 63/66, three cogs missing |

The time-limit overrun is retained, not rounded down. In the warm-start attempt,
presolve finishes at about 79 seconds; the first search line appears at 81.7
seconds. It increases nonzeros from **681,124 to 1,627,667**, and the root
relaxation does not finish. With presolve off, the first relaxation completes at
2.2 seconds and the solver spends its remaining allowance on cuts and heuristics,
but finds no better selection. These are local diagnostic observations, not
production speed or H5 evidence. Both returned layouts are byte-identical to the
already audited partial; those geometry checks are reused by exact hashes rather
than rerun. The bounds do not establish global geometric feasibility or impossibility.

A distinct [CP-SAT feasibility model](https://developers.google.com/optimization/cp/cp_solver)
then requires **all 66 parts exactly**, with the same 17,097 conflict cliques and
no partial-coverage objective or rounded area coefficients. The 63 known positions
are nonbinding positive hints. A single attempt uses seed 0, eight offline CCD1
workers and a [120-second limit](https://developers.google.com/optimization/cp/cp_tasks).
Pinned [OR-Tools 9.15.6755](https://pypi.org/project/ortools/9.15.6755/) runs only in
isolated diagnostic environments; no production dependency is added.

The first environment, based on Anaconda Python 3.11.5, terminates before returning
a solver status. Its wrapper exit is 1; no packing result is invented. A separate
two-variable, one-worker probe records a native **0xc0000005 access violation** at
the solve call. The complete original model, empty solver log and failing probe
remain preserved. A fresh environment from installed standard CPython 3.13.9,
with **every package version unchanged**, passes the identical tiny probe. Both
official Windows wheel hashes are checked. This local recovery does not identify
which interpreter, ABI, wheel or environment difference caused the crash.

The recovered run must export the **exact same model bytes** before solving. It
starts search after 4.07 seconds, but ends **UNKNOWN** after 120.185060 real seconds,
returning no complete selection. The saved response reports 36,530 branches and
27 conflicts. An independent parser verifies all 8,798 Boolean domains, all
17,097 literal lists, all four exact original-quantity equalities, and precisely
63 nonbinding hints. It verifies that there is no hidden partial objective or
additional model constraint. Neither the crash nor UNKNOWN is a packing result
or a proof of infeasibility.

[Checks](h5-contact-selection-20261018/checks.json),
[all raw geometry, models, logs, failures, environments' metadata and audits](h5-contact-selection-20261018/raw.zip),
[manifest](h5-contact-selection-20261018/raw-manifest.json),
[next investigation](h5-contact-selection-20261018/source-review.json).
All {len(manifest)} archive members, CRCs and byte hashes verify. Installed runtime
binaries are not included in the evidence archive; pinned package versions,
download provenance and wheel hashes are retained.

{next_step}

All six hosted checks on main `5743a32` pass ([record](h5-contact-selection-20261018/main-ci-5743a32.json));
that is the preceding pushed revision. Production source, all gate limits,
preview assets and all three accurate READMEs remain unchanged. H2/H5 stay open
at **60%**. No new native packing or quality run, runtime integration, release
qualification or gate credit is claimed.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 expanded contact selection, 2026-10-18:** [8,798 verified poses](../benchmarks/results/h5-contact-selection-20261018.md)
include 3,600 new outline contacts and sheet half-turns. Independent enumeration
of 29,902,803 pairs reproduces all 2,517,051 conflicts and verifies the equivalent
17,097-clique model. Three bounded MILP mechanism attempts preserve their timeouts
and the same 63-part partial. Disabling expensive presolve reaches the first
relaxation quickly but gives no better layout. Exact-inventory CP-SAT requires all
66 parts; its initial runtime crash and failing tiny probe are retained. Standard
CPython, with the same package versions, passes the probe and solves the identical
model bytes to UNKNOWN at 120 seconds, returning no complete layout. Independent
model parsing verifies every exact quantity and nonbinding hint. Next investigate
coordinated multi-cog components from actual contacts, retaining full original-job
validation before any feasibility claim. All six prior main `5743a32` checks pass.
No native quality run, runtime, gate, release or README change; H2/H5 remain at 60%.
'''
    prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==prior;append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 joint saved-placement selection, 2026-10-18:**';assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-contact-selection-20261018/** -text -whitespace\n');print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'full_target_witnesses':0}),flush=True)
if __name__=='__main__':main()
