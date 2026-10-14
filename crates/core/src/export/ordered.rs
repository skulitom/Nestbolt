//! Closed polylines or B-splines when a start point must survive DXF.
//! A mixed contour starting on a line uses an open spline followed by that
//! line: LightBurn joins them at the requested seam. A closed spline alone
//! loses the seam when its first and last spans are collinear.
//! Non-circular arcs use cubic spans with a 0.000001 mm geometric error bound;
//! LightBurn's rational-spline importer otherwise exceeds the 0.01 mm gate.
use anyhow::{Result, ensure};

use super::{Contour, Dxf, PI, Segment, num};
use crate::curves::Point;

type Cubic = [Point; 4];

fn mix(a: Point, b: Point, t: f64) -> Point {
    std::array::from_fn(|k| a[k] * (1.0 - t) + b[k] * t)
}
fn elevate(a: Point, b: Point, c: Point) -> Cubic {
    [a, mix(a, b, 2.0 / 3.0), mix(b, c, 1.0 / 3.0), c]
}

fn cubics(from: Point, segment: &Segment) -> Result<Vec<Cubic>> {
    Ok(match segment {
        Segment::Line { to } => {
            let (a, b) = (from, *to);
            vec![[a, mix(a, b, 1.0 / 3.0), mix(a, b, 2.0 / 3.0), b]]
        }
        Segment::Quad { control, to } => vec![elevate(from, *control, *to)],
        Segment::Cubic {
            controls: [a, b],
            to,
        } => vec![[from, *a, *b, *to]],
        Segment::Arc {
            center,
            radii,
            rotation,
            start,
            sweep,
        } => {
            let mut count = (sweep.abs() / (PI / 2.0)).ceil().max(1.0);
            ensure!(
                count.is_finite() && count <= 4096.0,
                "arc requires too many ordered spline spans"
            );
            // For a symmetric unit-circle cubic of sweep h, squared radius
            // minus one is A*t²*(1-t)²*(t-1/2)², where
            // A=16*sin(h/2)²*tan(h/4)^4. The polynomial factor is <=1/432,
            // and sqrt(1+x)-1 <= x/2. Scale by the ellipse's operator norm.
            // Spans <=90° cover the arc monotonically, so this bounds both
            // directed geometric distances, not a few sampled points.
            while {
                let h = sweep / count;
                let bound =
                    radii[0].max(radii[1]) * (h / 2.0).sin().powi(2) * (h / 4.0).tan().powi(4)
                        / 54.0;
                bound > 0.000001
            } {
                count *= 2.0;
                ensure!(
                    count <= 4096.0,
                    "arc requires too many ordered spline spans"
                );
            }
            let (s, c) = rotation.sin_cos();
            let at = |angle: f64| {
                let x = radii[0] * angle.cos();
                let y = radii[1] * angle.sin();
                [center[0] + c * x - s * y, center[1] + s * x + c * y]
            };
            let tangent = |angle: f64| {
                let x = -radii[0] * angle.sin();
                let y = radii[1] * angle.cos();
                [c * x - s * y, s * x + c * y]
            };
            (0..count as usize)
                .map(|i| {
                    let a = start + sweep * i as f64 / count;
                    let b = start + sweep * (i + 1) as f64 / count;
                    let (p, q) = (at(a), at(b));
                    let (dp, dq) = (tangent(a), tangent(b));
                    let k = 4.0 / 3.0 * ((b - a) / 4.0).tan();
                    [
                        p,
                        std::array::from_fn(|j| p[j] + k * dp[j]),
                        std::array::from_fn(|j| q[j] - k * dq[j]),
                        q,
                    ]
                })
                .collect()
        }
    })
}

