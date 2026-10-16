# Integrated score-bound preview: full H4 comparison — 2026-10-16

**At least one quality condition fails; do not release from this result.**
All 603 new layouts and 195 reused frozen-v1 layouts validate. These are
the originally planned outcomes for candidate `7eba929`; no unchanged-build
repeat, changed threshold or selected subset replaces a failed observation.
Scale and complete requirement review are separate, so this report alone
does not close H4 or change completed milestone weight.

[Results](h4-preview-score-release-20261016/results.json), [verification](h4-preview-score-release-20261016/verification.json),
[committed plan](h4-preview-score-release-20261016/plan.json).

## Method

The union of 65 development jobs and the eleven-job curve subset contains
67 jobs. Native, Chrome and Firefox each run all 67 at 60 seconds and seeds
0–2, giving 201 outcomes per engine. Only the 195 sealed frozen-v1 outcomes
are reused. There are no held-out jobs, final seeds or competitor claims.
One browser worker per job, at most eight physical CCD0 cores; separate
functional checks/builds use CCD1. Source, executable, site, runner, inputs
and environment guards stay unchanged.

The complete run took 80.939 minutes, below its four-hour cap.
Every layout hash, requested quantity and independent metric is checked.
Standalone and saved metrics agree exactly, including original-library
validation of the public examples. All six browser batches succeed with
zero affinity deviations.

## Full development comparisons

Positive differences mean more material. Three-seed job medians are used.
Native retains +0.5% median; browser G5 retains +2% median and total, also
checked separately for each seed.

| Comparison | Median | Total | Worst job | Result |
| --- | ---: | ---: | ---: | --- |
| Native vs frozen v1 | +0.000681% | +0.126176% | +1.695733% | pass |
| Chrome vs native | +0.091358% | +0.384971% | +3.451003% | pass |
| Firefox vs native | +0.026372% | +0.346902% | +3.455178% | pass |

| Browser | Seed | Median | Total | Result |
| --- | ---: | ---: | ---: | --- |
| Chrome | 0 | +0.006427% | +0.307758% | pass |
| Chrome | 1 | +0.090711% | +0.210789% | pass |
| Chrome | 2 | +0.147234% | +0.415277% | pass |
| Firefox | 0 | +0.006282% | +0.046756% | pass |
| Firefox | 1 | +0.075173% | +0.297410% | pass |
| Firefox | 2 | +0.046369% | +0.295262% | pass |

## Curve subset

Both browsers must stay at or below +1% median and +5% for every job.

| Browser | Valid | Median | Worst job | Total | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Chrome | 33/33 | +1.032679% | +3.320700% | +1.247775% | FAIL |
| Firefox | 33/33 | +0.881781% | +3.234662% | +1.070231% | pass |

## Retained evidence and next step

The original `0a9fb44` [failed comparison](h4-preview-development-20261016.md)
remains preserved. This candidate checks bounds after eight pole pairs
instead of only after a whole row, preserving exact finite-bound arithmetic
and equal-score behavior. Its [fixed-work and subset checks](h4-score-chunks-probe-20261016.md)
and [integrated application checks](h4-score-integration-20261016.md) are separate evidence.
No general speed gain follows from these wall-clock quality outcomes.

Investigate the failed condition before further release work; retain these results unchanged.
H2/H5 remain open independently. No tag, release or registry entry is created
by this report, and frozen v1 claims remain unchanged.

The [raw archive](h4-preview-score-release-20261016/raw.zip) contains 3,319 members,
9,459,175 bytes, SHA-256 `0c6530d8f0dc69b91eac3afc6e66a71a0763a83a682e3ba4cbc4e7cbab83b2fe`.
It preserves every new attempt, validation, original plan, browser/process
record and exact measured engine/site. CRC, member size and SHA-256 checks
all pass. Reused v1 bytes remain in their verified preceding archive.
