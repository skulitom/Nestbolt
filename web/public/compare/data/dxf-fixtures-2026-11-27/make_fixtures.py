"""Draw the DXF fixtures (2026-11-27) with ezdxf, a DXF library that shares no code with Nestbolt.

Usage: python make_fixtures.py <out-dir>
Three plates, the same real size in every file:
  A  80 x 50 mm plate with a 20 mm round hole in the middle
  B  60 x 40 mm rectangle
  C  70 x 70 mm L bracket, arms 25 mm wide
Files:
  plates-mm.dxf              R2000 text DXF, $INSUNITS 4 (millimetres), drawn in mm
  plates-inch.dxf            R2000 text DXF, $INSUNITS 1 (inches), drawn in inches
  units/plates-insunits-NN.dxf  the same plates in each of the 21 $INSUNITS length units (01 inches ... 21 US survey feet)
  plates-r12-nounit.dxf      R12 text DXF, no $INSUNITS (R12 has none), drawn in inches
  plates-mm-binary.dxf       plates-mm.dxf saved as binary DXF (two-byte group codes)
  plates-r12-binary.dxf      plates-r12-nounit.dxf saved as binary DXF (R12's one-byte group codes)
  plates-hidden-layers.dxf   R2000 mm; A and B on layer CUT (frozen), C on layer PROFILE (off), a 200 x 120 frame on NOTES
"""
import sys
from pathlib import Path

import ezdxf

IN = 25.4
# millimetres per drawing unit for each $INSUNITS length code (Autodesk's table; 21 is the US survey foot, 1200/3937 m)
MM_PER_UNIT = {1: 25.4, 2: 304.8, 3: 1609344.0, 4: 1.0, 5: 10.0, 6: 1000.0, 7: 1e6, 8: 25.4e-6, 9: 0.0254, 10: 914.4,
               11: 1e-7, 12: 1e-6, 13: 1e-3, 14: 100.0, 15: 1e4, 16: 1e5, 17: 1e12, 18: 1.495978707e14,
               19: 9.4607304725808e18, 20: 3.0856775814913674e19, 21: 1200 / 3937 * 1000}
A_OUT = [(0, 0), (80, 0), (80, 50), (0, 50)]
A_HOLE = ((40, 25), 10)
B_OUT = [(0, 0), (60, 0), (60, 40), (0, 40)]
C_OUT = [(0, 0), (70, 0), (70, 25), (25, 25), (25, 70), (0, 70)]
OFFSETS = {"A": (0, 0), "B": (100, 0), "C": (180, 0)}


def shift(points, dx, dy, k=1.0):
    return [((x + dx) * k, (y + dy) * k) for x, y in points]


def plates(doc, k=1.0, layers=None, r12=False):
    msp = doc.modelspace()
    layers = layers or {"A": "CUT", "B": "CUT", "C": "CUT"}
    for lay in sorted(set(layers.values())):
        if lay not in doc.layers:
            doc.layers.add(lay)
    for name, pts in (("A", A_OUT), ("B", B_OUT), ("C", C_OUT)):
        dx, dy = OFFSETS[name]
        p = shift(pts, dx, dy, k)
        attr = {"layer": layers[name]}
        if r12:
            msp.add_polyline2d(p, close=True, dxfattribs=attr)
        else:
            msp.add_lwpolyline(p, close=True, dxfattribs=attr)
    (cx, cy), r = A_HOLE
    msp.add_circle(((cx + OFFSETS["A"][0]) * k, (cy + OFFSETS["A"][1]) * k), r * k,
                   dxfattribs={"layer": layers["A"]})


def main(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)

    mm = ezdxf.new("R2000")
    mm.header["$INSUNITS"] = 4
    plates(mm)
    mm.saveas(out / "plates-mm.dxf")
    mm.saveas(out / "plates-mm-binary.dxf", fmt="bin")

    inch = ezdxf.new("R2000")
    inch.header["$INSUNITS"] = 1
    plates(inch, k=1 / IN)
    inch.saveas(out / "plates-inch.dxf")

    # one file per $INSUNITS length unit, codes 1 to 21, the same plates each time
    (out / "units").mkdir(exist_ok=True)
    for code, per in MM_PER_UNIT.items():
        d = ezdxf.new("R2000")
        d.header["$INSUNITS"] = code
        plates(d, k=1 / per)
        d.saveas(out / "units" / f"plates-insunits-{code:02d}.dxf")

    r12 = ezdxf.new("R12")
    plates(r12, k=1 / IN, r12=True)
    r12.saveas(out / "plates-r12-nounit.dxf")
    r12.saveas(out / "plates-r12-binary.dxf", fmt="bin")

    hid = ezdxf.new("R2000")
    hid.header["$INSUNITS"] = 4
    plates(hid, layers={"A": "CUT", "B": "CUT", "C": "PROFILE"})
    hid.layers.add("NOTES")
    hid.modelspace().add_lwpolyline([(-10, -10), (190, -10), (190, 110), (-10, 110)], close=True,
                                    dxfattribs={"layer": "NOTES"})
    hid.layers.get("CUT").freeze()
    hid.layers.get("PROFILE").off()
    hid.saveas(out / "plates-hidden-layers.dxf")

    # text DXF files get LF line ends, the form git keeps them in; the two binary files are left alone
    for f in sorted(out.rglob("*.dxf")):
        raw = f.read_bytes()
        if b"\x00" not in raw:
            f.write_bytes(raw.replace(b"\r\n", b"\n"))
    for f in sorted(out.rglob("*.dxf")):
        print(f.relative_to(out).as_posix(), f.stat().st_size, "bytes")


if __name__ == "__main__":
    main(sys.argv[1])
