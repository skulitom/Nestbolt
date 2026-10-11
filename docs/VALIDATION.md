# Independent geometry checks

`crates/validator` has no dependency on jagua-rs, Sparrow or geo. Its geometry
backend is [clipper2-rust 1.2.0](https://docs.rs/clipper2-rust/1.2.0/clipper2_rust/),
a pure Rust Clipper2 port under BSL-1.0. The lockfile and third-party notices record
that version and its licence. The crate compiles natively and to unthreaded WASM.

The geometry kernel independently transforms original f64 contours and measures
intersection and containment. It supports polygon holes, reflection, rotations,
translation, positive clearance, and explicit mm/inch/unitless coordinates.
Clearance uses round polygon offsets with boundary-segment distance confirmation;
holes may act as part interiors or container defects. Clipper operation failures
are errors, never interpreted as an empty intersection or a valid placement.

The integer grid is 0.000001 mm for physical jobs, or 0.000001 units for academic
unitless jobs. Positive clearance tolerates two grid units of rounding. Coordinates
are limited to ±10,000,000 mm (or unitless units), and a polygon to 10,000 vertices.
Consecutive duplicates and redundant collinear vertices are normalised. Collapsed,
self-intersecting, self-touching and doubled-back rings are rejected. Holes must
lie strictly inside their outer ring and cannot overlap, nest or touch one another.
Input geometry is never repaired silently across these topology errors.

## Current CLI adapter

```powershell
cargo run -p nestbolt-cli -- validate-sparrow --input original.json --layout result.json --units unitless
```

This checks a Sparrow strip result against a **separate original source file**;
embedded copies of source geometry or reported solver density are ignored.
It checks exact item demands/IDs, original polygons, rigid transforms, allowed
rotations, containment and all pair overlaps. Unknown transform fields such as
scale are rejected. Overlap is measured against the smaller part's area and must
not exceed 1e-6. Containment permits only two integer-grid units of boundary
rounding. Allowed angles tolerate 0.00001 degrees for historical f32 exports.
Historical empty orientation lists mean fixed orientation; null means free.
Invalid layouts print a JSON report and return a failing exit status.

The adapter handles the simple-polygon, zero-clearance strip jobs used for M0.
It does **not** yet provide the complete M1 stock/margin/quantity/fill/mirror-rule
job validator, or the M3 curve fidelity validator. The kernel's support for holes
does not mean the optimiser can nest parts in holes yet.

`python scripts/validate_m0.py --experiment NAME` records independent reports for
completed runs, preserving every raw layout and the original run record. Each
report includes binary/source/input/layout hashes and the checker commit.
Run this after each bounded M0 batch. It adds evidence without changing the
predeclared M0 quality comparison or discarding invalid outputs.

## Verification and remaining work

Seventeen tests cover analytic rectangle intersections, winding and quarter-turn
properties, clearance/contact, diagonal distance, holes and defects, inches,
mirroring, tiny slivers, malformed contours, changed embedded geometry, invalid
quantities/rotations and nonrigid transforms. Property checks use 48 cases per
property locally and in CI. These are targeted checks, not the plan's full fuzzing
or acceptance matrix.

Next: complete the engine-neutral job/layout model and stock/rotation/fill rules,
validate every competitor adapter through the same path, add adversarial fuzzing,
and measure large-job time/memory. Ring topology checking is currently quadratic
in its vertex count; do not infer 2,000-part browser performance from these tests.
