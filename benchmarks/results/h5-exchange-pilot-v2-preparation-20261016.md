# Common-line exchange pilot: scheduling correction — 2026-10-16

The original [prepared pilot](h5-exchange-pilot-20261016/plan.json) was never
opened. It required the integrated preview to pass H4 and both scale fixtures
before starting H5. The [completed preview matrix](h4-preview-development-20261016.md)
instead fails Chrome's curve subset, so that workflow prerequisite would prevent
an independent H5 investigation even after the benchmark machine was available.

The separate [replacement plan](h5-exchange-pilot-v2-20261016/plan.json) waits for
the original H4 matrix to be completed, verified and sealed, and for the isolated
score-bound probe to finish. It refuses to start while either runner is active.
It records their exact completed results without requiring a quality pass.
H4 remains failed; its release hold and every H4/H5 acceptance limit are unchanged.
The original plan, runner and unopened state remain preserved.

Search and scoring are identical to the prior plan: the same matched observer
binaries, four development jobs, two kerfs, seeds 0–2, three arms, 60-second
budgets, independent validation/exports, original +1% material comparison, and
72 attempts. Each three-arm block stays sequential on one physical CCD0 core,
with rotated order and at most eight concurrent blocks. This remains a pilot;
the full 13-job H5 gate is still required before claiming that milestone.

[Seven harness checks pass](h5-exchange-pilot-v2-20261016/preparation-checks.json):
the five existing coverage, failed-result, scoring, order and deadline checks
exercise the replacement module; two additional checks ensure that a running
matrix prevents a start and that a completed quality failure is only a resource
prerequisite, never a milestone pass. No search has started under either pilot.

The [preparation archive](h5-exchange-pilot-v2-20261016/preparation.zip) retains
the exact replacement runner, diff, test log and helper scripts: six members,
12,938 bytes, SHA-256
`d9fb002245343268a4118f2e852b51707969ce3ed3b18debb85d2dd3c30bb3d0`.
CRC, every member size and every SHA-256 were verified. Original implementation,
observer builds and cache-failure evidence remain in the
[preceding sealed preparation](h5-exchange-pilot-preparation-20261016.md).

Completion remains 45%; no production change, held-out evaluation or release is
made by this scheduling correction.
