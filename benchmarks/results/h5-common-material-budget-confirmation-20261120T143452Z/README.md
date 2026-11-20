# Common-line search development measurement

234/234 runs validated. 60 s wall budget, seeds [0, 1, 2].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Part-in-hole placement in both common-line arms: enabled.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-l | 0.2 | 4.843% | 25.576% | -0.030% |
| c-bracket-l | 1.5 | 3.576% | 22.553% | +0.037% |
| c-bracket-mixed | 0.2 | 3.487% | 22.210% | +1.074% |
| c-bracket-mixed | 1.5 | 2.233% | 21.471% | +0.355% |
| c-bracket-u | 0.2 | 3.436% | 19.787% | +0.001% |
| c-bracket-u | 1.5 | 3.892% | 19.362% | -0.003% |
| c-rect-equal | 0.2 | 17.217% | 30.743% | +0.000% |
| c-rect-equal | 1.5 | 38.833% | 38.833% | +0.000% |
| c-rect-mixed | 0.2 | 40.588% | 40.588% | +0.000% |
| c-rect-mixed | 1.5 | 9.149% | 31.497% | -0.000% |
| m-box-batch-500 | 0.2 | 13.120% | 13.120% | +0.000% |
| m-box-batch-500 | 1.5 | 13.768% | 13.768% | +0.000% |
| m-box-desktop | 0.2 | 0.541% | 5.305% | +0.029% |
| m-box-desktop | 1.5 | 0.000% | 4.006% | +0.009% |
| m-box-long | 0.2 | 12.858% | 12.958% | +0.000% |
| m-box-long | 1.5 | 12.318% | 12.394% | +0.000% |
| m-box-mini | 0.2 | 2.551% | 2.551% | +0.000% |
| m-box-mini | 1.5 | 7.270% | 7.270% | +0.000% |
| m-box-storage | 0.2 | 13.031% | 13.031% | +0.000% |
| m-box-storage | 1.5 | 13.101% | 13.101% | +0.000% |
| m-box-tool | 0.2 | 9.019% | 9.184% | +0.000% |
| m-box-tool | 1.5 | 10.011% | 10.011% | +0.000% |
| m-mechanical-large-plates | 0.2 | 0.000% | 10.631% | +0.006% |
| m-mechanical-large-plates | 1.5 | 0.000% | 7.720% | +0.886% |
| m-mechanical-panel-hardware | 0.2 | 0.000% | 2.406% | -0.015% |
| m-mechanical-panel-hardware | 1.5 | 0.000% | 4.898% | -0.322% |

0.2 mm: median savings 13.031%; median material cost +0.000%; worst material cost +1.074%. 13 complete job pairs.

1.5 mm: median savings 13.101%; median material cost +0.000%; worst material cost +0.886%. 13 complete job pairs.

[Full records and archived inputs/results](results.json)
