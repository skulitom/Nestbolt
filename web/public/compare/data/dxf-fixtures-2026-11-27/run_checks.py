"""Run Nestbolt's CLI on the DXF fixtures (2026-11-27) and check what comes back.

Usage: python run_checks.py <nestbolt executable> <fixtures dir> <out dir> [label for the build]

Nestbolt's own reports give the imported sizes. Every exported DXF is read back with ezdxf, which shares no code
with Nestbolt. Each claim also has a planted fault (a "mutant") that goes through the same check and must FAIL:
a check that cannot fail proves nothing. Writes <out>/RESULTS.txt, <out>/results.json and <out>/PLACEMENTS.tsv.
"""
import collections
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import ezdxf

NB = str(Path(sys.argv[1]).resolve())
FIX = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
LABEL = sys.argv[4] if len(sys.argv) > 4 else ""
IN = 25.4
PI = math.pi
# millimetres per drawing unit for each $INSUNITS length code (Autodesk's table; 21 is the US survey foot, 1200/3937 m)
MM_PER_UNIT = {1: 25.4, 2: 304.8, 3: 1609344.0, 4: 1.0, 5: 10.0, 6: 1000.0, 7: 1e6, 8: 25.4e-6, 9: 0.0254, 10: 914.4,
               11: 1e-7, 12: 1e-6, 13: 1e-3, 14: 100.0, 15: 1e4, 16: 1e5, 17: 1e12, 18: 1.495978707e14,
               19: 9.4607304725808e18, 20: 3.0856775814913674e19, 21: 1200 / 3937 * 1000}

# exact sizes of the drawn parts: (width, height, holes, area)
PLATES = [(80.0, 50.0, 1, 4000 - PI * 100), (60.0, 40.0, 0, 2400.0), (70.0, 70.0, 0, 2875.0)]
RESULTS = []


