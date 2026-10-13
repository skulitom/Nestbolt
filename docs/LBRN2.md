# LightBurn project format: local observations

Probed with the installed LightBurn **2.1.01** in the hidden Anode desktop on
2026-10-13, using the `No Machine` device. These are saved projects and observed
UI behaviour; no LightBurn executable was inspected or decompiled. The title bar
says **Pro**, although the earlier research described the installation as Core.
No edition change, activation, update or trial reset was performed here.

The starting reference is [V1_1_RESEARCH.md section 2](V1_1_RESEARCH.md#2-lightburn-lbrn2).
The probes below confirm only their stated observations. The reader checkpoint
below adds training geometry evidence; complete source coverage, lossless nesting
exports and H3 remain unproved.

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
Actual native opening of nested output still needs the H3 writer check.

Eight older training projects contain 122 Text shapes without backups. The reader
retains their XML, reports a native re-save instruction and marks their geometry
incomplete; it does not invent bounds. Thus 48 projects have complete compared
geometry, and full H3 reader acceptance remains open. This is a core inspection
API and diagnostic example: nesting-unit construction, per-sheet preserving
writes, UI/CLI/MCP integration and new native opening checks remain to be built.
See [the complete checkpoint](../benchmarks/results/h3-reader-checkpoint-20261013.md).
