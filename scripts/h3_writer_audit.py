"""Training-only writer audit: independently restrict each XML diff.

Uses deterministic diagnostic placements, not a search quality result. The core
independent validator checks the assembled unit polygons. Native opening and
independent source-geometry unit coverage remain separate H3 requirements.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
import time
import xml.etree.ElementTree as E

import psutil
from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def canonical(node):
    return E.canonicalize(E.tostring(node, encoding='unicode'), strip_text=True)


def matrix(node):
    return list(map(float, node.findtext('XForm', '1 0 0 1 0 0').split()))


def placed(old, transform):
    a,b,c,d,e,f = old
    s,cosa = math.sin(transform['rotation_radians']), math.cos(transform['rotation_radians'])
    tx,ty = transform['translation']; sign = -1 if transform['mirrored'] else 1
    return [sign*cosa*a-s*b, sign*s*a+cosa*b, sign*cosa*c-s*d,
            sign*s*c+cosa*d, sign*cosa*e-s*f+tx, sign*s*e+cosa*f+ty]


def audit(source, payload):
    root = E.fromstring(source)
    tops = root.findall('Shape')
    units = payload['nesting']['units']; fixed = payload['nesting']['fixed']
    all_members = [m for u in units for m in u['members']] + fixed
    assert sorted(all_members) == list(range(len(tops))), 'missing or repeated top-level shape'
    assert all(len(u['members']) == 1 for u in units if any(tops[m].get('Type') == 'Group' for m in u['members'])), 'split or attached group'
    definitions = {}
    for n in root.iter():
        for attribute, tag in [('VertID','VertList'),('PrimID','PrimList')]:
            if n.get(attribute) is not None and n.find(tag) is not None:
                definitions[attribute,n.get(attribute)] = canonical(n.find(tag))
        if n.get('Type') == 'Bitmap' and n.get('Data') is not None:
            definitions['SourceHash',n.get('SourceHash')] = n.get('Data')
    results = []
    for sheet in payload['files']:
        written = E.fromstring(sheet['xml']); output = written.findall('Shape')
        assert root.attrib == written.attrib, 'root metadata changed'
        moves = {member:p['transform'] for p in sheet['placements'] for member in units[p['unit']]['members']}
        kept = sorted(set(moves) | set(fixed))
        assert len(output) == len(kept)+1, 'incorrect sheet shape count'
        # All non-shape document elements must be unchanged, apart from adding
        # the missing T1 setting. Includes unknown XML, preferences and thumbnail.
        before_meta = [n for n in root if n.tag != 'Shape']
        after_meta = [n for n in written if n.tag != 'Shape']
        t1 = [n for n in root.findall('CutSetting') if n.find('index') is not None and n.find('index').get('Value') == '30']
        if not t1:
            extra = after_meta.pop()
            assert extra.tag == 'CutSetting' and extra.get('type') == 'Tool'
            assert extra.find('index').get('Value') == '30'
        assert list(map(canonical,before_meta)) == list(map(canonical,after_meta)), 'document settings changed'
        retained_defs = set()
        for index in kept:
            for n in tops[index].iter():
                for attribute, tag in [('VertID','VertList'),('PrimID','PrimList')]:
                    if n.get(attribute) is not None and n.find(tag) is not None:
                        retained_defs.add((attribute,n.get(attribute)))
                if n.get('Type') == 'Bitmap' and n.get('Data') is not None:
                    retained_defs.add(('SourceHash',n.get('SourceHash')))
        rehomes = Counter(); transform_error = 0.0
        for original_index, actual in zip(kept,output):
            original = tops[original_index]; normalized = deepcopy(actual)
            expected = placed(matrix(original),moves[original_index]) if original_index in moves else matrix(original)
            delta = max(abs(a-b) for a,b in zip(expected,matrix(actual)))
            assert delta < 1e-9, f'wrong composed transform: {delta}'
            transform_error = max(transform_error,delta)
            # Restore only the top-level XForm; a child or text-cache change will
            # still be seen by the canonical equality below.
            xf = normalized.find('XForm')
            if xf is not None: normalized.remove(xf)
            old_xf = original.find('XForm')
            if old_xf is not None:
                normalized.insert(list(original).index(old_xf),deepcopy(old_xf))
            def normalize_pair(old,new):
                for attribute,tag in [('VertID','VertList'),('PrimID','PrimList')]:
                    old_list = old.find(tag); new_list = new.find(tag)
                    if old_list is None and new_list is not None:
                        key = attribute,old.get(attribute)
                        assert key not in retained_defs, 'unnecessary shared-list edit'
                        assert canonical(new_list) == definitions[key], 'changed re-homed list'
                        retained_defs.add(key); rehomes[attribute] += 1
                        new.remove(new_list)
                if old.get('Data') is None and new.get('Data') is not None:
                    key = 'SourceHash',old.get('SourceHash')
                    assert key not in retained_defs and new.get('Data') == definitions[key]
                    retained_defs.add(key); rehomes['Data'] += 1; del new.attrib['Data']
                assert len(old) == len(new), 'unexpected child insertion/removal'
                for a,b in zip(old,new): normalize_pair(a,b)
            normalize_pair(original,normalized)
            assert canonical(original) == canonical(normalized), 'unapproved shape XML change'
        outline = output[-1]
        assert outline.attrib == {'Type':'Rect','CutIndex':'30','W':str(payload['width_mm']).removesuffix('.0'),'H':str(payload['height_mm']).removesuffix('.0')} or (
            outline.get('Type') == 'Rect' and outline.get('CutIndex') == '30' and
            float(outline.get('W')) == payload['width_mm'] and float(outline.get('H')) == payload['height_mm'])
        assert matrix(outline) == [1,0,0,1,payload['width_mm']/2,payload['height_mm']/2]
        results.append({'sheet':sheet['sheet'],'units':len(sheet['placements']),'kept_top_level':len(kept),
                        'fixed_shapes':len(fixed),'rehomes':dict(rehomes),'max_transform_error':transform_error,
                        'canonical_diff_allowed':True})
    assert payload['identity_byte_equal'], 'identity sheet changed bytes'
    validation = payload['validation']
    assert validation is None or validation['valid'], 'invalid diagnostic layout'
    return results


def main():
    # Reserve a fifth CCD0 physical core for Python/XML checks; child readers
    # use the first four physical cores, one process per core.
    psutil.Process().cpu_affinity([8])
    manifest_bytes = (CORPUS/'manifest.json').read_bytes()
    training = [r for r in json.loads(manifest_bytes)['files'] if r['split'] == 'training']
    rows = [r for r in training if Path(r['path']).suffix in ['.lbrn','.lbrn2']]
    assert len(rows) == 56
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT/'output'/f'h3-writer-{stamp}'; work.mkdir(exist_ok=False)
    binary = ROOT/'target/release/examples/lightburn_roundtrip.exe'
    binary_hash = sha256(binary.read_bytes()).hexdigest(); source_hash = source_digest()
    runner_hash = sha256(Path(__file__).read_bytes()).hexdigest()
    def run(index,row):
        path = CORPUS/row['path']; source = path.read_bytes()
        assert sha256(source).hexdigest() == row['sha256']
        begin = time.perf_counter()
        proc = subprocess.Popen([str(binary),str(path)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW|4)
        timeout = False
        try:
            child = psutil.Process(proc.pid); child.cpu_affinity([2*(index%4)]); child.resume()
            try: out,err = proc.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                timeout = True; proc.kill(); out,err = proc.communicate()
        except BaseException:
            proc.kill(); proc.communicate(); raise
        record = {'path':row['path'],'source_sha256':row['sha256'],'cpu':2*(index%4),
                  'elapsed_s':time.perf_counter()-begin,'exit_code':proc.returncode,
                  'status':'timeout' if timeout else 'error' if proc.returncode else 'returned',
                  'stderr':err.decode('utf-8',errors='replace')}
        if not proc.returncode:
            target = work/f'{index:03}.json'; target.write_bytes(out)
            payload = json.loads(out); record['status'] = payload['status']
            record.update(payload_path=str(target.relative_to(ROOT)),payload_sha256=sha256(out).hexdigest())
            if payload['status'] == 'written':
                try:
                    record['sheets'] = audit(source,payload)
                    record.update(units=len(payload['nesting']['units']),fixed=len(payload['nesting']['fixed']),
                                  identity_byte_equal=payload['identity_byte_equal'],
                                  independently_validated=payload['validation'] is not None and payload['validation']['valid'])
                except Exception as error:
                    record.update(status='audit_error',error=str(error))
            else: record['error'] = payload.get('error')
        print(f'{index+1}/56 {row["path"]}: {record["status"]}',flush=True)
        return record
    def batch(slot): return [run(i,r) for i,r in enumerate(rows) if i%4 == slot]
    with ThreadPoolExecutor(max_workers=4) as pool:
        reports = [r for group in pool.map(batch,range(4)) for r in group]
    reports.sort(key=lambda r:r['path'])
    assert source_hash == source_digest() and binary_hash == sha256(binary.read_bytes()).hexdigest()
    assert runner_hash == sha256(Path(__file__).read_bytes()).hexdigest()
    result = {'date':stamp,'scope':'Training unit assembly and preserving writer diagnostic; H3 incomplete',
              'H3':False,'held_out_read':False,'manifest_sha256':sha256(manifest_bytes).hexdigest(),
              'source_sha256':source_hash,'binary_sha256':binary_hash,'runner_sha256':runner_hash,
              'counts':dict(Counter(r['status'] for r in reports)),'rows':reports}
    output = ROOT/'benchmarks/results'/f'h3-writer-{stamp}.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n'); print(output)


if __name__ == '__main__': main()
