use nestbolt_core::{
    clock::Timing,
    project::{Library, Request},
    sheets::{Options, optimize},
};

#[test]
fn ci_hole_curve_near_quadrant_corner_stays_valid() {
    // Exact generated SVG and seed from Linux CI 38819422170. The hole
    // placement prepass used to panic in jagua-rs's quadrant classification.
    let source = include_str!("fixtures/ci-hole-curve.svg");
    let library =
        Library::import(&[("fuzz.svg".into(), source.into())], &Default::default()).unwrap();
    assert_eq!(library.parts.len(), 5);
    let quantities = [1, 2, 1, 2, 2];
    let parts: Vec<_> = library.parts.iter().zip(quantities).map(|(part, quantity)| {
        serde_json::json!({"id":part.id,"quantity":quantity,"rotations":{"kind":"free"}})
    }).collect();
    let request: Request = serde_json::from_value(serde_json::json!({
        "parts":parts,
        "sheets":[{"width_mm":120,"height_mm":80,"margins_mm":{"left":2,"right":2,"bottom":2,"top":2}}],
        "spacing_mm":0.5,"edge_spacing_mm":0.5
    })).unwrap();
    let (job, _) = request.job(&library).unwrap();
    let result = optimize(
        &job,
        Options {
            seconds: 2.0,
            seed: 659,
            timing: Timing::Work,
            // Keep the original work budget while allowing a slower CI machine.
            time_limit: Some(10.0),
            ..Options::default()
        },
        |_, _| {},
    )
    .unwrap();
    assert_eq!(result.layout.placements.len(), 8);
    assert!(result.validation.valid);
    assert!(
        nestbolt_validator::job::validate(&job, &result.layout)
            .unwrap()
            .valid
    );
}
