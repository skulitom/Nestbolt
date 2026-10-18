# Actual source-frontier repair witness — 2026-10-18

**The existing repair finds a lower valid layout when given the exposed source boundary.**

The earlier mechanical traces motivated an explicit boundary: selecting top
members often exposes unused height, but the original repair can return displaced
parts to that same upper band. This authored three-sheet case tests the mechanism
before changing automatic policy. Its original arrangement, proposed swap and
hand-arranged feasible solution all validate. The fixed first sheet is excluded
from the repair.

Both calls use the existing joint helper, seed zero and the same twelve-second
work allowance. The original crop leaves the source top at **87.200677 mm**.
The crop derived from the actual remaining source makes the helper find a layout
with a source top of **51.000558 mm**. The returned part migrates to the receiver;
both original extra source members remain on the source. Material falls from
**28,820.0677 to 25,200.0558 mm²** between these two actual outputs. This is a
constructed mechanism witness, not a development quality or speed comparison.

The targeted call finishes at work-clock 0.152745 with deadline 12.05001;
the original-crop call finishes at 0.152798 with the same deadline. These values
include setup and are not wall-time measurements. The helper validates both exact
internal containers and the reconstructed whole job. Independent frozen-CLI
checks validate seven unique saved layouts, including the selected-member-removed
component with adjusted quantities. Filled outer contours pass 26 pair checks
at the unchanged 1e-7 mm tolerance. Quantities, permitted orientations and the
fixed prefix remain correct.

The one new native test passes; all 165 previous test bodies and runtime policy
are unchanged. The 156 other source files match their parent exactly. The sealed
archive includes the complete original-runtime workspace, test executable,
original logs, helpers and saved geometry. All 209 members and CRCs verify.

This establishes useful behavior of an explicitly invoked helper. It does not
prove that automatic proposal selection will reach it, that the target is feasible
for the mechanical jobs, or that H5 will pass. The next step is isolated automatic
selection and qualification under the existing deadline, reserve, four-step cap,
strict material guard and rollback. Empty remaining sources need an explicit
policy so useful exchanges need not eliminate the last sheet. Production and
v0.2.0-alpha.1 remain unchanged; H2/H5 remain open at 60%.

[Native result](h5-frontier-witness-20261018/native-checks.json),
[independent checks](h5-frontier-witness-20261018/geometry-checks.json),
[saved witness](h5-frontier-witness-20261018/witness.json),
[source patch](h5-frontier-witness-20261018/witness.patch) and
[archive integrity](h5-frontier-witness-20261018/integrity.json).
