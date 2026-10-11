//! Comparator input preparation only. Final layouts are checked against the
//! original Job, never against these inset or clipped stock contours.
use anyhow::{Context, Result, ensure};
use clipper2_rust::{
    ClipType, Clipper64, ClipperOffset, EndType, FillRule, JoinType, Path64, Paths64, Point64,
    PolyTree64,
};
use nestbolt_validator::{
    GRID, Polygon, Units,
    job::{Job, Layout, Stock, rectangle, validate},
};
use serde::Serialize;

#[derive(Serialize)]
struct PreparedStock {
    id: String,
    geometry: Vec<Polygon>,
    inset: f64,
    grid: f64,
}

fn paths(polygons: &[Polygon], scale: f64) -> Paths64 {
    let mut result = vec![];
    for polygon in polygons {
        for (index, ring) in std::iter::once(&polygon.outer)
            .chain(&polygon.holes)
            .enumerate()
        {
            let mut path: Path64 = ring
                .iter()
                .map(|p| Point64::new((p[0] * scale).round() as i64, (p[1] * scale).round() as i64))
                .collect();
            let area: i128 = path
                .iter()
                .zip(path.iter().cycle().skip(1))
                .map(|(a, b)| a.x as i128 * b.y as i128 - a.y as i128 * b.x as i128)
                .sum();
            if (area > 0) != (index == 0) {
                path.reverse();
            }
            result.push(path);
        }
    }
    result
}

fn boolean(subject: &Paths64, clip: &Paths64, operation: ClipType) -> Result<Paths64> {
    let mut engine = Clipper64::new();
    engine.add_subject(subject);
    engine.add_clip(clip);
    let mut result = vec![];
    ensure!(
        engine.execute(operation, FillRule::NonZero, &mut result, None),
        "stock boolean failed"
    );
    Ok(result)
}

fn prepare(stock: &Stock, units: Units, edge: f64, native_gap: f64) -> Result<PreparedStock> {
    let scale = units.to_mm() / GRID;
    let m = stock.margins;
    let margin_box = paths(
        &[rectangle(
            m.left,
            m.bottom,
            stock.width - m.left - m.right,
            stock.height - m.bottom - m.top,
        )],
        scale,
    );
    let mut usable = if stock.outline.is_empty() {
        margin_box
    } else {
        boolean(
            &paths(&stock.outline, scale),
            &margin_box,
            ClipType::Intersection,
        )?
    };
    for defect in &stock.defects {
        usable = boolean(
            &usable,
            &paths(std::slice::from_ref(defect), scale),
            ClipType::Difference,
        )?;
    }
    // Deepnest inflates part exteriors by half its configured spacing, but its
    // pinned negative bin offset is skipped. Supply only the remaining inset.
    // Never expand a concave stock to compensate excessive native inflation:
    // expansion could join islands or erase genuine keep-out regions.
    let inset = (edge - native_gap / 2.0).max(0.0);
    if inset > 0.0 {
        let mut offset = ClipperOffset::new(2.0, 0.0, false, false);
        offset.add_paths(&usable, JoinType::Miter, EndType::Polygon);
        offset.execute(-inset * scale, &mut usable);
        ensure!(offset.error_code() == 0, "stock inset failed");
    }
    let mut engine = Clipper64::new();
    engine.add_subject(&usable);
    let mut tree = PolyTree64::new();
    ensure!(
        engine.execute_tree(ClipType::Union, FillRule::NonZero, &mut tree, &mut vec![]),
        "stock topology reconstruction failed"
    );
    let ring = |index: usize| {
        tree.nodes[index]
            .polygon()
            .iter()
            .map(|p| [p.x as f64 / scale, p.y as f64 / scale])
            .collect()
    };
    let geometry = (1..tree.nodes.len())
        .filter(|&i| !tree.is_hole(i))
        .map(|i| Polygon {
            outer: ring(i),
            holes: tree.nodes[i].children().iter().map(|&j| ring(j)).collect(),
        })
        .collect();
    Ok(PreparedStock {
        id: stock.id.clone(),
        geometry,
        inset,
        grid: 1.0 / scale,
    })
}

fn main() -> Result<()> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    ensure!(
        args.len() == 2,
        "usage: stock_adapter <original-job.json> <native-spacing>"
    );
    let job: Job = serde_json::from_slice(&std::fs::read(&args[0])?)?;
    let native_gap: f64 = args[1].parse().context("native spacing must be a number")?;
    ensure!(
        native_gap.is_finite() && native_gap >= job.clearance,
        "native spacing cannot weaken source clearance"
    );
    let checked = validate(
        &job,
        &Layout {
            version: 1,
            units: job.units,
            sheets: vec![],
            placements: vec![],
        },
    )?;
    ensure!(
        checked.violations.iter().all(|v| v.code == "quantity"),
        "invalid source job"
    );
    let stocks: Vec<_> = job
        .stocks
        .iter()
        .map(|s| prepare(s, job.units, job.edge_clearance, native_gap))
        .collect::<Result<_>>()?;
    println!("{}", serde_json::to_string_pretty(&stocks)?);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use nestbolt_validator::{Footprint, RigidTransform, job::Margins};

    fn stock() -> Stock {
        Stock {
            id: "remnant".into(),
            width: 100.0,
            height: 80.0,
            count: Some(1),
            margins: Margins {
                left: 5.0,
                right: 7.0,
                bottom: 3.0,
                top: 9.0,
            },
            outline: vec![],
            defects: vec![],
        }
    }

    fn area(output: &PreparedStock) -> f64 {
        Footprint::from_polygons(&output.geometry, Units::Mm, RigidTransform::default())
            .unwrap()
            .area()
    }

    #[test]
    fn asymmetric_margins_and_interior_defect_have_exact_known_area() {
        let mut source = stock();
        source.defects.push(rectangle(30.0, 20.0, 10.0, 10.0));
        let output = prepare(&source, Units::Mm, 3.0, 2.0).unwrap();
        assert_eq!(output.inset, 2.0);
        assert_eq!(output.geometry.len(), 1);
        assert_eq!(output.geometry[0].holes.len(), 1);
        assert_eq!(area(&output), 84.0 * 64.0 - 14.0 * 14.0);
    }

    #[test]
    fn boundary_defect_becomes_notch_and_margins_clip_remnant() {
        let mut source = stock();
        source.outline.push(rectangle(0.0, 0.0, 60.0, 70.0));
        source.defects.push(rectangle(0.0, 20.0, 20.0, 10.0));
        let output = prepare(&source, Units::Mm, 2.0, 4.0).unwrap();
        assert_eq!(output.geometry[0].holes.len(), 0);
        assert_eq!(area(&output), 55.0 * 67.0 - 15.0 * 10.0);
    }

    #[test]
    fn split_stock_is_retained_as_two_components_not_two_physical_sheets() {
        let mut source = stock();
        source.defects.push(rectangle(40.0, 0.0, 10.0, 80.0));
        let output = prepare(&source, Units::Mm, 0.0, 0.0).unwrap();
        assert_eq!(output.geometry.len(), 2);
        assert_eq!(area(&output), 78.0 * 68.0);
    }

    #[test]
    fn excess_native_inflation_never_expands_a_stock() {
        let source = stock();
        let output = prepare(&source, Units::Mm, 1.0, 10.0).unwrap();
        assert_eq!(output.inset, 0.0);
        assert_eq!(area(&output), 88.0 * 68.0);
        let output = prepare(&source, Units::Inch, 1.0, 10.0).unwrap();
        assert_eq!(output.grid, GRID / 25.4);
        assert_eq!(area(&output), 88.0 * 68.0);
    }
}
