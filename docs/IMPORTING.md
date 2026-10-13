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

These are initial N1 capabilities. Full corpus
fidelity, 10,000-case property testing and native LightBurn export checks still
need their H2 evidence. The frozen corpus and held-out partition must not change
in response to these tests.
