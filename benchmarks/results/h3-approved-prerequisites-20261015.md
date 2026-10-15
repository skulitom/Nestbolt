# H3: approved repair prerequisites — 2026-10-15

**Apply Artem's two decisions; H3 remains open on a separate open-path case.**
All eight native text repairs pass complete independent geometry checks. Mixed
active/fixed groups now reject consistently in public import and the lower-level
unit/writer API. The repaired L17 project still cannot nest because its first
standalone open path has a zero-width bounding rectangle. This failure is
retained and is not covered by the text or grouping approvals. Completed
milestone weight remains **20%** (H1 and H6).

[Approval and frozen hashes](h3-reviewed-decisions-20261015.json),
[current reader](h3-reader-20261015T190547Z.json),
[original geometry](h3-geometry-20261015T190554Z.json),
[native text repairs](h3-text-cache-20261015T190617Z.json),
[original writer](h3-writer-20261015T190627Z.json),
[independent unit geometry](h3-unit-geometry-20261015T190640Z.json),
[all 64 prerequisite/writer cases](h3-reviewed-prerequisites-20261015T190641Z/results.json),
[checks](h3-decision-checks-20261015/checks.json),
[raw archive integrity](h3-approved-prerequisites-20261015/integrity.json).

## Decisions and implementation

Artem explicitly accepted a documented repair prerequisite for the eight old
projects containing 122 Text objects without embedded outlines, followed by full
geometry checks on repaired files. Original files, labels, split and failed
checks remain unchanged. Native Save As changes some settings in every repaired
project; it is not evidence of lossless preservation of the original file.
The preserved writer must instead retain the chosen repaired input's settings.

Artem also chose rejection with regrouping instructions for Groups that mix
output-enabled artwork with Tool/output-off shapes. Public import already
rejected these. The lower-level writer still treated the whole group as fixed,
which could repeat active cutting artwork across outputs. Its existing guard
now lives in `Document::nesting_units`, covering all callers. The message asks
the user to ungroup in LightBurn and group movable artwork separately. Inspection
still parses and preserves original XML; no group is automatically split.

The writer-success test fixture's fixed group now contains only Tool children.
Its previously mixed case is retained in a separate fixture testing Tool,
output-disabled and nested variants. Tests also check that rejected CLI inputs
produce no library or sheet files, the MCP session remains usable, and both
browsers discard an invalid replacement and recover on a supported re-import.

## Fresh training and repair evidence

The unchanged training selection contains 56 original projects. Every project
parses and has byte-identical no-op output. Independent comparison passes all
1,550 comparable leaves; maximum bidirectional contour difference is 0.000906 mm,
bounds 0.000712 mm and image corners 0.000029 mm. The same 122 uncached Text
objects remain explicitly omitted, so original geometry is complete for 48
projects, not all 56. No omitted shape is scored as a successful comparison.

The eight existing frozen native repairs supply all 122 caches and retain every
text string. All 477 leaves / 1,223 contours pass the published MIT
`lbrn2-to-svg@0.5.3` oracle with its previously documented, native-verified adapter.
Maximum bidirectional contour difference is 0.000499 mm, bounds 0.000500 mm and
image corners 0.000029 mm. All leaves are compared, including every Text leaf.
The original 0.01 mm limit and 64 samples per contour remain unchanged.

| Public import outcome | Original projects | Native repaired projects |
|---|---:|---:|
| Imported | 45 | 7 |
| Uncached movable text: repair instruction | 6 | 0 |
| Mixed active/fixed group: regroup instruction | 1 | 0 |
| No movable units | 4 | 0 |
| Standalone zero-area open path | 0 | 1 |

The other two originals with uncached text keep that text fixed and issue explicit
repair warnings. Their original geometry is still incomplete; the repaired-file
geometry check is the approved evidence. No claim is made that their native
repair preserves the original settings or nesting membership.

On originals, the lower-level writer now accepts 49 projects and rejects the
same six movable-text cases plus the mixed group. Its 98 diagnostic sheet files
pass the canonical XML diff whitelist. The independent source-reference/GEOS
audit passes all 225 original unit footprints and all diagnostic placements
across those 49 projects. Four have no movable units and receive no layout-validity
credit. Previously accepted mixed-group diagnostic outputs remain historical
evidence, not evidence for the newly approved behavior.

Across originals and native repairs, 112 diagnostic sheet files pass canonical
diff checks against their own input bytes. Fifty-two projects produce
independently valid layouts covering 362 units. Repaired L17 is a clear rejection,
not a passing layout. All 64 cases preserve original input bytes and have recorded
inspection, import, writer results and hashes; none crashes or times out.

## Verification and remaining work

All **290 workspace tests pass** (one existing ignored), **25 optimized CLI tests
pass**, and **82 enabled browser tests pass** (four opt-in skips). The MCP tests
use real stdio sessions. Formatting, strict workspace lint across all targets,
native/diagnostic/WASM builds and product/test TypeScript pass. The initial
compile failure from one remaining duplicate guard call is retained separately;
it was removed before the full checks. Native CLI SHA-256 is
`2788c895294db86ad4ced3c303c5db87a9fdc866dc92a871d47105dc8cb400f1`.

Builds and tests use CCD1. Guarded diagnostics use separate CCD0 physical cores,
at most four child processes; independent oracle/GEOS comparisons use core 8.
All source, executable and runner guards pass. A 34,067,533-byte raw archive
preserves 4,354 members with CRC and SHA-256 checks, including native results,
normalized oracle inputs, SVG references, runner snapshots and original logs.
Six check logs have their own verified archive. The frozen shop manifest remains
`02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`.

Existing five-project native opening, positioning and settings-dialogue evidence
remains separate. No native application files, source labels or earlier failures
were rewritten. No held-out geometry, new final acceptance, release or registry
publication is involved. Next address L17's standalone open-line footprint and
finish the requirement-by-requirement H3 audit; H4 quality work then resumes.
