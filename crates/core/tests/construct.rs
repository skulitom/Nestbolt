use nestbolt_core::construct::{Options, construct};
use nestbolt_validator::{
    Polygon, Units,
    job::{Job, Margins, Mode, Part, Rotations, Stock, rectangle, validate},
};

fn part(id: &str, geometry: Vec<Polygon>, quantity: u32) -> Part {
    Part {
        id: id.into(),
        geometry,
        quantity,
        rotations: Rotations::List { degrees: vec![0.0] },
        allow_mirror: false,
        priority: 1.0,
    }
}
fn stock(id: &str, w: f64, h: f64, count: Option<u32>) -> Stock {
    Stock {
        id: id.into(),
        width: w,
        height: h,
        count,
        margins: Margins::default(),
        outline: vec![],
        defects: vec![],
    }
}
fn job(parts: Vec<Part>, stocks: Vec<Stock>) -> Job {
    Job {
        version: 1,
        name: "construction test".into(),
        units: Units::Mm,
        parts,
        stocks,
        clearance: 0.4,
        edge_clearance: 0.7,
        mode: Mode::All,
    }
}

#[test]
fn holed_and_disconnected_parts_preserve_source_and_repeat() {
    let mut ring = rectangle(-2.0, -3.0, 8.0, 9.0);
    ring.holes.push(rectangle(0.0, 0.0, 2.0, 2.0).outer);
    let source = job(
        vec![
            part("ring", vec![ring], 3),
            part(
                "letters",
                vec![
                    rectangle(-3.0, 0.0, 2.0, 3.0),
                    rectangle(1.0, 0.0, 2.0, 3.0),
                ],
                4,
            ),
        ],
        vec![stock("sheet", 24.0, 16.0, None)],
    );
    let before = serde_json::to_string(&source).unwrap();
    let first = construct(&source, Options::default()).unwrap();
    assert!(first.complete);
    assert!(first.layout.sheets.len() > 1);
    assert!(validate(&source, &first.layout).unwrap().valid);
    assert_eq!(before, serde_json::to_string(&source).unwrap());
    let second = construct(&source, Options::default()).unwrap();
    assert_eq!(
        serde_json::to_string(&first).unwrap(),
        serde_json::to_string(&second).unwrap()
    );
}

#[test]
fn mixed_stock_limits_and_fill_do_not_invent_sheets() {
    let mut source = job(
        vec![
            part("large", vec![rectangle(0.0, 0.0, 12.0, 9.0)], 2),
            part("small", vec![rectangle(0.0, 0.0, 3.0, 3.0)], 1),
        ],
        vec![
            stock("small", 8.0, 8.0, Some(1)),
            stock("large", 15.0, 12.0, Some(1)),
        ],
    );
    let result = construct(&source, Options::default()).unwrap();
    assert!(!result.complete);
    assert_eq!(result.unplaced, 1);
    assert_eq!(result.layout.sheets.len(), 2);
    source.mode = Mode::FillArea;
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert_eq!(result.unplaced, 1);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn exact_list_angles_and_mirror_are_rebuilt_in_source_coordinates() {
    let mut source = job(
        vec![part(
            "triangle",
            vec![Polygon {
                outer: vec![[5.0, -3.0], [12.0, -3.0], [5.0, 8.0]],
                holes: vec![],
            }],
            2,
        )],
        vec![stock("sheet", 32.0, 18.0, None)],
    );
    source.parts[0].rotations = Rotations::List {
        degrees: vec![37.0],
    };
    source.parts[0].allow_mirror = true;
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert!(validate(&source, &result.layout).unwrap().valid);
    assert!(
        result
            .layout
            .placements
            .iter()
            .all(|p| p.transform.rotation_radians == 37.0_f64.to_radians())
    );
}

#[test]
fn split_remnant_regions_share_one_stock_copy_and_avoid_defects() {
    let mut sheet = stock("remnant", 40.0, 16.0, Some(1));
    sheet.outline = vec![
        rectangle(0.0, 0.0, 16.0, 16.0),
        rectangle(24.0, 0.0, 16.0, 16.0),
    ];
    sheet.defects.push(rectangle(2.0, 2.0, 3.0, 3.0));
    sheet.margins.left = 1.0;
    let source = job(
        vec![part("block", vec![rectangle(0.0, 0.0, 7.0, 7.0)], 2)],
        vec![sheet],
    );
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert_eq!(result.layout.sheets.len(), 1);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn a_mirror_required_by_the_remnant_is_exported_as_one_rigid_transform() {
    let triangle = Polygon {
        outer: vec![[0.0, 0.0], [8.0, 0.0], [0.0, 8.0]],
        holes: vec![],
    };
    let mut sheet = stock("triangle-remnant", 10.0, 10.0, Some(1));
    sheet.outline = vec![Polygon {
        outer: vec![[0.0, 0.0], [10.0, 0.0], [10.0, 10.0]],
        holes: vec![],
    }];
    let mut source = job(vec![part("triangle", vec![triangle], 1)], vec![sheet]);
    source.clearance = 0.1;
    source.edge_clearance = 0.1;
    let unmirrored = construct(&source, Options::default()).unwrap();
    assert!(!unmirrored.complete);
    source.parts[0].allow_mirror = true;
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert!(result.layout.placements[0].transform.mirrored);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn a_long_rectangular_sheet_uses_its_usable_edges_without_random_sampling() {
    let mut sheet = stock("long", 400.0, 20.0, Some(1));
    sheet.margins = Margins {
        left: 5.0,
        right: 5.0,
        bottom: 2.0,
        top: 2.0,
    };
    let source = job(
        vec![part("bar", vec![rectangle(0.0, 0.0, 180.0, 12.0)], 2)],
        vec![sheet],
    );
    let result = construct(
        &source,
        Options {
            random_samples: 0,
            ..Options::default()
        },
    )
    .unwrap();
    assert!(result.complete);
    assert_eq!(result.layout.sheets.len(), 1);
    assert!(validate(&source, &result.layout).unwrap().valid);
}
