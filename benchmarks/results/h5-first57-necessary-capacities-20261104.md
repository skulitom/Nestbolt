# First57: continuous necessary domains and capacity bounds — 2026-11-04

Exact source-based capacity proofs exclude **196 of the 455 twelve-cog site
selections**, leaving **259** for the current first57 construction. This result
is conditional on the fixed 29 frame/insert placements and the existing 15 cog
poses. It excludes **no whole-job allocation**. All 440 allocation candidates
remain, and H2/H5 stay open at **60% completed milestone weight**.

The [preceding checkpoint](h5-direct-short9-and-grouped-first57-20261104.md)
preserves a source-valid direct short sheet with four brackets, two inserts
and three cogs. Its matching first57 needs eight brackets and eight additional
inserts around the fixed core and twelve selected cogs. That grouped model's
sole call remains closed UNKNOWN; this checkpoint makes no solver or native call.

## A necessary domain from original source bodies

[Independent exact containment checks](h5-first57-necessary-capacities-20261104/source-containment-audit.json)
verify 75 rectangles inside the original cog's convex pieces, their 1,125
translated copies at all 15 sites, 29 fixed-core rectangles, and 20 moving
rectangles across all 12 legal bracket/insert modes. All comparisons use exact
rational representations of the original transforms and inward-rounded integer
micrometre rectangles.

The resulting ten unique geometries use the **full physical first-sheet stock**,
with outward-rounded anchor bounds. They deliberately allow zero clearance.
The fixed frame holes are filled because common-line part-in-hole remains off.
For a moving inner rectangle, overlap with a fixed inner rectangle defines an
open forbidden rectangle in anchor space. These are necessary collision
conditions: ignoring the rest of each source body and the required gap enlarges
the possible domain.

[The exhaustive cover audit](h5-first57-necessary-capacities-20261104/continuous-cover-audit.json) independently
replays **160 site-bit fields** using two-dimensional event counts. Every
obstacle boundary splits each axis into point and open-interval classes, so
the classification is continuous and includes isolated boundary possibilities.
All **23,278,076 classes** are verified. Of these, **9,456,254** have no fixed-core
collision and require at most three cog sites to be empty. They are covered
exactly once by **3,275 closed boxes** across **548 geometry/mask combinations**.
Closing interval endpoints only enlarges the cover.

These boxes supply necessary domains for negative capacity proofs. The earlier
conservative source-safe construction regions did not establish this coverage.

## Exact area capacities

For each of the 455 empty-site triples, the first method sweeps each source
inner bracket rectangle over every eligible anchor box. The union of these
sweeps, minus all fixed source-contained obstacles, contains every possible
inner bracket body. Eight disjoint brackets require at least eight times the
smallest inner-body area across all modes.

The preparer uses GEOS to obtain candidate areas.
[A separate integer event/tree audit](h5-first57-necessary-capacities-20261104/global-area-audit.json), using no
geometry library or floating-point arithmetic, recomputes **every bracket
area for all 455 choices**. It certifies **139 exclusions**, leaving 316.
Insert and combined-area calculations are preserved as diagnostics; they are
not used as negative certificates.

The second method enumerates all 455 choices directly from the necessary
cover. It assigns every eligible anchor box, carrying both of its bracket
components, to one reachable-area group. Each group's floored area capacity
bounds the number of brackets assigned there. The capacities can be summed
even if groups overlap, because each bracket is assigned to exactly one group.

[Independent exact readback](h5-first57-necessary-capacities-20261104/component-area-audit.json) verifies
**1,156 group areas** and all **23,906 anchor-box assignments**, with no missing
or duplicated box. It certifies **196 exclusions in total**, including the
139 global-area exclusions, leaving **259 choices**. The surviving choices
and their component capacities are saved in the
[retained frontier](h5-first57-necessary-capacities-20261104/retained-choices.json).

| Certified bracket capacity | Site choices |
| --- | ---: |
| 3 | 2 |
| 4 | 12 |
| 5 | 38 |
| 6 | 41 |
| 7 | 103 |
| 8 | 114 |
| 9 | 59 |
| 10 | 57 |
| 11 | 27 |
| 12 | 2 |

Capacities below eight exclude the fixed construction. Larger values are
upper bounds, not placements or feasibility claims.

## Timings and remaining work

All four preparation processes were bounded before execution. Each completed
within its declared process cap, with no retry or overrun:

| Stage | Complete preparation process | Independent audit |
| --- | ---: | ---: |
| Source-contained rectangles | 2.778012 s | 2.974393 s |
| Continuous mask cover | 2.211135 s | 3.355394 s |
| Global reachable area | 13.678731 s | 7.870842 s |
| Direct component capacities | 14.375178 s | 4.492115 s |

[Process records](h5-first57-necessary-capacities-20261104/preparation-processes.json) retain the complete
wall-clock timings, internal timings, declared caps and outputs. The direct
component method does not consume the prior global-area results. These are
preparation and verification measurements; **no new complete construction
budget or search result is claimed**. A future construction must charge every
preparation it actually uses, including source geometry, short9 and model work,
under the original 60/90-second limits.

The [next step](h5-first57-necessary-capacities-20261104/next-step.json) is to derive stronger source-based
capacity or spatial constraints from the remaining component domains, or a
meaningfully smaller constructive model. The retained 259 choices do not
justify restarting the closed 35,735-variable model. All prior closed calls
remain closed.

The older fixed13-cog frontier remains two site choices / three count
distributions. A full66 layout still needs original-source checks before native
validation, then material validation, integration and the H5 matrix. H2 retains
its original gate and the 22 reserved vectors remain unopened. This checkpoint
does not qualify a new release.

At sealing, [main CI 41908888838](https://github.com/skulitom/Nestbolt/actions/runs/41908888838)
has five successful jobs and the Windows checks job still running. Local
checkpoint 67cbbdc2 and this evidence wait for all six jobs and the aggregate
run to pass before a normal atomic push to main and the working branch.

The [raw manifest](h5-first57-necessary-capacities-20261104/raw-manifest.json) contains 1007 new canonical
members and 1,145,377 compressed bytes.
[External references](h5-first57-necessary-capacities-20261104/external-evidence.json) and
[source bindings](h5-first57-necessary-capacities-20261104/source-bindings.json) preserve exact historical
inputs. An independent archive reader checks every new and reused member,
all source bindings and local report links before commit.
