"""Profile the current WASM on two declared H4 development jobs, never a gate.

One isolated Chrome page calls the same WASM nest_job entry point, sampled by
CDP every millisecond. All processes use physical CCD0 CPU 8; jobs run serially.
Sampling and main-page execution make these diagnostic timings, not app/G5
measurements. Do not edit sources during the session.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import threading
import time

import psutil
from g5_browser import serve
from h2_import_audit import source_digest
from h4_quality import cases, check

ROOT = Path(__file__).resolve().parents[1]
CPU = 8


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')


def summarize(path):
    data = json.loads(path.read_bytes())
    nodes = {n['id']:n for n in data['nodes']}
    parent = {c:n['id'] for n in nodes.values() for c in n.get('children',[])}
    self_time, total_time = {}, {}
    for node, delta in zip(data['samples'],data['timeDeltas'],strict=True):
        self_time[node] = self_time.get(node,0)+delta
        while node in nodes:
            total_time[node] = total_time.get(node,0)+delta
            node = parent.get(node)
    elapsed = sum(data['timeDeltas'])
    rows = []
    for node in nodes.values():
        frame = node['callFrame']
        rows.append({'function':frame['functionName'],'url':frame.get('url',''),
            'line':frame.get('lineNumber'),'self_seconds':self_time.get(node['id'],0)/1e6,
            'inclusive_seconds':total_time.get(node['id'],0)/1e6,
            'self_percent':100*self_time.get(node['id'],0)/elapsed})
    return {'sampled_seconds':elapsed/1e6,'sample_count':len(data['samples']),
            'top_self':sorted(rows,key=lambda r:r['self_seconds'],reverse=True)[:45],
            'top_inclusive':sorted(rows,key=lambda r:r['inclusive_seconds'],reverse=True)[:45]}


def main():
    rows = [r for r in cases() if r['id'] in ['example-letters','m-public-gear-1']]
    assert len(rows)==2
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT/'benchmarks/results'/f'h4-browser-profile-{stamp}'
    out.mkdir()
    site = ROOT/'output'/out.name/'site'
    site.mkdir(parents=True)
    shutil.copytree(ROOT/'web/src/pkg',site/'pkg')
    (site/'index.html').write_text('''<!doctype html><script type="module">
import init, { nest_job, memory_bytes } from './pkg/nestbolt_wasm.js';
await init(); window.profileJob = nest_job; window.profileMemory = memory_bytes;
window.profileReady = true;
</script>''',encoding='utf-8',newline='\n')
    guarded = [Path(__file__),ROOT/'web/bench/profile.mjs',ROOT/'scripts/h4_quality.py',
               ROOT/'scripts/h6_material_cost.py',ROOT/'scripts/g5_browser.py',ROOT/'target/release/nestbolt.exe']
    guarded += [p for p in (site/'pkg').iterdir() if p.is_file()]
    guarded += [ROOT/r['path'] for r in rows]
    guarded += [ROOT/r[k] for r in rows for k in ['library','request'] if k in r]
    def guards():
        return {'product':source_digest(),'files':{p.relative_to(ROOT).as_posix():digest(p) for p in guarded}}
    before = guards()
    server = serve(site)
    jobs = []
    for row in rows:
        folder = out/row['id']
        folder.mkdir()
        jobs.append({'id':row['id'],'path':str(ROOT/row['path']),'out':str(folder)})
    plan = {'scope':__doc__,'url':f'http://127.0.0.1:{server.server_address[1]}/index.html',
        'seconds':60,'seed':0,'jobs':jobs,'info':str(out/'browser.json'),'cpu':CPU,'guards':before,
        'held_out_read':False,'gate_evidence':False}
    write(out/'plan.json',plan)
    print(out,flush=True)
    stop, deviations, observed = threading.Event(), [], {}
    with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
        command = [shutil.which('node'),str(ROOT/'web/bench/profile.mjs'),str(out/'plan.json')]
        process = subprocess.Popen(command,cwd=ROOT/'web',stdout=stdout,stderr=stderr,
                                   creationflags=subprocess.CREATE_NO_WINDOW|4)
        proc = psutil.Process(process.pid)
        proc.cpu_affinity([CPU]);proc.resume()
        def watch():
            while not stop.is_set():
                try:
                    children = [proc,*proc.children(recursive=True)]
                except psutil.Error:
                    children = []
                for child in children:
                    try:
                        affinity = child.cpu_affinity()
                        if affinity != [CPU]:
                            deviations.append({'pid':child.pid,'affinity':affinity})
                            child.cpu_affinity([CPU])
                        observed[child.pid] = child.name()
                    except psutil.Error:
                        pass
                stop.wait(.1)
        watcher = threading.Thread(target=watch,daemon=True);watcher.start()
        start = time.perf_counter()
        try:
            code = process.wait(timeout=360)
        except subprocess.TimeoutExpired:
            code = 'timeout'
            for child in reversed(proc.children(recursive=True)):
                try: child.kill()
                except psutil.Error: pass
            process.kill();process.wait()
        finally:
            stop.set();watcher.join();server.shutdown()
    write(out/'execution.json',{'command':command,'exit_code':code,'wall_seconds':time.perf_counter()-start,
        'affinity_deviations':deviations,'processes':observed})
    assert code == 0 and not deviations
    records = []
    for row in rows:
        folder = out/row['id']
        result = json.loads((folder/'result.json').read_bytes())
        validation = check(row,folder,CPU,result)
        profile = summarize(folder/'cpu.cpuprofile')
        write(folder/'profile-summary.json',profile)
        records.append({'job':row['id'],'validation':validation,'profile':profile})
    assert guards()==before
    write(out/'results.json',{'scope':__doc__,'rows':records,'guards_unchanged':True,'gate_evidence':False})
    print(json.dumps([{'job':r['job'],'top_self':r['profile']['top_self'][:6]} for r in records]),flush=True)


if __name__ == '__main__':
    main()
