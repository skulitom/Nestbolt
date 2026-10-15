# Common-line cutting (v1.1 development)

Enable **Common-line cutting** after importing SVG/DXF cut outlines and enter
the measured kerf in millimetres (at least 0.05 mm). Kerf replaces part spacing;
edge spacing and sheet margins still apply. Turning the option off restores the
previous spacing. Parts are not nested inside other parts' holes in this mode.

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
It reserves the last tenth of the existing time budget for short translations
that align straight cutting edges. Its placement cost is material relative to
the refinement's starting layout minus saved length as a fraction of total cut
length. Every accepted move passes independent validation, including any lead
reservations, and adds at most 1% material relative to that starting layout.
This internal limit does not guarantee a 1% difference from a separate ordinary
nesting run: search time and the disabled part-in-hole option can affect that
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

[The geometry and native-import checkpoint](../benchmarks/results/h5-commonline-checkpoint-20261014.md)
includes independent Clipper2 tests and native LightBurn SVG/DXF saves. H5 remains
open: the [60-second, three-seed development comparison](../benchmarks/results/h5-cutting-development-20261015.md)
validates all 234 Nestbolt layouts and reaches 13.03% laser / 13.10% plasma median
cut savings. Both mechanical jobs exceed the +1% material limit, up to +6.51%.
The native Deepnest SVG comparison is also recorded, including its four
no-layout results. These development findings make no production quality claim
or new held-out claim.
