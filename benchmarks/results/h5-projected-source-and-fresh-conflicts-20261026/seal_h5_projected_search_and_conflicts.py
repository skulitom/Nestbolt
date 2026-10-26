"""Seal exact projection searches and newly verified expanded-domain conflict tables."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-projected-source-and-fresh-conflicts-20261026';OUT=ROOT/'benchmarks/results'/NAME;PROJ=ROOT/'output/h5-projected-expanded-model-20261026';PRUN=ROOT/'output/h5-projected-expanded-search-20261026';TRUTH=ROOT/'output/h5-projected-truth-model-20261026';TRUN=ROOT/'output/h5-projected-truth-search-20261026';CONFLICTS=ROOT/'output/h5-expanded-domain-conflicts-20261026';REVIEW=ROOT/'output/h5-projected-search-source-review-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(REVIEW/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='b3c2f2e025d782231409124f2e3aea0ee542942b';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
    for p in [PROJ/'audit/checks.json',TRUTH/'audit/checks.json',PRUN/'search-audit/checks.json',TRUN/'search-audit/checks.json',CONFLICTS/'audit/checks.json',CONFLICTS/'groups/audit/checks.json']:assert load(p)['passed']
    assert all(load(p/'search-audit/checks.json')['terminal_status']=='UNKNOWN' and load(p/'search-audit/checks.json')['shared_budget_honored'] for p in [PRUN,TRUN]);OUT.mkdir()
    copies=[(PROJ/'result.json','projected-model-result.json'),(PROJ/'audit/checks.json','projected-model-audit.json'),(PROJ/'audit/equivalence-proof.json','projected-model-proof.json'),(PRUN/'shared-search/result.json','projected-search-result.json'),(PRUN/'search-audit/checks.json','projected-search-audit.json'),(TRUTH/'result.json','truth-model-result.json'),(TRUTH/'audit/checks.json','truth-model-audit.json'),(TRUTH/'audit/equivalence-proof.json','truth-model-proof.json'),(TRUN/'shared-search/result.json','truth-search-result.json'),(TRUN/'search-audit/checks.json','truth-search-audit.json'),(CONFLICTS/'result.json','fresh-conflict-result.json'),(CONFLICTS/'audit/checks.json','fresh-conflict-audit.json'),(CONFLICTS/'groups/result.json','conflict-groups-result.json'),(CONFLICTS/'groups/audit/checks.json','conflict-groups-audit.json'),(REVIEW/'review.json','source-review.json'),(REVIEW/'main-ci.json','main-ci-d85f2b2a-snapshot.json')]
    for p,n in copies:shutil.copyfile(p,OUT/n)
    comparison=[]
    for label,base,model in [('one-sided-projection',PRUN,PROJ),('exact-unary-truth',TRUN,TRUTH)]:
        r=load(base/'shared-search/solve/result.json');a=load(base/'search-audit/checks.json');log=(base/'shared-search/solve/solver.log').read_text();start=re.findall(r'Starting search at ([0-9.]+)s with (\d+) workers',log);assert len(start)==1 and start[0][1]=='8'
        row={'formulation':label,'model_sha256':digest(model/'model.pb'),'status':r['status'],'solver_seconds':r['seconds'],'shared_seconds':a['actual_shared_seconds'],'solver_soft_limit_overshoot_seconds':a['solver_soft_limit_overshoot_seconds'],'search_started_at_solver_seconds':float(start[0][0]),'full_candidate':False,'single_observation_not_a_performance_benchmark':True}
        for field in ['booleans','conflicts','branches','propagations','integer_propagations']:row[field]=int(re.search(r'^'+field+r': (\d+)$',r['response_stats'],re.M).group(1))
        comparison.append(row)
    write(OUT/'search-observations.json',comparison)
    next_action=('All source/projection/truth calls are CLOSED; no restart/reseed/extension. The fresh54-fixed box-conflict census is complete and independently verified over9,437,545 pairs, with3,948,295 proven raw-original collisions. Its independently verified groups represent25,189,075 physical uses over all538 modes, using4010 auxiliaries and4687 nonzero group constraints. Next append these fresh groups to a complete audited projected source model (prefer the one-sided projected parent as the smaller encoded model; this is a working choice, not a demonstrated quality advantage). Keep every parent constraint,54 advisory hints, all66 mandatory originals,24 coordinates, full538 original source modes, two area rules and fresh capacity2. For each A group, define its flag as the sum of already mutually exclusive selected A domains; add at-most-one with all marked B domains, or OR(not group,not B mode) when all B rows conflict. Expected added variables4010, constraints8697, mutual-exclusion literals1,099,261. Independently verify every source bit/group/domain-to-variable mapping and full retained parent, actual solver import/export, then one separately declared bounded call if appropriate. False table bits are not evidence of feasible anchors. Do not transfer old fixed57 table or capacity clauses. Full66 original geometry/native validation and production integration/full13-job two-kerf matrix still required. Main d85f2b2a CI40258687459 was live with five jobs passed at02:49UTC; wait for terminal CI before pushing the queued checkpoints. H2 original gate and22 reserved vectors stay unchanged.')
    write(OUT/'next-step.json',{'action':next_action,'preferred_source_model':PROJ.relative_to(ROOT).as_posix(),'fresh_conflict_source':CONFLICTS.relative_to(ROOT).as_posix(),'required_originals':66,'moving_originals':12,'fixed_originals':54,'H5_complete':False})
    bases=[PROJ,PRUN,TRUTH,TRUN,CONFLICTS,REVIEW];members={};inputs={}
    for base in bases:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in load(p).get(field,{}).items():
                    if n in inputs:assert inputs[n]==h
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-expanded-cog-neighborhood-20261026','h5-expanded-source-search-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    # Matrices bind every query and original mutual obstacle separately.
    source=ROOT/'output/h5-expanded-cog-joint-prepared-20261026';cp=load(CONFLICTS/'plan.json')
    for directory,field in [('queries','query_hashes'),('mutual','mutual_hashes')]:
        for i,h in cp[field].items():p=source/directory/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for name in ['profiles.json','plan.json','audit/checks.json']:
        p=source/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_projected_expanded_model.py','audit_h5_projected_expanded_model.py','make_h5_projected_expanded_runner.py','run_h5_projected_expanded_search.py','make_h5_projected_expanded_readback.py','audit_h5_projected_expanded_search.py','prepare_h5_projected_truth_model.py','audit_h5_projected_truth_model.py','make_h5_projected_truth_runner.py','run_h5_projected_truth_search.py','audit_h5_projected_truth_search.py','make_h5_expanded_domain_conflict_helpers.py','build_h5_expanded_domain_conflicts.py','audit_h5_expanded_domain_conflicts.py','make_h5_expanded_conflict_group_helpers.py','prepare_h5_expanded_conflict_groups.py','audit_h5_expanded_conflict_groups.py','review_h5_projected_search_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py'];pending=[ROOT/'output'/n for n in names];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    for name in ['run_h5_expanded_source_search.py','audit_h5_expanded_source_search.py','build_h5_original_domain_conflicts.py','audit_h5_original_domain_conflicts.py','h5-convex-domain-conflicts-20261025/groups/prepare.py','h5-convex-domain-conflicts-20261025/groups/audit/audit.py']:
        p=ROOT/'output'/name;members['source-helpers/'+name]=p
    archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'required_originals':66,'moving_originals':12,'fixed_originals':54,'both_full_model_equivalence_audits_pass':True,'both_actual_solver_import_export_checks_pass':True,'new_solver_calls':2,'both_calls_closed_unknown_no_candidate':True,'both_shared_budgets_honored':True,'soft_solver_limit_overshoots_preserved':True,'fresh_conflict_pairs_independently_checked':9437545,'fresh_conflict_exclusions':3948295,'grouping_replayed_bitwise':True,'fresh_conflict_groups_not_yet_in_search_model':True,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: projected source models and fresh conflicts — 2026-10-26

**Two independently audited equivalent formulations finish their bounded calls
without a complete layout. Fresh collision tables for the expanded domains
are now independently verified.** H2/H5 remain open at **60%**.

## Exact signed projections

The complete 12-mover/54-fixed model keeps every original source constraint,
all 66 required originals, 24 anchor coordinates, 538 same-sheet pair modes,
two necessary area inequalities, the fresh second-sheet cog capacity of two
and 54 advisory hints. No coordinate lock or copy-order exclusion is introduced.

For each ordered physical pair, opposite primitive normals share one signed
integer projection `z = A*(xb-xa) + B*(yb-ya)`. The **201,575** old direction
definitions become unary lower/upper thresholds over **8,185** exact projections.
This reduces their coordinate terms, including new defining equalities, from
**777,018 to 242,236**: **534,782 fewer terms**. The complete model has
**223,086 variables / 289,916 constraints**. The projection bounds are verified
independently at all **130,960** coordinate-box corners. Eliminating the new
variables restores the complete parent proto exactly; actual import/export passes.

The single new call returns **UNKNOWN** after **45.869232 solver seconds** and
**48.289739 shared seconds**. Search starts at 9.85 solver seconds; the earlier
unfactored run started at 16.54 seconds and was killed at its outer deadline.
These are individual diagnostic observations, not a performance benchmark.
No candidate is saved. The **0.869232-second solver soft-limit overshoot** is
preserved; the shared 60-second budget is honored.

## Exact unary truth channels

A second formulation retains that complete projected model and appends
**201,575** complementary unary constraints. Each auxiliary flag now equals
its threshold's truth. An independent occurrence audit verifies that every old
flag appeared only in its own positive enforcement and positive source-face
disjunctions: **304,048** such disjunctive uses. Setting flags to actual threshold
truth can only turn false flags true, so no old source disjunction becomes false.
Dropping the complements restores the entire parent; both directions preserve
physical placement feasibility. Auxiliary assignments themselves need not match.

This model has **223,086 variables / 491,491 constraints** and the same 54 hints.
Its separate call returns **UNKNOWN** after **45.687183 solver seconds** and
**48.865027 shared seconds**, with a **0.687183-second solver soft-limit overshoot**.
Search starts at 12.82 solver seconds. Its solver response reports 246,297
Booleans, versus 443,411 in the one-sided projected call. These observations
do not establish a quality or speed advantage. No full layout is found.

Both readback audits verify the actual model, complete parameter bytes, returned
response/status and timing. Each call is closed: no restart, extension or reseed.
No native validation or production qualification occurs. Offline preparation
remains outside these diagnostic search budgets and cannot count toward H5.

## Fresh expanded-domain conflict census

Rebuild every conflict bit from the **54-fixed** domains; no old fixed57 table
is reused. The complete inventory contains **164 unique query pairs**,
**9,437,545 domain pairs**, and **538 physical query-mode uses over 66 pairs**.
For each domain pair, compute the entire signed anchor-difference rectangle,
pad it outward by one micrometre and require strict containment inside an
explicitly inset raw original collision obstacle. This proves incompatibility
for all anchors in the two domains, rather than sampling a few points.

Construction checks the complete census in 9.265043 seconds and certifies
**3,948,295 conflicts**, with no pending cases. The independent audit rebuilds
all 82 raw obstacles from **9,824 unmerged triangle-pair hulls**, checks every
packed bit, domain order and trailing padding, and proves each excluded rectangle
lies inside the independently reconstructed original obstacle. Its maximum
raw-boundary discrepancy is **1.654789e-11 mm**, and every inset core retains
at least **0.0000999999865 mm** of independently checked interior margin.
All **102** source query/mutual files match committed evidence. This audit takes
13.531452 seconds.

Identical B-conflict rows compress losslessly into **1,152 unique groups**,
including zero rows. An independent integer-bit replay verifies every row
partition and Boolean implication. Across physical pairs, the nonzero groups
represent **25,189,075** conflict uses with **4,010** group auxiliaries,
**4,687** nonzero group constraints and **1,099,261** mutual-exclusion literals.
A group flag equals a sum of already mutually exclusive A-domain selectors;
its exclusion with marked B selectors expresses exactly the recorded conflicts.
An unmarked bit is not proof that the two domains admit feasible anchors.

These groups are prepared and audited but **not yet added to a search model**.
Next append them to an intact projected source model, verify all group/domain
mappings and constraints, and audit actual import before a distinct bounded
call. Every original geometry guard, mandatory part and source clause remains.
Any positive still requires all 66 original outlines/cutouts, pair/stock/material
checks and native validation, followed by production integration and the full
13-job/two-kerf matrix.

## Repository and release state

The prior checkpoint b3c2f2e0 is queued locally above main d85f2b2a. At 02:49 UTC,
[main CI 40258687459](https://github.com/skulitom/Nestbolt/actions/runs/40258687459)
has five jobs passed and Windows checks still running. Preserve that run before
a normal push. Upstream heads/releases, product source and READMEs are unchanged.
No new release is qualified. H2 retains the original gate and all 22 reserved
vectors remain untouched.

Evidence: [projection audit]({NAME}/projected-model-audit.json),
[truth-channel audit]({NAME}/truth-model-audit.json),
[search observations]({NAME}/search-observations.json),
[fresh conflict audit]({NAME}/fresh-conflict-audit.json),
[group audit]({NAME}/conflict-groups-audit.json),
[checks]({NAME}/checks.json) and [raw manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}**
exact-content aliases are size/SHA-256/CRC verified in **{archive['archive_parts']}**
independently readable archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 projected models and fresh conflicts, 2026-10-26:** [the evidence]({link})
verifies exact signed projections for all 201,575 source direction definitions,
removing 534,782 repeated terms, and a separate exact unary truth-channel encoding.
Both full 12-mover/54-fixed models preserve all 66 required originals and pass
independent equivalence/import audits. Their separate calls return UNKNOWN in
48.289739 and 48.865027 shared seconds; no candidate is saved and both calls are
closed. Solver soft-limit overshoots remain recorded. A fresh complete census
checks 9,437,545 domain pairs and independently proves 3,948,295 raw-original
collision exclusions. Exact row grouping preserves 25,189,075 physical uses,
ready for independently audited integration into a complete source model.
No old fixed57 table is transferred and no unmarked pair is called feasible.
At 02:49 UTC main d85f2b2a has five CI jobs passed with Windows checks running;
queued evidence awaits terminal CI before a normal push. H2/H5 remain open at
60%; product source, READMEs, releases and the 22 reserved H2 vectors are unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
