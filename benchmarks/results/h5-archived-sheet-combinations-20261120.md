# Reusing common-line sheets across complete mechanical layouts

The public CLI validated and exported four complete mechanical layouts with
less material than the best individual archives. The reductions range from
51 to 2,805 mm². All four remain above the original material targets.

| Job | Kerf (mm) | Parts | New material (mm²) | Saved vs best archive (mm²) | Above target |
| --- | ---: | ---: | ---: | ---: | ---: |
| Large plates | 0.2 | 66 | 5,121,894 | 2,805 | 2.666% |
| Large plates | 1.5 | 66 | 5,178,976 | 104 | 2.506% |
| Panel hardware | 0.2 | 178 | 4,942,973 | 312 | 4.672% |
| Panel hardware | 1.5 | 178 | 4,997,062 | 51 | 4.055% |

The comparison uses the 651 distinct native layouts in the [archive census](h5-two-sheet-capacity-20261120.md#complete-archived-layouts).
For each job and kerf, keep one archived sheet intact and supply its remaining
parts from a horizontal band on either sheet of any layout. For each possible
upper edge, choosing the highest available lower edges for the required copies
of each family gives the shortest band ending there. The band can move vertically
as a unit. Dropping surplus copies preserves the relative positions of every
remaining pair. The construction examined 16,736 compatible combinations of
first-sheet inventory and donor sheet. For three combinations of job and kerf
the winning sheets came from different layouts. For the 0.2 mm large plates,
moving the original second sheet down 1.870130 mm gave the best result.

The [construction record](h5-archived-sheet-combinations-20261120/construction.json)
identifies both source sheets and the original request in each case. The
[validation results](h5-archived-sheet-combinations-20261120/verified.json)
give the exact material and layout hashes. Each original quantity is present,
all holes are reserved and each layout has zero validation violations.
The [four layouts, native reports and exports](h5-archived-sheet-combinations-20261120/layouts-and-exports.zip)
include the two process receipts. Construction took 6.812 s and independent
validation and export took 2.250 s. The source layouts came from earlier runs.
The original three-seed H5 comparison remains the acceptance measurement.

To reproduce, run [combine.py](h5-archived-sheet-combinations-20261120/combine.py)
with an empty output directory, then [verify.py](h5-archived-sheet-combinations-20261120/verify.py)
with that directory and the release CLI path.

## Stacking archived horizontal bands

On the 66-part large-plate laser job, even stacking bands with **zero space
between them** would require at least 53.069510 mm more combined sheet height
than the target allows. This result covers vertical translations of horizontal
bands from the 310 archived sheets. Their internal relative positions and
orientations are fixed. Parts crossing a band edge can be discarded.

The catalogue found 13,632 different band inventories. Four nonnegative
family weights give each possible band a total weight at most its height plus
0.2 mm. This makes the required 66 parts weigh 3,366.196413 mm. Even refunding
0.2 mm for every part leaves 3,352.996413 mm against 3,299.926903 mm of
usable stock height. The refund covers up to 66 nonempty bands.

An independent reader checked the weights against 214,376 subsets generated
directly from the original placements. It used interval trigonometry and
rounded each occupied interval inward to a nanometre. Every subset of a
horizontal band is covered because the weights are nonnegative. The smallest
verified slack was 1,263 nm. The price test closed this construction before
the conditional integer solver. Both fixed arrangements and the 418 possible
two-sheet allocations in the broader geometry problem remain open.
[Family weights](h5-archived-sheet-combinations-20261120/band-prices.json),
[independent check](h5-archived-sheet-combinations-20261120/band-verification.json)
and [catalogue and process logs](h5-archived-sheet-combinations-20261120/band-catalogue.zip).

Quarter-turning source windows also preserves the allowed part rotations.
After turning, each window must fit across the 1,487 mm usable width. Adding
those windows increases the catalogue from 13,632 to 16,046 inventories.
Pricing the combined catalogue directly at zero clearance between bands
gives a stronger bound. At least 3,364.630425 mm of height is needed, a
**64.703522 mm deficit** against the stock. An independent check tested
214,376 horizontal prefixes and 1,058,165 turned prefixes in 9,055 windows.
Every prefix satisfies the inequality with at least 1,999 nm of slack. The
conditional assignment stage was unnecessary. New individual part positions
remain outside this result.
[Quarter-turn prices](h5-archived-sheet-combinations-20261120/turned-prices.json),
[independent verification](h5-archived-sheet-combinations-20261120/turned-verification.json)
and [catalogue and process logs](h5-archived-sheet-combinations-20261120/turned-catalogue.zip).
