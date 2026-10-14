"""Authored DXF reader diagnostic: three encodings of an identical curved outline."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import ezdxf

ROOT = Path(__file__).resolve().parents[1]


def audit(folder):
    from h3_geometry_audit import normalize, product_paths
    from h6_start_audit import area_sign, digest, geometry
    import numpy as np
    from shapely.affinity import translate
    from shapely.ops import unary_union
    from svgpathtools import Document

    folder = folder.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    prepared = json.loads((folder/'preparation.json').read_text(encoding='utf-8'))
    assert digest(folder/'seams.dxf') == prepared['dxf_sha256']
    source = ROOT/'benchmarks/results/h6-starts-20261014T032245Z/exports/expected.json'
    row = json.loads(source.read_text(encoding='utf-8'))['contours'][-1]
    ref = geometry(product_paths({'paths':[{'curve':row['contour']}]})[0])
    scratch = ROOT/'output'/('h6-seam-audit-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    normalized = scratch/'normalized'
    normalized.mkdir(parents=True)
    xml,indices,omitted,zeros = normalize((folder/'seams-native.lbrn2').read_text(encoding='utf-8'))
    assert len(indices) == 3 and not omitted and not zeros
    (normalized/'dxf-native.lbrn2').write_text(xml,encoding='utf-8',newline='\n')
    subprocess.run(['node',str(ROOT/'scripts/h6_start_oracle.mjs'),str(normalized),str(scratch/'oracle')],check=True,timeout=30)
    paths = Document(scratch/'oracle/dxf-native.svg').paths()
    assert len(paths) == 3
    shapes = [geometry(p,flip=True) for p in paths]
    bounds = unary_union(shapes).bounds
    shift = [bounds[0]-ref.bounds[0],bounds[1]-ref.bounds[1]]
    records = []
    for variant,path,shape in zip(prepared['variants'],paths,shapes):
        expected = translate(ref,xoff=variant['offset_x_mm'])
        start = np.array([path.start.real,-path.start.imag])-shift
        records.append({'variant':variant['name'],
            'start_error_mm':float(np.linalg.norm(start-variant['expected_start_mm'])),
            'geometry_error_mm':expected.hausdorff_distance(translate(shape,xoff=-shift[0],yoff=-shift[1])),
            'native_winding_reversed':area_sign(ref)*area_sign(shape)<0})
    report = {'scope':'Native encoding diagnostic; not H6 acceptance','held_out_read':False,
        'records':records,'translation_mm':shift,'script_sha256':digest(Path(__file__)),
        'artifacts':{p.name:digest(p) for p in folder.iterdir() if p.is_file()}}
    target = folder/'native-audit.json'
    assert not target.exists()
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report['records'],indent=2))


def main():
    source = ROOT/'benchmarks/results/h6-starts-20261014T032245Z/exports/ordered.dxf'
    drawing = ezdxf.readfile(source)
    spline = [e for e in drawing.modelspace() if e.dxf.layer == 'CUT'][-1]
    assert spline.dxftype() == 'SPLINE'
    points = list(spline.control_points)
    assert len(points) == 16
    doc = ezdxf.new('R2013')
    doc.units = 4
    m = doc.modelspace()
    variants = []
    for i, name in enumerate(['open-spline', 'line-then-spline', 'spline-then-line']):
        pts = [(p[0]+i*100, p[1], 0) for p in points]
        chosen = pts[0][:2]
        rest = pts if i == 0 else pts[3:]
        count = (len(rest)-1)//3
        knots = [k for k in range(count+1) for _ in range(4 if k in [0,count] else 3)]
        if i == 1: m.add_line(pts[0],pts[3])
        m.add_open_spline(rest,degree=3,knots=knots)
        if i == 2: m.add_line(pts[0],pts[3])
        variants.append({'name': name, 'expected_start_mm': chosen,
                         'offset_x_mm': i*100, 'bounds_mm': [10+i*100,5,61.25+i*100,30]})
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT/'benchmarks/results'/f'h6-starts-seam-{stamp}'
    folder.mkdir()
    doc.saveas(folder/'seams.dxf')
    record = {'scope':'Authored seam encoding diagnostic only; no H6 gate claim',
              'held_out_read':False, 'source':str(source.relative_to(ROOT)).replace('\\','/'),
              'source_sha256':sha256(source.read_bytes()).hexdigest(), 'variants':variants,
              'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
              'dxf_sha256':sha256((folder/'seams.dxf').read_bytes()).hexdigest()}
    (folder/'preparation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    (folder/'LICENSES.md').write_text('Authored Nestbolt diagnostic and native derivatives: repository MIT LICENSE.\n',encoding='utf-8',newline='\n')
    print(folder)


if __name__ == '__main__':
    if len(sys.argv) == 2: audit(Path(sys.argv[1]))
    else: main()
