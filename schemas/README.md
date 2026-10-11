# Schema boundary

The current `inspect` command accepts **upstream jagua-rs 1.1.0 BPP JSON**, as shown
in [the generated sample](../examples/sheet-job.json). It is not yet a canonical
Nestbolt job or saved-project format. Units are a separate required CLI argument
or WASM parameter; the upstream payload has no units field.

The implemented format has a name, `min_item_separation`, items with numeric IDs,
demands, shapes and explicit orientations, and bins with stock/cost/geometry.
Rectangle and simple-polygon parts work. Part holes and multipolygons are rejected.
Stock is finite. The adapter bounds total demand to 1..2000, requires positive total
stock and unique IDs, and imports active geometry through jagua-rs. Zero-demand
parts and zero-stock bins are inactive. Original area is in squared input units.

Upstream permits unrelated metadata. Do not assume an arbitrary extra field such
as `margin` or `priority` becomes an enforced Nestbolt constraint. Inspection does
not solve or test feasibility. Geometry and orientation errors are reported by
the engine, not by a complete independent validator.

The JSON Schema for today's **output** is [inspection.schema.json](inspection.schema.json).
Versioned canonical `job.schema.json` and `result.schema.json` are a v1 requirement,
to be generated from the shared model once geometry fidelity, mixed-stock scoring,
units, file references and deterministic search budgets are settled. Do not freeze
those public interfaces around the temporary upstream interchange format.

## Independent benchmark contract

`nestbolt validate` reads the engine-neutral polygon model in `validator::job`:

- [benchmark-job.schema.json](benchmark-job.schema.json): original geometry,
  constraints, stock and fill mode.
- [benchmark-layout.schema.json](benchmark-layout.schema.json): stock assignments
  and rigid placements identified by original part and physical copy.
- [benchmark-validation.schema.json](benchmark-validation.schema.json): findings
  and independently computed metrics, absent for invalid layouts.

Regenerate with `python scripts/schemas.py`; CI checks consistency with the Rust
types. JSON Schema checks structure; the Rust validator checks semantic constraints
and geometry. Examples live in `examples/validation-job.json` and
`examples/validation-layout.json`.

This is the M1 polygon benchmark contract. It does not replace the future public
project/import/curve or solve-result formats, which must preserve original curves,
file references, progress and the search-budget contract. Those v1 deliverables
remain outstanding.
