# H5: original-outline collision regions — 2026-10-25

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
in **0.594856 seconds**, with nothing pending. Each raw
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
auditing takes **1.002896 seconds**. This diagnoses selected anchors,
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
The observed plan-to-failure interval is **9.849457
seconds**. Recovery conservatively charges 60 seconds to that phase and allows
only the remaining 60 seconds of the original 120-second limit.

Recovery omits that faulty reverse-subset guard; the actual subtraction is
unchanged. Every completed result is reused byte for byte, and only the
**1,388 unfinished queries** are computed. The recovered phase, including
verification of reused outputs, takes **13.915806 seconds**.
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
independent audit takes **20.510757 seconds**. Nonempty regions do not
show that the four movable parts fit together.

## Next work and repository state

Use only the independently certified outward covers from the recovered region audit as the next domain source. All100 original-fixed collision caches and all2650 eligible mode queries are complete; do not rerun their construction. Preserve the initial mixed-dimensional GEOS guard failure and1262 byte-identical reused outputs. Next declare a bounded convex-domain construction over all207 surviving cases and286 allocations: cover every polygon component of the padded regions, preserve every boundary/point through outward rounding, and independently verify full coverage and integer halfplanes. Then consider one separately declared bounded four-part joint model with all66 counts. Use the new floor-safe16-gon itself for moving cogs and exact coupled rectangle components for brackets/frames. Cross-part separation must include all edge normals of their convex-component Minkowski sums, with independently audited integer projection bounds; do not fall back to the weaker five-rectangle cog collision check alone. Keep all allowed source orientations and sheet allocations, full original-area charges and the target material limit. Any positive still requires actual cog angles/outlines, original clearance/native guards, production budget and all13 jobs/two kerfs. No unchanged search retry, gate reduction, reserved-vector access or new release. Poll existing main CI40233299884 and push accumulated commits normally after it is terminal.

Production source, all three accurate READMEs and release versions are unchanged.
The captured existing main CI40233299884 at 247e823a remains `in_progress` /
`pending`. Five checks have passed and Windows remains
live in that snapshot; it is not restarted or called successful. This checkpoint
starts at 6cb2227c. No native packing, quality matrix, held-out access or new
release occurs.

Evidence: [geometry plan](h5-original-outline-collision-regions-20261025/geometry-plan.json),
[geometry audit](h5-original-outline-collision-regions-20261025/geometry-audit-checks.json), [floor certificate](h5-original-outline-collision-regions-20261025/geometry-cog-floor-certificate.json),
[region plan](h5-original-outline-collision-regions-20261025/regions-plan.json), [region result](h5-original-outline-collision-regions-20261025/regions-result.json),
[whole-cell audit](h5-original-outline-collision-regions-20261025/regions-audit-checks.json), [surviving cases](h5-original-outline-collision-regions-20261025/regions-audit-surviving-neighborhoods.json),
[source review](h5-original-outline-collision-regions-20261025/source-review.json), [raw archive](h5-original-outline-collision-regions-20261025/raw-001.zip)
and [manifest](h5-original-outline-collision-regions-20261025/raw-manifest.json). All **5685**
canonical members and **1290** identical-content aliases
retain exact bytes with CRC/SHA-256 checks, including the original failure,
every raw obstacle/query, all certified covers, sources and executed helpers.
