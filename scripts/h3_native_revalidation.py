"""Revalidate/re-export the five saved native-checked H3 layouts without search.

Only their training/authored sources are read. Require the same native-checked
XML, apart from line endings and <=1e-9 mm top-level numeric replay; settings,
children, shared resources and every other canonical element remain exact.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as E

from h3_heldout_audit import guards
from h3_writer_audit import canonical, matrix
from h6_material_cost import run

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'benchmarks/results/h3-lightburn-20261014T001636Z'
OUT = ROOT/'benchmarks/results/h3-completion-native-revalidation-20261015'


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def main():
    OUT.mkdir()
    before = guards()
    script_hash = digest(Path(__file__))
    prepared = json.loads((BASE/'prepared.json').read_bytes())
    observed = json.loads((BASE/'native-check.json').read_bytes())
    assert observed['passed'] and all(c['passed'] for c in observed['cases'])
    training = {r['path']:r for r in json.loads((ROOT/'benchmarks/datasets/shop/manifest.json').read_bytes())['files'] if r['split']=='training'}
    rows = []
    for entry in prepared['cases']:
        source = ROOT/entry['source']
        assert digest(source) == entry['provenance']['sha256']
        if entry['name'] != 'mirrored-origin':
            key = source.relative_to(ROOT/'benchmarks/datasets/shop').as_posix()
            assert training[key]['sha256'] == digest(source)
        else:
            assert source.relative_to(ROOT/'benchmarks/datasets/shop').as_posix() == 'probes/origin-top-right.lbrn2'
        case = BASE/entry['name']
        out = OUT/entry['name']
        out.mkdir()
        arguments = ['--library',source,'--request',case/'request.json','--layout',case/'nested/layout.json']
        validate = run([ROOT/'target/release/nestbolt.exe','validate',*arguments],out,'validate',8,120)
        assert validate['exit_code'] == 0
        assert json.loads((out/'validate-stdout.json').read_bytes())['valid']
        exported = run([ROOT/'target/release/nestbolt.exe','export',*arguments,'--out-dir',out/'exported'],out,'export',8,120)
        assert exported['exit_code'] == 0
        comparisons = []
        for filename in entry['files']:
            old = case/'nested'/filename
            new = out/'exported'/filename
            a,b = E.fromstring(old.read_bytes()),E.fromstring(new.read_bytes())
            expected,actual = a.findall('Shape'),b.findall('Shape')
            assert len(expected) == len(actual)
            delta = 0.
            for x,y in zip(expected,actual,strict=True):
                delta = max(delta,max(abs(i-j) for i,j in zip(matrix(x),matrix(y),strict=True)))
                assert delta <= 1e-9
                old_xf,new_xf = x.find('XForm'),y.find('XForm')
                assert (old_xf is None) == (new_xf is None)
                if new_xf is not None:
                    at = list(y).index(new_xf)
                    y.remove(new_xf)
                    y.insert(at,deepcopy(old_xf))
            assert canonical(a) == canonical(b)
            comparisons.append({'file':filename,'prior_sha256':digest(old),'current_sha256':digest(new),
                'byte_equal':old.read_bytes()==new.read_bytes(),'maximum_top_level_xform_difference':delta,
                'remaining_canonical_XML_equal':True})
        rows.append({'name':entry['name'],'source_sha256':digest(source),'validation':validate,'export':exported,
                     'comparisons':comparisons,'passed':True})
    assert before == guards() and digest(Path(__file__)) == script_hash
    value = {'scope':__doc__,'guards':before,'guards_unchanged':True,'script_sha256':script_hash,
             'native_observations':str((BASE/'native-check.json').relative_to(ROOT)),
             'native_observations_sha256':digest(BASE/'native-check.json'),
             'held_out_geometry_read':False,'new_searches':0,'passed':len(rows)==5 and all(r['passed'] for r in rows),'rows':rows}
    (OUT/'results.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'passed':value['passed'],'projects':len(rows),'output':str(OUT)}))


if __name__ == '__main__':
    main()
