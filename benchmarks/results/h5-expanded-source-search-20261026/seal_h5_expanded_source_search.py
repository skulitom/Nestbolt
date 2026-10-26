"""Seal fresh full12-source model, preserved budget timeout and exact-normal census."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-expanded-source-search-20261026';OUT=ROOT/'benchmarks/results'/NAME;RUN=ROOT/'output'/NAME;MODEL=ROOT/'output/h5-expanded-source-model-20261026';CAP=ROOT/'output/h5-expanded-second-sheet-capacity-20261026';REVIEW=ROOT/'output/h5-expanded-search-source-review-20261026';SYNC=ROOT/'output/h5-expanded-source-main-sync-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(REVIEW/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='d85f2b2a6a165bd140975b125b5d6ba99b71af9c';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items());ma=load(MODEL/'audit/checks.json');ta=load(RUN/'timeout-audit/checks.json');ca=load(CAP/'audit/checks.json');assert all(c['passed'] for c in [ma,ta,ca]);assert ta['parent_terminal_status']=='SHARED_BUDGET_PROCESS_TIMEOUT' and ta['solver_terminal_status'] is None and ta['no_saved_response_or_candidate'];OUT.mkdir()
    copies=[(CAP/'certificate.json','fresh-capacity-certificate.json'),(CAP/'audit/checks.json','fresh-capacity-audit.json'),(MODEL/'result.json','model-result.json'),(MODEL/'audit/checks.json','model-audit.json'),(MODEL/'audit/projection-proof.json','model-proof.json'),(MODEL/'necessary-rules.json','necessary-rules.json'),(RUN/'shared-search/result.json','search-result.json'),(RUN/'shared-search/solve/model-audit.json','actual-model-audit.json'),(RUN/'search-audit/failure.txt','ordinary-completion-audit-failure.txt'),(RUN/'timeout-audit/checks.json','timeout-audit.json'),(RUN/'timeout-audit/factorization-census.json','factorization-census.json'),(REVIEW/'review.json','source-review.json'),(REVIEW/'main-ci.json','main-ci-d85f2b2a-snapshot.json'),(REVIEW/'prior-ci.json','prior-main-ci-d1645404-passed.json'),(SYNC/'receipt.json','main-push-receipt.json')]
    for p,n in copies:shutil.copyfile(p,OUT/n)
    action=('The full12-original/54-fixed source model is independently reconstructed and its single call is CLOSED after hard60second process timeout, not UNKNOWN/INFEASIBLE. Do not restart, extend or reseed it. Preparation completed and search began at16.54solver seconds; there is no saved response/candidate or native call. All66 originals remain mandatory. Next investigate exact shared linear projection variables for the201575 one-sided direction definitions, grouped by16082 exact ordered-physical-pair normals in timeout-audit/projection-groups.json. Define z=A*(xb-xa)+B*(yb-ya) with exact global coordinate extrema, then replace each flag-enforced plane by flag=>z>=C. Keep every old variable, source face OR, domain/mode/choice equation, two original-area inequalities, fresh second-sheet capacity2 and54 hints. No geometry/copy-order/witness lock or fixed57 exclusion may be introduced. This would add16082 variables/equalities but reduce direction-definition matrix terms by495561; no performance benefit has been established. Verify every replacement, complete parent restoration/elimination, safe integer bounds and real solver import/export independently before a separately declared bounded call. Any positive needs all66 original outlines/cutouts, source/pair/stock/material checks and native validation before production integration/full13-job two-kerf matrix. Currentmain d85f2b2a CI40258687459 is running with4jobs passed at02:31UTC; wait for terminal CI before another normal push. H2 remains open under the original gate; leave all22 reserved vectors untouched. No new release qualification.')
    write(OUT/'next-step.json',{'action':action,'source_model':'output/h5-expanded-source-model-20261026','source_model_sha256':ma['model_sha256'],'closed_call':'output/h5-expanded-source-search-20261026/shared-search','required_originals':66,'moving_originals':12,'fixed_originals':54,'full_target_witness':False,'H5_complete':False})
    members={};inputs={};bases=[CAP,MODEL,RUN,REVIEW,SYNC]
    for base in bases:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            data=load(p)
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in data.get(field,{}).items():
                    if n in inputs:assert inputs[n]==h
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    manifest=ROOT/'benchmarks/results/h5-expanded-cog-neighborhood-20261026/raw-manifest.json';members['source-inputs/'+manifest.relative_to(ROOT).as_posix()]=manifest
    names=['certify_h5_expanded_second_sheet_capacity.py','audit_h5_expanded_second_sheet_capacity.py','prepare_h5_expanded_source_model.py','audit_h5_expanded_source_model.py','run_h5_expanded_source_search.py','audit_h5_expanded_source_search.py','audit_h5_expanded_source_timeout.py','review_h5_expanded_source_search.py','push_h5_expanded_source_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py'];pending=[ROOT/'output'/n for n in names];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'all66_originals_mandatory':True,'fixed_originals':54,'moving_originals':12,'every_model_variable_and_constraint_independently_verified':True,'fresh_second_sheet_capacity_independently_verified':True,'actual_solver_import_export_verified':True,'single_search_call_closed':True,'hard_timeout_preserved_without_solver_status':True,'ordinary_completion_audit_failure_preserved':True,'outer_timeout_cleanup_overshoot_seconds':ta['outer_timeout_cleanup_overshoot_seconds'],'shared_budget_honored':False,'exact_normal_factorization_census_only':True,'new_solver_calls':1,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: expanded full-source search — 2026-10-26

**The full 12-mover model passes independent reconstruction, but its one bounded
call is terminated by the outer budget without a saved solution or solver
status.** All 66 originals remain mandatory. H2/H5 stay open at **60%**.

## Fresh necessary capacity and model

The original cog/cog collision boundary has 228 segments. Exact binary-rational
segment-distance checks and a separate endpoint/cross-product/ray-parity audit
confirm a strictly interior **258.082 mm** collision disk. All 32 fresh
second-sheet cog domains lie within integer anchor bounds
`[1094689,146489,1353511,179438]` on the micrometre grid. Two adjacent,
disjoint x bins cover those bounds. Each bin's squared diagonal is below the
necessary integer squared separation **66,606,318,725**. Hence at most two of
the nine moving cogs can select sheet 2. This is a new certificate for the
54-fixed construction; no old fixed57 regional certificate is transferred.

The new model includes all **12 mandatory movers / 54 unchanged fixed parts**,
**24 anchor coordinates**, **52 query modes**, **12,688 domain-choice flags**,
and all **538 same-sheet modes over 66 physical pairs**. It contains
**214,901 variables**, **281,731 constraints**, **201,575 shared direction flags**
and **54 advisory hints** from the repaired nine-cog partial. No hint becomes
a coordinate lock. No copy-order symmetry or old fixed57 conditional exclusion
is added.

The full guarded source relations account for **13,794 convex-face uses**:
5,630 are whole-box tautologies, two force their mode inactive, five have a
single possible outside edge and 8,157 retain complete disjunctions. Direction
normalization is exact integer gcd/ceiling division. Flags are shared only for
the same ordered physical pair and identical normalized inequality, imply
their own plane and occur positively in source-face disjunctions.

Two necessary filled-area inequalities are recomputed from exact original
binary-rational polygons and stock rectangles. Lower charges for the 54 fixed
parts are **3,681,713,590 / 249,662,718** units of 0.001 mm². The integer stock
upper limits are **4,441,669,000 / 465,322,303**. The second upper limit is one
unit tighter than an earlier outward-ceiling bound: integer lower-area sums
cannot exceed the floor of the exact available area. This changes no stock or
material target. Part-in-hole/common-line remain off for this job.

An independent audit verifies **119 committed source inputs**, reconstructs
every variable and constraint, evaluates all face simplifications using a
separate signed-interval calculation, verifies the existential shared-flag
projection, all hints and original IDs, and checks actual solver import/export.
The model digest is `{ma['model_sha256']}`. Offline preparation and audit do not
qualify the production budget.

## Preserved hard timeout

Declare one call with eight workers, seed zero, a **45-second solver soft
limit**, a **60-second shared outer budget**, and ten seconds reserved for
shutdown. The actual imported model and parameter bytes match their audits.
Loading/verification takes **2.318658 seconds**. The solver log reaches search
at **16.54 solver seconds**, after preparation, then records no final response.

The parent terminates the process at the shared deadline and returns after
**60.029781 seconds**, including **0.029781 seconds** beyond the outer budget.
This budget miss is preserved. There is no saved solver response, terminal
solver status, candidate or native validation; the result is **process timeout**,
not `UNKNOWN` or `INFEASIBLE`. The log does not establish which worker or
shutdown operation caused the delay. The process is absent at the subsequent
independent audit. The call is closed and must not be retried, extended or reseeded.

The first readback auditor expected a normal solver completion and failed on
the missing result file. Its original script, plan and traceback remain.
A separate timeout-specific audit verifies the preserved result, absence of a
candidate/response/process, actual parameters/model and timing. It does not
convert the failed run into a successful result.

## Evidence for a distinct next formulation

A deterministic census finds that the **201,575** direction definitions use
only **16,082 distinct exact normals per ordered physical pair**, with up to
75 thresholds sharing one normal. Their definitions contain **777,018**
nonzero coordinate terms. Introducing an integer projection
`z = A*(xb-xa) + B*(yb-ya)` once per group, then expressing each flag as
`flag => z >= C`, would reduce those definitions plus projection equalities
to **281,457** terms: **495,561 fewer**. It would add 16,082 variables and
equalities, producing 230,983 variables and 297,813 constraints.

This is a census and proposed exact reformulation, with **no demonstrated
performance benefit or additional solver call**. All source-face clauses,
domains, area/capacity rules, mandatory parts and hints must remain unchanged.
Every replacement, finite projection bound, complete parent recovery and actual
solver import/export must be independently checked before a distinct call.
Any eventual candidate still needs all 66 original outlines/cutouts, original
pair/stock/material checks and native validation, then production integration
and the complete 13-job/two-kerf benchmark matrix.

## Main, release and remaining gates

All six jobs of [main d1645404 CI 40256286467](https://github.com/skulitom/Nestbolt/actions/runs/40256286467)
passed before the normal push of **d85f2b2a**. The remote commit and push receipt
are verified. At 02:31 UTC, [its CI 40258687459](https://github.com/skulitom/Nestbolt/actions/runs/40258687459)
is running with four jobs passed. Preserve that run before the next main push.
Upstream heads/releases, production and READMEs are unchanged. These diagnostic
changes do not qualify another release; preview v0.2.0-alpha.1 and stable
v0.1.0 remain appropriate. H2 keeps its original gate and all 22 reserved vectors
remain untouched.

Evidence: [model audit]({NAME}/model-audit.json),
[fresh capacity audit]({NAME}/fresh-capacity-audit.json),
[timeout audit]({NAME}/timeout-audit.json),
[factorization census]({NAME}/factorization-census.json),
[checks]({NAME}/checks.json) and [raw manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}**
exact-content aliases are size/SHA-256/CRC verified in **{archive['archive_parts']}**
independently readable archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 expanded full-source search, 2026-10-26:** [the evidence]({link})
independently verifies the complete 12-mover/54-fixed model: all 66 originals,
214,901 variables, 281,731 constraints, 538 full source pair modes, two exact
area rules and a fresh second-sheet cog capacity of two. Its one call reaches
the hard shared deadline without a saved solver response or candidate, returning
after 60.029781 seconds. The 0.029781-second outer overrun and the ordinary
readback auditor's missing-result failure are preserved; a separate timeout
audit verifies closure without assigning UNKNOWN/INFEASIBLE or claiming native
acceptance. No retry is permitted. A census identifies 16,082 exact pair/normal
projection groups that could remove 495,561 repeated matrix terms; this needs
a separate whole-model audit before another distinct bounded call. The expanded
geometry checkpoint d85f2b2a is on main after all six prior checks passed; its
own CI has four jobs passed at 02:31 UTC. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors remain unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
