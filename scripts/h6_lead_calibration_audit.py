"""Measure the authored LightBurn preview coupons; raster evidence, not a geometry gate.

The crop and attachment location are explicitly read from the saved 1920x1080
screenshots. Do not reuse them for another window size or drawing. No image is
edited. The 20x10 mm rectangle supplies the scale; dark neutral pixels exclude
the red traversal move. The narrow lead crop also excludes the preview legend.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image
import psutil


def optimization_flags(path):
    observation = json.loads(path.read_text(encoding="utf-8"))
    text = "\n".join(c["text"] for c in observation["content"] if c["type"] == "text")
    return dict(re.findall(r"\.(cb\w+) .*?toggle: (\w+)", text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    psutil.Process().cpu_affinity([0])
    folder = args.folder.resolve()
    out = args.out or folder / "calibration.json"
    if out.exists():
        raise FileExistsError(f"Preserve the existing result; choose a new --out: {out}")
    rows = []
    for name, angle, style in [("line45", 45, "line"), ("arc45", 45, "arc"), ("arc90", 90, "arc")]:
        tree = ET.parse(folder / f"{name}-native.lbrn2").getroot()
        cut = tree.find("CutSetting")
        settings = {e.tag: e.get("Value") for e in cut}
        assert settings["leadIn"] == "1"
        assert settings["leadStyle"] == style
        assert float(settings["leadLength"]) == 3
        assert float(settings["leadAngle"]) == angle
        prefs = {e.tag: e.get("Value") for e in tree.find("UIPrefs")}
        assert prefs["Optimize_OptimalEntryPoint"] == "0"
        assert prefs["Optimize_AllowReverse"] == "0"
        pixels = np.asarray(Image.open(folder / f"{name}-preview-20261015.png").convert("RGB")).astype(int)
        assert pixels.shape == (1080, 1920, 3)
        gray = (pixels.max(axis=2) - pixels.min(axis=2) < 12) & (pixels.max(axis=2) < 170)
        edge_rows = np.flatnonzero(gray[260:700, 619:1301].sum(axis=1) > 600) + 260
        top, bottom = int(edge_rows.min()), int(edge_rows.max())
        edge_columns = np.flatnonzero(gray[top, 619:1301]) + 619
        left, right = int(edge_columns.min()), int(edge_columns.max())
        scale = (right - left) / 20.0
        assert abs((bottom - top) / scale - 10) < 0.05
        # The red attachment cross is at x=960, on the rectangle's upper edge.
        yy, xx = np.nonzero(gray[260:top - 3, 800:980])
        xx, yy = xx + 800, yy + 260
        assert len(xx) >= 60
        dx, dy = xx - 960, yy - top
        row = dict(case=name, native_settings=settings, rectangle_pixels=[left, top, right, bottom],
                   pixels_per_mm=scale, attachment_pixel=[960, top], measured_pixels=len(xx),
                   raster_tolerance_mm=0.05)
        if style == "line":
            length = float(np.hypot(xx.min() - 960, yy.min() - top) / scale)
            row["measured_length_mm"] = length
            assert abs(length - 3) < 0.05
        else:
            radius = 3 / math.radians(angle)
            fitted_radius = float(-np.sum(dy * (dx * dx + dy * dy)) / (2 * np.sum(dy * dy)) / scale)
            residual = np.abs(np.sqrt((dx / scale) ** 2 + (dy / scale + radius) ** 2) - radius)
            row.update(expected_radius_mm=radius, fitted_radius_mm=fitted_radius,
                       max_radial_residual_mm=float(residual.max()),
                       original_plan_radius_mm=1.5,
                       original_plan_radius_error_mm=abs(fitted_radius - 1.5))
            assert abs(fitted_radius - radius) < 0.05
            assert residual.max() < 0.05
            assert abs(fitted_radius - 1.5) > 0.25
        rows.append(row)
    original = optimization_flags(folder / "optimization-original-20261015.json")
    restored = optimization_flags(folder / "optimization-restored-20261015.json")
    assert len(original) >= 10 and original == restored
    evidence = [p for p in sorted(folder.iterdir()) if p.is_file() and p != out]
    result = dict(date="2026-10-15", scope="Authored development coupon; native raster calibration only",
                  application="LightBurn Pro 2.1.01", cpu_affinity=psutil.Process().cpu_affinity(),
                  rows=rows, optimization_restored=original, all_checks_pass=True,
                  limitations=["Raster tolerance 0.05 mm; not the 0.01 mm vector fidelity gate",
                               "Outer straight edge only; holes, corners, reversal, zero angle and searched exports pending"],
                  sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence})
    with out.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps(dict(all_checks_pass=True, cases=len(rows), output=str(out))))


if __name__ == "__main__":
    main()
