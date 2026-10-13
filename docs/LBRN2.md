# LightBurn project format: local observations

Probed with the installed LightBurn **2.1.01** in the hidden Anode desktop on
2026-10-13, using the `No Machine` device. These are saved projects and observed
UI behaviour; no LightBurn executable was inspected or decompiled. The title bar
says **Pro**, although the earlier research described the installation as Core.
No edition change, activation, update or trial reset was performed here.

The starting reference is [V1_1_RESEARCH.md section 2](V1_1_RESEARCH.md#2-lightburn-lbrn2).
The probes below confirm only their stated observations. Reader/oracle fidelity,
lossless nesting exports and H3 remain unproved.

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
- Export the default palette to SVG/DXF and verify RGB and ACI values, including T1.
- Verify the mirror normalization with actual nested outputs during H3.
- Compare all public/local geometry with the independent published MIT oracle.

## Export palette and DXF variants

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
and its screenshot. Adding DXF group 420 true colour does not fix the tool-layer
assignment: [palette-truecolor.dxf](../benchmarks/datasets/shop/probes/palette-truecolor.dxf)
has two rectangles with exact `#f36926` true colour, one with entity ACI 30 and
one BYLAYER (layer ACI 30, also exact true colour). Their
[native re-import](../benchmarks/datasets/shop/probes/palette-truecolor-reimport.lbrn2)
assigns C05 and C13, respectively, both cutting layers. Use the exact RGB in
Nestbolt exports and report this import limitation; an approximate ACI must not
be represented as preserving the T1 operation type. The `.lbrn2` format preserves
T1 directly and has no such loss.

The export dialogue offers Illustrator, AutoCAD Legacy DXF, AutoCAD Modern DXF
and SVG. The observed Modern DXF is **AC1021 with `$INSUNITS=4`**, explicitly mm.
The [Legacy export](../benchmarks/datasets/shop/probes/palette-legacy.dxf) is
**AC1009, also with `$INSUNITS=4`**. Do not treat LightBurn DXFs as unitless;
check the actual header. These observations correct the older blanket inference
in the research for the locally installed version and default settings.

Screenshots are under [n2-probes-20261013](../benchmarks/results/n2-probes-20261013/).
