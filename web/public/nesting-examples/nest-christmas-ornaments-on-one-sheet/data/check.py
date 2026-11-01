"""Independent check of Nestbolt's exported sheets (no Nestbolt code): reads each sheet-*.svg, rebuilds every placed
ornament as a polygon with its hole, and checks the copy counts, the shapes against ornaments.svg, the 6 mm border
(5 mm margin + 1 mm edge spacing) and the 2 mm spacing between parts.

Usage: .venv/Scripts/python.exe -I check.py <run-dir> <out-dir> [<out-dir> ...]
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from shapely.geometry import Polygon
from svgelements import SVG, Path as SvgPath

RUN = Path(sys.argv[1])
SHEET = 304.8
BORDER = 6.0
SPACING = 2.0
TOL = 1e-3


def rings(d, step=0.2):
    """Each subpath of an SVG path as a list of points."""
    out, cur = [], []
    for seg in SvgPath(d).segments():
        name = seg.__class__.__name__
        if name == "Move":
            if cur:
                out.append(cur)
            cur = [(seg.end.x, seg.end.y)]
            continue
        if name == "Close":
            continue
        n = max(1, int(math.ceil(seg.length(error=1e-4) / step))) if name != "Line" else 1
        for i in range(1, n + 1):
            q = seg.point(i / n)
            cur.append((q.x, q.y))
    if cur:
        out.append(cur)
    return out


def shape(d):
    rs = sorted((Polygon(r) for r in rings(d)), key=lambda p: -p.area)
    outer, holes = rs[0], rs[1:]
    return Polygon(outer.exterior.coords, [h.exterior.coords for h in holes]), len(holes)


# Reference shapes from the drawing, by document order (ornaments-1 .. ornaments-6).
src = (RUN / "ornaments.svg").read_text(encoding="utf-8")
ref = {}
for i, (tr, d) in enumerate(re.findall(r'<g transform="translate\(([^)]*)\)">.*?d="([^"]+)"', src), start=1):
    poly, nh = shape(d)
    ref[f"ornaments-{i}"] = (poly.area, nh)

report = {}
ok_all = True
for out in sys.argv[2:]:
    od = RUN / out
    req = json.loads((od / "request.json").read_text(encoding="utf-8"))
    placed, problems = [], []
    for sheet_svg in sorted(od.glob("sheet-*.svg")):
        text = sheet_svg.read_text(encoding="utf-8")
        for pid, d in re.findall(r'<path id="([^"#]+)#\d+"[^>]*d="([^"]+)"', text):
            poly, nh = shape(d)
            placed.append((sheet_svg.name, pid, poly))
            a0, nh0 = ref[pid]
            if abs(poly.area - a0) > 0.002 * a0:
                problems.append(f"{pid} area {poly.area:.1f} vs {a0:.1f}")
            if nh != nh0:
                problems.append(f"{pid} holes {nh} vs {nh0}")
            minx, miny, maxx, maxy = poly.bounds
            if minx < BORDER - TOL or miny < BORDER - TOL or maxx > SHEET - BORDER + TOL or maxy > SHEET - BORDER + TOL:
                problems.append(f"{pid} on {sheet_svg.name} inside the 6 mm border: {poly.bounds}")
    counts = Counter(pid for _, pid, _ in placed)
    for part in req["parts"]:
        if counts[part["id"]] > part["quantity"]:
            problems.append(f"{part['id']}: {counts[part['id']]} placed > {part['quantity']} requested")
    if req.get("mode", "all") == "all":
        for part in req["parts"]:
            if counts[part["id"]] != part["quantity"]:
                problems.append(f"{part['id']}: {counts[part['id']]} placed, {part['quantity']} requested")
    gap = math.inf
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            if placed[i][0] != placed[j][0]:
                continue
            g = placed[i][2].exterior.distance(placed[j][2].exterior) if not placed[i][2].intersects(placed[j][2]) else 0.0
            gap = min(gap, g)
            if g < SPACING - TOL:
                problems.append(f"{placed[i][1]} and {placed[j][1]} {g:.3f} mm apart")
    sheets = sorted({s for s, _, _ in placed})
    report[out] = {"ok": not problems, "placed": len(placed), "sheets": len(sheets),
                   "per_part": dict(sorted(counts.items())), "min_gap_mm": round(gap, 3), "problems": problems[:20]}
    ok_all &= not problems
    print(out, "ok" if not problems else "PROBLEMS", len(placed), "on", len(sheets), "min gap", round(gap, 3))
print(json.dumps({"ok": ok_all, "runs": report}, indent=1))
