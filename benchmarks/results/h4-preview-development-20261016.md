# Integrated preview H4: complete original measurement — 2026-10-16

**H4 fails and the preview release remains pending.** All 603 newly measured
layouts are valid, and all 195 reused frozen-v1 outcomes are verified. The
Chrome subset exceeds the original +1% median limit. Every completed outcome,
including Firefox, is retained; no unchanged-build repeat or threshold change
was used. Completed milestone weight remains 45%.

[Full results](h4-preview-development-20261016/results.json),
[artifact verification](h4-preview-development-20261016/verification.json),
[original committed plan](h4-preview-development-20261016/plan.json).

## Fixed method

Product source is the integrated preview at `0a9fb44`. The union of the 65-job
development matrix and eleven-job curve subset contains 67 jobs. Each engine
runs all 67 at 60 seconds and seeds 0–2: 201 native, 201 Chrome and 201 Firefox
attempts. Only 195 frozen-v1 development outcomes are reused, from the verified
preceding archive. No current-build outcome, held-out input or final seed is
substituted. One worker per browser job; eight physical CCD0 cores at most.
Separate builds/tests use CCD1. All source, executable, site, input, runner
and environment guards remain unchanged.

The run took 80.909 minutes, below its four-hour cap.
Every layout hash, requested part count and independent validation result is
checked; saved and standalone metrics agree exactly. The public examples also
pass validation against their original library/request. All six browser
batches exit successfully with zero affinity deviations.

## Full 65-job comparisons

Three-seed job medians; positive differences mean more material. Native uses
the unchanged +0.5% median bound. Browser G5 retains +2% median and total
bounds, also checked for each seed separately.

| Comparison | Median difference | Total difference | Worst job | Result |
| --- | ---: | ---: | ---: | --- |
| Native vs frozen v1 | +0.000000% | +0.108063% | +2.273625% | pass |
| Chrome vs native | +0.242546% | +0.571472% | +3.908865% | pass |
| Firefox vs native | +0.140371% | +0.401506% | +3.770437% | pass |

| Browser | Seed | Median difference | Total difference | Result |
| --- | ---: | ---: | ---: | --- |
| Chrome | 0 | +0.203930% | +0.692891% | pass |
| Chrome | 1 | +0.288641% | +0.624221% | pass |
| Chrome | 2 | +0.030970% | +0.190356% | pass |
| Firefox | 0 | +0.140400% | +0.537144% | pass |
| Firefox | 1 | +0.154760% | +0.482871% | pass |
| Firefox | 2 | +0.020489% | +0.135770% | pass |

## Eleven-job curve subset

The median must be at most +1%, and every job at most +5%. A full G5 pass
does not override a failed subset.

| Browser | Valid | Median difference | Worst job | Total difference | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Chrome | 33/33 | +1.046217% | +3.459929% | +1.440000% | FAIL |
| Firefox | 33/33 | +0.788924% | +3.420673% | +1.002360% | pass |

The earlier [Chrome failure report](h4-preview-chrome-failure-20261016.md)
remains an accurate checkpoint taken while Firefox was running. This report
adds the completed original arm. It does not identify which code change or
source of timing variation caused the observed difference.

## Decision and retained evidence

Do not release this candidate from the failed result. The separately prepared
[score-bound experiment](h4-score-chunks-preparation-20261016.md) must earn its
own evidence; no optimization is accepted from this failure alone. Current
scale checks have not been run on this failed build. The final corrected
candidate still needs full requirements and release verification. H2/H5 remain
open independently, and published v1 claims remain unchanged.

The [raw archive](h4-preview-development-20261016/raw.zip) retains 3,321 members,
9,440,624 bytes, SHA-256 `2fb60ac10d366b28a9db204cfd36bd04f05950b38599a3641476b3f0031d923e`.
It includes all new raw results and validation outputs, original plans,
process/browser metadata, exact native executables and the measured site.
CRC, every member size and every hash were verified against the
[inventory](h4-preview-development-20261016/integrity.json). Reused baseline
bytes remain in their separately verified archive.
