# H4 bounded collision-score evaluation — 2026-10-15

Retain bounded scoring. **Both browsers pass the eleven-job quality subset, and
all 99 layouts independently validate.** H4 remains open: full G5, the 195-run
native comparison and current-build scale confirmation are still required.
Completed milestone weight remains 45%, from H1, H3 and H6.

## Change and correctness

The [unchanged-build profiles](h4-browser-profile-20261015.md) identify collision
scoring as the largest sampled cost on letters. The candidate stops computing
an ordinary placed-item collision score once its nonnegative partial sum proves
that the candidate exceeds the incumbent. When the incumbent is collision-free,
any detected collision can be rejected without computing a numeric score.

The pole-pair sum retains the pinned Sparrow reference order, its original final
arithmetic and guided-search weight. The check compares `previous + partial`
directly with the bound; subtracting the previous loss could change rounding at
a tie. Equal scores remain eligible. Infinite bounds use the reference function.
Static hazards and pinned blockers retain their existing scorer. No geometry,
random sequence, work coefficient, deadline, search setting or dependency changes.
The adapted formula is covered by Sparrow's retained MIT copyright and license.

Two new tests compare 5,760 bound combinations against reference score bits and
exercise complete candidate evaluation with ordinary items, a pinned blocker,
sheet boundaries, rotations and reflections. They pass in debug and optimized
builds, along with the existing finite-weight regression.

## Equal-work comparisons

The frozen development jobs letters and gear-1, seeds 0/1, use a 20-work-second
budget and a 120-second real-time ceiling, on physical CCD0 CPUs 8/10. Every
search finishes repeatably. All layouts, search counters, work totals, history
and validation values match the unchanged baseline exactly. Original-job and
public letters-library/request validation pass with no metric difference.

- [Baseline, four layouts](h4-score-replay-20261015T213757Z/results.json): executable
  `ae539d3ac99aaa874c369ad2a7b5f58f94f460f284a93de2a1f7db5381aadaef`.
- [First CLI build, four exact comparisons](h4-score-replay-20261015T214511Z/comparison.json):
  executable `eebbb2f93e16a780c07ec906b99f3fbec177e27dfbbc2b2f63aae69268b85bf6`.
- [Final combined CLI/MCP build, four exact comparisons](h4-score-replay-20261015T215420Z/comparison.json):
  executable `5e07f350761f3b5dfb820e404c85982dacd039d0789b8bfca63f66e76bf20bf7`.

The final build changes the executable hash, so its four comparisons were run
again before the quality measurement. All twelve saved layouts remain valid;
eight candidate-to-baseline comparisons are exact. These short checks do not
establish a speed gain: initial wall differences range from -2.312871% to
+3.216384%; final differences range from -0.768583% to +16.416029%. The final
replay also overlaps browser build/tests on the separate CCD1. All source,
binary and runner guards pass for each replay.

## Checks and fixed measurement

[All seven check stages pass](h4-score-checks-20261015/progress.json): formatting,
strict lint, 297 workspace tests (one existing ignored), three optimized scoring
tests, 26 optimized CLI tests, native CLI/MCP builds, and the WASM/site build with
84 enabled Chromium/Firefox tests (four existing opt-in skips). Builds and tests
use CCD1. The final WASM is 3,528,845 bytes, SHA-256
`ac41d7d205813df71c9a5b8648877b1c5170da2654c312a6e3cf5dcc19474cf8`.

The [frozen measurement plan](h4-score-pruning-20261015/measurement-plan.json)
uses the existing H4 method: eleven development jobs, seeds 0-2, 60 seconds,
native/Chrome/Firefox, one browser worker per job, at most eight physical CCD0
cores. Source, binaries, site and input guards passed throughout measurement.
All optional environment overrides are absent. Every original-job and public
example validation is required; failures cannot be omitted or rounded into a
pass. The ACPI temperature query is denied; the saved 4201 MHz clock observation
does not establish temperature.

## Quality result and limits

The [complete quality record](h4-quality-20261015T215607Z/results.json) passes the
unchanged +1% median/+5% per-job subset limits in both installed Chrome
155.0.8059.41 and Firefox 157.0. Every saved/standalone metric agrees exactly;
all 18 additional public example library/request checks pass. All six browser
batches exit successfully with zero affinity deviations, taking 121.5–122.3 s
each. Source digest: `921ad6f59b0dae0b243ba9cd8e98a03dd4d6a3b6404d4e4251414105f26beb7c`.

| Engine | Valid | Median material vs native | Worst job | Total material vs native | Subset |
| --- | ---: | ---: | ---: | ---: | --- |
| Native | 33/33 | reference | reference | reference | reference |
| Chrome | 33/33 | +0.710335% | +3.316424% | +0.920698% | pass |
| Firefox | 33/33 | +0.664508% | +3.268252% | +1.001898% | pass |

The original Chrome failure at +1.014665% remains preserved. This run replaces
it as the current candidate's subset measurement, without rounding or relaxing
any limit. Full G5 and the 195-run native comparison are not evaluated here;
previous scale passes still need confirmation on this build. H4 stays open.


| Job | Native median | Chrome difference | Firefox difference |
| --- | ---: | ---: | ---: |
| m-mechanical-cog-washers | 1.871525427 | +0.578811% | +0.998869% |
| m-public-gear-1 | 0.939813910 | +3.316424% | +3.268252% |
| m-public-gear-2 | 0.824023990 | -0.010749% | +0.260558% |
| m-public-gear-3 | 0.508578907 | +1.337223% | +1.341053% |
| m-public-gear-4 | 0.552170088 | +0.341136% | +0.104556% |
| m-sign-1 | 0.717682980 | +0.942036% | +0.278884% |
| m-sign-2 | 0.573564910 | +0.710335% | +1.340604% |
| m-sign-3 | 0.138205734 | +1.752242% | +1.329283% |
| m-sign-4 | 0.320910648 | +1.042902% | +0.664508% |
| example-letters | 0.278024417 | -0.074765% | +0.055366% |
| example-gears | 0.938968355 | +0.379673% | +0.427230% |

## Diagnostics and retained evidence

A [historical seed-0 comparison](h4-score-pruning-20261015/historical-comparison.json)
against the prior unchanged-source thin-LTO browser runs gives median material
changes of -0.045601% for Chrome and +0.045622% for Firefox. Median charged-work
rate changes are +8.149475% and +0.698009%. These are trajectory-dependent,
single-seed diagnostics, not isolated kernel throughput or a general speed claim.
The three-seed native-relative table above supplies the subset decision.

All [verification checks](h4-score-pruning-20261015/checks.json) pass, including
all 1,181 frozen inventory hashes. No held-out geometry, final published v1 run,
release or registry state changes. The prior main product checkpoint `3fe8f96`
passed all six CI jobs; this source change receives its own CI run when pushed.

The [raw archive](h4-score-pruning-20261015/raw.zip) retains 740 members,
2,288,713 bytes, SHA-256
`0e56105353c99ccdf3e514f4c861f0befe9f3a894a732890d74557b5a5527581`.
It includes every quality and equal-work result, validation, build/test log,
measured site, candidate source and runner snapshot. CRC, member sizes and every
SHA-256 were checked before consolidating loose raw files; the
[integrity inventory](h4-score-pruning-20261015/integrity.json) refers to those
original archived bytes. Summary JSON remains directly accessible.

An initial report-assembly error treated the prior archive's list inventory as
a dictionary. Its helper and error record are retained; correction reads that
inventory by path without changing any measurement or repeating a search.
The separate profile archive retains the original sampling coverage gap.
