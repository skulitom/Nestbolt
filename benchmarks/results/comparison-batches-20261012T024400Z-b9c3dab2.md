# deepnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

M, 60 s, identical: 90/90 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| m-box-batch-500 | no_layout: 1, valid: 2 | 2.45508197 | 2.42073770 | failed |
| m-box-desktop | valid: 3 | 0.88700000 | 0.88600000 | 0.91450000 |
| m-box-long | valid: 3 | 0.32573770 | 0.32573770 | 0.32573770 |
| m-box-mini | valid: 3 | 0.71600001 | 0.69100001 | 0.71600001 |
| m-box-storage | valid: 3 | 0.53885246 | 0.53885246 | 0.53885246 |
| m-box-tool | valid: 3 | 1.47900000 | 1.47900000 | 1.50500000 |
| m-garment-bruce-1 | valid: 3 | 0.21860407 | 0.21857091 | 0.21985227 |
| m-garment-bruce-2 | valid: 3 | 0.47765410 | 0.47719716 | 0.47963824 |
| m-garment-bruce-3 | no_layout: 2, valid: 1 | failed | failed | failed |
| m-garment-teagan-1 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-2 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-3 | no_layout: 3 | failed | failed | failed |
| m-mechanical-batch-1000 | no_layout: 3 | failed | failed | failed |
| m-mechanical-cog-washers | invalid: 3 | failed | failed | failed |
| m-mechanical-defective-stock | invalid: 2, no_layout: 1 | failed | failed | failed |
| m-mechanical-frame-inserts | invalid: 3 | failed | failed | failed |
| m-mechanical-large-plates | invalid: 3 | failed | failed | failed |
| m-mechanical-mixed-stock | invalid: 3 | failed | failed | failed |
| m-mechanical-mounting-kit | invalid: 3 | failed | failed | failed |
| m-mechanical-panel-hardware | invalid: 3 | failed | failed | failed |
| m-mechanical-remnant-kit | no_layout: 3 | failed | failed | failed |
| m-mechanical-small-brackets | invalid: 3 | failed | failed | failed |
| m-public-gear-1 | no_layout: 3 | failed | failed | failed |
| m-public-gear-2 | no_layout: 3 | failed | failed | failed |
| m-public-gear-3 | no_layout: 2, timeout: 1 | failed | failed | failed |
| m-public-gear-4 | no_layout: 3 | failed | failed | failed |
| m-sign-1 | no_layout: 2, valid: 1 | failed | failed | failed |
| m-sign-2 | no_layout: 3 | failed | failed | failed |
| m-sign-3 | no_layout: 3 | failed | failed | failed |
| m-sign-4 | no_layout: 3 | failed | failed | failed |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T024400Z-b9c3dab2.json).

2 explicitly named harness failures were replaced: input guard or affinity setup before solving, or process cleanup after the budget. Original audited records and all replacement outcomes remain in the JSON. This option rejects solver crashes, invalid layouts, timeouts and no-layout outcomes.
