"""Smallest gap between the parts Nestbolt placed, from its layout.json and the library.json that `nestbolt import`
wrote. Measures the parts' outer outlines (a part placed inside another part's hole would need the holes too; these
examples place none there). Each placement rotates the library polygon about (0, 0), then translates it.

Usage: python gaps.py out/layout.json library.json      (needs Shapely: pip install shapely)
Made for Nestbolt's remnant nesting example, 2026-11-13. MIT licensed, like Nestbolt.
"""
import json
import math
import sys

from shapely import affinity
from shapely.geometry import Polygon

layout = json.load(open(sys.argv[1], encoding="utf-8"))
library = json.load(open(sys.argv[2], encoding="utf-8"))
parts = {p["id"]: p for p in library["parts"]}
placed = []
for placement in layout["placements"]:
    t = placement["transform"]
    if t.get("mirrored"):
        sys.exit("mirrored placement: not handled by this script")
    poly = Polygon(parts[placement["part_id"]]["polygon"]["outer"])
    poly = affinity.rotate(poly, t["rotation_radians"], origin=(0, 0), use_radians=True)
    poly = affinity.translate(poly, *t["translation"])
    placed.append((placement["part_id"], poly))

best = (math.inf, None, None)
for i in range(len(placed)):
    for j in range(i + 1, len(placed)):
        d = placed[i][1].distance(placed[j][1])
        if d < best[0]:
            best = (d, placed[i][0], placed[j][0])
print(f"{len(placed)} parts; smallest gap between parts {best[0]:.3f} mm ({best[1]} and {best[2]})")
