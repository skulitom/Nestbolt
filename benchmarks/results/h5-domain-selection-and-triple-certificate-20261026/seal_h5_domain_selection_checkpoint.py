"""Seal fresh conflicts, exact selected-domain results and independent triple geometry."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-domain-selection-and-triple-certificate-20261026';OUT=ROOT/'benchmarks/results'/NAME
folders={'conflict_model':'h5-projected-conflict-model-20261026','conflict_search':'h5-projected-conflict-search-20261026','convex':'h5-expanded-convex-conflicts-20261026','master':'h5-expanded-domain-master-20261026','master_search':'h5-expanded-domain-master-search-20261026','selected':'h5-selected-expanded-model-20261026','selected_search':'h5-selected-expanded-search-20261026','pairs':'h5-selected-pair-census-20261026','triples':'h5-selected-triple-census-20261026','certificate':'h5-selected-triple-collision-certificate-20261026','review':'h5-domain-selection-source-review-20261026','sync':'h5-projected-checkpoints-main-sync-20261026'}
paths={k:ROOT/'output'/v for k,v in folders.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
def main():
    review=load(paths['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']==review['main_head']=='6a27fec0e549bd39cbfcf597aecacf16816d1cfc';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items());ci=json.loads(load(paths['review']/'main-ci-later.json')['stdout']);assert ci['headSha']==review['main_head'] and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    audits=[('conflict_model','audit/checks.json'),('conflict_search','search-audit/checks.json'),('convex','audit/checks.json'),('convex','groups/audit/checks.json'),('convex','copy-symmetry/checks.json'),('master','audit/checks.json'),('master_search','selection-audit/checks.json'),('selected','audit/checks.json'),('selected_search','search-audit-repaired/checks.json'),('pairs','model-audit/checks.json'),('pairs','response-audit/checks.json'),('triples','model-audit/checks.json'),('triples','response-audit/checks.json'),('certificate','audit/checks.json')]
    assert all(load(paths[k]/n)['passed'] for k,n in audits);assert load(paths['conflict_search']/'search-audit/checks.json')['terminal_status']=='UNKNOWN';assert load(paths['selected_search']/'search-audit-repaired/checks.json')['terminal_status']=='INFEASIBLE';assert load(paths['pairs']/'response-audit/checks.json')['closed_calls']==46;assert load(paths['triples']/'response-audit/checks.json')['closed_calls']==120;OUT.mkdir()
    for k,n in audits:shutil.copyfile(paths[k]/n,OUT/(k+'-'+n.replace('/','-')))
    copies=[('convex','result.json','convex-refinement-result.json'),('master_search','selection-audit/verified-domain-selection.json','necessary-domain-selection.json'),('selected_search','shared-search/result.json','selected-domain-search-result.json'),('selected_search','search-audit/failure.txt','initial-readback-failure.txt'),('pairs','response-audit/verified-pair-witnesses.json','verified-pair-witnesses.json'),('triples','response-audit/conditional-negative-triples.json','conditional-negative-triples.json'),('certificate','certificate.json','raw-triple-certificate.json'),('certificate','audit/exact-box-checks.json','raw-triple-exact-box-checks.json'),('review','review.json','source-review.json'),('review','main-ci-later.json','main-ci-6a27fec0-success.json'),('sync','receipt.json','previous-main-push-receipt.json')]
    for k,n,dest in copies:shutil.copyfile(paths[k]/n,OUT/dest)
    next_action=('All169 diagnostic calls in this checkpoint are CLOSED. No restart/extension/reseed. The necessary master selection was not a full layout; its exact-coordinate subproblem is INFEASIBLE for that selected12-domain tuple only. All46 selected pairs have verified source witnesses. Of120 triple calls87 have checked witnesses,32 remain UNKNOWN, and one is conditionally INFEASIBLE. Independently of that solver conclusion, exact-rational raw geometry proves: if original insert part2/item50 selects query16 row0, at most one of the nine moving identical-profile cogs may select query18 row3. The proof applies to all36 cog-copy pairs and respects necessary-master family symmetry. Next append only sum(cog-domain-row3 flags for parts3..11)+8*(insert-query16-row0 flag)<=9 to the intact audited necessary master (17039variables/9793constraints/36hints), giving9794constraints. Independently replay the raw certificate, variable mapping, complete retained parent and import/export before a separately declared bounded call. Do not transfer old fixed57 cuts, generalize to unproved domains, or use UNKNOWN triples as exclusions. Each new domain selection needs a separately declared exact full-source coordinate subproblem. A positive still requires full66original outlines/90holes/10026holevertices, original stock/pair/material guards and native validation, then production integration and full13-job/two-kerf H5 matrix. All six checks for main6a27fec0 CI40261923411 pass, permitting a normal push. H2 original gate and22 reserved vectors unchanged.')
    write(OUT/'next-step.json',{'action':next_action,'raw_certificate':(paths['certificate']/'certificate.json').relative_to(ROOT).as_posix(),'necessary_master':paths['master'].relative_to(ROOT).as_posix(),'full_source_parent':'output/h5-projected-expanded-model-20261026','required_originals':66,'moving_originals':12,'fixed_originals':54,'H5_complete':False})
    members={};inputs={}
    for base in paths.values():
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in load(p).get(field,{}).items():
                    if n in inputs:assert inputs[n]==h,n
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    # Preserve every matrix/core used by the refinement, including explicit hash maps.
    for folder in ['h5-expanded-cog-joint-prepared-20261026','h5-expanded-domain-conflicts-20261026']:
        base=ROOT/'output'/folder
        for p in base.rglob('*'):
            if p.is_file():members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for name in ['h5-expanded-cog-neighborhood-20261026','h5-expanded-source-search-20261026','h5-projected-source-and-fresh-conflicts-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_projected_conflict_model.py','audit_h5_projected_conflict_model.py','make_h5_projected_conflict_runner.py','run_h5_projected_conflict_search.py','audit_h5_projected_conflict_search.py','make_h5_expanded_convex_conflict_helpers.py','build_h5_expanded_convex_conflicts.py','audit_h5_expanded_convex_conflicts.py','make_h5_expanded_convex_group_helpers.py','prepare_h5_expanded_convex_groups.py','audit_h5_expanded_convex_groups.py','audit_h5_expanded_master_copy_symmetry.py','prepare_h5_expanded_domain_master.py','audit_h5_expanded_domain_master.py','run_h5_expanded_domain_master.py','audit_h5_expanded_domain_selection.py','prepare_h5_selected_expanded_model.py','audit_h5_selected_expanded_model.py','make_h5_selected_expanded_runner.py','run_h5_selected_expanded_search.py','audit_h5_selected_expanded_search.py','audit_h5_selected_expanded_search_repaired.py','prepare_h5_selected_pair_census.py','audit_h5_selected_pair_census.py','run_h5_selected_pair_census.py','audit_h5_selected_pair_responses.py','prepare_h5_selected_triple_census.py','audit_h5_selected_triple_census.py','run_h5_selected_triple_census.py','audit_h5_selected_triple_responses.py','certify_h5_selected_triple_collision.py','audit_h5_selected_triple_collision.py','review_h5_domain_selection_checkpoint.py','push_h5_projected_checkpoints.py','pack_h5_evidence_archive.py','ccd1.py','run_h5_projected_expanded_search.py','audit_h5_projected_expanded_search.py','build_h5_convex_domain_conflicts.py','audit_h5_convex_domain_conflicts.py']
    # Generator source names are retained when present; imports are followed exactly.
    pending=[ROOT/'output'/n for n in names if (ROOT/'output'/n).is_file()];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    members['helpers/'+Path(__file__).name]=Path(__file__);archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'independent_audits_passed':len(audits),'diagnostic_calls_closed':169,'full_conflict_search_unknown':True,'necessary_selection_verified_but_exact_selected_coordinates_infeasible':True,'all46_pair_witnesses_verified':True,'triple_calls':120,'triple_witnesses_verified':87,'triple_unknowns_preserved':32,'one_conditional_negative_triple':True,'independent_exact_raw_geometry_certificate':True,'certificate_applicable_cog_copy_pairs':36,'initial_readback_failure_and_repaired_audit_preserved':True,'all_shared_budgets_honored':True,'soft_limit_overshoots_preserved':True,'required_originals':66,'moving_originals':12,'fixed_originals':54,'production_and_readmes_unchanged':True,'prior_main_ci_six_jobs_success':True,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: domain selection and a verified three-part collision — 2026-10-26

**A necessary domain selection fails the exact coordinate check. A complete pair
census and bounded triple census isolate a three-part conflict, now proved
independently from raw original geometry.** H2/H5 remain open at **60%**.

All 66 originals remain mandatory: 12 movable and 54 fixed. The target,
material accounting, native clearance and stock guards remain unchanged.
No full target layout or production qualification is claimed.

## Fresh conflicts and necessary selection

Adding the previously verified fresh box conflicts to the complete projected
source model gives 227,096 variables / 298,613 constraints / 54 advisory hints.
The complete retained-parent and appended-constraint audit passes. Its single
call returns UNKNOWN in **45.886847 solver / 48.814108 shared seconds**. The
0.886847-second soft-limit overrun is retained; the 60-second outer budget passes.

Separately, the complete convex-domain refinement checks all **5,489,250**
previously unmarked pairs and adds **27,798** exclusions, for **3,976,093** total.
The independent audit encloses actual vertices in exact outward integer boxes
and verifies every added whole difference hull against the raw original collision
core. All old bits remain; no unmarked pair is called feasible. Exact grouping
represents **25,543,004 physical uses** with 4,275 auxiliaries and 5,418 nonzero
group constraints. The full census still contains 9,437,545 pairs / 164 cases.

A necessary Boolean master keeps every original mandatory, all domain/query
choices, the fresh conflict groups, original area rules and fresh second-sheet
cog capacity of two. Nine copy-choice orders are justified for this master only
by a separate 6,418,067-bit symmetry replay; no symmetry of the full coordinate
model is assumed. Every variable and constraint is independently reconstructed:
**17,039 variables / 9,793 constraints / 36 advisory hints**.

Its sole call finds an OPTIMAL satisfaction assignment in **4.426261 solver /
7.127817 shared seconds**. This means only a feasible assignment of necessary
domain conditions, not a complete packing or material optimum. Readback checks
all 17,039 values / 9,793 constraints and the 46 selected same-sheet conflict bits.

## Exact selected coordinates and diagnosis

The coordinate subproblem retains the entire projected full-source parent,
adds exactly 12 domain-selector equalities and clears its 54 unrelated hints.
All 24 original coordinate variables remain free within the selected domains;
all 538 full source pair modes remain. Independent retained-parent/import checks
pass for **223,086 variables / 289,928 constraints / zero hints**.

The single call is **INFEASIBLE** in **2.839067 solver / 5.111598 shared seconds**.
This excludes only that exact twelve-domain tuple. It does not prove the wider
12-mover problem impossible. The first readback helper failed because it looked
for a parent rules file in the child directory. That failure and helper are
preserved; a separate repaired auditor reads the hash-bound original rules and
verifies the unchanged model, response, parameters and timing without reopening
the solver.

All **46** selected same-sheet pair subproblems are separately reconstructed
and audited before one bounded call each. All return checked source-pair witnesses
within **4.380634 total shared seconds**; no pair takes over its one-second limit.
Readback verifies 82,760 variable values, 4,469 active constraints, 357 source
inside planes and 1,918 complete guarded face clauses. These witnesses use
different coordinates and cannot be combined into a layout.

All **120** same-sheet triple models conjoin three audited pair models, sharing
exactly the six original coordinates. The independent audit restores all 360
parent pair models exactly and checks real import/export. The declared census
opens one 0.25-second call per triple, one worker and seed zero, within a shared
60-second budget. It completes in **21.802980 shared seconds**: **87** checked
source-triple witnesses, **32 UNKNOWN**, and **one conditional INFEASIBLE**.
All 32 small soft-limit overruns are retained; the largest is 0.019647 seconds.
No unresolved triple is converted into an exclusion.

## Independent raw-geometry certificate

The negative triple is insert **50** in query 16 / domain row 0, with cogs
**53 and 54** both in query 18 / row 3. Each pair separately fits. An independent
geometric argument proves the triple conflict without relying on solver status:

1. Rechecking all 228 raw cog/cog boundary segments with exact rational arithmetic
   proves the original collision disk. The cog strip permits at most 5.125 mm
   vertical separation, forcing at least **258.032 mm horizontal separation**.
2. Order the two cog anchors by x. They must occupy a left and a right bounding
   box. Split the insert's entire integer x interval into two adjacent halves.
3. Every insert anchor in the left half collides with every possible left cog;
   every anchor in the right half collides with every possible right cog. An
   independent exact-rational audit checks all **128 raw boundary/rectangle
   combinations** and interior ray parity to certify both complete collision
   boxes. No sampled-coordinate inference is used.

This proves a copy-invariant necessary rule for **all 36 pairs of the nine
identical-profile cogs**: if insert 50 selects query 16 / row 0, at most one cog
can select query 18 / row 3. The certificate applies only to those current domains.
It has not yet been added to a search model. Next add the single verified
conditional-capacity inequality to the intact necessary master, audit its entire
mapping and parent, then consider a distinct bounded call. All **169** calls in
this checkpoint are closed; none may be restarted, extended or reseeded.

A full positive still requires independent checks of all 66 original outlines,
90 cutouts and 10,026 hole vertices, all pair/stock/material guards and the native
validator, followed by production integration and the full 13-job/two-kerf matrix.

## Repository and release state

Both prior checkpoints were pushed normally to main **6a27fec0**. All six jobs
in [CI 40261923411](https://github.com/skulitom/Nestbolt/actions/runs/40261923411)
have now passed. Current upstream heads/releases show no stop-rule trigger.
Product source, READMEs and releases are unchanged; no new release is qualified.
The original H2 gate and all 22 reserved vectors remain untouched.

Evidence: [raw certificate]({NAME}/raw-triple-certificate.json),
[exact geometry audit]({NAME}/certificate-audit-checks.json),
[pair readback]({NAME}/pairs-response-audit-checks.json),
[triple readback]({NAME}/triples-response-audit-checks.json),
[checks]({NAME}/checks.json), [next step]({NAME}/next-step.json), and
[raw manifest]({NAME}/raw-manifest.json). **{archive['archive_members']:,}**
canonical files and **{archive['verified_aliases']:,}** exact aliases are
size/SHA-256/CRC verified across **{archive['archive_parts']}** archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 domain selection and three-part certificate, 2026-10-26:** [the evidence]({link})
retains a closed full-source UNKNOWN and refines 27,798 additional raw collision
exclusions. A verified necessary master selects domains, but its exact-coordinate
subproblem is INFEASIBLE for that tuple only. All 46 pair subproblems have checked
source witnesses; the complete bounded 120-triple census gives 87 checked
witnesses, 32 UNKNOWN and one conditional negative. Independently of solver
status, exact-rational original geometry proves that insert 50 in query16/row0
permits at most one of the nine cogs in query18/row3, covering all 36 copy pairs.
Next add and audit this single conditional-capacity rule in the necessary master;
all 169 calls here remain closed. The initial readback helper failure and repaired
audit are preserved, as are all soft-limit overruns; all outer budgets pass.
No full target/native/production qualification is claimed. All six checks on main
6a27fec0 pass, permitting a normal push. H2/H5 remain open at 60%; production,
READMEs, releases and the 22 reserved H2 vectors are unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
