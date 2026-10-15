# Missing LightBurn settings: native defaults and training membership repaired

Native LightBurn Pro 2.1.01 opens omitted vector settings as Line for the
authored indices 0 and 1, and Tool for indices 30 and 31. After opening an
explicit Fill project, reopening the omitted-settings input restores those
modes. The native save changes only the `priority` fields relative to its first
save, retaining the intervening layer order. The original frozen L36 project
also opens and saves with index 0 as Line. These are direct native observations
with the No Machine device, in hidden Anode session 2; no executable inspection,
activation, installation or trial change occurred.

The [probe plan](h3-missing-layer-native-20261015/plan.json) predates observation.
All three probe inputs remain byte-identical. Native saves are separate files.
[Native checks](h3-missing-layer-native-20261015/native-checks.json) retain the
settings and exact priority differences. Screenshots show the
[first open](h3-missing-layer-native-20261015/missing-initial.png),
[explicit Fill](h3-missing-layer-native-20261015/explicit-fill.png),
[second open](h3-missing-layer-native-20261015/missing-after-fill.png) and
[L36](h3-missing-layer-native-20261015/L36.png). The owned app was closed, the
1280×720 display restored and the desktop lease released.

## Product correction

A shared cutting classifier now applies the native Line default for omitted
vector settings 0–29 to both nesting membership and cutting sidecars. Omitted
T1/T2 settings keep shapes fixed. Bitmap settings remain a separate family.
Explicit settings, including Fill, output-off and cut sublayers, retain their
existing behavior. No default settings are inserted into the original XML.

The authored regressions verify contained Text and Bitmap membership, fixed
Tool shapes, rejection of mixed active/fixed groups, exact retained source
settings, and byte-identical SVG/DXF cutting sidecars compared with explicit
Line settings. Missing image settings do not turn Bitmaps into cut paths.

## Training evidence

The [fresh 64-input audit](h3-reviewed-prerequisites-20261015T204219Z/results.json)
checks all 56 original training projects and eight approved native repairs.
The originals still produce 45 imports and 11 documented rejections; every
repair imports. All no-op reads retain the source bytes, 114 canonical sheet
diffs pass, and 434 original/repaired nesting units independently validate.

The [comparison with the preceding build](h3-missing-layer-native-20261015/previous-comparison.json)
finds all 64 complete reader payloads identical. Consequently the previous
original/repaired leaf geometry evidence still applies. Writer payloads are
identical for 63 inputs; only L36 changes, from three units to the frozen
two-unit membership: the ellipse separately, and the outer path with its Text.

The [frozen-label audit](h3-reviewed-prerequisites-20261015T204219Z/labels.json)
matches **45/45 imported originals** on exact membership, physical cut holes,
fixed shapes and cutting layers. Physical holes are reconstructed with GEOS
from original Scene curves at 0.0002 mm, using the label's rule that group
holes exclude Text and Scan artwork. Conservative collision unions are not
used as a substitute for physical cut topology.

All eight repairs match membership, physical holes and fixed shapes. Seven
match the original cutting-layer labels. **L42 retains a real difference:**
native repair converts its legacy Scan+Cut layers 1–28 to Scan, leaving only
layer 0 cutting. This was already recorded in the
[text-cache audit](h3-text-cache-20261014T005902Z.md). The mismatch remains false
in this new report; no original label or score is changed. Nestbolt's canonical
writer checks preserve the repaired file's own settings. Repair acceptance is
not a claim that native re-saving leaves original machine settings unchanged.

L36 also completes an actual 10-second-limit, seed-0 CLI nesting request on a
50×50 mm sheet with lead allowances. Two units occupy one sheet. Standalone
validation agrees exactly with the saved metrics; the preserving project
passes its canonical source comparison. All three original cut contours have
validated lead reservations, with no flags. The SVG and DXF sidecars accompany
the preserved `.lbrn2`; the shortened text-contour lead is reported explicitly.
This is a development correctness check, not a quality benchmark.

All **295 workspace tests**, **26 optimized CLI tests**, and **84 enabled
Chromium/Firefox tests** pass (one native ignored test and four existing browser
skips). Formatting, strict workspace lint and both production builds pass.
[Checkpoint checks](h3-missing-layer-native-20261015/checks.json) record these
counts, exact binary hashes and the L36 validation. All 1,181 frozen corpus
inventory hashes remain unchanged.

## Retained raw evidence

The [raw archive](h3-missing-layer-native-20261015/raw.zip) contains 545 files:
native input/saved XML, UI observations, all per-case inspections/imports/writer
outputs, L36's searched project/sidecars, test logs and script/source snapshots.
Every member passed ZIP CRC and SHA256/size verification before loose raw files
were removed. Paths in case records refer to their repository-relative archive
member names. Extract into a separate evidence directory to inspect/replay them.
Top-level plans, results, label comparisons, checks and screenshots remain direct.
The [integrity manifest](h3-missing-layer-native-20261015/integrity.json) records
every member. Archive size is 10,549,988 bytes; SHA256 is
`38902589b54a10a334db0f149ef2c0bb1b76e2f3300bbbc37091c6e9a515984d`.

The first label-check invocation used a Python without Shapely and failed
before reading inputs; its log remains. Running it in the existing shop
environment completed. An initial authored test assertion attempted to
serialize a non-serializable review type; comparing its closed flags and exact
curves directly corrected the compile error without changing product behavior.

Three frozen native held-out projects remain unevaluated. H3 stays open;
milestone completion remains 20%. No frozen source, label, split, gate,
published v1 result or release state changes.
