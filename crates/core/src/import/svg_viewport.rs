//! Standalone SVG page coordinates, per SVG 2 sections 8.2 and 8.6.
//! https://www.w3.org/TR/SVG2/coords.html#ComputingAViewportsTransform
use super::{Affine, Options, svg_transform};
use anyhow::{Context, Result, ensure};
use svgtypes::{Align, AspectRatio, Length, LengthUnit, ViewBox};

fn parse_length(value: &str) -> Option<Length> {
    let value = value.trim();
    if let Ok(length) = value.parse() {
        return Some(length);
    }
    let value = value.to_ascii_lowercase();
    if let Some(quarters) = value.strip_suffix('q') {
        return Some(Length::new(
            quarters.parse::<svgtypes::Number>().ok()?.0 / 4.0,
            LengthUnit::Mm,
        ));
    }
    value.parse().ok()
}

pub(super) struct Page {
    pub transform: Affine,
    // Percentages use the viewBox dimensions, or the viewport size in its absence.
    width: Option<f64>,
    height: Option<f64>,
}

fn length_mm(length: Length, user_unit: f64) -> Option<f64> {
    use LengthUnit as U;
    let n = length.number;
    Some(match length.unit {
        U::None if user_unit != 25.4 / 96.0 => n * user_unit,
        U::None | U::Px => n * 25.4 / 96.0,
        U::Mm => n,
        U::Cm => n * 10.0,
        U::In => n * 25.4,
        U::Pt => n * 25.4 / 72.0,
        U::Pc => n * 25.4 / 6.0,
        U::Em | U::Ex | U::Percent => return None,
    })
}

impl Page {
    pub fn use_translation(&self, node: roxmltree::Node) -> Result<Affine> {
        Ok(Affine::translation([
            self.length(node, "x")?.unwrap_or(0.0),
            self.length(node, "y")?.unwrap_or(0.0),
        ]))
    }

    pub fn length(&self, node: roxmltree::Node, name: &str) -> Result<Option<f64>> {
        let Some(value) = node.attribute(name) else {
            return Ok(None);
        };
        if value.trim().eq_ignore_ascii_case("auto")
            && matches!(name, "width" | "height" | "rx" | "ry")
        {
            return Ok(None);
        }
        let local = parse_length(value).and_then(|len| match len.unit {
            LengthUnit::None | LengthUnit::Px => Some(len.number),
            LengthUnit::Percent | LengthUnit::Em | LengthUnit::Ex if len.number == 0.0 => Some(0.0),
            LengthUnit::Percent => {
                let basis = match name {
                    "r" => self.width?.hypot(self.height?) / std::f64::consts::SQRT_2,
                    "y" | "cy" | "ry" | "y1" | "y2" | "height" => self.height?,
                    _ => self.width?,
                };
                Some(len.number / 100.0 * basis)
            }
            _ => length_mm(len, 25.4 / 96.0).map(|mm| mm * (96.0 / 25.4)),
        });
        local.filter(|n| n.is_finite()).map(Some).with_context(|| format!(
            "cannot resolve SVG <{}> {name}={value:?}. Use a finite numeric or absolute length, set a page size for percentages, or convert the shape to a path",
            node.tag_name().name()
        ))
    }
}

pub(super) fn page(
    root: roxmltree::Node,
    options: &Options,
    warnings: &mut Vec<String>,
) -> Result<Page> {
    let view = root.attribute("viewBox").map(str::parse::<ViewBox>).transpose()
        .context("invalid SVG viewBox; set four finite values with positive width and height or re-export as plain SVG")?;
    let dimension = |name| -> Result<Option<f64>> {
        root.attribute(name).map(|value| {
            let mm = parse_length(value).and_then(|len| length_mm(len, options.svg_user_unit))
                .with_context(|| format!("SVG {name} {value:?} has no absolute size; set page width and height in mm or pixels before importing"))?;
            ensure!(mm.is_finite() && mm > 0.0,
                "SVG {name} must be finite and positive; set a positive page size before importing");
            // The outer transform acts in viewport units, outside the viewBox.
            Ok(mm / options.svg_user_unit)
        }).transpose()
    };
    let (width, height) = (dimension("width")?, dimension("height")?);
    let viewport = if let Some(v) = view {
        ensure!(
            [v.x, v.y, v.w, v.h].iter().all(|n| n.is_finite()) && v.w > 0.0 && v.h > 0.0,
            "SVG viewBox must be finite with positive width and height; repair the page size before importing"
        );
        // A standalone drawing with one absolute dimension inherits the viewBox
        // aspect ratio for the other. Without either, preserve the configured
        // user-unit scale instead of inventing a browser embedding viewport.
        let w = width.unwrap_or_else(|| height.map_or(v.w, |h| h * v.w / v.h));
        let h = height.unwrap_or_else(|| width.map_or(v.h, |w| w * v.h / v.w));
        let aspect = root.attribute("preserveAspectRatio").map(str::parse::<AspectRatio>).transpose()
            .context("invalid SVG preserveAspectRatio; use none or an xMin/xMid/xMax YMin/YMid/YMax alignment with meet or slice")?
            .unwrap_or_default();
        let (mut sx, mut sy) = (w / v.w, h / v.h);
        if aspect.align != Align::None {
            let scale = if aspect.slice { sx.max(sy) } else { sx.min(sy) };
            (sx, sy) = (scale, scale);
        }
        let ax = match aspect.align {
            Align::XMidYMin | Align::XMidYMid | Align::XMidYMax => 0.5,
            Align::XMaxYMin | Align::XMaxYMid | Align::XMaxYMax => 1.0,
            _ => 0.0,
        };
        let ay = match aspect.align {
            Align::XMinYMid | Align::XMidYMid | Align::XMaxYMid => 0.5,
            Align::XMinYMax | Align::XMidYMax | Align::XMaxYMax => 1.0,
            _ => 0.0,
        };
        if aspect.slice
            && aspect.align != Align::None
            && ((w - v.w * sx).abs() > 1e-9 || (h - v.h * sy).abs() > 1e-9)
        {
            warnings.push("SVG preserveAspectRatio slice: imported complete paths without viewport clipping; convert the visible edges to closed paths before cutting if page clipping is intended".into());
        }
        Affine {
            m: [[sx, 0.0], [0.0, sy]],
            t: [
                -v.x * sx + (w - v.w * sx) * ax,
                -v.y * sy + (h - v.h * sy) * ay,
            ],
        }
    } else {
        Affine::IDENTITY
    };
    let page = viewport
        .then(svg_transform(root.attribute("transform"))?)
        .then(Affine {
            m: [[options.svg_user_unit, 0.0], [0.0, -options.svg_user_unit]],
            t: [0.0, 0.0],
        });
    ensure!(
        page.m
            .iter()
            .flatten()
            .chain(page.t.iter())
            .all(|n| n.is_finite())
            && page.determinant() != 0.0,
        "SVG page transform is non-finite or collapses the drawing; apply a finite, nonzero transform before importing"
    );
    Ok(Page {
        transform: page,
        width: view.map(|v| v.w).or(width),
        height: view.map(|v| v.h).or(height),
    })
}
