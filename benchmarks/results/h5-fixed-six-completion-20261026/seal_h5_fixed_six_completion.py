"""Preserve complete conditional geometry proofs and verified main sync."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-fixed-six-completion-20261026';BASE=ROOT/'output'/NAME;REL=ROOT/'output/h5-single-cog-release-20261026';CAP=ROOT/'output/h5-top-cog-bracket-capacity-20261026';SYNC=ROOT/'output/h5-bounded-main-sync-20261026';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    proof=load(BASE/'result.json');audit=load(BASE/'audit-provenance-repaired/checks.json');release=load(REL/'audit-recovered/checks.json');comparison=load(REL/'audit-recovered/release-comparison.json');capacity=load(CAP/'audit/checks.json');sync=load(SYNC/'receipt.json')
    assert audit['passed'] and audit['all2418_bracket_domains_continuously_excluded'] and release['passed'] and release['complete_release_cases']==6 and capacity['passed'] and capacity['at_most_one_original_bracket']
    assert proof['pending_domains']==0 and not proof['cap_reached'] and all(p['all_original_parts_still_required']==66 for p in comparison)
    prior=load(ROOT/'benchmarks/results/h5-bounded-source-search-20261026/source-review.json');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head==mainhead==sync['source_head']=='822a5f67428e6dfdecab7bcea45e7c89cc31b159'
    ci=json.loads(subprocess.check_output(['gh','run','view','40248595273','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==head;write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('The exact six-cog witness cannot be completed by even one bracket in any of the 2,418 original inward bracket domains; the continuous rational proof includes all boundary points and is independently replayed. This conclusion is conditional on those six poses, source orientations/domains and fixed 57. '
        'Six distinct leave-one-cog-position-free censuses cover all 14,508 bracket domains. Releasing original cog54 or62 still leaves none. Releasing cog58 permits individual bracket regions, but all196 exact ordered residual-pair differences are empty under the original full guarded bracket clauses, proving capacity at most one. '
        'Next investigate releases of original cogs57,64 or65 (moving-part indices4,7,8). Prepare complete original inward regions for the missing insert and released cog against the other five fixed cogs, alongside the already audited bracket regions; retain every boundary/line/point and source angle. '
        'Use the correct signed displacement when the released cog occurs before or after a fixed cog in the original pair ordering. Derive integer bounds inward with exact rational arithmetic and preserve any continuous residual with no integer point as a separate result. '
        'For each candidate, construct a focused four-mover model containing both original brackets28/29, insert50 and the released original cog; the other62 originals stay fixed. Every one of66 originals remains mandatory, with all pair/source-domain/native/material rules. Do not fix a placed cog twice or omit the released cog. '
        'Retain both bracket copy-order symmetry only if their domains remain identical; do not impose the prior six-cog copy-index order on individually fixed poses. Include every original mutual source face among the four movers. Independently audit before any newly budgeted search, with separate60-second total preparation/import/audit/search accounting if claiming production qualification. Offline region preparation is not such a pass. '
        'These regions alone do not demonstrate room for both brackets, the insert and the released cog simultaneously. No completed solver or proof call should be restarted. Keep H5 open until a full original native-valid target and production integration/full13-job two-kerf matrix exist. '
        'Three previous checkpoints were normally pushed and exact remote main822a5f67 verified after all six prior CI jobs passed. Track its new CI40248595273; preserve remote changes before subsequent normal pushes. H2 keeps its original gate and22 reserved vectors untouched; no new release is qualified.')
    OUT.mkdir();copies={BASE/'plan.json':'fixed-six-plan.json',BASE/'result.json':'fixed-six-result.json',BASE/'summary.json':'fixed-six-query-summary.json',BASE/'audit-provenance-repaired/checks.json':'fixed-six-audit.json',BASE/'audit-provenance-repaired/conditional-no-bracket-completion.json':'conditional-no-bracket-completion.json',BASE/'audit/failure.txt':'initial-provenance-failure.txt',BASE/'audit/provenance-repair.json':'provenance-repair.json',REL/'result.json':'release-census-result.json',REL/'audit-recovered/checks.json':'release-census-audit.json',REL/'audit-recovered/release-comparison.json':'release-comparison.json',REL/'audit/failure-recovery.json':'release-aggregate-recovery.json',REL/'audit-recovered/witness-source-provenance.json':'additional-witness-provenance.json',CAP/'result.json':'bracket-capacity-result.json',CAP/'audit/checks.json':'bracket-capacity-audit.json',CAP/'audit/at-most-one-certificate.json':'bracket-capacity-certificate.json',SYNC/'receipt.json':'main-push-receipt.json',BASE/'main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'candidate_released_original_cogs':[57,64,65],'candidate_released_parts':[4,7,8],'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','new_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,'previous_checkpoints_pushed':3,'previous_main_ci_id':40246226212,'previous_main_ci_successful_jobs':6,'current_main_ci_id':40248595273,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for base in [BASE,REL,CAP,SYNC]:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h,(n,inputs[n],h)
                inputs[n]=h
    inputs.update(load(REL/'audit-recovered/witness-source-provenance.json')['inputs'])
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for previous in ['h5-bounded-source-search-20261026','h5-guarded-cell-search-20261025']:
        p=ROOT/'benchmarks/results'/previous/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prove_h5_fixed_six_completion.py','audit_h5_fixed_six_completion.py','repair_h5_fixed_six_provenance.py','audit_h5_fixed_six_completion_repaired.py','prepare_h5_single_cog_release_helpers.py','prove_h5_single_cog_release.py','audit_h5_single_cog_release.py','run_h5_single_cog_release_census.py','audit_h5_single_cog_release_census.py','recover_h5_release_census_audit.py','audit_h5_single_cog_release_census_recovered.py','prove_h5_top_cog_bracket_capacity.py','audit_h5_top_cog_bracket_capacity.py','prepare_h5_bounded_main_sync.py','push_h5_bounded_checkpoints.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'all_fixed_six_bracket_domains_continuously_excluded':True,'all_six_distinct_release_censuses_independently_replayed':True,'all196_cog58_release_bracket_pairs_excluded':True,'lower_dimensional_boundaries_preserved':True,'conditional_scope_only':True,'failed_provenance_and_aggregation_records_preserved':True,'completed_case3_audit_reused_without_rerun':True,'three_prior_checkpoints_normally_pushed_and_remote_verified':True,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    table='\n'.join(f"| {r['released_original_item']} | {r['released_source_sheet']+1} | {r['residual_domains']} | {r['residual_fragments']} | {r['lower_dimensional_residuals']} |" for r in comparison)
    report=f'''# H5: exact completion obstruction and single-cog release census — 2026-10-26

**The verified six-cog arrangement cannot accommodate either missing bracket
within the original inward placement domains.** Exact continuous-domain proofs
replace the earlier finite-pose observation. Releasing one cog position opens
bracket regions in four cases; a complete two-bracket capacity proof rules out
one more of those cases. Original cogs **57, 64 and 65** remain the useful
single-position releases to investigate. No complete layout is claimed.
H2/H5 remain open at **60%** completed milestone weight.

## Full continuous-domain check with all six cogs fixed

Keep the independently verified six original cog anchors and the other 57
original placements unchanged. Both original brackets 28/29 and insert 50
remain required. The identical brackets have **16 original mode/sheet queries
and 2,418 inward domains**; the insert has **2 queries and 338 domains**.

For each cog on the same sheet, translate every full guarded source collision
clause into a condition on the missing part's real anchor. With moving anchor
`(x,y)` and fixed cog `(cx,cy)`, the original outside inequality becomes:

`a*x + b*y <= a*cx + b*cy - outside_bound`.

Exact integer bounds first identify complete domain boxes inside a failed
clause and clauses true throughout a box. Otherwise clip the entire real inward
domain using rational arithmetic. Apply each outside-clause union by retaining
all closed halfplane pieces and carrying closed complements between splits.
This retains boundary lines and isolated points as well as areas. No grid
sample, floating polygon simplification, inset or new safety padding is added.

All **2,756 domains** finish in **{proof['seconds']:.6f}s**, with no pending case
or cap: **2,304** complete box exclusions, **451** further continuous exclusions,
and **one insert domain** remaining as **89** convex fragments. The insert
residual is original query 16, domain row/index 13. All **2,418 bracket domains
are empty**, so these exact 63 placed originals cannot be completed to all 66.

Independent audit takes **{audit['seconds']:.6f}s**. It checks committed source
provenance, rechecks all six witness domains and **427** original cog-pair
clauses, enumerates **5,816,904 exact integer corner values**, and replays all
**1,136 changed-clause events** with a separate candidate-vertex/convex-hull
clipper. Every initial domain, residual, line/point boundary and complete query
inventory agrees. Every retained insert fragment satisfies every source clause.

The first audit stopped at an archive lookup: two historical witness audit
summaries live in their original guarded-cell archive. A separate repaired
readback resolves exactly those hashes there; the failed source, plan and
traceback are retained. Three additional witness query/mutual files read during
the witness recheck are separately matched to committed hashes and archived.
No geometry computation or solver is repeated by this provenance repair.

This proves only a **conditional obstruction** with the exact six poses,
recorded source orientations/inward domains and fixed 57. It does not prove
unrestricted packing impossible and must not become a domain exclusion in a
model where these cogs can move.

## Six distinct single-position releases

Release each cog position in turn while keeping the other five and the 57
original source placements fixed. The released cog remains a required part;
this diagnostic only measures bracket regions before placing that cog and the
insert. It does not remove a part from the intended 66-original layout.

Each case covers all **2,418 bracket domains**. All six complete in a shared
**13.630690s**, below the declared 180-second preparation budget and each
60-second case cap. No solver is used. Independent exact replay verifies all
**14,508 domain cases**, including their original source clauses and boundaries.

| Released original cog | Source sheet | Residual domains | Convex fragments | Line/point fragments |
|---|---:|---:|---:|---:|
{table}

Cog 57 opens query 2 and 10 regions on the first sheet; cog 58 opens only query
8 on that sheet. Cog 64 opens query 3 and 15 regions on the second sheet.
Cog 65 opens queries 3, 7, 9, 11 and 15 there. These are complete real regions,
not distinct integer placements or a proof that two brackets fit together.

The initial aggregate reader stopped after successfully auditing the first
case because a counter omitted its zero-valued residual key. The verified
per-case summary explicitly records zero. A separate aggregate recovery reads
that value, reuses the completed first audit without repeating it, and audits
only the five unfinished cases. All original process logs and the recovery
record are preserved; no geometric proof or search is restarted.

## Releasing cog 58 cannot fit both brackets

The cog-58 release leaves **14 query-8 convex regions**, all with the same
original bracket orientation. Enumerate every **196 ordered pair**, including
two brackets choosing the same region. For each pair form the exact rational
convex difference hull `B-A` from all vertex differences, then apply every
original full guarded bracket/bracket separation clause to that whole hull.

All **196** allowable difference regions are empty. Preparation takes
**{load(CAP/'result.json')['seconds']:.6f}s**. Independent gift-wrapped hull
reconstruction and the separate clipping oracle verify all **392** changed
clause events in **{capacity['seconds']:.6f}s**, preserving closed boundaries.
Thus **at most one original bracket** fits with the other five cog poses fixed,
even before replacing cog 58 or the insert. Moving only cog 58 cannot complete
the required two brackets and all 66 originals. This remains conditional on
the recorded source domains and fixed poses.

## Next focused construction and repository state

Investigate original cogs **57, 64 or 65** (moving-part indices 4, 7, 8).
Prepare complete source-domain regions for the insert and released cog against
the five retained cog poses, alongside the audited bracket regions. Preserve
every boundary and handle the signed source displacement correctly when the
released cog occurs before or after a fixed cog in the original pair order.

Each resulting focused model must contain **four mandatory movers**: brackets
28/29, insert 50 and the released original cog, with **62 fixed originals**.
Keep all 66 counts, original shapes, areas, source-domain and mutual pair rules,
native guards and material target. The old six-cog copy-index symmetry order
must not constrain individually fixed poses. A region alone is not a complete
layout. Audit all model changes before a newly declared bounded search.

Offline geometric preparation remains diagnostic; it is not a production-budget
pass. A complete original-geometry/native-valid target, production integration
and the full 13-job/two-kerf H5 matrix are still required. No solver, native
validation or quality run occurs in this checkpoint. H2 keeps its original gate
and all 22 reserved vectors untouched.

All six jobs in prior main CI 40246226212 passed. The three previous local
checkpoints were **normally pushed to main**, advancing 728b2db2 to
**822a5f67**, and the exact remote ref was verified. The saved receipt includes
the fetch, ancestry, clean tracked state, unchanged production/README checks,
normal push and remote readback. Main's new
[CI 40248595273]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful
jobs at this snapshot. This new checkpoint waits for that run before the next
normal push. No existing CI was cancelled.

Production source, all three accurate READMEs, preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain unchanged. No new release is qualified.

Evidence: [continuous proof audit]({NAME}/fixed-six-audit.json),
[release census]({NAME}/release-census-audit.json),
[complete comparison]({NAME}/release-comparison.json),
[two-bracket capacity certificate]({NAME}/bracket-capacity-certificate.json),
[verified main push]({NAME}/main-push-receipt.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']} canonical files / {archive['verified_aliases']}
exact-content aliases** retain every original source, proof domain, rational
fragment, changed-clause event, failure, recovery and audit with size, SHA-256
and CRC verification.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 exact completion obstruction and single-cog release census, 2026-10-26:** [the evidence]({link})
proves that the verified six fixed cog poses leave none of the 2,418 original
bracket domains continuously feasible; the insert retains one domain with 89
fragments. All 2,756 domains and 1,136 exact clipping events pass independent
replay, including boundaries and 5,816,904 integer corner checks. Six distinct
single-cog releases cover all 14,508 bracket domains in 13.630690s, with no
pending cases. Releasing cogs 54 or 62 leaves no bracket space. Releasing cog
58 opens individual regions, but all 196 exact ordered region-pair differences
are empty: at most one bracket fits, while two are required. Cogs 57, 64 and 65
remain the useful single-position releases to investigate in focused four-mover,
62-fixed-original models. All 66 parts and original/native/material requirements
remain mandatory. These are conditional source-pose/domain proofs, not general
packing impossibility or H5 qualification. No solver/native/quality call occurs.
The provenance lookup failure and zero-counter aggregation failure are preserved;
completed proof work is reused without reruns. Three prior checkpoints were
normally pushed to verified main 822a5f67 after all six prior CI jobs passed;
new CI 40248595273 is tracked. H2/H5 remain open at 60%; production, READMEs,
releases and all 22 reserved H2 vectors remain unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
