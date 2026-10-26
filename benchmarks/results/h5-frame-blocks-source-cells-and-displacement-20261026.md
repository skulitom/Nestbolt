# H5: coordinated frames, source cells and a displacement obstruction — 2026-10-26

**A source-geometry certificate explains why small translations cannot repair
the mixed-frame candidate.** Four frames and one insert require 1,509.990 mm of
cross-section width on 1,487 mm usable stock. At least one of those five originals
must change orientation or move vertically by more than 180 mm. The proof does
not exclude the whole job. No complete layout has passed; H2/H5 stay open at
60% by completed gate weights.

## Coordinated frame choices

Instead of extending a closed local run, a new compound search changes 12–18
frame orientations and their starting positions together. All57 first originals
can translate jointly; all9 verified short originals stay fixed. Four source-valid
frame constructions are assigned to original identities by minimum squared
center displacement. Their frame modes remain fixed within that alternative;
legal modes for the other39 originals may change. Every initial frame pattern
passes153 source pairs and72 stock edges. The other39 positions start from the
saved previous candidate, with no claim that the complete initial layouts fit.

Each alternative receives at most20 positive weight updates and12 seconds,
within one60-second search/90-second shared call. All four close ITERATION_LIMIT.
Total search time is23.804778 seconds; shared time is26.417979 seconds.

| Frame construction | Frames turned | Search seconds | Source pair failures | Stock failures |
| --- | ---: | ---: | ---: | ---: |
| 12 turned, 6 wide | 12 | 7.114317 | 72 | 20 |
| Central notch:16 turned,2 wide | 16 | 5.162431 | 96 | 26 |
| Three tall columns | 18 | 7.692661 | 84 | 14 |
| Four turned columns:5/5/4/4 | 18 | 3.727039 | 106 | 28 |

Each independent reader reconstructs all66 original identities,90 cutouts and
10,026 hole vertices, checks1,632 source pairs and264 stock edges, and replays
all20 positive weight updates. No original or constraint is removed. Lower
penalties are not valid part counts or material savings. No native call qualifies.

## Simultaneous source-clearance constraints

A different feasibility method fixes the mixed candidate's source modes and
allows every first anchor to move within40 mm, intersected with stock bounds.
All1,596 pair domains are examined. For1,440 pairs the whole relative-position
box is safe. The other156 pairs use **571 convex collision-free cells** and
**2,056 exact integer halfplanes** from original-source configuration obstacles.
An additional0.002 mm obstacle expansion precedes micrometre rounding;23 rounded
cells fail conservative checks and are discarded. The smallest retained cell
distance to the already conservative obstacle is0.001355144 mm.

Independent checking reconstructs all114 coordinate domains, every pair box,
every cell's exact integer halfplanes and9,827 original-source clearance samples.
Full native/source acceptance remains mandatory for any eventual assignment.
This is a finite sufficient subset, not an exact enumeration of every legal
source pose in the neighborhood.

The serialized model has **685 variables and2,212 constraints**, with all57
first originals mandatory, no overlap objective,114 position hints and156
exactly-one cell choices. A separate reader reconstructs every serialized
constraint. The one60/90-second call closes **INFEASIBLE in presolve**:
0.021436 solver /0.026760 returned /1.184046 shared seconds, zero returned branches
and conflicts. No assignment is returned. The finite-cell result alone does
not exclude the whole translation neighborhood or the job.

Two initial geometry readers failed on an auxiliary distance-equality check.
The saved distance was computed before a polygon's vertex order was reversed;
the equivalent reversed polygon differs by at most1.129565191382298e-14 mm in
the library's diagnostic reduction. Both failed readers are retained. The final
reader exactly reproduces the saved value using either vertex order, while
independently requiring source containment, strict disjointness and positive
distance. No physical tolerance, geometry or model cell is changed.

## Independent source proof: more than180 mm or an orientation change

This proof does not rely on the solver or the cell approximation. Originals0–3
are frames turned90°; original31 is a vertical insert. Exact quarter-turn source
geometry contains four349.998 mm-wide rectangles and one109.998 mm-wide rectangle.
An independent rational reader verifies all80 corner/edge inclusion tests.
Filled outer areas remain reserved, as required with part-in-hole off.

Enclose each saved binary64 vertical anchor outward in micrometres. Permit any
vertical movement up to **180 mm** and relax stock containment to these inner
rectangles alone. Exact interval bounds prove **all10 vertical interval pairs
must intersect**; the smallest guaranteed overlap margin is22 micrometres.
Pairwise-intersecting intervals on a line share a common point, so in every
permitted placement all five rectangles cross one common horizontal line.
Their disjoint horizontal intervals then require **1,509.990 mm**, exceeding
the stock's **1,487 mm** by **22.990 mm**, even with zero clearance.

Horizontal positions are unrestricted within stock and the other61 originals
are not fixed. Therefore a valid source layout must change at least one of
these five modes or move at least one vertically by more than180 mm from this
candidate. This excludes a real source neighborhood, not just the finite cells.
It does not exclude other modes, large rearrangements or the entire target job.
The next hypothesis must explicitly relocate side inserts or restructure frame
rows beyond this obstruction; widening40 mm to another radius at most180 mm
cannot repair this fixed-mode candidate.

## Repository and evidence

Five independent audits pass. All four frame alternatives and the cell-model
call are CLOSED, without retry or extension. No native call, full quality run
or release is qualified. Production, READMEs, upstream heads/releases and all22
reserved H2 vectors remain unchanged.

At 2026-10-26T19:20:47.303575+00:00, [main f2322ccd checks](https://github.com/skulitom/Nestbolt/actions/runs/40381684665):
5 of six checks pass; the Windows check is still running. Preserve that job and wait for all six before the next push.

[Checks](h5-frame-blocks-source-cells-and-displacement-20261026/checks.json), [source certificate](h5-frame-blocks-source-cells-and-displacement-20261026/source-width-certificate.json),
[rational source audit](h5-frame-blocks-source-cells-and-displacement-20261026/source-width-certificate-checks.json),
[cell model audit](h5-frame-blocks-source-cells-and-displacement-20261026/source-cell-model-checks.json),
[scope](h5-frame-blocks-source-cells-and-displacement-20261026/scope.json), [next step](h5-frame-blocks-source-cells-and-displacement-20261026/next-step.json),
[raw manifest](h5-frame-blocks-source-cells-and-displacement-20261026/raw-manifest.json). The archive verifies
300 canonical files and48
aliases by bytes,SHA-256 and CRC.
