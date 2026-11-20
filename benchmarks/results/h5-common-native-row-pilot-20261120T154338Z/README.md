# Common-line search development measurement

36/36 runs validated. 60 s wall budget, seeds [0, 1, 2].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Part-in-hole placement in both common-line arms: enabled.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-mixed | 0.2 | 3.099% | 28.661% | -4.904% |
| c-bracket-mixed | 1.5 | 2.169% | 26.888% | -0.386% |
| m-mechanical-large-plates | 0.2 | 0.000% | 9.629% | +0.024% |
| m-mechanical-large-plates | 1.5 | 0.000% | 8.711% | +0.703% |

0.2 mm: median savings 19.145%; median material cost -2.440%; worst material cost +0.024%. 2 complete job pairs.

1.5 mm: median savings 17.800%; median material cost +0.159%; worst material cost +0.703%. 2 complete job pairs.

[Full records and archived inputs/results](results.json)
