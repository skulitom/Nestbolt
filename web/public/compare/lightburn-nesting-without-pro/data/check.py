"""Independent check of nested LightBurn sheets against the input project (no Nestbolt code involved).

Usage: python check.py <input.lbrn2> <request.json> <sheet.lbrn2> [more sheets]  -> JSON on stdout

Reads the files with ElementTree and checks, for every group on every sheet:
  1. it is a copy of an input group (matched by its first child's VertID), with the same children in the same order:
     same CutIndex, same VertList and PrimList text (geometry stored unchanged); copies per design <= the request's
     quantity, and == it unless the request's mode is fill_area;
  2. all its vertices and Bezier handles, on every layer, moved by ONE rigid transform: a rotation of 0/90/180/270
     degrees plus a shift (no mirroring), to within 1e-6 mm;
  3. every input CutSetting is byte-identical on the sheet; anything added is reported;
  4. geometry (shapely, Beziers sampled at 24 steps): Fill engraving (as an area) and Line scores (as strokes) on
     their part's material, inside its outline and clear of its hole; parts at least spacing_mm apart; parts inside the stock (the request's rectangle less margins,
     or its outline_mm with holes) by at least edge_spacing_mm (sampled, within 0.01 mm).
"""
import json
import math
import re
import sys
import xml.etree.ElementTree as ET

from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union


def xform(node):
    x = node.find("XForm")
    return tuple(float(v) for v in x.text.split()) if x is not None else (1, 0, 0, 1, 0, 0)


def mul(a, b):  # a after b
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3],
            a[1] * b[2] + a[3] * b[3], a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


