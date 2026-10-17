# Atomic-set proposal and repair diagnosis — 2026-10-17

**All four diagnostic layouts validate.** These observations locate filters
and repair stages; they do not measure improvement or replace the failed pilot.

The [committed plan](h5-obstruction-stage-diagnosis-20261017/plan.json) fixes
both mechanical jobs, both kerfs, seed zero, 60 seconds and serial CCD0 CPU 8.
Production and the original rejected candidate remain unchanged. Aggregate
tracing preserves decisions but may perturb wall-clock behavior.

| Job | Kerf mm | Attempted exchanges | Complete-set outcomes | Partial-set outcomes | Full-set samples accepted/rejected by area filter |
| --- | ---: | ---: | --- | --- | ---: |
| m-mechanical-large-plates | 0.2 | 3 | none | receiver_repair_failed: 2, accepted: 1 | 0 / 88 |
| m-mechanical-large-plates | 1.5 | 8 | none | receiver_repair_failed: 7, accepted: 1 | 0 / 195 |
| m-mechanical-panel-hardware | 0.2 | 6 | none | receiver_repair_failed: 6 | 0 / 107 |
| m-mechanical-panel-hardware | 1.5 | 12 | none | receiver_repair_failed: 12 | 0 / 230 |

The complete session takes 4.054 minutes. All four
original-job validations, quantities, metrics, zero reported hole riders
and public exports pass. Every immutable attempt archive passes CRC and
all member hashes; trace attempt/acceptance counts match saved solver counters.
[Full observations](h5-obstruction-stage-diagnosis-20261017/observed-stages.json)
retain sample eligibility, returned-area ratios and both repair losses.
[Verification](h5-obstruction-stage-diagnosis-20261017/verification.json) binds
source/binaries/inputs to the precommitted plan.

A rejected sample is not proof of a feasible exchange, and a failed repair
is not proof of impossibility. Any new heuristic needs separate authored
correctness checks and a committed comparison. Original H5 conditions,
failed measurements and the reserved split remain unchanged. **60% complete; H2/H5 open.**