def nb(*args, timeout=120):
    p = subprocess.run([NB, *map(str, args)], capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def clean(text, n=260):
    """Local folders out, white space folded, then cut at a word: the text no longer depends on where the kit sits."""
    for full, short in ((str(OUT), "<out>"), (str(FIX), "<fixtures>"), (OUT.as_posix(), "<out>"), (FIX.as_posix(), "<fixtures>")):
        text = text.replace(full, short)
    text = " ".join(text.split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " ..."


def fmt(v):
    return f"{v:.6f}".rstrip("0").rstrip(".")


def record(test, claim, ok, detail, mutant=False):
    detail = clean(detail, 2000)
    RESULTS.append({"test": test, "claim": claim, "ok": bool(ok), "mutant": mutant, "detail": detail})
    tag = ("CAUGHT" if not ok else "MISSED") if mutant else ("PASS" if ok else "FAIL")
    print(f"{tag:6} {test}: {claim}\n       {detail}")


def do_import(src, name, *flags):
    lib = OUT / "libraries" / f"{name}.json"
    lib.parent.mkdir(parents=True, exist_ok=True)
    if lib.exists():
        lib.unlink()
    rc, out, err = nb("import", src, "--output", lib, *flags)
    rep = None
    if rc == 0:
        rep = json.loads(out)
        (OUT / "libraries" / f"{name}.report.json").write_text(out, encoding="utf-8", newline="\n")
    return rc, rep, err.strip(), lib


def sizes(rep):
    rows = []
    for p in rep["parts"]:
        x0, y0, x1, y1 = p["bounds_mm"]
        rows.append((x1 - x0, y1 - y0, p["holes"], p["area_mm2"]))
    return rows


def match_parts(rep, expected, scale=1.0, size_tol=1e-6, area_tol=0.5):
    """Imported parts equal the drawn ones (any order): width and height to 0.000001 mm, straight from the import
    report with no rounding; area to 0.5 mm2 (a round hole is a many-sided polygon there). Returns (ok, text)."""
    if rep is None:
        return False, "no library: the import failed"
    got = sizes(rep)
    shown = [(fmt(g[0]), fmt(g[1]), g[2], round(g[3], 2)) for g in got]
    left = list(got)
    for w, h, holes, area in expected:
        w, h, area = w * scale, h * scale, area * scale * scale
        hit = [g for g in left if abs(g[0] - w) <= size_tol and abs(g[1] - h) <= size_tol and g[2] == holes
               and abs(g[3] - area) <= area_tol]
        if not hit:
            return False, f"expected {fmt(w)} x {fmt(h)} mm, {holes} hole(s), {area:.2f} mm2; got {shown}"
        left.remove(hit[0])
    if left:
        return False, f"extra parts; got {shown}"
    return True, "; ".join(f"{fmt(g[0])} x {fmt(g[1])} mm, {g[2]} hole(s), {g[3]:.2f} mm2" for g in got)


def nearest_id(rep, area):
    """The library id of the part whose area is nearest (ids come from the source file's name)."""
    return min(rep["parts"], key=lambda p: abs(p["area_mm2"] - area))["id"]


def units(rep):
    u = rep["imports"][0]["report"]["units"]
    return u["declared"], u["mm_per_unit"], u["possible_inches"]


def geometry(lib):
    d = json.loads(Path(lib).read_text(encoding="utf-8"))
    return [(p["outer"], p["holes"]) for p in d["parts"]]


# ---------- reading exported DXF with ezdxf ----------
def rnd(v, n=4):
    return tuple(round(float(x), n) for x in v)


def arc_ends(e):
    c, r = e.dxf.center, e.dxf.radius
    a0, a1 = math.radians(e.dxf.start_angle), math.radians(e.dxf.end_angle)
    return (c.x + r * math.cos(a0), c.y + r * math.sin(a0)), (c.x + r * math.cos(a1), c.y + r * math.sin(a1))


def sweep(e):
    s = (e.dxf.end_angle - e.dxf.start_angle) % 360.0
    return 360.0 if s == 0 else s


def signature(e):
    t = e.dxftype()
    if t == "LINE":
        return t, frozenset((rnd(e.dxf.start)[:2], rnd(e.dxf.end)[:2]))
    if t == "ARC":
        return t, rnd(e.dxf.center)[:2], round(e.dxf.radius, 4), round(e.dxf.start_angle % 360, 3), round(e.dxf.end_angle % 360, 3)
    if t == "CIRCLE":
        return t, rnd(e.dxf.center)[:2], round(e.dxf.radius, 4)
    if t == "LWPOLYLINE":
        return t, bool(e.closed), frozenset(rnd(p) for p in e.get_points("xy"))
    return t, str(e.dxf.handle)


def read_cut(path):
    doc = ezdxf.readfile(path)
    ents = list(doc.modelspace())
    other = collections.Counter(e.dxf.layer for e in ents if e.dxf.layer != "CUT")
    return doc, [e for e in ents if e.dxf.layer == "CUT"], other


def duplicates(ents):
    c = collections.Counter(signature(e) for e in ents)
    return [k for k, n in c.items() if n > 1]


def shoelace(pts):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))) / 2


def loops(ents, tol=0.01):
    """Chain LINE and ARC entities into closed loops; return (areas, open chains, bounding boxes, outlines)."""
    segs = []
    for e in ents:
        if e.dxftype() == "LINE":
            a, b = rnd(e.dxf.start, 6)[:2], rnd(e.dxf.end, 6)[:2]
            segs.append((a, b, [a, b]))
        elif e.dxftype() == "ARC":
            a, b = arc_ends(e)
            c, r, a0, sw = e.dxf.center, e.dxf.radius, math.radians(e.dxf.start_angle), math.radians(sweep(e))
            n = max(8, int(sw / math.radians(0.5)))
            pts = [(c.x + r * math.cos(a0 + sw * i / n), c.y + r * math.sin(a0 + sw * i / n)) for i in range(n + 1)]
            segs.append((a, b, pts))
    near = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1]) <= tol
    areas, boxes, polys, unused, open_chains = [], [], [], list(range(len(segs))), 0
    while unused:
        i = unused.pop(0)
        start, end, pts = segs[i][0], segs[i][1], list(segs[i][2])
        closed = False
        while True:
            if near(end, start) and len(pts) > 2:
                closed = True
                break
            nxt = None
            for j in unused:
                a, b, p = segs[j]
                if near(a, end):
                    nxt, add, new_end = j, p[1:], b
                    break
                if near(b, end):
                    nxt, add, new_end = j, p[::-1][1:], a
                    break
            if nxt is None:
                break
            unused.remove(nxt)
            pts += add
            end = new_end
        if closed:
            areas.append(shoelace(pts))
            boxes.append((min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts)))
            polys.append(pts)
        else:
            open_chains += 1
    return areas, open_chains, boxes, polys


