"""Seal the guarded fixed-core exclusion and the unresolved global relaxation."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-guarded-core-and-global-relaxation-20261025';OUT=ROOT/'benchmarks/results'/NAME
FIX=ROOT/'output/h5-guarded-alternate-outer-20261025';GLOBAL=ROOT/'output/h5-global-disk-relaxation-prepared-20261025';FAILED=ROOT/'output/h5-global-disk-relaxation-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    fa=load(FIX/'audit/checks.json');fm=load(FIX/'solve/model-audit.json');fr=load(FIX/'solve/result.json');ga=load(GLOBAL/'audit/checks.json');gm=load(GLOBAL/'solve/model-audit.json');gr=load(GLOBAL/'solve/result.json');ba=load(GLOBAL/'baseline-audit/checks.json');prior=load(ROOT/'benchmarks/results/h5-outer-coordinate-relaxation-20261025/source-review.json')
    assert all(v['passed'] for v in [fa,fm,ga,gm,ba]);assert fr['status']=='INFEASIBLE' and gr['status']=='UNKNOWN';assert fr['solver_calls']==gr['solver_calls']==1 and not fr['incumbents'] and not gr['incumbents'];assert not load(FIX/'pending.json') and load(FIX/'result.json')['completed_queries']==24;assert not(FIX/'solve/relaxed-layout.json').exists() and not(GLOBAL/'solve/relaxed-positions.json').exists();assert not(FAILED/'geometry.json').exists() and not(FAILED/'solve').exists()
    flog=(FIX/'solve/solver.log').read_text(encoding='utf-8');glog=(GLOBAL/'solve/solver.log').read_text(encoding='utf-8');assert re.findall(r'^#Done\s+([0-9.]+)s\s+([^\s]+)',flog,re.M)==[('9.78','no_lp')];assert 'Starting search at 1.83s' in flog and 'Starting search at 1.62s' in glog and 'status: UNKNOWN' in glog and 'LRAT_status: NA' in flog
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head.startswith('56678ee9') and mainhead.startswith('8f941426');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items());ci=json.loads(subprocess.check_output(['gh','run','view','40229962984','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==mainhead
    action='Do not retry or extend either completed call, or revisit small pose sampling with either excluded fixed core. Investigate propagation for the all-parts-movable necessary relaxation. First derive and independently audit original filled-area lower bounds and outward usable-sheet capacity bounds, preserving the actual cog areas even though the geometric model uses smaller inscribed polygons. Then derive optional inner rectangles for every original non-cog component and a rotation-invariant inner square for each cog; their floor-grid placement must remain a subset of every valid original placement. These support global NoOverlap2D/cumulative propagation across all parts without choosing a fixed frame/cog arrangement. Keep all original orientations and both original stock domains, all66 counts, original material target and no part-in-hole. Declare new limits before any strengthened model construction or single solver call, independently reconstruct the full encoding, and retain UNKNOWN/caps. Do not simply change the seed or extend time on the completed model. A positive relaxation still needs original cog shapes/angles, original clearance, native guards, the production budget and all13jobs at both kerfs. H2 remains open by explicit instruction; do not evaluate the22 reserved vectors or ask the same denominator question again.'
    OUT.mkdir();write(OUT/'next-step.json',{'action':action,'H5_complete':False,'full_target_witness':False})
    interpretation={'guarded_alternative':{'status':fr['status'],'seconds':fr['seconds'],'fixed_original_parts':33,'required_original_small_parts':33,'conditional_conclusion':'The audited complete continuous outer regions and model exclude a full66-part placement with the guarded core5 arrangement held fixed. Different frame/cog arrangements remain open.','proof_limit':'Solver-reported infeasibility of the fully audited model, without an independently checked LRAT proof; geometric implication is conditional on the recorded original polygon/rotation and outward-coverage audits.'},'global':{'status':gr['status'],'seconds':gr['seconds'],'fixed_parts':0,'required_original_parts':66,'conclusion':'Unresolved after one declared60-second call. No incumbent or proof; not evidence that the unrestricted target is impossible. The model uses cog inscribed polygons, so even a positive result would remain a relaxation.'},'H5_complete':False,'full_target_witness':False,'native_margin_qualified':False};write(OUT/'interpretation.json',interpretation)
    copies=[(FIX/'plan.json','guarded-plan.json'),(FIX/'result.json','guarded-generation.json'),(FIX/'audit/checks.json','guarded-coverage-audit.json'),(FIX/'audit/provenance.json','guarded-provenance.json'),(FIX/'solve/plan.json','guarded-model-plan.json'),(FIX/'solve/model-audit.json','guarded-model-audit.json'),(FIX/'solve/result.json','guarded-solver.json'),(GLOBAL/'plan.json','global-plan.json'),(GLOBAL/'generation.json','global-generation.json'),(GLOBAL/'audit/checks.json','global-geometry-audit.json'),(GLOBAL/'audit/provenance.json','global-provenance.json'),(GLOBAL/'baseline-audit/checks.json','global-baseline-audit.json'),(GLOBAL/'solve/plan.json','global-model-plan.json'),(GLOBAL/'solve/model-audit.json','global-model-audit.json'),(GLOBAL/'solve/result.json','global-solver.json')]
    for p,n in copies:shutil.copyfile(p,OUT/n)
    write(OUT/'main-ci.json',ci);write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':2,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,'next_investigation':action})
    members={};inputs={}
    for root in [FIX,GLOBAL,FAILED]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for source in [FIX/'audit/provenance.json',GLOBAL/'audit/provenance.json']:
        for row in load(source)['source_members_matching_committed_evidence']:
            for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
                p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['build_h5_guarded_alternate_outer.py','audit_h5_guarded_alternate_outer.py','prepare_h5_guarded_alternate_solver.py','solve_h5_guarded_alternate_outer.py','solve_h5_outer_coordinates.py','solve_h5_direct_coordinates.py','prepare_h5_global_disk_relaxation.py','audit_h5_global_disk_geometry.py','solve_h5_global_disks.py','audit_h5_global_disk_baseline.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'guarded_alternative_all24_continuous_regions_verified':True,'guarded_alternative_conditional_exclusion_recorded':True,'global_all66_parts_movable':True,'global_all_angle_disk_and_original_components_audited':True,'global_all_model_fields_verified':True,'global_result_unresolved_not_infeasible':True,'global_partial64_sanity_check_only':True,'one_call_per_model_no_extensions':True,'first_failed_preparation_preserved':True,'production_source_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,'H5_complete':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: guarded-core exclusion and all-parts-movable relaxation — 2026-10-25

**The guarded alternative cannot complete the inventory while its 33 frame/cog
placements stay fixed, within the audited outer geometry model. A new model
allowing all 66 parts to move is unresolved.** Neither result completes H5.
H2/H5 remain open at **60%** completed milestone weight.

## Guarded alternative: complete continuous regions

The preceding checkpoint moved one cog in saved core 5 by
(+0.0125, -0.0125) mm and independently checked all original fixed-part distances
and stock margins. Here all 24 zero-clearance forbidden unions and translation
regions are rebuilt for that changed arrangement. Only 36 hash-bound **local**
Minkowski obstacles are reused; their global translations and complete unions
are recomputed. All 12 permitted small-part orientation/reflection cases and
both original stock domains remain, including continuous unsampled positions.

Construction finishes in 1.075203 seconds within its declared 120 seconds,
with no pending queries. The independent 7.389211-second audit checks:

- 73 input/template/cache matches against committed manifests;
- 36 local obstacles from 860 convex-piece vertex sums and all 12 translated
  obstacles for the moved cog (maximum Hausdorff difference 1.28e-13 mm);
- all 24 new unions, subset exclusions and stock regions;
- 864 complete outer cells/domains, 18,724 required quantization vertices,
  and 4,681 outward rational halfspaces/expanded vertices;
- 33,720 saved small-part poses, 804,591 original fixed-pair distances and
  33,720 union-distance crosschecks.

All **12,860** saved original poses compatible with this core have encoded
floor-grid representatives. Compatible portions of four old baselines total
61, 61, 58 and 58 parts, including the 33 fixed parts; these remain partial.
Their 1,642 cross-part rectangle relations also check. As with core 0, the
0.001 mm subset exclusion, expanded stock, outward quantization and allowed
one-grid-unit overlap deliberately enlarge the diagnostic feasible space.
They are never acceptable production settings.

The model mandates all 12 brackets and 21 inserts in addition to 33 fixed parts.
Every field of its **20,907 variables and 121,531 constraints** is reconstructed
independently. It retains 15,795 domain choices, 360 orientation/sheet modes,
and all 978 cross-part component pairs with coupled bracket arms.

One declared 60-second call reaches search at 1.83 seconds and reports
`#Done 9.78s no_lp`, with total elapsed **{fr['seconds']:.6f} seconds**.
Status is `INFEASIBLE`, with 112,187 branches, 16,457 conflicts and no incumbent.
The conditional exclusion depends on the full coverage/model audits; there is
no separately verified LRAT proof. Other frame/cog arrangements remain open.
This completed call is not retried or extended.

## All parts movable: a new necessary relaxation

The next investigation removes the fixed arrangement entirely. All original
18 frames, 12 brackets, 21 inserts and 15 cogs choose positions across the same
two original sheet domains and material-height cap. Every permitted non-cog
orientation/reflection remains. No fixed frame set, finite pose list, hint,
objective or missing-part variable is used; only interchangeable-copy ordering
removes symmetry. Holes remain reserved, as required by the original plan.

The earlier exact-rational cog certificate proves a disk of radius
**109.1157 mm** lies strictly inside every filled cog outline, for every cog
rotation. Each cog is represented here by the same fixed-axis convex 16-gon
strictly inside that disk, with a freely moving center. This is a necessary
relaxation, not a substitute for the original cog outline in an accepted layout.
The three other part families retain exact original rectangular components;
the two bracket arms share one orientation and position.

An independent rational audit rechecks all 80 cog boundary distances and the
interior center, all 16 polygon vertices, all 16 non-cog orientation/reflection
cases and their complete rectangle decompositions. It independently constructs
1,792 Minkowski vertex sums, verifies every required separating normal and
all **496** outward separation thresholds. The 28 non-cog sheet/orientation
modes and two cog-center stock domains are rounded outward. Flooring positions
to 0.01 mm changes a relative coordinate by less than one grid unit per axis;
the exact integer inequalities explicitly allow that entire error. Positive
clearance is dropped only in this diagnostic relaxation.

The first preparation failed before producing geometry because an integral
source coordinate remained a floating value at a rational constructor. Its
original helper, plan and failure record are preserved. The corrected helper
checks integrality and converts to exact integers before transformation, in a
separate output directory. It completes in 0.004456 seconds; the independent
geometry audit completes in 0.060897 seconds. No solver had run in the failed
preparation, and no completed phase or capped search was resumed.

## Global encoding and bounded result

All **31,467 variables and 37,061 constraints** are independently reconstructed
from the audited geometry before execution. The model contains 462 modes,
all 2,145 physical-part pairs, 1,941 rectangle/rectangle component pairs,
945 disk/rectangle pairs and 105 disk/disk pairs. Every separating disjunction,
conditional sheet relation, component offset, coordinate bound, copy-order
constraint and solver parameter checks. Construction takes 1.021424 seconds;
the independent encoding audit takes 0.322366 seconds, both within declared
120-second caps.

One declared 60-second, eight-worker, seed-zero call reaches search at
1.62 seconds. It returns **`UNKNOWN`** in **{gr['seconds']:.6f} seconds**, retaining
the solver's small soft-limit overrun. There is no incumbent after 758,223
branches and 75,218 conflicts. This is unresolved, not an infeasibility proof.
No original layout is manufactured from this outcome, and the call is neither
extended nor repeated.

A separate sanity check maps the preserved original 64-part layout into this
new model. All stock domains and all 1,898 same-sheet component relations check;
the maximum quarter-turn transform difference is 5.69e-14 mm. It still lacks
two brackets and is never a solution to the mandatory 66-part model or a solver
hint. The global relaxation remains open even though the two previously tested
fixed arrangements have conditional negative results.

## Next investigation and repository state

{action}

Engine source, all three accurate READMEs and release versions are unchanged.
Main 8f941426's hosted checks are captured as `{ci['status']}` /
`{ci['conclusion'] or 'pending'}`; no unfinished hosted run is called a pass.
The three newer evidence commits remain local at source head {head[:8]} while
that main run completes, avoiding cancellation by another push. No production
tests are rerun for evidence-only changes. There are no native packing calls,
quality runs, held-out evaluations or newly qualified releases here.

Evidence: [guarded coverage]({NAME}/guarded-coverage-audit.json),
[guarded model]({NAME}/guarded-model-audit.json), [guarded result]({NAME}/guarded-solver.json),
[global plan]({NAME}/global-plan.json), [global geometry]({NAME}/global-geometry-audit.json),
[global model]({NAME}/global-model-audit.json), [global result]({NAME}/global-solver.json),
[partial baseline check]({NAME}/global-baseline-audit.json),
[interpretation]({NAME}/interpretation.json), [source review]({NAME}/source-review.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']} canonical members and {archive['verified_aliases']}
aliases retain exact bytes with CRC and SHA-256 checks, including both complete
models/logs, all guarded regions, global geometry and the failed preparation.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 guarded alternative and unrestricted relaxation, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) rebuilds and audits all 24
continuous regions around the guarded core-5 alternative: 864 outward domains,
18,724 coverage vertices and all 12,860 compatible saved small-part poses.
Its independently checked exact-count model reports INFEASIBLE in 9.923168
seconds, conditionally excluding that fixed arrangement. A new necessary
relaxation lets all 66 parts move and represents each freely rotating cog by
a polygon strictly inside its certified 109.1157 mm inscribed disk. Original
non-cog components, orientations, counts and target sheet domains remain.
Independent geometry and complete 31,467-variable/37,061-constraint encoding
audits pass. One 60-second call returns UNKNOWN in 60.152007 seconds with no
incumbent or proof; the preserved 64-part sanity check still lacks two brackets.
Both completed calls and the initial failed geometry preparation are retained.
Next investigate audited original-area bounds and global packing propagation;
do not retry unchanged calls or weaken acceptance. No full target witness,
native qualification, production-budget run or H5 matrix result is obtained.
Source, accurate READMEs and releases are unchanged; H2/H5 remain open at 60%.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
