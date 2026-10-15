"""Compare thin versus fat LTO without changing production build settings.

One declared compiler lever, eleven H4 development jobs, seed 0, 60 seconds.
Both real browsers, one fresh worker per job, eight physical CCD0 cores.
This is a pilot, never H4 gate evidence. Retain every outcome and restore the
original generated bindings after building the isolated candidate site.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time

from g5_browser import serve
from h2_import_audit import source_digest
from h4_quality import browser, cases

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix():digest(p) for p in sorted(root.rglob('*')) if p.is_file()}


def write(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-only',action='store_true')
    parser.add_argument('--prepared',type=Path)
    args = parser.parse_args()
    rows = cases()
    if args.prepared:
        out = args.prepared.resolve()
        assert out.is_relative_to(ROOT/'benchmarks/results')
        plan = json.loads((out/'plan.json').read_bytes())
    else:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        out = ROOT/'benchmarks/results'/f'h4-lto-probe-{stamp}'
        out.mkdir()
        build = ROOT/'output'/out.name
        build.mkdir()
        baseline, candidate = build/'site-thin',build/'site-fat'
        original_bindings = ROOT/'web/src/pkg'
        backup = build/'bindings-thin'
        shutil.copytree(ROOT/'web/dist',baseline)
        shutil.copytree(original_bindings,backup)
        plan = {'scope':__doc__,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'product_digest':source_digest(),'cases':rows,'seconds':60,'seed':0,'concurrency':8,
            'schedule':[['chrome','thin'],['chrome','fat'],['firefox','fat'],['firefox','thin']],
            'native_cli_sha256':digest(ROOT/'target/release/nestbolt.exe'),
            'baseline_bindings':inventory(original_bindings),'baseline_site':inventory(baseline),
            'build_directory':str(build),'sites':{'thin':str(baseline),'fat':str(candidate)},
            'build_environment':{'CARGO_PROFILE_RELEASE_LTO':'fat','CARGO_TARGET_DIR':str(ROOT/'.cache/h4-fat-lto-target')},
            'builds_cpu_affinity':list(range(16,32)),'measurement_cpu_affinity':list(range(0,16,2)),
            'held_out_read':False,'H4':False,'production_build_changed':False}
        write(out/'plan.json',plan)
        env = os.environ.copy()
        assert not env.get('RUSTFLAGS') and not env.get('CARGO_ENCODED_RUSTFLAGS')
        env.update(plan['build_environment'])
        commands = [(['cargo','build','--locked','--release','-p','nestbolt-wasm','--target','wasm32-unknown-unknown'],ROOT,env),
            (['wasm-bindgen','--target','web','--out-dir',str(build/'bindings-fat'),
              str(ROOT/'.cache/h4-fat-lto-target/wasm32-unknown-unknown/release/nestbolt_wasm.wasm')],ROOT,None)]
        records = []
        try:
            for index,(command,cwd,environment) in enumerate(commands):
                start = time.perf_counter()
                with (out/f'build-{index}.log').open('wb') as log:
                    done = subprocess.run(command,cwd=cwd,env=environment,stdout=log,stderr=subprocess.STDOUT)
                records.append({'command':command,'exit_code':done.returncode,'wall_seconds':time.perf_counter()-start})
                write(out/'build.json',records)
                assert done.returncode == 0, records[-1]
            # Only replace generated package files, never repository source.
            generated = [p for p in (build/'bindings-fat').iterdir() if p.is_file()]
            assert all(p.name.startswith('nestbolt_wasm') for p in generated)
            for p in generated:
                shutil.copyfile(p,original_bindings/p.name)
            command = [shutil.which('node'),str(ROOT/'web/node_modules/vite/bin/vite.js'),
                       'build','--outDir',str(candidate),'--emptyOutDir']
            start = time.perf_counter()
            with (out/'build-site.log').open('wb') as log:
                done = subprocess.run(command,cwd=ROOT/'web',stdout=log,stderr=subprocess.STDOUT)
            records.append({'command':command,'exit_code':done.returncode,'wall_seconds':time.perf_counter()-start})
            write(out/'build.json',records)
            assert done.returncode == 0
        finally:
            for p in backup.rglob('*'):
                if p.is_file():
                    shutil.copyfile(p,original_bindings/p.relative_to(backup))
            assert inventory(original_bindings) == plan['baseline_bindings']
        assert source_digest() == plan['product_digest']
        assert inventory(ROOT/'web/dist') == plan['baseline_site']
        plan['candidate_site'] = inventory(candidate)
        plan['candidate_bindings'] = inventory(build/'bindings-fat')
        plan['compiler'] = subprocess.check_output(['rustc','--version'],text=True).strip()
        plan['bindgen'] = subprocess.check_output(['wasm-bindgen','--version'],text=True).strip()
        write(out/'plan.json',plan)
        print(out,flush=True)
        if args.build_only:
            return

    def guards():
        assert source_digest() == plan['product_digest']
        assert digest(ROOT/'target/release/nestbolt.exe') == plan['native_cli_sha256']
        assert inventory(ROOT/'web/src/pkg') == plan['baseline_bindings']
        assert inventory(ROOT/'web/dist') == plan['baseline_site']
        for variant in ['thin','fat']:
            assert inventory(Path(plan['sites'][variant])) == plan['baseline_site' if variant=='thin' else 'candidate_site']
        for row in rows:
            assert digest(ROOT/row['path']) == row['sha256']
    guards()
    assert rows == plan['cases']
    scripts = [Path(__file__),ROOT/'scripts/h4_quality.py',ROOT/'web/bench/run.mjs']
    script_hashes = {p.relative_to(ROOT).as_posix():digest(p) for p in scripts}
    with (out/'opened.json').open('x',encoding='utf-8',newline='\n') as marker:
        marker.write(json.dumps({'plan_sha256':digest(out/'plan.json'),'scripts':script_hashes})+'\n')
    results = {}
    for engine,variant in plan['schedule']:
        guards()
        assert script_hashes == {p.relative_to(ROOT).as_posix():digest(p) for p in scripts}
        server = serve(Path(plan['sites'][variant]))
        try:
            batch = browser(engine,0,rows,argparse.Namespace(seconds=60,concurrency=8),out/variant,
                            f'http://127.0.0.1:{server.server_address[1]}/bench.html')
        finally:
            server.shutdown()
        results[f'{engine}-{variant}'] = batch
        write(out/'progress.json',{k:{'done':len(v),'valid':sum(r['status']=='valid' for r in v)} for k,v in results.items()})
        print(engine,variant,'valid',sum(r['status']=='valid' for r in batch),'/',len(batch),flush=True)
    guards()
    comparisons = {}
    for engine in ['chrome','firefox']:
        pairs = []
        for row in rows:
            saved = {}
            for variant in ['thin','fat']:
                result_path = out/variant/engine/'s0'/row['id']/'result.json'
                record = next(r for r in results[f'{engine}-{variant}'] if r['job']==row['id'])
                saved[variant] = {'record':record,'raw':json.loads(result_path.read_bytes()) if result_path.exists() else None}
            valid = all(v['record']['status']=='valid' for v in saved.values())
            pairs.append({'job':row['id'],'both_valid':valid,
                'material_change_percent':100*(saved['fat']['record']['material']/saved['thin']['record']['material']-1) if valid else None,
                'work_rate_change_percent':100*((saved['fat']['raw']['work']/saved['fat']['raw']['elapsed_seconds'])/
                    (saved['thin']['raw']['work']/saved['thin']['raw']['elapsed_seconds'])-1) if valid else None,
                'memory_change_bytes':saved['fat']['raw']['memory_bytes']-saved['thin']['raw']['memory_bytes'] if valid else None})
        complete = all(r['both_valid'] for r in pairs)
        comparisons[engine] = {'pairs':pairs,'all_valid':complete,
            'median_material_change_percent':statistics.median(r['material_change_percent'] for r in pairs) if complete else None,
            'median_work_rate_change_percent':statistics.median(r['work_rate_change_percent'] for r in pairs) if complete else None}
    write(out/'results.json',{'scope':__doc__,'plan_sha256':digest(out/'plan.json'),'scripts':script_hashes,
        'records':results,'comparisons':comparisons,'guards_unchanged':True,'H4':False,'production_build_changed':False})
    print(json.dumps(comparisons),flush=True)


if __name__ == '__main__':
    main()
