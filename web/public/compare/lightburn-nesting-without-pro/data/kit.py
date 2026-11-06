"""Write an engraved-ornament LightBurn project and three nesting requests for the LightBurn page.

Usage: python kit.py <ornament library.json> <traced-offcut.svg> <out dir>

The cut outlines are the six ornament designs from Nestbolt's ornament example (its ornaments.svg, imported by the
Nestbolt release into library.json: lines, circular arcs and cubics in mm). Each design becomes one LightBurn group:
  CUT (layer 00, Line): the outline and its hanging hole in one Path, arcs written as cubic Beziers;
  ENGRAVE (layer 01, Fill): a five-point star at the part's most open interior point;
  SCORE (layer 02, Line): a ring 1.5 mm outside the hanging hole.
Requests: full 12 x 12 in sheet (all parts), the traced offcut from the scrap example (fill_area), and a partly used
12 x 12 in sheet with a cut-away corner and two holes (fill_area). Settings are placeholders, not machine advice.
"""
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from shapely.geometry import Point, Polygon
from shapely.ops import polylabel

lib_path, offcut_svg, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
lib = json.load(open(lib_path, encoding="utf-8"))
NAMES = ["bauble", "star", "tree", "bell", "snowflake", "stocking"]
assert len(lib["parts"]) == 6, len(lib["parts"])

CUT_SETTINGS = """    <CutSetting type="Cut">
        <index Value="0"/>
        <name Value="CUT"/>
        <maxPower Value="70"/>
        <maxPower2 Value="70"/>
        <speed Value="10"/>
        <priority Value="2"/>
    </CutSetting>
    <CutSetting type="Scan">
        <index Value="1"/>
        <name Value="ENGRAVE"/>
        <maxPower Value="25"/>
        <maxPower2 Value="25"/>
        <speed Value="200"/>
        <interval Value="0.1"/>
        <priority Value="0"/>
    </CutSetting>
    <CutSetting type="Cut">
        <index Value="2"/>
        <name Value="SCORE"/>
        <maxPower Value="15"/>
        <maxPower2 Value="15"/>
        <speed Value="100"/>
        <priority Value="1"/>
    </CutSetting>
"""


def arc_to_beziers(center, r, start, sweep):
    """Split a circular arc into cubic pieces of at most 90 degrees: [(p0, c1, c2, p1), ...]."""
    n = max(1, math.ceil(abs(sweep) / (math.pi / 2) - 1e-9))
    d = sweep / n
    k = 4 / 3 * math.tan(d / 4)
    out = []
    for i in range(n):
        a0, a1 = start + i * d, start + (i + 1) * d
        p0 = (center[0] + r * math.cos(a0), center[1] + r * math.sin(a0))
        p1 = (center[0] + r * math.cos(a1), center[1] + r * math.sin(a1))
        c1 = (p0[0] - k * r * math.sin(a0), p0[1] + k * r * math.cos(a0))
        c2 = (p1[0] + k * r * math.sin(a1), p1[1] - k * r * math.cos(a1))
        out.append((p0, c1, c2, p1))
    return out


def contour(segpath, shift):
    """Nestbolt library contour {start, segments} -> {'pts': [...], 'segs': [(kind, c1, c2)]}, shifted."""
    sx, sy = shift
    mv = lambda p: (p[0] + sx, p[1] + sy)
    pts, segs = [mv(segpath["start"])], []
    for s in segpath["segments"]:
        if s["kind"] == "line":
            segs.append(("L", None, None))
            pts.append(mv(s["to"]))
        elif s["kind"] == "arc":
            assert abs(s["radii"][0] - s["radii"][1]) < 1e-9 and s["rotation"] == 0
            for p0, c1, c2, p1 in arc_to_beziers(s["center"], s["radii"][0], s["start"], s["sweep"]):
                segs.append(("C", mv(c1), mv(c2)))
                pts.append(mv(p1))
        elif s["kind"] == "cubic":
            c1, c2 = s["controls"]
            segs.append(("C", mv(c1), mv(c2)))
            pts.append(mv(s["to"]))
        else:
            raise ValueError(s["kind"])
    assert math.dist(pts[-1], pts[0]) < 1e-6, (pts[0], pts[-1])
    pts.pop()
    return {"pts": pts, "segs": segs}


