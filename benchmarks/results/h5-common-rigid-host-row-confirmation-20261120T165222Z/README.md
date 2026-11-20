# Common-line search development measurement

234/234 runs validated. 60 s wall budget, seeds [0, 1, 2].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Part-in-hole placement in both common-line arms: enabled.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-l | 0.2 | 4.932% | 25.576% | -0.700% |
| c-bracket-l | 1.5 | 5.054% | 25.379% | -0.055% |
| c-bracket-mixed | 0.2 | 3.833% | 28.661% | -4.955% |
| c-bracket-mixed | 1.5 | 2.768% | 26.888% | -3.073% |
| c-bracket-u | 0.2 | 2.302% | 25.680% | -0.007% |
| c-bracket-u | 1.5 | 2.385% | 19.978% | +0.000% |
| c-rect-equal | 0.2 | 16.215% | 39.743% | -0.000% |
| c-rect-equal | 1.5 | 38.833% | 39.619% | -0.000% |
| c-rect-mixed | 0.2 | 40.588% | 40.588% | +0.000% |
| c-rect-mixed | 1.5 | 36.217% | 39.569% | -4.071% |
| m-box-batch-500 | 0.2 | 13.120% | 13.120% | +0.000% |
| m-box-batch-500 | 1.5 | 13.768% | 13.768% | +0.000% |
| m-box-desktop | 0.2 | 1.082% | 5.727% | +0.002% |
| m-box-desktop | 1.5 | 0.000% | 4.167% | +0.013% |
| m-box-long | 0.2 | 12.858% | 12.958% | +0.000% |
| m-box-long | 1.5 | 12.318% | 12.394% | +0.000% |
| m-box-mini | 0.2 | 2.551% | 9.269% | -0.000% |
| m-box-mini | 1.5 | 7.270% | 10.130% | -5.878% |
| m-box-storage | 0.2 | 13.031% | 13.031% | +0.000% |
| m-box-storage | 1.5 | 13.101% | 13.101% | +0.000% |
| m-box-tool | 0.2 | 9.019% | 9.184% | +0.000% |
| m-box-tool | 1.5 | 10.011% | 10.011% | +0.000% |
| m-mechanical-large-plates | 0.2 | 0.000% | 12.903% | -0.008% |
| m-mechanical-large-plates | 1.5 | 0.000% | 11.951% | -0.645% |
| m-mechanical-panel-hardware | 0.2 | 0.000% | 2.139% | -0.302% |
| m-mechanical-panel-hardware | 1.5 | 0.000% | 2.712% | -0.115% |

0.2 mm: median savings 13.031%; median material cost -0.000%; worst material cost +0.002%. 13 complete job pairs.

1.5 mm: median savings 13.101%; median material cost -0.000%; worst material cost +0.013%. 13 complete job pairs.

[Full records and archived inputs/results](results.json)
