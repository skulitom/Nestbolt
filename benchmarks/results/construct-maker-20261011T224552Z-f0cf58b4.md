# Constructor v2: sheet-edge anchors

First Nestbolt constructor diagnostic: all 30 development maker jobs, seed 0, 64 random samples per orientation/region, 60-second process cap. No held-out jobs or quality gate.

**30/30 independently valid layouts.** All 30 use less material than constructor v1, with a median reduction of 20.061918%. This compares two Nestbolt starting solutions, not the competitors and not a completed quality gate.

Median elapsed time: 0.5550 s; maximum: 42.937 s. The 1,000-part case took 42.937 s versus 18.047 s in v1, so search speed still needs work. Concurrent-work timings are diagnostic, not a controlled G4 benchmark.

| Job | Sheets | Material | Reduction vs v1 | Seconds |
| --- | ---: | ---: | ---: | ---: |
| m-box-batch-500 | 3 | 2.037549 | 38.6202% | 13.375 |
| m-box-desktop | 1 | 0.837070 | 37.5451% | 0.266 |
| m-box-long | 1 | 0.325778 | 45.7708% | 0.469 |
| m-box-mini | 1 | 0.720066 | 20.1345% | 0.172 |
| m-box-storage | 1 | 0.538893 | 40.3969% | 0.485 |
| m-box-tool | 2 | 1.531028 | 16.2290% | 0.391 |
| m-garment-bruce-1 | 1 | 0.222983 | 9.3287% | 0.188 |
| m-garment-bruce-2 | 1 | 0.497079 | 10.9915% | 0.375 |
| m-garment-bruce-3 | 2 | 1.131270 | 14.5084% | 2.109 |
| m-garment-teagan-1 | 1 | 0.861007 | 7.5222% | 0.265 |
| m-garment-teagan-2 | 2 | 1.986728 | 22.7952% | 0.421 |
| m-garment-teagan-3 | 5 | 4.671630 | 32.3853% | 1.437 |
| m-mechanical-batch-1000 | 2 | 1.121736 | 21.4101% | 42.937 |
| m-mechanical-cog-washers | 3 | 2.199561 | 6.5595% | 0.500 |
| m-mechanical-defective-stock | 3 | 2.974480 | 19.9893% | 1.906 |
| m-mechanical-frame-inserts | 1 | 0.619678 | 23.2741% | 0.547 |
| m-mechanical-large-plates | 2 | 1.261241 | 21.2793% | 0.266 |
| m-mechanical-mixed-stock | 3 | 1.044011 | 21.1119% | 1.313 |
| m-mechanical-mounting-kit | 3 | 2.947257 | 12.4446% | 0.407 |
| m-mechanical-panel-hardware | 2 | 1.744425 | 21.7814% | 0.875 |
| m-mechanical-remnant-kit | 3 | 0.735041 | 19.1178% | 0.953 |
| m-mechanical-small-brackets | 7 | 6.890062 | 9.0451% | 0.313 |
| m-public-gear-1 | 2 | 1.625247 | 5.1681% | 1.437 |
| m-public-gear-2 | 2 | 1.449081 | 12.4800% | 1.797 |
| m-public-gear-3 | 1 | 0.839155 | 20.7646% | 11.907 |
| m-public-gear-4 | 1 | 0.954228 | 20.6740% | 2.828 |
| m-sign-1 | 1 | 0.875649 | 7.5801% | 0.500 |
| m-sign-2 | 1 | 0.713792 | 9.0736% | 0.563 |
| m-sign-3 | 1 | 0.167031 | 21.0224% | 0.969 |
| m-sign-4 | 1 | 0.437043 | 11.9189% | 1.000 |

[Full layouts, checks and hashes](construct-maker-20261011T224552Z-f0cf58b4.json); [v1 reference](construct-maker-20261011T223817Z-32654739.json).
