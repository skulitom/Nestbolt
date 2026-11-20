# Can the mixed brackets use a shorter last sheet?

On the saved layouts from the full scheduler confirmation, sliding the brackets down, left and down again reduced the mixed-bracket laser job’s material penalty from **1.074% to 1.051%**. The median last sheet was still **0.25745 mm taller** than the original +1% material limit permits. The sliding method increased the shared cutting length on all three confirmation layouts. Repositioning or rotating groups of brackets supplied no further improvement to the material median.

| Source of the three bonus layouts | Original material change vs matched ordinary | After three slides | Within +1% |
| --- | ---: | ---: | --- |
| First full opt-in comparison | +1.417% | +0.884% | Yes |
| Scheduler pilot | −0.457% | −0.461% | Yes |
| Full scheduler confirmation | +1.074% | +1.051% | No |

All percentages compare three-seed medians from the same measurement. These experiments started from saved layouts and consumed additional computation after the original 60-second runs. The [timed confirmation](h5-opt-in-material-budget-20261120.md) remains the gate result.

## What was tried

Across the three measurements there were 18 original layouts for this job and kerf, covering both common-line arms and all seeds. Each layout contains the original 80 parts on two 400 × 300 mm sheets, with 0.2 mm between parts and 1 mm at sheet edges. The rectangular decomposition includes the holes in the plates.

| Method | Attempts | Complete layouts validated |
| --- | ---: | ---: |
| Slide in one or three directions, with or without locking existing shared edges | 108 | 108 |
| Reposition individual high parts at each allowed rotation | 36 | 36 |
| Rebuild the last sheet in three part orders | 54 | 53 |
| Refill the top 4, 8 or 12 parts, also testing gaps on the first sheet | 108 | 108 |
| Joint translation and rotation using constraint programming | 126 | 14 |
| Total | 432 | 319 |

One whole-sheet construction could not fit every part. In the joint search, the first 36 optimization attempts reached their search limit without a solution. A second model sought a 1% reduction in the last sheet’s used height, limited by the highest fixed part. It found 34 constrained cases infeasible and left two unresolved. A third model used the actual matched material threshold. Fourteen cases returned a solution, seven were infeasible, five had a fixed part above the limit, and 28 reached the search limit. Those results apply only to the selected movable parts, conservative square kerf offsets, coordinate grid and solver budget. They leave the general packing question open.

## Verification and replay

Every produced layout passed the public CLI validator. A separate GEOS reconstruction from the original library paths checked the 80 copy identities, stock bounds, permitted rotations, material calculation and total source cutting length. Across **513,943 same-sheet distances**, the closest pair measured **0.200000038 mm**. A brute-force check of 16,900 integer translations independently tested the solver’s obstacle windows. The lowest median over all observed candidates, even allowing a different method for each seed, was still +1.051% on the confirmation layouts.

[Per-layout measurements and matched medians](h5-bracket-axis-compaction-20261120/geometry.json), [all source requests, proposed layouts, native validations and solver outcomes](h5-bracket-axis-compaction-20261120/layouts-and-validations.zip), and [archive and validator hashes](h5-bracket-axis-compaction-20261120/archive.json).

The replay scripts use the archived inputs from the [first full opt-in comparison](h5-common-opt-in-holes-20261120T135332Z/README.md), [scheduler pilot](h5-common-material-budget-pilot-20261120T142949Z/README.md) and [independent confirmation](h5-common-material-budget-confirmation-20261120T143452Z/README.md). Run [replay.py](h5-bracket-axis-compaction-20261120/replay.py), then the relocation, repacking and band scripts from that directory, each with the CLI executable and a work directory as arguments. Run [joint.py](h5-bracket-axis-compaction-20261120/joint.py) for each zero-based matrix and seed with the default arguments, then with `--windows` and `--matched`. It uses OR-Tools 9.15.6755, one worker, a deterministic-time limit of 0.65 and an 8-second wall limit per case. [verify.py](h5-bracket-axis-compaction-20261120/verify.py) takes the work directory and an output JSON path.
