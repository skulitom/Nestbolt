"""Preserve compact source searches and the broader-neighborhood inspection."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-one-sided-conflict-propagation-20261026';OUT=ROOT/'benchmarks/results'/NAME;REVIEW=ROOT/'output/h5-one-sided-source-review-20261026';NEIGHBOR=ROOT/'output/h5-fixed-source-neighborhood-review-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(REVIEW/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='7c5b8b28f8f939e604310eb7d66dcc195eee7ab1'
    assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items()) and review['main_ci_successful_jobs']==6 and review['main_ci_conclusion']=='success'
    OUT.mkdir();bases=[REVIEW,NEIGHBOR];rows=[]
    for name in ['one-sided','conflict-propagated']:
        model=ROOT/f'output/h5-{name}-source-model-20261026';run=ROOT/f'output/h5-{name}-source-search-20261026';bases.extend([model,run]);mr=load(model/'result.json');ma=load(model/'audit/checks.json');sa=load(run/'search-audit/checks.json');assert ma['passed'] and sa['passed'] and ma['all_original_full_guarded_source_clauses_retained'] and sa['terminal_status']=='UNKNOWN' and sa['solver_calls']==1 and sa['shared_budget_honored'] and not sa['full_guarded_source_candidate']
        dest=OUT/name;dest.mkdir()
        for p,n in [(model/'result.json','model-result.json'),(model/'audit/checks.json','model-audit.json'),(run/'shared-search/result.json','shared-search-result.json'),(run/'shared-search/solve/result.json','solver-result.json'),(run/'shared-search/solve/model-audit.json','actual-model-audit.json'),(run/'search-audit/checks.json','closed-search-audit.json')]:shutil.copyfile(p,dest/n)
        rows.append({'representation':name,'variables':mr['variables'],'constraints':mr['constraints'],'model_sha256':mr['model_sha256'],'preparation_seconds':mr['seconds'],'independent_model_audit_seconds':ma['seconds'],'terminal_status':'UNKNOWN','solver_seconds':sa['actual_solver_seconds'],'total_seconds':sa['actual_shared_seconds'],'soft_limit_overshoot_seconds':sa['solver_soft_limit_overshoot_seconds']})
    assert load(bases[2]/'audit/checks.json')['one_sided_monotone_projection_verified'] and load(bases[4]/'audit/checks.json')['complete_certified_conflict_table_restored']
    for p,n in [(bases[2]/'audit/equivalence-proof.json','one-sided-equivalence-proof.json'),(bases[4]/'audit/restored-propagation-proof.json','restored-conflict-proof.json'),(REVIEW/'review.json','source-review.json'),(REVIEW/'main-ci.json','main-ci-68c82ae1.json'),(NEIGHBOR/'fixed-neighborhood.png','fixed-neighborhood.png'),(NEIGHBOR/'result.json','neighborhood-inspection.json'),(NEIGHBOR/'first-sheet-fixed-neighbors.json','fixed-neighbor-distances.json')]:shutil.copyfile(p,OUT/n)
    write(OUT/'comparison.json',rows)
    action=('Both compact full-source calls are CLOSED UNKNOWN; neither may be restarted, extended or reseeded. The exact one-sided projection and complete restored conflict table preserve all original requirements but do not resolve the fixed57 source construction. Next inspect a broader geometric neighborhood: release fixed original cogs53,56,61 adjacent to witness cogs54,62,58, together with the existing9 movers. That means12 mandatory movable originals and54 unchanged fixed originals, still all66 total. First reconstruct the three released originals at their retained source angles, inventory and transforms; prepare fresh full-original free-region queries and pair geometry with the same native guards and material target. Recompute every conditional domain, area and capacity certificate: fixed57 exclusions, regional caps and the old domain tables must not be transferred to the expanded free regions. Verify that the previous63-original partial remains representable, while the two missing brackets and insert stay mandatory. Independently audit the new geometry/provenance before deciding a new bounded construction. The inspected distances identify neighboring pieces, not a proof that moving them succeeds. No complete target or production qualification is claimed. Original/native66-part validation, production integration and the entire13-job/two-kerf matrix remain required. H2 retains its original gate and22 vectors untouched. All6 jobs on main68c82ae1 now pass; commit and normally push this checkpoint with queued7c5b8b28 after fresh ancestry/ref verification. No new release is qualified.')
    write(OUT/'next-step.json',{'action':action,'proposed_additionally_movable_original_items':[53,56,61],'proposed_total_moving_originals':12,'proposed_fixed_originals':54,'new_neighborhood_not_yet_constructed':True,'full_target_witness':False,'H5_complete':False})
    members={};inputs={}
    for base in bases:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-convex-domain-conflicts-20261025','h5-source-area-and-direction-sharing-20261026','h5-guarded-cell-search-20261025','h5-guarded-source-adjustment-20261025']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_one_sided_source_model.py','audit_h5_one_sided_source_model.py','prepare_h5_one_sided_search_helpers.py','run_h5_one_sided_source_search.py','audit_h5_one_sided_source_search.py','prepare_h5_conflict_propagated_source_model.py','audit_h5_conflict_propagated_source_model.py','prepare_h5_conflict_propagated_search_helpers.py','run_h5_conflict_propagated_source_search.py','audit_h5_conflict_propagated_source_search.py','run_h5_shared_direction_source_search.py','audit_h5_shared_direction_source_search.py','inspect_h5_fixed_source_neighborhood.py','review_h5_one_sided_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py']
    for n in ['h5-one-sided-search-helper-generation-20261026.json','h5-conflict-propagated-search-helper-generation-20261026.json']:members['extra/'+n]=ROOT/'output'/n
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
    write(OUT/'checks.json',{'passed':True,'one_sided_exact_projection_verified':True,'complete_proved_conflict_table_restored':True,'all8449813_conflict_bits_and_group_partitions_verified':True,'all_added_constraints_and_actual_solver_imports_verified':True,'two_distinct_calls_closed_unknown':True,'both_total_budgets_honored':True,'both_soft_limit_overshoots_preserved':True,'neighborhood_figure_visually_inspected':True,'neighborhood_inventory_is_partial_not_target':True,'production_and_readmes_unchanged':True,'all6_prior_main_ci_jobs_passed':True,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    table='\n'.join(f"| {r['representation']} | {r['variables']:,} | {r['constraints']:,} | {r['solver_seconds']:.6f} / {r['total_seconds']:.6f} | {r['soft_limit_overshoot_seconds']:.6f} |" for r in rows)
    report=f'''# H5: one-sided directions and restored conflicts — 2026-10-26

**Both distinct searches return UNKNOWN.** No full layout or impossibility
proof is obtained. H2/H5 remain open at **60%** completed milestone weight.
All 66 originals remain mandatory, with nine movable and 57 fixed in the
recorded source construction. Geometry, native guards and target are unchanged.

| Representation | Variables | Constraints | Solver / total seconds | Soft-limit overrun |
|---|---:|---:|---:|---:|
{table}

## Exact one-sided representation

Remove the 101,455 false-flag complement definitions from the previously
verified shared-direction model. Keep every positive flag-implies-plane
definition, face OR, original base, 14 area constraints and 72 hints.
The independent occurrence audit checks all 101,455 definitions and 158,717
positive OR occurrences; no negative or arithmetic use of a shared flag remains.

Every parent solution satisfies the child. Conversely, complete any child
solution by setting each shared flag to its exact plane truth. Already true
flags remain true; only false-to-true changes occur. Positive ORs remain satisfied,
and each newly enabled plane is true. The removed complements then hold too.
This proves the same feasible projection within the source construction.
The complete parent is restored exactly and actual solver import/export matches.

## Restored whole-domain conflicts

The earlier table-free projection removed a necessary domain-conflict table
to reduce overhead. Restore that independently proved table beside the compact
one-sided source model: **5,561,575 unique conflicts**, representing **24,091,856**
physical uses, with only **3,395** additional Booleans and **7,886** constraints.
These cover all families and all 164 query cases, not only cog/cog pairs.

The independent reader checks all **8,449,813** matrix bits and every row
partition, reconstructs the 394 physical mode uses from the original inventory,
verifies domain-variable ordering, and rebuilds all 4,491 nonzero groups.
A group flag equals the sum of mutually exclusive A-domain flags. Its exclusion
against the listed B-domain flags implements exactly the saved pair conflicts.
The entire compact parent is retained and actual solver import/export matches.
No fresh geometric exclusion is inferred.

Both calls use eight workers, seed zero, a 45-second soft solver limit and
60 shared seconds with a ten-second shutdown reserve. Their **0.486188s** and
**0.358075s** soft-limit overruns are retained; both total budgets pass.
They are closed: no restart, extension or reseed. Neither produces a candidate
for original-geometry or native validation. Preparation and audits remain offline
diagnostics, not production-budget qualification.

## Broader geometric neighborhood

![Partial source layout and adjacent fixed originals]({NAME}/fixed-neighborhood.png)

The visual inspection reconstructs the already audited **63-original partial**,
missing brackets 28/29 and insert 50. Filled cutouts stay reserved. It is not
a cutting layout. Among 200 first-sheet witness/fixed pairs, fixed cogs
**53, 56 and 61** border the movable cog cluster at approximately **0.213–0.238 mm**.
Frame 17 and insert 31 also border it. Distances identify neighbors; they do not
prove that moving any neighbor will supply a complete layout.

Next prepare fresh geometry with cogs 53/56/61 additionally movable: **12
mandatory movers and 54 fixed originals**. Preserve their original source angles
initially, all counts, original outlines/cutouts, guards and the target.
The fixed57 domain tables, area bounds and conditional capacities cannot be
transferred unchanged. Recompute and independently audit the expanded regions,
and verify that the prior partial remains representable before deciding a new
bounded construction. All completed calls remain closed.

A complete native-valid target, production integration and the full
13-job/two-kerf H5 matrix remain required. H2 keeps its original gate and all
22 reserved vectors untouched. Production and READMEs are unchanged; no new
release is qualified. Preview v0.2.0-alpha.1 and stable v0.1.0 remain appropriate.

All **six** jobs on [main CI 40252355666](https://github.com/skulitom/Nestbolt/actions/runs/40252355666)
now pass for **68c82ae1**. Upstream Sparrow/Studio state is unchanged. This
checkpoint and queued **7c5b8b28** are ready for a normal main push after fresh
ancestry and remote-ref verification.

Evidence: [comparison]({NAME}/comparison.json),
[one-sided proof]({NAME}/one-sided-equivalence-proof.json),
[conflict proof]({NAME}/restored-conflict-proof.json),
[neighborhood inspection]({NAME}/neighborhood-inspection.json),
[checks]({NAME}/checks.json), and [raw manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}**
exact-content aliases are size/SHA-256/CRC verified in **{archive['archive_parts']}**
independently readable archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 one-sided directions and restored conflicts, 2026-10-26:** [the evidence]({link})
retains two closed UNKNOWN calls. Exact monotone completion permits removal
of 101,455 complement clauses. A second model restores all 5,561,575 proven
domain conflicts across all families, adding only 3,395 auxiliaries and 7,886
constraints. Complete model and bit-matrix audits pass. Both total budgets
pass at 47.741708s/48.140666s; soft overruns of 0.486188s/0.358075s remain recorded.
No target layout or impossibility proof is obtained. A visually inspected
63-original partial identifies adjacent fixed cogs 53/56/61 for a broader
12-mover/54-fixed geometry investigation. Its domains, area bounds and capacities
must be recomputed; prior fixed57 restrictions cannot be carried over. All
earlier calls remain closed. All six checks on main 68c82ae1 now pass, allowing
the queued checkpoints to be pushed normally. H2/H5 remain open at 60%; source,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'prior_main_ci_successes':6},flush=True)
if __name__=='__main__':main()
