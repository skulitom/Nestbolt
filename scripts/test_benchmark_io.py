"""Verify source preservation, mirror conventions and fail-closed benchmark IO."""
from copy import deepcopy
import math
import unittest

from benchmark_io import UnsupportedJob, jagua_input, jagua_layout


def job():
    return {"version": 1, "name": "adapter-fixture", "units": "inch", "mode": "all",
        "clearance": .1, "edge_clearance": .1,
        "parts": [{"id": "plate", "quantity": 3, "geometry": [{"outer": [[0, 0], [2, 0], [0, 1]], "holes": []}],
            "rotations": {"kind": "list", "degrees": [0, 180]}, "allow_mirror": True, "priority": 1}],
        "stocks": [{"id": "large", "width": 20, "height": 10, "count": None, "outline": [], "defects": [],
            "margins": {"left": 1, "right": 2, "bottom": 3, "top": 1}}]}


def output(rotation=0, reflected=False):
    return {"solution": {"layouts": [{"container_id": 0, "placed_items": [
        {"item_id": 0, "transformation": {"rotation": rotation, "reflected": reflected, "translation": [4, 5]}}
    ]}]}}


class AdapterTests(unittest.TestCase):
    def test_input_preserves_geometry_gap_units_stock_margins_and_orientation(self):
        original = job()
        converted = jagua_input(original)
        self.assertEqual(converted["items"][0]["shape"]["data"], original["parts"][0]["geometry"][0]["outer"])
        self.assertEqual(converted["items"][0]["demand"], 3)
        self.assertEqual(converted["min_item_separation"], .1)
        self.assertEqual(converted["items"][0]["orientation"], {
            "rotation": {"mode": "discrete", "angles": [0, 180]}, "reflection_axes": [90]})
        self.assertEqual(converted["bins"][0]["shape"]["data"], {"x_min": 1, "y_min": 3, "width": 17, "height": 6})
        self.assertEqual(converted["bins"][0]["stock"], 3)
        original["stocks"][0]["count"] = 1
        self.assertEqual(jagua_input(original)["bins"][0]["stock"], 1)
        original["stocks"][0]["defects"] = [{"outer": [[2, 4], [4, 4], [2, 5]], "holes": []}]
        self.assertEqual(jagua_input(original)["bins"][0]["zones"], [
            {"quality": 0, "shape": {"type": "simple_polygon", "data": [[2, 4], [4, 4], [2, 5]]}}])
        converted["items"][0]["shape"]["data"][0][0] = 999
        self.assertEqual(original["parts"][0]["geometry"][0]["outer"][0], [0, 0])

    def test_mirror_conversion_matches_upstream_for_arbitrary_point_and_angle(self):
        for degrees in [0, 15, 90, 180, 279.73, -90, 360]:
            for reflected in [False, True]:
                layout = jagua_layout(job(), output(degrees, reflected))
                transform = layout["placements"][0]["transform"]
                x, y = 2.3, -1.7
                upstream_y = -y if reflected else y
                a = math.radians(degrees)
                expected = (x * math.cos(a) - upstream_y * math.sin(a) + 4,
                            x * math.sin(a) + upstream_y * math.cos(a) + 5)
                canonical_x = -x if transform["mirrored"] else x
                a = transform["rotation_radians"]
                actual = (canonical_x * math.cos(a) - y * math.sin(a) + 4,
                          canonical_x * math.sin(a) + y * math.cos(a) + 5)
                for a, b in zip(actual, expected):
                    self.assertAlmostEqual(a, b, places=12)
                self.assertEqual(layout["units"], "inch")

    def test_copy_ids_span_all_sheets_and_embedded_source_is_ignored(self):
        data = output()
        data["solution"]["layouts"].append(deepcopy(data["solution"]["layouts"][0]))
        data["instance"] = {"items": "untrusted substitute geometry"}
        layout = jagua_layout(job(), data)
        self.assertEqual([p["copy_index"] for p in layout["placements"]], [0, 1])
        self.assertEqual([p["sheet_id"] for p in layout["placements"]], ["sheet-0", "sheet-1"])

    def test_output_refuses_unknown_ids_nonrigid_or_nonfinite_transforms(self):
        for change in [
            lambda v: v["solution"]["layouts"][0].update(container_id=7),
            lambda v: v["solution"]["layouts"][0]["placed_items"][0].update(item_id=-1),
            lambda v: v["solution"]["layouts"][0]["placed_items"][0]["transformation"].update(scale=2),
            lambda v: v["solution"]["layouts"][0]["placed_items"][0]["transformation"].update(rotation=float("nan")),
            lambda v: v["solution"]["layouts"][0]["placed_items"][0]["transformation"].update(reflected="false"),
        ]:
            data = output()
            change(data)
            with self.assertRaises(ValueError):
                jagua_layout(job(), data)

    def test_unsupported_constraints_are_never_silently_relaxed(self):
        for change in [
            lambda j: j.update(edge_clearance=.2),
            lambda j: j.update(mode="fill_area"),
            lambda j: j["parts"][0]["geometry"][0].update(holes=[[[.1, .1], [.3, .1], [.1, .3]]]),
            lambda j: j["parts"][0]["geometry"].append(deepcopy(j["parts"][0]["geometry"][0])),
            lambda j: j["stocks"][0].update(outline=deepcopy(j["parts"][0]["geometry"])),
        ]:
            original = job()
            change(original)
            with self.assertRaises(UnsupportedJob):
                jagua_input(original)

    def test_step_rule_is_not_rounded_to_a_divisor_of_360(self):
        original = job()
        original["parts"][0]["rotations"] = {"kind": "step", "degrees": 100}
        self.assertEqual(jagua_input(original)["items"][0]["orientation"]["rotation"],
                         {"mode": "discrete", "angles": [0, 100, 200, 300]})


if __name__ == "__main__":
    unittest.main()
