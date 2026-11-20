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
