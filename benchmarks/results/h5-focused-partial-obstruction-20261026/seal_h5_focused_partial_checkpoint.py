"""Preserve two bounded calls, fresh focused constructions and exact obstruction."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-focused-partial-obstruction-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={
 'bottom_model':'h5-free-bottom-cog-source-model-20261026',
 'bottom_search':'h5-free-bottom-cog-source-search-20261026',
 'plot_original':'h5-partial64-bottom-cog-visual-20261026',
 'plot_repaired':'h5-partial64-bottom-cog-visual-repaired-20261026',
 'regions62':'h5-partial62-fixed-regions-20261026',
 'proof_failed':'h5-partial62-capacity-obstruction-20261026',
 'proof62':'h5-partial62-capacity-obstruction-repaired-20261026',
 'regions61':'h5-partial61-fixed-regions-20261026',
 'domains61':'h5-partial61-joint-prepared-20261026',
 'model61':'h5-partial61-source-model-20261026',
 'search61':'h5-partial61-source-search-20261026',
 'review_failed':'h5-partial61-checkpoint-review-20261026',
 'review':'h5-partial61-checkpoint-review-repaired-20261026',
 'sync':'h5-conditional-selection-main-sync-20261026',
 'initial_ci':'h5-bottom-cog-prior-main-check-20261026',
 'later_ci':'h5-bottom-cog-main-readiness-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']==review['main_head']=='679e97e0d7fca4798ba2a1d690c044d72b8f72e2'
    assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
    audits=[('bottom_model','audit/checks.json'),('bottom_search','search-audit/checks.json'),('regions62','audit/checks.json'),('proof62','audit/checks.json'),('regions61','audit/checks.json'),('domains61','audit/checks.json'),('model61','audit/checks.json'),('search61','search-audit/checks.json')]
    assert all(load(base[k]/n)['passed'] for k,n in audits)
    assert load(base['bottom_search']/'search-audit/checks.json')['terminal_status']=='UNKNOWN'
    assert load(base['search61']/'search-audit/checks.json')['terminal_status']=='INFEASIBLE'
    assert load(base['proof62']/'audit/checks.json')['focused62_fixed_source_construction_infeasible']
    receipt=load(base['sync']/'receipt.json');assert receipt['source_head']==review['main_head'] and receipt['previous_ci_successful_jobs']==6
    OUT.mkdir()
    for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
    for k,n,dest in [('proof62','certificate.json','focused62-raw-certificate.json'),('regions61','query-summary.json','fresh61-query-summary.json'),('regions61','prior-three-cog-membership.json','prior-three-cog-membership.json'),('domains61','query-summary.json','fresh61-domain-summary.json'),('model61','result.json','five-mover-model-result.json'),('search61','shared-search/solve/result.json','five-mover-solver-result.json'),('bottom_search','shared-search/solve/result.json','broader-bottom-cog-solver-result.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-679e97e0-snapshot.json'),('sync','receipt.json','main-push-receipt.json'),('sync','prior-ci.json','main-ci-b8535505-passed.json'),('proof_failed','failure-record.json','initial-certificate-failure.json'),('review_failed','failure-record.json','initial-review-failure.json'),('plot_repaired','partial64-first-sheet.png','partial64-first-sheet.png')]:shutil.copyfile(base[k]/n,OUT/dest)
    next_action=('Both solver calls in this checkpoint are CLOSED. The broad54-fixed model with only eight retained non-bracket domains remains UNKNOWN; do not infer infeasibility or retry unchanged. The62-fixed four-mover construction is excluded by an independently verified exact original-geometry certificate. The61-fixed five-mover finite source model is INFEASIBLE, but this is not a raw continuous or unrestricted packing proof. A distinct next construction can release the upper-right bracket27 and cog58 as well as brackets28/29 and cogs53/54/61, based on the inspected verified64-part partial. This gives59 fixed originals and7 mandatory movers (three brackets/four cogs), all66 retained. Rebuild all free regions and inward domains, derive fresh filled-area charges and every physical pair, preserve all native guards and target stock/material bounds. The10 source profiles and original mutual obstacle geometry may be reused only with verified hashes and explicit unused IDs; no54/61/62-fixed domain table, capacity, obstruction or solver exclusion transfers. Rebuild and independently audit whole geometry/model/import before any separately declared bounded search. A full positive still requires original66/90cutout/10026vertex reconstruction, native validation, production integration and the full13-job/two-kerf H5 matrix. Preserve live main679e97e0 CI40267513191 before a normal checkpoint push. H2 retains the original gate and22reserved vectors stay unevaluated.')
    write(OUT/'next-step.json',{'action':next_action,'next_proposed_moving_originals':[27,28,29,53,54,58,61],'next_proposed_fixed_originals':59,'source_partial':'output/h5-insert-cog-partial64-20261026/partial64-placements.json','all_prior_calls_closed':True,'H5_complete':False})
    members={};inputs={}
    for folder in base.values():
        assert folder.is_dir(),folder
        for p in folder.rglob('*'):
            if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
        for p in folder.rglob('plan.json'):
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in load(p).get(field,{}).items():
                    if n in inputs:assert inputs[n]==h,n
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-conditional-selection-and-partial64-20261026','h5-domain-selection-and-triple-certificate-20261026','h5-expanded-cog-neighborhood-20261026','h5-full-original-joint-20261025','h5-source-area-and-direction-sharing-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helpers=['prepare_h5_free_bottom_cog_model.py','audit_h5_free_bottom_cog_model.py','make_h5_free_bottom_cog_runner.py','run_h5_free_bottom_cog_search.py','audit_h5_free_bottom_cog_search.py','plot_h5_insert_cog_partial64.py','plot_h5_insert_cog_partial64_repaired.py','build_h5_partial62_fixed_regions.py','audit_h5_partial62_fixed_regions.py','certify_h5_partial62_capacity_obstruction.py','audit_h5_partial62_capacity_obstruction.py','certify_h5_partial62_capacity_obstruction_repaired.py','audit_h5_partial62_capacity_obstruction_repaired.py','make_h5_partial61_region_helpers.py','build_h5_partial61_fixed_regions.py','audit_h5_partial61_fixed_regions.py','make_h5_partial61_domain_helpers.py','build_h5_partial61_joint_domains.py','audit_h5_partial61_joint_domains.py','make_h5_partial61_model_helpers.py','prepare_h5_partial61_source_model.py','audit_h5_partial61_source_model.py','make_h5_partial61_search_helpers.py','run_h5_partial61_source_search.py','audit_h5_partial61_source_search.py','review_h5_partial61_checkpoint.py','repair_h5_partial61_review_helper.py','review_h5_partial61_checkpoint_repaired.py','push_h5_conditional_selection_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py']
    pending=[ROOT/'output'/n for n in helpers]+[Path(__file__)];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);assert p.is_file(),p;members['helpers/'+p.name]=p;source=p.read_text(encoding='utf-8')
        for name in re.findall(r"['\"]([A-Za-z0-9_.-]+\.py)['\"]",source):
            q=ROOT/'output'/name
            if q.is_file():pending.append(q)
        for node in ast.walk(ast.parse(source)):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'independent_audits_passed':8,'new_closed_solver_calls':2,'broader54_fixed_model_result':'UNKNOWN','focused62_raw_original_geometry_obstruction_verified':True,'focused61_finite_source_model_result':'INFEASIBLE','original_failed_certificate_predicate_preserved':True,'initial_review_workflow_name_failure_preserved':True,'initial_unclipped_plot_preserved':True,'repaired_plot_visually_inspected':True,'both_shared_budgets_honored':True,'broader_solver_soft_overrun_seconds':.42320369998924434,'next_construction_not_run_in_this_checkpoint':True,'production_and_readmes_unchanged':True,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: focused original-geometry obstruction and broader search — 2026-10-26

**Two narrower arrangements are now ruled out within their stated scope; the
broader search remains unresolved. No complete 66-part target layout has been
found. H2/H5 remain open at 60%.** All original parts and gate limits are retained.

## Broader bottom-cog search

Starting from the full 54-fixed source model, free both brackets and both
bottom-strip cogs across all their source choices. Keep eight other non-bracket
domain restrictions and all 60 nonbinding partial hints. One additional clause
excludes both released cogs returning simultaneously to their previous domains.
An independent implication audit restores the exact previously INFEASIBLE
ten-domain model when those two flags are true. This is scoped solver-model
evidence, not a raw-geometry or formal UNSAT certificate.

The complete audit passes: **223,086 variables, 289,925 constraints, 60 hints**,
all 66 originals mandatory. The one call returns **UNKNOWN in 45.423204 solver /
47.721778 shared seconds**. Its 0.423204-second soft overrun is recorded; the
60-second outer budget passes. Actual model, parameters, response and timing
readback pass. This call is closed and supplies no infeasibility claim.

## Exact obstruction with 62 fixed originals

Freeze the independently verified 64-part partial except cogs 53/54, leaving
both missing brackets 28/29 mandatory. Rebuild all 20 free-region queries from
62 original outlines. An independent reconstruction checks **1,414 fixed pairs,
248 stock edges, 82 cutouts and 8,894 cutout vertices**; all 100 cached guarded
profile obstacles are reverified. No old conditional cuts are transferred.

Only bracket queries 0/8 remain nonempty. The two cogs have five small free-space
components in two separate zones. Exact rational checks of all **228 raw cog
collision-boundary segments** establish a strict collision disk and capacity
one in each zone. Both zones must therefore be occupied. For either bracket
orientation, its entire possible position relative to the compulsory left cog
lies strictly inside the raw original collision region. Independent exact
segment clipping and parity check **162 boundary/box cases**. This excludes
completion within this particular 62-fixed, original-angle construction,
without a solver call. The broader 54-fixed construction is not excluded.

An initial helper had an incorrect empty-region assertion and produced no
certificate. Its failure is preserved; a separate corrected construction and
independent audit pass. The original plot with unclipped labels is also retained;
the repaired rendering below was visually inspected. It remains a partial,
not a cutting layout.

![Verified original64 partial; brackets28/29 missing]({NAME}/partial64-first-sheet.png)

## Fresh five-mover construction

Free the adjacent middle cog 61 as well: **61 fixed originals and five mandatory
movers**, original items 28/29/53/54/61. The independent rebuild checks **1,362
fixed pairs, 244 stock edges, 81 cutouts and 8,694 cutout vertices**. All three
prior cog anchors remain represented. The 62-fixed obstruction is not reused.

All 20 queries finish without a construction cap or uncovered raw area.
There are **2,120 raw convex faces, 2,118 inward domains and two recorded
discards**, with 6,954 independently verified inside inequalities. All 82
historical mutual cases retain their original IDs and byte-verified geometry;
73 are used, nine explicitly unused. The unchanged insert queries 16/17 are
computed but unused by the five movers. The full physical inventory has ten
pairs and 230 same-sheet query combinations. Half are impossible because their
empty-query selectors are forced false, leaving **115 active-capable modes**.

Independent whole-model reconstruction and actual solver import pass:
**22,545 variables / 39,619 constraints / 18 advisory hints**. All ten anchor
coordinates remain free; two original-area inequalities are freshly derived.
No prior capacity, domain conflict or conditional exclusion is copied.
The single bounded call returns **INFEASIBLE in 17.065219 solver / 18.006190
shared seconds**, with no overrun. The exact response and model readback pass.
This excludes only this finite 61-fixed source construction, not arbitrary
orientations or unrestricted packing. Both calls in this checkpoint are closed.

The next distinct construction will also release upper-right bracket27 and
cog58, giving 59 fixed originals and seven movers. Every free region, domain,
area charge and applicable pair must be rebuilt and independently checked.
No exclusion from the older fixed arrangements can be transferred silently.
Any positive still requires all **66 originals, 90 cutouts and 10,026 hole
vertices**, native validation and material checks, followed by production
integration and the full 13-job/two-kerf H5 matrix.

## Repository and release state

Previous main b8535505 passes all six jobs in CI40264589776. The verified
conditional-selection checkpoint **679e97e0 is pushed normally to main**.
At {review['utc']}, [its checks](https://github.com/skulitom/Nestbolt/actions/runs/{review['main_ci_id']})
are {review['main_ci_status']} with {review['main_ci_successful_jobs']} jobs passed;
preserve the live run before the next normal push. An initial review selected
an incorrect workflow name; raw results and failure are preserved, and the
separate repaired review uses the observed name, Checks.

Upstream heads and releases are unchanged; no stop rule has triggered. Product
source, READMEs and releases are unchanged. No new release is qualified. H2
retains the original gate and all 22 reserved vectors remain unevaluated.

Evidence: [raw geometric certificate]({NAME}/focused62-raw-certificate.json),
[five-mover readback]({NAME}/search61-search-audit-checks.json),
[checks]({NAME}/checks.json), [next step]({NAME}/next-step.json), and
[raw manifest]({NAME}/raw-manifest.json). **{archive['archive_members']:,}** canonical
files and **{archive['verified_aliases']:,}** aliases are independently checked by
size, SHA-256 and ZIP CRC across **{archive['archive_parts']}** archive parts.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 focused original-geometry obstruction, 2026-10-26:** [the evidence]({link})
retains the broader 54-fixed call as UNKNOWN in 47.721778 shared seconds,
including its 0.423204-second solver soft overrun. A fresh 62-fixed construction
is excluded by exact original-geometry checks: both mandatory cogs must occupy
two separate pockets, and every available bracket position collides with the
left cog. A separate rebuild frees middle cog61, giving five mandatory movers
and 61 fixed originals. All geometry, 2,118 inward domains and the complete
22,545-variable/39,619-constraint model pass independent checks; its one call is
INFEASIBLE in 18.006190 shared seconds. These are conditional results, not an
unrestricted impossibility claim. Both calls are closed and failures retained.
Next also release upper-right bracket27/cog58 and rebuild the 59-fixed geometry.
Main679e97e0 is pushed after all six prior checks passed; its own CI40267513191
is live. H2/H5 remain open at 60%; source, READMEs, releases and the 22 reserved
vectors are unchanged. No complete target layout or new release is qualified.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
