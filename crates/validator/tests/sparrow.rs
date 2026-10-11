use nestbolt_validator::{Units, sparrow::validate};
use serde_json::{Value, json};

fn fixture() -> (Value, Value) {
    let input = json!({"name":"original", "strip_height":10,
        "items":[{"id":0,"demand":2,"allowed_orientations":[0,180],
            "shape":{"type":"simple_polygon","data":[[0,0],[4,0],[4,4],[0,4]]}}]});
    let output = json!({"solution":{"strip_width":10,"layout":{"placed_items":[
        {"item_id":0,"transformation":{"rotation":0,"translation":[0,0]}},
        {"item_id":0,"transformation":{"rotation":0,"translation":[5,0]}}
    ]}}});
    (input, output)
}

#[test]
fn checks_original_geometry_instead_of_embedded_solver_input() {
    let (input, mut output) = fixture();
    output["items"] = json!([{"shape":{"type":"simple_polygon","data":[[0,0],[1,0],[1,1],[0,1]]}}]);
    output["solution"]["layout"]["placed_items"][1]["transformation"]["translation"] =
        json!([2, 0]);
    let report = validate(&input.to_string(), &output.to_string(), Units::Unitless).unwrap();
    assert!(!report.valid);
    assert_eq!(report.maximum_overlap_ratio, 0.5);
}

#[test]
fn quantities_rotations_containment_and_unknown_items_fail() {
    let (input, output) = fixture();
    assert!(
        validate(&input.to_string(), &output.to_string(), Units::Unitless)
            .unwrap()
            .valid
    );
    let mut variants = vec![];
    let mut missing = output.clone();
    missing["solution"]["layout"]["placed_items"]
        .as_array_mut()
        .unwrap()
        .pop();
    variants.push(missing);
    let mut angle = output.clone();
    angle["solution"]["layout"]["placed_items"][1]["transformation"]["rotation"] =
        json!(std::f64::consts::FRAC_PI_2);
    variants.push(angle);
    let mut outside = output.clone();
    outside["solution"]["layout"]["placed_items"][1]["transformation"]["translation"] =
        json!([9, 0]);
    variants.push(outside);
    let mut unknown = output.clone();
    unknown["solution"]["layout"]["placed_items"][1]["item_id"] = json!(9);
    variants.push(unknown);
    for invalid in variants {
        let report = validate(&input.to_string(), &invalid.to_string(), Units::Unitless).unwrap();
        assert!(!report.valid);
        assert!(!report.violations.is_empty());
    }
}

#[test]
fn rejects_nonrigid_transform_fields_and_duplicate_source_ids() {
    let (mut input, mut output) = fixture();
    output["solution"]["layout"]["placed_items"][0]["transformation"]["scale"] = json!(0.5);
    assert!(validate(&input.to_string(), &output.to_string(), Units::Mm).is_err());
    let item = input["items"][0].clone();
    input["items"].as_array_mut().unwrap().push(item);
    assert!(validate(&input.to_string(), &fixture().1.to_string(), Units::Mm).is_err());
}

#[test]
fn accepts_float32_angle_rounding_but_not_arbitrary_angles() {
    let (input, mut output) = fixture();
    output["solution"]["layout"]["placed_items"][1]["transformation"] =
        json!({"rotation":3.1415925,"translation":[9,4]});
    let report = validate(&input.to_string(), &output.to_string(), Units::Unitless).unwrap();
    assert!(report.valid, "{:?}", report.violations);
}

#[test]
fn empty_rotation_list_is_fixed_while_null_is_free() {
    let (mut input, mut output) = fixture();
    input["items"][0]["allowed_orientations"] = json!([]);
    output["solution"]["layout"]["placed_items"][1]["transformation"] =
        json!({"rotation":std::f64::consts::FRAC_PI_2,"translation":[9,0]});
    assert!(
        !validate(&input.to_string(), &output.to_string(), Units::Unitless)
            .unwrap()
            .valid
    );
    input["items"][0]["allowed_orientations"] = Value::Null;
    assert!(
        validate(&input.to_string(), &output.to_string(), Units::Unitless)
            .unwrap()
            .valid
    );
}
