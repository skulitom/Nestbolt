"""Verify original per-attempt archives and report the descriptive H5 pilot."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import psutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h5-return-frame-pilot-20261017'
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'output'))
import h5_return_frame_pilot as pilot
load,write,digest=pilot.load,pilot.write,pilot.digest
result=load(OUT/'results.json')
plan=load(OUT/'plan.json')
opened=load(OUT/'opened.json')
assert not psutil.pid_exists(opened['pid']) or not any('h5_return_frame_pilot.py' in p for p in psutil.Process(opened['pid']).cmdline())
assert result['guards_unchanged'] and pilot.guards()==plan['guards']
assert digest(OUT/'plan.json')==opened['plan_sha256']
assert subprocess.check_output(['git','show','HEAD:'+(OUT/'plan.json').relative_to(ROOT).as_posix()],cwd=ROOT)==(OUT/'plan.json').read_bytes()
summary=pilot.summarize(result['records'])
assert json.loads(json.dumps(summary))==result['summary'] and summary['coverage_complete']
assert result['wall_seconds']<3600
archives=[]
for row in result['records']:
    archive=OUT/row['archive']
    assert digest(archive)==row['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        assert case=={k:v for k,v in row.items() if k not in ['archive','archive_sha256']}
        assert set(z.namelist())==set(case['artifacts'])|{'case.json'}
        for name,expected in case['artifacts'].items():assert sha256(z.read(name)).hexdigest()==expected
        if row['status']=='valid':
            search=json.loads(z.read('nested/search.json'))
            checked=json.loads(z.read('validate-stdout.json'))
            assert checked['valid'] and search['validation']['valid']
            pilot.equivalent(checked['metrics'],search['validation']['metrics'])
            assert checked['metrics']==row['metrics'] and checked['metrics']['normalized_material']==row['material']
            job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
            assert len(layout['placements'])==sum(p['quantity'] for p in job['parts'])
            assert row['search']['exit_code']==row['validation']['exit_code']==row['export']['exit_code']==0
            assert search['stats']==row['stats'] and search['riders']==row['riders']
            assert sha256(z.read('nested/layout.json')).hexdigest()==row['layout_sha256']
            if row['arm']!='normal':
                assert row['riders']==0
                before=sum(r['cut_length_without_common_mm'] for r in checked['common_line'])
                after=sum(r['cut_length_with_common_mm'] for r in checked['common_line'])
                assert before==row['cut_without_common_mm'] and after==row['cut_with_common_mm']
                assert row['saved_fraction']==1-after/before
        archives.append({'path':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'members':len(z.namelist())})
write(OUT/'verification.json',{'all_original_archives_verified':True,'archives':archives,
    'attempts':len(result['records']),'valid':sum(r['status']=='valid' for r in result['records']),
    'summary_recomputed':True,'production_and_observer_guards_unchanged':True,'H5_complete':False,'integrated':False})
shutil.copyfile(__file__,OUT/'finish.py')
lines=['# Reciprocal return-frame common-line exchange pilot — 2026-10-17','',
    f"**{sum(r['status']=='valid' for r in result['records'])}/{len(result['records'])} attempts are valid.**",
    'This four-job diagnostic does not complete H5. The full 13-job comparison',
    'remains required, and no original acceptance limit changes. This pilot',
    'earns no completed H5 milestone weight.','',
    '[Committed reciprocal return-frame plan](h5-return-frame-pilot-20261017/plan.json),',
    '[all results](h5-return-frame-pilot-20261017/results.json),',
    '[archive verification](h5-return-frame-pilot-20261017/verification.json).','',
    '## Method','',
    'The isolated candidate exchanges a last-sheet part with an actual',
    'obstruction set of up to three parts on an earlier sheet, repairs both sheets,',
    'and accepts only after',
    'the independent whole-job geometry/material guard passes. It keeps the',
    'incumbent intact on failure. The call now runs at the first feasible window',
    'before fill can short-circuit relocation, sharing the existing ten-percent',
    'budget and capped at 1.2 seconds. Ordinary mode retains its original path.',
    'Both matched arms include the current aba989e collision-tree depth change.',
    'Complete two/three-blocker sets are eligible regardless of combined part area,',
    'mapping complete return groups into the reciprocal incoming frame when every',
    'member permits the resulting orientation, otherwise retaining translation.',
    'It preserves relative transforms and the original smaller single-part',
    'fallbacks. It changes neither budget nor coefficients. Production is unchanged.',
    'Source, tests and matched observers are retained in the',
    '[preparation evidence](h5-return-frame-preparation-20261017.md).','',
    'Each job/kerf/seed block runs ordinary baseline, common-line baseline and',
    'common-line candidate sequentially on the same physical CCD0 core. Order',
    'rotates; seeds are 0–2, both kerfs are tested, every search gets 60 seconds,',
    'and at most eight blocks run together. Original frozen geometry, quantities,',
    'stocks and rotations are unchanged. Independent validation, public export',
    'and the ban on part-in-hole in common mode are required for a valid outcome.',
    f"The complete session took {result['wall_seconds']/60:.3f} minutes.",'',
    '## Three-seed medians','',
    'Positive material differences are worse. The candidate must remain within',
    '+1% of ordinary mode; improving over a failing common-line baseline alone',
    'does not pass that condition. Exchange counts sum all three seeds.','',
    '| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs common baseline | Candidate cut saving | Exchanges / attempts | Within +1% |',
    '| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
for pair in summary['pairs']:
    if not pair['complete']:
        lines.append(f"| {pair['job']} | {pair['kerf_mm']} | incomplete | incomplete | incomplete | incomplete | incomplete | no |")
        continue
    candidate=pair['arms']['candidate']
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {pair['baseline_vs_normal_percent']:+.6f}% | {pair['candidate_vs_normal_percent']:+.6f}% | {pair['candidate_vs_baseline_percent']:+.6f}% | {candidate['cut_savings_median_percent']:.6f}% | {candidate['exchanges']} / {candidate['exchange_attempts']} | {'yes' if pair['candidate_within_original_material_limit'] else 'NO'} |")
lines += ['', '## Evidence and limits','',
    'Every attempted outcome, including failures, has its own immutable ZIP.',
    'CRC, all member hashes, layout hashes, saved counters and independently',
    'computed metrics/cut savings were checked; the summary is recomputed from',
    'all original records. No valid-only median replaces a failed/incomplete arm.',
    'Source, binary, runner, data and environment guards remain unchanged.','',
    'The [earlier complete-set pilot](h5-complete-set-pilot-20261017.md)',
    'remains preserved with all 72 valid outcomes and four failed material pairs.',
    '[Four diagnostic traces](h5-complete-stage-diagnosis-20261017.md) observed',
    '23 complete sets repair the receiving sheet, then fail return-sheet repair.',
    'Those traces did not include poses and do not prove a rotation cause.',
    'A separate authored witness, strict-material rejection test and successful',
    'fixed-envelope exchange motivate this initialization experiment. The',
    'original compile and test failures remain in preparation evidence.',
    'No quality/material limit changes, and no isolated candidate is automatically integrated.',
    'H2/H5 remain open; completed milestone weight is 60%.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'all_valid':summary['all_valid'],'pairs':[{k:v for k,v in p.items() if k not in ['arms','per_seed']} for p in summary['pairs']]}))
