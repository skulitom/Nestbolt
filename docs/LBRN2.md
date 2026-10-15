# LightBurn project format: local observations

Probed with the installed LightBurn **2.1.01** in the hidden Anode desktop on
2026-10-13, using the `No Machine` device. These are saved projects and observed
UI behaviour; no LightBurn executable was inspected or decompiled. The title bar
says **Pro**, although the earlier research described the installation as Core.
No edition change, activation, update or trial reset was performed here.

The starting reference is [V1_1_RESEARCH.md section 2](V1_1_RESEARCH.md#2-lightburn-lbrn2).
The probes below confirm only their stated observations. Historical checkpoints
retain their original outcomes. Current approved repair prerequisites are below;
the complete gate status is tracked in [STATUS.md](STATUS.md).

## Required preparation for older or mixed projects

Artem approved these requirements on 2026-10-15 in
[reviewed decisions 5 and 6](PLAN_V1_1.md#10-reviewed-decisions).

- **Text without embedded outlines:** open the project in LightBurn, verify that
  the text looks correct, and save a separate copy; alternatively convert the
  text to paths. Import that prepared copy into Nestbolt. A font name alone does
  not establish the original glyph geometry, so Nestbolt does not substitute
  fonts or invent missing outlines. Keep the original project. LightBurn may
  normalize settings during its save; review those settings before cutting.
- **Groups mixing active and fixed artwork:** ungroup them in LightBurn, then
  group the movable artwork separately from Tool/output-disabled shapes. Import
  the regrouped project. Nestbolt rejects the mixed group before nesting; it
  does not split the group automatically or place its active cuts on every sheet.

Standalone open paths can be nested without grouping. A bounding-box axis narrower
than two curve tolerances is widened symmetrically to that width (at least two
0.000001 mm validator grid units). The same rule protects grouped
strokes and engraving attachment checks. This is collision geometry only:
the original open path, vertices, settings and editability are preserved in the
LightBurn output; the protective rectangle is never exported as a cut.

The [eight-project native repair audit](../benchmarks/results/h3-text-cache-20261014T005902Z.md)
retains the original 122 missing text caches and verifies every repaired leaf
against the independent reader. Its historical “not approved” status is
superseded by Artem's decision; its measurements, original failures, frozen
sources and labels remain unchanged. Reader inspection and no-op preservation
remain available even for projects that require preparation before nesting.

## Coordinate systems and origins

The original [geometry.svg](../benchmarks/datasets/shop/probes/geometry.svg)
contains a 40 × 25 mm rectangle, a 10 × 10 mm inner rectangle, an 8 mm circle,
and an asymmetric cubic outline. Importing it produces three Path shapes and
one Ellipse. LightBurn positions the imported drawing at the workspace centre.

Four projects were saved after changing only Device Settings → Origin in the UI:

| Device origin | MirrorX | MirrorY | Saved file |
| --- | --- | --- | --- |
| Bottom left | False | False | [project](../benchmarks/datasets/shop/probes/origin-bottom-left.lbrn2) |
| Top left | False | True | [project](../benchmarks/datasets/shop/probes/origin-top-left.lbrn2) |
| Top right | True | True | [project](../benchmarks/datasets/shop/probes/origin-top-right.lbrn2) |
| Bottom right | True | False | [project](../benchmarks/datasets/shop/probes/origin-bottom-right.lbrn2) |

The serialized Shape subtrees, including XForms, stay identical across all four
files. Changing origin reflects the drawing displayed by LightBurn. Do not
interpret these flags as per-shape transforms or apply them twice. The probe's
workspace was 300 × 200 mm; that device size is not a root project attribute.
The per-sheet writer's normalization must therefore be checked explicitly in
LightBurn for both default and mirrored origins.

For the bottom-left project, the rectangle vertices retain the SVG x coordinates
20…60 but y becomes −30…−55. Its XForm is `1 0 0 1 90 137.05078`.
The circle instead retains an Ellipse with `Rx=Ry=4` and XForm
`1 0 0 -1 138 95.050781`. This directly demonstrates that either geometry or the
transform can carry the input's y inversion. The matrix convention remains
`x′=a*x+c*y+e`, `y′=b*x+d*y+f`, with local transforms before parent transforms.

## Shared paths, groups and bitmap data

In the origin probes, the 40 × 25 mm rectangle defines `PrimID=0` as
`LineClosed`. The inner 10 × 10 mm rectangle also uses `PrimID=0` but a different
`VertID`, and omits PrimList. Primitive and vertex sharing must be resolved
**independently**, across the document rather than only within a group.

[features-before-leads.lbrn2](../benchmarks/datasets/shop/probes/features-before-leads.lbrn2)
was made by grouping the imported shapes, duplicating, rotating and reflecting
the duplicate in LightBurn, adding editable text, and importing and duplicating
the original MIT [checker bitmap](../benchmarks/datasets/shop/probes/checker.png).

- The original group has identity XForm. Its reflected/rotated copy has
  `-0.86602539 -0.5 -0.5 0.86602539 233.0192 88.397461`. Children keep their own
  transforms and reused geometry references.
- The Text is `Str="Nestbolt probe"`, `H="25"`, `HasBackupPath="1"`, and a
  BackupPath is present. Preserve editable text attributes and its backup geometry.
- Three Bitmap shapes share `SourceHash="0"`. Only the first contains `Data`.
  Their translations are (150,100), (180,100) and (200,100) mm; dimensions are
  8.4656086 × 6.3492064 mm. The saved source File path is metadata, not a dependency
  needed to render the embedded image. Zero is a valid shared identifier.

## Layer settings and leads

The CUT layer was set to 1,200 mm/min, 35% power and 0.2 mm outward kerf in the UI.
It serializes as `speed=20`, `maxPower=35`, `kerf=0.2`: speed is mm/s even when the
UI is displaying mm/min. Keep these settings unchanged during nesting.

The following are CutSetting child elements, each with a `Value` attribute:

| UI setting | XML field | Observed value |
| --- | --- | --- |
| Add Lead-In | leadIn | 1 |
| Lead length | leadLength | 3 |
| Lead angle | leadAngle | 45 |
| Line style | leadStyle | line |
| Arc style | leadStyle | arc |

See [line probe](../benchmarks/datasets/shop/probes/features-line-leads.lbrn2)
and [arc probe](../benchmarks/datasets/shop/probes/features-arc-leads.lbrn2).
Lead-out remains off. No lead geometry is serialized as extra Shape elements.
The arc probe also has a native Rect on T1: `CutIndex=30`, `W=52`, `H=26`,
XForm `1 0 0 1 226 26`, plus a `CutSetting type="Tool"` with index 30.

The local 2.1.01 mode dropdown contains Line, Fill and Offset Fill. In
[layer-modes.lbrn2](../benchmarks/datasets/shop/probes/layer-modes.lbrn2), Fill
followed by Line is `CutSetting type="Scan"` with a child `SubLayer type="Cut"`
(`index="1"`), not `Scan+Cut`. Unit classification must include a cutting
sub-layer when deciding whether a closed contour is a cutting unit. Offset Fill
serializes as `type="Offset"`.

**Layer identity also includes the setting family.** This file has both
`CutSetting index=0` (CUT, 35%, 20 mm/s, kerf and leads) and `CutSetting_Img index=0`
(Image, 20%, 100 mm/s). A Bitmap's `CutIndex=0` belongs to the image setting; a
Path's `CutIndex=0` belongs to the vector setting. An index-only map would lose
settings. Preserve both and select by shape type.

## Explicit start points

The Set Start Point tool does **not** reorder the path's vertices in the local
probe. Choosing the outer rectangle's opposite corner adds `StartV="2"` to that
Path Shape. The two [before](../benchmarks/datasets/shop/probes/start-before.lbrn2)
and [after](../benchmarks/datasets/shop/probes/start-after.lbrn2) projects differ
only by that attribute and the Thumbnail. Its VertList/PrimList remain shared with
the grouped copy. Preserve StartV during N2 round-trip; when choosing new starts
for lead allowances, a reader must honor this explicit override rather than assume
the first vertex is always the start. This corrects the research's first-point
inference for files with an explicitly selected start.

## Remaining format probes

- Output-off shapes; legacy combined `Scan+Cut` from public projects.
- Verify the mirror normalization with actual nested outputs during H3.
- Compare all public/local geometry with the independent published MIT oracle.

## Export palette and DXF variants

The [N1 product export check](../benchmarks/results/h2-lightburn-20261013T195848Z.md)
applies the palette below to Nestbolt's AC1021 and SVG outputs. Both native saves
confirm indices 0/1/2/30 and a Tool setting for 30. Ten nested exports retain
their analytic dimensions within 0.000033 mm in native saved geometry. Two spline
width fields differ by 0.003275 mm despite the retained curves; native UI bounds
are not assumed to be exact analytic bounds. This is separate from H3 project
preservation, which remains pending.

Local exports [palette.svg](../benchmarks/datasets/shop/probes/palette.svg) and
[palette.dxf](../benchmarks/datasets/shop/probes/palette.dxf) establish:

| LightBurn layer | RGB | DXF ACI |
| --- | --- | --- |
| 00 / CUT | #000000 | 7 (adaptive black/white) |
| 01 / COMMON | #0000ff | 5 |
| 02 / LEADIN | #ff0000 | 1 |
| T1 / SHEET | #f36926 | 30 (approximation) |

The installed `palette.json` confirms the first three RGBs. T1 is outside that
30-entry file; the native SVG export supplies its RGB. Tool geometry is exported
with `display:none` in the SVG.

**ACI 30 is not a lossless T1 round-trip.** Re-importing LightBurn's own DXF puts
the tool rectangle on C05 (orange), as shown by
[palette-dxf-reimport.lbrn2](../benchmarks/datasets/shop/probes/palette-dxf-reimport.lbrn2)
and its screenshot. With **Allow Importing to Tool Layers off** (the installed
default), adding DXF group 420 true colour does not fix the tool-layer
assignment: [palette-truecolor.dxf](../benchmarks/datasets/shop/probes/palette-truecolor.dxf)
has two rectangles with exact `#f36926` true colour, one with entity ACI 30 and
one BYLAYER (layer ACI 30, also exact true colour). Their
[native re-import](../benchmarks/datasets/shop/probes/palette-truecolor-reimport.lbrn2)
assigns C05 and C13, respectively, both cutting layers.

**Follow-up with the option on:** re-importing that same unchanged DXF into a
new project assigns the explicit-ACI rectangle to C05, but the BYLAYER rectangle
to **T1**. See [the native save](../benchmarks/datasets/shop/native/tool-layer-enabled.lbrn2)
and [screenshot](../benchmarks/results/n0-native-20261013/tool-layer-enabled.png).
Thus exact layer RGB with BYLAYER entities can preserve the tool classification
when the user enables this import option. Do not promise this for an explicit
ACI 30 entity or with the option off. Use the exact RGB in Nestbolt exports and
explain the required LightBurn option. `.lbrn2` preserves T1 directly.
The setting was restored to off after this probe.

The export dialogue offers Illustrator, AutoCAD Legacy DXF, AutoCAD Modern DXF
and SVG. The observed Modern DXF is **AC1021 with `$INSUNITS=4`**, explicitly mm.
The [Legacy export](../benchmarks/datasets/shop/probes/palette-legacy.dxf) is
**AC1009, also with `$INSUNITS=4`**. Do not treat LightBurn DXFs as unitless;
check the actual header. These observations correct the older blanket inference
in the research for the locally installed version and default settings.

Screenshots are under [n2-probes-20261013](../benchmarks/results/n2-probes-20261013/).

## Real-design native corpus (N0 collection)

The [native recipe](../benchmarks/datasets/shop/native/recipe.json) records 15
licensed real designs imported, duplicated, positioned, saved and exported in
LightBurn 2.1.01. Each includes an original feature coupon prepared from the
above native probes, with Cut, Score, Fill, Image and Tool content; its source
licence and modification notice accompany every derivative. These are 15 native
projects, 15 SVGs, 15 ordinary legacy DXFs and five additional legacy DXFs with
Convert Arcs to Lines enabled. The prepared coupon input is explicitly identified
as agent-authored preparation, not counted as a native corpus design.

The five line-mode legacy DXFs fail ezdxf 1.4.4 (including recovery) with
`DXFStructureError: Expected DXF entity POLYLINE or SEQEND`. Their original native
bytes are retained. The raw record stream has unequal POLYLINE/SEQEND counts;
it also retains CIRCLE records despite the selected line conversion option.
This is an observed writer output, not a Nestbolt import result. The ordinary
15 DXFs parse; at initial collection their bounds agreed with the corresponding
SVG viewBoxes within 0.000054 mm. After the pre-freeze coupon correction described
below, actual DXF/SVG vector bounds agree within 0.000008 mm. SVG viewBoxes also
include bitmaps absent from DXF, so full viewBox bounds are retained as a separate
observation. This is a bounding-box check only, not full contour fidelity.

The installed import/export settings observed for these saves are auto-detected
DXF units, mm fallback, 0.010 mm auto-close, SVG 96 DPI with auto-detection, and
0.050 mm output curve tolerance. Export Arcs was selected for the ordinary
exports, then Convert Arcs to Lines for the five variants, then restored.
See [the collection report](../benchmarks/results/n0-native-20261013.md), including
settings screenshots. All 50 native files now have labels; public-project labels
and the frozen split remain before H1.

## Nested Text BackupPath is a world-space cache (local 2.1.01 observation)

The [label review](../benchmarks/results/n0-labels-20261013.md) found a small
coupon/source overlap in four wide native samples. Their coupon group X
translation changed from 1200 to 1600 before another native Save As/export.
The Text child's XForm stayed `1 0 0 1 80.858231 43.830421`, but its BackupPath
XForm changed from `1 0 0 1 1280.8583 43.830421` to
`1 0 0 1 1680.8583 43.830421`. The group and cached backup each moved +400 mm;
the local Text transform did not. Native SVG text outlines confirm the resulting
world position. This observation is limited to these native samples/version.

Do not treat this cached BackupPath as an ordinary child path and apply its
ancestor transforms again. The published `lbrn2-to-svg@0.5.3` converter does so
for this nested text, causing an oversized text position/bounds. It also warns
and skips Polygon shapes, compact LineOpen primitives, Text without usable
backups and shared bitmaps whose Data resides on another shape. Returning an SVG
does not establish complete independent geometry. H3 needs explicit coverage of
these oracle limitations using the native exports and local probes.

Native resaving also renumbered shared-list IDs, serialized default Group
CutIndex=0 and regenerated Thumbnail. After resolving those exact changes,
all geometry/settings are equal except the intended coupon translation and
updated text cache. Original bytes are in commit `8bbc1fb`; old/new checksums
are retained in the recipe. [Corrected native audit](../benchmarks/results/n0-native-corrected-20261013.json).

## Public-project reference normalization and native export limits

The [44-project N0 review](../benchmarks/results/n0-public-labels-20261013.md)
compared the unmodified published package, with explicitly normalized reference
inputs, against native 2.1.01 SVG exports. In the package, SVG Y reflection is
applied at every Group as well as every leaf. Multi-child nested Groups therefore
have an extra reflection; a matching overall bounding box can conceal the error.
Reference-only conversion composes transforms into leaves and omits Group
wrappers. Original XML membership is retained separately for labels. This is not
an implementation or H3 acceptance of the Nestbolt reader.

After normalization, all 44 exported vector sets and all 151 image rectangles
agree within 0.01 mm with native SVG. The reference manifest documents compact
primitive expansion, shared bitmap data, regular Polygon support and Text cache
promotion. Hidden layers (`hide=1`) are omitted entirely from native SVG; disabled
output alone is exported with `display:none`. Fixed geometry must be retained
from the project even when it is absent from the visible reference rendering.

Older public text can lack BackupPath. Native re-save supplies a cache for these
references, but the original remains unchanged and its missing-cache warning is
part of the label. The L40 Sans Serif warning does not imply altered geometry:
its existing backup and native SVG bounds agree. A font-dependent approximation
must not be reported as exact cached geometry.

Native save of legacy L42 changes `Scan+Cut` to `Scan`. Thus native re-save is
useful as geometry evidence, not a canonical preservation oracle. Original layer
state, including legacy mode strings and unknown settings, remains authoritative.
The reference corpus also demonstrates mixed fixed/movable children in L11:
keep the entire rigid Group fixed and warn, rather than move a disabled child.
L17's 32 axis-aligned open Paths have degenerate bounds; retain and report them,
requiring grouping or an explicit nonzero proxy before nesting.

## Reader implementation checkpoint — 2026-10-13

The shared Rust `lightburn::Document` reader preserves the entire original XML
and separately builds a scene in serialized millimetres/Y-up coordinates. It
reads versions 0 and 1, resolves vertex/primitive IDs independently (including
forward references), resolves embedded bitmap sharing, applies group transforms,
honours StartV and distinguishes vector/image settings with the same index.
Tool/output-off content is marked fixed; a mixed rigid group remains fixed.
Kerf is reported without changing spacing. No external image paths or fonts load.

[All 56 training projects](../benchmarks/results/h3-reader-20261013T220428Z.json)
parse and retain byte-identical no-op output. The maximum reader time is 0.252 s.
[Independent comparisons](../benchmarks/results/h3-geometry-20261013T220610Z.json)
cover 1,550 leaf shapes and 2,046 contours: 64 samples per contour in each
direction, bounding boxes and bitmap corners, all below 0.01 mm. The greatest
contour distance is 0.000906 mm. The published MIT converter remains unmodified;
the test adapter records the known reference limitations described above.

**New format correction:** compact vertices can omit a handle's zero x or y
coordinate. `V265 0c0x267.76141c1x1`, for example, has outgoing handle
(267.76141, 0); the lone incoming `c1x1` is the missing-handle sentinel. A lone
`c1y154.76143` has x=0. Both the initial product reader and the published oracle
misread these cases. The first comparison's eight failures remain recorded.
The repaired reader and test normalization also agree directly with LightBurn's
frozen SVG exports for all eight affected shapes (maximum 0.000283 mm).

For cached Text, the reader applies the Text's transform chain to backup-local
vertices. The cached BackupPath XForm matches that world transform in the native
samples and must not be applied again. Applying the live Text chain also makes
the inspection geometry follow a moved group without rewriting child XML.
The later controlled native writer probes below verify moved/rotated cached Text;
the full H3 check on actual searched layouts remains pending.

Eight older training projects contain 122 Text shapes without backups. The reader
retains their XML, reports a native re-save instruction and marks their geometry
incomplete; it does not invent bounds. Thus 48 projects have complete compared
geometry, and full H3 reader acceptance remains open. This is a core inspection
API and diagnostic example. The later checkpoints below add nesting units,
per-sheet preserving writes and controlled native opening checks; UI/CLI/MCP
integration and full H3 native acceptance remain pending.
See [the complete checkpoint](../benchmarks/results/h3-reader-checkpoint-20261013.md).

## Unit assembly and preserving writer checkpoint — 2026-10-13

The core now assembles rigid units and writes version-1 sheet files while keeping
unrelated XML byte-for-byte. Fifty training projects pass identity writes and
100 independently checked canonical sheet diffs; six refuse incomplete movable
text. All 227 unit footprints match the independent reference within 0.000579 mm.
Two projects with uncached text can still write because that text is fixed; this
does not establish its geometry. Four outputs have no movable units.

Only top-level placement matrices, omitted units, required shared definitions
and the optional T1 outline change. Fixed content remains on every output.
This is still a core API and diagnostic, with legacy conversion, actual search,
public surfaces and native origin/settings checks pending. See the
[complete writer checkpoint](../benchmarks/results/h3-writer-checkpoint-20261013.md).


## Controlled native writer probes — 2026-10-13 UTC

[Ten native checks](../benchmarks/results/h3-native-probe-20261013T224854Z.md)
cover moved/rotated Text, a mirrored group, an isolated shared Bitmap copy,
all four saved origin flags and two source-origin variants under a top-right
device. Each opens without warning. Native fields differ from analytic placement
by at most 0.004558 mm; independently converted native saves agree over 13 leaf
shapes and 50 contours within 0.000499 mm.

Text follows the live transform even when its BackupPath XForm remains stale.
LightBurn refreshes that cache on Save As. The isolated second Bitmap renders
with the re-homed Data, and its native saved Data is identical.

Root origin flags are retained by Nestbolt. Opening either source-origin variant
in the top-right device still shows the expected numeric position; the display
reflects with the active device axes. Native Save As writes the active device's
flags. A flag mismatch marks the project dirty without a warning. Thus placement
coordinates must not receive another reflection merely from these root flags.
This does not promise identical physical screen orientation across device origins.
The original bottom-left device origin was restored and verified after testing.

The product's XML diffs preserve all settings. Native Save As removes unused
settings; in the bitmap-only file it also changes image-layer priority 3 to 0.
That retained-settings mismatch remains explicit in the failing overall probe
report, alongside all ten passing geometry checks. The native serializer is not
the product's canonical preservation oracle. Full H3 still requires five actual
searched projects, before/after cut-settings dialogues, complete reader coverage,
legacy output and all three public surfaces.


## Public import/search/export checkpoint — 2026-10-13 UTC

The [surface checkpoint](../benchmarks/results/h3-surfaces-20261013T233512Z.md)
connects original project XML to the shared Library/Request model, CLI direct
`.lbrn2` nesting, MCP tools and browser import/download. Disconnected group
components remain one rigid unit and contribute to previews and area estimates.
Each exported sheet keeps the original settings, editable artwork, fixed
inactive shapes and shared-resource definitions. T1 is on by default and can
be disabled. Validation re-derives geometry from source XML, so editing cached
preview polygons cannot bypass the check.

The original MIT integration fixture contains a disconnected group, cutting
rectangle with attached cached Text and Bitmap, another shared Bitmap copy,
three operation-layer families, a fixed Tool rectangle and a mirrored root.
CLI, MCP, Chromium and Firefox exercise real search and preserving sheet files.
This does not replace the five-project native H3 check. Legacy conversion,
uncached movable text, mixed fixed/active groups and native cut-settings-dialogue
comparisons remain open. Mixed groups now fail in public imports with a repair
instruction; the core diagnostic's older whole-group-fixed policy alone is not
enough to validate active fixed artwork on every sheet.

## Legacy conversion and native element order — 2026-10-14 UTC

The [legacy checkpoint](../benchmarks/results/h3-legacy-20261013T235803Z.md)
uses the original MIT features probe saved by LightBurn 2.1.01 as `.lbrn`.
Typing that extension in Save As produces `FormatVersion="0"`, with 285 `V`
and 285 `P` elements including editable Text's BackupPath. Merely changing the
root version loses paths in native LightBurn; the failed variant is retained.

The writer now adds equivalent VertList/PrimList data, uses the native `c0x1`
and `c1x1` absent-handle markers, and writes FormatVersion 1. It preserves the
original V/P XML, unknown attributes and comments. Only recognized Shape trees
and Text backups are converted; opaque project metadata stays untouched. A
missing format attribute is treated as legacy. The original document no-op
remains byte-identical, and converting an already modern sheet is idempotent.

Native saves of the original legacy project and the converted identity sheet
are canonically equal across the **entire project**. A real CLI search places
all six units on one sheet, with independent overlap/outside ratios zero.
Three native reference comparisons cover 37 leaves and 85 contours; maximum
bidirectional point difference is 0.000497 mm, below the 0.01 mm gate tolerance.

This check exposed an existing outline bug: adding T1 after Notes makes
LightBurn silently omit the setting and rectangle. New settings now precede
shapes, and the outline follows existing shapes before trailing metadata. The
corrected native UI shows seven objects and the complete 300 × 200 mm outline.
The failed file and report remain beside the correction. Native Save As changes
only the **newly generated** T1 name from SHEET to T1 and supplies priority 4;
all four original settings remain canonically identical. The initial strict
comparison of the new default fields is retained separately and documented.

CLI, MCP, Chromium and Firefox exercise legacy import, real nesting and modern
exports. Legacy conversion is now implemented; uncached movable text, mixed
fixed/active groups and the five-project native settings-dialogue check still
prevent H3 completion. Neither this authored probe nor these checks touch the
frozen corpus or change published v1 results.


## Five searched native projects — 2026-10-14 UTC

The [five-project native check](../benchmarks/results/h3-lightburn-20261014T001636Z.md) now passes on four frozen training
projects and the original MIT top-right-origin probe. Each actual CLI search
produces one independently valid sheet with an allowed canonical XML diff.
All 16 placed units match LightBurn's position/size fields within 0.003652 mm.
All 23 original setting instances remain canonically equal through native
baseline and output saves; 34 dialog-page comparisons check 648 controls.
The four native design projects include cached editable Text, shared vectors,
three shared Bitmaps, groups, Cut/Score/Fill/Image settings, kerf and arc leads.

Native baseline/output geometry produces 409 independent leaf comparisons and
537 contours; maximum sampled point/bounds differences are 0.000527/0.000530 mm.
The curved origin probe's larger 0.003652 mm UI width discrepancy is retained
and is below the 0.01 mm threshold. The newly generated Tool setting alone gets
native name T1 and priority 3; every original setting remains exact. Initial
incomplete accessibility and selection-label failures remain alongside the
passing result. Device origin and size were restored and the test app closed.

This satisfies H3's five searched native projects and settings-dialogue check.
Uncached movable Text and groups mixing fixed and active children still prevent
full H3 completion. The existing canonical contract forbids splitting a Group;
the requested clarification is pending, and public import still rejects such
mixed groups clearly. The frozen corpus and published v1 results are unchanged.


## Missing Text backups — 2026-10-14 UTC

The [training-only repair audit](../benchmarks/results/h3-text-cache-20261014T005902Z.md)
finds 122 uncached Text objects in eight original projects. All specify Arial
without an embedded font program. The existing N0 native re-saves supply all
caches and preserve text strings: 477 leaves / 1,223 contours, including all
122 Text leaves, match the independent oracle within 0.000500 mm. This verifies
the repair path, not original geometry or a lossless native re-save. All eight
native saves change canonical settings; original XML remains authoritative.

The proposed treatment is to require an explicit repair for uncached text,
retain no-op preservation, and evaluate geometry after re-saving/converting
text to paths. This narrows literal H3 and awaits Artem's decision. No exception
is applied. Zero-area open paths and mixed fixed/active Groups remain separate
issues. See [LightBurn's portability explanation](https://docs.lightburnsoftware.com/legacy/UI/FontsAndText).

## Ordered contour export probes — 2026-10-14 UTC

The [N5 start-point checkpoint](../benchmarks/results/h6-contour-starts-checkpoint-20261014.md)
records native SVG/DXF seam behavior. SVG retains four selected starts, including
elliptical and Bézier interiors. Closed DXF rational splines can lose a collinear
start and LightBurn approximates the tested ellipse outside 0.01 mm. Ordered DXF
now uses closed polylines for straight/circular contours and bounded polynomial
splines for other curves. A mixed contour starting on a straight edge needs its
open spline followed by that LINE. Five final native DXF starts match within
0.000011 mm; maximum geometry error is 0.000449 mm.

The spline/line join reverses native winding in the mixed probe. Lead-footprint
work must cover the actual native direction and verify native leads explicitly.
These red markers are not lead allowances, and these authored probes do not
close H6. “Choose best starting point” must be off for the eventual native lead
check. Failed rational, subdivision and mixed-contour probes remain published.

## Calibrated leads and searched previews — 2026-10-15 UTC

Native 3 mm arc leads use 3 mm of arc length: radius approximately 3.82 mm at
45° and 1.91 mm at 90°. [Plan decision 3](PLAN_V1_1.md#10-reviewed-decisions)
records Artem's approval to replace the original fixed-radius rule.
[Calibration evidence](../benchmarks/results/h6-lead-native-calibration-20261015.md)
preserves that original assumption and the native measurements.

The [lead-planner checkpoint](../benchmarks/results/h6-lead-planner-checkpoint-20261015.md)
adds three actual searched native previews: line 45° on rectangular panels,
arc 45° on rings, and arc 90° on rectangular panels. Each has four copies and
eight contours. Native settings use length 3 mm, no overcut/lead-out, best-start
selection off and best-direction selection on. Both directions are reserved.
LEADIN/C02 and the sheet outline are output-disabled. The 24 saved native starts
match within 0.000002569 mm; the largest contour difference is 0.00245745 mm.

Each coupon uses one angle for both outer and hole contours. LightBurn stores
`leadAngle` per layer; applying different outer/hole angles or different shortened
lengths needs separate settings. The [public lead controls and reports](LEAD_INS.md)
now expose these settings, flag unreserved contours and list shortened lengths.
The separate-layer/default-angle/shortened-length workflow still needs a native
check. These previews do not complete H6; multi-component planning, broader
independent coverage/owner auditing and material-cost evidence remain.


## Lead cutting files alongside preserved projects — 2026-10-15 UTC

[Reviewed decision 4](PLAN_V1_1.md#10-reviewed-decisions) keeps editable LBRN2 child geometry, starts and settings unchanged while separate SVG/DXF cutting files carry new starts and LEADIN review paths. The [group checkpoint](../benchmarks/results/h6-lead-group-checkpoint-20261015.md) implements this through UI/CLI/MCP, including disconnected pieces, holes, islands and flagged open cuts. Protected engraving and image bounds do not become cut paths. See [the export workflow](LEAD_INS.md#current-scope) before combining cutting files with the editable project.

An actual two-group search opens/saves in LightBurn Pro 2.1.01. Thirty independent native contour comparisons pass; sixteen SVG/DXF closed-contour starts match within 0.000002237 mm. Maximum contour differences are 0.001819 mm for SVG and 0.000008422 mm for DXF. Open paths remain open, and the preserved project's cut settings equal its native baseline. This session did not generate native leads or inspect a new cutting preview; the earlier native lead tests remain separate. Uncached text and mixed fixed/active groups remain unresolved, and H3/H6 are not complete.

## Current lead-allowance status — 2026-10-15 UTC

The later [H6 completion audit](../benchmarks/results/h6-complete-20261015.md)
supersedes the unfinished H6 status in the historical checkpoints above. It
combines independent source/footprint validation, exact exported starts, the
three searched native previews, separate outer/hole settings and shortened
lengths, all public surfaces, and the 156-layout material-cost measurement.
The original native starts and reservations revalidate unchanged.

H6 is complete; H3 remains open for uncached Text and mixed fixed/active groups.
The separate cutting files do not change that preservation contract. Weighted
v1.1 completion remains 20% (H1 and H6); see [STATUS.md](STATUS.md).


## Approved prerequisites: fresh verification — 2026-10-15 UTC

The [current-build audit](../benchmarks/results/h3-approved-prerequisites-20261015.md)
supersedes the pending-approval status in historical checkpoints. All 56 original
training projects retain exact no-op bytes. All 1,550 comparable original leaves
and all 477 leaves in the eight native repaired projects pass the independent
geometry checks; the 122 missing original text caches remain explicitly missing.
The mixed-group case rejects through public import and lower-level unit/writer
preparation. All 112 produced diagnostic sheets pass the allowed canonical diff.

H3 is still incomplete: repaired L17 has a standalone zero-width open-path
bounding rectangle and is explicitly refused. Its full repaired geometry check
passes, but this does not make it a valid nesting result. The current checks pass
290 workspace tests, 25 optimized CLI tests and 82 enabled browser tests. Overall
completion remains 20%; the open-line footprint and full H3 audit are next.


## Open strokes and H3 training verification — 2026-10-15 UTC

The [open-stroke checkpoint](../benchmarks/results/h3-open-line-fix-20261015.md) resolves the repaired L17 rejection. Bounding axes narrower than two curve tolerances receive a symmetric conservative footprint; original open paths and cut settings remain exact in the preserving export. The first grid-only attempt still failed on seventeen nearly horizontal strokes and remains archived. All eight native repairs now import, with 477 independently compared leaves and 210 unit footprints. Original training adds 225 independently compared units; 114 canonical diagnostic sheet diffs pass.

L17 nests 73 units on one sheet. Two new native saves preserve 36 open paths in total and pass 93 leaf comparisons within 0.000516 mm. The earlier five native-checked layouts revalidate with unchanged canonical contents apart from sub-picometre top-level XForm replay. All 293 workspace, 26 optimized CLI and 84 enabled browser tests pass. Three frozen native held-out projects remain unevaluated, so H3 is still open and completion remains 20%. Frozen inputs, labels, split and all failures remain intact.
