"""Archive stronger necessary collision geometry and fully covered pair regions."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-original-outline-collision-regions-20261025';OUT=ROOT/'benchmarks/results'/NAME
GEO=ROOT/'output/h5-original-fixed-collision-geometry-20261025'
FAILED=ROOT/'output/h5-original-fixed-pair-regions-20261025'
REG=ROOT/'output/h5-original-fixed-pair-regions-recovered-20261025'
PRIOR=ROOT/'output/h5-pair-core-relocation-regions-20261025'
load=lambda p:json.loads(p.read_bytes())

def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    geometry=load(GEO/'generation.json');ga=load(GEO/'audit/checks.json');diag=load(GEO/'diagnosis.json')
    regions=load(REG/'result.json');ra=load(REG/'audit/checks.json');recovery=load(REG/'recovery-plan.json')
    assert ga['passed'] and ra['passed'] and geometry['cache_cases_completed']==100 and not load(GEO/'pending.json')
    assert regions['queries_completed']==regions['queries_planned']==2650 and not load(REG/'pending.json')
    assert ra['complete_cases']==229 and (ra['cases_excluded'],ra['surviving_cases'],ra['surviving_allocations'])==(22,207,286)
    assert not ra['empty_status_changes'] and ra['selected_anchor_rejections']==3
    assert not regions['vertex_cap_reached'] and not regions['time_limit_reached']
    assert recovery['wall_seconds_plan_to_failure']<60 and regions['seconds']<60
    assert ra['previously_completed_query_bytes_preserved']==1262 and ra['newly_completed_queries']==1388
    prior=load(ROOT/'benchmarks/results/h5-pair-core-relocation-and-outline-diagnosis-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('6cb2227c') and mainhead.startswith('247e823a')
    ci=load(GEO/'source-sync/main-ci.json');assert ci['headSha']==mainhead
    action='Use only the independently certified outward covers from the recovered region audit as the next domain source. All100 original-fixed collision caches and all2650 eligible mode queries are complete; do not rerun their construction. Preserve the initial mixed-dimensional GEOS guard failure and1262 byte-identical reused outputs. Next declare a bounded convex-domain construction over all207 surviving cases and286 allocations: cover every polygon component of the padded regions, preserve every boundary/point through outward rounding, and independently verify full coverage and integer halfplanes. Then consider one separately declared bounded four-part joint model with all66 counts. Use the new floor-safe16-gon itself for moving cogs and exact coupled rectangle components for brackets/frames. Cross-part separation must include all edge normals of their convex-component Minkowski sums, with independently audited integer projection bounds; do not fall back to the weaker five-rectangle cog collision check alone. Keep all allowed source orientations and sheet allocations, full original-area charges and the target material limit. Any positive still requires actual cog angles/outlines, original clearance/native guards, production budget and all13 jobs/two kerfs. No unchanged search retry, gate reduction, reserved-vector access or new release. Poll existing main CI40233299884 and push accumulated commits normally after it is terminal.'
    OUT.mkdir()
    for root,prefix,paths in [(GEO,'geometry',['plan.json','generation.json','audit/checks.json','diagnosis.json','cog-floor-certificate.json','selected-anchor-conflicts.json']),
                              (REG,'regions',['plan.json','result.json','audit/checks.json','audit/selected-anchor-checks.json','audit/surviving-neighborhoods.json'])]:
        for path in paths:shutil.copyfile(root/path,OUT/(prefix+'-'+path.replace('/','-')))
    write(OUT/'next-step.json',{'action':action,'H5_complete':False,'full_target_witness':False})
    shutil.copyfile(GEO/'source-sync/main-ci.json',OUT/'main-ci.json')
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,
          'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
          'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,
          'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':0,'native_packing_calls':0,
          'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,
          'current_main_ci_id':40233299884,'next_investigation':action})
    members={};inputs={}
    for root in [GEO,FAILED,REG]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for n,h in load(REG/'plan.json')['prior_case_hashes'].items():
        p=PRIOR/'cases'/f'{int(n):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for row in load(GEO/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['prepare_h5_original_fixed_collision_geometry.py','audit_h5_original_fixed_collision_geometry.py',
             'build_h5_original_fixed_pair_regions.py','recover_h5_original_fixed_pair_regions.py',
             'build_h5_original_fixed_pair_regions_recovered.py','audit_h5_original_fixed_pair_regions.py',
             'snapshot_h5_original_collision_ci.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    p=ROOT/'output/h5-pair-region-recovery-plan.json';members['helpers/'+p.name]=p
    archive,manifest=pack(ROOT,OUT,NAME,members)
    checks={'passed':True,'moving_proxy_subsets_exactly_certified_for_all_floor_errors':True,
            'all100_fixed_original_obstacle_caches_independently_reconstructed':True,
            'all43_source_poses_and2000_compatible_pairs_preserved':True,'both_known_false_cog_conflicts_rejected':True,
            'initial_mixed_dimension_guard_failure_preserved':True,'completed1262_queries_reused_byte_identically':True,
            'all2650_queries_and229_cases_covered_after_bounded_recovery':True,
            'all42226_whole_prior_cells_accounted_for_including3081_lower_dimensional_cells':True,
            'independent_positive_padding_is_outer_cover_only':True,'additional22_cases_excluded':True,
            'remaining207_cases286_allocations_not_claimed_feasible':True,'solver_calls':0,
            'production_source_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,
            'H5_complete':False,'completion_percent':60,**archive}
    write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: original-outline collision regions — 2026-10-25

**Stronger necessary geometry rejects three of the four selected coordinates
from the previous false proxy layout and excludes another 22 two-core cases.**
All eligible regions are now covered independently. **207 cases with 286 sheet
allocations remain unresolved.** No solver call or accepted layout is produced;
H2/H5 remain open at **60%** completed milestone weight.

## Stronger geometry with exact subset certificates

All 64 source fixed shapes use their actual original filled outer polygons.
Only exact family/rotation/mirror duplicates share a local collision cache;
every owner, transform and sheet remains distinct. Removing the two released
owners leaves the original 62 fixed parts in each conditional neighborhood.

Moving brackets and horizontal frames retain their existing floor-safe inner
rectangles. A new fixed-axis 16-gon replaces the weaker five-rectangle cog
collision proxy. Its integer vertex radius is 109.1000 mm, inside the certified
all-angle disk of radius 109.1157 mm. The independent audit re-proves the disk
using rational winding and all 80 original edge distances. All 64 vertex/error
corner combinations remain strictly inside that disk after the full 0.01 mm
coordinate-floor uncertainty, with squared margin 35,535,031 at 10,000 geometry
units/mm. Convexity extends this check to every polygon point and every floor
error. All 272 non-cog vertex/error checks also pass. Another 320 exact integer
halfplane checks prove the old five cog rectangles lie strictly inside the new
polygon. Thus the new shape preserves the old necessary conditions and adds
collision geometry without restricting actual cog angles.

Construction completes all **100 fixed-style/moving-proxy cache combinations**
in **{geometry['seconds']:.6f} seconds**, with nothing pending. Each raw
zero-clearance Minkowski obstacle is eroded with a 0.001 mm parameter and
intersected with its raw geometry; only a strict interior subset is forbidden.
This enlarges the diagnostic feasible region and does not change acceptance.

The independent audit uses **106 unmerged constrained triangles and 1,908
component Minkowski hulls**, separately from construction's merged convex
decomposition. All raw obstacles agree within 7.106×10⁻¹⁴ mm Hausdorff distance
and 6.617×10⁻¹⁴ mm² symmetric-difference area. Every eroded exclusion is wholly
inside the independently reconstructed raw obstacle, with minimum actual
boundary distance **0.000994946 mm**; the nominal erosion parameter is not
misreported as an exact achieved distance. All 64 original transforms reconstruct
exactly in this audit. Ten source inputs match committed evidence.

All **43** original frame/bracket/cog source floor poses remain compatible
with their other fixed originals, including **2,000** direct intersection
checks. Testing the four previously selected placements against 62 remaining
originals checks 124 same-sheet pairs and finds five conservative conflicts,
including both previously diagnosed angle-independent cog overlaps. Geometry
auditing takes **{ga['seconds']:.6f} seconds**. This diagnoses selected anchors,
not every coordinate in their former free cells.

## Complete region construction and preserved recovery

The 229 earlier area-surviving cases have 424 allocations and **2,650 unique
eligible role/mode queries**. Each query begins with the entire closed union of
its earlier exact integer free cells. Isolated points and lines are retained.
Only the new strict-interior forbidden sets of the remaining original owners
are subtracted. This is a necessary outer relaxation; positive clearance remains
omitted only in the diagnostic, and all 66 original parts remain mandatory.

The first phase wrote **1,262 complete query results**, then GEOS raised an
overlay-dimension assertion in the optional `free.difference(cover)` consistency
guard at query 1262. The required subtraction itself had succeeded. The failure
and original code/plan remain preserved. No time or cell cap had been reached.
The observed plan-to-failure interval is **{recovery['wall_seconds_plan_to_failure']:.6f}
seconds**. Recovery conservatively charges 60 seconds to that phase and allows
only the remaining 60 seconds of the original 120-second limit.

Recovery omits that faulty reverse-subset guard; the actual subtraction is
unchanged. Every completed result is reused byte for byte, and only the
**1,388 unfinished queries** are computed. The recovered phase, including
verification of reused outputs, takes **{regions['seconds']:.6f} seconds**.
All 2,650 queries finish, with **157,870** raw output vertices, nothing pending
and no vertex/time cap reached. No completed search or query is restarted.

## Independent whole-cell coverage

The audit rebuilds forbidden unions from every remaining fixed original without
the construction's intersection filter. It reconstructs free space separately
for each prior primitive, avoiding the mixed-dimensional reverse-subset operation.
It then positively pads the raw and independently reconstructed free primitives
with a 0.001 mm parameter and unions them into an explicit outward cover.
That padding belongs only to this necessary cover, never accepted geometry.

Every raw and independently reconstructed free primitive is contained in the
cover. More strongly, **cover union verified collision exclusions covers every
whole prior cell**: **42,226** exhaustive cells, including **3,081** isolated
point/line cells. This is not a point sample. All **29,314** raw primitives and
29,314 independently reconstructed primitives are covered. The largest added
outer area is **17.180844 mm²**. This is a deliberate permissive enlargement;
no false accepted layout or original-area charge is inferred from it.

All **458** applicable released source-pose memberships pass. Padding changes
no query's empty/nonempty status. There are **974 empty queries**. Rechecking
every allocation against complete role availability excludes **22 cases** and
leaves **207 cases / 286 allocations**. Three of the prior four selected anchors
are outside these certified covers, including the falsely placed cog. This
independent audit takes **{ra['seconds']:.6f} seconds**. Nonempty regions do not
show that the four movable parts fit together.

## Next work and repository state

{action}

Production source, all three accurate READMEs and release versions are unchanged.
The captured existing main CI40233299884 at 247e823a remains `{ci['status']}` /
`{ci['conclusion'] or 'pending'}`. Five checks have passed and Windows remains
live in that snapshot; it is not restarted or called successful. This checkpoint
starts at {head[:8]}. No native packing, quality matrix, held-out access or new
release occurs.

Evidence: [geometry plan]({NAME}/geometry-plan.json),
[geometry audit]({NAME}/geometry-audit-checks.json), [floor certificate]({NAME}/geometry-cog-floor-certificate.json),
[region plan]({NAME}/regions-plan.json), [region result]({NAME}/regions-result.json),
[whole-cell audit]({NAME}/regions-audit-checks.json), [surviving cases]({NAME}/regions-audit-surviving-neighborhoods.json),
[source review]({NAME}/source-review.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All **{archive['archive_members']}**
canonical members and **{archive['verified_aliases']}** identical-content aliases
retain exact bytes with CRC/SHA-256 checks, including the original failure,
every raw obstacle/query, all certified covers, sources and executed helpers.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 original-outline collision regions, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) verifies a stronger floor-safe
16-gon for all cog angles against the actual fixed original outlines. Exact
subset checks and an independent triangle oracle verify all 100 obstacle caches;
all 43 source poses and 2,000 compatible pairs remain valid. A mixed-dimensional
GEOS guard failure is preserved; 1,262 completed queries are reused unchanged
and only 1,388 unfinished queries resume within the original work budget.
All 2,650 queries finish. Independent outward covers account for every whole
prior cell: 42,226 cells including 3,081 points/lines. They reject three prior
false anchors and exclude another 22 cases, leaving 207 cases/286 allocations.
Next construct fully covered convex domains and a joint model using the stronger
cog polygon itself. No solver call, accepted target layout or H5 qualification
is claimed. Source, accurate READMEs and releases stay unchanged; H2/H5 remain
open at 60% completed milestone weight.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)

if __name__=='__main__':main()
