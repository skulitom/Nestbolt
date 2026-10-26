"""Seal the complete two-cog census and closed conditional source search."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-two-cog-source-focus-20261026';REGROOT=ROOT/'output/h5-two-cog-regions-20261026';REG=REGROOT/'release-7-8';MODEL=ROOT/'output/h5-two-cog-fixed-source-model-20261026';RUN=ROOT/'output/h5-two-cog-fixed-source-search-20261026';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    regions=load(REG/'result.json');ra=load(REG/'audit/checks.json');model=load(MODEL/'result.json');ma=load(MODEL/'audit/checks.json');run=load(RUN/'shared-search/result.json');audit=load(RUN/'search-audit/checks.json')
    assert ra['passed'] and ma['passed'] and audit['passed'] and audit['terminal_status']=='INFEASIBLE' and regions['pending_domains']==0 and not regions['cap_reached']
    prior=load(ROOT/'benchmarks/results/h5-single-cog-obstruction-20261026/source-review.json');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head=='fdb436a7f3ce0c950bc69429bcf3d434c8922212' and mainhead=='822a5f67428e6dfdecab7bcea45e7c89cc31b159'
    ci=json.loads(subprocess.check_output(['gh','run','view','40248595273','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead;success=sum(j['conclusion']=='success' for j in ci['jobs'])
    OUT.mkdir();write(OUT/'main-ci-snapshot.json',ci)
    copies={REG/'result.json':'region-result.json',REG/'summary.json':'region-query-summary.json',REG/'audit/checks.json':'region-audit.json',REG/'audit/conditional-region-summary.json':'conditional-regions.json',MODEL/'result.json':'model-result.json',MODEL/'audit/checks.json':'model-audit.json',MODEL/'runner-preparation-recovery.json':'runner-preparation-recovery.json',RUN/'shared-search/result.json':'shared-search-result.json',RUN/'shared-search/solve/result.json':'solver-result.json',RUN/'shared-search/solve/model-audit.json':'actual-model-audit.json',RUN/'search-audit/checks.json':'closed-search-audit.json'}
    for a,b in copies.items():shutil.copyfile(a,OUT/b)
    action=('The distinct two-second-sheet-cog focus (original64/65,parts7/8) is closed INFEASIBLE after one5.966434s call,9.166805s total. Preserve this solver negative; it is not an independent unrestricted geometry proof. Do not restart, extend or reseed it. Next investigate a distinct first-sheet two-cog release: original57/58,parts4/5, keeping cog54/62/64/65 (parts3/6/7/8) and57 source originals fixed. Both brackets28/29,insert50 and both released cogs remain mandatory: five movers,61 fixed originals. Prepare all20 original query regions and3523 source domains against those four fixed cogs, with correct signed original pair direction and all rational boundaries. Both released cogs have the same ordering against fixed3/6/7/8; verify rather than assume their shared domains. Never transfer the single-cog obstruction or this fixed64/65 solver negative into that model. Append only audited region exclusions and exact fixed coordinates to a fully verified full-source model; preserve original counts/areas/guards/material target and document inherited copy ordering. Audit before any new bounded one-shot call. A positive needs full66-original source/geometry/native validation, then production integration and full13-job/two-kerf H5 matrix. Offline preparation does not qualify a production-budget pass. H2 remains open under its unchanged gate with22 reserved vectors untouched. Wait for terminal main CI before the next normal push, preserving remote changes; no new release is qualified.')
    write(OUT/'next-step.json',{'action':action,'next_released_parts':[4,5],'next_released_originals':[57,58],'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','new_solver_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,'current_main_ci_id':40248595273,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for base in [REGROOT,MODEL,RUN]:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in load(ROOT/'output/h5-single-cog-release-20261026/audit-recovered/witness-source-provenance.json')['inputs'].items():inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for priorname in ['h5-bounded-source-search-20261026','h5-guarded-cell-search-20261025']:
        p=ROOT/'benchmarks/results'/priorname/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    p=ROOT/'output/h5-fixed-six-completion-20261026/audit/provenance-repair.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_two_cog_region_helpers.py','prove_h5_two_cog_regions.py','audit_h5_two_cog_regions.py','prove_h5_focused_other_regions.py','audit_h5_focused_other_regions.py','prepare_h5_two_cog_fixed_source_model.py','audit_h5_two_cog_fixed_source_model.py','prepare_h5_two_cog_search_runner.py','run_h5_two_cog_fixed_source_search.py','run_h5_bounded_source_search.py','audit_h5_two_cog_fixed_source_search.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'all3523_two_cog_domain_cases_independently_replayed':True,'complete_parent_model_preserved':True,'all6372_appended_constraints_independently_verified':True,'actual_model_and_parameters_verified':True,'one_completed_search_closed':True,'pre_search_runner_prose_substitution_failure_preserved':True,'independent_negative_proof_claimed':False,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: focused movement of both second-sheet cogs — 2026-10-26

**The distinct five-mover source model returned INFEASIBLE in
{audit['actual_solver_seconds']:.6f}s**, with {audit['actual_shared_seconds']:.6f}s
total import/audit/search time. This is a conditional solver negative with all
parent construction restrictions retained, not an independent proof of
unrestricted packing impossibility. H2/H5 remain open at **60%**.

## Complete source regions

Release original cogs **64/65** while keeping cogs **54/57/58/62** at their
verified first-sheet poses and the other 57 source placements fixed. Both
brackets 28/29, insert 50 and both released cogs remain mandatory: **five
movers, 61 fixed originals, 66 total**.

Exact rational clipping examines all **20 original queries / 3,523 inward
domains** in **{regions['seconds']:.6f}s**. All domains finish, with no cap or
pending work. **173** domains retain **261** convex fragments. Both brackets
and both released cogs have regions only on the second sheet; the insert has
one domain on each sheet (89 first-sheet fragments, one second-sheet fragment).
Both released cogs follow the four fixed cogs in original part order, so their
source inequalities and domains are identical; each remains a separate part.

An independent replay takes **{ra['seconds']:.6f}s** and verifies all **991**
changed-clause events, **10,044,240** exact integer corner values, full source
clauses, complete inventories and all closed rational boundaries. No source
angle, geometry, count, guard or material target changes.

## Focused complete-source model and sole call

Preserve every variable, constraint and hint of the previously audited
167,044-variable complete source model. Append **eight** exact coordinate
equalities for the retained cog poses and **6,364** zero equalities for domain
flags proved empty by the new census. Retain all **344** nonempty physical
domain flags across the five movers. The resulting model has **382,735
constraints** and all **72** advisory hints. Every original count, area rule,
full guarded pair clause and parent copy-order restriction remains present.
No single-cog conditional obstruction is reused.

The independent audit removes only the appended constraints and recovers the
entire parent protobuf exactly; it reconstructs every new restriction from
the witness and complete source inventory. Actual solver import/export also
matches. This audit takes **{ma['seconds']:.6f}s**.

One search uses eight workers, seed zero, a 45-second solver cap and a shared
60-second import/audit/search budget with a ten-second shutdown reserve.
It returns **INFEASIBLE in {audit['actual_solver_seconds']:.6f}s**, total
**{audit['actual_shared_seconds']:.6f}s**. No candidate is produced, so no native
validation is attempted. The terminal readback verifies model hashes, every
parameter, timing, the sole call and absence of a positive. The call is closed;
it will not be restarted, extended or reseeded. No independent negative tree
is claimed for this solver result.

The runner's initial preparation stopped before creating a runner because a
prose substitution named a sentence belonging to the model preparer. Its
source and failure/recovery record are retained. Removing that absent prose
substitution leaves all runtime substitutions unchanged. No region/model
computation or solver call was repeated.

## Next case and repository state

Investigate a distinct first-sheet pair: original cogs **57/58**, retaining
cogs **54/62/64/65** and the 57 source placements. Rebuild and audit the full
conditional regions with correct source pair direction before another focused
model. Do not transfer this negative or any single-cog obstruction into the
new case. All 66 originals, native guards and material target remain required.

Offline preparation is diagnostic, not a production-budget pass. H5 still
needs a complete native-valid target, production integration and the full
13-job/two-kerf matrix. H2 keeps its original gate and all 22 reserved vectors.
Product source, READMEs, preview v0.2.0-alpha.1 and stable Latest v0.1.0 remain
unchanged; no new release is qualified.

Current main 822a5f67 [CI 40248595273]({ci['url']}) is **{ci['status']}**, with
**{success}/6** successful jobs at this snapshot. The local proof/search
checkpoints wait for this run to finish before the next normal main push.

Evidence: [region audit]({NAME}/region-audit.json),
[model audit]({NAME}/model-audit.json),
[closed search]({NAME}/closed-search-audit.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']:,}** canonical files and
**{archive['verified_aliases']:,}** exact-content aliases are verified by
size, SHA-256 and CRC.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 two-cog focused source search, 2026-10-26:** [the retained result]({link})
releases original cogs64/65, preserving both brackets, insert and every original
part (five movers,61 fixed). All3,523 original domain cases finish exact clipping
and independent replay;173 domains/261 fragments remain. Both brackets and
released cogs must use the second sheet in these source conditions. The full
parent model is preserved exactly, with eight fixed-coordinate equalities and
6,364 independently verified empty-domain exclusions appended. One bounded
call returns INFEASIBLE in5.966434s,9.166805s total; actual model/parameters and
terminal state pass readback. This conditional solver negative is not an
independent unrestricted geometry proof, and the call is closed. Next examine
first-sheet cogs57/58 with new regions and correct pair ordering. No previous
conditional obstruction may be transferred. The pre-search prose-substitution
failure and recovery are preserved; no solver repeated. Production integration,
full original/native target and complete H5 matrix remain required. H2/H5 stay
open at60%; original limits, production, READMEs, releases and22 reserved H2
vectors are unchanged. Main CI40248595273 is tracked before the next normal push.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
