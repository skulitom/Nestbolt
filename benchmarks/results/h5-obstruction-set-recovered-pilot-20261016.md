# Atomic obstruction-set common-line exchange pilot — 2026-10-16

**72/72 attempts are valid.**
This four-job diagnostic does not complete H5. The full 13-job comparison
remains required, and no original acceptance limit changes. This pilot
earns no completed H5 milestone weight.

[Committed obstruction-set plan](h5-obstruction-set-recovered-pilot-20261016/plan.json),
[all results](h5-obstruction-set-recovered-pilot-20261016/results.json),
[archive verification](h5-obstruction-set-recovered-pilot-20261016/verification.json).

## Method

The isolated candidate exchanges a last-sheet part with a smaller actual
obstruction set of up to three parts on an earlier sheet, repairs both sheets,
and accepts only after
the independent whole-job geometry/material guard passes. It keeps the
incumbent intact on failure. The call now runs at the first feasible window
before fill can short-circuit relocation, sharing the existing ten-percent
budget and capped at 1.2 seconds. Ordinary mode retains its original path.
Both matched arms include the current aba989e collision-tree depth change.
The candidate returns all actual blockers together when their combined area
is smaller, preserving relative transforms and the existing single-part
fallbacks. It changes neither budget nor coefficients. Production is unchanged.
Source, tests and matched observers are retained in the
[preparation evidence](h5-obstruction-set-preparation-20261016.md).

Each job/kerf/seed block runs ordinary baseline, common-line baseline and
common-line candidate sequentially on the same physical CCD0 core. Order
rotates; seeds are 0–2, both kerfs are tested, every search gets 60 seconds,
and at most eight blocks run together. Original frozen geometry, quantities,
stocks and rotations are unchanged. Independent validation, public export
and the ban on part-in-hole in common mode are required for a valid outcome.
The complete session took 8.957 minutes.

## Three-seed medians

Positive material differences are worse. The candidate must remain within
+1% of ordinary mode; improving over a failing common-line baseline alone
does not pass that condition. Exchange counts sum all three seeds.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs common baseline | Candidate cut saving | Exchanges / attempts | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.440241% | +4.754489% | -0.650370% | 11.104487% | 3 / 12 | NO |
| m-mechanical-large-plates | 1.5 | +4.574142% | +4.663095% | +0.085062% | 11.581554% | 2 / 21 | NO |
| m-mechanical-panel-hardware | 0.2 | +6.026417% | +5.962959% | -0.059851% | 5.301357% | 0 / 39 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.142400% | +5.771428% | +0.598264% | 5.358518% | 0 / 43 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | -0.987999% | +1.540301% | +2.553529% | 21.555543% | 3 / 6 | NO |
| c-bracket-mixed | 1.5 | +0.826819% | +0.993578% | +0.165392% | 21.110507% | 2 / 26 | yes |

## Evidence and limits

Every attempted outcome, including failures, has its own immutable ZIP.
CRC, all member hashes, layout hashes, saved counters and independently
computed metrics/cut savings were checked; the summary is recomputed from
all original records. No valid-only median replaces a failed/incomplete arm.
Source, binary, runner, data and environment guards remain unchanged.

The [earlier single-blocker pilot](h5-early-exchange-pilot-20261016.md) remains
preserved with 72 valid outcomes, five failed material pairs and ten accepted
exchanges. Separate traces found 35 of 37 proposals fail receiver repair,
with two or three blockers in every attempt. Those traces locate an observed
failure stage; they do not establish infeasibility or a material benefit.
Only this distinct pilot evaluates the complete-group hypothesis on these
development jobs. No quality or material
condition is changed, and no isolated candidate is automatically integrated.

## Integration decision

**Do not integrate this candidate.** Five of eight job/kerf pairs exceed the
original +1% material limit. All four mechanical pairs remain +4.663095% to
+5.962959% above ordinary mode; the mixed-bracket laser pair is +1.540301%.
The candidate records 147 exchange attempts and ten accepted exchanges, with
none accepted on either panel-hardware kerf. Mini-box controls remain unchanged.
These findings do not prove the material target impossible. No unchanged-build
repeat, changed limit or replacement of failed outcomes is justified.

The complete original H5 gate remains open; this four-job pilot cannot replace
its thirteen-job comparison. H4 is complete independently, so completed
v1.1 milestone weight is 60%. The qualified release retains its original
production code and documented common-line limitations. [Decision record](h5-obstruction-set-recovered-pilot-20261016/decision.json).
