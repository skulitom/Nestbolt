# Common-line search development measurement

72/72 runs validated. 60 s wall budget, seeds [0, 1, 2].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Part-in-hole placement in both common-line arms: enabled.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-mixed | 0.2 | 3.124% | 28.661% | -2.338% |
| c-bracket-mixed | 1.5 | 2.093% | 26.888% | -0.391% |
| c-rect-mixed | 0.2 | 40.588% | 40.588% | +0.000% |
| c-rect-mixed | 1.5 | 12.203% | 39.569% | -2.754% |
| m-mechanical-large-plates | 0.2 | 0.000% | 14.436% | -0.007% |
| m-mechanical-large-plates | 1.5 | 0.000% | 11.954% | -1.416% |
| m-mechanical-panel-hardware | 0.2 | 0.000% | 5.577% | +0.055% |
| m-mechanical-panel-hardware | 1.5 | 0.000% | 4.932% | -0.133% |

0.2 mm: median savings 21.549%; median material cost -0.003%; worst material cost +0.055%. 4 complete job pairs.

1.5 mm: median savings 19.421%; median material cost -0.903%; worst material cost -0.133%. 4 complete job pairs.

[Full records and archived inputs/results](results.json)
