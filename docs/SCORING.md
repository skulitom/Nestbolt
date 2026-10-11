# Benchmark scoring conventions

These conventions are defined before the sheet benchmark matrix or optimiser is
frozen. They preserve the plan's fewest-sheets objective and equal-stock metric,
and make the mixed-stock case measurable. `validator::job` computes scores from
original geometry and placements, not from a solver's reported utilisation.

## Complete jobs

The search objective remains lexicographic: place every required copy, minimise
the sheet count, then minimise consumed material and keep a trailing offcut.
Reports show both sheet count and material area. The headline G2 comparison uses
material, as required by the plan; a favourable sheet count alone cannot pass it.

Stock coordinates have X to the right and Y upwards. A last sheet is compressed
towards Y=0. Its used height is the largest placed-part Y plus the top margin and
edge clearance, rounded upwards to the independent checker's grid. One sheet
may be treated as the last sheet: choose the one with the largest trailing offcut
area (stable sheet-ID order breaks a tie). All other occupied sheets are charged
in full. Empty declared sheets are invalid, not free stock.

For rectangular sheets of one size, the reported `normalized_material` is exactly
`(sheets_used - 1) + last_used_height / sheet_height`, including the declared
margins/edge clearance in the used height. A regression test checks this identity.

For mixed sizes:

1. Sum the physical areas of all occupied stock outlines.
2. Subtract the trailing offcut of the chosen last sheet only.
3. Divide by the largest **available stock outline area in the job**, a fixed
   reference independent of either solver's choices.

The denominator cancels in a percentage comparison for a given job. Thus mixed
stock is compared by actual material area, without pretending that different
sheet sizes consume the same amount. Remnant area is its supplied physical
outline (including existing holes). Defects affect where parts fit but do not
discount purchased material. For a remnant, the last-sheet charge is the outline
intersected with the used-height prefix.

`trailing_offcut_area` is geometric uncut stock, not a guarantee that a particular
future part will fit it. Utilisation is original net placed-part area divided by
consumed material. Areas are mm² for physical units and squared model units for
unitless academic jobs. Only valid layouts receive metrics.

## Fill and strip jobs

Fill permits missing copies but prohibits duplicate, unknown or excess copies.
`fill_area` is scored by net placed area. `fill_priority` is scored by the sum of
placed-copy priorities. Both still report material and utilisation; an empty fill
layout has zero area/priority/material. A validity pass alone says nothing about
the quality of that empty solution.

Strip jobs retain strip length as their metric. The Sparrow adapter feeds the
same job validator but returns the original strip-width value for comparison.
M0's predeclared reference/method is unchanged by these sheet conventions.

The final G2 matrix, time budgets, settings and held-out split are not frozen yet.
No headline quality pass or material-reduction claim follows from these formulas.
