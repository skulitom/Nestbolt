# Joint repair across two sheets — authored witness, 2026-10-18

The [assignment-bridge pilot](h5-assignment-bridge-pilot-20261018.md) misses all four
mechanical material limits. Some saved source inventories cannot meet the target
area without changing membership. This fixture tests one specific limitation of
repairing the receiver and source separately, using the existing separator.

## Construction and actual result

All stock is 100 × 100 mm, edge clearance is 1 mm, part clearance is 0.2 mm,
rotation is fixed at zero, and mirroring is forbidden. An earlier sheet is fixed.
The receiver initially holds a 20 × 94 mm filler and a 60 × 85 mm return part;
the source holds a 30 × 94 mm incoming part and a 40 × 50 mm extra part.

An authored proposal swaps incoming and return parts. Its receiver is valid, but
the source now contains two overlapping rectangles. Their widths plus clearance
total 100.2 mm and their heights plus clearance total 135.2 mm. Both exceed the
full sheet's 98 mm usable dimension. Two axis-aligned rectangles must separate
along at least one axis, so this fixed source inventory cannot fit. This is a
proof about these rectangles and this sheet, not about whole development jobs.

With seed 0 and a maximum 12 charged-work-second allowance per repair, the
source-only separator returns nonzero loss and an invalid layout. A hand-authored
joint rearrangement is valid. The actual joint separator also finds a valid
rearrangement: the extra part migrates to the receiver and the source retains the
return part. Material changes from **29,699.9994 to 28,799.9993 mm²**. The fixed
prefix is exactly unchanged; quantities, permitted poses and boundaries validate.
The joint call ends before its deadline. The allowance is a functional-test
bound, not a wall-time speed comparison or a new production budget.

The incoming/return proposal is deliberately constructed. This test does not
establish that current proposal selection would choose it, or that the current
exchange policy has no other route. The normal window separator already supports
cross-sheet sampling; the gap demonstrated here is fixed membership during
directed-proposal repair. No runtime policy has changed.

## Independent checks and retained failure

The frozen public CLI validates the before layout, hand-authored feasible layout
and actual joint output, and rejects the overlapping proposal and source-only
repair output. Shapely independently checks all eight same-sheet filled-outer
pairs across valid outputs, stock boundaries, quantities and allowed orientations.
All four runtime layouts retain an exactly identical earlier-sheet placement.
The hand-authored prefix is checked separately against its exact [2, 2] pose.

The first audit mistakenly required byte equality between that authored f64 pose
and the solver's f32 round-trip. Its failed checker, saved CLI outputs and failure
record remain in the raw archive. The corrected audit reuses the original native
outputs, retains exact equality among runtime poses, and changes no geometry
tolerance. There was no search rerun or changed fixture.

One optimized native test passes; 156 existing tests are filtered out and their
bodies are verified unchanged, together with every runtime source file. This
witness does not claim a new complete-suite qualification. The exact binary,
formatted sources, logs, helper scripts, original failure and corrected checks
are archived with member hashes and verified ZIP CRCs.

## Next decision

Qualify a distinct joint-repair policy while retaining the original short phase,
overall deadline, validation reserve and strict final whole-job acceptance.
Repair only the two selected sheets in a temporary two-sheet container so an
unselected active sheet cannot move. Preserve the original cropped source boundary,
stock walls/defects, original item models and all earlier sheets. Failure, expiry
or non-improvement must leave the incumbent intact. Proposal counters must not
claim that only the initially selected parts moved during joint repair.

Require positive and failed joint repairs, expiry, nonadjacent selected sheets,
fixed intervening sheets, quantities/poses, reserved holes, exact replay and old
fast-phase behavior before any new matched development comparison. A hand-authored
success is not evidence of improved real-job quality. Production, releases,
reserved inputs, thresholds and completed milestone weight remain unchanged.

[Native check](h5-joint-repair-witness-20261018/native-checks.json),
[independent checks](h5-joint-repair-witness-20261018/independent-checks.json),
[first audit failure](h5-joint-repair-witness-20261018/first-audit-failure.json),
[source patch](h5-joint-repair-witness-20261018/witness.patch),
[archive integrity](h5-joint-repair-witness-20261018/integrity.json).
