# Agent interface

`nestbolt-mcp` is a native stdio MCP server (rmcp 3.5.1) with five tools over the
same core as the CLI. It needs no network, account or credentials.

| Tool | What it does |
| --- | --- |
| `import_parts` | Reads SVG/DXF files or one LightBurn project, writes a part library (exact curves plus nesting polygons, mm) and returns part ids, areas, bounds, import warnings and separate stock-outline summaries |
| `nest` | Nests library parts on fixed sheets with a repeatable budget (`time_budget_s` ≤ 300, `seed`); writes `job.json`, `layout.json`, `report.json` and per-sheet SVG/DXF or preserving LBRN2 files; sends progress notifications |
| `validate_layout` | Checks a layout file against a request with the independent validator |
| `export_layout` | Writes per-sheet SVG/DXF or preserving LBRN2 files from a valid layout; arcs and splines stay curves |
| `estimate_sheets` | Net part area over usable sheet area: a necessary lower bound, never a layout; flags parts that fit no sheet |

A `nest` request names library parts and the sheets, in millimetres:

```json
{
  "parts": [{"id": "parts-1", "quantity": 4}, {"id": "parts-2", "quantity": 12, "rotations": {"kind": "free"}}],
  "sheets": [{"width_mm": 600, "height_mm": 400, "margins_mm": {"left": 5, "right": 5, "bottom": 5, "top": 5}}],
  "spacing_mm": 1.0,
  "edge_spacing_mm": 1.0
}
```

Rotations default to 0/90/180/270 degrees and mirroring to off. Parts may be
placed inside the holes of larger parts. See `examples/nest-request.json`.
The library, request and `report.json` formats are JSON Schemas in
[schemas/](../schemas/README.md). `report.json` lists exported files relative to
its own directory; the `nest` reply lists them relative to the workspace.

## Rules

- **Workspace.** Every path must lie inside the server's working directory, or
  `NESTBOLT_WORKSPACE` when set. Paths with `..` or outside it are refused.
- **No overwrites.** Libraries, layouts and exports are always new files; an
  output directory must be new or empty.
- **Small replies.** Geometry stays in files; the combined part/stock summary is
  capped at 200 entries, with separate total counts and truncation flags.
- **Repeatable.** `nest` measures its budget in deterministic work, so the same
  library, request, budget and seed give the same layout on the same build. If
  the real-time limit (`time_budget_s`) arrives first, the reply says
  `"repeatable": false` and explains that a larger budget repeats. See the
  [search contract](SEARCH_CONTRACT.md).
- **Checked.** Every returned layout has passed the independent validator.
  Errors say what to change (unknown part ids, missing sheets, paths).

## Connecting

Build the server, then register the absolute path of the executable:

```sh
cargo build --release -p nestbolt-mcp --locked
```

```powershell
claude mcp add --transport stdio --scope local nestbolt -- C:/DEV/Nestbolt/target/release/nestbolt-mcp.exe
codex mcp add nestbolt -- C:/DEV/Nestbolt/target/release/nestbolt-mcp.exe
```

On Linux/macOS the binary has no `.exe` suffix. For Claude Desktop or a project
configuration, merge this object into the MCP settings:

```json
{
  "mcpServers": {
    "nestbolt": {
      "command": "C:/DEV/Nestbolt/target/release/nestbolt-mcp.exe",
      "args": [],
      "env": {"NESTBOLT_WORKSPACE": "C:/path/to/your/cutting/files"}
    }
  }
}
```

For Codex:

```toml
[mcp_servers.nestbolt]
command = 'C:\DEV\Nestbolt\target\release\nestbolt-mcp.exe'
env = { NESTBOLT_WORKSPACE = 'C:\path\to\your\cutting\files' }
```

## Evidence and remaining acceptance

`crates/mcp/tests/connection.rs` starts the real executable as an MCP child
process, lists the five tools, imports `examples/parts.svg`, nests twice with
the same seed (identical layouts when repeatable), validates, exports and
estimates, and checks that a path outside the workspace is refused.

G7 still requires a real client: Claude Code run with
`claude -p --mcp-config <file> --strict-mcp-config`, listing the tools, importing
a sample SVG, nesting with a 10-second budget and exporting, with the result
passing the independent validator. That run uses Artem's Claude Code account.

Release packaging remains M4 work: Windows/Linux/macOS archives with notices and
checksums, a tag-triggered release workflow, an MCPB bundle and `server.json`
validated with `mcp-publisher validate`, following
[Cutbolt #2](https://github.com/skulitom/Cutbolt/pull/2) and
[Inkbolt #1](https://github.com/skulitom/Inkbolt/pull/1). Nothing is published
until Artem says go.


## Imported sheet boundaries

`import_parts` discovers the `SHEET` layer independently of cut selection.
`sheet_layers` chooses other stock layers. Its reply includes `sheet_outlines`
summaries and a `sheet_outline_count`; actual polygons stay in the library.
Use `{"from_import":"arranged-sheet-1","count":1}` as a request sheet. The same
request is used for nesting, validation, re-export and estimation. See
[stock selection, normalization and curve clearance](IMPORTING.md#sheet-outlines-in-pre-arranged-nests).


## LightBurn projects

`import_parts` accepts one `.lbrn2`/`.lbrn` file. Its `lightburn` reply reports the
source name, unit count, fixed-shape count, origin flags and up to 200 layers,
including kerf in millimetres. Full XML remains in the library file. Nesting and
validation derive the rigid units again from that source, including disconnected
group components; area estimates include every component.

`nest` exports `.lbrn2` automatically for a LightBurn library. `export_layout`
also accepts `format: "lbrn2"`; omit `format` to use the source default. Its
`sheet_outline` defaults to true for LightBurn and false for SVG/DXF. Set it to
false to omit the added T1 boundary. Requests, quantities, rotations, mirrors,
stock choices, independent validation and no-overwrite rules are shared.
The LightBurn-to-SVG/DXF path is refused because it would discard project data.
See [current import limitations](IMPORTING.md#editable-lightburn-projects),
including pending legacy conversion and mixed fixed/movable groups.
