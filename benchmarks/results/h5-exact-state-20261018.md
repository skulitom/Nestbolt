# Exact-state observations on panel hardware — 2026-10-18

**1 of 6 neutral trials exactly preserve the complete internal physical state.**

Two serial seed-zero, 60-second panel-hardware diagnostics use kerfs 0.2
and 1.5 mm on physical CCD0 CPU 8. All original decisions, repairs, full
validation and strict material guards remain. Logging can alter wall-clock
trajectories; this is neither a quality comparison nor a speedup claim.

Both final layouts and all 12 saved intermediate layouts validate.
Independent filled-outer checks cover 111,838 same-sheet pairs
with the unchanged 1e-7 mm clearance tolerance. Every original quantity,
archive member/hash, trace counter, metric and source/binary/input guard
verifies. The session takes 2.036 minutes.

| Kerf mm | Attempts | Neutral rejections | Exact internal state | Neutral validation seconds | Identity check seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.2 | 8 | 3 | 1 | 0.2864983 | 0.0000435 |
| 1.5 | 8 | 3 | 0 | 0.3007107 | 0.0000463 |

1 of 6 saved neutral pairs have exactly equal public pose multisets.
The comparison ignores copy indices only within the same original part ID,
retaining sheet, full pose and multiplicity. The internal predicate also
requires the same immutable model/container objects and exact f32 bits.
Signed zero and equivalent angles may therefore yield a conservative false
result. Equal public poses are not substituted for the internal predicate.

| Kerf mm | Attempt | Exact internal | Exact public | Unmatched incumbent/trial public poses |
| --- | ---: | --- | --- | ---: |
| 0.2 | 0 | True | True | 0 / 0 |
| 0.2 | 1 | False | False | 3 / 3 |
| 0.2 | 2 | False | False | 2 / 2 |
| 1.5 | 0 | False | False | 4 / 4 |
| 1.5 | 1 | False | False | 3 / 3 |
| 1.5 | 2 | False | False | 3 / 3 |

An exact-state early rejection now has an observed target, but its impact on
search quality is unproven. A separate candidate may reject only a complete
exact-state match before repeated validation, preserving shared container and
original-item identity, full transform bits, reflection and multiplicity.
Every changed state and every accepted exchange must retain the original
full geometry/material checks. Qualify the predicate and early branch with
authored regressions, preserve expired/disabled behavior and rollback, and
repeat the existing paired development protocol only for that changed build.
Do not infer a quality gain or promote it from these diagnostic timings.

[Committed plan](h5-exact-state-20261018/plan.json),
[archive and metric verification](h5-exact-state-20261018/verification.json),
[every saved layout and independent check](h5-exact-state-20261018/layout-checks.json),
[all attempts](h5-exact-state-20261018/observed-exchanges.json),
[source review](h5-exact-state-20261018/source-review.json).

**H2/H5 remain open; completed weight stays 60%.** Production, reserved
inputs and earlier failed results remain unchanged. No new release is
warranted by this diagnostic; the existing preview and READMEs stay current.

The first independent-audit helper looked up before-material on an attempt
instead of its enclosing trace and stopped before checking any saved layout.
Its failed source and result remain preserved. The corrected helper uses
the same recorded inputs and tolerances; no search was rerun. See
[audit repair](h5-exact-state-20261018/audit-repair.json).
