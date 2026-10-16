"""Sensitivity checks for the independent saved-export checker, no search."""
import io,math,sys,unittest,zipfile
import ezdxf
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import h4_curve_export_check_v3 as check

PART={'outer':{'start':[0,0],'segments':[
    {'kind':'line','to':[4,0]},
    {'kind':'quad','control':[4,2],'to':[2,2]},
    {'kind':'cubic','controls':[[1,2],[0,1]],'to':[0,0]}]},'holes':[]}
PLACE={'part_id':'p','copy_index':0,'transform':{'mirrored':False,'rotation_radians':math.pi/2,'translation':[10,20]}}
SVG='<svg xmlns="http://www.w3.org/2000/svg"><g id="CUT"><path id="p#0" fill-rule="evenodd" d="M10 80 L10 76 Q8 76 8 78 C8 79 9 80 10 80 Z"/></g></svg>'

def bundle(svg=SVG,move=0,omit=False,extra=False,rational=False):
    d=ezdxf.new('R2010');m=d.modelspace()
    m.add_line((10,20),(10,24),dxfattribs={'layer':'CUT'})
    s=m.add_spline(degree=2,dxfattribs={'layer':'CUT'});s.control_points=[(10,24,0),(8,24,0),(8,22,0)];s.knots=[0,0,0,1,1,1]
    if not omit:
        s=m.add_spline(degree=3,dxfattribs={'layer':'CUT'});s.control_points=[(8,22,0),(8+move,21,0),(9,20,0),(10,20,0)];s.knots=[0,0,0,0,1,1,1,1]
        if rational:s.weights=[1,2,1,1]
    if extra:m.add_line((0,0),(1,0),dxfattribs={'layer':'CUT'})
    text=io.StringIO();d.write(text);raw=io.BytesIO()
    with zipfile.ZipFile(raw,'w') as z:
        z.writestr('s.svg',svg);z.writestr('s.dxf',text.getvalue())
    return zipfile.ZipFile(io.BytesIO(raw.getvalue()))

class Checks(unittest.TestCase):
    def test_known_quarter_turn_and_all_three_primitives(self):
        with bundle() as z:
            svg=check.svg_check(z,'s.svg',{'p':PART},[PLACE],100)
            count,error=check.compare(check.source_segments(PART,PLACE),check.dxf_segments(z,'s.dxf'))
            self.assertEqual(dict(count),{'line':1,'quad':1,'cubic':1})
            self.assertEqual(svg['primitives'],dict(count));self.assertLess(error,1e-12)
            self.assertEqual(dict(check.dxf_entity_types(z,'s.dxf')),{'LINE':1,'SPLINE':2})
    def test_svg_control_displacement_fails(self):
        with bundle(svg=SVG.replace('C8 79','C8.02 79')) as z,self.assertRaises(AssertionError):
            check.svg_check(z,'s.svg',{'p':PART},[PLACE],100)
    def test_missing_svg_path_fails(self):
        with bundle(svg='<svg xmlns="http://www.w3.org/2000/svg"/>') as z,self.assertRaises(AssertionError):
            check.svg_check(z,'s.svg',{'p':PART},[PLACE],100)
    def test_extra_svg_path_fails(self):
        with bundle(svg=SVG.replace('</g>','<path id="extra" fill-rule="evenodd" d="M0 0 L1 0"/></g>')) as z,self.assertRaises(KeyError):
            check.svg_check(z,'s.svg',{'p':PART},[PLACE],100)
    def test_dxf_control_displacement_fails(self):
        with bundle(move=.02) as z,self.assertRaises(AssertionError):
            check.compare(check.source_segments(PART,PLACE),check.dxf_segments(z,'s.dxf'))
    def test_missing_last_dxf_entity_fails(self):
        with bundle(omit=True) as z,self.assertRaises(AssertionError):
            check.compare(check.source_segments(PART,PLACE),check.dxf_segments(z,'s.dxf'))
    def test_extra_dxf_entity_fails(self):
        with bundle(extra=True) as z,self.assertRaises(AssertionError):
            check.compare(check.source_segments(PART,PLACE),check.dxf_segments(z,'s.dxf'))
    def test_rational_spline_is_not_bezier(self):
        with bundle(rational=True) as z,self.assertRaises(AssertionError):
            check.compare(check.source_segments(PART,PLACE),check.dxf_segments(z,'s.dxf'))

if __name__=='__main__':unittest.main(verbosity=2)
