# Compatible source-repair reuse pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. The full 13-job comparison and
every original acceptance limit remain required.

[Committed plan](h5-return-reuse-pilot-20261018/plan.json),
[all outcomes](h5-return-reuse-pilot-20261018/results.json),
[archive verification](h5-return-reuse-pilot-20261018/verification.json),
[repair reuse counters](h5-return-reuse-pilot-20261018/reuse-counters.json).

## Method

The isolated candidate retains one best source-sheet repair state within
each exchange invocation. It resumes only when the static container and
original part-object multiset match, all stored poses are permitted and
the saved loss is no worse than the fresh state. Restoring the snapshot
also restores tracker indices; guided-search weights and RNG continue.
Normal mode, proposal caps, repair deadlines, the whole-job acceptance
guard and production remain unchanged. All 90 preceding tests and six
new tests pass; see the [preparation](h5-return-reuse-preparation-20261018.md).

Four frozen jobs, two kerfs and seeds 0–2 produce 72 outcomes across
ordinary baseline, common-line baseline and common-line candidate.
The three arms run sequentially on the same physical CCD0 core in
rotating order; at most eight blocks run together. Each search receives
60 seconds. Frozen geometry, quantities, stock and rotations are unchanged.
The paired blocks, scoring and measurement functions remain AST-identical
to the preceding return-frame pilot. Every output requires independent
public validation and export; common mode must reserve hole interiors.
The session took 8.931 minutes.

## Three-seed medians

Positive material differences are worse. The candidate must remain within
+1% of ordinary mode. Counts sum all three seeds; a reuse is not an
accepted exchange or evidence of material improvement.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs baseline | Cut saving | Accepted / attempted | Reuses | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.606119% | +5.607522% | +0.001329% | 12.033162% | 2 / 13 | 6 | NO |
| m-mechanical-large-plates | 1.5 | +4.985998% | +5.124968% | +0.132370% | 13.738068% | 1 / 23 | 9 | NO |
| m-mechanical-panel-hardware | 0.2 | +6.867012% | +6.668421% | -0.185830% | 4.173532% | 0 / 14 | 11 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.590473% | +5.745273% | +0.146604% | 5.204868% | 0 / 12 | 9 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 | yes |
| c-bracket-mixed | 0.2 | +0.534595% | +2.419752% | +1.875133% | 21.541415% | 4 / 7 | 2 | NO |
| c-bracket-mixed | 1.5 | +0.480601% | +1.016169% | +0.533006% | 21.916840% | 4 / 4 | 0 | NO |

## Evidence and limits

Every attempted outcome, including failures, retains its original ZIP.
CRC, member hashes, layout hashes, counters and independent metrics are
verified. The summary is recomputed from every record; incomplete or
failed arms cannot yield a passing median. Source, binary, runner, inputs
and environment guards remain unchanged.

The earlier [return-frame pilot](h5-return-frame-pilot-20261017.md),
[capacity traces](h5-return-capacity-diagnosis-20261017.md) and
[fixed-assignment witnesses](h5-assignment-repack-20261018.md) are preserved.
Three fixed assignments have independent feasible witnesses; the fourth
remains unresolved. Those diagnostic timings do not establish the minimum
repair time or prove whether this bounded reuse method can satisfy H5.
No relaxed threshold or automatic integration. H2/H5 remain open at 60%.


## Independent hole-reservation check and decision

All 48 common-mode layouts pass the independent filled-outer audit of
133,470 same-sheet pairs. Shapely 2.1.2
transforms each original outer ring and checks disjointness and at least the
requested kerf, with the unchanged 0.00000010 mm
checking tolerance. Minimum clearance slack is 9.99999247131e-07 mm.
No hole interiors are subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** There are 6 failed material pairs out of eight.
m-mechanical-large-plates at 0.2 mm: +5.607522%; m-mechanical-large-plates at 1.5 mm: +5.124968%; m-mechanical-panel-hardware at 0.2 mm: +6.668421%; m-mechanical-panel-hardware at 1.5 mm: +5.745273%; c-bracket-mixed at 0.2 mm: +2.419752%; c-bracket-mixed at 1.5 mm: +1.016169%
The candidate records 11 accepted exchanges from 73 attempts,
with 37 compatible source-repair reuses. Counters alone do not identify
the repair stages that remain unsuccessful, establish causality or prove
impossibility. No unchanged-build rerun, production integration or relaxed
limit follows. H2/H5 remain open; milestone completion stays 60%.
