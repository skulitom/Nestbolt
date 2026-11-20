# Interlocking brackets in repeatable rows

All 80 original mixed brackets fit below the material ceiling at both kerfs when rows can contain groups of up to four parts. At 0.2 mm the construction used 2.800% less material than the ordinary median in the [full scheduler confirmation](h5-opt-in-material-budget-20261120.md) and saved 25.967% of cutting distance. At 1.5 mm it used 0.585% less material and saved 25.983% of cutting distance. This is a construction from the source shapes. H5 still requires a fresh equal-budget product comparison on all 13 jobs.

| Largest group allowed | Laser material, normalized sheets | Plasma material, normalized sheets |
| --- | ---: | ---: |
| Two parts | 1.756000 | 1.845000 |
| Three parts | 1.722667 | 1.806667 |
| Four parts | 1.632000 | 1.800000 |
| Original +1% ceiling for this comparison | 1.695809 | 1.828692 |

The construction uses only the part inventory, allowed rotations, stock bounds and requested clearance. It places straight-sided parts against each other at the kerf distance, combines compact groups across the stock width, and selects rows that cover all quantities across the two sheets. It uses the same rule at both kerfs. A separate attempt repeated rectangular regions from each previously saved layout. All 36 of those reconstructions passed the CLI validator. They supplied no passing laser material median on the confirmation layouts. [Donor layout replays](h5-repeated-bands-20261120/donor-replay.zip).

The CLI validated and exported all six source constructions. Independent checks measured 9,468 distances and compared the original path vertices and cutting layers in SVG and DXF. The four-part laser and plasma layouts contained 170 and 169 shared straight edges, respectively. Minimum measured clearance was 0.200006 and 1.500006 mm. The four-part Python prototype took approximately five seconds per kerf outside the original nesting run. [Geometry checks](h5-repeated-bands-20261120/geometry.json), [native layouts, reports and exports](h5-repeated-bands-20261120/source-rows.zip), and [construction code](h5-repeated-bands-20261120/rows.py).
