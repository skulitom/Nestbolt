//! Compact and legacy LightBurn path syntax. Original lists remain in the XML.
use anyhow::{Context, Result, bail, ensure};
use roxmltree::Node;

use super::{Path, Resources, number};
use crate::curves::{Contour, Point, Segment};

#[derive(Clone, Debug)]
struct Vertex {
    point: Point,
    outgoing: Option<Point>,
    incoming: Option<Point>,
}

#[derive(Clone, Copy)]
struct Primitive {
    from: usize,
    to: usize,
    cubic: bool,
}

fn handle(x: Option<f64>, y: Option<f64>) -> Option<Point> {
    match (x, y) {
        (None, None) | (Some(1.0), None) => None,
        // Native 2.1.01 omits a zero coordinate of an otherwise present handle.
        // A lone x=1 is reserved as the absent-handle marker instead.
        _ => Some([x.unwrap_or(0.0), y.unwrap_or(0.0)]),
    }
}

struct Scanner<'a>(&'a str);
impl Scanner<'_> {
    fn trim(&mut self) {
        self.0 = self.0.trim_start();
    }
    fn take(&mut self, token: &str) -> bool {
        self.trim();
        if let Some(rest) = self.0.strip_prefix(token) {
            self.0 = rest;
            true
        } else {
            false
        }
    }
    fn number(&mut self) -> Result<f64> {
        self.trim();
        let text = self.0.as_bytes();
        let mut i = usize::from(matches!(text.first(), Some(b'+' | b'-')));
        let mut digits = 0;
        while i < text.len() && text[i].is_ascii_digit() {
            i += 1;
            digits += 1;
        }
        if text.get(i) == Some(&b'.') {
            i += 1;
            while i < text.len() && text[i].is_ascii_digit() {
                i += 1;
                digits += 1;
            }
        }
        ensure!(
            digits > 0,
            "expected a number in LightBurn path near {:?}",
            self.0.chars().take(32).collect::<String>()
        );
        if matches!(text.get(i), Some(b'e' | b'E')) {
            i += 1;
            i += usize::from(matches!(text.get(i), Some(b'+' | b'-')));
            let first = i;
            while i < text.len() && text[i].is_ascii_digit() {
                i += 1;
            }
            ensure!(i > first, "invalid exponent in LightBurn path");
        }
        let value = self.0[..i].parse::<f64>()?;
        ensure!(value.is_finite(), "non-finite LightBurn coordinate");
        self.0 = &self.0[i..];
        Ok(value)
    }
    fn index(&mut self) -> Result<usize> {
        self.trim();
        let len = self.0.bytes().take_while(u8::is_ascii_digit).count();
        ensure!(
            len > 0,
            "expected an integer vertex index in LightBurn primitive"
        );
        let index = self.0[..len].parse::<usize>()?;
        self.0 = &self.0[len..];
        Ok(index)
    }
}

fn compact_vertices(text: &str) -> Result<Vec<Vertex>> {
    let mut s = Scanner(text);
    let mut vertices = vec![];
    while {
        s.trim();
        !s.0.is_empty()
    } {
        ensure!(s.take("V"), "expected V in LightBurn VertList");
        let point = [s.number()?, s.number()?];
        let mut handles = [None; 4];
        loop {
            s.trim();
            if s.0.is_empty() || s.0.starts_with('V') {
                break;
            }
            if s.take("S") {
                continue;
            }
            let field = ["c0x", "c0y", "c1x", "c1y"]
                .iter()
                .position(|name| s.take(name))
                .context(
                    "unknown vertex field in LightBurn VertList; re-save the project in LightBurn",
                )?;
            ensure!(
                handles[field].is_none(),
                "repeated handle coordinate in LightBurn vertex"
            );
            handles[field] = Some(s.number()?);
        }
        // A lone c0x1/c1x1 is LightBurn's missing-handle sentinel.
        vertices.push(Vertex {
            point,
            outgoing: handle(handles[0], handles[1]),
            incoming: handle(handles[2], handles[3]),
        });
    }
    Ok(vertices)
}

fn compact_primitives(text: &str, vertex_count: usize) -> Result<Vec<Primitive>> {
    let text = text.trim();
    if matches!(text, "LineClosed" | "LineOpen") {
        let edges = if text == "LineClosed" {
            vertex_count
        } else {
            vertex_count.saturating_sub(1)
        };
        return Ok((0..edges)
            .map(|i| Primitive {
                from: i,
                to: (i + 1) % vertex_count,
                cubic: false,
            })
            .collect());
    }
    let mut s = Scanner(text);
    let mut primitives = vec![];
    while {
        s.trim();
        !s.0.is_empty()
    } {
        let cubic = if s.take("L") {
            false
        } else if s.take("B") {
            true
        } else {
            bail!("unknown LightBurn primitive; expected L or B")
        };
        primitives.push(Primitive {
            from: s.index()?,
            to: s.index()?,
            cubic,
        });
    }
    Ok(primitives)
}

