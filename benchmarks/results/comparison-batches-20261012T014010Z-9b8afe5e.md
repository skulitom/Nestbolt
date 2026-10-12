# deepnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

B, 60 s, expanded: 105/105 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| b-albano-nest-mb-free | valid: 3 | 3.48052045 | 3.23984342 | 3.59931951 |
| b-albano-nest-mb-given | valid: 3 | 2.90199956 | 2.90199956 | 2.90322662 |
| b-albano-strip-sheet | valid: 3 | 1.90003443 | 1.89535043 | 1.93133500 |
| b-blaz1-nest-mb-free | valid: 3 | 10.89428067 | 10.78047367 | 11.28047367 |
| b-blaz1-nest-mb-given | valid: 3 | 9.80000000 | 9.80000000 | 9.80000000 |
| b-blaz1-strip-sheet | valid: 3 | 3.60000000 | 3.51666667 | 3.61666667 |
| b-dagli-strip-sheet | valid: 3 | 0.96149427 | 0.95574713 | 0.97574713 |
| b-fu-nest-mb-free | valid: 3 | 5.65200229 | 5.25275283 | 5.65427043 |
| b-fu-nest-mb-given | valid: 3 | 3.66666667 | 3.66666667 | 3.71428571 |
| b-fu-strip-sheet | valid: 3 | 1.53658818 | 1.47882041 | 1.67618883 |
| b-jakobs1-nest-mb-free | valid: 3 | 4.60085400 | 4.56833496 | 4.63376033 |
| b-jakobs1-nest-mb-given | valid: 3 | 3.83333333 | 3.79166667 | 3.87500000 |
| b-jakobs1-strip-sheet | valid: 3 | 0.82500000 | 0.81875000 | 0.85000000 |
| b-jakobs2-nest-mb-free | valid: 3 | 3.93903271 | 3.93713267 | 3.94326494 |
| b-jakobs2-nest-mb-given | valid: 3 | 3.79166667 | 3.72916667 | 3.81250000 |
| b-jakobs2-strip-sheet | valid: 3 | 0.96904763 | 0.92988096 | 0.97075894 |
| b-mao-nest-mb-free | valid: 3 | 2.73509667 | 2.55697828 | 2.75181736 |
| b-mao-nest-mb-given | valid: 3 | 2.80048174 | 2.79455249 | 2.80098497 |
| b-mao-strip-sheet | valid: 3 | 0.89527756 | 0.89253053 | 0.89896889 |
| b-marques-strip-sheet | valid: 3 | 1.27197802 | 1.22733516 | 1.28983516 |
| b-shapes0-nest-mb-free | valid: 3 | 7.85201452 | 7.73529660 | 7.87599419 |
| b-shapes0-nest-mb-given | valid: 3 | 7.80952381 | 7.80952381 | 7.80952381 |
| b-shapes0-strip-sheet | valid: 3 | 2.90000000 | 2.90000000 | 2.90000000 |
| b-shapes1-nest-mb-free | valid: 3 | 7.85201452 | 7.73529660 | 7.87599419 |
| b-shapes1-nest-mb-given | valid: 3 | 7.80952381 | 7.80952381 | 7.80952381 |
| b-shapes1-strip-sheet | valid: 3 | 2.45000000 | 2.45000000 | 2.50000000 |
| b-shirts-nest-mb-free | invalid: 1, valid: 2 | 8.47462462 | 8.20713287 | failed |
| b-shirts-nest-mb-given | valid: 3 | 8.87179487 | 8.82051282 | 8.87179487 |
| b-shirts-strip-sheet | valid: 3 | 2.59375000 | 2.58125000 | 2.60491071 |
| b-swim-nest-mb-free | valid: 3 | 5.62896794 | 5.62040827 | 5.67664120 |
| b-swim-nest-mb-given | valid: 3 | 4.89074698 | 4.85024868 | 4.92590500 |
| b-swim-strip-sheet | valid: 3 | 1.69424863 | 1.69298112 | 1.74775860 |
| b-trousers-nest-mb-free | valid: 3 | 3.72335210 | 3.72096745 | 3.77176564 |
| b-trousers-nest-mb-given | valid: 3 | 3.31116906 | 3.31116906 | 3.33637549 |
| b-trousers-strip-sheet | valid: 3 | 2.34858813 | 2.27555989 | 2.34858813 |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T014010Z-9b8afe5e.json).

1 explicitly named harness failures were replaced: input guard or affinity setup before solving, or process cleanup after the budget. Original audited records and all replacement outcomes remain in the JSON. This option rejects solver crashes, invalid layouts, timeouts and no-layout outcomes.
