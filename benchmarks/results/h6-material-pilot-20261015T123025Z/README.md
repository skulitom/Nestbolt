# Lead allowance material cost

4/12 runs validated. 2 s wall budget, seeds [0].
Both arms use common-line mode at the same kerf, bonus off. Leads use default line / 3 mm / 45° outer / 90° hole.
Geometry is the frozen polygon job, represented as exact line contours. Material includes lead extents. Flags remain unresolved and are never hidden.
Every pair uses the ratio of the two seed medians. Incomplete pairs are not scored. This development result does not change published v1 claims.

| Job | Kerf mm | Baseline material | Lead material | Cost | Flagged / expected (max) |
| --- | ---: | ---: | ---: | ---: | ---: |
| c-bracket-mixed | 0.2 | failed/incomplete | — | — | — |
| c-bracket-mixed | 1.5 | failed/incomplete | — | — | — |
| m-box-batch-500 | 0.2 | failed/incomplete | — | — | — |
| m-box-batch-500 | 1.5 | failed/incomplete | — | — | — |
| m-box-mini | 0.2 | 0.660000 | 0.711866 | +7.858% | 0/68 |
| m-box-mini | 1.5 | failed/incomplete | — | — | — |

0.2 mm kerf: median measured cost +7.858% across 1 complete job pairs.

[Full records and archived raw inputs/results](results.json)
