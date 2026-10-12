# Reproducing the benchmark

One command rebuilds the datasets, runs every comparison that is missing and
writes the results table, chart and page (`web/public/results/`, published at
<https://skulitom.github.io/Nestbolt/results/>):

```sh
python scripts/reproduce.py --phase development
```

It runs four stages in order; `--only <stage>` picks one, `--dry-run` lists what
would run.

| Stage | What it does |
| --- | --- |
| `datasets` | Rebuilds the 48 academic jobs from the pinned OR-Datasets sources and the 40 maker jobs from their pinned generators (boxes.py, FreeSewing, Noto Sans, procedural parts, Openclipart), then checks every byte against the freeze and the frozen job/seed coverage. |
| `competitors` | Runs Deepnest (deepnest-next), SVGnest and the Sparrow CLI with the sealed settings in `benchmarks/final-settings.json` (identical constraints and each tool's own best settings) over every job, budget (60 s, and 300 s on the long subset) and seed of the phase. |
| `nestbolt` | Runs Nestbolt over the same jobs and seeds at 60 s and 300 s, plus 30 s on the long subset for the speed gate. |
| `report` | Aggregates per-job medians and quartiles, compares Nestbolt with the best competitor and with each tool, and writes `results.json`, `index.html` and its chart. |

Every attempt is checked by the independent validator (`crates/validator`) and
kept, including invalid, unsupported and failed ones; nothing is retried
automatically. A slot whose audited record already exists is reused, so the run
can be split across sessions. Runs are single-threaded, one per physical core,
at most eight at once.

## Phases

- **Development** uses seeds 0, 1 and 2 and leaves out the ten held-out maker
  jobs. All development competitor runs already exist in the repository's
  evidence, so a fresh run only adds what is missing.
- **Final** (`--phase final --final-acceptance`) uses fresh seeds 1000-1004 and
  includes the held-out jobs. Running Nestbolt on held-out jobs ends tuning, so it
  happens once, after the development results meet the gates.

Seeds are reserved per phase: development batches refuse final seeds and
held-out jobs, and the final phase refuses development seeds.

## Requirements

Rust (the repository selects 1.98.1), Python 3.11+ with `psutil` and
`matplotlib`, Node.js 24, and the tool setups: `python scripts/svgnest.py setup`,
`python scripts/deepnest.py setup` and `python scripts/sparrow_benchmark.py build`.
Deepnest opens Electron windows; on Windows they can run in a hidden desktop
(Artem's PC uses Anode) with `--tools deepnest`, and the other tools from a normal
shell. The full final matrix is about 2,700 competitor runs, roughly 115 CPU-hours.
