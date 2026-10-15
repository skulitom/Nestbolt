# Preview readiness: retained curve-search failure

On 2026-10-16 (London), release preparation found a new failure in the Linux
checks for `e897e91182e2e5b457f905a92c05465c0efa8ea8`:
[CI job 116712070745](https://github.com/skulitom/Nestbolt/actions/runs/38819422170/job/116712070745),
run 38819422170. The failed test is
`random_curved_svg_parts_nest_validly`; the log retains its shrunk input and
random-generation seed. This is a release blocker, not a rerun to discard.

The exact generated drawing has three rings, a narrow ellipse and an arc lens.
Ring tuples `(radius, hole offset, quantity)` are
`(12.478479167719012, 0, 1)`, `(2.6805745106261756, 0, 2)` and
`(13.120391613622374, 0, 1)`; `rx=2`, `ry=5.610405755197782`,
`bulge=0.1`, search seed `659`. The request retains the test's 120 × 80 mm stock,
2 mm margins, 0.5 mm spacing and two-second deterministic work budget.

A standalone Windows debug harness imports that drawing and calls the public
search API without changing production files. It reproduces the same assertion
at jagua-rs 1.1.0 `qt_traits.rs:122`: quadrant classification is
`[true, true, true, false]` while the dependency's f64 oracle reports
`[true, false, true, true]`. The retained stack reaches this predicate from
Sparrow's placement evaluator during Nestbolt's part-in-hole grouping pass.
The evidence establishes a crash in checked builds and a non-conservative
classification; it does not establish that a returned production layout is
invalid. The repair still needs verification.

The existing optimized CLI was also run once against the exact saved polygon
job with the same seed and work budget, followed by its standalone validator.
Both commands exit successfully: all eight copies are placed, independent
validation passes and reported metrics agree exactly. Its executable SHA-256 is
`5e07f350761f3b5dfb820e404c85982dacd039d0789b8bfca63f66e76bf20bf7`.
This functional check runs on CCD1 CPU 16 and is not a timing measurement.
It does not repair the non-conservative query or replace the failed checked-build
test. The optimized CLI has debug assertions disabled, so its successful result
does not establish that the dependency predicate is correct.

The first standalone harness build failed because it also tried to call a
private dependency trait directly. Its source and compiler failure remain
preserved. The corrected harness removes only that private-API probe; it builds
successfully and exits 101 on the reproduced search assertion. Neither result
is reported as a pass. Source and binary guards for the live H4 comparison match
before and after both attempts.

Raw evidence is in [release-readiness-20261016](release-readiness-20261016/):
the CI log, both harness sources and execution records, compiler output,
reproduced SVG, public polygon job, stack trace, optimized CLI layout and its
independent validation. The CI log SHA-256 is
`4ab4458638c7876baa9a50060233bf38dc8f0dc3beab7c2ee6a8d67c8aeebadc`.
The successful build's search stderr SHA-256 is
`56fac0b69135219656256939e9aaf999b0c5f232a6d713df65d8959ad663d502`.

This is functional failure diagnosis on CCD1, not a benchmark or held-out
evaluation. No production source, dependency, measured executable or browser
build changed. No milestone weight changes. See
[release readiness](../../docs/RELEASE_READINESS.md) for the remaining release
checks and approved scope.
