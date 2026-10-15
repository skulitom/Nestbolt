//! Optional, bounded translation search on exact source cutting edges.
//!
//! Placement cost is material / starting material - saved cut / total cut.
//! Stock use may grow by at most 1% of this phase's independently valid start;
//! the external equal-budget H5 comparison still has to measure its own guard.
//! Rotations, sheet assignments, quantities and the independent validator stay
//! unchanged. Collision envelopes (including lead reservations) remain binding.
use super::*;
use crate::clock::{Clock, Timing, Work};
use crate::sheets::{Progress, SheetResult};
use jagua_rs::Instant;

pub(crate) struct Bonus<'a> {
    pub job: &'a Job,
    pub outlines: &'a HashMap<String, Outline>,
    pub options: Options,
}

struct PartEdges {
    sheet: String,
    edges: Vec<Edge>,
    bounds: [f64; 4],
}

fn shifted(edges: &[Edge], delta: Point) -> Vec<Edge> {
    edges
        .iter()
        .map(|e| Edge {
            a: add(e.a, delta),
            b: add(e.b, delta),
            ..e.clone()
        })
        .collect()
}

fn length_against(edges: &[Edge], others: &[&PartEdges], owners: &[String]) -> f64 {
    // This is a proposal score. Every accepted move is rescored with analyze's
    // unioned source coverage and unique COMMON paths, never this pair sum.
    edges
        .iter()
        .flat_map(|a| {
            others.iter().flat_map(move |part| {
                part.edges.iter().filter_map(move |b| {
                    match_edges(a, b, owners).map(|s| distance(s.from_mm, s.to_mm))
                })
            })
        })
        .sum()
}

fn totals(reports: &[Report]) -> (f64, f64) {
    (
        reports.iter().map(|r| r.cut_length_without_common_mm).sum(),
        reports.iter().map(|r| r.saved_length_mm).sum(),
    )
}

