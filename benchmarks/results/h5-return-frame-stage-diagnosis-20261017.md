# Return-frame legality and repair diagnosis — 2026-10-17

**All four diagnostic layouts validate.** These observations locate filters
and repair stages; they do not measure improvement or replace the failed pilot.

The [committed plan](h5-return-frame-stage-diagnosis-20261017/plan.json) fixes
both mechanical jobs, both kerfs, seed zero, 60 seconds and serial CCD0 CPU 8.
Production and the original rejected candidate remain unchanged. Aggregate
tracing preserves decisions but may perturb wall-clock behavior.

| Job | Kerf mm | Attempted exchanges | Complete-set outcomes | Partial-set outcomes | Eligible full-set samples: smaller / equal-or-larger area |
| --- | ---: | ---: | --- | --- | ---: |
| m-mechanical-large-plates | 0.2 | 7 | source_repair_failed: 7 | none | 0 / 197 |
| m-mechanical-large-plates | 1.5 | 6 | source_repair_failed: 6 | none | 0 / 88 |
| m-mechanical-panel-hardware | 0.2 | 6 | source_repair_failed: 6 | none | 0 / 17 |
| m-mechanical-panel-hardware | 1.5 | 4 | source_repair_failed: 4 | none | 0 / 17 |

The complete session takes 4.060 minutes. All four
original-job validations, quantities, metrics, zero reported hole riders
and public exports pass. Every immutable attempt archive passes CRC and
all member hashes; trace attempt/acceptance counts match saved solver counters.
[Full observations](h5-return-frame-stage-diagnosis-20261017/observed-stages.json)
retain sample eligibility, returned-area ratios and both repair losses.
[Frame observations](h5-return-frame-stage-diagnosis-20261017/observed-frames.json)
retain orientation modes, per-mode outcomes and validated material changes.
[Verification](h5-return-frame-stage-diagnosis-20261017/verification.json) binds
source/binaries/inputs to the precommitted plan.

An eligible sample is not proof of a feasible exchange, and a failed repair
is not proof of impossibility. Any new heuristic needs separate authored
correctness checks and a committed comparison. Original H5 conditions,
failed measurements and the reserved split remain unchanged. **60% complete; H2/H5 open.**


## Reviewed result and next question

All **23 complete-set attempts use a permitted reciprocal frame**, with every
hypothetical and actual return orientation allowed. All receiving-sheet repairs
succeed; all return-sheet repairs fail. There are no orientation fallbacks,
partial attempts, accepted exchanges or trials reaching final independent
geometry/material acceptance in these observations. The previously demonstrated
0.0007 mm² guard rejection is not the failure stage here.

Returned area is 2.000000–3.000000 times incoming area. That helps
explain why mapping a group into one vacated part's frame may give repair a hard
starting point, but **does not prove the assignment impossible**: available
source-sheet capacity and every other source pose were not recorded. The next
scope is source capacity and group placement. A balanced exchange of several
parts in both directions needs an independent authored feasibility example
before any new heuristic or performance trial. Original limits remain unchanged.
