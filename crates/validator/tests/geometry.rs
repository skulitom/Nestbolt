use nestbolt_validator::{Footprint, Polygon, RigidTransform, Units};
use proptest::prelude::*;

fn rectangle(x: f64, y: f64, w: f64, h: f64) -> Polygon {
    Polygon {
        outer: vec![[x, y], [x + w, y], [x + w, y + h], [x, y + h]],
        holes: vec![],
    }
}

fn footprint(p: Polygon) -> Footprint {
    Footprint::new(&p, Units::Mm, RigidTransform::default()).unwrap()
}

#[test]
fn overlap_is_measured_against_the_smaller_part() {
    let a = footprint(rectangle(0.0, 0.0, 10.0, 10.0));
    let b = footprint(rectangle(9.0, 0.0, 2.0, 2.0));
    let check = a.compare(&b, 0.0).unwrap();
    assert_eq!(check.overlap_area, 2.0);
    assert_eq!(check.overlap_ratio, 0.5);
}

#[test]
fn contact_and_clearance_are_distinguished() {
    let a = footprint(rectangle(0.0, 0.0, 10.0, 10.0));
    let touching = footprint(rectangle(10.0, 0.0, 10.0, 10.0));
    assert_eq!(a.compare(&touching, 0.0).unwrap().overlap_area, 0.0);
    assert!(!a.compare(&touching, 0.0).unwrap().clearance_violation);
    assert!(a.compare(&touching, 0.1).unwrap().clearance_violation);
    let separated = footprint(rectangle(10.2, 0.0, 10.0, 10.0));
    assert!(!a.compare(&separated, 0.2).unwrap().clearance_violation);
    assert!(a.compare(&separated, 0.2001).unwrap().clearance_violation);
}

#[test]
fn diagonal_clearance_uses_euclidean_distance() {
    let a = footprint(rectangle(0.0, 0.0, 10.0, 10.0));
    let b = footprint(rectangle(13.0, 14.0, 10.0, 10.0));
    assert!(!a.compare(&b, 5.0).unwrap().clearance_violation);
    assert!(a.compare(&b, 5.001).unwrap().clearance_violation);
}

#[test]
fn parts_fit_inside_holes_with_clearance() {
    let mut ring = rectangle(0.0, 0.0, 20.0, 20.0);
    ring.holes.push(rectangle(5.0, 5.0, 10.0, 10.0).outer);
    let ring = footprint(ring);
    assert_eq!(ring.area(), 300.0);
    let part = footprint(rectangle(6.0, 6.0, 8.0, 8.0));
    let check = ring.compare(&part, 1.0).unwrap();
    assert_eq!(check.overlap_area, 0.0);
    assert!(!check.clearance_violation);
    assert!(ring.compare(&part, 1.1).unwrap().clearance_violation);
}

#[test]
fn containment_respects_defects_and_boundary_spacing() {
    let mut sheet = rectangle(0.0, 0.0, 20.0, 20.0);
    sheet.holes.push(rectangle(8.0, 8.0, 4.0, 4.0).outer);
    let sheet = footprint(sheet);
    let in_defect = footprint(rectangle(9.0, 9.0, 2.0, 2.0));
    assert_eq!(in_defect.inside(&sheet, 0.0).unwrap().outside_area, 4.0);
    let at_edge = footprint(rectangle(0.0, 0.0, 2.0, 2.0));
    assert_eq!(at_edge.inside(&sheet, 0.0).unwrap().outside_area, 0.0);
    assert!(at_edge.inside(&sheet, 0.1).unwrap().clearance_violation);
    let outside = footprint(rectangle(-1.0, 2.0, 2.0, 2.0));
    assert_eq!(outside.inside(&sheet, 0.0).unwrap().outside_area, 2.0);
}

#[test]
fn rigid_transform_mirrors_then_rotates_then_translates() {
    let shape = rectangle(0.0, 0.0, 2.0, 1.0);
    let p = Footprint::new(
        &shape,
        Units::Mm,
        RigidTransform {
            mirrored: true,
            rotation_radians: std::f64::consts::FRAC_PI_2,
            translation: [10.0, 10.0],
        },
    )
    .unwrap();
    assert_eq!(p.bounds(), [9.0, 8.0, 10.0, 10.0]);
    assert_eq!(p.area(), 2.0);
}

