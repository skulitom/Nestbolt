"""Deepnest quantity/source identity, independent edge margins and axis regressions."""
from copy import deepcopy
import json
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from benchmark_io import UnsupportedJob
from deepnest_io import prepare, layout

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = json.loads((ROOT / 'benchmarks/deepnest/tool.json').read_bytes())['settings']['identical']


def job():
    return json.loads((ROOT / 'benchmarks/fixtures/svgnest-edge-gap.json').read_bytes())


def placement(prepared, key='0', sheet='0000-0000', x=20, y=30, angle=180):
    return {'placements': [{'sheet': prepared['stocks'][sheet]['source'], 'sheetid': sheet,
        'sheetplacements': [{'id': int(key), 'source': prepared['copies'][key]['source'],
                            'x': x, 'y': y, 'rotation': angle}]}]}


class DeepnestAdapterTests(unittest.TestCase):
    def test_quantities_and_holes_preserve_every_original_vertex(self):
        source = job()
        prepared = prepare(source, SETTINGS)
        self.assertEqual(len(prepared['copies']), 4)
        self.assertEqual(len(prepared['imports']), len(source['parts'])+1)
        for i, part in enumerate(source['parts']):
            native = prepared['imports'][i]
            self.assertEqual(native['quantity'], part['quantity'])
            component = part['geometry'][0]
            for node, ring in zip(ET.fromstring(native['svg']), [component['outer'], *component['holes']], strict=True):
                points = [[float(n) for n in point.split(',')] for point in node.attrib['points'].split()]
                self.assertEqual(points, [[y,-x] for x,y in ring])

    def test_mixed_stock_caps_and_native_negative_offset_behavior(self):
        source = job()
        second = deepcopy(source['stocks'][0])
        second.update(id='small', width=200, height=100, count=2)
        source['stocks'].append(second)
        for axis in ['x','y']:
            prepared = prepare(source, SETTINGS, axis)
            self.assertEqual(len(prepared['stocks']), 6)
            self.assertEqual(prepared['stocks']['0001-0001']['stock_id'], 'small')
            inputs = prepared['imports'][-1]
            corners = [[float(n) for n in point.split(',')] for point in list(ET.fromstring(inputs['svg']))[0].attrib['points'].split()]
            expected = [200-3-5-14+4,100-11-13-14+4]
            self.assertEqual(corners[2], expected if axis == 'x' else expected[::-1])

    def test_conservative_gap_keeps_original_edge_locations(self):
        source = job()
        prepared = prepare(source, {**SETTINGS, 'spacing_multiplier': 2}, 'x')
        gap = prepared['config']['spacing']
        self.assertEqual(gap, 2*source['clearance'])
        stock = prepared['stocks']['0000-0000']
        # Native inflated contour touches zero; original contour starts half a gap in.
        self.assertEqual(stock['origin'][0]+gap/2, source['stocks'][0]['margins']['left']+source['edge_clearance'])
        self.assertNotIn('spacing_multiplier', prepared['config'])

    def test_transform_recovers_original_stock_coordinate_frame(self):
        for axis in ['x','y']:
            prepared = prepare(job(), SETTINGS, axis)
            stock = prepared['stocks']['0000-0000']
            native = placement(prepared)
            item = layout(prepared, native)['placements'][0]
            x, y = 20+stock['origin'][0], 30+stock['origin'][1]
            expected = [x,y] if axis == 'x' else [stock['original_width']-y,x]
            self.assertEqual(item['transform']['translation'], expected)
            self.assertAlmostEqual(item['transform']['rotation_radians'], math.pi)

    def test_unknown_duplicate_and_altered_source_ids_fail(self):
        prepared = prepare(job(), SETTINGS)
        for change in ['duplicate_part','duplicate_stock','source','stock_source','nonrigid','nan']:
            native = placement(prepared)
            sheet = native['placements'][0]
            item = sheet['sheetplacements'][0]
            if change == 'duplicate_part': sheet['sheetplacements'].append(deepcopy(item))
            if change == 'duplicate_stock': native['placements'].append(deepcopy(sheet))
            if change == 'source': item['source'] = 100
            if change == 'stock_source': sheet['sheet'] = 100
            if change == 'nonrigid': item['scale'] = 2
            if change == 'nan': item['x'] = math.nan
            with self.assertRaises(ValueError): layout(prepared, native)

    def test_unimplemented_constraints_and_rotation_loss_fail_explicitly(self):
        for change in ['remnant','defect','disconnected','angles']:
            source = job()
            if change == 'remnant': source['stocks'][0]['outline'] = deepcopy(source['parts'][0]['geometry'])
            if change == 'defect': source['stocks'][0]['defects'] = deepcopy(source['parts'][0]['geometry'])
            if change == 'disconnected': source['parts'][0]['geometry'] *= 2
            if change == 'angles': source['parts'][0]['rotations']['degrees'] = [0,45,180]
            with self.assertRaises(UnsupportedJob): prepare(source, SETTINGS)


if __name__ == '__main__':
    unittest.main()
