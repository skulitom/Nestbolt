# H5: fixed-nine exclusions and an all-movable short-sheet preflight

Date: 2026-10-29. Evidence and documentation only. H2/H5 remain open at
60% completed milestone weight; no new release qualifies.

## Result

The 5-bracket/6-insert/2-cog short-sheet allocation cannot retain nine of the
twelve exact parent poses. All **200 distinct fixed-nine geometries and 330
identity variants** are excluded by independently audited necessary bounds.
At least four parent poses must change. This does not exclude the allocation,
other parent arrangements or the original 66-part job.

The next preparation lets **all thirteen short-sheet originals move**. Its
source geometry, exact no-fit formulas and rounding argument pass independent
audit. No solver model or search has been opened. No new original-source
13-part layout, first-sheet 53-part placement or complete 66-part layout is
claimed. The existing valid 64-part layout and 444 necessary allocation
survivors remain unchanged.

## Fixed-nine inventory

Starting from the [fixed-ten exclusion](h5-fixed-ten-joint-cog-bound-20261029.md),
each new variant sends one parent bracket to the first sheet and releases
two further originals. Both released originals remain mandatory short-sheet
movers alongside the new cog and insert. Deduplication yields 200 geometries
from 330 identity variants; all 66 original identities are accounted for
exactly once in every variant.

All 200 fixed-nine layouts pass source readback, including 7,200 independent
pair checks. The angle-independent stock bound and filled-source cog core
exclude 144 geometries / 244 variants. The audit verifies 119 unique no-fit
polygons, all 18,325 uses of them, 2,699 certificate nodes, 1,366 covered leaves
and 196,704 leaf-corner half-plane checks. It verifies each of the remaining
56 necessary core witnesses without treating them as source placements.
Preparation takes 9.277091 s and audit 6.319209 s.
See the [inventory audit](h5-fixed-nine-triple-and-global-short-preflight-20261029/inventory-audit.json).

## Required pairs and triples

The 56 survivors require 253 cog/cog or cog/bracket pair tests. Complete
coverage closes 205 pair cases; 28 have exact relaxation witnesses and
20 stop at the frozen depth-40 cap. All partial cases remain preserved and
unexcluded by that individual test. Where another required pair has a
complete exclusion, that separate proof can still close the geometry.

Independent reconstruction verifies all 36,371 obstacle uses, 20,195 nodes,
9,753 covered leaves and 3,694,400 exact leaf-vertex half-plane checks. This
closes 51 additional geometries / 72 variants, leaving five geometries and
fourteen identity variants. Pair construction takes 15.147907 s and audit
7.741981 s. See the [pair audit](h5-fixed-nine-triple-and-global-short-preflight-20261029/pair-bound-audit.json).

Four remaining geometries need a cog and two brackets; the fifth needs two
cogs and a bracket. The triple proof includes every remaining legal bracket
mode, including modes with depth-limited pair results, and all ordered
bracket-mode combinations. Both cog rotations remain arbitrary real values.
No separate pair witness is assumed to work with another pair's witness.

All fifteen six-variable domains are completely covered. Every exact child
partition and all 64 actual vertices of every leaf are checked independently:
6,049 nodes, 3,032 covered leaves and 4,561,920 integer-scaled rational
half-plane checks. Two source-valid positive triple controls cover both mover
arrangements; coincident cog centers fail the negative control. Construction
takes 4.457018 s and audit 2.048409 s, within the frozen 120-second proof cap.
No triple case reaches a depth, node or time limit.

The [triple audit](h5-fixed-nine-triple-and-global-short-preflight-20261029/triple-bound-audit.json) and
[necessity argument](h5-fixed-nine-triple-and-global-short-preflight-20261029/necessity-proof.json) close the final five
geometries, yielding the stated exclusion of all 200 layouts / 330 variants.
These studies make **zero construction, solver or native calls**.

## New global short-sheet preparation

The new necessary model retains the original target stock and all 66
identities, with 13 independent short-sheet anchors and 53 explicit
first-sheet requirements. All eight bracket rotation/mirror modes and all
four insert quarter rotations are retained. Cog rotation remains unrestricted
in the necessary geometry, using the previously proved filled-source core
for collisions and the larger convex-hull disk only for stock.

The five brackets and six inserts supply sixteen mandatory orthogonal core
pieces. A global rectangle non-overlap constraint can handle those pieces.
Thirty-two cog/rectangle predicates each use 36 complete symbolic facet
directions; one cog/cog predicate uses 32. Variable rectangle supports avoid
duplicating every pair of orientation choices. All twenty mode rectangles
are proved strictly source-contained with 112 exact source-edge checks.
Independent convex-hull reconstruction proves every symbolic facet formula.

The [rounding argument](h5-fixed-nine-triple-and-global-short-preflight-20261029/global-rounding-proof.json) maps any legal
continuous source placement into this proposed integer relaxation: rounding
an anchor to micrometres moves a part by less than 0.708 micrometres, and two
parts by less than 1.416 micrometres relative to each other. The original gap
exceeds 211 micrometres. Stock bounds are expanded enough to contain this
rounding. Therefore a legal source layout cannot be lost by the proposed
integer core model. A core-model assignment does not establish the reverse.

A positive 11-part source control has no core violations; only cog 0 and
insert 0 are missing from the required 13. The full negative control has
78 original-source pair failures, 95 orthogonal-core collisions, 32
cog/rectangle failures and one cog/cog failure, with valid stock bounds.
Expected identity arguments are normalized to tuples. The
[independent preflight audit](h5-fixed-nine-triple-and-global-short-preflight-20261029/global-preflight-audit.json) checks both
controls, all legal modes, all identities and the rounding proof.

Next, build and audit the saved protobuf model and its source-to-core
mapping before the sole declared 60/90-second call. Any feasible relaxation
still requires original cog-angle/contour realization and a complete
first-sheet placement before a 66-part native check. No CP model, new search,
production change or H5 completion exists at this checkpoint.

## Publication

Main remains `6b0a1d0b`; checkpoint `1d545cac` is already queued locally.
At the fresh [CI 40789500705 snapshot](https://github.com/skulitom/Nestbolt/actions/runs/40789500705),
five jobs have passed and the Windows check is running. Both queued
checkpoints wait for that final check before a normal push.
Production, all three READMEs, upstream heads/releases and Nestbolt's
`v0.1.0` stable / `v0.2.0-alpha.1` preview releases remain unchanged.
H2 retains its original gate and 22 unopened vector files.

The [manifest](h5-fixed-nine-triple-and-global-short-preflight-20261029/raw-manifest.json) preserves 3294 canonical members,
2008 identical-content aliases and 14385541 compressed bytes, including
the complete inventory, depth-limited results, coverage certificates,
source controls, global preflight, scripts and recursive input bindings.
