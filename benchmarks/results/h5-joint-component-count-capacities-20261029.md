# H5 joint component count capacities — 2026-10-29

Independent necessary-area checks eliminate **197 of 329** ways to distribute
seven brackets and six inserts among their continuous source-support regions.
There are **132 distributions across all 29 cog-site choices** left to examine.
No entire cog-site choice or overall allocation is excluded. No new solver or
native call was opened, and H5 remains open at **60% milestone completion**.

Unlike the finite pose pools in the
[previous checkpoint](h5-finite-source-poses-and-equivalent-graph-reduction-20261029.md),
these constraints hold for every position in the saved conservative unary source
hulls. They retain all legal source modes. They do not cover arbitrary cog
positions or prove global infeasibility.

## Continuous source components

The starting geometry is the independently audited swept cover of each original
source piece over each compatible unary hull. Each 10 mm grid cell conservatively
covers possible occupied material. Because each filled bracket or insert is
connected, it must lie in one eight-neighbour component of its family's support.
The independent readers reconstruct those components with a queue-based grid
traversal and attribute every compatible source-mode region.

Contained rectangles, inset 1e-6 mm and checked against the transformed original
source pieces using exact rationals, give conservative occupied-area lower bounds.
The first reader verifies all 80 rectangle corners. These lower bounds, rather
than rounded nominal part areas, are used in the new mixed-family inequalities.

Initially merging the two families' supports produced only 30 joint components
across 29 choices. A complete 4.114713-second diagnostic found no additional
constraint in 15,120 axis halfspaces. Its [independent reader](h5-joint-component-count-capacities-20261029/joint-audit.json)
verified 132,247 component cells, 6,940 source-region attributions and all initial
and final count sets by independent integer dynamic programming. It did not
recompute every unrecorded halfspace value. No claim of optimality follows from
that diagnostic's lack of new bounds.

## Keeping each family's components separate

The next construction retains 122 family components across the 29 choices.
Bracket components retain the earlier independently proved area/halfspace
capacities; insert capacities use contained-source area and support area.
Enumerating all integer counts with totals seven brackets and six inserts gives
329 possible distributions.

For every subset of those components, the sum of mandatory source area cannot
exceed the area of their union of possible occupied material. This accounts for
overlap between bracket and insert supports instead of giving each family the
same space independently. Of 643 subset-area bounds, 33 certificates exclude
190 distributions, leaving 139. Global axis-halfspace scans add no exclusion.
Preparation took 2.140112 s. The [independent certificate audit](h5-joint-component-count-capacities-20261029/separated-audit.json)
took 2.912051 s and verified all 33 exclusions, all 329 starting distributions,
all 122 components and 6,940 source-region attributions. Unrecorded scan values
are diagnostic; every claimed exclusion is independently checked.

## Halfspaces of mixed component subsets

Restricting the available halfspace area to each selected component subset is
stronger than using the global union. For a selected component and legal source
mode, the exact extrema of all attributed unary hull positions bound translation.
Occupied area above an axis cut increases with the corresponding translation;
below-cut area decreases. The extrema therefore give a lower bound for every
position. Taking the minimum over all legal modes keeps the inequality necessary.

The complete scan covered 425 mixed-family subsets and 214,200 axis halfspaces
in 15.999728 s. Six recorded certificates excluded another seven distributions,
leaving 132. The [independent reader](h5-joint-component-count-capacities-20261029/subset-halfspace-audit.json) used
118 exact polygon clippings, rather than the builder's rectangle-length formula,
to verify every recorded mode coefficient, available support area and removed
distribution. It took 1.903700 s. It did not recompute unrecorded scan values.

| Stage | Starting distributions | Verified exclusions | Remaining | Entire site choices excluded |
| --- | ---: | ---: | ---: | ---: |
| Separate-family subset areas | 329 | 190 | 139 | 0 |
| Mixed-subset halfspaces | 139 | 7 | 132 | 0 |

All preparation stages finished within their declared 60-second discovery caps,
with no cap overrun or partial scan. Each retained choice and distribution is
preserved in the [full count table](h5-joint-component-count-capacities-20261029/all29-subset-halfspaces.json), alongside
its prior component table and every exclusion witness. These are preparation
and proof results; no end-to-end packing runtime is claimed. A future placement
call must charge its required construction stages within the unchanged budget.

## Next work and preserved state

The [next step](h5-joint-component-count-capacities-20261029/next-step.json) is to add conditional component counts to
the local-coordinate source-hull model, keeping variable source positions and
the complete original inventory. Every new constraint and source mapping must
be independently audited before a single bounded call. All prior calls remain
closed. A full66 original-source check must pass before native/material checks,
production integration and the complete H5 matrix.

The 440 overall allocation candidates, 29 site choices, valid short11 and valid64
are unchanged. H2 retains its original gate; none of its reserved vectors was
evaluated. Production code, all three READMEs, upstream Sparrow/Studio state and
releases are unchanged. Stable Latest remains v0.1.0 and preview v0.2.0-alpha.1;
these research results do not qualify a new release.

At the [publication snapshot](h5-joint-component-count-capacities-20261029/publication-review.json), the previous
checkpoint was committed as c2280967 and main remained at 286223ae. Main's
browser, benchmark smoke, both maker jobs and Ubuntu checks had passed; Windows
was still running. The next normal push requires all six checks to pass, no
live main run and fresh remote-head checks. No CI run was cancelled.

The [manifest](h5-joint-component-count-capacities-20261029/raw-manifest.json) preserves 4755 canonical files and
837 identical aliases in 56240641 bytes of multipart evidence. The separate
archive verification checks every byte, recursive binding and local report link.
