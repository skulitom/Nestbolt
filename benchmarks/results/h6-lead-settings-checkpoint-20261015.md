# Native mixed lead settings and precision — 2026-10-15

LightBurn's lead-length field rounds 1.162 mm to 1.2 mm. Nestbolt now constructs
and checks lead trials at native 0.1 mm precision, and requires angle settings
with at most two decimal places. Reports and browser tooltips show the exact
one-decimal length. This supersedes the micrometre setting assumption in the
preceding public-surface checkpoint; the original report and failed assumption
remain unchanged.

## Scope and provenance

All inputs are repository-authored MIT geometry. No corpus geometry, labels,
held-out evaluation, release or registry action was used. The initial CLI
preparation at source digest `618a043fc09685aefda2ca82c25c42d3fbfe7188551df2657ac884a7b9cfae29`
searched two copies of the authored leads fixture on a 60 × 35 mm sheet, with
0.2 mm kerf, 0.2 mm spacing, 1 mm margins, seed 0 and one repeatable work-second.
Both line and arc jobs had six contours, four reservations and two tiny-hole
flags. The original straight/arc hole lengths were 1.771/1.162 mm.

The revised core independently validates and exports both styles on the retained
actual searched arc layout, with no movement or solver rerun. All CUT path
attributes, including starts, remain identical. Source digest is
`35ea0b8a7c616d733793c8c03529109863483d54d8d1c8106f89fd0f709c91f6`;
the native CLI SHA-256 is
`bed1c773d1694c38d509dafc6c5677dc88150e8dabb602365bdf94cf96017b6c`.
The committed source digest is
`d08735b62e2becf91b0af1022e2a3b81cc252e62551d32c94abb93f58b0e3a23`:
the unchanged `Sparrow_LICENSE` and `sheets/vstrip.rs` have CRLF in the working
checkout and LF in Git; all other source bytes match. Both digests are retained.
The revised hole settings are 1.7 mm line and 1.2 mm arc. Trial rounding is
performed before clearance checks: 1.2 mm fits at an earlier arc trial than
the former unrounded sequence. Original placed material remains 391.68 mm².
Searches and bounded CLI/audit processes use CPU 0; builds/tests use CCD1.

[Initial preparation](h6-lead-settings-20261015T102840Z/preparation.json) and
[revised validation/export](h6-lead-settings-20261015T102840Z/revised-2/preparation.json)
retain commands, source/binary hashes and input/output hashes.

## Native workflow and evidence

In hidden Anode, LightBurn Pro 2.1.01 imported the original searched SVG.
Ungrouping exposed six closed contours and four red review paths. Outer contours
remained C00; the larger holes were assigned C04; tiny flagged holes C03.
LEADIN/C02 output was disabled for the original precision probe and its review
objects were then removed through LightBurn's layer controls. The revised
exports have the same CUT geometry, so the native projects exercise those exact
contours without stale review objects. No native XML was edited to set options.

| Native layer | Straight case | Arc case |
| --- | --- | --- |
| C00 outer contours | 3.0 mm, +45°, line | 3.0 mm, +45°, arc |
| C04 larger holes | 1.7 mm, −90°, line | 1.2 mm, −90°, arc |
| C03 flagged tiny holes | Cut enabled, native lead disabled | Cut enabled, native lead disabled |

Lead-out and overcut remain off. Choose best starting point is off; Choose best
direction is on. The previews show the two hole leads within the hole waste and
outer leads clear of neighbours. All four tiny-hole occurrences across the two
previews have no lead. These are previews, not machine cuts or cut-order approval.
The saved projects were reopened for retained captures.

- [Straight native preview](h6-lead-settings-20261015T102840Z/line-native-preview.png)
- [Arc native preview](h6-lead-settings-20261015T102840Z/arc-native-preview.png)
- [Original rounding observation](h6-lead-settings-20261015T102840Z/arc-rounded-input-observation.json)
- [Independent native audit](h6-lead-settings-20261015T102840Z/native-audit-20261015T105414231690Z.json)

The unmodified MIT lbrn2-to-svg package reads normalized copies of the saved
projects. All 12 closed contour shapes, starts and layer assignments match the
public SVG exports; maximum geometry and start error are both 0.00000224 mm,
well within the 0.01 mm vector comparison threshold. The only removed transform
is LightBurn's common import translation. Eight native lead traces match a
reserved direction within 0.026764 mm using the declared 0.075 mm raster
tolerance. The raster check samples expected paths against native cut pixels;
it supports visual inspection and does not replace independent vector clearance.

All ten optimization checkboxes are unchanged. Owned LightBurn instances were
closed, the hidden display restored to 1280 × 720 at 100%, and the lease released.

## Verification and retained failures

The revised core passes 16 focused lead tests, both public-library tests,
the MCP lead integration test and all 22 optimized CLI feature tests. Production
WASM/browser build, strict Clippy, formatting and schema checks pass. Four
focused browser tests pass (lead and common-line cases in Chromium and Firefox),
including rejection of over-precise angles and exact 1.2 mm shortened reporting.
These are focused checks, not a repeated full workspace/browser suite.
All 1,181 frozen corpus hashes and the manifest hash remain unchanged; no
held-out file contents were interpreted. [Checks and artifact inventory](h6-lead-settings-20261015T102840Z/checks.json).

The evidence retains the original 1.162→1.2 mm native input and saved project.
The first recheck harness expected 1.1 mm after flooring the old accepted trial;
the new planner correctly accepts a 1.2 mm earlier trial. Its incomplete
`revised/` output remains, followed by successful `revised-2/` output.
An initial audit import failed because the independent Python environment lacks
psutil; removing an unnecessary preparation-module import fixed it. The next
attempt found missing saved screenshots: oversized capture writes had failed.
The original stored captures were saved in checked chunks and both final
projects reopened for new captures. A retained failed raster audit excluded
dark-red cut pixels where traversal overlays the cut. Observed cut/traversal
RGB was 110/57/57, versus 181/127/127 for traversal alone; the corrected mask
counts dark cuts without including traversal alone. Physical tolerance and
geometry comparisons were unchanged. All failures and the passing audit remain.

H6 is still incomplete: multipart planning, broader independent final
coverage/owner/source-attachment checks and material-cost measurements remain.
Only N0/H1 is complete; overall milestone progress stays **15%**.