def circle(c, r):
    return {"pts": [p0 for p0, *_ in arc_to_beziers(c, r, 0, 2 * math.pi)],
            "segs": [("C", c1, c2) for _, c1, c2, _ in arc_to_beziers(c, r, 0, 2 * math.pi)]}


def star(c, r_out):
    r_in = r_out * 0.42
    pts = [(c[0] + (r_out if i % 2 == 0 else r_in) * math.cos(math.radians(90 + 36 * i)),
            c[1] + (r_out if i % 2 == 0 else r_in) * math.sin(math.radians(90 + 36 * i))) for i in range(10)]
    return {"pts": pts, "segs": [("L", None, None)] * 10}


def fnum(v):
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Ids:
    n = 0

    def next(self):
        self.n += 1
        return self.n - 1


def path_xml(contours, cut_index, ids, indent):
    verts, prims, base = [], [], 0
    for c in contours:
        n = len(c["pts"])
        o, inc = [None] * n, [None] * n
        for k, (kind, c1, c2) in enumerate(c["segs"]):
            if kind == "C":
                o[k] = c1
                inc[(k + 1) % n] = c2
        for k, p in enumerate(c["pts"]):
            s = f"V{fnum(p[0])} {fnum(p[1])}"
            s += f"c0x{fnum(o[k][0])}c0y{fnum(o[k][1])}" if o[k] else "c0x1"
            s += f"c1x{fnum(inc[k][0])}c1y{fnum(inc[k][1])}" if inc[k] else "c1x1"
            verts.append(s)
        for k, (kind, _, _) in enumerate(c["segs"]):
            prims.append(f"{'B' if kind == 'C' else 'L'}{base + k} {base + (k + 1) % n}")
        base += n
    sp = " " * indent
    return (f'{sp}<Shape Type="Path" CutIndex="{cut_index}" VertID="{ids.next()}" PrimID="{ids.next()}">\n'
            f"{sp}    <XForm>1 0 0 1 0 0</XForm>\n"
            f"{sp}    <VertList>{''.join(verts)}</VertList>\n"
            f"{sp}    <PrimList>{''.join(prims)}</PrimList>\n"
            f"{sp}</Shape>\n")


# Lay the six designs out in a row on the LightBurn workspace, as a user would have drawn them.
ids, body, summary, x_cursor = Ids(), [], [], 10.0
for name, part in zip(NAMES, lib["parts"]):
    x0, y0, x1, y1 = part["bounds_mm"]
    shift = (x_cursor - x0, 20.0 - y0)
    x_cursor += (x1 - x0) + 15.0
    outer = contour(part["outer"], shift)
    assert len(part["holes"]) == 1, name
    hole_seg = part["holes"][0]
    hole = contour(hole_seg, shift)
    arcs = [s for s in hole_seg["segments"] if s["kind"] == "arc"]
    hc = (arcs[0]["center"][0] + shift[0], arcs[0]["center"][1] + shift[1])
    hr = arcs[0]["radii"][0]
    poly = Polygon([(x + shift[0], y + shift[1]) for x, y in part["polygon"]["outer"]],
                   [[(x + shift[0], y + shift[1]) for x, y in h] for h in part["polygon"]["holes"]])
    ring_r = hr + 1.5
    assert Polygon(poly.exterior).contains(Point(hc).buffer(ring_r + 0.75)), f"{name}: no room for the score ring"
    room = poly.difference(Point(hc).buffer(ring_r + 2.0))
    room = max(getattr(room, "geoms", [room]), key=lambda g: g.area)
    pole = polylabel(room, tolerance=0.05)
    clear = room.exterior.distance(pole)
    for h in room.interiors:
        clear = min(clear, Polygon(h).exterior.distance(pole))
    r_star = round(min(9.0, 0.8 * clear), 3)
    assert r_star >= 2.5, f"{name}: star would be {r_star} mm"
    st = star((pole.x, pole.y), r_star)
    assert poly.buffer(-0.5).contains(Polygon(st["pts"])), name
    kids = (path_xml([outer, hole], 0, ids, 12) + path_xml([st], 1, ids, 12)
            + path_xml([circle(hc, ring_r)], 2, ids, 12))
    body.append(f'    <Shape Type="Group">\n        <XForm>1 0 0 1 0 0</XForm>\n'
                f"        <Children>\n{kids}        </Children>\n    </Shape>\n")
    summary.append({"design": name, "size_mm": [round(x1 - x0, 2), round(y1 - y0, 2)],
                    "area_mm2": round(part["area_mm2"], 1), "star_r_mm": r_star, "score_ring_r_mm": ring_r})

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<LightBurnProject FormatVersion="1" MirrorX="False" MirrorY="False">\n'
       + CUT_SETTINGS + "".join(body) + "</LightBurnProject>\n")
