"""Rebuild reviewed, pinned shop inputs without fetching source code.

The source lock records each file and its licence evidence. This is collection,
not the H1 freeze: labels and the held-out allocation are separate requirements.
No Nestbolt importer is called here.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'benchmarks/datasets/shop'
ALLOWED = {'CC0-1.0', 'CC-BY-3.0', 'CC-BY-4.0', 'CC-BY-SA-3.0',
           'CC-BY-SA-4.0', 'MIT', 'BSD-2-Clause', 'BSD-3-Clause',
           'Apache-2.0', 'Unlicense', 'CERN-OHL-P-2.0', 'public-domain'}


def digest(data):
    return sha256(data).hexdigest()


def destination(relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or '\\' in relative or ':' in relative:
        raise ValueError(f'Unsafe corpus path: {relative}')
    result = (CORPUS / path).resolve()
    if not result.is_relative_to(CORPUS.resolve()):
        raise ValueError(f'Path escapes corpus: {relative}')
    return result


def download(url):
    if not url.startswith('https://raw.githubusercontent.com/'):
        raise ValueError('Source lock must use immutable raw GitHub URLs')
    request = Request(url, headers={'User-Agent': 'Nestbolt licensed shop corpus'})
    with urlopen(request, timeout=60) as response:
        return response.read()


def restore(entry):
    path = destination(entry['path'])
    if path.exists():
        data = path.read_bytes()
    else:
        data = download(entry['download_url'])
    if digest(data) != entry['sha256']:
        raise ValueError(f'Checksum mismatch: {entry["path"]}')
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return entry['path']


def load_lock(path):
    lock = json.loads(path.read_text(encoding='utf-8'))
    seen = set()
    for source in lock['sources']:
        if source['licence'] not in ALLOWED:
            raise ValueError(f'Excluded licence: {source["licence"]}')
        revision = source['revision']
        if len(revision) != 40 or any(c not in '0123456789abcdef' for c in revision):
            raise ValueError('Sources must be pinned to a full revision')
        prefix = f'https://raw.githubusercontent.com/{source["repository"]}/{revision}/'
        for entry in [*source['evidence'], *source['files']]:
            destination(entry['path'])
            if entry['path'] in seen:
                raise ValueError(f'Duplicate destination: {entry["path"]}')
            seen.add(entry['path'])
            if not entry['download_url'].startswith(prefix):
                raise ValueError('Download URL does not match the pinned source')
        if not source['evidence'] or not source['review']:
            raise ValueError('Missing licence review')
    return lock


def attribution(lock):
    lines = ['# Shop corpus licences and attribution', '',
             'Source drawings retain the following licences. They are not relicensed',
             'under Nestbolt\'s MIT licence. Source bytes are unchanged. The source',
             'lock pins downloads and licence evidence; H1 is not yet frozen.', '',
             '## Original format probes', '',
             '`probes/geometry.svg` and LightBurn projects made from it are original',
             'Nestbolt test drawings under the repository MIT licence. Writer:',
             'LightBurn 2.1.01 in the hidden Anode desktop, 2026-10-13.', '']
    for source in lock['sources']:
        lines += [f'## {source["repository"]}', '',
                  f'Licence: **{source["licence"]}**. Attribution: {source["attribution"]}.', '',
                  f'Revision: `{source["revision"]}`. {source["review"]}', '']
        for evidence in source['evidence']:
            lines += [f'- [Licence evidence]({evidence["path"]}) ([upstream]({evidence["source_url"]})).']
        lines += ['', '| File | Original |', '| --- | --- |']
        lines += [f'| [{f["path"]}]({quote(f["path"])}) | [source]({f["source_url"]}) |'
                  for f in source['files']]
        lines += ['']
    native_manifest = CORPUS / 'native/manifest.json'
    if native_manifest.exists():
        lines += ['## Native LightBurn derivatives', '',
                  'These are modified test derivatives saved/exported by LightBurn 2.1.01',
                  'in the hidden Anode desktop. Each retains its source design licence.',
                  'Modifications: duplicate and reposition the source design, add an original',
                  'Nestbolt feature coupon (text, shared bitmaps, score/engrave layers, kerf,',
                  'lead settings and a start point), then save/export. The original MIT',
                  'coupon is included under each derivative\'s stated licence.',
                  'The [recipe](native/recipe.json) and [native manifest](native/manifest.json)',
                  'record sources, modifications, writer evidence and hashes.', '',
                  '| File | Licence | Original / attribution |', '| --- | --- | --- |']
        for row in json.loads(native_manifest.read_text(encoding='utf-8'))['files']:
            source = f'[{row["derived_from"]}]({quote(row["derived_from"])}) — author notices in its source section above' if row.get('derived_from') else 'Original Nestbolt test geometry; repository MIT notice'
            lines.append(f'| [{row["path"]}]({quote(row["path"])}) | {row["licence"]} | {source} |')
        lines += ['']
    generated_manifest = CORPUS / 'generated/manifest.json'
    if generated_manifest.exists():
        generated = json.loads(generated_manifest.read_text(encoding='utf-8'))
        lines += ['## Original generated shop habits', '',
                  'All ten clean bases and 170 generated DXFs are **MIT**, copyright Nestbolt',
                  'contributors, under the repository LICENSE. They derive only from original',
                  'Nestbolt examples and the non-held-out procedural maker geometry.',
                  'The [generated manifest](generated/manifest.json) records each source path,',
                  'source hash, selected element, transformation, label and generator seed.', '',
                  '| Clean base | Original source |', '| --- | --- |']
        for b in generated['bases']:
            lines.append(f'| [{b["path"]}]({b["path"]}) | `{b["source"]}`: {", ".join(b["source_elements"])} |')
        lines += ['', '| Generated DXF (MIT) | Clean base | Label |', '| --- | --- | --- |']
        for row in generated['files']:
            lines.append(f'| [{row["path"]}]({row["path"]}) | {row["base"]} | [{row["label"]}]({row["label"]}) |')
        lines += ['']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path, default=CORPUS / 'sources.lock.json')
    parser.add_argument('--check', action='store_true', help='Verify local bytes without downloading')
    args = parser.parse_args()
    lock = load_lock(args.lock)
    entries = [entry for s in lock['sources'] for entry in [*s['evidence'], *s['files']]]
    if args.check:
        for entry in entries:
            if digest(destination(entry['path']).read_bytes()) != entry['sha256']:
                raise ValueError(f'Checksum mismatch: {entry["path"]}')
    else:
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(restore, entries))
        (CORPUS / 'LICENSES.md').write_text(attribution(lock), encoding='utf-8', newline='\n')
    print(json.dumps({'sources': len(lock['sources']),
                      'files': sum(len(s['files']) for s in lock['sources']),
                      'verified_entries': len(entries), 'h1_frozen': False}))


if __name__ == '__main__':
    main()
