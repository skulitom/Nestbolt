# M1 baseline complete — 2026-10-12

All 1,878 declared development comparison slots are audited. The full
[baseline table](../benchmarks/results/baseline-gap-20261012T033547Z-e9539412.md)
sets the G2 median material-reduction target to **10.77231473513936%**.
This establishes the baseline, not a Nestbolt quality or speed result.

| Requirement | Evidence |
| --- | --- |
| Independent validator | [Original-geometry contract and tests](VALIDATION.md), [material scoring](SCORING.md); all four output adapters use this checker |
| Frozen datasets S/B/M | [13 S and 35 B jobs](../benchmarks/datasets/README.md), [40 maker jobs](../benchmarks/makers/README.md), ten maker holdouts excluded from all tuning |
| Automated runners | [LBF](../benchmarks/lbf/README.md), [SVGnest](../benchmarks/svgnest/README.md), [Deepnest](../benchmarks/deepnest/README.md), [Sparrow](../benchmarks/sparrow-benchmark/README.md); bounded runs with retained versions, inputs, settings and outputs |
| Complete three-seed comparisons | 27 selected tables, both declared settings and both budgets; every selection and checksum is in the [frozen target](../benchmarks/baseline-target.json) |
| Measured gap | Every available competitor compared with LBF; failure-valued medians and missing finite comparisons remain explicit |

| Tool | Declared slots | Valid | Invalid | No layout | Timed out | Unsupported |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LBF | 450 | 283 | 5 | 0 | 0 | 162 |
| SVGnest | 450 | 225 | 23 | 170 | 2 | 30 |
| Deepnest | 450 | 330 | 30 | 88 | 2 | 0 |
| Sparrow | 528 | 127 | 43 | 0 | 0 | 358 |

The slot counts include documented structural non-applicability; they do not
claim that 1,878 solver processes ran. Sparrow also covers the strip population.
Earlier harness faults and their explicitly audited replacements remain in the
reports and [append-only log](../BENCHMARKS.md); native failures were not rerun
to obtain a better score.

| Budget | Development B/M jobs | Finite competitor/LBF pairs | No finite competitor | No finite LBF | Median competitor reduction vs LBF |
| --- | ---: | ---: | ---: | ---: | ---: |
| 60 s | 65 | 38 | 13 | 14 | 17.09055736% |
| 300 s | 10 | 6 | 1 | 3 | 21.54462947% |

The [policy fixed before search implementation](../benchmarks/STATISTICS.md)
sets the target to `max(5, 0.5 * max(0, gap_60, gap_300))`. The exact value in
`baseline-target.json` applies independently to both final G2 budgets. The
90% wins/ties and maximum 1% regression requirements also remain in force.
Jobs without a finite competitor median earn no free win. Final seeds,
held-out comparisons and all Nestbolt acceptance gates remain outstanding.

To re-audit the retained raw local records and regenerate the table in PowerShell:

```powershell
$baselineFreeze = Get-Content benchmarks/baseline-target.json -Raw | ConvertFrom-Json
$tableArgs = @($baselineFreeze.tables | ForEach-Object { '--table'; $_ })
python scripts/baseline_gap.py @tableArgs
```

The audit refuses incomplete coverage. Regeneration writes a new report and
does not replace the frozen target. A fresh checkout must recreate the raw runs
before this raw-record audit; the committed reports preserve the selected
records, statistics and their hashes.

Next is M2: stronger sheet search and the full validity, strip-parity and speed
gates. Conservative maker proxies already allow every development job to produce
a valid layout. True part-in-part placement and curve import/export remain M3.
