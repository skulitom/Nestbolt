# H5: exact cog coverage and a two-insert short sheet — 2026-10-26

**An exact continuous coverage proof shows that no additional cog fits while
the former first-sheet 55 placements stay fixed. A revised allocation stacks
both inserts on the short sheet and restores a first-sheet cog, producing a
verified 64-part partial. Two cogs still require a first-sheet rearrangement.
H2/H5 remain open at 60%; there is no complete target witness.**

## A diagnostic screen, then an exact proof

First compute a diagnostic center map using a 109.10 mm moving disk against
all 55 original filled outers, zero pair clearance and stock relaxed outward
by 0.020 mm. The disk lies inside every original cog. All-angle stock support
of 139.270 mm bounds the center domain. The floating map is empty, but that
result alone is not accepted as a formal exclusion.

The independent certificate covers the entire continuous rectangle
**[145.750, 1354.250] × [145.750, 2854.250] mm** with **242 leaf rectangles**
in a **483-node binary partition**. Each leaf's four corners are strictly
inside one conservative collision disk. Convexity then covers its whole
continuous interior and boundary; every split is checked exactly, with no gaps.

The construction seeds 7,403 collision disks and uses **222** in the final
cover. A 109.10 mm disk is centered near an exact point of a fixed original
filled outer; a 218.20 mm disk is centered near a fixed cog's inscribed-disk
center. The moving cog has an independently certified 109.115 mm inscribed
radius. Fixed cogs have the same radius. Thus the reserved radius losses are
0.015 mm and 0.030 mm, respectively.

The auditor uses exact rational winding/boundary tests for source-point
membership. For each of three stored rotation angles it bounds sine and
cosine by a Taylor polynomial through degree 59, with rigorous remainder
|angle|^60 / 60!. It propagates these intervals through the source transform
and proves the rounded center error fits the reserved radius loss. Exact
integer squared-distance checks certify every leaf corner; the smallest
strict squared margin is **51,526,014 square micrometres**.

No floating polygon buffer, sampled cog angle, finite center grid, or solver
timeout establishes this negative. It covers every real cog angle and every
continuous center within the relaxed stock domain. Filled outers are the
occupied geometry because part-in-hole is disabled. Moving any fixed original
changes the problem and is not excluded by this certificate.

## Revised 64-part allocation

Move insert **36** from the first sheet to the short sheet, stacked above
insert **37** with a 0.225 mm gap. Restore cog **53** at its earlier verified
first-sheet pose, and replace the identical short-sheet cog copy with **65**.
The other **54 first-sheet placements** remain exactly unchanged.

The short sheet now contains **nine originals**: six brackets
**21/22/25/26/28/29**, inserts **36/37**, and cog **65**. The old eight-part
bound concerned a different first-sheet allocation and is not transferred.
The new partial places **64 originals**, with cogs **63/64** explicitly
required on the first sheet. All 66 identities are accounted for exactly once.

All **1,521 same-sheet original filled-outer pairs and 256 stock edges** pass.
The **88 cutouts and 9,626 cutout vertices** are preserved. Minimum pair
distance is 0.212500 mm against the required native guarded distance of
0.211708673 mm; minimum extra stock margin is 0.012500 mm. A separate auditor
directly transforms every original vertex, checks allowed rotations/mirrors,
cutout coordinates and areas, and repeats the pair and stock checks.

The new fixed55 still cannot accept an extra cog. Four exact corner checks
prove the removed insert's whole rectangular outer lies inside the restored
cog53 inscribed disk. The new fixed filled union therefore contains the old
one, so the exact collision cover transfers. The remaining two cogs require
moving first-sheet originals; a complete native job is not run on this partial.

## The next rearrangement retains all originals

Release all **12 existing first-sheet cogs**, retaining **43 non-cog first
originals** and the **nine short-sheet originals**. Together with the two
unplaced cogs, all **14 first-sheet cogs** are mandatory movers with their
original free-rotation/no-mirror rules. The 12 saved poses are diagnostic seeds,
not locks or a completeness claim. The inventory independently accounts for
all 66 originals exactly once.

The disk-only screen for those 43 fixed originals has one component of area
**474,313.726959 mm²**, bounded by X=370.125555–1354.250 mm and
Y=2216.737600–2784.387400 mm. A preceding 44-fixed diagnostic map had area
429,417.482877 mm². All three maps and **142 fixed obstacles** are replayed,
but the maps remain screening data, not original-cog feasible regions or
exact exclusions. Original-support constraints and complete domain audits
should precede a new bounded search. A positive necessary placement still
needs actual cog angles and every original mutual clearance.

This checkpoint makes **zero solver calls** and does not reopen any closed
call. Full66 native/material validation, production integration within 60
seconds and the complete H5 matrix remain required.

## Repository and evidence

At **2026-10-26T11:03:19.182699+00:00**, local HEAD **2274a7a1** is queued above main **9842e4c1**.
All six jobs in [CI40305808059](https://github.com/skulitom/Nestbolt/actions/runs/40305808059)
have passed, permitting a normal push of both checkpoints after staged-byte
and ancestry checks. Production and README digests, upstream stop-rule state
and the 22 reserved H2 vectors remain unchanged. H2 retains its original gate;
no new release is qualified.

All **five audits pass**. [Checks](h5-exact-cog-coverage-and-two-insert-strip-20261026/checks.json),
[exact exclusion](h5-exact-cog-coverage-and-two-insert-strip-20261026/exact-fixed55-exclusion.json),
[partial64](h5-exact-cog-coverage-and-two-insert-strip-20261026/partial64-placements.json),
[next inventory](h5-exact-cog-coverage-and-two-insert-strip-20261026/released-cog-neighborhood.json),
[scope](h5-exact-cog-coverage-and-two-insert-strip-20261026/scope.json), [next step](h5-exact-cog-coverage-and-two-insert-strip-20261026/next-step.json),
[raw manifest](h5-exact-cog-coverage-and-two-insert-strip-20261026/raw-manifest.json). The archive verifies
84 canonical files and 58
aliases by bytes, SHA-256 and CRC.
