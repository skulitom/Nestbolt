# Balanced two-to-three exchange witness — 2026-10-17

The independent CLI validator accepts both authored layouts with seven parts
and **identical metrics, including 19,700 mm² material**. Two 30 × 45 mm parts
move from the last sheet to the first, and three 30 × 30 mm squares move back.
Both moved groups have area 2,700 mm². Each sheet keeps one 60 × 94 mm filler.
All rotations are fixed at zero, stock is 100 × 100 mm, edge clearance is 1 mm,
and part clearance is 0.2 mm. Only sheet assignments change in the valid witness.

## Why moving one selected incoming part is insufficient

This bound concerns those two narrow incoming parts and three return squares,
with one filler on each sheet; it does not rule out other part selections or
global layouts. The filler may move within its sheet without invalidating the bound.

Each usable sheet is 98 × 98 mm. Its filler leaves only 4 mm of combined space
above/below it, so every small rectangle must lie to one side. Combined side
space is 38 mm; two sides cannot each fit a 30 mm-wide part. All small parts
therefore share one side band of width at most 38 mm. Their 30 mm-wide horizontal
intervals overlap, so their heights must stack without overlap within 98 mm.

Moving only one 45 mm-high incoming part and returning k squares gives these
necessary heights, even before adding positive clearance:

| Returned squares k | Receiving sheet | Return sheet | Can both fit within 98 mm? |
| ---: | ---: | ---: | --- |
| 0 | 135 mm | 45 mm | No |
| 1 | 105 mm | 75 mm | No |
| 2 | 75 mm | 105 mm | No |
| 3 | 45 mm | 135 mm | No |

Moving both incoming parts and all three squares instead requires 90.2 mm and
90.4 mm including minimum inter-part clearance. The saved concrete placements
use 2 mm gaps and pass the independent validator. The group exchange therefore
addresses a real limitation of these single-incoming choices without changing
geometry, quantities, orientations or the material limit.

No optimizer ran, no mechanical benchmark feasibility or improvement is proved,
and no new search heuristic is implemented here. The mechanical traces still
need source-capacity/placement inspection. H2/H5 remain open at 60%.
