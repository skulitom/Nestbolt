# H4 preview cache — 2026-10-15

Reusing exact preview geometry substantially reduces the measured preview
stalls. Chrome's largest Long Task between Nest and the final result falls from
**1,608 ms to 111 ms**. Its conservative heartbeat gap falls from 2,092.6 to
209.2 ms; Firefox's falls from 733 to **370 ms**. Both saved layouts remain
byte-identical to the earlier run and pass fresh native validation with zero
metric difference. **H4 still fails memory and responsiveness; completion stays
20%.**

[Machine-readable record](h4-preview-cache-20261015.json),
[raw-run summary](h4-curve-scale-20261015T170537Z/summary.json),
[phase comparison](h4-curve-scale-20261015T170537Z/phase-comparison.json),
[checks](h4-preview-checks-20261015/checks.json).

## Change and measurement

Baseline `1b23217`. Preview bounds previously traversed every placed vertex on
every progress redraw and again for each final caption. Bounds now reuse each
part's exact orientation and each immutable layout's sheet extents. Weak keys
release old projects/layouts; each part retains at most 128 orientation bounds.
Original outer vertices still determine the bounds. No proxy, flattening,
collision, search or export geometry changes.

The final SVG now defines each part path once per sheet and uses placement
matrices for its copies. Every component and hole vertex is retained, without
the former three-decimal preview rounding. Unique SVG IDs avoid collisions
between sheets; titles, colours, hole fill rules and rigid mirroring/rotation
remain. The live canvas reuses the same extent calculation.

This measures preview reuse as one lever. Worker selection, ZIP assembly,
native binary, WASM, solver options, the frozen fixture and runner are unchanged.
Quick initial layout is enabled in both compared runs. The actual app uses the
default two effective workers on physical cores 0 and 2, a 60-second search
budget, 2,000 parts, 1250 × 2500 mm stock, 5 mm margins, 1.5 mm spacing/edge gap,
quarter turns and no mirrors. Independent native validation uses core 4;
builds and functional tests use CCD1.

| Measurement | Chrome 155.0.8059.41 | Firefox 157 |
| --- | ---: | ---: |
| Import | 0.336 s | 0.535 s |
| Nest to final result | 109.910 s | 109.297 s |
| Previous Nest to result | 159.730 s | 115.973 s |
| Nest/preview maximum Long Task | 111 ms | API unavailable |
| Nest/preview maximum heartbeat gap | 209.2 ms | 370 ms |
| Export | 88.499 s | 93.949 s |
| Whole-workflow maximum heartbeat gap | 2,801 ms | 1,569 ms |
| Peak working set | 2.099 GB | 2.074 GB |
| Peak private memory | 2.569 GB | 1.977 GB |

Chrome's remaining 2,779 ms Long Task is at ZIP assembly. Firefox has no Long
Tasks API; its unavailable value remains null. Full workflow telemetry, including
import, live/final preview, export and the post-download observer delivery, is
retained. The 20 ms heartbeat is conservative and is not substituted with a
smaller number. Even the nest/preview heartbeat still exceeds 200 ms in both
browsers. These are one-run development observations, not a statistical speed
claim or the H4 quality matrix.

Both exports contain all 2,000 placements on three sheets, with 500 hole riders
and normalized material 2.2468772308. All expected SVG/DXF entries exist and ZIP
CRCs pass. Their saved layout SHA-256 remains
`e63e6ed152da3526feee8a9297c21c7c3b96f12ec14abf0e5e5ab9a26bc82873`.
All source, runner, asset, fixture and executable guards pass in this run.
The earlier comparison batch's validator-binary guard failure remains documented
in its [original report](h4-quick-start-20261015.md); its browser assets were
unchanged and its saved geometry was separately rechecked.

## Checks and next action

All **66 enabled** Chromium/Firefox suite tests pass; four opt-in cases remain
skipped. The new direct-vertex oracle covers 320 orientation/identity trials,
including arbitrary angles, mirrors, multiple sheets and changed libraries.
Path tests retain every component/hole point and verify SVG matrices; actual UI
tests check unique cross-sheet references, titles, fill rules, extents and placed
coordinates in both browsers. Product/test TypeScript checks and the production
web build pass. Existing real nesting, lead/common-line and export tests pass.
Native sources are unchanged, so native tests were not rerun for this UI change.

Initial test failures remain in the original logs: missing test-module extensions
and one authored fixture field, signed-zero expectations in SVG text, and a
Firefox context-teardown protocol error. Corrected test expectations preserve
all geometric tolerances; the subsequent full suite passes. Original logs and
browser records are archived without newline normalization and verified by CRC
and SHA-256. The frozen shop manifest checksum is unchanged.

Keep the preview cache. Next, measure one worker on this same job to separate
worker memory/CPU contention from remaining drawing costs, then move ZIP
assembly off the main thread. Do not change gate thresholds. Browser quality,
the full G5 bounds and the 195-run native matrix still need evidence. No held-out
geometry, published defaults, release or final acceptance changes.
