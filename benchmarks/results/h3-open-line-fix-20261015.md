# H3 — open strokes and the completed training audit

The repaired L17 project now imports, nests **73 units on one 900 × 900 mm sheet**,
and exports its original editable paths. All **32 open paths remain open** in
LightBurn Pro 2.1.01. The full training and repair checks pass. **H3 remains open**
because its three frozen native held-out projects have not been evaluated;
completed milestone weight remains **20%**.

## Change and retained failure

Standalone lines previously failed when a bounding-box axis was zero, although
the same lines already received protection inside groups. The first correction
also covered widths below the validator grid, but an actual L17 search then
failed on its fourth unit: seventeen almost-horizontal lines have a height of
about 0.000019 mm, which collapses in the solver's floating-point representation.
The [failed attempt](h3-open-lines-20261015T193120Z/failure.json) and its inputs,
source snapshot and diagnostics remain in the raw archive.

The final rule widens each bounding axis to at least two curve tolerances,
symmetrically, adding at most one tolerance on either side. The minimum is two
validator grid units. This applies consistently to standalone strokes, grouped
strokes and attachment bounds. It changes collision footprints only. Original
vertices, open-path primitives, groups and cut settings remain in the preserved
XML; protective rectangles never become exported cuts.

The authored MIT fixture covers a vertical stroke, a mirrored almost-horizontal
stroke, a near-vertical transform and a diagonal. Core checks exercise rotations,
mirroring, identity writes and very small tolerances. Actual CLI, MCP stdio,
Chromium and Firefox tests import, nest, validate and export it.

## Current evidence

| Check | Result |
| --- | --- |
| Original training inspection/no-op | 56/56; all 64 original/repair inspection payloads are byte-identical to the previous approved-prerequisite audit |
| Original independent unit geometry | 225/225 across 49 writer projects; maximum boundary difference 0.000579 mm |
| Approved native repairs | All eight import; 477 leaves, 1,223 contours and 122 Text leaves pass; maximum point/bounds difference below 0.000500 mm |
| Repaired unit geometry | All 210 units pass at diagnostic and public-import tolerances |
| Combined diagnostic writer | 114 allowed canonical sheet diffs; 53 nonempty projects and 435 units independently validate |
| L17 actual search | 73/73 on one sheet, spacing/edge spacing 1 mm, seed 0, 60 s budget; returned in 8.736 s; native validator and independent GEOS reference placement checks pass |
| Public import disposition | 45 original imports; six uncached movable-text prerequisites, one mixed-group rejection, four no-movable-unit rejections; all eight repaired imports succeed |
| Regression checks | 293 workspace tests, 26 optimized CLI tests and 84 enabled browser tests pass; one existing ignored test and four opt-in browser tests remain skipped |

All 1,550 comparable original leaf results from the previous independent reader
audit remain applicable: source bytes and every inspection payload are unchanged.
The repaired leaves were compared afresh with the published MIT oracle. The
public footprint comparison reaches 0.005 mm on a flattened circle, within the
unchanged 0.01 mm gate. There is no overlap or outside area in either actual
search's independent reference placement check.

Compared with the previous checkpoint, 61/64 complete diagnostic writer payloads
are identical. L17 changes from rejection to support; repaired L21 and training
`native/lb-14.lbrn2` gain protection for narrow grouped strokes. Both are covered
by the new independent geometry checks. Empty/fixed-only diagnostic sheets do
not receive validity credit.

## Native verification

The authored search and L17 search both open without warnings and save separately
in hidden Anode seat 2. [Native verification](h3-open-line-native-20261015/verification.json)
checks **93 leaves**, with maximum point difference **0.000516 mm** and bounds
difference **0.000503 mm**. The four authored paths and 32 L17 paths remain open.
Overall selected bounds, including the sheet outline, match the 900 × 900 mm
sheet exactly in LightBurn's fields. Individual paths are checked through the
native-save geometry, not separate per-line field measurements.

All original L17 settings remain canonically equal. LightBurn adds defaults to
the intentionally minimal authored CutSetting; every supplied value is retained.
The [five previously native-checked layouts](h3-open-line-native-20261015/prior-five.json)
also revalidate with this build. Re-exports differ only in XML line endings and
top-level numeric replay by at most **2.274e-13 mm**; every other canonical XML
element is equal. The initial stricter byte/canonical comparisons remain in the
archive. This does not rerun or replace their 16 native unit measurements and
34 settings-dialog comparisons.

The startup low-resolution notice was dismissed with Ignore. The desktop was
temporarily enlarged, then restored to 1280 × 720. No device settings changed;
the owned LightBurn window was closed and the lease released. Screenshots:
[authored](h3-open-line-native-20261015/authored-opened.png),
[L17](h3-open-line-native-20261015/L17-opened.png).

L17 derives from [qbalsdon/etcher Grid.lbrn2](https://github.com/qbalsdon/etcher/blob/3e4f8a30d77926dc07d015eb37e7c1ad7c436b82/Grid.lbrn2)
under its [MIT licence](https://github.com/qbalsdon/etcher/blob/3e4f8a30d77926dc07d015eb37e7c1ad7c436b82/LICENSE).
The other repaired inputs retain their frozen per-file attributions. The new
fixture is original Nestbolt MIT material.

## H3 requirement audit and limits

Reader, no-op, preserving writer, validity and public-surface requirements are
evidenced for the training scope under reviewed decisions 5–6. The five-project
native requirement already passes, with current revalidation above. Three native
held-out projects remain sealed: `lb-01`, `lb-06` and `lb-08`. Only their manifest
metadata and integrity hashes were inspected. Consequently this is not full H3
acceptance and does not change the milestone weight. H2's separate held-out
denominator clarification remains pending.

The original projects, labels, split and failed results remain unchanged. The
manifest still hashes to `02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`;
all 1,181 inventory files match. No held-out geometry, new final quality run,
solver-wide default, release or published v1 claim changed.

The [machine report](h3-open-line-fix-20261015.json) links every result. The
[raw archive integrity record](h3-open-line-fix-20261015/integrity.json) verifies
2,016 archived members by CRC and SHA-256, including failures and source snapshots.
[Final check logs](h3-open-line-final-checks-20261015/checks.json) also pass formatting,
strict lint, native/WASM builds and product/test TypeScript. Builds/tests used
CCD1; audit subprocesses used distinct CCD0 physical cores, with the independent
checks and searches sequentially on CPU 8 and LightBurn on CPU 4. Guarded runs
retained unchanged product sources and executables.
