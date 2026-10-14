# H2 large-sheet margins: two nesting failures repaired

The two Gherkin DXFs in the [full training fidelity sweep](h2-fidelity-20261013T202338Z.md)
imported correctly but could not nest. Jagua's depth-limited pole search failed
on a narrow margin barrier: a 5 mm strip across roughly 7,281 or 7,994 mm of
stock. It was an artificial sheet margin, not a thin part or source contour.

## Change

The constructor partitions margin rectangles whose aspect ratio exceeds 256.
Their contiguous rectangles cover the same barrier, and offsetting their union
preserves its clearance. Adjacent endpoints share f32 coordinates. Ordinary
margins retain their original representation. Source geometry, requested margins,
stock dimensions and export curves are untouched. At most 4,096 pieces per margin
are allowed; more extreme margins fail clearly with a size/margin repair message.
No dependency or search setting changed.

An authored 8,000 by 9,000 mm stock case, also transposed, reproduced the original
`no pole found with 10 levels of recursion` failure before the fix. Afterward it
places four panels on one sheet, passes the independent clearance/overlap check,
and leaves the complete source job unchanged. All 11 constructor tests pass.

## Frozen training rerun

[Full per-file measurements](h2-fidelity-20261014T010851Z.json),
[table](h2-fidelity-20261014T010851Z.md).
Reproduce with `python scripts/h2_fidelity.py --only gherkin_` after building
the optimized `fidelity` example on CCD1.

| Source | Parts | Elapsed s | Maximum SVG difference mm | Maximum DXF difference mm |
| --- | ---: | ---: | ---: | ---: |
| Gherkin super slim DXF | 3 | 10.58 | 0.000000664311 | 0.000000671033 |
| Gherkin with steps DXF | 8 | 22.26 | 0.000000691051 | 0.000000694418 |

Both layouts pass independent validation; all 358 contour comparisons match with
no missing or extra contours. The same-family SVG negatives retain their clear
repair instructions. Across the original sweep and explicit corrective reruns,
242 vectors now have passing fidelity evidence, 11 reject clearly and four dense
Iris DXFs remain timeouts. This cumulative statement does not imply a fresh full
sweep on the current build. Original failed results remain unchanged.

## Remaining dense-file timing failure

A [bounded diagnostic](h2-dense-profile-20261014T011204Z.json) on training input
`30a5fb13-iris-rev3-bottom-plate.dxf` requests one second of repeatable work with a
20-second cooperative limit. The process still exceeds a 90-second external
limit. Its group phase finishes at 0.04 s, but no warm-start completion is reported;
only the imported library is written. Model/warm-start preparation needs further
profiling. This is an explicitly retained timeout, not a fidelity pass or proof
of a specific slow function. The other three earlier dense timeouts remain open.
Reproduce with `python scripts/h2_dense_profile.py --only 30a5fb13 --timeout 90`.

## Verification and scope

The current workspace suite passes 199 tests with one existing ignored test;
all 20 optimized CLI feature tests pass. Strict Clippy, formatting, dependency
notices, and the optimized WASM/TypeScript/browser build pass. All 48 enabled Chromium/Firefox end-to-end tests pass; four opt-in
benchmark/scale tests remain skipped. No fresh H4 quality/scale claim is made.

The four-file fidelity run used CCD0 physical cores 0/2/4/6; the single bounded
profile used CPU 8. Builds/tests used CCD1. Product and runner hashes remained
stable during each diagnostic. Frozen manifest SHA256 is
`02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`;
all 1,181 inventory hashes pass. Training entries were selected before reading
any source/label. No held-out geometry or labels were interpreted. Published v1
results and defaults remain unchanged; no quality claim or release is made.
H2/H3 remain incomplete and completed milestone weight stays 15%.
