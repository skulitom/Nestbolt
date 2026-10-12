# svgnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

B, 300 s, expanded: 18/18 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| b-albano-nest-mb-free | valid: 3 | 3.61399240 | 3.50148132 | 3.73167090 |
| b-fu-strip-sheet | valid: 3 | 1.37111139 | 1.36976622 | 1.38292412 |
| b-jakobs2-strip-sheet | invalid: 2, valid: 1 | failed | failed | failed |
| b-shapes0-nest-mb-free | invalid: 1, valid: 2 | 8.79283738 | 8.77731933 | failed |
| b-swim-nest-mb-given | valid: 3 | 5.16220649 | 5.04800896 | 5.20846828 |
| b-trousers-nest-mb-given | valid: 3 | 3.23728814 | 3.20338983 | 3.27422860 |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T021336Z-74941dfd.json).
