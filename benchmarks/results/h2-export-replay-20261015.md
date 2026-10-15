# H2 current public export replay — 2026-10-15

**All 246 saved training layouts validate and export through the current CLI.**
Current imports retain the same source geometry, tolerance and stock outlines.
Of 492 SVG/DXF files, 491 are byte-identical to their retained previously
measured outputs. The remaining SVG stays within the original 0.01 mm fidelity
limit under a separately checked geometric bound. H2 remains open.

[Frozen replay inputs](h2-export-replay-20261015/plan.json),
[original replay result](h2-export-replay-20261015/results.json),
[geometric review](h2-export-replay-20261015/review.json),
[archive integrity](h2-export-replay-20261015/integrity.json).

## Scope and method

The earlier [complete vector fidelity sweep](h2-fidelity-20261014T012836Z.md)
measured 246 importable training files and retained eleven clear rejections.
Export code has since changed for leads and native cutting sidecars. This replay
checks that current public default exports retain that earlier evidence.

Select the training split before reading inputs. Match all 257 retained case
results exactly to their committed report rows; preserve the eleven rejections
without treating them as successful imports. For each of the 246 passed cases:

1. Import the frozen original through the current CLI with its recorded options.
2. Require exact equality of parts, original curves, collision polygons,
   tolerance and stock outlines with the retained library.
3. Reconstruct the original public request from its saved job, with one copy of
   every part, the same rotations/mirroring, stock and margins. Assert the
   original clearance additions, leaving leads and common-line mode off.
4. Export the saved layout through the current public CLI, which independently
   validates it before exporting. No nesting search is performed.
5. Compare the complete per-sheet SVG/DXF set against the retained old files.

These functional checks ran sequentially on CCD1 CPU 16. They provide no
performance claim and do not use the physical CCD0 lanes running the separate
H4 comparison. Source and executable guards stay unchanged: product digest
`921ad6f59b0dae0b243ba9cd8e98a03dd4d6a3b6404d4e4251414105f26beb7c`,
CLI `5e07f350761f3b5dfb820e404c85982dacd039d0789b8bfca63f66e76bf20bf7`.

The historical raw files were retained locally, and each original case result
matches its committed report row. Their raw-file hashes are recorded for the
first time in this replay; they are not claimed to have been sealed at the
original measurement. Copies of both old and new outputs are now archived.

## Retained byte difference

The original stricter byte-equality result remains **failed** for
`real/keebio--iris-case/34325b83-iris-switch-plate-3mm-thick.svg`.
Its DXF is byte-identical. Its SVG changes eight coordinate tokens by
0.000001 mm, affecting endpoints of twelve straight segments.

Independent `svgpathtools` parsing checks all 43 subpaths and 402 segments.
Segment types/order, every nonlinear segment and all other XML are exact.
The maximum changed endpoint distance is 0.0000009999999975 mm. A point on a
straight segment is a convex combination of its endpoints, so that value
bounds the symmetric Hausdorff difference between the two SVGs.

Adding this bound to the original measured source difference gives
**0.000491917842 mm**, below the unchanged **0.01 mm** gate. This supplies
geometric fidelity evidence without relabelling the byte comparison as equal.
The difference is consistent with serialized-layout rounding at the six-decimal
export boundary; no isolated cause is claimed.

An initial review sentence used the wrong unit name. The correct displacement
is one **nanometre**, not one micrometre; the numerical values and checks were
always unchanged. The original sentence remains in the raw archive, and the
readable review records the editorial correction explicitly.

## Preservation and remaining work

The verified archive contains 3,942 members and is 16,469,209 bytes, SHA-256
`cb0428616f396cf1959bb16e6b06c46a6c92e56e08b27d5cf140bb5b624ddfd0`.
Every member size/hash and archive CRC passed before loose case files were
consolidated. Original results, failures, requests, libraries, layouts, old/new
exports and both review scripts are retained. The original numerical sweep
and all frozen sources/labels/splits remain unchanged.

This closes the current vector-export regression concern. The twelve missing
native explanations in the [warning review](h2-native-warning-review-20261015.md)
still need implementation, and complete H2 acceptance still needs the remaining
reserved evaluation and its pending denominator decision. No held-out geometry,
new quality claim, release or registry publication is involved. Completion
remains **45%**.
