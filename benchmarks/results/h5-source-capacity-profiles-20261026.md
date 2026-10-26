# H5: exact source capacity profiles — 2026-10-26

**The smaller staged model preserves the source-strip capacity information,
but returns UNKNOWN without a candidate.** Its first and only solve returns in
30.043256 seconds; the pipeline closes after 32.950780 shared seconds. H2/H5
remain open at 60% by completed gate weights.

## Exact capacity with fewer intervals

The previous geometry audit verified 781 disjoint source-contained rectangles,
including 728 cog strips. Their cumulative height and width demands can be
represented independently of the expensive additional 781-rectangle NoOverlap2D.
For every original and axis, the preparation sweeps all integer rectangle
endpoints, sums perpendicular demand and merges adjacent equal-demand slabs.

The resulting piecewise profiles contain 1,498 X intervals and 437 Y intervals.
Splitting overlapping X intervals increases that representation's size, so the
model retains the original 781 X intervals and uses the compact 437 Y profile
intervals: **1,218 instead of 1,562 projection intervals**. Both representations
measure exactly the same occupied source-strip capacity for arbitrary whole-part
translations. They do not replace two-dimensional collision checking.

An independent reader checks all 114 original/axis profiles through **2,315
integer event slabs**, with direct active-rectangle summation rather than the
producer's sweep. It also checks all 114 integrated source areas and interval
merging. The source rings and strip containment are unchanged.

## A different staged model

The new initial model has **114 whole-stock coordinates and 1,400 constraints**.
It keeps the older 65-rectangle non-overlap, its two cumulative constraints and
47 equivalent-copy orders, then adds the 1,218 exact strip intervals and two
capacity constraints. All 57 first-sheet originals remain mandatory, together
with the verified short nine. Ninety non-cog hints fix no coordinate.

The additional global strip non-overlap and all initial detailed source-cell
selectors are absent. After a returned candidate, the pipeline would inspect
all 66 original rings and add complete cell disjunctions for every newly failing
first-sheet pair. Each later round must change the constraints. The declared
limits are four rounds, 30 seconds for the first solve and eight for later
solves, all within 60 algorithm/90 shared seconds. UNKNOWN stops immediately.

An independent protobuf reader checks every initial and round-zero constraint,
both profile representations, all hints and unchanged whole-stock domains. The
model SHA-256 is `8bc5e5e3bfb19b669821c12ade47c31e7ad621857041e76e0916781e487076f6`.

## Closed result and timing

Only round zero runs. It returns **UNKNOWN**, with **155,233 branches and
22,875 conflicts**, no assignment, no source candidate and no new source cut.
The `fj` worker that overran the previous different model is explicitly excluded;
the serialized parameters and log confirm this, with `fs_random_no_lp` as the
first-solution worker. This does not establish a universal timing guarantee.

Solver time is **30.041647 seconds**, returned solve **30.043256**, algorithm
**32.720068** and shared process **32.950780**. The 0.041647/0.043256 second soft
overruns are recorded. The total algorithm and process boundaries are met. The
call remains CLOSED without extension, reseeding or unchanged-model retry.

The profile audit and complete serialized-model/response audit pass. No native
validation, full quality run, source-fit claim or unrestricted exclusion occurs.
The next distinct investigation can vary the short-sheet allocation across the
already proved surviving count frontier, instead of preserving the same fixed
nine-part short sheet and fixed source modes. That investigation has not opened
a search here and must keep every original and the target material boundary.

## Repository and evidence

The preceding three checkpoints were pushed normally as ff5036af at
2026-10-26T20:14:53.105642+00:00, after all six db4d2309 checks passed; remote main was verified.
At 2026-10-26T20:22:54.462245+00:00, [ff5036af checks](https://github.com/skulitom/Nestbolt/actions/runs/40393931732):
3 of six checks pass. Preserve the remaining live checks before the next push. Production, READMEs and upstream heads/releases remain unchanged.
All 22 reserved H2 vectors are unopened, and no new release is qualified.

[Checks](h5-source-capacity-profiles-20261026/checks.json), [profile audit](h5-source-capacity-profiles-20261026/profile-checks.json),
[initial model](h5-source-capacity-profiles-20261026/initial-model-checks.json), [response](h5-source-capacity-profiles-20261026/response-checks.json),
[scope](h5-source-capacity-profiles-20261026/scope.json), [next step](h5-source-capacity-profiles-20261026/next-step.json) and
[raw manifest](h5-source-capacity-profiles-20261026/raw-manifest.json). The archive verifies
62 canonical files and 26
identical-content aliases by bytes, SHA-256 and CRC.
