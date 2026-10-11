"""Original-coordinate checks for the current single-strip comparator."""
from copy import deepcopy
import math
import unittest

from benchmark_io import UnsupportedJob
from sparrow_io import prepare, layout, strip_length
from test_benchmark_io import job


class SparrowAdapterTests(unittest.TestCase):
    def test_separate_edge_gap_and_original_geometry(self):
        source = job()
        source['edge_clearance'] = 1
        prepared = prepare(source)
        self.assertAlmostEqual(prepared['input']['strip_height'], 4.2)
        self.assertEqual(prepared['origin'], [1.9, 3.9])
        self.assertEqual(prepared['input']['items'][0]['shape']['data'], source['parts'][0]['geometry'][0]['outer'])
        self.assertEqual(prepared['input']['items'][0]['orientation']['reflection_axes'], [90])
        self.assertEqual(source['edge_clearance'], 1)

    def test_axis_rotation_restores_reflected_and_unmirrored_points(self):
        source = job()
        for axis in ['x','y']:
            prepared = prepare(source,axis)
            for reflected in [False,True]:
                for degrees in [0,15,90,180,271]:
                    raw={'solution':{'strip_width':12,'layout':{'container_id':0,'placed_items':[
                        {'item_id':0,'transformation':{'rotation':degrees,'reflected':reflected,'translation':[4,5]}}]}}}
                    t=layout(source,prepared,raw)['placements'][0]['transform']
                    px,py=2.3,-1.7
                    x,y=(py,-px) if axis=='y' else (px,py)
                    if reflected: y=-y
                    a=math.radians(degrees)
                    x,y=x*math.cos(a)-y*math.sin(a)+4,y*math.cos(a)+x*math.sin(a)+5
                    x,y=x+prepared['origin'][0],y+prepared['origin'][1]
                    if axis=='y': x,y=source['stocks'][0]['width']-y,x
                    if reflected: px=-px
                    a=t['rotation_radians']
                    actual=[px*math.cos(a)-py*math.sin(a)+t['translation'][0],px*math.sin(a)+py*math.cos(a)+t['translation'][1]]
                    for wanted,got in zip([x,y],actual): self.assertAlmostEqual(wanted,got,places=12)
            if axis=='y': self.assertEqual(prepared['input']['items'][0]['orientation']['reflection_axes'],[0])

    def test_unrepresentable_jobs_are_explicit(self):
        for change in [lambda j:j['stocks'].append(deepcopy(j['stocks'][0])),
                       lambda j:j['stocks'][0].update(count=0),
                       lambda j:j['stocks'][0].update(defects=[{'outer':[[0,0],[1,0],[0,1]],'holes':[]}]),
                       lambda j:j['parts'][0]['geometry'][0].update(holes=[[[.1,.1],[.2,.1],[.1,.2]]]),
                       lambda j:j.update(mode='fill_area')]:
            source=job();change(source)
            with self.assertRaises(UnsupportedJob): prepare(source)

    def test_strip_score_ignores_reported_width(self):
        source=job();prepared=prepare(source)
        raw={'solution':{'strip_width':999,'layout':{'container_id':0,'placed_items':[
            {'item_id':0,'transformation':{'rotation':0,'translation':[4,5]}}]}}}
        common=layout(source,prepared,raw)
        expected=max(x for x,y in source['parts'][0]['geometry'][0]['outer'])+4+prepared['origin'][0]
        self.assertEqual(strip_length(source,common),expected)


if __name__=='__main__': unittest.main()
