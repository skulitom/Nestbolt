# Common-line search development measurement

234/234 runs validated. 60 s wall budget, seeds [0, 1, 2].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Part-in-hole placement in both common-line arms: enabled.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-l | 0.2 | 5.980% | 25.576% | +0.391% |
| c-bracket-l | 1.5 | 3.490% | 25.505% | +0.016% |
| c-bracket-mixed | 0.2 | 2.771% | 21.407% | +1.417% |
| c-bracket-mixed | 1.5 | 3.677% | 21.075% | +0.546% |
| c-bracket-u | 0.2 | 3.235% | 20.336% | -0.000% |
| c-bracket-u | 1.5 | 1.957% | 18.610% | -0.013% |
| c-rect-equal | 0.2 | 17.217% | 30.743% | +0.000% |
| c-rect-equal | 1.5 | 38.833% | 38.833% | +0.000% |
| c-rect-mixed | 0.2 | 40.588% | 40.588% | +0.000% |
| c-rect-mixed | 1.5 | 8.813% | 31.741% | -1.763% |
| m-box-batch-500 | 0.2 | 13.120% | 13.120% | +0.000% |
| m-box-batch-500 | 1.5 | 13.768% | 13.768% | +0.000% |
| m-box-desktop | 0.2 | 0.541% | 5.017% | +0.000% |
| m-box-desktop | 1.5 | 4.167% | 4.167% | +0.024% |
| m-box-long | 0.2 | 12.858% | 12.958% | +0.000% |
| m-box-long | 1.5 | 12.318% | 12.394% | +0.000% |
| m-box-mini | 0.2 | 2.551% | 2.551% | +0.000% |
| m-box-mini | 1.5 | 7.270% | 7.270% | +0.000% |
| m-box-storage | 0.2 | 13.031% | 13.031% | +0.000% |
| m-box-storage | 1.5 | 13.101% | 13.101% | +0.000% |
| m-box-tool | 0.2 | 9.019% | 9.184% | +0.000% |
| m-box-tool | 1.5 | 10.011% | 10.011% | +0.000% |
| m-mechanical-large-plates | 0.2 | 0.000% | 11.036% | +0.000% |
| m-mechanical-large-plates | 1.5 | 0.000% | 9.574% | -1.430% |
| m-mechanical-panel-hardware | 0.2 | 0.000% | 2.200% | +0.149% |
| m-mechanical-panel-hardware | 1.5 | 0.000% | 3.531% | -0.457% |

0.2 mm: median savings 13.031%; median material cost +0.000%; worst material cost +1.417%. 13 complete job pairs.

1.5 mm: median savings 13.101%; median material cost +0.000%; worst material cost +0.546%. 13 complete job pairs.

[Full records and archived inputs/results](results.json)