impl Bonus<'_> {
    pub(crate) fn refine(
        &self,
        collision: &Job,
        result: &mut SheetResult,
        clock: &Clock,
        until: f64,
        progress: &mut impl FnMut(&Progress, &dyn Fn() -> Option<Layout>),
    ) -> Result<()> {
        if !result.validation.valid || clock.now() >= until {
            return Ok(());
        }
        let start = Instant::now();
        let (total, mut saved) = totals(&analyze(
            self.job,
            &result.layout,
            self.outlines,
            self.options,
        )?);
        clock.validated(self.job, &result.layout);
        let mut check_cost = start.elapsed().as_secs_f64();
        if total <= EPS {
            return Ok(());
        }
        let baseline_material = result.validation.metrics.as_ref().unwrap().material_area;
        if baseline_material <= EPS {
            return Ok(());
        }
        let mut cost = 1.0 - saved / total;
        let owners: Vec<_> = result
            .layout
            .placements
            .iter()
            .map(|p| format!("{}#{}", p.part_id, p.copy_index))
            .collect();
        let mut contours = HashMap::new();
        for sheet in &result.layout.sheets {
            contours.extend(placed(self.job, &result.layout, &sheet.id, self.outlines)?.0);
        }
        let mut parts = vec![];
        for (index, p) in result.layout.placements.iter().enumerate() {
            let outer = &contours[&owners[index]][0];
            let polygon = outer.flatten(0.0005)?;
            let bounds = polygon.iter().fold(
                [
                    f64::INFINITY,
                    f64::INFINITY,
                    f64::NEG_INFINITY,
                    f64::NEG_INFINITY,
                ],
                |b, p| {
                    [
                        b[0].min(p[0]),
                        b[1].min(p[1]),
                        b[2].max(p[0]),
                        b[3].max(p[1]),
                    ]
                },
            );
            let mut edges = edges(outer, index, self.options.kerf_mm / 2.0)?.0;
            edges.retain(|e| e.length + EPS >= MIN_SHARED_MM);
            parts.push(PartEdges {
                sheet: p.sheet_id.clone(),
                edges,
                bounds,
            });
        }
        let n = parts.len();
        for pass in 0..4 {
            let before = result.stats.common_line_moves;
            for step in 0..n {
                let finish = match clock.timing() {
                    Timing::Wall => until - check_cost * 1.5,
                    Timing::Work => until,
                };
                if clock.now() >= finish {
                    return Ok(());
                }
                let index = (step + (result.seed % n as u64) as usize + pass) % n;
                let part = &parts[index];
                if part.edges.is_empty() {
                    continue;
                }
                let b = part.bounds;
                // Local moves only. Endpoint alignments also move tangentially
                // so unequal edges can share their full overlapping length.
                let reach = 0.25 * (b[2] - b[0]).hypot(b[3] - b[1]).max(40.0);
                let nearby: Vec<_> = parts
                    .iter()
                    .enumerate()
                    .filter(|(i, p)| {
                        *i != index
                            && p.sheet == part.sheet
                            && p.bounds[0] <= b[2] + reach + self.options.kerf_mm
                            && p.bounds[2] >= b[0] - reach - self.options.kerf_mm
                            && p.bounds[1] <= b[3] + reach + self.options.kerf_mm
                            && p.bounds[3] >= b[1] - reach - self.options.kerf_mm
                    })
                    .map(|(_, p)| p)
                    .collect();
                let old_shared = length_against(&part.edges, &nearby, &owners);
                let mut deltas = vec![];
                for a in &part.edges {
                    if clock.now() >= finish {
                        return Ok(());
                    }
                    for other in &nearby {
                        clock.charge(Work::EvaluatedVertex, other.edges.len() as f64);
                        for e in &other.edges {
                            if dot(a.normal, e.normal) > -0.999999999 {
                                continue;
                            }
                            // Leave 0.000001 mm of numerical clearance, far
                            // below the 0.01 mm COMMON detection tolerance.
                            let normal = dot(sub(e.a, a.a), a.normal) - 0.000001;
                            if normal.abs() > reach {
                                continue;
                            }
                            for tangent in [
                                0.0,
                                dot(sub(e.a, a.b), a.u),
                                dot(sub(e.b, a.a), a.u),
                                dot(sub(mul(add(e.a, e.b), 0.5), mul(add(a.a, a.b), 0.5)), a.u),
                            ] {
                                let delta = add(mul(a.normal, normal), mul(a.u, tangent));
                                if delta[0].hypot(delta[1]) <= reach
                                    && delta[0].hypot(delta[1]) > EPS
                                {
                                    deltas.push(delta);
                                }
                            }
                        }
                    }
                }
                deltas.sort_by(|a, b| a[0].total_cmp(&b[0]).then(a[1].total_cmp(&b[1])));
                deltas.dedup_by(|a, b| distance(*a, *b) < 1e-7);
                deltas.sort_by(|a, b| a[0].hypot(a[1]).total_cmp(&b[0].hypot(b[1])));
                deltas.truncate(512);
                let mut candidates = vec![];
                for delta in deltas {
                    if clock.now() >= finish {
                        return Ok(());
                    }
                    clock.charge(
                        Work::EvaluatedVertex,
                        (part.edges.len() * nearby.iter().map(|p| p.edges.len()).sum::<usize>())
                            as f64,
                    );
                    let new_edges = shifted(&part.edges, delta);
                    let gain = length_against(&new_edges, &nearby, &owners) - old_shared;
                    if gain > 1e-6 {
                        candidates.push((gain, delta, new_edges));
                    }
                }
                candidates.sort_by(|a, b| b.0.total_cmp(&a.0));
                for (_, delta, new_edges) in candidates.into_iter().take(32) {
                    if clock.now() >= finish {
                        return Ok(());
                    }
                    let started = Instant::now();
                    let mut trial = result.layout.clone();
                    let translation = &mut trial.placements[index].transform.translation;
                    translation[0] += delta[0] / trial.units.to_mm();
                    translation[1] += delta[1] / trial.units.to_mm();
                    let checked = validate(collision, &trial)?;
                    clock.validated(collision, &trial);
                    let material = checked.metrics.as_ref().map(|m| m.material_area);
                    let proposed = if checked.valid
                        && material.is_some_and(|m| m <= baseline_material * 1.01)
                    {
                        // Also enforces no parts in holes, using original curves.
                        let reports = analyze(self.job, &trial, self.outlines, self.options);
                        clock.validated(self.job, &trial);
                        reports.ok().map(|r| (checked, totals(&r).1))
                    } else {
                        None
                    };
                    check_cost = check_cost.max(started.elapsed().as_secs_f64());
                    if let Some((checked, new_saved)) = proposed {
                        let metrics = checked.metrics.as_ref().unwrap();
                        let new_cost =
                            metrics.material_area / baseline_material - new_saved / total;
                        if new_saved <= saved + 1e-6 || new_cost >= cost - 1e-12 {
                            continue;
                        }
                        cost = new_cost;
                        saved = new_saved;
                        let update = Progress {
                            elapsed_seconds: clock.now(),
                            stage: "common-line",
                            sheets: metrics.sheets_used,
                            material: metrics.normalized_material,
                        };
                        progress(&update, &|| Some(trial.clone()));
                        result.history.push(update);
                        result.accepted_at_seconds = update.elapsed_seconds;
                        result.layout = trial;
                        result.validation = checked;
                        result.stats.common_line_moves += 1;
                        parts[index].edges = new_edges;
                        parts[index].bounds = [
                            b[0] + delta[0],
                            b[1] + delta[1],
                            b[2] + delta[0],
                            b[3] + delta[1],
                        ];
                        break;
                    }
                }
            }
            if result.stats.common_line_moves == before {
                break;
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use nestbolt_validator::job::{
        Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle,
    };
    use nestbolt_validator::{RigidTransform, Units};

    fn fixture() -> (Job, Layout) {
        let job = Job {
            version: 1,
            name: "shared-cut translation".into(),
            units: Units::Mm,
            parts: vec![Part {
                id: "p".into(),
                quantity: 2,
                geometry: vec![rectangle(0.0, 0.0, 20.0, 30.0)],
                rotations: Rotations::List { degrees: vec![0.0] },
                allow_mirror: false,
                priority: 1.0,
            }],
            stocks: vec![Stock {
                id: "s".into(),
                width: 100.0,
                height: 100.0,
                count: None,
                margins: Margins::default(),
                outline: vec![],
                defects: vec![],
            }],
            clearance: 0.2,
            edge_clearance: 1.0,
            mode: Mode::All,
        };
        let layout = Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![Sheet {
                id: "sheet".into(),
                stock_id: "s".into(),
            }],
            placements: [1.0, 22.0]
                .iter()
                .enumerate()
                .map(|(i, x)| Placement {
                    part_id: "p".into(),
                    copy_index: i as u32,
                    sheet_id: "sheet".into(),
                    transform: RigidTransform {
                        translation: [*x, 1.0],
                        ..Default::default()
                    },
                })
                .collect(),
        };
        (job, layout)
    }

    fn refine(job: &Job, collision: &Job, layout: Layout) -> SheetResult {
        let validation = validate(collision, &layout).unwrap();
        assert!(validation.valid, "{:?}", validation.violations);
        let mut result = SheetResult {
            algorithm: "test",
            seed: 0,
            seconds: 10.0,
            warm_start: validation.metrics.clone().unwrap(),
            unsupported: None,
            riders: 0,
            layout,
            validation,
            history: vec![],
            stats: Default::default(),
            accepted_at_seconds: 0.0,
            elapsed_seconds: 0.0,
            work: 0.0,
            counts: Default::default(),
            repeatable: true,
        };
        Bonus {
            job,
            outlines: &HashMap::new(),
            options: Options {
                kerf_mm: 0.2,
                search_bonus: true,
            },
        }
        .refine(
            collision,
            &mut result,
            &Clock::new(Timing::Work, 30.0),
            10.0,
            &mut |_, _| {},
        )
        .unwrap();
        result
    }

    #[test]
    fn aligns_original_edges_with_repeatable_valid_moves() {
        let (job, layout) = fixture();
        let first = refine(&job, &job, layout.clone());
        let second = refine(&job, &job, layout);
        assert!(first.stats.common_line_moves > 0);
        assert_eq!(
            serde_json::to_value(&first.layout).unwrap(),
            serde_json::to_value(&second.layout).unwrap()
        );
        let r = analyze(
            &job,
            &first.layout,
            &HashMap::new(),
            Options {
                kerf_mm: 0.2,
                search_bonus: true,
            },
        )
        .unwrap();
        assert!((r[0].saved_length_mm - 30.0).abs() < 1e-5);
        assert!(first.validation.valid);
        assert!(
            first.validation.metrics.as_ref().unwrap().material_area
                <= first.warm_start.material_area * 1.01
        );
        for p in &first.layout.placements {
            assert_eq!(p.transform.rotation_radians, 0.0);
            assert!(!p.transform.mirrored);
        }
    }

    #[test]
    fn cannot_cross_a_stock_defect_to_share_a_cut() {
        let (mut job, layout) = fixture();
        job.edge_clearance = 0.1;
        job.stocks[0].defects = vec![rectangle(21.4, 0.0, 0.2, 100.0)];
        let r = refine(&job, &job, layout.clone());
        assert_eq!(r.stats.common_line_moves, 0);
        assert_eq!(
            serde_json::to_value(r.layout).unwrap(),
            serde_json::to_value(layout).unwrap()
        );
    }

    #[test]
    fn lead_reservation_envelopes_remain_binding() {
        let (job, mut layout) = fixture();
        layout.placements[1].transform.translation[0] = 25.0;
        let mut collision = job.clone();
        collision.parts[0].geometry = vec![rectangle(0.0, 0.0, 23.0, 30.0)];
        let r = refine(&job, &collision, layout.clone());
        assert_eq!(r.stats.common_line_moves, 0);
        assert_eq!(
            serde_json::to_value(r.layout).unwrap(),
            serde_json::to_value(layout).unwrap()
        );
    }

    #[test]
    fn search_bonus_is_opt_in() {
        let default: Options = serde_json::from_str(r#"{"kerf_mm":0.2}"#).unwrap();
        assert!(!default.search_bonus);
    }
}
