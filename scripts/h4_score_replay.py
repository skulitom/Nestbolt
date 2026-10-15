"""Equal-work development replay for collision-score pruning; never quality gates.

Letters and gear-1, seeds 0/1, 20 work seconds with a 120-second hard limit.
Validate all originals and compare exact layouts, counters and metric values.
Wall times are diagnostic only. Use the unmodified reference binary first.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from queue import Queue
import traceback

from h2_import_audit import source_digest
from h4_quality import cases, check
from h6_material_cost import run

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary',type=Path,required=True)
    parser.add_argument('--reference',type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    rows = [r for r in cases() if r['id'] in ['example-letters','m-public-gear-1']]
    assert len(rows)==2
    out = ROOT/'benchmarks/results'/('h4-score-replay-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    out.mkdir()
    paths = [binary,Path(__file__),ROOT/'scripts/h4_quality.py',ROOT/'scripts/h6_material_cost.py']
    paths += [ROOT/r['path'] for r in rows]
    def guards():
        return {'product':source_digest(),'files':{str(p.relative_to(ROOT)):digest(p) for p in paths}}
    before = guards()
    write(out/'plan.json',{'scope':__doc__,'guards':before,'cases':rows,'seeds':[0,1],
        'seconds':20,'timing':'work','time_limit':120,'cpus':[8,10],
        'reference':str(args.reference) if args.reference else None,'held_out_read':False})
    print(out,flush=True)
    cpus = Queue()
    for cpu in [8,10]:cpus.put(cpu)
    def one(pair):
        row,seed = pair
        cpu = cpus.get()
        folder = out/f's{seed}'/row['id'];folder.mkdir(parents=True)
        record = {'job':row['id'],'seed':seed,'passed':False,'directory':folder.relative_to(ROOT).as_posix()}
        try:
            record['run'] = run([binary,'sheets','--job',ROOT/row['path'],'--output',folder/'layout.json',
                '--seconds',20,'--seed',seed,'--repeatable','--time-limit',120],folder,'search',cpu,150)
            assert record['run']['exit_code']==0
            result = json.loads((folder/'search-stdout.json').read_bytes())
            assert result['repeatable'], 'Reached wall deadline instead of work budget'
            record['validation'] = check(row,folder,cpu,result)
            record['counts'] = result['counts']
            record['work'] = result['work']
            record['stats'] = result['stats']
            record['metrics'] = result['validation']['metrics']
            if args.reference:
                prior = args.reference/f's{seed}'/row['id']
                original = json.loads((prior/'search-stdout.json').read_bytes())
                assert json.loads((prior/'layout.json').read_bytes()) == json.loads((folder/'layout.json').read_bytes())
                assert all(original[k]==result[k] for k in ['counts','work','stats','history','validation','repeatable'])
                record['identical_layout_counters_history_validation'] = True
            record['passed'] = True
        except Exception:
            record['error'] = traceback.format_exc()
        finally:
            cpus.put(cpu)
        write(folder/'case.json',record)
        print(row['id'],seed,record['passed'],flush=True)
        return record
    with ThreadPoolExecutor(2) as pool:
        results = list(pool.map(one,[(r,s) for s in [0,1] for r in rows]))
    assert guards()==before
    write(out/'results.json',{'scope':__doc__,'rows':results,'all_passed':all(r['passed'] for r in results),
        'guards_unchanged':True,'gate_evidence':False})
    assert all(r['passed'] for r in results)


if __name__ == '__main__':
    main()
