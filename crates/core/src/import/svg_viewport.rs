//! Standalone SVG page coordinates, per SVG 2 sections 8.2 and 8.6.
//! https://www.w3.org/TR/SVG2/coords.html#ComputingAViewportsTransform
use super::{Affine, Options, length_mm, svg_transform};
use anyhow::{Context, Result, ensure};
use svgtypes::{Align, AspectRatio, ViewBox};

pub(super) fn page(
    root: roxmltree::Node,
    options: &Options,
    warnings: &mut Vec<String>,
) -> Result<Affine> {
    let view = root.attribute("viewBox").map(str::parse::<ViewBox>).transpose()
        .context("invalid SVG viewBox; set four finite values with positive width and height or re-export as plain SVG")?;
    let dimension = |name| -> Result<Option<f64>> {
        root.attribute(name).map(|value| {
            let mm = length_mm(value, options.svg_user_unit)
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
    Ok(page)
}
