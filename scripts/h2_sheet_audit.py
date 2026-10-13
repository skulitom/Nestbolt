"""Frozen training-only pre-arranged sheet-outline checks; never held-out data."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
import time

import psutil
from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def point_segment(p, a, b):
    delta = [b[i]-a[i] for i in range(2)]
    length2 = sum(v*v for v in delta)
    t = max(0, min(1, sum((p[i]-a[i])*delta[i] for i in range(2))/length2)) if length2 else 0
    return math.hypot(*(p[i]-a[i]-t*delta[i] for i in range(2)))


def ring_distance(a, b):
    def directed(left, right):
        return max(min(point_segment(p, right[i], right[(i+1) % len(right)]) for i in range(len(right))) for p in left)
    return max(directed(a, b), directed(b, a))


def main():
    manifest_bytes = (CORPUS/'manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    training = [r for r in manifest['files'] if r['split'] == 'training']
    rows = [r for r in training if r['path'].endswith('--existing-nest.dxf')]
    assert len(rows) == 10
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT/'output'/f'h2-sheets-{stamp}'
    work.mkdir(exist_ok=False)
    binary = ROOT/'target/release/nestbolt.exe'
    digest, binary_hash = source_digest(), sha256(binary.read_bytes()).hexdigest()
    script_hash = sha256(Path(__file__).read_bytes()).hexdigest()
    results = []
    for i, row in enumerate(rows):
        assert sha256((CORPUS/row['path']).read_bytes()).hexdigest() == row['sha256']
        label_bytes = (CORPUS/row['label']).read_bytes()
        assert sha256(label_bytes).hexdigest() == row['label_sha256']
        label = json.loads(label_bytes)
        output = work/f'{i}.json'
        command = [str(binary), 'import', str(CORPUS/row['path']), '--output', str(output)]
        for key, flag in [('layers', '--layers'), ('colors', '--colors'), ('close_gaps_mm', '--close-gaps')]:
            if key in label['import_options']:
                value = label['import_options'][key]
                command += [flag, ','.join(map(str,value)) if isinstance(value,list) else str(value)]
        start = time.perf_counter()
        proc = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW | 4)
        try:
            child = psutil.Process(proc.pid)
            child.cpu_affinity([0])
            child.resume()
        except BaseException:
            proc.kill()
            proc.communicate()
            raise
        timed_out = False
        try:
            stdout, stderr = proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            stdout, stderr = proc.communicate()
        result = {'path':row['path'],'source_sha256':row['sha256'],'label_sha256':row['label_sha256'],
                  'cpu':0,'elapsed_s':time.perf_counter()-start,'exit_code':proc.returncode,'timed_out':timed_out,
                  'stderr':stderr.decode('utf-8',errors='replace')[-2000:],'pass':False}
        if proc.returncode == 0:
            library = json.loads(output.read_text(encoding='utf-8'))
            outlines = library.get('sheet_outlines',[])
            result['sheet_count'] = len(outlines)
            result['cut_parts_match'] = len(library['parts']) == len(label['cut_parts']) and sorted(len(p['holes']) for p in library['parts']) == sorted(p['holes'] for p in label['cut_parts'])
            result['availability_warning'] = any('sheet_outline_available' in w for w in library['warnings'])
            if len(outlines) == 1:
                sheet = outlines[0]
                expected = label['features']['sheet_outline_mm']
                bbox = [min(p[0] for p in expected), min(p[1] for p in expected), max(p[0] for p in expected), max(p[1] for p in expected)]
                normalized = [[p[0]-bbox[0],p[1]-bbox[1]] for p in expected]
                polygons = sheet['outline_mm']
                distance = ring_distance(normalized,polygons[0]['outer']) if len(polygons)==1 else None
                result.update(sheet_id=sheet['id'],width_mm=sheet['width_mm'],height_mm=sheet['height_mm'],origin_mm=sheet['origin_mm'],distance_mm=distance)
                result['dimensions_match'] = max(abs(sheet['width_mm']-(bbox[2]-bbox[0])),abs(sheet['height_mm']-(bbox[3]-bbox[1])),*(abs(sheet['origin_mm'][i]-bbox[i]) for i in range(2))) <= label['geometry_tolerance_mm']
                result['pass'] = bool(result['cut_parts_match'] and result['availability_warning'] and result['dimensions_match'] and distance is not None and distance <= label['geometry_tolerance_mm'] and not polygons[0]['holes'])
        results.append(result)
    assert source_digest()==digest and sha256(binary.read_bytes()).hexdigest()==binary_hash
    assert sha256(Path(__file__).read_bytes()).hexdigest()==script_hash
    report = {'recorded_at':stamp,'scope':'Ten frozen training pre-arranged nest sheet outlines; import/geometry check only',
              'H2':False,'held_out_read':False,'source_sha256':digest,'binary_sha256':binary_hash,'runner_sha256':script_hash,
              'manifest_sha256':sha256(manifest_bytes).hexdigest(),'passed':sum(r['pass'] for r in results),'attempted':len(results),'rows':results}
    target = ROOT/'benchmarks/results'/f'h2-sheets-{stamp}.json'
    target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    table = '\n'.join(f"| {r['path']} | {r.get('width_mm','—')} × {r.get('height_mm','—')} | {r.get('distance_mm','—')} | {r['pass']} |" for r in results)
    target.with_suffix('.md').write_text(f"# Training sheet-outline audit — {stamp}\n\n{report['passed']}/{len(results)} pass. H2 remains incomplete. One CCD0 physical core, affinity assigned before execution, ten-second import limit; source/binary/runner hashes unchanged. No held-out geometry or labels read. Compares stock outline dimensions and polygon boundaries to independent frozen generator labels, while preserving cut-part/hole counts and checking the availability message. It is not a solver performance or full fidelity claim.\n\n| Training file | Stock size mm | Boundary distance mm | Pass |\n|---|---:|---:|---|\n{table}\n\n[Machine-readable record]({target.name}).\n",encoding='utf-8',newline='\n')
    print(json.dumps({'report':str(target),'passed':report['passed'],'attempted':len(results)}))


if __name__ == '__main__':
    main()
