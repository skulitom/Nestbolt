# Open-stroke preservation test: CI timing correction

The [web CI job for 9364ec4](https://github.com/skulitom/Nestbolt/actions/runs/38797983412/job/116639321118)
passed 83 tests and failed the new Firefox open-stroke test (four opt-in tests
skipped). The test allowed only one wall second to find a complete layout before
checking preservation. Its original assertion showed an alert count but omitted
the error text.

Four simultaneous Firefox copies on one CCD1 logical CPU (16) reproduced two
failures. Both reported `no complete layout within 1 s`. This is the documented
short-budget outcome, not evidence of changed XML. The other two copies passed.
The improved assertion retains the actual alert text in future failures.

An intermediate repeatable-work diagnostic passed four copies, but retained the
one-second real-time ceiling and returned non-repeatable results when that limit
was reached. It was not selected as the correction. The final test keeps ordinary
wall-clock mode and allows ten seconds. All four copies then passed the same
contention check, including unchanged source XML, path identities, vertices and
primitives. All ten LightBurn tests pass in Chromium and Firefox at normal CCD1
affinity, and the test TypeScript check passes.

Only the test budget and its failure reporting changed. Product code, default
budgets, benchmark budgets, frozen inputs and preservation assertions are
unchanged. This does not establish a one-second performance guarantee or complete
H3. The original CI log, local failure contexts, intermediate diagnostic and final
checks are retained in the [verified archive](ci-open-lines-20261015/raw.zip), with
[member hashes and sizes](ci-open-lines-20261015/integrity.json).
