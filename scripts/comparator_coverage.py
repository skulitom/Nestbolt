"""Inspect development-job adapter coverage without running any optimiser."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import uuid

from benchmark_io import UnsupportedJob, jagua_input
from deepnest_io import prepare as deepnest
from sparrow_io import prepare as sparrow
from stock_inputs import prepare_stocks
from svgnest import ROOT, digest, write
from svgnest_io import prepare as svgnest


def main():
    subprocess.run(['python', 'scripts/matrix_plan.py', '--check'], cwd=ROOT, check=True)
    plan_path = ROOT/'benchmarks/matrix-plan.json'
    plan = json.loads(plan_path.read_bytes())
    settings = {tool:json.loads((ROOT/f'benchmarks/{tool}/tool.json').read_bytes())['settings']['identical']
                for tool in ['deepnest','svgnest']}
    stamp = datetime.now(timezone.utc)
    stem = f'comparator-coverage-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    evidence = ROOT/'output'/stem
    evidence.mkdir(parents=True)
    sources = {p.relative_to(ROOT).as_posix():digest(p) for p in [
        Path(__file__).resolve(), ROOT/'scripts/deepnest_io.py', ROOT/'scripts/svgnest_io.py',
        ROOT/'scripts/benchmark_io.py', ROOT/'scripts/sparrow_io.py', ROOT/'scripts/stock_inputs.py',
        ROOT/'crates/validator/examples/stock_adapter.rs', ROOT/'benchmarks/deepnest/tool.json',
        ROOT/'benchmarks/svgnest/tool.json']}
    rows = []
    for case in plan['cases']:
        if case['held_out'] or case['set'] == 'S':
            continue
        path = ROOT/'benchmarks/datasets'/case['path']
        if digest(path) != case['sha256']:
            raise ValueError('Frozen job changed')
        job = json.loads(path.read_bytes())
        outcomes = {}
        for tool in ['lbf','svgnest','deepnest','sparrow']:
            try:
                if tool == 'lbf':
                    jagua_input(job)
                elif tool == 'svgnest':
                    svgnest(job,settings[tool],'y')
                elif tool == 'sparrow':
                    sparrow(job,'y')
                else:
                    stocks = None
                    if any(s['outline'] or s['defects'] for s in job['stocks']):
                        stocks,proof = prepare_stocks(path,job['clearance'],evidence/f'{case["id"]}-stock.json')
                        write(evidence/f'{case["id"]}-stock-proof.json',proof)
                    deepnest(job,settings[tool],'y',stocks)
                outcomes[tool] = {'status':'prepared_for_native_trial'}
            except UnsupportedJob as error:
                outcomes[tool] = {'status':'unsupported_by_current_adapter','reason':str(error)}
            except Exception as error:
                outcomes[tool] = {'status':'preparation_failed','reason':str(error)}
        rows.append({'job':case['id'],'set':case['set'],'job_sha256':case['sha256'],'tools':outcomes})
    if any(digest(ROOT/name) != checksum for name,checksum in sources.items()):
        raise ValueError('Adapter changed during coverage inspection')
    summary = {tool:{group:sum(row['tools'][tool]['status']=='prepared_for_native_trial'
                              for row in rows if row['set']==group) for group in ['B','M']}
               for tool in ['lbf','svgnest','deepnest','sparrow']}
    result = {'recorded_at':stamp.isoformat(),'scope':'Development-only static input preparation: 35 B and 30 M. No optimiser was run. Prepared inputs do not prove native parsing, feasibility, validity, quality or performance. Ten held-out jobs are excluded.',
              'matrix_plan_sha256':digest(plan_path),'sources':sources,'summary':summary,'rows':rows,
              'stock_evidence':{p.relative_to(ROOT).as_posix():digest(p) for p in evidence.iterdir()}}
    target = ROOT/'benchmarks/results'/stem
    write(target.with_suffix('.json'),result)
    lines = ['# Comparator input coverage', '', result['scope'], '',
             '| Tool | B inputs prepared / 35 | Development M inputs prepared / 30 |',
             '| --- | ---: | ---: |']
    for tool,counts in summary.items(): lines.append(f'| {tool} | {counts["B"]} | {counts["M"]} |')
    lines.extend(['',f'[Every outcome, reason and source checksum]({stem}.json).',''])
    with target.with_suffix('.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines))
    print(json.dumps(summary))
    print(target.with_suffix('.md'))


if __name__ == '__main__':
    main()
