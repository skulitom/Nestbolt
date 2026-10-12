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

## Current CLI adapters

```powershell
cargo run -p nestbolt-cli -- validate --job examples/validation-job.json --layout examples/validation-layout.json
cargo run -p nestbolt-cli -- validate-sparrow --input original.json --layout result.json --units unitless
```

The polygon job/layout contract checks finite or unlimited stock, margins,
irregular remnant outlines, overlapping defect zones, parts with holes or multiple
rigid components, exact physical copies, rotation steps/lists/free rotation,
mirroring permission, units, edge/inter-part clearance, and all/fill-area/fill-priority
modes. It rejects empty declared sheets and gives invalid layouts **no metrics**.
Fill can validly place nothing, including when defects cover all usable stock;
that has zero quality score. Diagnostics retain a total count and at most 128
messages, bounding report memory on heavily overlapping layouts.

The example places an insert inside a frame's hole, alongside two brackets.
It is a hand-authored validity fixture, not a solver-quality result. The
[internal schemas](../schemas/README.md) are generated from the actual Rust types.
Material scoring, including mixed stock, follows [SCORING.md](SCORING.md).

This checks a Sparrow strip result against a **separate original source file**;
embedded copies of source geometry or reported solver density are ignored.
It checks exact item demands/IDs, original polygons, rigid transforms, allowed
rotations, containment and all pair overlaps. It adapts into the same job checker,
not a second scoring implementation. Unknown transform fields such as
scale are rejected. Overlap is measured against the smaller part's area and must
not exceed 1e-6; cumulative overlap per part must also stay below 1e-6 of its area.
Containment permits only two integer-grid units of boundary
rounding. Allowed angles tolerate 0.00001 degrees for historical f32 exports.
Historical empty orientation lists mean fixed orientation; null means free.
Invalid layouts print a JSON report and return a failing exit status.

The strip adapter handles the simple-polygon, zero-clearance jobs used for M0.
The M3 curve fidelity validator is not implemented. Support for checking part-in-part
layouts does not mean a Nestbolt optimiser can produce them yet.

`python scripts/validate_m0.py --experiment NAME` records independent reports for
completed runs, preserving every raw layout and the original run record. Each
report includes binary/source/input/layout hashes and the checker commit.
Run this after each bounded M0 batch. It adds evidence without changing the
predeclared M0 quality comparison or discarding invalid outputs.

## Verification and remaining work

Thirty-three validator tests cover the geometry kernel, stock/fill constraints,
scoring identities and strip adaptation. They include a fixed-seed 10,000-case
adversarial polygon fuzz test, analytic rectangle/winding properties (48 cases
each), and a 2,000-copy layout. Two additional CLI integration tests check actual
success/failure exit behavior. These are bounded tests, not the complete G1 matrix;
curve fuzzing and heterogeneous browser-scale evidence remain outstanding.

Boundary-distance checks prune edge pairs whose bounding boxes cannot improve
the closest known distance, with two grid units reserved for numerical rounding.
The exact segment predicates and distance calculations are unchanged. Two new
tests compare against the exhaustive reference, including 3,000 fixed-seed pairs
in both directions, curved and multipart boundaries, near-touching contours and
large coordinates. All 104 retained development validation reports match
exactly in the [replay and timing diagnostic](../benchmarks/results/validator-speed-20261012T0420.md).

`scripts/validator_replay.py --binary PATH --pilot RESULT.json` repeats those
independent checks without rerunning a solver. Multiple `--pilot` arguments are
allowed; only frozen development jobs are accepted. The
`profile_geometry` validator example reports time spent constructing original
and transformed footprints, checking pairs and validating the full layout.

Next: feed every competitor adapter through this same contract, expand fuzzing
and measure heterogeneous large-job time/memory. Ring topology checking is
currently quadratic in its vertex count; the passing 2,000-rectangle native test
does not establish the browser's 2,000-part import/solve/export requirement.
