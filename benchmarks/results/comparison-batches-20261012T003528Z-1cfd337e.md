# deepnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

B, 60 s, identical: 105/105 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| b-albano-nest-mb-free | valid: 3 | 2.59437486 | 2.59437486 | 2.69676994 |
| b-albano-nest-mb-given | valid: 3 | 2.84464953 | 2.84209519 | 2.84464953 |
| b-albano-strip-sheet | valid: 3 | 1.78487146 | 1.78476328 | 1.79751988 |
| b-blaz1-nest-mb-free | valid: 3 | 9.80000000 | 9.73333333 | 10.23333333 |
| b-blaz1-nest-mb-given | valid: 3 | 9.76666667 | 9.71666667 | 10.21666667 |
| b-blaz1-strip-sheet | valid: 3 | 3.33333333 | 3.33333333 | 3.35000003 |
| b-dagli-strip-sheet | valid: 3 | 0.95045977 | 0.94455123 | 0.95200018 |
| b-fu-nest-mb-free | valid: 3 | 3.66666667 | 3.66666667 | 3.71428571 |
| b-fu-nest-mb-given | valid: 3 | 3.66666667 | 3.66666667 | 3.71428571 |
| b-fu-strip-sheet | valid: 3 | 1.38439853 | 1.37640979 | 1.38674814 |
| b-jakobs1-nest-mb-free | valid: 3 | 3.90476200 | 3.82738100 | 3.91071433 |
| b-jakobs1-nest-mb-given | valid: 3 | 3.90476200 | 3.82738100 | 3.91071433 |
| b-jakobs1-strip-sheet | valid: 3 | 0.77500005 | 0.77500002 | 0.78750002 |
| b-jakobs2-nest-mb-free | valid: 3 | 3.58333333 | 3.58333333 | 3.62500000 |
| b-jakobs2-nest-mb-given | valid: 3 | 3.58333333 | 3.58333333 | 3.62500000 |
| b-jakobs2-strip-sheet | valid: 3 | 0.85238096 | 0.84940477 | 0.85297619 |
| b-mao-nest-mb-free | valid: 3 | 1.91077634 | 1.87029927 | 1.91441953 |
| b-mao-nest-mb-given | valid: 3 | 2.17137648 | 2.17137648 | 2.17137648 |
| b-mao-strip-sheet | valid: 3 | 0.86994809 | 0.86215107 | 0.87329681 |
| b-marques-strip-sheet | valid: 3 | 1.10576923 | 1.10096154 | 1.12500000 |
| b-shapes0-nest-mb-free | valid: 3 | 7.52380952 | 7.50000000 | 7.52380952 |
| b-shapes0-nest-mb-given | valid: 3 | 7.52380952 | 7.52380952 | 7.54761905 |
| b-shapes0-strip-sheet | valid: 3 | 2.77500000 | 2.77500000 | 2.77500000 |
| b-shapes1-nest-mb-free | valid: 3 | 7.52380952 | 7.52380952 | 7.54761905 |
| b-shapes1-nest-mb-given | valid: 3 | 7.57142857 | 7.52380952 | 7.66666667 |
| b-shapes1-strip-sheet | valid: 3 | 2.50000000 | 2.50000000 | 2.50000000 |
| b-shirts-nest-mb-free | valid: 3 | 7.46153846 | 7.43589744 | 7.46153846 |
| b-shirts-nest-mb-given | valid: 3 | 8.20512821 | 8.20512821 | 8.28205128 |
| b-shirts-strip-sheet | valid: 3 | 2.56309528 | 2.56175598 | 2.56412340 |
| b-swim-nest-mb-free | failed: 1, valid: 2 | 4.90342161 | 4.89321386 | failed |
| b-swim-nest-mb-given | valid: 3 | 4.62451510 | 4.61856796 | 4.71991222 |
| b-swim-strip-sheet | valid: 3 | 1.70219783 | 1.69785572 | 1.71396167 |
| b-trousers-nest-mb-free | valid: 3 | 2.66666667 | 2.66666667 | 2.66666667 |
| b-trousers-nest-mb-given | valid: 3 | 3.26428123 | 3.26428123 | 3.29022406 |
| b-trousers-strip-sheet | valid: 3 | 2.20253165 | 2.20253165 | 2.20253165 |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T003528Z-1cfd337e.json).
