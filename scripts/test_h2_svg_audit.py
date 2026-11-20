"""Regression controls for the independent SVG training-export check."""
from io import BytesIO
from math import pi
import unittest

from h2_svg_audit import measure


def rectangle(x1, y1, x2, y2):
    points = [[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]
    return {
        "start": points[0],
        "segments": [{"kind": "line", "to": p} for p in points[1:]],
    }


class SvgTrainingExport(unittest.TestCase):
    # Hand-placed corners: mirror x, rotate 90 degrees, translate by (20,35),
    # then reflect for a 50 mm high SVG sheet. File coordinates are (20-y,15+x).
    outer = "M20 15 L20 25 L14 25 L14 15 Z"
    first = "M19 16 L19 18 L16 18 L16 16 Z"
    second = "M18 21 L18 23 L17 23 L17 21 Z"

    def measure_svg(
        self, contours, width="40mm", viewbox="0 0 40 50", attributes="", path_attributes=""
    ):
        part = {
            "outer": rectangle(0, 0, 10, 6),
            "holes": [rectangle(1, 1, 3, 4), rectangle(6, 2, 8, 3)],
        }
        placement = {
            "part_id": "tile",
            "copy_index": 0,
            "transform": {
                "mirrored": True,
                "rotation_radians": pi / 2,
                "translation": [20, 35],
            },
        }
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="50mm" viewBox="{viewbox}">'
            f'<g id="CUT" stroke="#000000" {attributes}><path id="tile#0" {path_attributes} d="{" ".join(contours)}"/></g></svg>'
        )
        return measure(
            BytesIO(svg.encode()),
            {"width": 40, "height": 50},
            {"tile": part},
            [placement],
        )

    def test_one_to_one_matching_accepts_reordered_holes_and_opposite_winding(self):
        result = self.measure_svg(
            [self.second, "M14 15 L14 25 L20 25 L20 15 Z", self.first]
        )
        self.assertEqual(result["placements"], 1)
        self.assertEqual(result["contours"], 3)
        self.assertLess(result["max_hausdorff_mm"], 1e-9)

    def test_missing_duplicate_and_deformed_cuts_fail(self):
        # The deformed outer still has the original bounding box.
        for contours in (
            [self.outer, self.first],
            [self.outer, self.first, self.first],
            [self.outer.replace("L20 25", "L19 20 L20 25"), self.first, self.second],
        ):
            with self.subTest(contours=contours), self.assertRaises(ValueError):
                self.measure_svg(contours)

    def test_edges_between_matching_vertices_must_follow_the_source(self):
        crossed = "M20 15 L14 25 L20 25 L14 15 Z"
        extra_diagonal = self.outer[:-1] + "L20 15 L14 25 L20 15 Z"
        for outer in (crossed, extra_diagonal):
            with self.subTest(outer=outer), self.assertRaisesRegex(ValueError, "one-to-one"):
                self.measure_svg([outer, self.first, self.second])

    def test_straight_edges_can_be_split_or_reversed_within_tolerance(self):
        outer = "M20.0095 15 L14.0095 15 L14.0095 25 L20.0095 25 L20.0095 22 Z"
        result = self.measure_svg([outer, self.first, self.second])
        self.assertAlmostEqual(result["max_hausdorff_mm"], 0.0095)
        self.assertLessEqual(result["max_continuous_upper_bound_mm"], 0.01)

    def test_wrong_physical_size_and_unhandled_presentation_fail(self):
        for kwargs in (
            {"width": "80mm"},
            {"viewbox": "0 0 80 50"},
            {"attributes": 'transform="scale(2)"'},
            {"attributes": 'display="none"'},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.measure_svg([self.outer, self.first, self.second], **kwargs)

    def test_path_stroke_selects_the_cut_layer(self):
        contours = [self.outer, self.first, self.second]
        for colour in ("inherit", "black", "#000", "#000000"):
            with self.subTest(colour=colour):
                result = self.measure_svg(contours, path_attributes=f'stroke="{colour}"')
                self.assertEqual(result["contours"], 3)
        for colour in ("#ff0000", "none"):
            with self.subTest(colour=colour), self.assertRaisesRegex(
                ValueError, "black stroke"
            ):
                self.measure_svg(contours, path_attributes=f'stroke="{colour}"')


if __name__ == "__main__":
    unittest.main()
