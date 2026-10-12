# deepnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

M, 300 s, clearance-safe: 12/12 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| m-box-mini | valid: 3 | 0.72400000 | 0.72400000 | 0.72400000 |
| m-garment-teagan-2 | no_layout: 3 | failed | failed | failed |
| m-mechanical-defective-stock | valid: 3 | 3.32140000 | 3.15680766 | 3.33100000 |
| m-mechanical-mixed-stock | valid: 3 | 1.02072135 | 1.02069110 | 1.02351616 |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T033500Z-e03868ab.json).
