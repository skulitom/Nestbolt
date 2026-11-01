"""Draw six original ornament outlines (mm) and write the Nestbolt inputs for the ornament page.

Usage: .venv/Scripts/python.exe -I gen.py <out-dir>
Writes ornaments.svg (one copy of each design), the per-design fill requests, the mixed request and grid.json
(the bounding-box grid baseline). Every shape is drawn here from numbers; nothing is traced or copied.
"""
import json
import math
import sys
from pathlib import Path

from shapely.affinity import rotate, translate
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

SHEET = 304.8          # 12 x 12 inches
MARGIN = 5.0
EDGE = 1.0
SPACING = 2.0


def circle_path(cx, cy, r):
    return (f"M {cx + r:.3f} {cy:.3f} A {r} {r} 0 1 0 {cx - r:.3f} {cy:.3f} "
            f"A {r} {r} 0 1 0 {cx + r:.3f} {cy:.3f} Z")


def poly_path(coords):
    pts = list(coords)
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    head = f"M {pts[0][0]:.3f} {pts[0][1]:.3f} "
    return head + " ".join(f"L {x:.3f} {y:.3f}" for x, y in pts[1:]) + " Z"


# Each design: name, outline path (local coords, y down, centred near 0,0), hanging hole (cx, cy, r).
designs = []

# 1. Round bauble with a rounded cap.
yc = 6 - math.sqrt(32 ** 2 - 8 ** 2)
designs.append(("bauble",
                f"M -8 {yc:.3f} L -8 -30 A 8 8 0 0 1 8 -30 L 8 {yc:.3f} A 32 32 0 1 1 -8 {yc:.3f} Z",
                (0, -31, 2.0)))

# 2. Five-point star.
star = []
for i in range(10):
    r = 38 if i % 2 == 0 else 16
    a = math.radians(-90 + 36 * i)
    star.append((r * math.cos(a), r * math.sin(a)))
designs.append(("star", poly_path(star), (0, -24, 1.75)))

# 3. Three-tier tree with a trunk.
tree = [(0, -38), (14, -18), (8, -18), (22, 4), (14, 4), (30, 26), (7, 26), (7, 38), (-7, 38), (-7, 26),
        (-30, 26), (-14, 4), (-22, 4), (-8, -18), (-14, -18)]
designs.append(("tree", poly_path(tree), (0, -27, 1.75)))

# 4. Bell with a hanging loop and a clapper.
lx = math.sqrt(36 - 16)
cx = math.sqrt(6.5 ** 2 - 5 ** 2)
bell = (f"M {-lx:.3f} -28 A 6 6 0 1 1 {lx:.3f} -28 L 9 -26 C 22 -24 22 6 30 22 L 32 26 L {cx:.3f} 26 "
        f"A 6.5 6.5 0 1 1 {-cx:.3f} 26 L -32 26 L -30 22 C -22 6 -22 -24 -9 -26 Z")
designs.append(("bell", bell, (0, -32, 2.2)))

# 5. Six-arm snowflake: bars, side branches and round tips, slightly rounded.
parts = []
for k in range(6):
    ang = -90 + 60 * k
    arm = box(-3, -31, 3, 0)
    tip = Point(0, -31).buffer(5, quad_segs=16)
    b1 = rotate(box(-2.5, -11, 2.5, 0), 50, origin=(0, 0))
    b1 = translate(b1, 0, -17)
    b2 = rotate(box(-2.5, -11, 2.5, 0), -50, origin=(0, 0))
    b2 = translate(b2, 0, -17)
    one = unary_union([arm, tip, b1, b2])
    parts.append(rotate(one, ang + 90, origin=(0, 0)))
parts.append(Point(0, 0).buffer(9, quad_segs=16))
flake = unary_union(parts).buffer(1.0, quad_segs=8).buffer(-1.0, quad_segs=8)
flake = flake.simplify(0.02)
assert flake.geom_type == "Polygon" and not flake.interiors
designs.append(("snowflake", poly_path(flake.exterior.coords), (0, -31, 1.5)))

# 6. Stocking with a cuff.
stock = ("M -20 -38 H 10 V -27 H 7 V 6 C 7 12 14 14 22 15 C 32 16 34 26 30 31 C 27 36 20 37 12 37 "
         "H -4 C -16 37 -21 28 -19 18 L -17 -27 H -20 Z")