(out / "engraved-ornaments.lbrn2").write_text(xml, encoding="utf-8", newline="\n")


# --- stock -------------------------------------------------------------------------------------------------
def traced_outline(svg):
    root = ET.parse(svg).getroot()
    vb = [float(v) for v in root.get("viewBox").split()]
    d = next(el.get("d") for el in root.iter() if el.tag.endswith("path"))
    assert not re.search(r"[^MLZ0-9.\s-]", d), "traced outline must be M/L/Z only"
    loops = []
    for cmd, args in re.findall(r"([MLZ])([^MLZ]*)", d):
        nums = [float(v) for v in args.split()]
        if cmd == "M":
            loops.append([(nums[0], nums[1])])
            nums = nums[2:]
        for i in range(0, len(nums), 2):
            loops[-1].append((nums[i], nums[i + 1]))
    flip = [[[round(x, 4), round(vb[3] - y, 4)] for x, y in L] for L in loops]  # SVG Y down -> mm Y up
    return vb[2], vb[3], {"outer": flip[0], "holes": flip[1:]}


def ngon(cx, cy, r, n=72):
    return [[round(cx + r * math.cos(2 * math.pi * i / n), 4), round(cy + r * math.sin(2 * math.pi * i / n), 4)]
            for i in range(n)]


SHEET = 304.8
tw, th, traced = traced_outline(offcut_svg)
# Partly used 12 x 12 in sheet: an earlier job took a 150 x 120 mm top-right corner, a 70 mm disc and a
# 90 x 50 mm plate. Holes are clockwise, the outer anticlockwise (Y up).
partly = {"outer": [[0, 0], [SHEET, 0], [SHEET, SHEET - 120], [SHEET - 150, SHEET - 120], [SHEET - 150, SHEET],
                    [0, SHEET]],
          "holes": [ngon(80, 200, 35)[::-1], [[170, 60], [170, 110], [260, 110], [260, 60]]]}

rot = {"kind": "list", "degrees": [0, 90, 180, 270]}
part_ids = [f"engraved-ornaments-unit-{i}" for i in range(1, 7)]


def request(name, qty, sheet, spacing, edge, mode=None):
    r = {"name": name, "parts": [{"id": p, "quantity": qty, "rotations": rot} for p in part_ids],
         "sheets": [sheet], "spacing_mm": spacing, "edge_spacing_mm": edge}
    if mode:
        r["mode"] = mode
    return r


reqs = {
    "full-sheet-request.json": request("18 engraved ornaments (3 of each design) on a 12 x 12 in sheet", 3,
                                       {"width_mm": SHEET, "height_mm": SHEET,
                                        "margins_mm": {"left": 5, "right": 5, "bottom": 5, "top": 5}}, 2.0, 1.0),
    "traced-offcut-request.json": request("Engraved ornaments onto the traced plywood offcut: place what fits", 4,
                                          {"width_mm": tw, "height_mm": th, "outline_mm": [traced], "count": 1},
                                          2.0, 5.0, "fill_area"),
    "partly-used-request.json": request("Engraved ornaments onto a partly used 12 x 12 in sheet: place what fits",
                                        3, {"width_mm": SHEET, "height_mm": SHEET, "outline_mm": [partly],
                                            "count": 1}, 2.0, 2.0, "fill_area"),
}
for fn, r in reqs.items():
    (out / fn).write_text(json.dumps(r, indent=1) + "\n", encoding="utf-8", newline="\n")
stock = {"traced": Polygon(traced["outer"], traced["holes"]), "partly": Polygon(partly["outer"], partly["holes"])}
print(json.dumps({"designs": summary, "traced_offcut_mm": [tw, th, round(stock["traced"].area, 1)],
                  "partly_used_area_mm2": round(stock["partly"].area, 1)}, indent=1))
