# Full H4 development comparison — 2026-10-16

**All 780 layouts validate, and every recorded native/browser quality limit passes.**
This completes the 65-job, three-seed comparison for the bounded-score build.
The separate release repair changes the hole collision index and still needs
integration and performance confirmation. H4 closure on the resulting build
remains pending; completed milestone weight stays 45%.

[Full results](h4-full-development-20261015/results.json),
[artifact verification](h4-full-development-20261015/verification.json),
[frozen plan](h4-full-development-20261015/plan.json),
[archive inventory](h4-full-development-20261015/integrity.json).

## Fixed method and coverage

The plan was committed before opening the measurement. All 65 development jobs
use 60-second budgets and seeds 0–2. Frozen v1 executable `75cbb32` is measured
on these development inputs with these seeds; published final/held-out runs and
their seeds are not substituted or reopened. There are 699 new attempts and 81
hash-verified reused outcomes from the identical build’s nine shared subset jobs.
Both browser examples remain covered separately by the eleven-job H4 subset.

Each engine has all 195 required job/seed pairs. Every original-job validation
succeeds with the requested part count and exact agreement between saved and
standalone validation metrics. Every layout hash is checked. No failed, missing
or duplicate attempt is discarded. The six browser batches each contain 56 new
jobs; all exit successfully with zero affinity deviations. One worker per job,
at most eight jobs, physical CCD0 CPUs 0/2/4/6/8/10/12/14. Chrome is
155.0.8059.41 and Firefox is 157.0. Independent builds/tests use CCD1.

The run took 88.799 minutes, below the four-hour session cap.
Source, executable, site, runner, fixture and environment guards remain unchanged.
The environment record retains the unavailable temperature readings: ACPI access
was denied and no hardware-monitor provider was present. Its 4201 MHz observation
is a clock reading, not temperature.

## Three-seed job medians

Positive differences mean more material. The native gate limits the median to
+0.5%; it does not impose a new individual-job bound. Full browser comparisons
retain both original +2% median and +2% total limits.

| Comparison | Valid | Median difference | Total difference | Worst job | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Native vs frozen v1 | 195/195 | +0.000000% | -0.000327% | +2.559175% | pass |
| Chrome vs native | 195/195 | +0.150364% | +0.615913% | +3.720068% | pass |
| Firefox vs native | 195/195 | +0.194317% | +0.755448% | +3.912155% | pass |

The native median is exactly zero, but some individual jobs worsen, by up to
2.559175%. A passing median does not mean every job improves.

## Every original G5 single-seed comparison

All three seeds also pass the unchanged median and total bounds separately.

| Browser | Seed | Median difference | Total difference | Result |
| --- | ---: | ---: | ---: | --- |
| Chrome | 0 | +0.041540% | +0.565911% | pass |
| Chrome | 1 | +0.122383% | +0.548797% | pass |
| Chrome | 2 | +0.049705% | +0.331503% | pass |
| Firefox | 0 | +0.029931% | +0.576123% | pass |
| Firefox | 1 | +0.457900% | +0.905865% | pass |
| Firefox | 2 | +0.049705% | +0.350009% | pass |

## Related evidence and remaining verification

The [eleven-job subset](h4-score-pruning-20261015.md) already passes at this exact
source/binary/site: median +0.710335% Chrome / +0.664508% Firefox, with every job
within +5%. The [current-build scale checks](h4-current-scale-20261015.md) also
pass all four 2,000-part import/nest/export workflows with the documented worker
policy and Quick initial layout settings. Those unchanged records remain linked
rather than being relabelled as newly measured results.

The newly reproduced [CI curve failure](release-readiness-20261016.md) has an
[isolated repair](ci-curve-optimized-profile-20261016.md). Its flat hole index
can affect search cost, so this full result must not be silently transferred to
that modified build. Integration, full regression checks and the affected
performance review remain necessary before the authorized preview release.
The final H4 requirement review will identify which evidence applies to that
build. No comparison to competing tools or fresh final acceptance is claimed.

## Sealed raw evidence

The archive retains 3,928 members, 10,321,737 bytes, SHA-256
`ec3f145a6887c588ca2db09a99a189f11b940cf66a351154d417fff00af1a20a`.
It includes every new search and validation result, plans, browser metadata,
execution logs, snapshots of both native executables and the measured site.
The 81 reused attempts remain bound to the separately verified earlier archive.
CRC, every member size and every member SHA-256 were checked before consolidation.

An initial finalization preflight compared integer in-memory seed keys with
their string keys after JSON storage. It stopped before consolidation. The
corrected verifier applies the same JSON round trip before requiring exact
summary equality. The failed helper and explanation are retained; no numeric
result, threshold or search was changed or repeated.

Product digest: `921ad6f59b0dae0b243ba9cd8e98a03dd4d6a3b6404d4e4251414105f26beb7c`.
Current CLI: `5e07f350761f3b5dfb820e404c85982dacd039d0789b8bfca63f66e76bf20bf7`.
Frozen v1 CLI: `1dd58ac0ef3347af878271f888b7c326045961ba9d959cc4743acbce04b526de`.
WASM: `ac41d7d205813df71c9a5b8648877b1c5170da2654c312a6e3cf5dcc19474cf8`.