pub(super) fn read(
    node: Node,
    resources: &Resources,
    warnings: &mut Vec<String>,
    shape_index: usize,
) -> Result<Vec<Path>> {
    let vertices = if let Some(list) = resources.list(node, "VertList", "VertID")? {
        compact_vertices(list.text().unwrap_or(""))?
    } else {
        node.children()
            .filter(|n| n.has_tag_name("V"))
            .map(|v| {
                let read_handle = |x, y| -> Result<Option<Point>> {
                    let coordinate =
                        |name| v.attribute(name).map(|_| number(v, name, None)).transpose();
                    Ok(handle(coordinate(x)?, coordinate(y)?))
                };
                Ok(Vertex {
                    point: [number(v, "vx", None)?, number(v, "vy", None)?],
                    outgoing: read_handle("c0x", "c0y")?,
                    incoming: read_handle("c1x", "c1y")?,
                })
            })
            .collect::<Result<Vec<_>>>()?
    };
    let primitives = if let Some(list) = resources.list(node, "PrimList", "PrimID")? {
        compact_primitives(list.text().unwrap_or(""), vertices.len())?
    } else {
        node.children()
            .filter(|n| n.has_tag_name("P"))
            .map(|p| {
                let index = |name| -> Result<usize> {
                    p.attribute(name)
                        .with_context(|| format!("missing {name} in LightBurn primitive"))?
                        .parse()
                        .context("invalid LightBurn vertex index")
                };
                let cubic = match p.attribute("T") {
                    Some("L") => false,
                    Some("B") => true,
                    _ => bail!("unknown legacy LightBurn primitive; expected L or B"),
                };
                Ok(Primitive {
                    from: index("p0")?,
                    to: index("p1")?,
                    cubic,
                })
            })
            .collect::<Result<Vec<_>>>()?
    };
    ensure!(
        vertices.is_empty() == primitives.is_empty(),
        "LightBurn Path has vertices without primitives or primitives without vertices; re-save the project"
    );
    ensure!(
        primitives
            .iter()
            .all(|p| p.from < vertices.len() && p.to < vertices.len()),
        "LightBurn primitive refers to a missing vertex; re-save the project"
    );
    let missing = primitives
        .iter()
        .filter(|p| {
            p.cubic && (vertices[p.from].outgoing.is_none() || vertices[p.to].incoming.is_none())
        })
        .count();
    if missing > 0 {
        let straight = primitives
            .iter()
            .filter(|p| {
                p.cubic && vertices[p.from].outgoing.is_none() && vertices[p.to].incoming.is_none()
            })
            .count();
        warnings.push(format!(
            "LightBurn shape {shape_index}: native endpoint fallback for missing Bezier control points; affected segments: {missing}, straight line segments with both controls absent: {straight}; original XML is preserved"
        ));
    }
    let start_override = node
        .attribute("StartV")
        .map(str::parse::<usize>)
        .transpose()
        .context("invalid LightBurn StartV")?;
    if let Some(start) = start_override {
        ensure!(
            start < vertices.len(),
            "LightBurn StartV refers to a missing vertex"
        );
    }
    let mut groups: Vec<Vec<Primitive>> = vec![];
    for primitive in primitives {
        let new = groups.last().is_none_or(|g| {
            let last = g.last().expect("nonempty primitive group");
            last.to != primitive.from || last.to == g[0].from
        });
        if new {
            groups.push(vec![]);
        }
        groups.last_mut().expect("primitive group").push(primitive);
    }
    let mut paths = vec![];
    for mut group in groups {
        let end = group.last().expect("primitive group").to;
        let closed = group[0].from == end || vertices[group[0].from].point == vertices[end].point;
        if closed
            && let Some(start) = start_override
            && let Some(i) = group.iter().position(|p| p.from == start)
        {
            group.rotate_left(i);
        }
        let start = vertices[group[0].from].point;
        let segments = group
            .iter()
            .map(|p| {
                let a = &vertices[p.from];
                let b = &vertices[p.to];
                if p.cubic {
                    Segment::Cubic {
                        controls: [a.outgoing.unwrap_or(a.point), b.incoming.unwrap_or(b.point)],
                        to: b.point,
                    }
                } else {
                    Segment::Line { to: b.point }
                }
            })
            .collect();
        paths.push(Path {
            closed,
            curve: Contour { start, segments },
        });
    }
    Ok(paths)
}