impl Dxf {
    fn polyline_contour(&mut self, layer: &str, contour: &Contour) -> Result<bool> {
        if !contour.segments.iter().all(|s| match s {
            Segment::Line { .. } => true,
            Segment::Arc { radii, .. } => {
                (radii[0] - radii[1]).abs() <= 1e-12 * radii[0].max(radii[1])
            }
            _ => false,
        }) {
            return Ok(false);
        }
        let mut vertices = vec![];
        let mut from = contour.start;
        for s in &contour.segments {
            match s {
                Segment::Line { .. } => vertices.push((from, 0.0)),
                Segment::Arc {
                    center,
                    radii,
                    rotation,
                    start,
                    sweep,
                } => {
                    let count = (sweep.abs() / PI).ceil().max(1.0);
                    ensure!(
                        count.is_finite() && count <= 4096.0,
                        "arc requires too many polyline spans"
                    );
                    for i in 0..count as usize {
                        let a = start + rotation + sweep * i as f64 / count;
                        let point = if i == 0 {
                            from
                        } else {
                            [
                                center[0] + radii[0] * a.cos(),
                                center[1] + radii[0] * a.sin(),
                            ]
                        };
                        vertices.push((point, (sweep / count / 4.0).tan()));
                    }
                }
                _ => unreachable!(),
            }
            from = s.end();
        }
        self.entity("LWPOLYLINE", layer);
        self.pair(100, "AcDbPolyline");
        self.pair(90, vertices.len());
        self.pair(70, 1);
        for (p, bulge) in vertices {
            self.pair(10, num(p[0]));
            self.pair(20, num(p[1]));
            self.pair(42, format!("{bulge:.16}"));
        }
        Ok(true)
    }

    pub(super) fn ordered_contour(&mut self, layer: &str, contour: &Contour) -> Result<()> {
        if self.polyline_contour(layer, contour)? {
            return Ok(());
        }
        if let Some(Segment::Line { to }) = contour.segments.first() {
            let remainder = Contour {
                start: *to,
                segments: contour.segments[1..].to_vec(),
            };
            self.ordered_spline(layer, &remainder, false)?;
            self.segment(layer, contour.start, &contour.segments[0]);
            return Ok(());
        }
        self.ordered_spline(layer, contour, true)
    }

