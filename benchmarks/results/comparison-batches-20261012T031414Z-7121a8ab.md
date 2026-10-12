# deepnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

B, 300 s, identical: 18/18 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| b-albano-nest-mb-free | valid: 3 | 2.59437486 | 2.59437486 | 2.61491980 |
| b-fu-strip-sheet | valid: 3 | 1.36842105 | 1.36842105 | 1.36842105 |
| b-jakobs2-strip-sheet | valid: 3 | 0.83869049 | 0.83720239 | 0.83991816 |
| b-shapes0-nest-mb-free | valid: 3 | 7.28571429 | 7.04761905 | 7.28571429 |
| b-swim-nest-mb-given | valid: 3 | 4.63553770 | 4.56304866 | 4.66756127 |
| b-trousers-nest-mb-given | valid: 3 | 3.26428123 | 3.07545029 | 3.26428123 |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T031414Z-7121a8ab.json).
