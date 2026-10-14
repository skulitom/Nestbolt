//! Union coincident straight spans, split intersections, then find a minimum
//! trail decomposition. Virtual edges pair odd-degree vertices; removing them
//! from Euler circuits gives max(1, odd/2) paths per connected component.
use super::{EPS, add, cross, distance, dot, mul, sub};
use crate::curves::{Contour, Point, Segment};
use std::collections::BTreeSet;

fn merge(a: [Point; 2], b: [Point; 2]) -> Option<[Point; 2]> {
    let len = distance(a[0], a[1]);
    let u = mul(sub(a[1], a[0]), 1.0 / len);
    if cross(sub(b[0], a[0]), u).abs() > EPS || cross(sub(b[1], a[0]), u).abs() > EPS {
        return None;
    }
    let p = dot(sub(b[0], a[0]), u);
    let q = dot(sub(b[1], a[0]), u);
    if p.min(q) > len + EPS || p.max(q) < -EPS {
        return None;
    }
    Some([
        add(a[0], mul(u, p.min(q).min(0.0))),
        add(a[0], mul(u, p.max(q).max(len))),
    ])
}

pub(super) fn paths(mut lines: Vec<[Point; 2]>) -> Vec<Contour> {
    lines.retain(|s| distance(s[0], s[1]) > EPS);
    let mut i = 0;
    while i < lines.len() {
        let mut j = i + 1;
        while j < lines.len() {
            if let Some(union) = merge(lines[i], lines[j]) {
                lines[i] = union;
                lines.remove(j);
                j = i + 1;
            } else {
                j += 1;
            }
        }
        i += 1;
    }
    let mut splits = vec![vec![0.0, 1.0]; lines.len()];
    for i in 0..lines.len() {
        let a = lines[i];
        let r = sub(a[1], a[0]);
        for j in i + 1..lines.len() {
            let b = lines[j];
            let s = sub(b[1], b[0]);
            let denominator = cross(r, s);
            if denominator.abs() < 1e-12 {
                continue;
            }
            let delta = sub(b[0], a[0]);
            let t = cross(delta, s) / denominator;
            let u = cross(delta, r) / denominator;
            if (-EPS..=1.0 + EPS).contains(&t) && (-EPS..=1.0 + EPS).contains(&u) {
                splits[i].push(t.clamp(0.0, 1.0));
                splits[j].push(u.clamp(0.0, 1.0));
            }
        }
    }
    let mut points: Vec<Point> = vec![];
    let mut edges = vec![];
    let mut unique = BTreeSet::new();
    for (line, mut values) in lines.into_iter().zip(splits) {
        values.sort_by(f64::total_cmp);
        values.dedup_by(|a, b| (*a - *b).abs() < 1e-12);
        for interval in values.windows(2) {
            let mut nodes = [0; 2];
            for k in 0..2 {
                let p = add(line[0], mul(sub(line[1], line[0]), interval[k]));
                nodes[k] = match points.iter().position(|q| distance(*q, p) < EPS) {
                    Some(index) => index,
                    None => {
                        points.push(p);
                        points.len() - 1
                    }
                };
            }
            if nodes[0] != nodes[1]
                && unique.insert((nodes[0].min(nodes[1]), nodes[0].max(nodes[1])))
            {
                edges.push((nodes[0], nodes[1], false));
            }
        }
    }
    let mut adjacency = vec![vec![]; points.len()];
    for (id, &(a, b, _)) in edges.iter().enumerate() {
        adjacency[a].push((b, id));
        adjacency[b].push((a, id));
    }
    let mut seen = vec![false; points.len()];
    let mut roots = vec![];
    for root in 0..points.len() {
        if seen[root] {
            continue;
        }
        roots.push(root);
        let mut stack = vec![root];
        seen[root] = true;
        let mut odd = vec![];
        while let Some(node) = stack.pop() {
            if adjacency[node].len() % 2 == 1 {
                odd.push(node);
            }
            for &(next, _) in &adjacency[node] {
                if !seen[next] {
                    seen[next] = true;
                    stack.push(next);
                }
            }
        }
        odd.sort_unstable();
        for pair in odd.as_chunks::<2>().0 {
            let id = edges.len();
            edges.push((pair[0], pair[1], true));
            adjacency[pair[0]].push((pair[1], id));
            adjacency[pair[1]].push((pair[0], id));
        }
    }
    let mut used = vec![false; edges.len()];
    let mut output = vec![];
    for root in roots {
        let mut stack = vec![(root, None)];
        let mut reverse = vec![];
        while let Some(&(node, _)) = stack.last() {
            while adjacency[node].last().is_some_and(|(_, id)| used[*id]) {
                adjacency[node].pop();
            }
            if let Some((next, id)) = adjacency[node].pop() {
                used[id] = true;
                stack.push((next, Some(id)));
            } else {
                reverse.push(stack.pop().unwrap());
            }
        }
        reverse.reverse();
        let mut walk: Vec<_> = reverse
            .windows(2)
            .map(|p| (p[0].0, p[1].0, p[1].1.unwrap()))
            .collect();
        if let Some(fake) = walk.iter().position(|(_, _, id)| edges[*id].2) {
            let size = walk.len();
            walk.rotate_left((fake + 1) % size);
        }
        let mut contour: Option<Contour> = None;
        for (a, b, id) in walk {
            if edges[id].2 {
                if let Some(c) = contour.take() {
                    output.push(c);
                }
            } else {
                contour
                    .get_or_insert_with(|| Contour {
                        start: points[a],
                        segments: vec![],
                    })
                    .segments
                    .push(Segment::Line { to: points[b] });
            }
        }
        if let Some(c) = contour {
            output.push(c);
        }
    }
    output
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn overlap_union_and_crossing_have_no_retraced_edges_and_minimum_trails() {
        let output = paths(vec![
            [[0.0, 0.0], [20.0, 0.0]],
            [[15.0, 0.0], [5.0, 0.0]],
            [[10.0, -10.0], [10.0, 10.0]],
        ]);
        assert_eq!(output.len(), 2); // Four odd vertices need exactly two trails.
        let total: f64 = output.iter().map(super::super::length::contour).sum();
        assert!((total - 40.0).abs() < EPS);
        assert_eq!(output.iter().map(|p| p.segments.len()).sum::<usize>(), 4);
    }

    #[test]
    fn loop_attached_to_a_branch_does_not_get_stranded_in_an_extra_path() {
        let output = paths(vec![
            [[0.0, 0.0], [10.0, 0.0]],
            [[10.0, 0.0], [10.0, 10.0]],
            [[10.0, 10.0], [0.0, 10.0]],
            [[0.0, 10.0], [0.0, 0.0]],
            [[0.0, 0.0], [-10.0, 0.0]],
        ]);
        assert_eq!(output.len(), 1);
        assert!((super::super::length::contour(&output[0]) - 50.0).abs() < EPS);
    }
}
