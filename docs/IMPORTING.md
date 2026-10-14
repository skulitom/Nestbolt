# Import options and repair reports

Curve precision controls how closely nesting polygons follow the exact source
curves. It does not permit larger gaps to close: the silent endpoint join limit
is always **0.005 mm**.

To repair larger gaps, opt in to **Close larger gaps** and enter a maximum from
0 to 1 mm. Import the drawing, or use **Apply import options** to re-read the most
recent files with the new setting. Re-reading replaces those files' parts and
messages; it does not leave parts from an earlier import behind. The option is
off by default and resets when another project is opened.

The equivalent CLI command is:

```powershell
nestbolt import drawing.dxf --output library.json --close-gaps 0.05
```

MCP `import_parts` accepts `close_gaps_mm: 0.05`. Omit the parameter to leave
larger-gap repair off. Values over 1 mm, negative values and non-finite values
are rejected with a corrective message.

Every repaired gap over 0.005 mm is recorded with its source, endpoints and size
in millimetres. Repair inserts a straight bridge so the original neighbouring
curve endpoints remain intact. Open contours that remain unimported report their
endpoints, endpoint gap and a suggested repair tolerance when it is within the
1 mm limit. Larger gaps require editing the source drawing. If any selected
contour remains open, the UI, CLI and MCP reject the import without producing a
partial library. Exclude score/construction layers or repair the cut outlines
and import again. Low-level geometry inspection still returns the open-contour
report. In the browser, a failed re-import removes those files' earlier parts
and clears the previous layout; unrelated files stay available.

Libraries and CLI/MCP responses include an `imports` entry per file:

```json
{
  "file": "drawing.dxf",
  "report": {
    "silent_join_mm": 0.005,
    "close_gaps_mm": 0.05,
    "closed_gaps": [
      {
        "source": "CUT:LINE",
        "from_mm": [0, 0.05],
        "to_mm": [0, 0],
        "size_mm": 0.05
      }
    ],
    "open_contours": []
  }
}
```

## File encoding and units

