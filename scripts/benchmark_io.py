"""Strict file adapters between the frozen polygon contract and jagua-rs JSON.

No solver score or embedded source geometry is trusted. Output transforms refer
back to the original job, which is checked by the independent Rust validator.
"""
from collections import defaultdict
from copy import deepcopy
import math


class UnsupportedJob(ValueError):
    """The adapter cannot express all of this job's constraints faithfully."""


def jagua_input(job):
    if job["version"] != 1 or job["mode"] != "all":
        raise UnsupportedJob("LBF adapter currently supports version 1 all-parts jobs only")
    # Upstream's shared separation applies to part-part and part-boundary gaps.
    if job["clearance"] != job["edge_clearance"]:
        raise UnsupportedJob("LBF requires equal inter-part and edge clearance")
    items = []
    for index, part in enumerate(job["parts"]):
        if len(part["geometry"]) != 1 or part["geometry"][0]["holes"]:
            raise UnsupportedJob("LBF has no holed or disconnected items; refusing to fill holes silently")
        rotation = part["rotations"]
        if rotation["kind"] == "free":
            ext_rotation = {"mode": "continuous"}
        elif rotation["kind"] == "list":
            ext_rotation = {"mode": "discrete", "angles": deepcopy(rotation["degrees"])}
        elif rotation["kind"] == "step":
            # The benchmark permits a final partial interval; jagua stepped mode
            # requires an exact divisor of 360, so express the actual angle list.
            step = rotation["degrees"]
            if not math.isfinite(step) or step <= 0 or step > 360:
                raise ValueError("Invalid angle step")
            count = math.ceil(360 / step)
            if count > 65536:
                raise UnsupportedJob("Rotation step exceeds upstream's 65,536-angle limit")
            ext_rotation = {"mode": "discrete", "angles": [i * step for i in range(count)]}
        else:
            raise UnsupportedJob("Unknown rotation rule")
        items.append({"id": index, "demand": part["quantity"],
            "shape": {"type": "simple_polygon", "data": deepcopy(part["geometry"][0]["outer"])},
            "orientation": {"rotation": ext_rotation,
                            "reflection_axes": [90] if part["allow_mirror"] else []},
            "min_quality": None})
    bins = []
    total_copies = sum(p["quantity"] for p in job["parts"])
    for index, stock in enumerate(job["stocks"]):
        if stock["outline"]:
            raise UnsupportedJob("Remnant clipping with margins is not implemented in the LBF adapter yet")
        if any(d["holes"] for d in stock["defects"]):
            raise UnsupportedJob("LBF quality zones cannot contain holes")
        m = stock["margins"]
        bins.append({"id": index,
            # More than one sheet per copy cannot improve a complete packing.
            "stock": min(total_copies, stock["count"]) if stock["count"] is not None else total_copies,
            "cost": 1,
            "shape": {"type": "rectangle", "data": {"x_min": m["left"], "y_min": m["bottom"],
                "width": stock["width"] - m["left"] - m["right"],
                "height": stock["height"] - m["bottom"] - m["top"]}},
            "zones": [{"quality": 0, "shape": {"type": "simple_polygon", "data": deepcopy(d["outer"])}}
                for d in stock["defects"]]})
    return {"name": job["name"], "min_item_separation": job["clearance"], "items": items, "bins": bins}


def finite_number(value):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError("Solver transformation must contain finite numbers")
    return value


def jagua_layout(job, output):
    """Convert BPP output (degrees, mirror across X) to common radians/Y mirror."""
    result = {"version": 1, "units": job["units"], "sheets": [], "placements": []}
    copies = defaultdict(int)
    layouts = output["solution"]["layouts"]
    if len(layouts) > 2000:
        raise ValueError("Solver returned too many sheets")
    for index, sheet in enumerate(layouts):
        container = sheet["container_id"]
        if type(container) is not int or not 0 <= container < len(job["stocks"]):
            raise ValueError("Solver returned an unknown container ID")
        sheet_id = f"sheet-{index}"
        result["sheets"].append({"id": sheet_id, "stock_id": job["stocks"][container]["id"]})
        for placed in sheet["placed_items"]:
            if set(placed) != {"item_id", "transformation"}:
                raise ValueError("Unexpected fields in solver placement")
            item = placed["item_id"]
            if type(item) is not int or not 0 <= item < len(job["parts"]):
                raise ValueError("Solver returned an unknown item ID")
            transform = placed["transformation"]
            if set(transform) - {"rotation", "translation", "reflected"}:
                raise ValueError("Unexpected/non-rigid solver transformation field")
            degrees = finite_number(transform["rotation"])
            reflected = transform.get("reflected", False)
            if type(reflected) is not bool:
                raise ValueError("Solver reflection flag must be boolean")
            xy = transform["translation"]
            if len(xy) != 2:
                raise ValueError("Solver translation must contain two coordinates")
            xy = [finite_number(v) for v in xy]
            # R(a) * mirrorX == R(a - 180°) * mirrorY.
            radians = math.radians((degrees - (180 if reflected else 0)) % 360)
            result["placements"].append({"part_id": job["parts"][item]["id"],
                "copy_index": copies[item], "sheet_id": sheet_id,
                "transform": {"translation": xy, "rotation_radians": radians, "mirrored": reflected}})
            copies[item] += 1
            if len(result["placements"]) > 2000:
                raise ValueError("Solver returned too many placements")
    return result
