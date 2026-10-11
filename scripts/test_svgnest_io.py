"""Coordinate, constraint and output-identity regressions for the browser adapter."""
from copy import deepcopy
import json
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from benchmark_io import UnsupportedJob
from svgnest_io import prepare, layout
from svgnest import guard_held_out

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = json.loads((ROOT / 'benchmarks/svgnest/tool.json').read_bytes())['settings']['identical']


def job():
    value = json.loads((ROOT / 'examples/validation-job.json').read_bytes())
    value['stocks'][0]['count'] = None
    return value


class SvgNestTests(unittest.TestCase):
    def test_input_preserves_every_vertex_hole_copy_and_angle(self):
        original = job()
        prepared = prepare(original, SETTINGS)
        nodes = {p.attrib['id']: p for p in ET.fromstring(prepared['svg'])}
        self.assertEqual(prepared['copies'], sum(p['quantity'] for p in original['parts']))
        self.assertEqual(prepared['config']['rotations'], 2)
        parts = {p['id']: p for p in original['parts']}
        for key, mapping in prepared['mapping'].items():
            source = parts[mapping['part_id']]['geometry'][0]
            for i, ring in enumerate([source['outer'], *source['holes']]):
                name = key if i == 0 else f'{key}-hole-{i}'
                actual = [[float(n) for n in pair.split(',')] for pair in nodes[name].attrib['points'].split()]
                expected = [[y + mapping['offset'][0], -x + mapping['offset'][1]] for x, y in ring]
                self.assertEqual(actual, expected)

    def test_margin_and_independent_edge_gap_match_virtual_bin(self):
        value = job()
        value['clearance'], value['edge_clearance'] = 4, 7
        value['stocks'][0]['margins'] = {'left': 3, 'right': 5, 'bottom': 11, 'top': 13}
        for axis in ['x', 'y']:
            prepared = prepare(value, SETTINGS, axis)
            points = [[float(n) for n in p.split(',')] for p in list(ET.fromstring(prepared['svg']))[0].attrib['points'].split()]
            w, h = value['stocks'][0]['width'], value['stocks'][0]['height']
            expected = (w-3-5-14+8, h-11-13-14+8) if axis == 'x' else (h-11-13-14+8, w-5-3-14+8)
            self.assertEqual(points[2], list(expected))
            self.assertEqual(prepared['origin'], [3+7-2, 11+7-2] if axis == 'x' else [11+7-2, 5+7-2])

    def test_returned_rigid_transform_is_inverse_of_gallery_and_axis(self):
        for axis in ['x', 'y']:
            prepared = prepare(job(), SETTINGS, axis)
            source = prepared['mapping']['copy-0']
            ox, oy = source['offset']
            # A 90 degree placement with desired original translation (23,41).
            target = [23, 41] if axis == 'x' else [41, prepared['original_width']-23]
            matrix = [0, 1, -1, 0, target[0]+oy-prepared['origin'][0], target[1]-ox-prepared['origin'][1]]
            groups = [[{'outer_id': 'copy-0', 'hole_ids': ['copy-0-hole-1'], 'matrix': matrix}]]
            converted = layout(prepared, groups)['placements'][0]
            self.assertEqual(converted['transform']['translation'], [23, 41])
            self.assertAlmostEqual(converted['transform']['rotation_radians'], math.pi/2)
            self.assertEqual(converted['part_id'], source['part_id'])
            for bad in [[2, 0, 0, 2, 0, 0], [-1, 0, 0, 1, 0, 0], [1, 0, 0, 1, math.nan, 0]]:
                groups[0][0]['matrix'] = bad
                with self.assertRaises(ValueError):
                    layout(prepared, groups)

    def test_constraints_cannot_be_silently_removed(self):
        for change in ['mixed', 'defect', 'disconnected', 'angles']:
            value = job()
            if change == 'mixed': value['stocks'].append(deepcopy(value['stocks'][0]))
            if change == 'defect': value['stocks'][0]['defects'] = [value['parts'][0]['geometry'][0]]
            if change == 'disconnected': value['parts'][0]['geometry'] *= 2
            if change == 'angles': value['parts'][0]['rotations']['degrees'] = [0, 45, 180]
            with self.assertRaises(UnsupportedJob): prepare(value, SETTINGS)
        value = job()
        value['parts'][0]['quantity'] = 2001
        with self.assertRaises(ValueError): prepare(value, SETTINGS)
        value['name'] = 'm-box-compact-2000'
        with self.assertRaisesRegex(ValueError, 'Held-out'): guard_held_out(value, 'development')

    def test_missing_holes_unknown_and_duplicate_copies_fail(self):
        prepared = prepare(job(), SETTINGS)
        base = {'outer_id': 'copy-0', 'hole_ids': ['copy-0-hole-1'], 'matrix': [1, 0, 0, 1, 0, 0]}
        for groups in [[[{**base, 'hole_ids': []}]], [[{**base, 'outer_id': 'intruder'}]], [[base, base]],
                       [[{**base, 'hole_ids': ['copy-0-hole-1', 'copy-0-hole-1']}]]]:
            with self.assertRaises(ValueError): layout(prepared, groups)


if __name__ == '__main__':
    unittest.main()
