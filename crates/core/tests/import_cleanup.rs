use nestbolt_core::import::{Options, import_svg};
use proptest::prelude::*;

fn svg(paths: &str) -> String {
    format!(r#"<svg width="100mm" height="100mm" viewBox="0 0 100 100">{paths}</svg>"#)
}

#[test]
fn removes_forward_reverse_and_zero_segments_without_dropping_circles() {
    let paths = r#"<path d="M0 0 H20 V20 H0 Z"/><path d="M0 0 H20 M20 0 H0 M0 0 L0 0"/>
        <circle cx="10" cy="10" r="2"/><circle cx="10" cy="10" r="2"/>"#;
    let result = import_svg(&svg(paths), &Options::default()).unwrap();
    assert_eq!(result.parts.len(), 1);
    assert_eq!(result.parts[0].holes.len(), 1);
    assert_eq!(result.report.cleanup.duplicate_segments_removed, 3);
    assert_eq!(result.report.cleanup.zero_length_segments_removed, 1);
    assert_eq!(result.report.cleanup.overlapping_segments_merged, 0);
    assert_eq!(result.parts[0].outer.segments.len(), 4);
    assert!(matches!(
        result.parts[0].holes[0].segments[0],
        nestbolt_core::curves::Segment::Arc { .. }
    ));
}

#[test]
fn reversed_beziers_are_duplicates_but_a_nonempty_closed_curve_is_not_zero() {
    let paths = r#"<path d="M0 0 C10 -10 20 -10 30 0 L30 20 H0 Z"/>
        <path d="M30 0 C20 -10 10 -10 0 0"/>
        <path d="M10 10 C0 5 20 5 10 10"/>"#;
    let result = import_svg(&svg(paths), &Options::default()).unwrap();
    assert_eq!(result.parts.len(), 1);
    assert_eq!(result.parts[0].holes.len(), 1);
    assert_eq!(result.report.cleanup.duplicate_segments_removed, 1);
    // SVG Z at the already-closed cubic adds an empty final line, not an empty cubic.
    assert!(matches!(
        result.parts[0].holes[0].segments[0],
        nestbolt_core::curves::Segment::Cubic { .. }
    ));
}

#[test]
fn merges_partial_and_contained_collinear_overlaps_without_merging_nearby_lines() {
    let paths = r#"<path d="M0 0 H12 M20 0 H8 M5 0 H10 M20 0 V20 H0 V0"/>
        <path d="M40 0 H60 V20 H40 Z"/>
        <path d="M40 0.01 H60"/>"#;
    let result = import_svg(&svg(paths), &Options::default()).unwrap();
    assert_eq!(result.parts.len(), 2);
    assert_eq!(result.report.cleanup.overlapping_segments_merged, 2);
    assert_eq!(result.report.open_contours.len(), 1);
    assert_eq!(
        result
            .parts
            .iter()
            .map(|p| p.outer.segments.len())
            .collect::<Vec<_>>(),
        [4, 4]
    );
}

#[test]
fn cleanup_preserves_closed_retraced_arc_endpoints() {
    // A short gap-repair bridge doubles back along the following line. Unioning
    // them would detach the line from the arc and turn this closed hole into
    // three open paths. This is an independently authored regression drawing.
    let result = import_svg(
        include_str!("fixtures/closed-retrace.svg"),
        &Options::default(),
    )
    .unwrap();
    assert!(result.report.open_contours.is_empty());
    assert_eq!(result.parts.len(), 1);
    assert_eq!(result.parts[0].holes.len(), 1);
    assert_eq!(result.parts[0].holes[0].segments.len(), 10);
    assert_eq!(result.report.cleanup.overlapping_segments_merged, 0);
    // Retain the exact extremum of the backtracking line, not just the
    // intended rectangle: deleting a 0.05 mm spur would violate fidelity.
    assert!(
        result.parts[0].holes[0]
            .segments
            .iter()
            .any(|s| s.end() == [40.05, -10.0])
    );
    assert_eq!(result.report.cleanup.closed_path_overlaps_preserved, 2);
    assert!(
        result
            .warnings
            .iter()
            .any(|w| w.contains("keep closed paths connected"))
    );
}

#[test]
fn exact_retraces_stay_closed_but_a_second_copy_is_removed() {
    let paths = r#"<path d="M0 0 H20 V20 H0 V10 H-1 H0 V0 Z"/>
        <path d="M0 0 H20 V20 H0 V10 H-1 H0 V0 Z"/>"#;
    let result = import_svg(&svg(paths), &Options::default()).unwrap();
    assert!(result.report.open_contours.is_empty());
    assert_eq!(result.parts.len(), 1);
    assert_eq!(result.parts[0].outer.segments.len(), 7);
    assert_eq!(result.report.cleanup.duplicate_segments_removed, 7);
    assert_eq!(result.report.cleanup.closed_path_overlaps_preserved, 1);
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(1024))]
    #[test]
    fn shuffled_overlaps_and_duplicates_keep_the_exact_rectangle(
        w in 10u32..500, h in 10u32..500, overlap in 1u32..500, seed in any::<u64>(),
    ) {
        let (w,h,d)=(w as f64,h as f64,overlap as f64/1000.0);
        let mut segments=[([0.0,0.0],[w/2.0+d/2.0,0.0]),([w/2.0-d/2.0,0.0],[w,0.0]),
            ([w,0.0],[w,h]),([w,h],[0.0,h]),([0.0,h],[0.0,0.0]),
            ([w,h],[w,0.0]),([w,0.0],[w,h]),([0.0,0.0],[0.0,0.0])];
        let mut state=seed;
        for i in (1..segments.len()).rev() {
            state=state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            segments.swap(i,(state as usize)%(i+1));
            if state & 128 != 0 { let (a,b)=segments[i]; segments[i]=(b,a); }
        }
        let paths=segments.iter().map(|(a,b)|format!("<path d=\"M{} {} L{} {}\"/>",a[0],a[1],b[0],b[1])).collect::<String>();
        let r=import_svg(&svg(&paths),&Options::default()).unwrap();
        prop_assert_eq!(r.parts.len(),1);
        prop_assert_eq!(r.parts[0].bounds,[0.0,-h,w,0.0]);
        prop_assert!((r.parts[0].area-w*h).abs()<1e-8);
        prop_assert_eq!(r.report.cleanup.duplicate_segments_removed,2);
        prop_assert_eq!(r.report.cleanup.zero_length_segments_removed,1);
        prop_assert_eq!(r.report.cleanup.overlapping_segments_merged,1);
        prop_assert!(r.report.open_contours.is_empty());
    }
}
