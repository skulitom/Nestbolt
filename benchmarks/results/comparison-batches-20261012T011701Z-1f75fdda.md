# svgnest: three-seed development comparison

Development comparison slice, not a complete M1 or final quality gate. All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.

M, 60 s, identical: 90/90 attempts audited.

| Job | Outcomes | Median | Q1 | Q3 |
| --- | --- | ---: | ---: | ---: |
| m-box-batch-500 | no_layout: 3 | failed | failed | failed |
| m-box-desktop | no_layout: 3 | failed | failed | failed |
| m-box-long | no_layout: 3 | failed | failed | failed |
| m-box-mini | no_layout: 2, valid: 1 | failed | failed | failed |
| m-box-storage | no_layout: 3 | failed | failed | failed |
| m-box-tool | no_layout: 3 | failed | failed | failed |
| m-garment-bruce-1 | no_layout: 3 | failed | failed | failed |
| m-garment-bruce-2 | no_layout: 3 | failed | failed | failed |
| m-garment-bruce-3 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-1 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-2 | no_layout: 3 | failed | failed | failed |
| m-garment-teagan-3 | no_layout: 3 | failed | failed | failed |
| m-mechanical-batch-1000 | no_layout: 3 | failed | failed | failed |
| m-mechanical-cog-washers | no_layout: 3 | failed | failed | failed |
| m-mechanical-defective-stock | unsupported: 3 | failed | failed | failed |
| m-mechanical-frame-inserts | no_layout: 3 | failed | failed | failed |
| m-mechanical-large-plates | no_layout: 3 | failed | failed | failed |
| m-mechanical-mixed-stock | unsupported: 3 | failed | failed | failed |
| m-mechanical-mounting-kit | no_layout: 3 | failed | failed | failed |
| m-mechanical-panel-hardware | no_layout: 3 | failed | failed | failed |
| m-mechanical-remnant-kit | unsupported: 3 | failed | failed | failed |
| m-mechanical-small-brackets | no_layout: 3 | failed | failed | failed |
| m-public-gear-1 | no_layout: 3 | failed | failed | failed |
| m-public-gear-2 | no_layout: 3 | failed | failed | failed |
| m-public-gear-3 | no_layout: 3 | failed | failed | failed |
| m-public-gear-4 | no_layout: 3 | failed | failed | failed |
| m-sign-1 | no_layout: 3 | failed | failed | failed |
| m-sign-2 | no_layout: 3 | failed | failed | failed |
| m-sign-3 | no_layout: 3 | failed | failed | failed |
| m-sign-4 | no_layout: 3 | failed | failed | failed |

Metric: original-polygon strip length for S, normalized material for B/M. This explicitly selected batch set retains runner and validator versions per attempt; it does not establish a frozen final comparison.

[Full precision, selection and audited evidence](comparison-batches-20261012T011701Z-1f75fdda.json).

7 explicitly named checker-build failures occurred before the competitor started. Their audited records remain in the JSON alongside all replacement outcomes. Solver failures, invalid layouts and timeouts are never replaced by this option.

6 explicitly named harness failures were replaced: input guard or affinity setup before solving, or process cleanup after the budget. Original audited records and all replacement outcomes remain in the JSON. This option rejects solver crashes, invalid layouts, timeouts and no-layout outcomes.