#[test]
fn units_are_explicit_and_inches_are_converted() {
    let shape = rectangle(0.0, 0.0, 1.0, 1.0);
    let inch = Footprint::new(&shape, Units::Inch, RigidTransform::default()).unwrap();
    let mm = footprint(shape);
    assert!((inch.area() - 645.16).abs() < 1e-10);
    assert!(inch.compare(&mm, 0.0).is_err());
}

#[test]
fn normalizes_duplicate_closing_and_collinear_points() {
    let shape = Polygon {
        outer: vec![
            [0.0, 0.0],
            [0.0, 0.0],
            [5.0, 0.0],
            [10.0, 0.0],
            [10.0, 10.0],
            [0.0, 10.0],
            [0.0, 0.0],
        ],
        holes: vec![],
    };
    assert_eq!(footprint(shape).area(), 100.0);
}

#[test]
fn rejects_invalid_rings_and_hole_topology() {
    let invalid = [
        Polygon {
            outer: vec![[0.0, 0.0], [10.0, 10.0], [0.0, 10.0], [10.0, 0.0]],
            holes: vec![],
        },
        Polygon {
            outer: vec![[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]],
            holes: vec![],
        },
        Polygon {
            outer: vec![[0.0, 0.0], [f64::NAN, 1.0], [1.0, 0.0]],
            holes: vec![],
        },
        Polygon {
            outer: rectangle(0.0, 0.0, 10.0, 10.0).outer,
            holes: vec![rectangle(9.0, 9.0, 2.0, 2.0).outer],
        },
        Polygon {
            outer: rectangle(0.0, 0.0, 10.0, 10.0).outer,
            holes: vec![rectangle(0.0, 0.0, 2.0, 2.0).outer],
        },
        Polygon {
            outer: rectangle(0.0, 0.0, 10.0, 10.0).outer,
            holes: vec![
                rectangle(2.0, 2.0, 4.0, 4.0).outer,
                rectangle(3.0, 3.0, 1.0, 1.0).outer,
            ],
        },
    ];
    for shape in invalid {
        assert!(Footprint::new(&shape, Units::Mm, RigidTransform::default()).is_err());
    }
}

#[test]
fn slivers_and_small_overlap_remain_measurable() {
    let a = footprint(rectangle(0.0, 0.0, 10.0, 0.00001));
    let b = footprint(rectangle(5.0, 0.0, 10.0, 0.00001));
    let check = a.compare(&b, 0.0).unwrap();
    assert!((check.overlap_ratio - 0.5).abs() < 1e-10);
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(48))]
    #[test]
    fn rectangle_intersections_agree_with_analytic_area(
        ax in -100i32..100, ay in -100i32..100, aw in 1i32..50, ah in 1i32..50,
        bx in -100i32..100, by in -100i32..100, bw in 1i32..50, bh in 1i32..50,
    ) {
        let a = footprint(rectangle(ax.into(),ay.into(),aw.into(),ah.into()));
        let b = footprint(rectangle(bx.into(),by.into(),bw.into(),bh.into()));
        let width = ((ax+aw).min(bx+bw)-ax.max(bx)).max(0);
        let height = ((ay+ah).min(by+bh)-ay.max(by)).max(0);
        prop_assert_eq!(a.compare(&b,0.0).unwrap().overlap_area, f64::from(width*height));
    }

    #[test]
    fn winding_and_quarter_turns_preserve_area(w in 1i32..100, h in 1i32..100, quarter in 0u8..4, mirror in any::<bool>()) {
        let mut p=rectangle(0.0,0.0,w.into(),h.into()); p.outer.reverse();
        let f=Footprint::new(&p, Units::Mm, RigidTransform { rotation_radians: f64::from(quarter)*std::f64::consts::FRAC_PI_2, mirrored: mirror, translation: [13.0,-27.0] }).unwrap();
        prop_assert_eq!(f.area(),f64::from(w*h));
    }
}
