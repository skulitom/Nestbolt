# Benchmark groundwork

Run `python scripts/smoke.py` for two sequential five-second Sparrow runs. The
first invocation builds the pinned native executable with four compilation jobs.
Subsequent invocations reuse it. Outputs are never overwritten. Each run sets
`--workers 1` and `RAYON_NUM_THREADS=1`. Full sessions remain local; keep below
eight concurrent runs and about four hours. Artem waived the temperature-monitoring
prerequisite for this project on 2026-10-11; bounded concurrency remains in place.

`smoke.json` freezes generated MIT fixtures and the current Sparrow revision.
`locks/sparrow.Cargo.lock` freezes its transitive dependencies, which upstream
does not commit. The tool's full source, notices and licence remain in its ignored
checkout under `.cache/upstream/sparrow`. No benchmark datasets have been imported
or relicensed from that checkout. Use `--verify-only` to check fixtures offline.

## M0 reproduction complete

Sparrow's published runs use historical source revisions, dated nightly compilers,
SIMD flags and run-specific seeds. The current stable build smoke is a separate
integration check. The historical source, compiler, timing and 39-run matrix are
frozen in [the reproduction method](sparrow-repro/README.md). Experiment
`published-20261011` completed all 39 runs. Every layout passes independent
validation and all 13 means meet the predeclared 1% threshold;
the worst absolute difference is 0.986671%.
See [the complete reproduction](results/m0-published-20261011T215820Z-10a30c6f.md).

## M1 baseline complete

- Independent layout validation and polygon contracts are implemented. All four
  competitor output adapters use the same original-geometry checker.
- [13 S, 35 B and 40 M jobs](datasets/README.md) are frozen and checked;
  ten M jobs are reserved for final acceptance and excluded from tuning.
- [LBF](lbf/README.md), [SVGnest](svgnest/README.md),
  [Deepnest](deepnest/README.md) and [current Sparrow](sparrow-benchmark/README.md)
  have automated runners, bounded sessions and audited three-seed reports for
  identical constraints and the declared best native settings.
- [Statistics](STATISTICS.md) define 60/300-second populations, medians/IQR,
  failed outcomes, tie tolerance and the baseline-gap formula. Failed or missing
  competitor output never earns a free win.
- [Mixed-stock material scoring](../docs/SCORING.md) uses original geometry.
  Final acceptance seeds and held-out reservations are fixed in
  [the matrix plan](matrix-plan.json); final runner/configuration hashes will be
  sealed before acceptance runs.

The [M1 completion audit](../docs/M1_BASELINE.md) covers all 1,878 declared slots
and links the complete gap table and frozen target.
See [current completion and evidence](../docs/STATUS.md). Per-run raw records and
all earlier experiments remain linked from [the append-only log](../BENCHMARKS.md).

The current runner's `completed_unvalidated` status is deliberately ineligible for
any quality claim. A fixed seed and wall-clock budget do not promise bitwise repeatability.
