# nestbolt-validator

An independent checker for 2D nesting layouts. Give it a job (parts, stock
sheets, spacing) and a layout (which copy sits where), and it reports whether
the layout is valid and how much material it uses.

It is the validator behind [Nestbolt](https://github.com/skulitom/Nestbolt),
published separately so a layout from any nesting tool can be checked the same
way. It shares no code with a nesting engine: it depends on
[clipper2-rust](https://crates.io/crates/clipper2-rust) for polygon clipping
and on nothing from jagua-rs, Sparrow or `geo`.

## What it checks

- every requested copy is placed exactly once, on a sheet that exists;
- parts do not overlap and keep the requested clearance from each other;
- parts stay inside the sheet, its margins and any remnant outline, and clear
  of marked defects, with the requested edge clearance;
- rotations and mirroring are ones the job allows;
- stock counts are respected.

Placements are rebuilt from the original polygons and a rigid transform
(mirror, then rotate, then translate). Geometry already transformed by a solver
is never accepted. Clipping runs on a one-nanometre integer grid for physical
jobs (`1e-6` mm), or `1e-6` coordinate units for unitless ones.

A valid layout gets metrics: sheets used, material area, utilisation and the
trailing offcut on the last sheet. An invalid layout gets a list of violations
and no score.

## Example

```rust
use nestbolt_validator::job::{
    Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle, validate,
};
use nestbolt_validator::{RigidTransform, Units};

fn place(copy_index: u32, x: f64) -> Placement {
    Placement {
        part_id: "square".into(),
        copy_index,
        sheet_id: "sheet-1".into(),
        transform: RigidTransform { translation: [x, 0.0], ..Default::default() },
    }
}

let job = Job {
    version: 1,
    name: "two squares".into(),
    units: Units::Mm,
    parts: vec![Part {
        id: "square".into(),
        quantity: 2,
        geometry: vec![rectangle(0.0, 0.0, 10.0, 10.0)],
        rotations: Rotations::Step { degrees: 90.0 },
        allow_mirror: false,
        priority: 1.0,
    }],
    stocks: vec![Stock {
        id: "plywood".into(),
        width: 100.0,
        height: 100.0,
        count: None,
        margins: Margins::default(),
        outline: vec![],
        defects: vec![],
    }],
    clearance: 1.0,
    edge_clearance: 0.0,
    mode: Mode::All,
};
let sheets = vec![Sheet { id: "sheet-1".into(), stock_id: "plywood".into() }];

// 11 mm apart: the 1 mm clearance holds.
let good = Layout {
    version: 1,
    units: Units::Mm,
    sheets: sheets.clone(),
    placements: vec![place(0, 0.0), place(1, 11.0)],
};
let report = validate(&job, &good)?;
assert!(report.valid);
assert_eq!(report.metrics.as_ref().map(|m| m.sheets_used), Some(1));

// 10.5 mm apart: the parts do not overlap, but the clearance is broken.
let tight = Layout {
    version: 1,
    units: Units::Mm,
    sheets,
    placements: vec![place(0, 0.0), place(1, 10.5)],
};
let report = validate(&job, &tight)?;
assert!(!report.valid);
assert!(report.metrics.is_none());
# Ok::<(), anyhow::Error>(())
```

`Job`, `Layout` and `Report` are plain `serde` types with JSON Schemas
(`schemars`), so the same check works on JSON files written by another program.

## Licence

MIT. See `LICENSE`.