def seg_gap(a, b, c, d):
    """Smallest distance between segments ab and cd (0 when they cross)."""
    def side(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])

    def to_seg(p, u, v):
        dx, dy = v[0] - u[0], v[1] - u[1]
        ln = dx * dx + dy * dy
        t = 0.0 if ln == 0 else max(0.0, min(1.0, ((p[0] - u[0]) * dx + (p[1] - u[1]) * dy) / ln))
        return math.hypot(p[0] - (u[0] + t * dx), p[1] - (u[1] + t * dy))

    if (side(c, d, a) > 0) != (side(c, d, b) > 0) and (side(a, b, c) > 0) != (side(a, b, d) > 0):
        return 0.0
    return min(to_seg(a, c, d), to_seg(b, c, d), to_seg(c, a, b), to_seg(d, a, b))


def inside(p, poly):
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > p[1]) != (y1 > p[1]) and p[0] < x0 + (p[1] - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def outline_gap(p, q):
    """Smallest gap between two closed outlines; 0 when they cross or one lies in the other."""
    if inside(p[0], q) or inside(q[0], p):
        return 0.0
    return min(seg_gap(a, b, c, d) for a, b in zip(p, p[1:]) for c, d in zip(q, q[1:]))


def plates_on_sheets(paths, bounds, placements=None, spacing=2.0):
    """Read exported sheets with ezdxf. Count the plates by the area of each closed outline; every 20 mm hole must
    sit at the middle of exactly one 80 x 50 plate; nothing may leave the margins; and no two plates may be closer
    than the spacing asked for (our own segment-to-segment distances, not Nestbolt's validator).
    Returns (counts, problems, smallest gap per sheet)."""
    counts, problems, gaps = collections.Counter(), [], {}
    x0, y0, x1, y1 = bounds
    for p in paths:
        name = Path(p).name
        _, ents, other = read_cut(p)
        if other:
            problems.append(f"{name}: entities on other layers {dict(other)}")
        if duplicates(ents):
            problems.append(f"{name}: doubled entities")
        kinds = collections.Counter(e.dxftype() for e in ents)
        if set(kinds) - {"LINE", "CIRCLE"}:
            problems.append(f"{name}: unexpected entity types {dict(kinds)}")
        lines = [e for e in ents if e.dxftype() == "LINE"]
        zero = [e for e in lines if math.hypot(e.dxf.end.x - e.dxf.start.x, e.dxf.end.y - e.dxf.start.y) < 1e-9]
        if zero:
            problems.append(f"{name}: {len(zero)} zero-length LINE entities")
        areas, open_chains, boxes, polys = loops([e for e in lines if e not in zero])
        if open_chains:
            problems.append(f"{name}: {open_chains} outline(s) do not close")
        found = []
        for a, bx in zip(areas, boxes):
            kind = next((k for k, v in (("A", 4000.0), ("B", 2400.0), ("C", 2875.0)) if abs(a - v) <= 0.01), f"?{a:.2f}")
            found.append((kind, bx))
        holes = []
        for e in ents:
            if e.dxftype() == "CIRCLE":
                c, r = e.dxf.center, e.dxf.radius
                ok_r = abs(r - 10) < 1e-6
                found.append(("A-hole" if ok_r else f"?circle r={r:.4f}", (c.x - r, c.y - r, c.x + r, c.y + r)))
                if ok_r:
                    holes.append((c.x, c.y))
        a_mids = [((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2) for kind, bx in found if kind == "A"]
        for mid in a_mids:
            n = sum(1 for h in holes if math.hypot(h[0] - mid[0], h[1] - mid[1]) <= 0.001)
            if n != 1:
                problems.append(f"{name}: the 80 x 50 plate centred at ({mid[0]:.3f}, {mid[1]:.3f}) has {n} holes at its middle")
        for h in holes:
            if not any(math.hypot(h[0] - mid[0], h[1] - mid[1]) <= 0.001 for mid in a_mids):
                problems.append(f"{name}: a hole at ({h[0]:.3f}, {h[1]:.3f}) is not at the middle of any 80 x 50 plate")
        gap = min((outline_gap(p1, p2) for i, p1 in enumerate(polys) for p2 in polys[i + 1:]), default=None)
        gaps[name] = gap
        if gap is not None and gap < spacing - 1e-6:
            problems.append(f"{name}: two plates are {gap:.3f} mm apart, closer than the {spacing:g} mm asked for")
        for kind, bx in found:
            counts[kind] += 1
            if bx[0] < x0 - 1e-3 or bx[1] < y0 - 1e-3 or bx[2] > x1 + 1e-3 or bx[3] > y1 + 1e-3:
                problems.append(f"{name}: {kind} outside the margins at {tuple(round(v, 3) for v in bx)}")
            if placements is not None and kind in ("A", "B", "C"):
                placements.append((name, kind, round(bx[0], 3), round(bx[1], 3), round(bx[2] - bx[0], 3), round(bx[3] - bx[1], 3)))
    return counts, problems, gaps


def nest(lib, request, name, seconds=20):
    run = OUT / "runs" / name
    if run.exists():
        shutil.rmtree(run)
    run.parent.mkdir(parents=True, exist_ok=True)
    rc, out, err = nb("nest", "--library", lib, "--request", request, "--out-dir", run, "--seconds", seconds,
                      "--seed", 1, "--repeatable", timeout=180)
    rep = json.loads((run / "report.json").read_text(encoding="utf-8")) if (run / "report.json").exists() else None
    return rc, rep, run


def summarise(ver, name="RESULTS.txt", js="results.json"):
    real = [r for r in RESULTS if not r["mutant"]]
    muts = [r for r in RESULTS if r["mutant"]]
    passed, caught = sum(r["ok"] for r in real), sum(not r["ok"] for r in muts)
    lines = [f"Nestbolt DXF fixture run: {ver.strip()}" + (f" ({LABEL})" if LABEL else ""),
             f"Python {sys.version.split()[0]}, ezdxf {ezdxf.__version__}",
             f"{passed} of {len(real)} checks pass; {caught} of {len(muts)} planted faults caught", ""]
    for r in RESULTS:
        tag = ("CAUGHT" if not r["ok"] else "MISSED") if r["mutant"] else ("PASS" if r["ok"] else "FAIL")
        lines += [f"{tag:6} {r['test']}  {r['claim']}", f"         {r['detail']}"]
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    (OUT / js).write_text(json.dumps(RESULTS, indent=1), encoding="utf-8", newline="\n")
    print(f"\n{passed} of {len(real)} checks pass; {caught} of {len(muts)} planted faults caught")
    return 0 if passed == len(real) and caught == len(muts) else 1


def main():
    for d in ("libraries", "runs", "mutants", "requests"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    rc, ver, _ = nb("--version")
    print("nestbolt:", ver.strip())

    # ---- units ----
    rc, mm, err, lib_mm = do_import(FIX / "plates-mm.dxf", "mm")
    ok, text = match_parts(mm, PLATES)
    record("U1", "a DXF marked millimetres ($INSUNITS 4) imports at its drawn size",
           ok and units(mm)[:2] == (True, 1.0), f"{text}; units report declared, mm per unit = {units(mm)[:2]}")

    rc, inch, err, lib_in = do_import(FIX / "plates-inch.dxf", "inch")
    ok, text = match_parts(inch, PLATES)
    record("U2", "the same plates drawn in inches ($INSUNITS 1) import at the same millimetre size",
           ok and units(inch)[:2] == (True, 25.4), f"{text}; declared, mm per unit = {units(inch)[:2]}")

    rc, r12, err, _ = do_import(FIX / "plates-r12-nounit.dxf", "r12-nounit")
    ok, text = match_parts(r12, PLATES, scale=1 / IN)
    decl, mpu, maybe_in = units(r12)
    warn = " | ".join(r12.get("warnings", []))
    record("U3", "an R12 DXF with no units is not rescaled silently: 1 mm per unit, and the report flags possible inches",
           ok and (decl, mpu, maybe_in) == (False, 1.0, True) and "inch" in warn.lower(),
           f"{text}; declared {decl}, mm per unit {mpu}, possible_inches {maybe_in}; warning: {clean(warn, 300)}")

    rc, r12f, err, lib_r12f = do_import(FIX / "plates-r12-nounit.dxf", "r12-nounit-25.4", "--dxf-unit-mm", "25.4")
    ok, text = match_parts(r12f, PLATES)
    record("U4", "the same R12 file with --dxf-unit-mm 25.4 imports at the drawn size",
           ok and units(r12f)[:2] == (False, 25.4), f"{text}; declared, mm per unit = {units(r12f)[:2]}")

    rc, inch10, err, _ = do_import(FIX / "plates-inch.dxf", "inch-fallback-10", "--dxf-unit-mm", "10")
    ok, text = match_parts(inch10, PLATES)
    record("U5", "units declared in the file win over --dxf-unit-mm (inch file, fallback 10)",
           ok and units(inch10)[:2] == (True, 25.4), f"{text}; declared, mm per unit = {units(inch10)[:2]}")

    good, bad = [], []
    for code, per in MM_PER_UNIT.items():
        rc, other, err, _ = do_import(FIX / "units" / f"plates-insunits-{code:02d}.dxf", f"insunits-{code:02d}")
        ok, text = match_parts(other, PLATES)
        if ok and other and units(other)[0] is True and abs(units(other)[1] - per) <= per * 1e-12:
            good.append(code)
        else:
            bad.append(f"{code}: {clean(err.splitlines()[-1] if err else text, 60)}")
    record("U6", "the same plates in each $INSUNITS length code from 1 to 21 import at the same millimetre size",
           not bad, f"{len(good)} of 21 codes import at the drawn size (codes {good}); not imported: {bad or 'none'}")

    # ---- binary DXF ----
    rc, bn, err, lib_bn = do_import(FIX / "plates-mm-binary.dxf", "mm-binary")
    ok, text = match_parts(bn, PLATES)
    same = bn is not None and geometry(lib_bn) == geometry(lib_mm)
    record("B1", "a binary DXF (two-byte group codes) imports the same parts as its text twin",
           ok and same, f"{text}; curves equal to the text file's: {same}")

    rc, bn12, err, lib_bn12 = do_import(FIX / "plates-r12-binary.dxf", "r12-binary-25.4", "--dxf-unit-mm", "25.4")
    ok, text = match_parts(bn12, PLATES)
    same = bn12 is not None and geometry(lib_bn12) == geometry(lib_r12f)
    record("B2", "an R12 binary DXF (one-byte group codes) imports the same parts as its text twin",
           ok and same, f"{text}; curves equal to the text file's: {same}" + (f"; error: {clean(err)}" if rc else ""))

    # ---- hidden layers ----
    rc, hid, err, _ = do_import(FIX / "plates-hidden-layers.dxf", "hidden-layers", "--layers", "CUT,PROFILE")
    ok, text = match_parts(hid, PLATES)
    record("L1", "chosen layers are read when frozen (CUT) or off (PROFILE); the NOTES frame stays out",
           ok, text + (f"; error: {clean(err)}" if rc else ""))

    rc, hid0, err, _ = do_import(FIX / "plates-hidden-layers.dxf", "hidden-layers-auto")
    got0 = sizes(hid0) if hid0 else []
    mode = hid0["imports"][0]["report"]["selection_mode"] if hid0 else "-"
    only_frame = len(got0) == 1 and abs(got0[0][0] - 200) < 0.02 and abs(got0[0][1] - 120) < 0.02
    warn0 = " | ".join(hid0.get("warnings", [])) if hid0 else err
    record("L2", "with no --layers, hidden layers stay out: only the visible NOTES frame is imported (a limit, stated as one)",
           only_frame, f"parts {[(fmt(g[0]), fmt(g[1]), g[2]) for g in got0]}; selection mode {mode}; warnings: {clean(warn0, 320) or 'none'}")

    # ---- quantities over three sheets ----
    plate_id = {k: nearest_id(mm, a) for k, a in (("A", PLATES[0][3]), ("B", PLATES[1][3]), ("C", PLATES[2][3]))}
    req = OUT / "requests" / "quantity.json"
    req.write_text(json.dumps({
        "name": "Quantity job: 12 + 16 + 10 plates",
        "parts": [{"id": plate_id["A"], "quantity": 12}, {"id": plate_id["B"], "quantity": 16}, {"id": plate_id["C"], "quantity": 10}],
        "sheets": [{"width_mm": 300, "height_mm": 200, "margins_mm": {"left": 5, "right": 5, "bottom": 5, "top": 5}}],
        "spacing_mm": 2.0, "edge_spacing_mm": 0.0}, indent=2), encoding="utf-8", newline="\n")
    rc, rep, run = nest(lib_mm, req, "quantity")
    m = rep["validation"]["metrics"] if rep else {}
    vrc, vout, verr = nb("validate", "--library", lib_mm, "--request", req, "--layout", run / "layout.json")
    valid = vrc == 0 and json.loads(vout)["valid"]
    vnote = "" if vrc == 0 else f" (it exited {vrc}: {verr.strip().splitlines()[0][:120] if verr.strip() else 'no message'})"
    sheets = sorted(run.glob("sheet-*.dxf"))
    placements = []
    counts, problems, gaps = plates_on_sheets(sheets, (5, 5, 295, 195), placements)
    want = {"A": 12, "B": 16, "C": 10, "A-hole": 12}
    record("Q1", "12 + 16 + 10 plates on 300 x 200 mm sheets: every part placed, three sheets, a valid layout",
           rc == 0 and rep and rep["validation"]["valid"] and valid and m.get("placed_parts") == 38
           and m.get("requested_parts") == 38 and m.get("sheets_used") == 3 and len(sheets) == 3,
           f"report: placed {m.get('placed_parts')} of {m.get('requested_parts')}, sheets {m.get('sheets_used')}, "
           f"valid {rep['validation']['valid'] if rep else None}; `nestbolt validate`: valid {valid}{vnote}; "
           f"material {m.get('normalized_material', 0):.3f} sheets")
    record("Q2", "the three exported DXF sheets, read with ezdxf, hold exactly the requested plates: holes in place, inside the margins, 2 mm apart",
           dict(counts) == want and not problems,
           f"counted {dict(counts)} (wanted {want}); smallest gap between plates per sheet (mm): "
           f"{ {k: round(v, 3) for k, v in gaps.items() if v is not None} }; problems: {problems or 'none'}")
    with open(OUT / "PLACEMENTS.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("sheet\tplate\tx_mm\ty_mm\twidth_mm\theight_mm\n")
        for row in placements:
            f.write("\t".join(map(str, row)) + "\n")

    # ---- planted faults: each must be CAUGHT by the same check ----
    mut = OUT / "mutants"
    d = ezdxf.readfile(FIX / "plates-inch.dxf")
    d.header["$INSUNITS"] = 4
    d.saveas(mut / "inch-drawing-marked-mm.dxf")
    rc, r, err, _ = do_import(mut / "inch-drawing-marked-mm.dxf", "mutant-units")
    ok, text = match_parts(r, PLATES)
    record("M1", "units: an inch drawing whose header says millimetres must not pass the size check", ok, text, mutant=True)

    raw = (FIX / "plates-mm-binary.dxf").read_bytes()
    (mut / "truncated-binary.dxf").write_bytes(raw[: len(raw) * 6 // 10])
    rc, r, err, _ = do_import(mut / "truncated-binary.dxf", "mutant-binary")
    ok, text = match_parts(r, PLATES)
    record("M2", "binary: a truncated binary DXF must not pass", ok, f"{text}; exit {rc}; message: {clean(err)}", mutant=True)

    rc, r, err, _ = do_import(FIX / "plates-hidden-layers.dxf", "mutant-layers", "--layers", "NOTES")
    ok, text = match_parts(r, PLATES)
    record("M3", "layers: choosing only the NOTES layer must not pass", ok, f"{text}" + (f"; exit {rc}: {clean(err, 200)}" if rc else ""), mutant=True)

    d = ezdxf.readfile(sheets[1])
    for victim in [e for e in d.modelspace() if e.dxftype() == "LINE"][:4]:
        d.modelspace().delete_entity(victim)
    d.saveas(mut / "quantity-sheet-1-one-outline-deleted.dxf")
    counts, problems, _ = plates_on_sheets([sheets[0], mut / "quantity-sheet-1-one-outline-deleted.dxf", sheets[2]], (5, 5, 295, 195))
    record("M4", "quantities: a sheet with the first four lines of one plate deleted must not pass the count",
           dict(counts) == want and not problems, f"counted {dict(counts)} (wanted {want}); problems: {problems or 'none'}", mutant=True)

    d = ezdxf.readfile(FIX / "units" / "plates-insunits-21.dxf")
    d.header["$INSUNITS"] = 2
    d.saveas(mut / "survey-foot-drawing-marked-feet.dxf")
    rc, r, err, _ = do_import(mut / "survey-foot-drawing-marked-feet.dxf", "mutant-survey-foot")
    ok, text = match_parts(r, PLATES)
    record("M5", "units: a US-survey-foot drawing whose header says feet (2 parts in a million apart) must not pass the size check",
           ok, text, mutant=True)

    d = ezdxf.readfile(sheets[0])
    hole = next(e for e in d.modelspace() if e.dxftype() == "CIRCLE")
    hole.dxf.center = (hole.dxf.center.x + 30, hole.dxf.center.y, 0)
    d.saveas(mut / "quantity-sheet-0-one-hole-moved.dxf")
    counts, problems, _ = plates_on_sheets([mut / "quantity-sheet-0-one-hole-moved.dxf"], (5, 5, 295, 195))
    record("M6", "holes: a sheet with one hole moved 30 mm off its plate must not pass",
           not any("holes at its middle" in q or "is not at the middle" in q for q in problems),
           f"problems: {problems or 'none'}", mutant=True)

    d = ezdxf.readfile(sheets[0])
    _, cut, _ = read_cut(sheets[0])
    _, _, boxes, polys = loops([e for e in cut if e.dxftype() == "LINE"])
    areas = [shoelace(q) for q in polys]
    movers = [i for i, a in enumerate(areas) if abs(a - 2400.0) <= 0.01]      # a 60 x 40 plate: no hole to leave behind
    i, j = movers[0], next(k for k in range(len(boxes)) if k != movers[0])
    dx, dy = boxes[j][0] - boxes[i][0] + 3, boxes[j][1] - boxes[i][1] + 3
    bx = boxes[i]
    for e in d.modelspace():
        if e.dxftype() == "LINE" and all(bx[0] - 1e-6 <= q.x <= bx[2] + 1e-6 and bx[1] - 1e-6 <= q.y <= bx[3] + 1e-6 for q in (e.dxf.start, e.dxf.end)):
            e.dxf.start = (e.dxf.start.x + dx, e.dxf.start.y + dy, 0)
            e.dxf.end = (e.dxf.end.x + dx, e.dxf.end.y + dy, 0)
    d.saveas(mut / "quantity-sheet-0-one-plate-moved-onto-another.dxf")
    counts, problems, mgaps = plates_on_sheets([mut / "quantity-sheet-0-one-plate-moved-onto-another.dxf"], (5, 5, 295, 195))
    record("M7", "spacing: a sheet with one plate moved onto another must not pass our own spacing check",
           not any("apart" in q for q in problems), f"problems: {[q for q in problems if 'apart' in q] or 'none'}", mutant=True)

    return summarise(ver)


if __name__ == "__main__":
    sys.exit(main())
