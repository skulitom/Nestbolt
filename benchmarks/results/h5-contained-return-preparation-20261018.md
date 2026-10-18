# Contained return initialization — preparation, 2026-10-18

The [failure diagnosis](h5-exchange-failure-observer-20261018.md) finds eighteen
source repairs with positive loss and actual remaining filled-outer violations.
Four valid trials retain the height-setting inserts and increase material by
only 0.0025–0.00375 mm². The strict acceptance guard remains appropriate.
This motivates a return-initialization hypothesis, not a feasibility claim.

The isolated candidate translates a returned group as a whole into the existing
source-container bounding box when it fits. It retains orientations/reflection;
relative positions share the same translation, subject to native float arithmetic.
Already contained, oversized, malformed and numerically uncontained groups keep
their old poses exactly. The original and shifted collision-shape bounds are
charged. A small interior offset, capped at half the available space, avoids
placing a rotated group exactly on a rounded boundary. The second containment
check remains exact; no acceptance tolerance changes. This box is only an initial
seed constraint: all existing collision repairs and full-job checks still apply.

All 133 optimized tests pass, with 130 prior tests unchanged. Against the old
behavior the new tests first show two expected movement failures and one no-op
pass. The first implementation passes 132 tests but fails rotated containment;
its source, binary and log remain. The interior-seed correction changes no test
or exact containment assertion. The saved authored witness independently confirms
translation of original contours, unchanged rotation/reflection, charged work and
a valid source fixture. It is not a searched output or quality comparison.

Twelve rejection-boundary outcomes pass 24 frozen-CLI checks. Ten public outcomes,
four CLI comparisons, exact normal results and deterministic common replays apart
from wall time pass. Strict lint and the experimental executable build pass.
All 156 formatted files reconstruct exactly; 155 and all other runtime blocks
are unchanged. Five adversarial harness checks pass. Pilot execution, scoring,
case ordering and the previously qualified PID-reuse guard remain AST-identical.

The next pilot must commit its plan before measurement, retaining the same four
development jobs, two kerfs, three seeds, matched 60-second budgets and eight
physical CCD0 cores. No quality measurement has started at this checkpoint.
Any pilot success still requires the full original 13-job H5 gate.
Production, reserved inputs, release and README claims are unchanged.
**H2/H5 remain open; completed milestone weight is 60%.**

[Checks](h5-contained-return-preparation-20261018/checks.json),
[retained initial failures](h5-contained-return-preparation-20261018/expected-failure.json),
[preserved boundary-contact failure and repair](h5-contained-return-preparation-20261018/containment-repair.json),
[original-contour witness](h5-contained-return-preparation-20261018/seed-checks.json),
[source reconstruction](h5-contained-return-preparation-20261018/reconstruction.json),
[raw archive integrity](h5-contained-return-preparation-20261018/integrity.json).
