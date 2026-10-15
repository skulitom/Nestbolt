# Lead allowance material cost

155/156 runs validated. 60 s wall budget, seeds [0, 1, 2].
Both arms use common-line mode at the same kerf, bonus off. Leads use default line / 3 mm / 45° outer / 90° hole.
Geometry is the frozen polygon job, represented as exact line contours. Material includes lead extents. Flags remain unresolved and are never hidden.
Every pair uses the ratio of the two seed medians. Incomplete pairs are not scored. This development result does not change published v1 claims.

| Job | Kerf mm | Baseline material | Lead material | Cost | Flagged / expected (max) |
| --- | ---: | ---: | ---: | ---: | ---: |
| c-bracket-l | 0.2 | 0.711900 | 0.798543 | +12.171% | 0/60 |
| c-bracket-l | 1.5 | 0.782324 | 0.917582 | +17.289% | 0/60 |
| c-bracket-mixed | 0.2 | 1.708131 | 1.846914 | +8.125% | 0/128 |
| c-bracket-mixed | 1.5 | 1.830439 | 2.169455 | +18.521% | 0/128 |
| c-bracket-u | 0.2 | 1.214035 | 1.280693 | +5.491% | 0/50 |
| c-bracket-u | 1.5 | 1.218594 | 1.408556 | +15.589% | 0/50 |
| c-rect-equal | 0.2 | 1.361000 | 1.411168 | +3.686% | 0/60 |
| c-rect-equal | 1.5 | 1.367500 | 1.561835 | +14.211% | 0/60 |
| c-rect-mixed | 0.2 | 1.174000 | 1.179692 | +0.485% | 0/90 |
| c-rect-mixed | 1.5 | failed/incomplete | — | — | — |
| m-box-batch-500 | 0.2 | 2.037541 | 2.124222 | +4.254% | 0/4300 |
| m-box-batch-500 | 1.5 | 2.171148 | 2.238111 | +3.084% | 3800/4300 |
| m-box-desktop | 0.2 | 0.830635 | 0.830847 | +0.026% | 0/174 |
| m-box-desktop | 1.5 | 0.844001 | 0.890494 | +5.509% | 144/174 |
| m-box-long | 0.2 | 0.308361 | 0.308499 | +0.045% | 0/165 |
| m-box-long | 1.5 | 0.310492 | 0.310688 | +0.063% | 0/165 |
| m-box-mini | 0.2 | 0.660000 | 0.661294 | +0.196% | 0/68 |
| m-box-mini | 1.5 | 0.723000 | 0.733735 | +1.485% | 48/68 |
| m-box-storage | 0.2 | 0.517378 | 0.518497 | +0.216% | 0/171 |
| m-box-storage | 1.5 | 0.519509 | 0.540317 | +4.005% | 0/171 |
| m-box-tool | 0.2 | 1.329000 | 1.329051 | +0.004% | 0/148 |
| m-box-tool | 1.5 | 1.329000 | 1.432813 | +7.811% | 0/148 |
| m-mechanical-large-plates | 0.2 | 1.149495 | 1.161789 | +1.070% | 0/156 |
| m-mechanical-large-plates | 1.5 | 1.163954 | 1.189762 | +2.217% | 0/156 |
| m-mechanical-panel-hardware | 0.2 | 1.594343 | 1.651505 | +3.585% | 0/436 |
| m-mechanical-panel-hardware | 1.5 | 1.606755 | 1.704689 | +6.095% | 0/436 |

0.2 mm kerf: median measured cost +1.070% across 13 complete job pairs.

1.5 mm kerf: median measured cost +5.802% across 12 complete job pairs.

[Full records and archived raw inputs/results](results.json)
