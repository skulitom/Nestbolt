# Provisional assignment sequences — preparation, 2026-10-18

The [extended-repair pilot](h5-extended-repair-pilot-20261018.md) still fails five
material pairs. Five of its six large-plate last-sheet assignments exceed the area
available at the conditional target height. Longer repair alone cannot fit those
same inventories into that same target prefix. Other assignments remain possible;
this is not global infeasibility evidence.

A new authored four-sheet fixture demonstrates an actual missing transition.
Three tall source parts share the upper boundary. Three existing exchanges reduce
source filled area from 7,650 to 5,700, 3,750 and 1,800 mm². Material stays at
38,800.001 mm² after the first two steps, then falls to 32,200.0559 mm². The previous
short-plus-strict-tail policy stops before that gain. Eight frozen-CLI checks and
48 independent filled-outer pair checks validate every saved intermediate state
and the previous policy's output. The fixture does not predict real-job quality.

The candidate retains the original short phase. During the remaining existing
relocation allowance, a validated material-flat step may remain provisional only
if the last sheet's canonical filled area strictly decreases. Original part order
and multiplicities make this area independent of placement keys; hole interiors
remain reserved. This ranking prevents revisiting an equal-material, equal-area
state. Area scans and snapshots are charged work. The acceptance deadline is
checked again after scanning. The original four-step cap includes provisional
steps as well as committed steps across both phases.

A sequence commits only when whole-job material strictly decreases. Failure,
expiry or exhaustion of the move cap restores the last committed layout and its
matching tracker. Original accepted counters are restored too; attempts, flat
steps and rollbacks remain visible separately. Existing quantity, orientation,
frozen-sheet, filled-hole, material and geometry checks remain. The whole-search
budget and validation reserve are unchanged.

All 156 optimized native tests pass: 148 prior test bodies unchanged, the original
policy witness and seven new policy tests. Before implementation, the seven new
tests produce five expected runtime failures and two preservation passes; their
source, binary and log remain. Twelve saved new outputs pass 24 frozen-CLI checks
and 156 independent filled-outer pairs. They include committed flat-to-gain
sequences, a real partially completed sequence that expires and rolls back, the
one-slot rollback, repeatability, disabled/expired behavior and prior fast gains.
Every previously independently checked native witness remains byte-equivalent as
JSON; those old checks are reused only for exact matching witnesses.

Strict lint, executable build, ten public outcomes, four CLI comparisons and five
adversarial harness tests pass. Normal results remain exact except wall time;
common replay is exact. All 156 formatted files reconstruct exactly, with 153
unchanged. Reversing the explicit policy adapter restores the original per-step
runtime; the caller changes only its dispatch name. Measurement, scoring, rotating
order and process identity functions remain AST-identical to the preceding pilot.
The guards additionally require that preceding pilot to be terminal.

The next matched four-job, two-kerf, three-seed pilot must commit its plan before
measurement. Each of 72 searches receives 60 seconds on a physical CCD0 core, with
at most eight running together. No quality run has begun. Production and releases
are unchanged. Every original H5 limit and the complete 13-job gate remain.
**H2/H5 are open; completed milestone weight stays 60%.**

[Checks](h5-assignment-bridge-preparation-20261018/checks.json),
[initial sequence](h5-assignment-bridge-preparation-20261018/initial-geometry.json),
[new outputs and exact prior witnesses](h5-assignment-bridge-preparation-20261018/bridge-checks.json),
[reconstruction](h5-assignment-bridge-preparation-20261018/reconstruction.json),
[raw evidence](h5-assignment-bridge-preparation-20261018/raw.zip),
[archive integrity](h5-assignment-bridge-preparation-20261018/integrity.json).
