# Schemas

All schemas are generated from the Rust types by `python scripts/schemas.py`; CI
checks they match. JSON Schema checks structure only; the engine and the
independent validator check meaning and geometry.

## Nesting files (CLI, MCP server and browser)

- [library.schema.json](library.schema.json): parts imported from SVG or DXF, in
  millimetres. Each part keeps its exact outer and hole contours (lines,
  elliptical arcs in centre form, quadratic and cubic Béziers; DXF splines become
  cubics), the polygon the solver uses and the flattening `tolerance` between them.
  Produced by `nestbolt import` and the `import_parts` tool.
- [request.schema.json](request.schema.json): what to nest: part ids and
  quantities, rotations, mirroring, priorities, sheet sizes with counts, margins,
  defects and remnant outlines, part and edge spacing, and the fill mode. Clearances
  grow by the library tolerance so the true curves keep the requested gaps.
  Optional `quick_start` tries a conservative initial arrangement before the
  normal improvement search; it defaults to false and may change material use.
- [nest-report.schema.json](nest-report.schema.json): the `report.json` written
  next to `job.json` and `layout.json` by `nestbolt nest` and the `nest` tool:
  seed, budget, whether the run is repeatable, parts placed in holes, exported
  files (relative to the report) and the independent validation report.

The browser app saves the same library and request inside its project ZIP.

## Independent benchmark contract

`nestbolt validate` reads the engine-neutral polygon model in `validator::job`:

- [benchmark-job.schema.json](benchmark-job.schema.json): original geometry,
  constraints, stock and fill mode. `job.json` from a nest uses this format.
- [benchmark-layout.schema.json](benchmark-layout.schema.json): stock assignments
  and rigid placements identified by original part and physical copy; `layout.json`.
- [benchmark-validation.schema.json](benchmark-validation.schema.json): findings
  and independently computed metrics, absent for invalid layouts.

Examples live in `examples/validation-job.json` and `examples/validation-layout.json`.

## Upstream interchange

`nestbolt inspect` accepts **upstream jagua-rs 1.1.0 BPP JSON** with explicit units
([sample](../examples/sheet-job.json)); its output is
[inspection.schema.json](inspection.schema.json). It is an interchange format for
benchmarks, not a Nestbolt project format, and extra upstream metadata is not
enforced as a constraint.


## Imported stock outlines

`library.schema.json` includes optional `sheet_outlines` separate from parts.
A request sheet may use `from_import` with one of those IDs and omit its dimensions.
The browser's standalone stock import returns [sheet-import.schema.json](sheet-import.schema.json).
All coordinates are millimetres. The curve error is reserved at sheet edges; see
[imported stock rules](../docs/IMPORTING.md#sheet-outlines-in-pre-arranged-nests).
