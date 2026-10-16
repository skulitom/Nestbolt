# Early directed common-line exchange pilot — 2026-10-16

**72/72 attempts are valid.**
This four-job diagnostic does not complete H5. The full 13-job comparison
remains required, and no original acceptance limit changes. Completed
milestone weight remains 45%.

[Committed early-call plan](h5-early-exchange-pilot-20261016/plan.json),
[all results](h5-early-exchange-pilot-20261016/results.json),
[archive verification](h5-early-exchange-pilot-20261016/verification.json).

## Method

The isolated candidate exchanges a last-sheet part with a smaller actual
obstruction on an earlier sheet, repairs both sheets, and accepts only after
the independent whole-job geometry/material guard passes. It keeps the
incumbent intact on failure. The call now runs at the first feasible window
before fill can short-circuit relocation, sharing the existing ten-percent
budget and capped at 1.2 seconds. Ordinary mode retains its original path.
The current 7eba929 baseline and candidate both include the finer score bound.
Source, tests and matched observers are retained in the
[preparation evidence](h5-early-exchange-preparation-20261016.md).

Each job/kerf/seed block runs ordinary baseline, common-line baseline and
common-line candidate sequentially on the same physical CCD0 core. Order
rotates; seeds are 0–2, both kerfs are tested, every search gets 60 seconds,
and at most eight blocks run together. Original frozen geometry, quantities,
stocks and rotations are unchanged. Independent validation, public export
and the ban on part-in-hole in common mode are required for a valid outcome.
The complete session took 8.915 minutes.

## Three-seed medians

Positive material differences are worse. The candidate must remain within
+1% of ordinary mode; improving over a failing common-line baseline alone
does not pass that condition. Exchange counts sum all three seeds.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs common baseline | Candidate cut saving | Exchanges / attempts | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.469806% | +5.324324% | -0.137936% | 12.213433% | 3 / 4 | NO |
| m-mechanical-large-plates | 1.5 | +5.406810% | +6.390250% | +0.932995% | 12.528010% | 2 / 18 | NO |
| m-mechanical-panel-hardware | 0.2 | +6.524167% | +6.235856% | -0.270652% | 6.651442% | 0 / 40 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.647621% | +5.584986% | -0.059286% | 5.785155% | 0 / 40 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +0.122582% | +1.251430% | +1.127467% | 21.733206% | 3 / 51 | NO |
| c-bracket-mixed | 1.5 | +0.173380% | +0.178205% | +0.004817% | 21.381623% | 2 / 26 | yes |

## Integration decision

Do not integrate this candidate. Earlier calling makes the experiment reachable:
179 proposals are attempted and 10 accepted. It does not meet the material guard.
All four mechanical/kerf pairs still fail (+5.324324% to +6.390250%); the laser
bracket control also regresses to +1.251430% versus ordinary mode. The 13-job
acceptance matrix is therefore not started. [Assessment](h5-early-exchange-pilot-20261016/assessment.json)
records this decision. Inspect geometry or failed repair stages before another
candidate; do not repeat this unchanged pilot or relax its budget/material limit.

## Evidence and limits

Every attempted outcome, including failures, has its own immutable ZIP.
CRC, all member hashes, layout hashes, saved counters and independently
computed metrics/cut savings were checked; the summary is recomputed from
all original records. No valid-only median replaces a failed/incomplete arm.
Source, binary, runner, data and environment guards remain unchanged.

The [earlier late-call pilot](h5-exchange-pilot-v2-20261016.md) remains
preserved with 72 valid outcomes, four failed mechanical material pairs
and zero attempted exchanges. The targeted authored window test proves
early-call reachability; only this measured pilot establishes whether it
reaches useful proposals on these development jobs. No quality or material
condition is changed, and no isolated candidate is automatically integrated.
