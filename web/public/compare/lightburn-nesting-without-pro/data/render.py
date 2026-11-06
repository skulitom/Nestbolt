"""SVG figures drawn from the .lbrn2 files themselves (and the request's stock), for the LightBurn page.

Usage: python render.py project <input.lbrn2> <out.svg>
       python render.py sheet <sheet.lbrn2> <request.json> <out.svg> [title]
Colours follow LightBurn's default layer palette: 00 black (CUT), 01 blue (ENGRAVE, filled), 02 red (SCORE).
The stock is drawn from the request: its outline_mm (with holes) or its rectangle; the dashed line is the margin.
"""
import json
import sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from check import read  # noqa: E402  (same folder; the reader only, no checks)

COL = {0: "#000000", 1: "#0000ff", 2: "#ff0000"}


def d_of(loops, fy):
    return " ".join("M " + " L ".join(f"{x:.2f} {fy(y):.2f}" for x, y in r) + " Z" for r in loops)


def shapes_svg(groups, fy):
    out = []
    for g in groups:
        for k in g["kids"]:
            c = k["cut"]
            if c == 1:
                out.append(f'<path d="{d_of(k["rings"], fy)}" fill="{COL[1]}" fill-rule="evenodd" stroke="none"/>')
            else:
                w = 0.5 if c == 0 else 0.35
                out.append(f'<path d="{d_of(k["rings"], fy)}" fill="none" stroke="{COL[c]}" stroke-width="{w}"/>')
    return out


def main():
    mode = sys.argv[1]
    if mode == "project":
        _, _, _, shapes = read(sys.argv[2])
        groups = [s for s in shapes if s["type"] == "Group"]
        xs = [p[0] for g in groups for k in g["kids"] for r in k["rings"] for p in r]
        ys = [p[1] for g in groups for k in g["kids"] for r in k["rings"] for p in r]
        x0, x1, y0, y1 = min(xs) - 6, max(xs) + 6, min(ys) - 6, max(ys) + 6
        fy = lambda y: y1 - y + y0  # Y up -> SVG Y down, same box
        body = shapes_svg(groups, fy)
        w, h = x1 - x0, y1 - y0
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" '
               f'width="{w * 2.4:.0f}" height="{h * 2.4:.0f}" role="img" aria-label="The six engraved ornament '
               f'designs as drawn in the LightBurn project">\n<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" '
               f'height="{h:.2f}" fill="#fff"/>\n' + "\n".join(body) + "\n</svg>\n")
        open(sys.argv[3], "w", encoding="utf-8", newline="\n").write(svg)
        return
    sheet, req_path, out = sys.argv[2], sys.argv[3], sys.argv[4]
    label = sys.argv[5] if len(sys.argv) > 5 else "A nested sheet"
    req = json.load(open(req_path, encoding="utf-8"))
    sh = req["sheets"][0]
    W, H = sh["width_mm"], sh["height_mm"]
    fy = lambda y: H - y
    pad = 4
    parts = []
    if sh.get("outline_mm"):
        o = sh["outline_mm"][0]
        loops = [o["outer"]] + o.get("holes", [])
        parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#999" stroke-width="0.4" '
                     f'stroke-dasharray="3 3"/>')
        parts.append(f'<path d="{d_of(loops, fy)}" fill="#f1e2c6" fill-rule="evenodd" stroke="#8a6d3b" '
                     f'stroke-width="0.6"/>')
    else:
        m = sh.get("margins_mm", {})
        parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f1e2c6" stroke="#8a6d3b" stroke-width="0.6"/>')
        parts.append(f'<rect x="{m.get("left", 0)}" y="{m.get("top", 0)}" width="{W - m.get("left", 0) - m.get("right", 0)}" '
                     f'height="{H - m.get("top", 0) - m.get("bottom", 0)}" fill="none" stroke="#8a6d3b" '
                     f'stroke-width="0.4" stroke-dasharray="3 3"/>')
    _, _, _, shapes = read(sheet)
    groups = [s for s in shapes if s["type"] == "Group"]
    parts += shapes_svg(groups, fy)
    vb = f"{-pad} {-pad} {W + 2 * pad} {H + 2 * pad}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{(W + 2 * pad) * 2:.0f}" '
           f'height="{(H + 2 * pad) * 2:.0f}" role="img" aria-label="{label}">\n'
           f'<rect x="{-pad}" y="{-pad}" width="{W + 2 * pad}" height="{H + 2 * pad}" fill="#fff"/>\n'
           + "\n".join(parts) + "\n</svg>\n")
    open(out, "w", encoding="utf-8", newline="\n").write(svg)


if __name__ == "__main__":
    main()
