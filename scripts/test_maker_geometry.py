"""Meaningful bounds/topology regressions for maker source conversion."""
import unittest

from shapely.geometry import LineString, Point
from svgpathtools import Arc, CubicBezier, QuadraticBezier, parse_path

from maker_geometry import classify_rings, flatten_segment, normalize, path_rings
from makers import unfold


class MakerGeometryTests(unittest.TestCase):
    def test_chord_bound_survives_inflections_loops_and_large_arcs(self):
        curves = [CubicBezier(0j, 200+900j, -300-900j, 100+0j),
                  CubicBezier(0j, 100+100j, -100+100j, 0j),
                  QuadraticBezier(0j, -100+0j, 10+0j),
                  Arc(0j, 400+60j, 37, True, True, 500+150j)]
        for curve in curves:
            points = flatten_segment(curve)
            line = LineString([(p.real, p.imag) for p in points])
            # Independent dense evaluations, including non-midpoint samples.
            distances = [line.distance(Point(curve.point(i/2000).real, curve.point(i/2000).imag)) for i in range(2001)]
            self.assertLessEqual(max(distances), .005000001)

    def test_holes_islands_and_disconnected_components_are_preserved(self):
        geometry = classify_rings(path_rings(
            'M0,0 H100 V100 H0 Z M10,10 H90 V90 H10 Z '
            'M20,20 H30 V30 H20 Z M120,0 H130 V10 H120 Z'))
        self.assertEqual(len(geometry), 3)
        self.assertEqual([len(c['holes']) for c in geometry], [1, 0, 0])
        shifted, offset = normalize(classify_rings(path_rings('M-10,-20 H10 V30 H-10 Z')))
        self.assertEqual(offset, [-10, -20])
        self.assertEqual(shifted[0]['outer'][0], [0, 0])

    def test_invalid_cut_paths_are_rejected_without_repair(self):
        for d in ['M0,0 L10,0 L10,10', 'M0,0 L10,10 L0,10 L10,0 Z',
                  'M0,0 H10 V10 H0 Z M0,2 H5 V5 H0 Z']:
            with self.assertRaises(ValueError):
                classify_rings(path_rings(d))

    def test_fold_stitch_lines_are_removed_but_curves_are_retained(self):
        d = unfold('M0,5 L0,10 L20,10 C30,10 30,0 20,0 L0,0')
        path = parse_path(d)
        self.assertTrue(path.isclosed())
        self.assertEqual(sum(isinstance(s, CubicBezier) for s in path), 2)
        self.assertEqual(len(classify_rings(path_rings(d))), 1)
        self.assertNotIn(5j, [s.start for s in path])
        with self.assertRaises(ValueError):
            unfold('M1,10 L20,10 L20,0 L1,0')


if __name__ == '__main__':
    unittest.main()
