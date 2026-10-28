# H5: short-sheet exchange regions and continuous cog exclusion

Date: 2026-10-28. Evidence and documentation only. H2 and H5 remain open;
completed milestone weight is 60%. No new release qualifies.

## Result and scope

All six proposed fixed 11-part short-sheet layouts exclude another original
cog at **every real rotation and continuous center**, independently of the
extra insert. This exact necessary bound closes these particular layouts.
It does not exclude the 5-bracket/6-insert/2-cog allocation, other fixed poses,
or the original 66-part job. More existing poses must move to pursue this
allocation. The 444 necessary allocation survivors and the valid 64-part
layout remain unchanged.

The [previous inventory](h5-fixed-cog-rows-and-short-exchange-20261028.md)
removed bracket copy 3, 4, 7, 8, 10 or 11 from the same valid 12-part parent.
Each case retains eleven exact source poses and proposes cog copy 0 and insert
copy 0. Its target short sheet contains 5 brackets, 6 inserts and 2 cogs;
the first sheet must still contain all 18 frames, 7 brackets, 15 inserts and
13 cogs. All 66 identities are accounted for exactly once. No new 13-part
short sheet or complete 66-part layout was produced.

## Complete finite geometry audit

Fresh original-source construction prepared 262 no-fit obstacles from
264,312 convex Minkowski hulls: 190 fixed-type/moving-mode combinations and
72 cog/insert combinations. Preparation took 13.906852 seconds, within its
frozen 120-second limit. The six cases have 228 complete free domains across
36 declared cog modes and two insert modes. All **216 cog domains are empty**;
four insert domains have independently valid 12-part source controls.

The first validator retained all 262 obstacle checks but wrote no final
result. Its process exit code was unavailable after recovery. Inspection
identified a tuple-versus-list mismatch in the final sample comparison.
The original script and incomplete evidence remain preserved. A separate
validator normalizes that representation, leaves the geometry unchanged,
and rechecks every obstacle, free domain and identity partition. It passes
in 13.561847 seconds, including all four source controls.
See the [corrected audit](h5-short-exchange-continuous-bound-20261028/geometry-audit.json) and
[retained incomplete audit](h5-short-exchange-continuous-bound-20261028/retained-incomplete-audit.json).

The [finite construction closes at preflight](h5-short-exchange-continuous-bound-20261028/finite-construction-closure.json)
with zero anchors and **zero construction, solver or native calls**. Its
unused time is not reused and it is not retried. Empty conservative domains
alone make no all-angle or original-feasibility claim.

## Independent necessary bound at every angle

An exact source-centered disk contains a 32-vertex integer polygon with
nominal radius 109.113 mm. Exact rational point-to-segment distances prove
every vertex lies strictly inside the original filled cog. The disk is
rotation invariant, so this same world-aligned polygon lies inside the cog
at every real rotation, centered at the transformed original center.
Common-line PIH remains off; the filled outer reserves its holes.

The parent twelve parts supply 119 strictly source-contained rectangles.
Each fixed eleven-part case supplies 117. Independent rational corner
parity and clipping perform 476 corner checks and 8,252 source-edge checks.
Every rectangle is inside its actual fixed source outline; no obstacle
from a different pose is reused. Exact vertex differences form convex
necessary no-fit polygons without adding clearance. Any contact between
these contained shapes violates the original positive source gap.

Outward-rounded stock bounds contain every possible source-valid cog
center. Each of the six certificates partitions the entire continuous
center rectangle into eight covered leaves using fifteen tree nodes.
The audit verifies all 90 nodes, 48 leaves, 89,856 vertex sums and 6,912
leaf-corner half-plane checks with exact integers or rational numbers.
Every child pair exactly partitions its parent; every leaf lies completely
inside one convex forbidden polygon. There is no coordinate-grid or
sampled-angle assumption. All cases finish below the frozen 100,000-node
and depth-30 caps.

The original parent cog is a positive control against the other eleven
parent parts, and its occupied center is a negative control against itself.
Both checks pass. The [independent audit](h5-short-exchange-continuous-bound-20261028/bound-audit.json),
[six case results](h5-short-exchange-continuous-bound-20261028/bound-cases.json) and
[necessity proof](h5-short-exchange-continuous-bound-20261028/necessity-proof.json) record the precise scope.
The proof construction took 0.375918 seconds; its audit took 1.293972 seconds.

## Publication and next step

All six jobs for main `83f3f51f` passed in
[CI 40783629977](https://github.com/skulitom/Nestbolt/actions/runs/40783629977).
The prior queued checkpoint and this checkpoint are ready for a guarded
normal fast-forward push after commit. Fresh upstream heads and release
reads match the previous checkpoint. Production and all three READMEs are
unchanged; stable remains `v0.1.0`, preview remains `v0.2.0-alpha.1`.
H2 retains its original gate and 22 unopened vector files.

Next, prepare a separate inventory that releases one more original from
each fixed eleven-part case. Deduplicate equivalent geometry while retaining
the identity variants, and apply the necessary cog-core preflight before
choosing a new bounded construction. An uncovered core center would only
leave a relaxation open; it would not certify a full source placement.
This next geometry and search have not started.

The [manifest](h5-short-exchange-continuous-bound-20261028/raw-manifest.json) contains 1404 canonical members,
991 identical-content aliases and 5568894 compressed bytes. Recursive
input bindings, scripts, unchanged original inputs, the incomplete validator,
both successful audits, certificates and publication snapshots are retained.
The [checkpoint checks](h5-short-exchange-continuous-bound-20261028/checks.json) report no H5 completion claim.
