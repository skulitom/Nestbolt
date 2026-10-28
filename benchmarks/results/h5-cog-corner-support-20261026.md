# H5: exact capacity audit and actual-tooth corner support — 2026-10-26

**The short sheet is limited to three cogs; the first-sheet capacity remains
unresolved.** A new, independently checked corner theorem strengthens the
all-angle geometry without assigning cog angles or treating their convex hulls
as solid parts. H2/H5 remain open at **60%**. There is no full 66-part fit,
fixed-49 exclusion, native validation or release qualification.

## The bounded capacity search stays closed

The existing 4,548-cell cover for the corrected source-valid 49 originals is
converted to exact compatibility graphs. Two cells are adjacent only when their
maximum possible squared point distance reaches the proved 254,297 µm minimum
cog-center separation. Each individual cell has smaller diameter, so every
source-valid set of cog centers implies a clique in this necessary graph.

The short-sheet four-cog target is excluded by one coloring certificate node.
The first-sheet 13-cog target reaches the shared **200,000-node cap** without a
clique or complete exclusion. Targets 14 and 15 consume zero additional nodes
after that cap; they are not explored. Total preparation/search/recording time is
53.578805 seconds within the declared 60-second bound. There is no external
solver call, random restart or extension.

The independent reader verifies **9,420,646 cell pairs** and replays all
**199,989 completed certificate nodes**, including the partial first-sheet
certificate. Its missing root prevents a first-sheet exclusion claim. The first
read-only audit is stopped because its repeated pairwise color checks are costly;
that code and interruption are retained. An exact equivalent bitset check then
replays the entire certificate successfully in **88.263258 seconds**. No packing
search is repeated during this reader repair.

## Corner collision follows from actual original vertices

All 40 convex-hull vertices are original cog vertices with radius at least
139,999 µm. Exact cross/dot inequalities establish that each adjacent angular
gap is below 90° and has sine at most 0.234. Because these vertices form a convex
cycle around the origin, some actual vertex is within half the maximum gap of
any requested direction, for every real rotation.

The resulting simultaneous signed-coordinate supports, in µm, are:

| Direction | Original-source support | After conservative center rounding |
|---|---:|---:|
| Diagonal | (86,641, 86,641) | (86,639, 86,639) |
| 4:3 | (101,023, 69,887) | (101,021, 69,885) |
| 3:4 | (69,887, 101,023) | (69,885, 101,021) |

For each source-contained rectangle, the lower corner-offset bounds also ensure
that the selected actual vertex remains before both far edges. Every center in
one of the resulting **closed forbidden boxes** therefore puts an actual source
vertex strictly inside that rectangle. This proves positive-area source overlap.
The convex hull certifies angular coverage only; it is never used as filled
collision geometry. The cog-pair virtual disk is not used for mixed collisions.

The exact reader verifies all 80 original vertices, 40 angular gaps and **1,116
corner boxes**: 828 for the 69 fixed rectangles, and 288 for the 24 moving-bracket
components. Whole-cell containment removes **34 additional cells**, leaving
**4,514** (4,302 first-sheet and 212 short-sheet). All legal boundary centers stay
covered, and all 15 previously checked cog-center cells remain available.

This is a modest tightening. No new feasibility search is opened merely because
these boxes exist. The next placement work needs a materially stronger geometric
decomposition or a different source construction, with all 66 originals and the
same source guards and material target still required. All 22 reserved H2 vectors
remain unopened.

[Checks](h5-cog-corner-support-20261026/checks.json),
[capacity result](h5-cog-corner-support-20261026/capacity-result.json),
[capacity reader](h5-cog-corner-support-20261026/capacity-checks.json),
[corner proof](h5-cog-corner-support-20261026/necessity-proof.json),
[corner reader](h5-cog-corner-support-20261026/corner-checks.json),
[manifest](h5-cog-corner-support-20261026/raw-manifest.json).
The 11,671,716-byte archive verifies 44 canonical files and five identical-content
aliases by exact length, SHA-256 and CRC.


## Publication reconciliation — 2026-10-28

Remote main advanced to `effd34c5` with the layered laser-kit example page.
Its14 changed files are preserved by exact Git blob identity in a clean merge;
the local checkpoint's changed files are also preserved exactly, with no overlap
or conflict. [The local parent](https://github.com/skulitom/Nestbolt/actions/runs/40412648984)
and [new main parent](https://github.com/skulitom/Nestbolt/actions/runs/40488718114)
each pass all six jobs. The sparse-checkout browser run passes86 tests with
four opt-in skips; checkout takes10 seconds. The product source, README files
and Sparrow/Studio heads and releases remain unchanged. The combined head will
receive its own main CI run after the normal push. No new release is qualified.

[Merge preservation](h5-cog-corner-support-20261026/merge-preservation.json),
[publication review](h5-cog-corner-support-20261026/publication-review.json),
[next step](h5-cog-corner-support-20261026/next-step.json).
