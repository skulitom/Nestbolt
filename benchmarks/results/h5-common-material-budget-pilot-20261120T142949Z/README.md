# Common-line search development measurement

36/36 runs validated. 60 s wall budget, seeds [0, 1, 2].
Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.
Part-in-hole placement in both common-line arms: enabled.
Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.

| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |
| --- | ---: | ---: | ---: | ---: |
| c-bracket-mixed | 0.2 | 2.740% | 22.006% | -0.457% |
| c-bracket-mixed | 1.5 | 2.328% | 21.551% | +0.098% |
| m-mechanical-large-plates | 0.2 | 0.000% | 10.226% | -0.000% |
| m-mechanical-large-plates | 1.5 | 0.000% | 8.931% | +0.745% |

0.2 mm: median savings 16.116%; median material cost -0.228%; worst material cost -0.000%. 2 complete job pairs.

1.5 mm: median savings 15.241%; median material cost +0.422%; worst material cost +0.745%. 2 complete job pairs.

[Full records and archived inputs/results](results.json)