designs.append(("stocking", stock, (-6.5, -32.5, 2.0)))

# Measure each outline with svgelements-free sampling: rebuild it with shapely for bounds and area.
from svgelements import Path as SvgPath  # noqa: E402


def to_poly(d, step=0.25):
    p = SvgPath(d)
    pts = []
    for seg in p.segments():
        if seg.__class__.__name__ == "Move":
            continue
        n = max(2, int(math.ceil(seg.length(error=1e-4) / step)))
        for i in range(n):
            q = seg.point(i / n)
            pts.append((q.x, q.y))
    return Polygon(pts).buffer(0)


meta = []
cell_w = 90
svg_parts = []
for i, (name, d, (hx, hy, hr)) in enumerate(designs):
    outline = to_poly(d)
    hole = Point(hx, hy).buffer(hr, quad_segs=32)
    assert outline.is_valid and outline.contains(hole.buffer(1.4)), name   # >= 1.4 mm wall round the hole
    minx, miny, maxx, maxy = outline.bounds
    w, h = maxx - minx, maxy - miny
    net = outline.area - hole.area
    ox = 10 + i * cell_w - minx + (cell_w - 10 - w) / 2
    oy = 10 - miny
    svg_parts.append(
        f'  <g transform="translate({ox:.3f} {oy:.3f})"><title>{name}</title>'
        f'<path fill="none" stroke="#000" stroke-width="0.2" fill-rule="evenodd" '
        f'd="{d} {circle_path(hx, hy, hr)}"/></g>')
    meta.append({"design": name, "width_mm": round(w, 2), "height_mm": round(h, 2),
                 "net_area_mm2": round(net, 1), "hole_diameter_mm": 2 * hr})

W = 10 + cell_w * len(designs)
H = 100
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n'
       f'  <title>Six ornament outlines, about 3 in (76 mm) tall, each with a hanging hole: bauble, star, tree, '
       f'bell, snowflake, stocking. Drawn for Nestbolt\'s ornament example; MIT licensed.</title>\n'
       + "\n".join(svg_parts) + "\n</svg>\n")
(OUT / "ornaments.svg").write_text(svg, encoding="utf-8", newline="\n")

rot = {"kind": "list", "degrees": [0, 90, 180, 270]}
sheet = {"width_mm": SHEET, "height_mm": SHEET,
         "margins_mm": {"left": MARGIN, "right": MARGIN, "bottom": MARGIN, "top": MARGIN}}
for i, m in enumerate(meta, start=1):
    req = {"name": f"As many {m['design']} ornaments as fit on one 12 x 12 in (304.8 mm) sheet",
           "parts": [{"id": f"ornaments-{i}", "quantity": 40, "rotations": rot}],
           "sheets": [dict(sheet, count=1)],
           "spacing_mm": SPACING, "edge_spacing_mm": EDGE, "mode": "fill_area"}
    (OUT / f"fill-{m['design']}-request.json").write_text(json.dumps(req, indent=2) + "\n", encoding="utf-8",
                                                           newline="\n")

for each in (3, 4):
    req = {"name": f"A mixed set: {each} of each of the six ornaments on 12 x 12 in (304.8 mm) sheets",
           "parts": [{"id": f"ornaments-{i}", "quantity": each, "rotations": rot} for i in range(1, len(meta) + 1)],
           "sheets": [sheet],
           "spacing_mm": SPACING, "edge_spacing_mm": EDGE}
    (OUT / f"mixed-{each * len(meta)}-request.json").write_text(json.dumps(req, indent=2) + "\n", encoding="utf-8",
                                                                 newline="\n")

# Grid baseline: equal rows and columns of each shape's bounding box, the better of 0 and 90 degrees.
usable = SHEET - 2 * (MARGIN + EDGE)
for m in meta:
    best = 0
    for w, h in ((m["width_mm"], m["height_mm"]), (m["height_mm"], m["width_mm"])):
        n = math.floor((usable + SPACING) / (w + SPACING)) * math.floor((usable + SPACING) / (h + SPACING))
        best = max(best, n)
    m["grid_count"] = best
(OUT / "grid.json").write_text(json.dumps({"sheet_mm": SHEET, "margin_mm": MARGIN, "edge_spacing_mm": EDGE,
                                            "spacing_mm": SPACING, "usable_span_mm": usable,
                                            "designs": meta}, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(meta, indent=1))
