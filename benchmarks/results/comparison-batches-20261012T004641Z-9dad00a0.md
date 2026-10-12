# svgnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

B, 60 s, expanded: 105/105 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| b-albano-nest-mb-free | valid: 3 | 3.35640932 | 3.33947724 | 3.47971568 |
| b-albano-nest-mb-given | valid: 3 | 4.16172270 | 4.13480554 | 4.16172270 |
| b-albano-strip-sheet | timeout: 1, valid: 2 | 3.22207855 | 3.18614132 | failed |
| b-blaz1-nest-mb-free | valid: 3 | 18.53333333 | 18.05665020 | 18.55665020 |
| b-blaz1-nest-mb-given | valid: 3 | 15.53333333 | 15.53333333 | 16.01666667 |
| b-blaz1-strip-sheet | valid: 3 | 3.60000000 | 3.60000000 | 3.70000000 |
| b-dagli-strip-sheet | valid: 3 | 0.97816093 | 0.97760537 | 0.98074713 |
| b-fu-nest-mb-free | valid: 3 | 4.77230395 | 4.75163155 | 4.81338957 |
| b-fu-nest-mb-given | valid: 3 | 3.80952381 | 3.73809524 | 3.84523810 |
| b-fu-strip-sheet | valid: 3 | 1.39473684 | 1.38292412 | 1.42105263 |
| b-jakobs1-nest-mb-free | invalid: 1, valid: 2 | 5.54998650 | 5.45541521 | failed |
| b-jakobs1-nest-mb-given | invalid: 2, valid: 1 | failed | failed | failed |
| b-jakobs1-strip-sheet | invalid: 2, valid: 1 | failed | failed | failed |
| b-jakobs2-nest-mb-free | valid: 3 | 4.67311212 | 4.63055937 | 4.74793560 |
| b-jakobs2-nest-mb-given | invalid: 2, valid: 1 | failed | failed | failed |
| b-jakobs2-strip-sheet | invalid: 2, valid: 1 | failed | failed | failed |
| b-mao-nest-mb-free | valid: 3 | 2.51096341 | 2.46995647 | 2.69512999 |
| b-mao-nest-mb-given | valid: 3 | 2.42696281 | 2.38479915 | 2.44625743 |
| b-mao-strip-sheet | valid: 3 | 0.89362960 | 0.88547900 | 0.91801353 |
| b-marques-strip-sheet | valid: 3 | 1.19230769 | 1.19230769 | 1.19711538 |
| b-shapes0-nest-mb-free | invalid: 1, valid: 2 | 8.73014795 | 8.69478383 | failed |
| b-shapes0-nest-mb-given | invalid: 2, valid: 1 | failed | failed | failed |
| b-shapes0-strip-sheet | valid: 3 | 2.82500000 | 2.82500000 | 2.82500000 |
| b-shapes1-nest-mb-free | invalid: 1, valid: 2 | 8.76405343 | 8.71173657 | failed |
| b-shapes1-nest-mb-given | invalid: 3 | failed | failed | failed |
| b-shapes1-strip-sheet | invalid: 2, valid: 1 | failed | failed | failed |
| b-shirts-nest-mb-free | timeout: 1, valid: 2 | 9.52699333 | 9.45625413 | failed |
| b-shirts-nest-mb-given | valid: 3 | 8.87179487 | 8.85897436 | 8.90598290 |
| b-shirts-strip-sheet | valid: 3 | 2.71047620 | 2.69933534 | 2.71744048 |
| b-swim-nest-mb-free | valid: 3 | 5.70307189 | 5.63148478 | 5.76047886 |
| b-swim-nest-mb-given | valid: 3 | 5.41155583 | 5.32883191 | 5.48110204 |
| b-swim-strip-sheet | valid: 3 | 2.31618383 | 2.30406947 | 2.36914525 |
| b-trousers-nest-mb-free | valid: 3 | 3.74303568 | 3.70986884 | 3.77381231 |
| b-trousers-nest-mb-given | valid: 3 | 3.31116906 | 3.27422860 | 3.36462408 |
| b-trousers-strip-sheet | valid: 3 | 2.31645570 | 2.29113924 | 2.32278481 |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T004641Z-9dad00a0.json).

16 explicitly named checker-build failures occurred before the competitor started. Their audited records remain in the JSON alongside all replacement outcomes. Solver failures, invalid layouts and timeouts are never replaced by this option.
