"""Independent authored group/native sidecar audit using the unmodified MIT reader."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

import numpy as np
from shapely.affinity import affine_transform, translate
from shapely.ops import unary_union
from svgpathtools import Document, parse_path

from h3_geometry_audit import normalize
from h6_start_audit import geometry

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    folder = parser.parse_args().folder.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    work = ROOT/'output'/f'h6-group-audit-{stamp}'
    work.mkdir()
    prep = json.loads((folder/'search/preparation.json').read_text(encoding='utf-8'))
    for name,wanted in prep['artifacts'].items(): assert digest(folder/'search'/name)==wanted,name
    projects, layers = [], {}
    for name in ['original','preserved','svg','dxf']:
        source = folder/f'native/{name}.lbrn2'
        xml,indices,omitted,zeros = normalize(source.read_text(encoding='utf-8'))
        assert not omitted,omitted
        (work/f'{name}.lbrn2').write_text(xml,encoding='utf-8',newline='\n')
        layers[name] = {i:int(s.get('CutIndex','0')) for i,s in zip(indices,E.fromstring(xml).findall('Shape'))}
        projects.append({'path':name,'normalized_xml':str(work/f'{name}.lbrn2'),
                         'shape_indices':indices,'svg_directory':str(work/name)})
    request = {'projects':projects,'oracle_report':str(work/'oracle.json')}
    (work/'request.json').write_text(json.dumps(request),encoding='utf-8',newline='\n')
    subprocess.run(['node',str(ROOT/'scripts/h3_geometry_oracle.mjs'),str(work/'request.json')],check=True,capture_output=True,timeout=30)
    oracle = json.loads((work/'oracle.json').read_text(encoding='utf-8'))
    assert all('error' not in r and not r['warnings'] for r in oracle['reports']),oracle
    def paths(name):
        return [sub for i,layer in layers[name].items() if layer==0
                for p in Document(work/name/f'{i}.svg').paths() for sub in p.continuous_subpaths()]
    original = paths('original')
    assert len(original)==5 and sum(p.isclosed() for p in original)==4
    layout = json.loads((folder/'search/nested/layout.json').read_text(encoding='utf-8'))
    expected_original = []
    for placement in layout['placements']:
        t=placement['transform'];c,s=np.cos(t['rotation_radians']),np.sin(t['rotation_radians']);m=-1 if t['mirrored'] else 1
        expected_original.extend(affine_transform(geometry(p,flip=True),[c*m,-s,s*m,c,*t['translation']]) for p in original)
    root = E.parse(folder/'search/nested/lead-group-sheet-1-cuts.svg').getroot()
    height=float(root.get('height').removesuffix('mm'))
    cuts=next(g for g in root if g.get('id')=='CUT')
    planned=[sub for p in cuts for sub in parse_path(p.get('d')).continuous_subpaths()]
    references=[translate(geometry(p,flip=True),yoff=height) for p in planned]
    starts=[np.array([p.start.real,height-p.start.imag]) for p in planned]
    assert len(references)==10 and sum(p.isclosed() for p in planned)==8
    results=[]
    for name in ['preserved','svg','dxf']:
        native=paths(name)
        assert len(native)==10,(name,len(native))
        actual=[geometry(p,flip=True) for p in native]
        expected=expected_original if name=='preserved' else references
        shift=np.array(unary_union(actual).bounds[:2])-unary_union(expected).bounds[:2]
        if name=='preserved': assert np.linalg.norm(shift)<0.0001,shift
        actual=[translate(p,xoff=-shift[0],yoff=-shift[1]) for p in actual]
        actual_starts=[np.array([p.start.real,-p.start.imag])-shift for p in native]
        unmatched=set(range(10));rows=[]
        for index,ref in enumerate(expected):
            match=min(unmatched,key=lambda i:ref.hausdorff_distance(actual[i]));unmatched.remove(match)
            distance=ref.hausdorff_distance(actual[match])
            # Open paths can reverse without inventing a closed seam. Their
            # endpoints and geometry, not a lead attachment, must be preserved.
            start_error=None if name=='preserved' or not planned[index].isclosed() else float(np.linalg.norm(actual_starts[match]-starts[index]))
            closed=bool(actual[match].coords[0]==actual[match].coords[-1])
            expected_closed=bool(ref.coords[0]==ref.coords[-1])
            rows.append({'contour_index':index,'geometry_error_mm':distance,'start_error_mm':start_error,
                         'closed':closed,'expected_closed':expected_closed,
                         'pass':distance<0.01 and (start_error is None or start_error<0.01) and closed==expected_closed})
        results.append({'format':name,'translation_mm':shift.tolist(),'contours':rows,'pass':all(r['pass'] for r in rows)})
    def settings(name):
        return [E.tostring(c,encoding='unicode') for c in E.parse(folder/f'native/{name}.lbrn2').getroot().findall('CutSetting')]
    settings_same=settings('original')==settings('preserved')
    result={'date':stamp,'scope':'Native opening/save of authored original, preserved nested project and both cutting sidecars; no new native lead generation',
            'held_out_geometry_read':False,'H6_complete':False,'oracle':'lbrn2-to-svg@0.5.3 (unmodified MIT)',
            'original_cut_settings_unchanged':settings_same,'results':results,
            'pass':settings_same and all(r['pass'] for r in results),
            'script_sha256':digest(Path(__file__)),
            # The outer checks manifest is finalized after this audit; pin the
            # actual immutable inputs instead of a changing aggregate inventory.
            'artifacts':{p.relative_to(folder).as_posix():digest(p)
                         for parent in [folder/'native',folder/'search']
                         for p in sorted(parent.rglob('*')) if p.is_file()}}
    target=folder/f'native-audit-{stamp}.json'
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'report':str(target),'pass':result['pass'],'settings_unchanged':settings_same,
                      'results':[{'format':r['format'],'pass':r['pass'],'maximum_geometry_mm':max(c['geometry_error_mm'] for c in r['contours']),
                                  'maximum_start_mm':max((c['start_error_mm'] or 0) for c in r['contours'])} for r in results]},indent=2))
    assert result['pass'],'Failed native audit retained'


if __name__ == '__main__':
    main()
