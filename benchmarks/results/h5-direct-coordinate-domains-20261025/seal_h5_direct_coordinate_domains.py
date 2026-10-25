"""Seal verified continuous safe domains before constructing the exact-count solver model."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-direct-coordinate-domains-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    generation=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');merge=load(BASE/'consolidated/result.json');checked=load(BASE/'consolidated/audit/checks.json');prior=load(ROOT/'benchmarks/results/h5-occupied-area-relaxation-20261025/source-review.json');assert audit['passed'] and checked['passed'] and generation['pending_queries']==merge['pending_merge_queues']==0;assert checked['implied_per_copy_domain_choices']==55992
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items());head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head==mainhead=='8f9414267add0024177ea7172079d8f16dd27842'
    oldci=json.loads(subprocess.check_output(['gh','run','view','40228140192','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));ci=json.loads(subprocess.check_output(['gh','run','view','40229962984','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==head
    action='Construct and independently check one exact-count coordinate model from consolidated/audit/integer-domains.json. Use one anchor x/y pair, permitted orientation and sheet choice per physical small part. Require all12 brackets and21 inserts; keep core0 unchanged. Connect each piecewise-convex domain to its orientation and sheet with all inward-rounded inequalities and bounds. Model each bracket as two coupled original rectangular arms; enforce at least0.22mm directional separation only between rectangles belonging to different physical parts, including all cross-arm pairs. All original stock bounds,0.02mm additional new-part stock margin and fixed-part safe domains remain. Symmetry ordering may only permute identical copies. The remaining55992 per-copy domain alternatives motivate certified containment removal or factoring before encoding; any removed domain must map to a retained same-sheet/same-orientation superset with independently checked rational halfspace certificates. No lost feasible grid point or arbitrary candidate pruning is allowed. Preserve all source regions and baselines. Verify every model and parameter field before exactly one predeclared60-second/eight-worker/seed-zero solver call. UNKNOWN is not infeasibility and the call must not be extended or repeated. Any full witness requires original geometry and CLI checks, actual native collision checks, original production budget and all13 jobs at both kerfs. No renewed capped pose generation, acceptance weakening, reserved-file access or new release is authorized by this diagnostic.'
    write(BASE/'next-step.json',{'action':action,'solver_calls':0,'full_target_witness':False})
    OUT.mkdir()
    for source,name in [('plan.json','plan.json'),('result.json','generation.json'),('audit/checks.json','audit.json'),('audit/provenance.json','provenance.json'),('consolidated/plan.json','consolidation-plan.json'),('consolidated/result.json','consolidation.json'),('consolidated/audit/checks.json','consolidation-audit.json'),('next-step.json','next-step.json')]:shutil.copyfile(BASE/source,OUT/name)
    write(OUT/'previous-main-ci.json',oldci);write(OUT/'main-ci.json',ci)
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','full_target_witness':False,'native_margin_qualified':False,'solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'next_investigation':action};write(OUT/'source-review.json',review)
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for row in load(BASE/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['build_h5_direct_coordinate_domains.py','audit_h5_direct_coordinate_domains.py','consolidate_h5_direct_coordinate_domains.py','audit_h5_consolidated_coordinate_domains.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'all20_safe_regions_verified':True,'all12_permitted_orientations_accounted_for':True,'all3884_source_faces_preserved':True,'integer_rounding_independently_verified':True,'all_consolidated_hulls_inside_checked_positive_clearance_regions':True,'no_solver_called':True,'original_full_inventory_required':True,'native_margin_qualified':False,'full_target_witness':False,'production_source_and_readmes_unchanged':True,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: checked direct-coordinate domains — 2026-10-25

**Continuous placement regions are verified; packing has not been solved.**
The next model requires all 12 brackets and 21 inserts around the unchanged
18-frame/15-cog core 0. Original quantities, stock/material target and native
requirements remain. H2/H5 are open at **60%** completed weight.

## A different representation of the remaining placement problem

Earlier searches chose among finite saved poses or whole macro rectangles.
This construction instead permits each small part to move on a 0.01 mm
coordinate grid within independently checked convex translation regions.
Source-exact quarter turns and reflections turn the L bracket into its two
coupled rectangular arms. The insert is one rectangle. All twelve permitted
orientation/reflection cases map to ten distinct normalized shapes; equivalent
insert quarter turns are explicitly recorded. The normalized original floating
transforms differ by at most {audit['maximum_original_float_transform_error_mm']:.3g} mm.
Holes remain reserved. No arbitrary part contour or inventory is substituted.

Core 0 is selected because the previous census finds it alone passes both
conservative pair and stock screens. This still requires actual native
transformed-collision validation. New-part regions use **0.22 mm** separation
plus an explicit construction margin, and **0.02 mm** additional stock margin.

## Construction and exact inward rounding

All **20** orientation/sheet queries complete in
**{generation['seconds']:.6f} seconds**, within 120 seconds, with no pending query.
Exactly covering convex-piece Minkowski sums build the fixed-part obstacles.
Their union is expanded with an explicitly circumscribed 128-sided clearance
polygon at 0.22 + 0.0001 mm. Original stock domains are reduced by the declared
extra margin. Constrained triangulation covers the safe regions exactly;
only convex adjacent unions merge. All unmerged faces remain.

The first independent audit verifies 20 cached obstacles from 396 convex-piece
vertex sums, every complete safe region, 3,884 convex faces and 12,865 rational
halfspaces. Edge coefficients are derived from exact rational representations
of the stored binary-float vertices. Their integer bounds subtract the full
worst-case rounding error over the bounded coordinate domain, plus one unit.
Exact rational clipping verifies **16,455** vertices against the original face
edges. Twelve domains have empty rational intersections or empty integer
bounding intervals; 3,872 remain, implying 58,434 per-copy alternatives.
Removing these empty domains loses no feasible point from this grid model.

## Certified domain consolidation

A separate predeclared 60-second/200,000-attempt consolidation completes in
**{merge['seconds']:.6f} seconds** after 36,810 merge attempts. Every source
face remains represented exactly once in a recorded lineage. A convex hull
may replace adjacent faces only if the entire hull lies in a separately
reconstructed safe region with the same **0.22 mm** gap and an additional
0.00001 mm construction margin. A hull can add translation space but remains
inside that checked region; its area is not packed material or a quality score.
No part count, required gap or stock domain is reduced.

The independent consolidation audit rebuilds every clearance envelope and
stock domain, verifies all source-face coverage and all hull containment,
and checks **12,655** rational halfspaces and **16,191** resulting vertices.
It retains **3,703** grid domains: 2,419 bracket and 1,284 insert domains.
Twelve proven-empty domains are retained as explicit exclusions. The total
per-copy alternative count falls to **55,992**. Every merge queue finishes;
neither construction phase is repeated or extended.

The resulting domains are conservative feasible subsets. Their inability to
pack would not prove the unrestricted original geometry impossible. No
solver, complete layout, native qualification or production-quality result
has been produced by this work.

## Next exact-count model

{action}

## Repository and evidence

Both earlier audit checkpoints are pushed to main as **8f941426**. Its hosted
checks are captured as `{ci['status']}` / `{ci['conclusion'] or 'pending'}`.
Previous main 55835d7c's run is `{oldci['conclusion'] or oldci['status']}`;
the repository's CI workflow cancels an older in-progress run on the same
branch when a newer push starts. Its earlier successful jobs remain recorded.
Engine source, all three accurate READMEs and published releases are unchanged.
No native packing, H5 quality matrix or held-out evaluation occurs.

Evidence: [construction plan]({NAME}/plan.json), [generation]({NAME}/generation.json),
[first audit]({NAME}/audit.json), [consolidation plan]({NAME}/consolidation-plan.json),
[consolidation result]({NAME}/consolidation.json),
[independent consolidation audit]({NAME}/consolidation-audit.json),
[source review]({NAME}/source-review.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All {archive['archive_members']} canonical
members and {archive['verified_aliases']} aliases pass exact byte, SHA-256 and CRC
checks. Original input hashes, every source face, empty-domain reason and
orientation alias are preserved.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 direct-coordinate domain preparation, 2026-10-25:** [the original-geometry and rational audit](../benchmarks/results/{NAME}.md)
checks all20 orientation/sheet regions around fixed core0, representing all
twelve permitted orientation/reflection cases. New placements retain0.22mm
separation and0.02mm extra stock margin. Every inward-rounded halfspace and
all3884 source faces verify. Certified consolidation retains3703 nonempty
grid domains, including all source-face lineages, with55992 per-copy choices
for the full12 brackets and21 inserts. No solver has run and no complete
layout is claimed. Next encode and independently check the exact-count model,
using only certified containment removal if needed before its one declared
60-second solve. Both prior checkpoints are pushed as8f941426; its CI is
pending and the older main run is cancelled. Engine source, accurate READMEs
and releases are unchanged. H2/H5 stay open at60% completed milestone weight.
'''
    # Use readable spacing in durable prose without altering evidence values.
    for a,b in [('all20','all 20'),('core0','core 0'),('retain0.22mm','retain 0.22 mm'),('and0.02mm','and 0.02 mm'),('all3884','all 3,884'),('retains3703','retains 3,703'),('with55992','with 55,992'),('full12','full 12'),('and21','and 21'),('as8f941426','as 8f941426'),('at60%','at 60%')]:note=note.replace(a,b)
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
