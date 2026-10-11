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

## M0 reproduction in progress

Sparrow's published runs use historical source revisions, dated nightly compilers,
SIMD flags and run-specific seeds. The current stable build smoke is a separate
integration check. The historical source, compiler, timing and 39-run matrix are
frozen in [the reproduction method](sparrow-repro/README.md). Experiment
`published-20261011` is running; partial results do not close M0.

## Required for M1

- Independent layout validation and polygon contracts are implemented; remaining
  competitor output adapters must use the same checker.
- [13 S, 35 B and 40 M jobs](datasets/README.md) are frozen and checked;
  ten M jobs are reserved for final acceptance and excluded from tuning.
- [LBF](lbf/README.md) has a valid first B batch. The [SVGnest runner](svgnest/README.md)
  has a 24-job pilot with 23 independently valid layouts after a documented export
  precision correction. The [Deepnest runner](deepnest/README.md) passes real
  spacing and mixed-stock smoke checks; startup stability, full batches and best
  settings remain pending. Complete the applicable Sparrow adapter.
- 60/300-second budgets, seed matrices, medians/IQR, raw records and charts.
- [Mixed-stock material scoring](../docs/SCORING.md) is implemented; freeze all
  tool settings and the seed matrix before quality tuning.

The current runner's `completed_unvalidated` status is deliberately ineligible for
any quality claim. A fixed seed and wall-clock budget do not promise bitwise repeatability.
