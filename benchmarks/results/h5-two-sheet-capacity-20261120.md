# Whole-sheet capacity on the 66-part common-line job

**418 allocations remain possible under these tests.** The previously reported
440 came from the short sheet alone. Four of those had already been ruled out
by the area of their complementary first sheet. Two new tests exclude another
18 allocations on the short sheet. These exclusions apply to every placement
and permitted rotation of the 66 parts for the laser large-plate target.
The best validated layout within that material target contains 64 of 66 parts.

| Check | Allocations entering | Excluded | Remaining |
| --- | ---: | ---: | ---: |
| Original occupied outer area on both sheets | 440 | 4 previously known | 436 |
| Bracket, insert and inscribed cog sections on the short sheet | 436 | 8 | 428 |
| Full cog area and width on the short sheet | 428 | 10 | 418 |

The frozen job has 18 frames, 12 brackets, 21 inserts and 15 cogs. The
first sheet has 1,487 × 2,987 mm of usable stock. The short sheet is 1,487 mm
wide and slightly under 313 mm high. Both dimensions come from the original
+1% [material target](h5-six-unturned-frame-construction-20261107/benchmark-target.json).
All 90 holes remain reserved in common-line mode.

The [October short-sheet frontier](h5-short12-exclusion-and-seven-part-readback-20261029/updated-allocations.json)
still included short-sheet counts of (0,0,0), (0,1,0), (0,2,0) and (1,0,0),
in bracket, insert, cog order. Recomputing occupied area from the original
outer rings confirms that the remaining parts exceed the first sheet's
4,441,669 mm² for each of those counts. An [earlier coupled calculation](h5-coupled-allocation-model-20261026/source-area-excluded-count-vectors.json)
had already recorded exactly these four exclusions.

## Why a vertical section rules out an allocation

At any horizontal position the combined height of the occupied material must
fit within the sheet. Give each possible bracket or insert section height an
integer weight. Enumerating all combinations that fit vertically gives an
upper bound on the total weight at that position. Integrating across the sheet
gives the available capacity. Each part must use at least the smaller of the
weights integrated over its legal orientations. A strict deficit excludes the
allocation even when all parts can move.

The [first screen](h5-two-sheet-capacity-20261120/results.json) includes
conservative strips from a 109 mm radius disk inside every cog. All eight
exclusions at this stage are allocations with zero cogs on the short sheet.
The [second screen](h5-two-sheet-capacity-20261120/cog-results.json) uses the
entire cog outline. Its occupied area exceeds 50,062 mm² and its horizontal
extent is at most 282 mm at every angle. A cog's weight at a section is its
occupied height times a nonnegative slope, less a fixed charge while it crosses
that section. Integrating gives a lower bound from its area and maximum width.
The audit checks all possible counts from zero through fifteen simultaneous
cog sections. Ten allocations that include one or more cogs exceed capacity.

Floating-point linear programs suggest weights. The [independent verifier](h5-two-sheet-capacity-20261120/verify.py)
uses exact rational source coordinates and integer arithmetic. It rebuilds the
section widths for every rotation and mirror, verifies the cog's inner and
outer disks, and checks every allocation. From the repository root run

```sh
cd benchmarks/results/h5-two-sheet-capacity-20261120
python verify.py results.json cog-results.json
```

The initial preflight rejected its own disk test before producing a result. It
used distances to infinite edge lines. The correction checks distances to the
actual line segments and verifies that the disk center lies inside the original
outline. The [process receipts](h5-two-sheet-capacity-20261120/stages.json)
preserve that failure and both successful independent audits. These calculations
produced no new layouts. The [measured common-line comparison](h5-cutting-development-20261015.md)
still determines H5.

A [complementary first-sheet calculation](h5-two-sheet-capacity-20261120/first-sheet-recheck.zip)
tested the four remaining allocations with the heaviest first-sheet inventories
under componentwise ordering. Horizontal and vertical section weights used the
same frame, bracket and insert orientations. All four searches produced the
same integer weights, which exclude zero additional allocations.
The [two-axis short-sheet check](h5-two-sheet-capacity-20261120/short-sheet-recheck.zip)
also excludes zero after testing all 33 maximal remaining short-sheet inventories.

## Complete archived layouts

The current CLI validated and exported the complete layout with the least
material in each of the four mechanical job and kerf combinations below. Each
target is 101% of the original three-seed ordinary-mode median for that
combination. Percentages in the last column use the target as the denominator.

| Job | Kerf (mm) | Parts placed | Target (mm²) | Best archived complete layout (mm²) | Above target |
| --- | ---: | ---: | ---: | ---: | ---: |
| Large plates | 0.2 | 66 | 4,988,890 | 5,124,700 | 2.72% |
| Large plates | 1.5 | 66 | 5,052,372 | 5,179,080 | 2.51% |
| Panel hardware | 0.2 | 178 | 4,722,330 | 4,943,285 | 4.68% |
| Panel hardware | 1.5 | 178 | 4,802,345 | 4,997,113 | 4.06% |

The [census](h5-two-sheet-capacity-20261120/layout-census.json) covers the
666 archived native common-line results with complete inventory and validation
records in the 676 selected mechanical-job ZIPs. These contain 651 distinct
layout files across the four comparisons. Six Deepnest archives and four
assignment diagnostics have different output formats. The census is a
retrospective comparison of saved layouts. The original matched three-seed
matrix remains the H5 measurement.

The first inventory pass missed 48 early records whose part counts lived in
the validation output. Its follow-up found that the pair probes validate an
expanded layout. The final pass reads the layout named in each recorded
validation command, checks the original parts, stock, mode and spacing, and
retains every eligible record. The [scripts, file list and process logs](h5-two-sheet-capacity-20261120/layout-census-replay.zip)
include both earlier attempts.
