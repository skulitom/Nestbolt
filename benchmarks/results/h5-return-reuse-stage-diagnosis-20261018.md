# Source-repair reuse stages — 2026-10-18

**All four diagnostic layouts validate.** These observations locate repair
and acceptance stages. They do not measure improvement or replace the
failed 72-outcome comparison.

The [committed plan](h5-return-reuse-stage-diagnosis-20261018/plan.json)
uses both mechanical jobs, both kerfs, seed zero, 60 seconds and serial
physical CCD0 CPU 8. Production and the rejected candidate are unchanged.
Read-only tracing preserves decisions but can perturb wall deadlines.

| Job | Kerf mm | Attempts | Reuses | Outcomes after reuse | Other outcomes |
| --- | ---: | ---: | ---: | --- | --- |
| m-mechanical-large-plates | 0.2 | 7 | 4 | source_repair_failed: 4 | source_repair_failed: 3 |
| m-mechanical-large-plates | 1.5 | 8 | 5 | source_repair_failed: 5 | source_repair_failed: 3 |
| m-mechanical-panel-hardware | 0.2 | 5 | 4 | source_repair_failed: 4 | source_repair_failed: 1 |
| m-mechanical-panel-hardware | 1.5 | 4 | 3 | source_repair_failed: 3 | source_repair_failed: 1 |

The session takes 4.065 minutes. Original quantities,
independently recomputed metrics, public exports and zero reported hole
riders pass. Every original ZIP passes CRC and member/hash checks. Trace
attempt, acceptance and reuse counts match the saved solver counters.
Reused attempts preserve the prior inventory and best unweighted loss
within the same invocation, and start no worse than the fresh alternative.

There are 16 reused source attempts; 7
reduce their initial loss and 0 finish with zero source loss.
A zero internal loss still requires whole-job geometry and material checks.

[Source loss/time observations](h5-return-reuse-stage-diagnosis-20261018/observed-reuse.json)
retain every fresh/resumed repair, inventory, loss, available budget and
elapsed duration. [All stages](h5-return-reuse-stage-diagnosis-20261018/observed-stages.json)
and [frames](h5-return-reuse-stage-diagnosis-20261018/observed-frames.json)
retain sampling and orientation context. The
[verification](h5-return-reuse-stage-diagnosis-20261018/verification.json)
binds the results to the unchanged source, binary and input guards.

Failed finite repairs do not establish impossibility. Observed repair
durations are not minimum required times, and losses are not quality scores.
Any new candidate needs separate correctness checks and a committed paired
comparison. No gate change, integration or reserved-input access.
**H2/H5 remain open; completed weight stays 60%.**


## Interpretation and next constraint

All 24 complete-obstruction exchanges repair the receiver, then fail source
repair. Sixteen resume a compatible saved state; seven reduce loss further,
none reaches zero, and none reaches final material/geometry acceptance.
The reader verifies original inventories and exact restored loss across each
reuse. The issue is incomplete repair, not observed cache-state corruption.

Each case spends 0.903–1.054 seconds in source repairs within the existing
early-call budget. Available windows shrink after successive attempts; three
late attempts reach source repair with an already-expired pair deadline and
return their unchanged state. These observed durations are not minimum required
repair times and do not prove that a larger allowance would solve H5.

The prior fixed-assignment witnesses and balanced two-to-three authored
exchange remain distinct evidence. Continuing one failed assignment longer
and changing the incoming group are separate hypotheses; the current cache
does neither. The next search change should alter the assignment or its repair
strategy with authored correctness checks and a new committed comparison,
while retaining the original whole-job budget and acceptance limits.
