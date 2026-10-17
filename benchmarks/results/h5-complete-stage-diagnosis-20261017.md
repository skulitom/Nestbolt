# Complete-set eligibility and repair diagnosis — 2026-10-17

**All four diagnostic layouts validate.** These observations locate filters
and repair stages; they do not measure improvement or replace the failed pilot.

The [committed plan](h5-complete-stage-diagnosis-20261017/plan.json) fixes
both mechanical jobs, both kerfs, seed zero, 60 seconds and serial CCD0 CPU 8.
Production and the original rejected candidate remain unchanged. Aggregate
tracing preserves decisions but may perturb wall-clock behavior.

| Job | Kerf mm | Attempted exchanges | Complete-set outcomes | Partial-set outcomes | Eligible full-set samples: smaller / equal-or-larger area |
| --- | ---: | ---: | --- | --- | ---: |
| m-mechanical-large-plates | 0.2 | 7 | source_repair_failed: 7 | none | 0 / 197 |
| m-mechanical-large-plates | 1.5 | 7 | source_repair_failed: 7 | none | 0 / 196 |
| m-mechanical-panel-hardware | 0.2 | 4 | source_repair_failed: 4 | none | 0 / 17 |
| m-mechanical-panel-hardware | 1.5 | 5 | source_repair_failed: 5 | none | 0 / 17 |

The complete session takes 4.054 minutes. All four
original-job validations, quantities, metrics, zero reported hole riders
and public exports pass. Every immutable attempt archive passes CRC and
all member hashes; trace attempt/acceptance counts match saved solver counters.
[Full observations](h5-complete-stage-diagnosis-20261017/observed-stages.json)
retain sample eligibility, returned-area ratios and both repair losses.
[Verification](h5-complete-stage-diagnosis-20261017/verification.json) binds
source/binaries/inputs to the precommitted plan.

An eligible sample is not proof of a feasible exchange, and a failed repair
is not proof of impossibility. Any new heuristic needs separate authored
correctness checks and a committed comparison. Original H5 conditions,
failed measurements and the reserved split remain unchanged. **60% complete; H2/H5 open.**


## Observed bottleneck

All 23 actual attempts are complete sets. Receiving-sheet repair succeeds in
every attempt; returning the displaced group to the last sheet fails in all 23
within the unchanged repair budget. No partial sets are attempted and no
exchanges are accepted in these four traces. Sampling observes 427 eligible
complete sets with equal or larger combined area and zero smaller complete sets.

The next concrete investigation is return-group initialization and repair within
the existing constraints. These observations establish neither sufficient room
for a successful exchange nor mathematical impossibility. Changing more search
time or replaying the same candidate is not supported by this evidence. The
failed paired pilot remains the quality result; production remains unchanged.
