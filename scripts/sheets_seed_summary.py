"""Three-seed development summary of `nestbolt sheets` batches, G2-style.

For each development job, the Nestbolt median over the given batches (one seed
each) is compared with the frozen M1 three-seed competitor median at the same
budget. A failed or missing seed makes the job's median a failure, as in the
statistics policy. Development evidence only: no held-out jobs or final seeds.
"""
import argparse
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT/'benchmarks/results/baseline-gap-20261012T033547Z-e9539412.json'
TARGET = json.loads((ROOT/'benchmarks/baseline-target.json').read_bytes())
TIE = 0.000001


def median_with_failures(values):
    """Failures (None) rank after every score, as in STATISTICS.md."""
    ranked = sorted(v for v in values if v is not None) + [None] * sum(v is None for v in values)
    n = len(ranked)
    if n < 3:
        return None
    rank = (n - 1) * 0.5
    lo, hi = int(rank), min(int(rank) + 1, n - 1)
    if ranked[lo] is None or ranked[hi] is None:
        return None
    return ranked[lo] + (ranked[hi] - ranked[lo]) * (rank - lo)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batches', nargs='+', type=Path)
    parser.add_argument('--seconds', type=int, choices=[60, 300], default=60)
    args = parser.parse_args()
    runs = {}
    seeds = []
    for path in args.batches:
        data = json.loads(path.read_bytes())
        seeds.append(data['seed'])
        for row in data['rows']:
            runs.setdefault(row['job'], []).append(row.get('material') if row['status'] == 'valid' else None)
    if len(set(seeds)) != len(seeds):
        parser.error('each batch must use a different seed')
    competitors = {r['job']: r['competitor']['median'] for r in json.loads(BASELINE.read_bytes())['rows']
                   if r['seconds'] == args.seconds and r.get('competitor')}
    rows = []
    for job, values in sorted(runs.items()):
        ours = median_with_failures(values) if len(values) == len(seeds) else None
        c = competitors.get(job)
        if c is None:
            rows.append((job, ours, None, None, 'no finite competitor'))
            continue
        if ours is None:
            rows.append((job, None, c, None, 'failed or missing seed'))
            continue
        outcome = 'tie' if abs(ours - c) <= TIE * c else ('win' if ours < c else 'loss')
        rows.append((job, ours, c, 100 * (1 - ours / c), outcome))
    compared = [r for r in rows if r[3] is not None]
    reductions = [r[3] for r in compared]
    wins = sum(r[4] != 'loss' for r in compared)
    worse = sum(r[2] is not None and r[1] / r[2] > 1.01 for r in compared)
    print(f'seeds {sorted(seeds)}; {args.seconds} s references; target {TARGET["target_percent"]:.4f}%')
    print(f'compared {len(compared)}; wins/ties {wins} ({100 * wins / len(compared):.1f}%); '
          f'more than 1% worse {worse}; median reduction {statistics.median(reductions):.4f}%')
    print(f'all seeds valid: {all(v is not None for vs in runs.values() for v in vs)}')
    for job, ours, c, red, outcome in rows:
        if outcome == 'loss' or (red is not None and red < 2):
            print(f'  {job:32} ours {ours:.4f} competitor {c:.4f} reduction {red:+.3f}% {outcome}')


if __name__ == '__main__':
    main()