SVG page sizing follows `viewBox` and `preserveAspectRatio`: the default fits the
whole viewBox inside the page, `none` permits different horizontal and vertical
scales, and `slice` fills the page. All nine alignment choices and the root
`transform` are applied before converting to millimetres and Y-up coordinates,
following the [SVG viewport transform specification](https://www.w3.org/TR/SVG2/coords.html#ComputingAViewportsTransform).
If only width or height is provided, the other dimension inherits the viewBox
aspect ratio. With neither, the configured SVG user-unit scale applies (96 DPI
by default). Invalid or relative page sizes need an absolute size in mm or pixels.
Nested SVG viewports must be flattened into a single page first.

Page clipping does not trim cutting paths. A `slice` mapping that extends beyond
the page warns that complete paths were imported; convert visible edges into
closed paths if clipping is intended to define the cut.

DXF polyline widths do not change cutting geometry: Nestbolt imports the
centreline and warns when an LWPOLYLINE, POLYLINE or VERTEX specifies a nonzero
width. This covers both constant and variable widths from the
[DXF polyline fields](https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-DXF/files/GUID-748FC305-F3F2-4F74-825A-61F04D757A50.htm).
Convert widths to closed outline paths in the source drawing if their outer
edges are the intended cut. This warning appears in the UI, CLI and MCP.

The UI, CLI and MCP decode the original file bytes with the same reader. Older
DXFs use their `$DWGCODEPAGE` setting, defaulting to Windows-1252 when it is absent;
DXF R2007 and later use UTF-8. DXF Unicode escapes are decoded too, so non-ASCII
layer names remain selectable. SVG follows its byte-order mark or XML encoding
declaration. Invalid bytes or unsupported encodings give a re-export instruction;
no replacement characters are silently inserted. These DXF rules follow the
[ezdxf encoding reference](https://ezdxf.readthedocs.io/en/stable/dxfinternals/fileencoding.html).

DXF file units take precedence over a fallback. mm, cm, metres, inches and feet
are supported; unsupported unit codes request a re-export in one of these units.
Without declared units, the default remains 1 mm per drawing unit. If the largest
selected dimension is under 60 drawing units, the report warns that the drawing
may be in inches. It never changes scale automatically.

For a DXF without units, use its **DXF units when missing** dropdown and apply
the options. CLI uses `--dxf-unit-mm 25.4`; MCP uses `dxf_unit_mm: 25.4`. A value of
10 selects centimetres. These settings do not override units declared by the
file. The structured `units` report records whether units were declared, the
applied millimetres per unit, the largest selected dimension in drawing units
and the possible-inches flag.

## Duplicate and overlap cleanup

Before joining paths, the importer removes exact duplicate segments (including
reversed lines and Béziers) and genuinely zero-length segments. Full circles and
closed Bézier loops are retained. Overlapping collinear lines are merged into
their union; neighbouring parallel lines are not merged. This does not flatten
curves or increase the 0.005 mm join threshold.

Retraces needed to keep a closed path connected retain their exact curves and
produce a warning plus `cleanup.closed_path_overlaps_preserved`. Cleanup does
not disconnect a neighbouring arc to remove a short overlapping bridge.

Every report has `cleanup.duplicate_segments_removed`,
`cleanup.zero_length_segments_removed` and `cleanup.overlapping_segments_merged`,
including zero counts. The browser displays these counts beside each file's
inventory, and nonzero cleanup also appears in its import messages. CLI and MCP
return the same report. Selection happens first, so excluded operation layers do
not participate in cleanup of the chosen cutting geometry.

## Layers and colours

The browser shows a per-file list of layers and colours with entity counts,
including ignored entities. Automatic selection prefers layer names containing
`cut`, `outline` or `profile`; otherwise it uses closed contours. Choose individual
layers or colours and press **Apply import options**. Choices apply per file;
when both filters are set, an entity must match both. **Use automatic selection**
clears the filters. The inventory is available even if every outline is open.

CLI equivalents are `--layers CUT,PROFILE` and `--colors 7` for DXF ACI colour 7,
or `--colors '#000000'` for RGB black. MCP accepts `layers: ["CUT", "PROFILE"]`
and `colors: ["7"]` or `colors: ["#000000"]`. DXF ACI entries are reported as
`aci:7`; RGB colours are normalized to lowercase six-digit hex. Layer names match
without case sensitivity. Unknown choices name the available alternatives.

DXF counts include expanded block instances and each INSERT. Layer-0 children
inherit the insertion layer; BYBLOCK and BYLAYER colours are resolved before
selection. Block base points, rotation, scale and the negative-Z INSERT extrusion
are applied to the source curves. Malformed POLYLINE sequences require a corrected
export. Text, dimensions, hatches, leaders, solids, attributes and images are
reported but are not cutting geometry. Bend, extent and construction layers,
hidden entities and paper-space geometry are also reported and ignored.
The block fields follow Autodesk's [BLOCK](https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-DXF/files/GUID-66D32572-005A-4E23-8B8B-8726E8C14302.htm)
and [INSERT](https://help.autodesk.com/cloudhelp/2018/ENU/AutoCAD-DXF/files/GUID-28FA4CFB-9D5E-4880-9F11-36C97578252F.htm)
references; the exact-arc tests cover the composed placement.

SVG layers use Inkscape layer labels or top-level group IDs. Stroke colour is used
when present, otherwise fill colour. Presentation attributes, inline styles and
simple tag/class/ID stylesheet rules are supported, including inheritance through
groups and `<use>`. More complex CSS selectors require a plain SVG export with
presentation attributes; the importer reports this fix instead of guessing.
Ordinary SVG DOCTYPE declarations are accepted without fetching external resources.
Text and images require conversion to paths if they are to be cut.

Reports include `layers` and `colors` lists. Each entry has `name`, `entities`,
`geometry_entities` and `selected_entities`. `selection_mode` is `explicit`,
`named_cut_layers` or `closed_contours`. These counts describe selection before
chaining; the open-contour messages still need review for missing outlines.

The browser can expand its import messages to show every warning. Its worker
uses the same native import options and report model. The existing WebAssembly
`import_files` entry point remains available; new integrations can pass JSON
options to `import_files_with_options`.

## Export colours and LightBurn

SVG groups and DXF layers use the locally verified LightBurn palette:

| Operation | LightBurn layer | SVG / DXF true colour | DXF ACI fallback |
| --- | --- | --- | --- |
| CUT | C00 | `#000000` | 7 |
| COMMON | C01 | `#0000ff` | 5 |
| LEADIN | C02 | `#ff0000` | 1 |
| SHEET | T1 | `#f36926` | 30 |

DXF export is now AutoCAD 2007 (`AC1021`), in millimetres. Entities use BYLAYER
colour; each layer records both its exact RGB and an ACI fallback. SVG uses the
same RGB strokes. True-size closed part outlines remain on CUT. Exporting and
re-importing a drawing with these groups automatically selects CUT, while the
other operation layers remain available for explicit selection.

When including a sheet outline, enable **Settings → Import / Export → Allow
Importing to Tool Layers** in LightBurn before importing. This is required for
SHEET to arrive on T1. With the option off, LightBurn can assign that colour to
a cutting layer. ACI 30 alone is also insufficient; see the [native palette
probes](LBRN2.md#export-palette-and-dxf-variants). Leave sheet-outline export off
when a boundary is unnecessary.

The core exporter can accept already-computed COMMON and LEADIN review paths,
preserving open endpoints. Their generation and user-facing controls belong to
N4/N5 and are not implemented by this palette change.

The [ten-file native check](../benchmarks/results/h2-lightburn-20261013T195848Z.md)
records sizes and palette assignments, including a small LightBurn spline-size
display discrepancy whose saved geometry remains exact within native precision.
These are initial N1 capabilities. Full corpus fidelity and 10,000-case property
testing still need their H2 evidence. The frozen corpus and held-out partition
must not change in response to these tests.


## Sheet outlines in pre-arranged nests

Importing a drawing offers closed boundaries on its `SHEET` layer separately
from the cutting parts. The availability message and `sheet_outlines` list give
each outline an ID, measured size and original position. Discovery does not
change the chosen cutting layers or automatically replace your stock.

In the browser, select **Imported sheet outline** for the required sheet size.
The **Remnant outline** file picker also prefers `SHEET` over `CUT`, so parts
already placed on a sheet do not become holes in the stock. For another layer
name, tick it under **Sheet outline layers**, apply the import options, then
choose the resulting outline. Several separate stock outlines are offered
individually; the file picker asks you to choose rather than guessing.

CLI imports discover `SHEET` automatically. Use `--sheet-layers MATERIAL` for a
custom stock layer; MCP `import_parts` takes `sheet_layers: ["MATERIAL"]`.
An explicit empty list disables discovery; CLI uses `--sheet-layers` without
values. Cut-layer and cut-colour choices
remain independent of stock-layer discovery. Failed automatic stock discovery
is reported while valid cutting parts remain importable; an explicitly requested
invalid stock layer fails with a repair instruction.

```powershell
nestbolt import arranged.dxf --output library.json
```

A nesting request can select the returned ID without copying its geometry:

```json
{
  "sheets": [{"from_import": "arranged-sheet-1", "count": 1}],
  "spacing_mm": 1,
  "edge_spacing_mm": 1
}
```

This works with CLI `nest` and MCP `nest`, `validate_layout`, `export_layout` and
`estimate_sheets`. `from_import` resolves against the same part library.
Dimensions may be omitted or set to the measured values; conflicting sizes are
rejected, never used to stretch the stock. Count, margins and defects remain
request settings. MCP returns bounded summaries; complete outline geometry is
kept in the library file.

The sheet and its own holes move together to the lower-left origin in mm, Y-up
coordinates. `origin_mm` records that translation. Curved stock records its
flattening error; edge clearance covers both this error and the part-library
curve tolerance. Self-intersecting or touching stock contours require repair in
the source drawing: the outward repair used for part collision proxies cannot
create extra usable stock. Gap closure still requires the same explicit setting.
An explicit `outline_mm` may carry `outline_tolerance_mm` when supplied by the
shared sheet importer; it cannot be combined with `from_import`.

The shared WebAssembly `import_sheet` entry point returns
[`SheetImport`](../schemas/sheet-import.schema.json), including selected outlines,
import warnings and the layer/colour/gap report. Plain remnant drawings without
a `SHEET` layer still use their closed outlines.


## Editable LightBurn projects

Open one `.lbrn` or `.lbrn2` project in the browser. Groups remain rigid units, with all
separate components shown in the preview. Layer modes, output flags and kerf
values are displayed; kerf does not change part spacing automatically. Choose
quantities, rotations, mirroring and sheet sizes as usual. Download one
`<project>-sheet-<k>.lbrn2` per sheet, all sheets as a ZIP, or a Project ZIP that
also retains the original XML and nesting request. The T1 sheet outline is on
by default and can be turned off. The preview shows collision footprints;
exports retain editable text, images, curves and project settings.

CLI accepts the original project directly:

```powershell
nestbolt nest --library drawing.lbrn2 --request request.json --out-dir nested --seconds 30
nestbolt export --library drawing.lbrn2 --request request.json --layout nested/layout.json --out-dir without-outline --sheet-outline false
```

`nestbolt import drawing.lbrn2 --output library.json` also works. The library
keeps the source XML, and nesting/validation re-derive geometry from it rather
than trusting editable cached preview polygons. Files from different projects
cannot be combined because their layer settings may conflict. SVG/DXF layer,
colour, gap and sheet-layer overrides must be cleared for LightBurn imports.
SVG/DXF export of an imported LightBurn project is refused to avoid losing text,
images and cut settings.

Legacy `.lbrn` projects export as modern `.lbrn2`: compact path data is added,
while the original path elements, attributes and comments are retained. Native
LightBurn checks confirm that the retained legacy data does not duplicate cuts.
The source stored in the library or Project ZIP remains unchanged.

This is an N2 development checkpoint, not H3 acceptance. Movable text without cached
outlines requires re-saving in LightBurn. Groups mixing active artwork with
Tool/output-off shapes must be separated before nesting: active fixed artwork
is not yet independently validated against every output sheet. Full native
settings verification and the remaining format cases are tracked in
[LBRN2.md](LBRN2.md).
