"""Retain the final M0 table only after all frozen runs and geometry checks pass."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

import m0
from m0_reference import digest


def summarize(experiment):
    integrity = m0.report(argparse.Namespace(experiment=experiment))
    if not integrity['complete'] or not integrity['pass']:
        raise ValueError('M0 is incomplete or fails the unchanged published-quality threshold')
    root = m0.ROOT/'output/m0'/experiment
    metadata = json.loads((root/'experiment.json').read_bytes())
    reference = json.loads(m0.MANIFEST.read_bytes())
    if metadata['smoke'] or metadata['seconds'] != 1200:
        raise ValueError('Only the frozen full-budget reproduction can establish M0')
    for name, checksum in metadata['source_hashes'].items():
        if digest(m0.ROOT/name) != checksum:
            raise ValueError(f'Historical runner changed: {name}')
    runs = []
    for instance in reference['instances']:
        for index in reference['method']['run_indices']:
            path = root/f'{instance["name"]}-{index}'
            run = json.loads((path/'run.json').read_bytes())
            validations = list(path.glob('validation-*.json'))
            if not validations:
                raise ValueError(f'Missing independent validation: {path.name}')
            vp = max(validations,key=lambda p:json.loads(p.read_bytes())['validated_at'])
            validation = json.loads(vp.read_bytes())
            if (not validation['valid'] or validation['exit_code'] != 0 or not validation['report']['valid']
                    or validation['input_sha256'] != run['input_sha256']
                    or validation['layout_sha256'] != run['outputs']['output/layout.json']):
                raise ValueError(f'Independent original-geometry check failed or changed: {path.name}')
            runs.append({'instance':instance['name'],'run':run,'run_sha256':digest(path/'run.json'),
                         'independent_validation':validation,'validation_sha256':digest(vp)})
    if len(runs) != 39 or len(integrity['rows']) != 13:
        raise ValueError('Expected exactly 39 frozen runs and 13 instance comparisons')
    stamp = datetime.now(timezone.utc)
    name = f'm0-published-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    target = m0.ROOT/'benchmarks/results'/name
    proof = {'recorded_at':stamp.isoformat(),'milestone':'M0','milestone_pass':True,
        'scope':'39-run native quality reproduction: the three predeclared seeds for every instance, compared with all 100 archived lengths per instance. This is not a full statistical replication, Nestbolt optimiser result, or G1-G8 pass.',
        'summary_source_sha256':digest(Path(__file__)), 'experiment':metadata,
        'reference_sha256':digest(m0.MANIFEST),'integrity_report':integrity,'runs':runs}
    m0.write_new(target.with_suffix('.json'),proof)
    lines = ['# M0: published Sparrow reproduction', '',
        '**Pass: all 13 instance means are within 1% of the published archive means.**', '',
        'All 39 predeclared 1,200-second runs finished and passed the independent original-polygon checker. No failed or incomplete attempt was discarded.', '',
        proof['scope'], '',
        '| Instance | Published mean length | Native three-seed mean | Difference |',
        '| --- | ---: | ---: | ---: |']
    for row in integrity['rows']:
        lines.append(f"| {row['instance']} | {row['reference_mean_width']:.8f} | {row['mean_width']:.8f} | {row['relative_difference']:+.3%} |")
    lines.extend(['',
        'Historical Sparrow 0.1.0 and jagua-rs 0.6.2 are unmodified. This run uses native Windows on the Ryzen 9 7950X3D, three workers per instance and the frozen nightly-2025-06-14 toolchain. The paper used a Ryzen 9 7950X under WSL2. Time-limited searches do not promise identical layouts.', '',
        'The historical dependency lock is reconstructed, not the missing original lock. Six original inputs retain the paper’s 0.01% strip-height inflation; the reported length metric requires no adjustment. SHAPES2 is the source named blaz1.', '',
        f'[All records, validation evidence, hashes and full precision]({name}.json).',
        '[Frozen reproduction method](../sparrow-repro/README.md).', '',
        'M0 contributes 5% of the project’s milestone weighting. The sheet optimiser, full baseline, browser, import/export, MCP and final quality gates remain separate work.', ''])
    with target.with_suffix('.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines))
    m0.append_log(f'- {stamp.isoformat()} | M0 published reproduction PASS: 39/39 independently valid runs, 13/13 complete means within 1%; [table](benchmarks/results/{name}.md). Historical native quality reproduction only; M1-M5 and G1-G8 remain pending.')
    print(target.with_suffix('.md'))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment',required=True)
    summarize(parser.parse_args().experiment)
