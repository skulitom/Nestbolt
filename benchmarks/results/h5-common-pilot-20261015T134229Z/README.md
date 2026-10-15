# Common-line search development measurement

78/78 runs validated. 10 s wall budget, seeds [0].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-l | 0.2 | 4.051% | 24.282% | +0.547% |
| c-bracket-l | 1.5 | 2.505% | 24.779% | +0.234% |
| c-bracket-mixed | 0.2 | 3.442% | 16.303% | +4.809% |
| c-bracket-mixed | 1.5 | 2.678% | 21.093% | +0.458% |
| c-bracket-u | 0.2 | 3.386% | 20.734% | +0.002% |
| c-bracket-u | 1.5 | 3.354% | 20.484% | +4.480% |
| c-rect-equal | 0.2 | 36.048% | 36.517% | +0.000% |
| c-rect-equal | 1.5 | 6.091% | 36.899% | +0.214% |
| c-rect-mixed | 0.2 | 40.588% | 40.588% | +0.000% |
| c-rect-mixed | 1.5 | 36.217% | 36.902% | +0.000% |
| m-box-batch-500 | 0.2 | 13.120% | 13.120% | +0.000% |
| m-box-batch-500 | 1.5 | 13.768% | 13.768% | +0.000% |
| m-box-desktop | 0.2 | 9.487% | 9.791% | +0.000% |
| m-box-desktop | 1.5 | 9.430% | 9.762% | +0.000% |
| m-box-long | 0.2 | 12.858% | 12.958% | +0.000% |
| m-box-long | 1.5 | 12.118% | 12.201% | +0.000% |
| m-box-mini | 0.2 | 1.276% | 1.276% | +0.000% |
| m-box-mini | 1.5 | 7.270% | 7.270% | +0.000% |
| m-box-storage | 0.2 | 13.365% | 13.365% | +0.000% |
| m-box-storage | 1.5 | 13.430% | 13.430% | +0.000% |
| m-box-tool | 0.2 | 8.586% | 8.668% | +0.000% |
| m-box-tool | 1.5 | 8.568% | 8.650% | +0.000% |
| m-mechanical-large-plates | 0.2 | 0.000% | 5.840% | +5.533% |
| m-mechanical-large-plates | 1.5 | 0.000% | 5.442% | +3.529% |
| m-mechanical-panel-hardware | 0.2 | 0.000% | 1.087% | +6.205% |
| m-mechanical-panel-hardware | 1.5 | 0.000% | 0.700% | +5.364% |

0.2 mm: median savings 13.120%; median material cost +0.000%; worst material cost +6.205%. 13 complete job pairs.

1.5 mm: median savings 13.430%; median material cost +0.000%; worst material cost +5.364%. 13 complete job pairs.

[Full records and archived inputs/results](results.json)
