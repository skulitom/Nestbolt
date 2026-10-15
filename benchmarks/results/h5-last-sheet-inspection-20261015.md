# H5 saved-layout inspection — 2026-10-15

The saved failures support investigating exchanges between sheets. This is a
read-only analysis of the retained 60-second H5 development measurement, with
no new searches, changes to the solver or gate adjustments. It does not prove
the complete material target impossible.

For each of the two mechanical jobs, two kerfs and three arms, inspect the
layout that supplies the existing three-seed material median. All twelve source
archives and the used job/layout members match their recorded SHA-256 hashes.
The [machine record](h5-last-sheet-inspection-20261015.json) retains the exact
references, selected seeds, final-sheet part counts and bounds.

| Job | Kerf | Normal final-sheet parts | Bonus final-sheet parts |
| --- | ---: | --- | --- |
| large plates | 0.2 mm | 2 brackets, 4 cogs | 6 brackets, 3 cogs, 5 inserts |
| large plates | 1.5 mm | 5 brackets, 2 cogs | 5 brackets, 4 cogs, 5 inserts |
| panel hardware | 0.2 mm | 18 brackets, 2 frames, 40 cogs | 18 brackets, 2 frames, 42 cogs, 34 inserts |
| panel hardware | 1.5 mm | 17 brackets, 2 frames, 42 cogs | 18 brackets, 2 frames, 42 cogs, 35 inserts |

Common mode reserves holes, so filled outer polygons cannot overlap. A weak
lower bound for a fixed assignment is therefore:

`full sheets + sum(final-sheet filled outer areas) / gross sheet area`.

It deliberately ignores margins, kerf and packing gaps. Normal mode permits
hole riders and does not receive this bound.

For the saved 0.2 mm large-plates bonus median (seed 2), the bound is
**1.108708479292**, already above the unchanged allowed material
**1.108642300777**. Rearranging only those same final-sheet parts cannot meet
the limit. This says nothing about other assignments: moving or exchanging
parts between sheets may improve it. The other seven common-mode median
assignments have this weak area bound below their respective limits, which
does not establish that they can be packed to those limits.

The prior longer warm stages and fixed bracket-pair trials remain rejected.
A future exchange experiment should preserve valid incumbents, account for
all original parts, keep holes reserved and share the existing deadline. All
H5 material/savings requirements and the frozen development inputs remain
unchanged. H5 stays open; completed milestone weight remains 45%.
