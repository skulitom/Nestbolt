# Benchmark groundwork

Run `python scripts/smoke.py` for two sequential five-second Sparrow runs. The
first invocation builds the pinned native executable with four compilation jobs.
Subsequent invocations reuse it. Outputs are never overwritten. Each run sets
`--workers 1` and `RAYON_NUM_THREADS=1`. Full sessions remain local; keep below
eight concurrent runs and about four hours, with temperature checks between sessions.

`smoke.json` freezes generated MIT fixtures and the current Sparrow revision.
`locks/sparrow.Cargo.lock` freezes its transitive dependencies, which upstream
does not commit. The tool's full source, notices and licence remain in its ignored
checkout under `.cache/upstream/sparrow`. No benchmark datasets have been imported
or relicensed from that checkout. Use `--verify-only` to check fixtures offline.

## Required before M0 can close

Sparrow's published runs use historical source revisions, dated nightly compilers,
SIMD flags and run-specific seeds. The current stable build smoke is a separate
integration check. Follow the [upstream reproduction instructions](https://github.com/JeroenGar/sparrow/blob/4629b22795ae6b25b3b460ccde6fb36a71292b6d/data/experiments/README.md)
to select, freeze and reproduce the published comparison within 1%.

## Required for M1

- Independent layout validation, shared geometry conversion and constraint checks.
- Licensed/checksummed S, B and 40 M jobs; mark 10 M jobs held out before any tuning.
- LBF, deepnest-next and SVGnest runners; identical-constraint and best-settings modes.
- 60/300-second budgets, seed matrices, medians/IQR, raw records and charts.
- Decide mixed-stock material scoring before freezing the matrix (see architecture notes).

The current runner's `completed_unvalidated` status is deliberately ineligible for
any quality claim. A fixed seed and wall-clock budget do not promise bitwise repeatability.
