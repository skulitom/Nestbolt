# Directed common-line exchange pilot — 2026-10-16

**The exchange candidate does not satisfy H5 and remains isolated.** All 72
attempts are valid, but all four mechanical-job/kerf medians exceed the +1%
material limit. None of the 24 candidate runs records an exchange proposal.
This four-job diagnostic does not complete H5. The full 13-job comparison
remains required, and no original acceptance limit changes. Completed
milestone weight remains 45%.

[Fixed replacement plan](h5-exchange-pilot-v2-20261016/plan.json),
[all results](h5-exchange-pilot-v2-20261016/results.json),
[archive verification](h5-exchange-pilot-v2-20261016/verification.json).

## Method

The isolated candidate exchanges a last-sheet part with a smaller actual
obstruction on an earlier sheet, repairs both sheets, and accepts only after
the independent whole-job geometry/material guard passes. It keeps the
incumbent intact on failure and uses the existing stalled-window budget.
Ordinary mode retains its original path. The source, tests and matched
observers are retained in the [preparation evidence](h5-exchange-pilot-preparation-20261016.md).

Each job/kerf/seed block runs ordinary baseline, common-line baseline and
common-line candidate sequentially on the same physical CCD0 core. Order
rotates; seeds are 0–2, both kerfs are tested, every search gets 60 seconds,
and at most eight blocks run together. Original frozen geometry, quantities,
stocks and rotations are unchanged. Independent validation, public export
and the ban on part-in-hole in common mode are required for a valid outcome.
The complete session took 8.972 minutes.

## Three-seed medians

Positive material differences are worse. The candidate must remain within
+1% of ordinary mode; improving over a failing common-line baseline alone
does not pass that condition. Exchange counts sum all three seeds.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs common baseline | Candidate cut saving | Exchanges / attempts | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.594027% | +4.833618% | -0.720125% | 11.655838% | 0 / 0 | NO |
| m-mechanical-large-plates | 1.5 | +4.173735% | +4.175294% | +0.001497% | 12.714817% | 0 / 0 | NO |
| m-mechanical-panel-hardware | 0.2 | +5.701457% | +5.869406% | +0.158890% | 3.090691% | 0 / 0 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.534846% | +5.492849% | -0.039795% | 5.324076% | 0 / 0 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +0.875951% | +0.939681% | +0.063176% | 22.582155% | 0 / 0 | yes |
| c-bracket-mixed | 1.5 | -1.283469% | -1.086753% | +0.199274% | 20.507871% | 0 / 0 | yes |

## Evidence and limits

Every attempted outcome, including failures, has its own immutable ZIP.
CRC, all member hashes, layout hashes, saved counters and independently
computed metrics/cut savings were checked; the summary is recomputed from
all original records. No valid-only median replaces a failed/incomplete arm.
Source, binary, runner, data and environment guards remain unchanged.

The [scheduling correction](h5-exchange-pilot-v2-preparation-20261016.md)
preserves the original unopened pilot and H4 failure. It changes when an
independent pilot can start, not what qualifies as an H4/H5 pass. Neither
pilot evidence nor an isolated candidate is automatically integrated.

Two subsequent [debug path observations](h5-exchange-path-20261016.md) validate
but contain no exchange call in their timers. The call is behind a repeated-stall
condition; these two trajectories do not reach it. A future experiment can test
the existing bounded initial relocation opportunity. No such scheduling change
is integrated, and the observed material differences cannot be attributed to
successful exchanges when none was attempted.
