use nestbolt_core::{Units, inspect_json};
use proptest::prelude::*;
use serde_json::{Value, json};

const EXAMPLE: &str = include_str!("../../../examples/sheet-job.json");

fn example() -> Value {
    serde_json::from_str(EXAMPLE).unwrap()
}

fn error(job: Value) -> String {
    format!(
        "{:#}",
        inspect_json(&job.to_string(), Units::Mm).unwrap_err()
    )
}

#[test]
fn imports_real_geometry_and_preserves_declared_units() {
    let report = inspect_json(EXAMPLE, Units::Mm).unwrap();
    assert_eq!(report.total_parts, 6);
    assert_eq!(report.part_types, 2);
    assert_eq!(report.available_sheets, 2);
    assert_eq!(report.total_part_area, 16_800.0);
    assert_eq!(report.units, Units::Mm);
    let inches = inspect_json(EXAMPLE, Units::Inch).unwrap();
    assert_eq!(inches.units, Units::Inch);
    assert_eq!(inches.total_part_area, report.total_part_area);
}

#[test]
fn rejects_duplicate_ids() {
    let mut job = example();
    job["items"][1]["id"] = json!(10);
    assert!(error(job).contains("item IDs must be unique"));
    let mut job = example();
    let bin = job["bins"][0].clone();
    job["bins"].as_array_mut().unwrap().push(bin);
    assert!(error(job).contains("sheet IDs must be unique"));
}

#[test]
fn rejects_overflow_and_excessive_demand_before_geometry_import() {
    for demand in [2_001_u64, u64::MAX] {
        let mut job = example();
        job["items"][0]["demand"] = json!(demand);
        assert!(inspect_json(&job.to_string(), Units::Mm).is_err());
    }
}

#[test]
fn rejects_invalid_rotation_spacing_and_empty_stock() {
    let mut job = example();
    job["items"][0]["orientation"]["rotation"]["step"] = json!(91);
    assert!(error(job).contains("rotation step"));
    let mut job = example();
    job["min_item_separation"] = json!(-1);
    assert!(error(job).contains("nonnegative"));
    let mut job = example();
    job["bins"][0]["stock"] = json!(0);
    assert!(error(job).contains("positive sheet stock"));
}

#[test]
fn refuses_item_holes_instead_of_silently_filling_them() {
    let mut job = example();
    job["items"][0]["shape"] = json!({"type": "polygon", "data": {
        "outer": [[0,0], [80,0], [80,40], [0,40]],
        "inner": [[[10,10], [20,10], [20,20], [10,20]]]
    }});
    assert!(error(job).contains("unsupported holes"));
}

#[test]
fn inactive_items_do_not_contribute_area() {
    let mut job = example();
    job["items"][0]["demand"] = json!(0);
    let report = inspect_json(&job.to_string(), Units::Mm).unwrap();
    assert_eq!(report.total_parts, 2);
    assert_eq!(report.part_types, 1);
    assert_eq!(report.total_part_area, 4_000.0);
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(32))]
    #[test]
    fn rectangular_area_scales_with_quantity(width in 5_u32..100, height in 5_u32..100, count in 1_u32..1999) {
        let mut job = example();
        job["items"][0]["shape"]["data"]["width"] = json!(width);
        job["items"][0]["shape"]["data"]["height"] = json!(height);
        job["items"][0]["demand"] = json!(count);
        let report = inspect_json(&job.to_string(), Units::Mm).unwrap();
        prop_assert_eq!(report.total_parts, u64::from(count) + 2);
        prop_assert!((report.total_part_area - f64::from(width * height * count + 4000)).abs() < 0.1);
    }
}
