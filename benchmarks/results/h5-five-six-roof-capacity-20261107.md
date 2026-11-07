# Five- and six-turned upper-frame capacity — 2026-11-07

**Sixteen source-valid 44-part partial layouts cannot extend to all 66 parts.**
The stronger result also rules out their exact eighteen-frame/fourteen-cog
first-sheet cores when every other original part can move between sheets.
No whole allocation or orientation class is excluded. H2/H5 remain open at
**60% completed milestone weight**; the preserved valid 64-part layout remains best.

[Source construction](h5-five-six-roof-capacity-20261107/source-plan.json) retains twelve turned base
frames and the valid short sheet containing six brackets, five inserts and
one cog. The six upper frames use either five or six quarter-turns. Their
coordinates derive from original source dimensions, the declared gap and the
existing charged 6.75-degree cog phase and source axis pitch. No phase/pitch
sweep or saved optimized placement is used. Five turned frames yield fifteen
cog sites and fifteen choices of fourteen; six turned frames yield fourteen
sites and one choice.

[Independent source replay](h5-five-six-roof-capacity-20261107/source-audit.json) verifies all sixteen
44-part partials, **718 pool contacts, 8,992 same-sheet pairs and 896 original
holes** across cases. Minimum passing cog gap is **0.301548 mm**. Each partial
still needs six brackets and sixteen inserts; partial validity is not a full
job result.

Changed geometry requires [fresh necessary-center covers](h5-five-six-roof-capacity-20261107/cover-plan.json).
Only the independently audited local cog inner rectangles are reused; every
world obstacle and mask is rebuilt. Eight bracket modes and four insert modes
use full physical stock domains. Closed cover boxes include every boundary
point and open interval that avoids fixed-frame conflict and permits the
declared zero/one empty cog site. Two source rectangular components cover
each L-shaped bracket; one covers each insert. Their swept occupied regions
are clipped to outward stock bounds and have definitely occupied fixed
source interiors removed.

[Independent exact readback](h5-five-six-roof-capacity-20261107/cover-audit.json) verifies **2,269 source
inner rectangles, 20 component bounds, 24 fresh mode masks and 70,912,992
continuous classes**. Separate signed-corner prefix counts classify every
continuous class; a separate interval-event sweep checks **48 exact
union-difference areas**. Conservative source body-area rounding is bounded
by 0.049153 mm²; lower bounds use 39,999 mm² per bracket and 19,799 per insert.

| Upper turned frames | Exact cases | Combined occupied area at most (mm²) | Bracket capacity at most |
|---|---:|---:|---:|
| Five | 15 | 370,518.393503 | 5 |
| Six | 1 | 520,032.836202 | 0 |

The remaining six brackets and sixteen inserts require **556,778 mm²**.
[All sixteen fixed 44-part layouts are excluded](h5-five-six-roof-capacity-20261107/fixed44-capacities.json).

[A broader inventory relaxation](h5-five-six-roof-capacity-20261107/inventory-plan.json) keeps only the
exact eighteen frames and fourteen cogs on the first sheet, releases all
twelve brackets, twenty-one inserts and the last cog, then ignores that last
cog entirely. The existing independently verified material definition and
target bound the entire second sheet's usable area by **465,326.048858 mm²**;
three or more sheets exceed the material target. All brackets and inserts
still require at least **895,767 mm²**.

[Independent inventory readback](h5-five-six-roof-capacity-20261107/inventory-audit.json) finds that the
fifteen five-turned cores remain short by at least **59,922.557639 mm²** even
under this relaxation. The six-turned core permits no first-sheet bracket,
so all twelve must fit on the short sheet: their lower area exceeds that
sheet by **14,661.951142 mm²**. [Every exact first32 core is excluded](h5-five-six-roof-capacity-20261107/fixed32-capacities.json).
Changing only the companion inventory cannot rescue these geometries.

| Bounded stage | Complete preparation (s) | Separate audit (s) |
|---|---:|---:|
| Source partials | 0.895462 | 1.070807 |
| Fresh covers and component capacity | 10.078285 | 16.112959 |
| Released companion inventory | 0.173062 | 0.253429 |

The [source](h5-five-six-roof-capacity-20261107/roof-sources-process.json), [cover](h5-five-six-roof-capacity-20261107/roof-covers-process.json)
and [inventory](h5-five-six-roof-capacity-20261107/inventory-bound-process.json) preparations plus all
inherited work total **30.001913 s** if consumed by a successor. Their separate
[source](h5-five-six-roof-capacity-20261107/roof-sources-audit-process.json), [cover](h5-five-six-roof-capacity-20261107/roof-covers-audit-process.json)
and [inventory](h5-five-six-roof-capacity-20261107/inventory-bound-audit-process.json) audits pass. All six
Job Objects close three processes under unchanged 2 GiB, CCD1 and single-thread
controls. No optimizer, retry or extension is opened.

[Next](h5-five-six-roof-capacity-20261107/next-step.json), validate one-cog transfers for the earlier
one-turned and three-turned source pools. The latter's two collided pool pairs
must both be removed before source replay; no candidate validity is assumed.
Old masks may be reused only for exactly matching geometry and modes; missing
insert masks and changed-world obstacles must be rebuilt.

Four earlier fixed arrangements and 440 whole-job allocation candidates
remain. Full66 source/native/material acceptance, product integration,
UI/CLI/MCP parity and the original H5 matrix remain required.

[Main and the working branch reached 66192d0d](h5-five-six-roof-capacity-20261107/prior-main-push-receipt.json)
by ordinary atomic fast-forward after all six prior checks passed and 52
protected files were verified. [Fresh CI](h5-five-six-roof-capacity-20261107/main-ci-at-review.json) records
**4 passed / 2 live jobs**. This checkpoint awaits the next
ordinary push gate. Product code, README and releases remain unchanged.

[Archive checks](h5-five-six-roof-capacity-20261107/archive-checks.json), [manifest](h5-five-six-roof-capacity-20261107/raw-manifest.json),
[source bindings](h5-five-six-roof-capacity-20261107/source-bindings.json), [historical references](h5-five-six-roof-capacity-20261107/external-evidence.json)
and [runtime pins](h5-five-six-roof-capacity-20261107/runtime-bindings.json) preserve all evidence.
