# Lead allowance material cost

7/8 runs validated. 5 s wall budget, seeds [0].
Both arms use common-line mode at the same kerf, bonus off. Leads use default line / 3 mm / 45° outer / 90° hole.
Geometry is the frozen polygon job, represented as exact line contours. Material includes lead extents. Flags remain unresolved and are never hidden.
Every pair uses the ratio of the two seed medians. Incomplete pairs are not scored. This development result does not change published v1 claims.

| Job | Kerf mm | Baseline material | Lead material | Cost | Flagged / expected (max) |
| --- | ---: | ---: | ---: | ---: | ---: |
| c-bracket-mixed | 0.2 | 1.951834 | 1.974927 | +1.183% | 0/128 |
| c-bracket-mixed | 1.5 | 1.953011 | 2.262735 | +15.859% | 0/128 |
| m-box-batch-500 | 0.2 | 2.037541 | 2.139954 | +5.026% | 0/4300 |
| m-box-batch-500 | 1.5 | failed/incomplete | — | — | — |

0.2 mm kerf: median measured cost +3.105% across 2 complete job pairs.

1.5 mm kerf: median measured cost +15.859% across 1 complete job pairs.

[Full records and archived raw inputs/results](results.json)
