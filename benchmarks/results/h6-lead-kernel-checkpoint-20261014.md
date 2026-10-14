# N5 independent lead-footprint kernel — 2026-10-14

This checkpoint adds an independently reconstructed physical lead envelope and
collision checks. It is groundwork for H6, not a completed lead-in feature or a
native LightBurn lead acceptance result. The base is `0c67442`.

## Implemented contract

`crates/validator/src/leads.rs` accepts analytic line or circular-arc paths in
local millimetres. It rebuilds mirror/rotation/translation from the original
layout, including inch translations. It does not accept solver polygons as the
lead's physical shape. Kerf is finite, positive and at most 1,000 mm; the upper bound and
10,000-point arc limit make unsupported inputs explicit.

The envelope consists of a half-kerf-radius stroke and a pierce disc with
**diameter twice the kerf**. Chords have at most 0.0001 mm sagitta. Round offset
approximation and the 0.000001 mm integer grid are covered by an extra 0.000304 mm
stroke radius and 0.000204 mm pierce radius. Final bounds must remain inside the
validator's coordinate range. These guards reserve slightly more room than the
analytic physical path.

One contour can reserve two traversal directions at the same attachment. This
supports the observed native winding reversal in the
[contour-start probe](h6-contour-starts-checkpoint-20261014.md). A future planner
must actually provide both paths; accepting two paths does not generate them.

The checker first requires a valid original layout, then checks each supplied
allowance against:

- Every other original part copy on that sheet, including parts nested in holes.
- Every other contour's allowance on that sheet, including the same part's other
  contours. The two alternatives of one contour may overlap each other.
- The original stock outline, margins, defects and requested edge clearance.

Malformed paths, missing owners, duplicate contour records, mismatched
attachments and out-of-range contour indices fail explicitly. Geometric
collisions return a report with a total count and at most 128 diagnostics.
Unrelated sheets do not collide. Physical overlap remains a strict positive-area
failure; no collision tolerance was relaxed to pass the tests.

The validator also exposes footprint union and conversion back to declared-unit
polygons, preserving holes and nested islands. These will let the planner form
collision geometry while retaining original parts for material metrics.

## Independent tests and retained failures

The focused suite has 14 tests, including three 64-case property families:
analytic swept-disc coverage, independent matrix transformation and analytically
known rectangle unions. An independent floating-point ray crossing test samples
the exact physical stroke and pierce circles against the reconstructed polygons.
Full-circle cases cover radii from 0.000002 to 30 mm and kerfs from 0.000002 to
1,000 mm. Cases also cover pierce-only collisions, hole nesting, crossing leads,
separate sheets, inch jobs, margin/remnant/defect crossings and malformed inputs.
Union tests retain holes inside islands inside holes and check inch round trips.

The first run passed 10 tests and failed two assertions that required exact
containment after separately rounded polygon boolean operations. The observed
differences were 0.0000000043625 mm² for two alternatives and
0.0000279703265 mm² for a rotated rectangle union. The saved property seed remains
in `crates/validator/tests/leads.proptest-regressions`. The tests now check strict
analytic physical coverage for lead alternatives and a perimeter-times-two-grid
area bound for generic unions. This is the declared integer-grid error, not a
new overlap allowance in the checker. Subsequent focused runs pass.

The first strict lint run reported four unnecessary clones in the tests; these
are corrected. Initial failures and final check logs are retained with raw and
normalized hashes in the [JSON evidence bundle](h6-lead-kernel-checks-20261014/checks.json).

Review then found a real supported-range precision fault: adding a 0.000123-radian
sweep to a 100,000,000-radian start on a 1,000,000 mm radius loses about
0.005816 mm at the endpoint. The regression fails on the original implementation.
Arc evaluation now composes rotations, and rigid transforms combine principal
angles obtained with `atan2(sin, cos)` rather than adding large angles or using a
rounded multiple of tau. The final regression checks endpoints, mirrored and
unmirrored transformations within 0.0000001 mm, and exact endpoint stroke
coverage. The transformation property family now spans the entire supported
angle range. The original failure and arithmetic diagnostic are retained.

The workspace run passes 236 tests with one existing ignored test before the
final angle/positive-kerf adjustments. On the final sources, all 49 validator
tests pass, including the 14 lead tests; strict workspace Clippy, formatting and
both validator/browser WASM builds pass. Tests/builds use CCD1. The frozen
inventory check confirms all 1,181 hashes and the original manifest hash.
No browser interaction test is claimed for this internal API checkpoint.

## Remaining H6 work

This API validates supplied allowances only. It does not yet establish complete
contour coverage, waste-side placement against the owner's own material,
attachment to original source curves, length/angle settings, shortening or
shared-segment exclusion. In particular, the owner is exempt from the other-part
check because a valid lead necessarily meets its cut contour. A planner must
establish that the path stays on the appropriate waste side before enabling the
feature. An empty allowance list is not proof of complete lead coverage.

Lead planning and collision-geometry integration, actual LightBurn line/arc
calibration, export wiring, three searched native checks, material-cost reporting
on the common-line set, and UI/CLI/MCP parity remain pending. Public nesting and
export behavior is unchanged by this kernel. No held-out geometry or labels were
opened, and no native application was used in this checkpoint. H6 remains open;
completed milestone weight remains 15%.
