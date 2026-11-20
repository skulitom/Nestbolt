# Common-line search development measurement

72/72 runs validated. 60 s wall budget, seeds [0, 1, 2].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Part-in-hole placement in both common-line arms: enabled.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-mixed | 0.2 | 2.780% | 28.661% | -4.932% |
| c-bracket-mixed | 1.5 | 2.522% | 26.888% | -0.486% |
| c-rect-mixed | 0.2 | 40.588% | 40.588% | +0.000% |
| c-rect-mixed | 1.5 | 36.217% | 39.569% | -4.071% |
| m-mechanical-large-plates | 0.2 | 0.000% | 11.136% | +1.375% |
| m-mechanical-large-plates | 1.5 | 0.000% | 6.455% | -0.020% |
| m-mechanical-panel-hardware | 0.2 | 0.119% | 2.115% | -0.008% |
| m-mechanical-panel-hardware | 1.5 | 0.000% | 1.672% | +0.685% |

0.2 mm: median savings 19.898%; median material cost -0.004%; worst material cost +1.375%. 4 complete job pairs.

1.5 mm: median savings 16.671%; median material cost -0.253%; worst material cost +0.685%. 4 complete job pairs.

[Full records and archived inputs/results](results.json)
