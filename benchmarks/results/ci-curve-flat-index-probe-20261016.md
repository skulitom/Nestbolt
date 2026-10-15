# Isolated fix candidate for the curve-search assertion

The [retained CI failure](release-readiness-20261016.md) occurs while packing a
small part into a hole. A copy of the engine under `output/ci-curve-probe/`
changes only that pass's jagua-rs configuration to `quadtree_depth: 0`. The hole
container retains a collision index without subdividing it, so placement queries
avoid the non-conservative quadrant classifier. All independent pattern/layout
checks remain in place. The upstream dependency and production source are
unchanged; debug assertions remain enabled.

The exact shrunk case passes in this candidate: eight copies, independent
validation and no assertion. An expanded copy of the existing generated-curve
test also passes all 128 cases with generation seed `20261016`. Its generated
drawings include rings with holes, ellipses and arc lenses. That property permits
valid layouts or explicit infeasibility errors; it is not a claim that every
generated job produced a layout. The exact regression is separately required
to produce a valid eight-copy layout.

For the expanded check, the probe's dependency lock was reset from the production
lock. Every third-party version/source/checksum entry matches. The exact case
was then rebuilt and rerun with that lock: input SVG and polygon job are byte
identical to the original reproduction, and the existing standalone optimized
CLI validates the candidate layout with exactly matching metrics. The first
candidate build's log remains preserved separately; its incidental dev-dependency
resolution is not the aligned-lock verification.

These are functional experiments on CCD1, using an isolated debug workspace.
The candidate engine is a workspace member and this probe does not reproduce
the production workspace's explicit per-engine development optimization profile.
No speed, material-quality or current-build acceptance claim follows. Integrate
and test in the real workspace only after the guarded H4 matrix finishes; then
measure the change's effect on part-in-hole packing and affected development
quality. A flat index may have a different cost on holes with many small parts.

The original failure, production executable and browser build remain unchanged.
H4 guards match before and after the probes. The release blocker remains open
pending integration and required checks; milestone completion stays 45%.

Retained evidence:

- [Initial candidate check](ci-curve-flat-index-probe-20261016/checks.json)
- [128 cases and aligned-lock exact regression](ci-curve-flat-index-probe-20261016/fuzz/checks.json)
- [Candidate module](ci-curve-flat-index-probe-20261016/candidate-holes.rs)
- [Expanded test output](ci-curve-flat-index-probe-20261016/fuzz/curves-stdout.txt)
- [Original source/candidate integrity](ci-curve-flat-index-probe-20261016/integrity.json)
