# Search quadtree registration fix — 2026-10-13

The [Linux CI failure](ci-search-panic-20261013.json) reproduces locally with the
exact shrunk input and seed 162. Both initial runs panic in jagua-rs 1.1.0's
`QTHazard::constrict`. The new direct regression requires all three parts to be
placed and independently validated; it does not accept an error as success.
The original proptest seed is also saved alongside the earlier regression seed.

The unbounded separator search proposed a position whose bounding box intersects
the collision grid, while the actual angled outline lies outside it. Our existing
box-only guard accepted that position. Registering its hazard leaves no outline
edge in any root quadrant, violating the collision engine's assertion.

An independent GEOS check of the captured proposed outline confirms:

- Bounding-box intersection: 2.150572438 mm².
- Actual polygon intersection: 0 mm².
- Actual polygon distance from the grid: 0.125632298 mm.

The separator now keeps the current position when a proposed outline has no edge
in the collision grid. Completely contained bounding boxes use the existing fast
path without scanning edges. The source geometry, validator and search settings
are unchanged. The fixed job completes with all three parts valid.

The local jagua-rs source tree matches every file in the published crate archive,
whose SHA-256 is the checksum in Cargo.lock:
`2968688d182525c3b5b80d49e497f620b626c0e242816fcf3a4f2a91ac64ab06`.
No dependency source was modified. The fix is in Nestbolt's separator guard.

The machine-readable companion records final local checks and source/log hashes.
This is a crash correction, not a new quality benchmark. Published v1 results
remain unchanged; no held-out geometry or labels were used. The v1.1 goal remains
at 15% completed milestone weight.

Validation: 189 workspace tests pass, one existing test is ignored, and the
regression passes in both debug and optimized builds with all three placements
valid. Strict workspace Clippy, the WASM core check, formatting and dependency
notices pass. Linux/Windows CI verification follows the next push.
See [the machine-readable evidence](ci-quadtree-fix-20261013.json).
