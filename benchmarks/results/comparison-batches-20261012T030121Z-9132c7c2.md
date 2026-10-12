# deepnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

M, 60 s, clearance-safe: 90/90 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| m-box-batch-500 | no_layout: 2, valid: 1 | failed | failed | failed |
| m-box-desktop | valid: 3 | 0.94500000 | 0.94500000 | 0.94500000 |
| m-box-long | valid: 3 | 0.32704918 | 0.32704918 | 0.32704918 |
| m-box-mini | valid: 3 | 0.77400000 | 0.76300000 | 0.78050000 |
| m-box-storage | valid: 3 | 0.54016393 | 0.54016393 | 0.54016393 |
| m-box-tool | valid: 3 | 1.47900000 | 1.45600000 | 1.47900000 |
| m-garment-bruce-1 | valid: 3 | 0.22518335 | 0.22481910 | 0.22693502 |
| m-garment-bruce-2 | valid: 3 | 0.48774992 | 0.48380252 | 0.49490312 |
| m-garment-bruce-3 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-1 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-2 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-3 | no_layout: 3 | failed | failed | failed |
| m-mechanical-batch-1000 | no_layout: 3 | failed | failed | failed |
| m-mechanical-cog-washers | valid: 3 | 2.18250000 | 2.18250000 | 2.18250000 |
| m-mechanical-defective-stock | no_layout: 2, valid: 1 | failed | failed | failed |
| m-mechanical-frame-inserts | valid: 3 | 0.62253933 | 0.61959317 | 0.62316564 |
| m-mechanical-large-plates | valid: 3 | 1.23966667 | 1.22716667 | 1.24163990 |
| m-mechanical-mixed-stock | valid: 3 | 1.02845061 | 1.02515035 | 1.03310206 |
| m-mechanical-mounting-kit | valid: 3 | 2.79208828 | 2.76676175 | 2.79307543 |
| m-mechanical-panel-hardware | valid: 3 | 1.73985619 | 1.73510791 | 1.75633437 |
| m-mechanical-remnant-kit | no_layout: 3 | failed | failed | failed |
| m-mechanical-small-brackets | valid: 3 | 6.67000000 | 6.65000000 | 6.72500000 |
| m-public-gear-1 | no_layout: 3 | failed | failed | failed |
| m-public-gear-2 | no_layout: 3 | failed | failed | failed |
| m-public-gear-3 | no_layout: 3 | failed | failed | failed |
| m-public-gear-4 | no_layout: 3 | failed | failed | failed |
| m-sign-1 | valid: 3 | 0.94477330 | 0.92717096 | 0.94636743 |
| m-sign-2 | no_layout: 3 | failed | failed | failed |
| m-sign-3 | no_layout: 3 | failed | failed | failed |
| m-sign-4 | no_layout: 2, timeout: 1 | failed | failed | failed |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T030121Z-9132c7c2.json).
