"""Seal complete stronger two-core exclusion and the next conflict-owner census."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-strong-pair-relocation-exclusion-20261025';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-strong-pair-convex-domains-recovered-20261025'
FAILED=ROOT/'output/h5-strong-pair-convex-domains-20261025'
REG=ROOT/'output/h5-original-fixed-pair-regions-recovered-20261025'
PRIOR=ROOT/'output/h5-pair-core-relocation-regions-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    generation=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');model=load(BASE/'solve/model-audit.json')
    solved=load(BASE/'solve/result.json');recovery=load(BASE/'recovery-plan.json');nextcase=load(BASE/'next-neighborhood/census.json')
    assert audit['passed'] and model['passed'] and generation['queries_completed']==generation['queries_planned']==2206
    assert not load(BASE/'pending.json') and not generation['domain_cap_reached'] and not generation['merge_cap_queries'] and not generation['merge_time_queries']
    assert solved['status']=='INFEASIBLE' and solved['solver_calls']==1 and not solved['incumbents'] and not solved['has_full_stronger_proxy_solution']
    assert not (BASE/'solve/positions.json').exists()
    log=(BASE/'solve/solver.log').read_text(encoding='utf-8');assert 'Starting search at 4.70s' in log and '#Done   20.57s no_lp' in log and 'LRAT_status: NA' in log
    assert load(PRIOR/'audit/checks.json')['excluded_cases']==299 and load(REG/'audit/checks.json')['cases_excluded']==22
    assert 299+22+audit['cases']==528 and nextcase['fixed_original_parts']+nextcase['mandatory_movable_original_parts']==66
    prior=load(ROOT/'benchmarks/results/h5-original-outline-collision-regions-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('8528180d') and mainhead.startswith('247e823a')
    ci=load(BASE/'source-sync/completed-main-ci.json');assert ci['headSha']==mainhead and ci['conclusion']=='success' and all(j['conclusion']=='success' for j in ci['jobs'])
    action='All528 recorded two-core relocation neighborhoods are now excluded:299 by prior area bounds,22 by complete empty-role regions,207 by this fully audited stronger bounded model. Do not retry or extend any completed call, or expand this into an unsupported unrestricted impossibility claim. Next use the prepared conflict-owner census for a distinct larger construction: release originals50,54,57,58,62,64,65 (one vertical insert and six cogs), restore all seven, and add both missing brackets. Keep57 other source originals fixed; all nine movable originals remain mandatory and every allowed sheet/position stays free. This releases every fixed owner in the certified prior conflict list, not a selected subset. Independently certify the moving insert proxy and its new fixed-original collision cache entries; reuse immutable existing caches. Build fresh complete domains from the original stock bounds, not the narrower two-core free cells, under a declared budget. Preserve original area charges, material cap, finite source orientation inventory and all-angle cog containment. Independently audit full domain coverage and exact mutual convex-component separation before any separately declared bounded model. A positive still needs actual cog outlines/angles, original clearance/native guards, production budget and all13 jobs/two kerfs. H2 stays open; no held-out access or new release. Main CI40233299884 now passed all six jobs; perform the authorized normal push of accumulated checkpoints after this evidence is committed, and follow the new run separately.'
    OUT.mkdir()
    for path,name in [('plan.json','domain-plan.json'),('result.json','domain-result.json'),('audit/checks.json','domain-audit.json'),
                      ('support-atlas.json','support-atlas.json'),('audit/selected-anchor-checks.json','selected-anchor-checks.json'),
                      ('solve/plan.json','solver-plan.json'),('solve/model-audit.json','model-audit.json'),('solve/result.json','solver-result.json'),
                      ('next-neighborhood/census.json','next-neighborhood.json'),('source-sync/completed-main-ci.json','completed-main-ci.json')]:
        shutil.copyfile(BASE/path,OUT/name)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head_before_push':mainhead,
          'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
          'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,
          'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,
          'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,
          'completed_main_ci_id':40233299884,'completed_main_checks':6,'normal_push_ready_after_commit':True,'next_investigation':action})
    members={};inputs={}
    for root in [FAILED,BASE]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for n,h in load(BASE/'plan.json')['region_cover_hashes'].items():
        p=REG/'audit/covers'/f'{int(n):04d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for n,h in load(BASE/'solve/plan.json')['prior_case_hashes'].items():
        p=PRIOR/'cases'/f'{int(n):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for row in load(BASE/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['build_h5_strong_pair_domains.py','recover_h5_strong_pair_domains.py',
             'build_h5_strong_pair_domains_recovered.py','audit_h5_strong_pair_domains.py','solve_h5_strong_pair_neighborhoods.py',
             'audit_h5_strong_pair_model.py','prepare_h5_conflict_neighborhood_census.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    p=ROOT/'output/h5-strong-domain-recovery-plan.json';members['helpers/'+p.name]=p
    archive,manifest=pack(ROOT,OUT,NAME,members)
    checks={'passed':True,'all207_cases286_allocations_and2206_queries_covered':True,
            'all32626_convex_domains_and165640_outward_halfplanes_audited':True,
            'all324_exact_minkowski_hulls_and1852_facet_normals_verified':True,
            'empty_set_guard_failure_preserved_and40_queries_reused_unchanged':True,
            'all56046_variables356662_constraints_and_parameters_reconstructed':True,
            'one_bounded_stronger_call_infeasible_without_incumbent':True,'lrat_certificate_available':False,
            'all528_recorded_two_core_neighborhoods_conditionally_excluded':True,
            'unrestricted_infeasibility_claimed':False,'next57_plus9_neighborhood_retains_all66_original_parts':True,
            'all6_previous_main_checks_passed':True,'production_source_and_readmes_unchanged':True,
            'full_target_witness':False,'native_margin_qualified':False,'H5_complete':False,'completion_percent':60,**archive}
    write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: stronger two-core relocation exclusion — 2026-10-25

**The stronger joint model returns INFEASIBLE for all 207 remaining two-core
cases and 286 sheet allocations.** With the earlier 299 area exclusions and
22 empty-role exclusions, all **528 recorded two-core neighborhoods** are now
closed. This is conditional on the source poses and finite orientation
inventory; it does not prove unrestricted packing impossibility. H2/H5 remain
open at **60%** completed milestone weight.

## Complete convex domains

All eligible modes of the 207 cases produce **2,206 queries**. The domain
source is the previously audited outward region cover, including all original
grid anchors and boundary cases. Each positive-area component is triangulated;
only convex adjacent unions are merged, with every unmerged face retained.
Each face expands by a 0.001 mm square, and the complete expanded union must
cover the whole input region. This is a necessary outer cover, not accepted
cutting geometry. No extra floor-anchor shift or sampled pose set is introduced.

The first phase writes 40 complete query outputs, then an empty input region
triggers a guard failure: GEOS `covers(empty, empty)` returns false even though
empty-set coverage is vacuously satisfied. The failure and original code are
preserved. Its observed plan-to-failure interval is
**{recovery['wall_seconds_plan_to_failure']:.6f} seconds**. Recovery charges 60
seconds to that phase and uses at most the remaining 60 seconds of the original
120-second budget. It reuses all 40 query files and the support atlas byte for
byte, changes only the empty-region guard, and computes 2,166 unfinished queries.

The recovered phase completes in **{generation['seconds']:.6f} seconds**, with
**32,626 convex domains**, no pending queries and no domain, merge or time cap.
Each normalized rational edge is rounded at coefficient scale 10⁷. The exact
worst-case coefficient error over the complete coordinate range is added,
plus one unit, before ceiling the upper bound. Integer bounding intervals also
round outward. This preserves every source integer anchor.

Independent verification takes **{audit['seconds']:.6f} seconds**. It checks
all **165,640 outward halfplanes** with **960,962 exact rational vertex tests**,
complete whole-region coverage, all 2,206 source-cover hashes against committed
evidence, six other source matches and **398** original source-pose integer
memberships. Three selected false anchors remain rejected after rounding.

## Exact stronger collision conditions

The moving cog uses the complete floor-safe 16-gon, already proved inside every
rotated original cog across all coordinate-floor errors. Brackets retain two
coupled rectangle components and restored horizontal frames one rectangle.
An exact integer support atlas contains **18 convex component types** and
**20 common edge normals**. An independent integer monotone-chain oracle
reconstructs all **324 ordered component Minkowski hulls**, verifies all support
values, and confirms all **1,852 hull facets** use normals in that basis.

Coordinates use 0.01 mm units and shape vertices 0.0001 mm units. For every
cross-part convex-component pair on the same sheet, some normal must satisfy
`100 × n·(anchorB − anchorA) ≥ supportA(n) + supportB(−n)`.
Every term is integer, so no projection rounding is needed. Touching is allowed
in this necessary diagnostic. Both bracket arms share the same part position
and mode; no same-part separation is imposed. The old five-rectangle cog check
is not used as a substitute for the stronger polygon.

## Fully audited bounded search

One model retains all 207 cases and 286 allocations, with 62 original source
poses fixed per selected case and four movable parts mandatory. It contains:

| Model element | Count |
| --- | ---: |
| Variables / constraints | 56,046 / 356,662 |
| Role/mode choices | 3,958 |
| Complete per-part convex-domain choices | 51,197 |
| Reified outward domain halfplanes | 248,866 |
| Physical part pairs / component pairs | 6 / 13 |
| Exact projection separation choices | 260 |
| Component support variables | 120 |

Original area charges and sheet-allocation links remain. There are no optional
original parts, objectives, hints or copy-order restrictions. Construction takes
**{model['construction_seconds']:.6f} seconds** and a separate protobuf oracle
reconstructs every variable, constraint, support value, sheet-XOR truth table
and solver parameter in **{model['audit_seconds']:.6f} seconds**.

One declared 60-second, eight-worker, seed-zero call starts search at 4.70
seconds and records `#Done 20.57s no_lp`. It returns **INFEASIBLE in
{solved['seconds']:.6f} seconds**, with 29,266 branches, 7,458 conflicts and no
incumbent. The solver reports `LRAT_status: NA`; no separate formal LRAT proof
is claimed. The completed call is neither retried nor extended.

## Broader construction prepared from actual conflicts

The previous false arrangement moved cogs 58 and 65. Its certified fixed-owner
collision list contains items **50, 54, 57, 62 and 64**. The next census releases
all of them together: one vertical insert (class 13, modes 22/23) and six cogs,
plus both mandatory missing brackets. That gives **57 fixed originals + 9
mandatory movable originals = 66**, with no deletion or partial-count objective.
All source orientations and permitted sheets are recorded. This is preparation,
not a search or feasibility claim. Fresh domains must start at the full original
stock bounds; the narrower two-core domains must not restrict the larger move.

{action}

## Repository and evidence

All six jobs in main 247e823a's existing **CI40233299884** now pass. The snapshot
is terminal success, not a restarted run or inferred pass. The accumulated
checkpoints are ready for the next authorized normal push after this evidence
is committed. This source checkpoint starts at {head[:8]}; a new post-push run
must be tracked separately. Production source, all three accurate READMEs and
release versions remain unchanged. No native packing, quality matrix, held-out
evaluation or new release occurs; H5 is not qualified by this diagnostic.

Evidence: [domain plan]({NAME}/domain-plan.json), [domain audit]({NAME}/domain-audit.json),
[support atlas]({NAME}/support-atlas.json), [full model audit]({NAME}/model-audit.json),
[bounded result]({NAME}/solver-result.json), [next neighborhood]({NAME}/next-neighborhood.json),
[completed main CI]({NAME}/completed-main-ci.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All **{archive['archive_members']}**
canonical members and **{archive['verified_aliases']}** identical-content aliases
retain exact bytes with CRC/SHA-256 checks, including the initial guard failure,
all domains/rounding data, full model/log, source inputs and executed helpers.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 stronger two-core relocation exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) covers all 207 remaining cases
and 286 allocations with 32,626 convex domains, 165,640 outward halfplanes and
960,962 exact vertex tests. The empty-set guard failure is preserved; 40 completed
queries are reused unchanged within the original work budget. An exact support
atlas audits 324 convex Minkowski hulls and every relevant edge normal. The full
56,046-variable/356,662-constraint model uses the stronger cog 16-gon directly.
One bounded call returns INFEASIBLE in 20.878256 seconds with no incumbent or
LRAT certificate. Together with prior 299 area and 22 empty-role exclusions,
all 528 recorded two-core neighborhoods are closed, conditionally on the source
poses/inventory. A distinct conflict-owner census prepares 57 fixed plus nine
mandatory movable originals, preserving all 66 parts. All six existing main
checks now pass; accumulated commits are ready for the next normal push.
No unrestricted impossibility, accepted target or H5 qualification is claimed.
Source, accurate READMEs and releases stay unchanged; H2/H5 remain open at 60%.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)

if __name__=='__main__':main()
