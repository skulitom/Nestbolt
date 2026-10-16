# Isolated eight-pair score-bound probe — 2026-10-16

**The eleven-job subset passes its unchanged limits.**
This is an isolated candidate, not an integrated release or complete H4 gate.
Completed milestone weight remains 45%. The original preview failure is
preserved and no unchanged-build trial was repeated.

[Fixed plan](h4-score-chunks-probe-20261016/plan.json),
[complete results](h4-score-chunks-probe-20261016/results.json),
[artifact verification](h4-score-chunks-probe-20261016/verification.json).

## Correctness and method

Only exact-bound check granularity changes: check after eight pole pairs
rather than an entire row. [Preparation checks](h4-score-chunks-preparation-20261016.md)
cover reference score bits, ties, complete evaluation, long/partial chunks,
optimized builds and strict lint. No geometry, score arithmetic, accumulation
order, work charge, default, deadline or dependency changes.

Before quality measurement, all eight fixed-work native runs validate.
Four baseline/candidate pairs retain the entire result except actual elapsed
wall time, including layouts, counters, history, accepted-at time and metrics.
Their median wall difference is +0.204357%.
These short, baseline-first pairs do not establish a speed gain.

The quality plan uses the same eleven development jobs, seeds 0–2 and
60-second budgets in native, installed Chrome and Firefox. It runs once,
with one worker per browser job and at most eight physical CCD0 cores.
The unchanged root CLI independently validates every output, including the
actual public library/request for both examples. Source, binary, site, input,
runner and environment guards remain unchanged. No held-out geometry is read.
The session took 18.605 minutes.

## Subset result

The original limits are +1% median material and +5% for every job versus
native, using the median of each job’s three seeds.

| Browser | Valid | Median difference | Worst job | Total difference | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Chrome | 33/33 | +0.378238% | +3.103068% | +0.793854% | pass |
| Firefox | 33/33 | +0.432882% | +2.969688% | +0.497120% | pass |

| Job | Native median | Chrome difference | Firefox difference |
| --- | ---: | ---: | ---: |
| m-mechanical-cog-washers | 1.892581830 | -0.434589% | -0.438119% |
| m-public-gear-1 | 0.940156535 | +3.103068% | +0.079427% |
| m-public-gear-2 | 0.823208955 | +0.359091% | +0.269679% |
| m-public-gear-3 | 0.509175120 | +1.061289% | +1.044135% |
| m-public-gear-4 | 0.551950188 | +0.378238% | +0.015620% |
| m-sign-1 | 0.717860665 | +0.189449% | +0.432882% |
| m-sign-2 | 0.578875570 | +0.266965% | +0.437464% |
| m-sign-3 | 0.137587174 | +1.576464% | +1.265711% |
| m-sign-4 | 0.321070256 | +0.741238% | +0.912595% |
| example-letters | 0.284094290 | -1.862612% | -0.048741% |
| example-gears | 0.943861885 | +2.921093% | +2.969688% |

## Limits and retained evidence

A [historical diagnostic](h4-score-chunks-probe-20261016/historical-diagnostics.json)
compares charged-work rates and material against the original preview on the
same jobs/seeds. Search trajectories and wall-time conditions differ, so those
rates are not isolated kernel throughput or a general speed claim.

The full 65-job G5/native matrix, scale confirmation and final integration
checks remain separate. This subset does not complete H4 or authorize a new
public comparison. H2 and H5 remain open independently.

The [raw archive](h4-score-chunks-probe-20261016/raw.zip) retains 651 members,
832,260 bytes, SHA-256 `2d5119357e95a0dc5c6681a5c902a9c6028e784fff3f26a4b83083adbb3fd911`.
CRC, every member size and hash were verified. Exact candidate binaries,
source and site remain bound to the separately verified preparation archive;
the original baseline is retained in the complete preview archive.