    fn ordered_spline(&mut self, layer: &str, contour: &Contour, closed: bool) -> Result<()> {
        let mut pieces = vec![];
        let mut from = contour.start;
        for segment in &contour.segments {
            pieces.extend(cubics(from, segment)?);
            from = segment.end();
        }
        ensure!(!pieces.is_empty(), "ordered contour has no segments");
        let spans = pieces.len();
        let points: Vec<_> = std::iter::once(pieces[0][0])
            .chain(pieces.into_iter().flat_map(|p| [p[1], p[2], p[3]]))
            .collect();
        ensure!(
            points.iter().all(|p| p.iter().all(|v| v.is_finite())),
            "invalid ordered spline coordinates"
        );
        self.entity("SPLINE", layer);
        self.pair(100, "AcDbSpline");
        self.pair(70, if closed { 9 } else { 8 }); // planar, optionally closed
        self.pair(71, 3);
        self.pair(72, points.len() + 4);
        self.pair(73, points.len());
        self.pair(74, 0);
        for k in 0..=spans {
            for _ in 0..if k == 0 || k == spans { 4 } else { 3 } {
                self.pair(40, k);
            }
        }
        for p in &points {
            self.pair(10, num(p[0]));
            self.pair(20, num(p[1]));
            self.pair(30, 0);
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::curves::{Affine, hausdorff};
    use crate::import::{Options as ImportOptions, import_dxf};
    use nestbolt_validator::RigidTransform;
    use proptest::prelude::*;

    fn point(c: &Cubic, t: f64) -> Point {
        let u = 1.0 - t;
        let b = [u * u * u, 3.0 * u * u * t, 3.0 * u * t * t, t * t * t];
        std::array::from_fn(|k| c.iter().zip(b).map(|(p, b)| p[k] * b).sum())
    }

    #[test]
    fn cubic_spans_stay_within_the_ellipse_error_bound() {
        for sweep in [-5.1, 1.1, 2.0 * PI] {
            let s = Segment::Arc {
                center: [14.0, -22.0],
                radii: [81.0, 7.0],
                rotation: 0.9,
                start: 1.3,
                sweep,
            };
            let spans = cubics([0.0, 0.0], &s).unwrap(); // Arcs carry their own start angle.
            for c in spans {
                for i in 0..=64 {
                    let p = point(&c, f64::from(i) / 64.0);
                    let (x, y) = (p[0] - 14.0, p[1] + 22.0);
                    let a = (x * 0.9_f64.cos() + y * 0.9_f64.sin()) / 81.0;
                    let b = (-x * 0.9_f64.sin() + y * 0.9_f64.cos()) / 7.0;
                    // Radially project in the unit-circle frame, then map
                    // independently back to the rotated ellipse.
                    let angle = b.atan2(a);
                    let (ex, ey) = (81.0 * angle.cos(), 7.0 * angle.sin());
                    let expected = [
                        14.0 + ex * 0.9_f64.cos() - ey * 0.9_f64.sin(),
                        -22.0 + ex * 0.9_f64.sin() + ey * 0.9_f64.cos(),
                    ];
                    assert!((p[0] - expected[0]).hypot(p[1] - expected[1]) <= 0.00000101);
                }
            }
        }
    }

    proptest! {
        #![proptest_config(ProptestConfig::with_cases(64))]
        #[test]
        fn ellipse_cubics_meet_the_bound_across_scale_and_eccentricity(
            radius in 0.001_f64..100000.0, ratio in 0.01_f64..1.0,
            rotation in -PI..PI, start in -PI..PI, sweep in -2.0*PI..2.0*PI
        ) {
            let arc=Segment::Arc { center:[10.0,-7.0], radii:[radius,radius*ratio],
                rotation,start,sweep };
            let (s,c)=rotation.sin_cos();
            for span in cubics([0.0,0.0],&arc).unwrap() {
                for i in 0..=32 {
                    let p=point(&span,f64::from(i)/32.0);
                    let (x,y)=(p[0]-10.0,p[1]+7.0);
                    let angle=((y*c-x*s)/(radius*ratio)).atan2((x*c+y*s)/radius);
                    let (ex,ey)=(radius*angle.cos(),radius*ratio*angle.sin());
                    let expected=[10.0+ex*c-ey*s,-7.0+ex*s+ey*c];
                    prop_assert!((p[0]-expected[0]).hypot(p[1]-expected[1])<=0.00000101);
                }
            }
        }

        #[test]
        fn ordered_circular_polylines_keep_geometry_after_mirroring(
            t in 0.001_f64..0.999, angle in -PI..PI, mirror in any::<bool>(), radius in 0.1_f64..100.0
        ) {
            let original = Contour {
                start: [radius, 0.0],
                segments: vec![Segment::Arc { center: [0.0,0.0], radii: [radius,radius],
                    rotation: 0.0, start: 0.0, sweep: 2.0*PI }],
            }.transformed(&Affine::placement(&RigidTransform {
                translation: [30.0, -70.0], rotation_radians: angle, mirrored: mirror,
            }));
            let restarted = original.restarted(0,t).unwrap();
            let mut writer = Dxf { text: String::new(), handle: 0 };
            writer.ordered_contour("CUT", &restarted).unwrap();
            prop_assert!(writer.text.starts_with("0\nLWPOLYLINE\n"));
            let codes: Vec<_> = writer.text.lines().collect();
            let first_x = codes.as_chunks::<2>().0.iter().find(|p| p[0]=="10").unwrap()[1].parse::<f64>().unwrap();
            let first_y = codes.as_chunks::<2>().0.iter().find(|p| p[0]=="20").unwrap()[1].parse::<f64>().unwrap();
            prop_assert!((first_x-restarted.start[0]).hypot(first_y-restarted.start[1])<0.000001);
            let dxf = format!("0\nSECTION\n2\nENTITIES\n{}0\nENDSEC\n0\nEOF\n", writer.text);
            let imported = import_dxf(&dxf, &ImportOptions { tolerance: 0.0001, ..Default::default() }).unwrap();
            prop_assert_eq!(imported.parts.len(),1);
            prop_assert!(hausdorff(&original.flatten(0.0001).unwrap(),&imported.parts[0].polygon.outer)<0.00021);
            let mut from = imported.parts[0].outer.start;
            for s in &imported.parts[0].outer.segments {
                // The importer can add a tiny closing join after rounded
                // DXF endpoints; the circular spans must remain arcs.
                prop_assert!(matches!(s,Segment::Arc { .. }) ||
                    (from[0]-s.end()[0]).hypot(from[1]-s.end()[1])<0.000002,
                    "circle must retain its arcs except its rounded closing join");
                from=s.end();
            }
        }
    }
}