def ap(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


def verts(text):
    out = []
    for chunk in re.findall(r"V[^V]+", text):
        nums = re.match(r"V([-\d.e]+) ([-\d.e]+)", chunk)
        p = (float(nums.group(1)), float(nums.group(2)))
        h = dict(re.findall(r"(c[01][xy])([-\d.e]+)", chunk))
        c0 = (float(h["c0x"]), float(h["c0y"])) if "c0y" in h else None
        c1 = (float(h["c1x"]), float(h["c1y"])) if "c1y" in h else None
        out.append((p, c0, c1))
    return out


def prims(text):
    return [(k, int(a), int(b)) for k, a, b in re.findall(r"([LB])(\d+) (\d+)", text)]


def rings(vs, ps, m, steps=24):
    loops, cur, start = [], [], None
    for k, a, b in ps:
        if not cur:
            start = a
        pa, pb = vs[a][0], vs[b][0]
        if k == "L":
            cur.append(ap(m, pa))
        else:
            c1, c2 = vs[a][1], vs[b][2]
            for s in range(steps):
                t = s / steps
                u = 1 - t
                q = tuple(u ** 3 * pa[i] + 3 * u * u * t * c1[i] + 3 * u * t * t * c2[i] + t ** 3 * pb[i]
                          for i in (0, 1))
                cur.append(ap(m, q))
        if b == start:
            loops.append(cur)
            cur = []
    assert not cur, "open loop"
    return loops


def even_odd(loops):
    g = Polygon(loops[0])
    for r in loops[1:]:
        g = g.symmetric_difference(Polygon(r))
    return g


def read(path):
    root = ET.parse(path).getroot()
    settings = [ET.tostring(n, encoding="unicode").strip() for n in root if n.tag.startswith("CutSetting")]
    names, modes = {}, {}
    for n in root:
        if n.tag.startswith("CutSetting"):
            names[int(n.find("index").get("Value"))] = n.find("name").get("Value")
            modes[int(n.find("index").get("Value"))] = n.get("type")
    shapes = []
    for top in root.findall("Shape"):
        m = xform(top)
        if top.get("Type") == "Group":
            kids = []
            for ch in top.find("Children").findall("Shape"):
                mm = mul(m, xform(ch))
                vt, pt = ch.find("VertList").text, ch.find("PrimList").text
                vs = verts(vt)
                kids.append({"cut": int(ch.get("CutIndex")), "vid": ch.get("VertID"), "vtext": vt, "ptext": pt,
                             "points": [ap(mm, q) for v in vs for q in (v[0], v[1], v[2]) if q],
                             "rings": rings(vs, prims(pt), mm)})
            shapes.append({"type": "Group", "kids": kids})
        else:
            shapes.append({"type": top.get("Type"), "attrs": dict(top.attrib), "xform": m})
    return settings, names, modes, shapes


def rigid(src, dst):
    a0, b0 = src[0], dst[0]
    j = max(range(len(src)), key=lambda i: math.dist(src[i], a0))
    va = (src[j][0] - a0[0], src[j][1] - a0[1])
    vb = (dst[j][0] - b0[0], dst[j][1] - b0[1])
    ang = math.atan2(vb[1], vb[0]) - math.atan2(va[1], va[0])
    c, s = math.cos(ang), math.sin(ang)
    t = (b0[0] - (c * a0[0] - s * a0[1]), b0[1] - (s * a0[0] + c * a0[1]))
    res = max(math.dist((c * p[0] - s * p[1] + t[0], s * p[0] + c * p[1] + t[1]), q) for p, q in zip(src, dst))
    return math.degrees(ang) % 360, res


def main():
    inp, req_path, sheets = sys.argv[1], sys.argv[2], sys.argv[3:]
    req = json.load(open(req_path, encoding="utf-8"))
    spacing, edge = req["spacing_mm"], req.get("edge_spacing_mm", 0)
    sh = req["sheets"][0]
    W, H = sh["width_mm"], sh["height_mm"]
    mg = sh.get("margins_mm", {"left": 0, "right": 0, "bottom": 0, "top": 0})
    if sh.get("outline_mm"):
        stock = unary_union([Polygon(o["outer"], o.get("holes", [])) for o in sh["outline_mm"]])
    else:
        stock = box(0, 0, W, H)
    usable = stock.intersection(box(mg["left"], mg["bottom"], W - mg["right"], H - mg["top"])).buffer(-edge)
    fill = req.get("mode") == "fill_area"
    qty = [p["quantity"] for p in req["parts"]]
    in_settings, names, modes, in_shapes = read(inp)
    in_groups = [s for s in in_shapes if s["type"] == "Group"]
    assert len(in_groups) == len(in_shapes) == len(qty), "input must be groups only, one per request part"
    by_vid = {g["kids"][0]["vid"]: (n, g) for n, g in enumerate(in_groups)}
    seen = [0] * len(in_groups)
    problems, report = [], {"sheets": []}
    for si, sp in enumerate(sheets, 1):
        settings, _, _, shapes = read(sp)
        missing = [s for s in in_settings if s not in settings]
        added = [re.sub(r"\s+", " ", s)[:120] for s in settings if s not in in_settings]
        if missing:
            problems.append(f"sheet {si}: {len(missing)} input layer settings missing or changed")
        sheet = {"file": sp.replace("\\", "/").split("/")[-1], "copies": 0, "rotations": {},
                 "layer_shapes": {v: 0 for v in names.values()}, "layer_settings_identical": not missing,
                 "settings_added": added, "other_shapes": []}
        geoms = []
        for s in shapes:
            if s["type"] != "Group":
                sheet["other_shapes"].append({k: s["attrs"].get(k) for k in ("Type", "CutIndex", "W", "H")})
                continue
            vid = s["kids"][0]["vid"]
            if vid not in by_vid:
                problems.append(f"sheet {si}: a group not in the input")
                continue
            n, g = by_vid[vid]
            seen[n] += 1
            sheet["copies"] += 1
            if not (len(g["kids"]) == len(s["kids"]) and all(
                    a["cut"] == b["cut"] and a["vtext"] == b["vtext"] and a["ptext"] == b["ptext"]
                    for a, b in zip(g["kids"], s["kids"]))):
                problems.append(f"design {n + 1}: children differ from the input")
            ang, res = rigid([p for k in g["kids"] for p in k["points"]], [p for k in s["kids"] for p in k["points"]])
            quarter = min(abs(ang - q) for q in (0, 90, 180, 270, 360)) < 1e-6
            if res > 1e-6 or not quarter:
                problems.append(f"design {n + 1}: not one quarter-turn rigid move (angle {ang:.6f}, res {res:.2e})")
            r = str(round(ang) % 360)
            sheet["rotations"][r] = sheet["rotations"].get(r, 0) + 1
            for k in s["kids"]:
                sheet["layer_shapes"][names[k["cut"]]] += 1
            cut = even_odd(s["kids"][0]["rings"])
            for k in s["kids"][1:]:
                # Fill (Scan) art is an area; Line (Cut) art is its stroke: check what the laser marks
                art = even_odd(k["rings"]) if modes[k["cut"]] == "Scan" else unary_union(
                    [LineString(r + r[:1]) for r in k["rings"]])
                if not cut.buffer(1e-6).contains(art):
                    problems.append(f"design {n + 1}: {names[k['cut']]} not inside its cut part")
            outer = Polygon(max(s["kids"][0]["rings"], key=lambda q: abs(Polygon(q).area)))
            geoms.append(outer)
        gaps = [a.distance(b) for i, a in enumerate(geoms) for b in geoms[i + 1:]]
        min_gap = min(gaps) if gaps else None
        if min_gap is not None and min_gap < spacing - 0.01:
            problems.append(f"sheet {si}: parts {min_gap:.3f} mm apart, under {spacing}")
        outside = [i for i, gm in enumerate(geoms) if not usable.buffer(0.01).contains(gm)]
        if outside:
            problems.append(f"sheet {si}: {len(outside)} parts closer than {edge} mm to the stock edge or a hole")
        boundary = stock.boundary
        sheet["min_gap_mm"] = round(min_gap, 3) if min_gap is not None else None
        sheet["min_distance_to_stock_edge_or_hole_mm"] = round(min(boundary.distance(gm) for gm in geoms), 3)
        sheet["part_area_mm2"] = round(sum(gm.area for gm in geoms), 1)
        sheet["stock_area_mm2"] = round(stock.area, 1)
        report["sheets"].append(sheet)
    for n, q in enumerate(qty):
        if seen[n] > q or (not fill and seen[n] != q):
            problems.append(f"design {n + 1}: {seen[n]} copies for quantity {q}")
    report["copies_per_design"] = seen
    report["requested_per_design"] = qty
    report["input_layer_shapes"] = {v: sum(1 for g in in_groups for k in g["kids"] if names[k["cut"]] == v)
                                    for v in names.values()}
    report["problems"] = problems
    report["ok"] = not problems
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
