"""Append corrected validation of saved native SVGs; never rerun search or edit history."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import uuid

from lbf_report import contained_file
from svg_export_transform import groups_from_exports
from svgnest import ROOT, digest, write
from svgnest_io import layout


def correct(paths, scope):
    subprocess.run(['cargo','build','--locked','-p','nestbolt-cli'],cwd=ROOT,check=True)
    binary = ROOT/'target/debug'/('nestbolt.exe' if os.name == 'nt' else 'nestbolt')
    stamp = datetime.now(timezone.utc)
    identifier = f'{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    output = ROOT/'output/playwright/svg-corrections'/identifier
    output.mkdir(parents=True)
    sources = {name:digest(ROOT/name) for name in ['scripts/redecode_svgnest.py','scripts/svg_export_transform.py','scripts/svgnest_io.py']}
    rows = []
    for path, expected in paths:
        if digest(path) != expected:
            raise ValueError('Original run differs from its expected immutable record')
        original = json.loads(path.read_bytes())
        for name, checksum in original['outputs'].items():
            if digest(contained_file(path.parent,name)) != checksum:
                raise ValueError('Original output changed')
        if digest(path.parent/'job.json') != original['job_sha256']:
            raise ValueError('Original job changed')
        row = {'source_record':path.relative_to(ROOT).as_posix(),'source_record_sha256':expected,
               'original':original,'status':original['status'],'score':None,'metrics':None,'redecoded':False}
        raw_path = path.parent/'browser-result.json'
        raw = json.loads(raw_path.read_bytes()) if raw_path.exists() else {}
        if raw.get('status') == 'completed' and not raw['errors']:
            if raw['last']['elapsed_ms'] > original['seconds']*1000:
                raise ValueError('Saved native result exceeded its original budget')
            destination = output/path.parent.name
            destination.mkdir()
            request = json.loads((path.parent/'request.json').read_bytes())
            converted = layout(request['prepared'], groups_from_exports(raw['last']['svgs']))
            write(destination/'layout.json',converted)
            checked = subprocess.run([str(binary),'validate','--job',str(path.parent/'job.json'),'--layout',str(destination/'layout.json')],
                                     cwd=ROOT,capture_output=True,timeout=120)
            (destination/'validation.json').write_bytes(checked.stdout)
            validation = json.loads(checked.stdout)
            valid = checked.returncode == 0 and validation['valid']
            row.update(redecoded=True,status='valid' if valid else 'invalid',validation=validation,
                       validator_exit_code=checked.returncode,outputs={p.relative_to(ROOT).as_posix():digest(p) for p in destination.iterdir()})
            if valid:
                row.update(metrics=validation['metrics'],score=validation['metrics']['normalized_material'])
        elif original['status'] == 'valid':
            raise ValueError('Previously valid record lacks a completed native export')
        rows.append(row)
    checkpoint = {'recorded_at':stamp.isoformat(),'kind':'svgnest_export_decode_correction','scope':scope,
        'method':'native_svg_attributes_v2',
        'reason':'Chromium SVGMatrix rounded translations to float32. Decode original native SVG transform attributes at full Python float precision.',
        'search_rerun':False,'source_runs_modified':False,'decoder_sources':sources,
        'validator_binary_sha256':digest(binary),
        'validator_sources':{p.relative_to(ROOT).as_posix():digest(p) for p in [ROOT/'Cargo.lock',*sorted((ROOT/'crates/validator/src').glob('*.rs'))]},
        'rows':rows}
    write(output/'correction.json',checkpoint)
    stem = f'svgnest-correction-{identifier}'
    retained = ROOT/'benchmarks/results'/stem
    write(retained.with_suffix('.json'),checkpoint)
    lines = ['# SVGnest export precision correction','',scope,'',checkpoint['reason'],'',
             'Search was not rerun. Original run records and their outcomes remain unchanged. All selected native exports were revalidated, including previously valid ones.','',
             '| Original run | Job | Old outcome | Corrected outcome | Corrected material |','| --- | --- | --- | --- | ---: |']
    for row in rows:
        score = f'{row["score"]:.9f}' if row['score'] is not None else '—'
        lines.append(f'| {Path(row["source_record"]).parent.name} | {row["original"]["job"]} | {row["original"]["status"]} | {row["status"]} | {score} |')
    lines += ['',f'[Full precision, original records and independent correction evidence]({stem}.json).','']
    with retained.with_suffix('.md').open('x',encoding='utf-8',newline='\n') as file:file.write('\n'.join(lines))
    with (ROOT/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as file:
        file.write(f'\n- {stamp.isoformat()} | SVGnest output-decoder correction for all {len(rows)} selected records | '
                   f'[audit](benchmarks/results/{stem}.md). Native search unchanged, originals retained, full-precision SVG attributes revalidated. Provisional only.\n')
    print(json.dumps({'selected':len(rows),'redecoded':sum(r['redecoded'] for r in rows),'valid_after':sum(r['status']=='valid' for r in rows),'report':retained.with_suffix('.md').relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all',action='store_true',help='Every saved standard SVGnest run, including preparation failures')
    group.add_argument('--batch',type=Path,help='A complete selected batch with frozen original run hashes')
    args = parser.parse_args()
    if args.all:
        paths = [(p,digest(p)) for p in sorted((ROOT/'output/playwright/svgnest').glob('*/run.json'))]
        scope = 'All saved SVGnest preparation and pilot results. Mixed budgets/settings; this is an output-decoder audit, not a quality comparison.'
    else:
        batch = json.loads(args.batch.read_bytes())
        if not batch['complete'] or len(batch['runs']) != len(batch['cases']):
            raise ValueError('Batch is incomplete')
        paths = [(contained_file(ROOT,r['record']),r['sha256']) for r in batch['runs']]
        scope = f'Provisional {len(paths)}-case B batch {batch["batch_id"]}, {batch["seconds"]} s, seed {batch["seed"]}, {batch["settings"]}. Full M1 and quality gates remain pending.'
    if not paths:raise ValueError('No saved records selected')
    correct(paths,scope)
