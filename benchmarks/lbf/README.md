# Pinned jagua-rs LBF baseline

This runs Jeroen Gardeyn's **unmodified** one-pass Left Bottom Fill implementation
from [jagua-rs revision 9e00fd8](https://github.com/JeroenGar/jagua-rs/tree/9e00fd867be0fc493002aea68a1c6613d5b833d6).
The upstream workspace and its committed dependency lock are pinned in `tool.json`.
LBF and jagua-rs remain MPL-2.0; keep `UPSTREAM_LICENSE` and
`THIRD_PARTY_NOTICES`. The benchmark executable is separate from Nestbolt's product.

```powershell
python scripts/lbf.py build
python scripts/notices.py --lbf --check
python scripts/lbf.py run --job benchmarks/datasets/B/b-fu-nest-mb-given.json --seconds 60 --seed 0
python scripts/lbf.py batch --seconds 60 --seed 0
python scripts/lbf.py batch --dataset M --seconds 60 --seed 0
python scripts/lbf_report.py --batch output/lbf-batches/<batch-id>/batch.json
```

The batch runs all 35 frozen B jobs sequentially with both configurations, or
all 30 development maker jobs with `--dataset M`. All ten held-out jobs are
excluded; the individual run command also enforces the phase guard. Each
run has one worker, `RAYON_NUM_THREADS=1`, a hard process deadline and independent
validation. Batch selection is bounded below three hours even if each solve and
validation reaches its limit. Run another seed explicitly; never discard failures.
These are provisional M1 measurements. Full competitor settings,
development/final seed aggregation and final comparison gate remain to be built.
The [first maker batch](../results/lbf-20261011T212716Z-c9c2fc4b.md) retains all
60 attempts: eleven valid garment layouts, one clearance failure and 48
unsupported outcomes. Native LBF cannot model the holed parts in those 24 jobs;
they are neither filled in nor omitted from the table.

## Configuration and fairness

- `identical`: upstream's 5,000 placement samples and 20% local sampling, with
  simplification and narrow-concavity closing disabled. Original polygons and
  constraints are used without additional approximation.
- `upstream-default`: the original simplification and concavity-closing defaults,
  with the same original input. Validation still uses original contours.

Both preserve allowed angles, reflection permissions, quantities and stock.
Neither setting has been tuned. The seed is supplied explicitly. This is the
construction baseline the plan compares with the other tools; it is not included
as a G2 best-competitor alternative. A one-pass solver can finish before the time
limit, and its measured time is retained. We do not repeat it secretly until a
favourable result appears. A published Table 5 score is not a substitute for a
fresh equal-budget run of deepnest-next, SVGnest or applicable Sparrow.

## Conversion and independent checks

The adapter assigns numeric upstream IDs and restores original string IDs on
output. It preserves coordinates and explicit units. Unlimited stock becomes at
most one sheet per requested copy, a sufficient bound for a complete layout.
Rectangular sheets are cropped by their margins; defect polygons become forbidden
quality-zero zones. Upstream's single spacing rule currently requires equal
inter-part and edge clearance.

Upstream exports rotations in degrees and reflection across local X. The checker
uses radians and reflection across local Y, so reflected transforms receive the
corresponding 180-degree adjustment. Tests check this geometrically, including
non-quarter-turn rotations. Embedded solver geometry and reported density/cost
never determine validity or score.

The original job is checked before solving. Original part geometry, reconstructed
transforms and the original stock then go to the independent Clipper2 validator.
Only a valid report receives a material score. Incomplete layouts, invalid
placements, process errors and timeouts remain failures with no score.

The current adapter explicitly rejects item holes/disconnected components,
remnants, defects with holes, unequal spacing rules and fill modes. It does not
silently fill holes, discard defects or alter a constrained job. Support/handling
of these maker-job cases remains M1 work. This runner handles BPP sheet jobs, not
the S strip objective.

## Evidence and smoke checks

Each run gets a new directory under `output/lbf`, copied source/config/input,
stdout/stderr, original solver JSON/SVG, converted layout, validator report and
hashes. Records include compiler, native CPU flags, binary hash, source revision,
dependency lock, adapter hashes, hardware, seed, limit and actual elapsed time.
Windows checkout line endings are normalized for the upstream lock's Git-blob
checksum; the raw checkout hash is also retained. Existing results are never
overwritten. `BENCHMARKS.md` receives an append-only entry.

The report command verifies every saved output, the frozen source job and the
validator's score before creating an immutable full-precision JSON checkpoint
and readable table under `benchmarks/results`. It refuses changed records,
missing cases, duplicate cases or differing adapter code within a batch.

The CI smoke uses FU and `fixtures/lbf-constraints.json`, an original MIT fixture
covering mixed stock, a capped sheet, margins, a defect, 1 mm gaps and reflection
permissions. Unit tests also reject unknown IDs, non-rigid transforms, invalid
numbers and unsupported constraints. Hosted CI still requires a configured remote.
