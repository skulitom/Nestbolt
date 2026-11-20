# Common-line cutting (v1.1 development)

Enable **Common-line cutting** after importing SVG/DXF cut outlines and enter
the measured kerf in millimetres (at least 0.05 mm). Kerf replaces part spacing;
edge spacing and sheet margins still apply. Turning the option off restores the
previous spacing. Common-line cutting reserves holes by default.

**Nest parts inside holes** lets inserts use a larger part’s window when the
required kerf clearance fits. Both the hole wall and the insert keep their
true-size CUT contours. Only straight outer edges of separate parts can share a
cut. Enable this independently of the search bonus with the browser checkbox,
the CLI flag `--common-line-part-in-hole` alongside `--common-line`, or
`"allow_part_in_hole": true` inside the JSON/MCP `common_line` object.

CLI example, using an existing imported library and nesting request:

```powershell
nestbolt nest --library library.json --request request.json --out-dir nested --common-line --kerf 0.2 --seconds 30
```

The effective request is saved as `nested/request.json`. Reuse it when exporting
the layout again. JSON requests, including MCP `nest` and `export_layout`, enable
the same feature with `"common_line": {"kerf_mm": 0.2}`. Omit `common_line` for
ordinary nesting. The browser Project ZIP retains this setting and its report.

**Search for more shared cuts** is optional and off by default. Enable it in the
browser, add `--common-line-bonus` to the CLI example, or set
`"common_line": {"kerf_mm": 0.2, "search_bonus": true}` in a JSON/MCP request.
It reserves the last tenth of the existing time budget for shared-cut placement.
With **Nest parts inside holes** enabled, repeated right-angled parts can also
form interlocking groups of up to four. Nestbolt tries arranging these groups in
rows on rectangular stock. It accepts a row layout only when it reduces stock
use and preserves or increases the shared cutting length. Short translations
then align straight cutting edges. Their placement cost is material relative to
the refinement's starting layout minus saved length as a fraction of total cut
length. Every accepted move passes independent validation, including any lead
reservations, and adds at most 1% material relative to that starting layout.
This internal limit does not guarantee a 1% difference from a separate ordinary
nesting run: search time and the selected hole placement policy can affect that
comparison. Compare both material use and saved cutting length for your job.

COMMON contains one copy of each detected shared straight cut, offset by half
the kerf. Detection uses outer edges only, requires at least 10 mm of overlap,
and allows at most 0.01 mm between the two offset lines. Neither holes nor sheet
edges are shared. Connected edges are chained without adding bridging cuts.
CUT remains the original, closed, true-size outlines. COMMON is blue (LightBurn
C01; DXF ACI 5 and true colour `#0000ff`); CUT is black (C00).

**Prepare the cutting operations in CAM:** replace the corresponding shared
sections of CUT with COMMON. Do not cut both the complete CUT references and
COMMON. Turn **CAM kerf compensation off for COMMON**, since compensation is
already in its coordinates. Remaining exterior cuts still need the normal CAM
setup. The export does not generate machine code or choose pierces or cut order.

The report compares the original total contour length with the length after
replacing shared sections, and reports the original contour count and resulting
path count. These describe geometry, not cycle time or pierce savings. Some
layouts have no shared edges and zero savings, even with the optional search.
Curved drawings retain the conservative flattening allowance used for collision
checks; this can prevent their otherwise straight edges from meeting the 0.01 mm
detection tolerance. Ordinary nesting is unchanged.

Editable LightBurn project exports preserve their native artwork and settings.
For this common-line workflow, first export their cutting outlines as SVG/DXF
from LightBurn and import those outlines into Nestbolt.

For plasma, a shared cut cannot give both adjacent parts the preferred cut side;
bevel and part quality can differ. Avoid piercing directly on a finished edge
and review the pierce positions and cutting sequence in CAM. Small or narrow
parts may tip up when freed; support and retention need consideration. See
[Primecut's kerf and cut-side guidance](https://kineticusa.com/PrimecutHelp/common-line-and-common-crop-cu.html)
and [OSH Cut's explanation of retention tabs](https://www.oshcut.com/design-guide/understanding-micro-joints).

## Development measurements

With **Nest parts inside holes** and **Search for more shared cuts** enabled, the 13 development jobs saved a median 13.031% of cutting distance at 0.2 mm kerf and 13.101% at 1.5 mm. The largest measured increase in material use was approximately 0.0125% relative to ordinary nesting at the same spacing. All 234 layouts passed validation. The comparison uses three seeds and 60 seconds per run. Individual jobs can have lower savings. [Per-job cutting and material results](../benchmarks/results/h5-rigid-host-rows-20261120.md).

With the default hole-reserving policy, both mechanical jobs exceeded the +1% material ceiling in the earlier comparison. The largest increase was 6.51%. The original opt-in search also exceeded the ceiling on the mixed-bracket laser job at +1.417%. [Default-policy comparison](../benchmarks/results/h5-cutting-development-20261015.md) and [earlier opt-in comparison](../benchmarks/results/h5-opt-in-holes-20261120.md).

The laser SVG and plasma DXF were opened in LightBurn. The archived screenshots show the separate COMMON layer and measured dimensions. [Native import and independent geometry checks](../benchmarks/results/h5-commonline-checkpoint-20261014.md).
