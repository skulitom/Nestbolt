# Remaining short-sheet count screen — 2026-10-28

The bounded screen excludes four more short-sheet allocations, leaving **448
necessary candidates**. It does not produce a complete source layout or close H5.
The excluded counts, in brackets / inserts / cogs order, are **0/10/5, 1/8/5,
2/9/4 and 4/7/3**. All 4,576 original allocation rows remain recorded, including
every previous exclusion. The known source-valid 7/4/1 and 8/5/0 controls remain.

## Frozen scope and independent model check

The complete prior frontier had 452 survivors and 32 maximal count vectors.
All 32 were selected and ordered before search, by descending bracket count,
then descending cog count and descending insert count. Previously excluded
7/5/1 and 7/6/1 were never reopened. Every original in each selected vector is
mandatory; every allowed bracket/insert outer mode and every real cog angle
retain their complete reference-coordinate domain.

The source X-capacity model uses only disjoint source-contained rectangles:
three coarse components per bracket mode, one per insert mode and sixteen
guaranteed strips per cog. The full stems used for pair spacing are not added
as extra height. The 121 directed pair distances are unchanged. In particular,
the 251,956 µm cog/cog horizontal bound applies to arbitrary independent real
angles throughout the complete short-stock Y domain. Identical copies may be
relabelled in X order, including multiple cogs. No source Y or cog angle is fixed.

Before any search, an independent protobuf reader verifies **6,649 variables
and 85,989 constraints** across the 32 models. It rejects unreviewed fields and
checks all coordinate domains, mode selectors, source intervals, capacity,
symmetry and both directions of every selected original pair. It does not
import the model builder. The source-to-model necessity mapping and deletion
argument are recorded in the [necessity proof](h5-short-count-x-screen-20261028/necessity-proof.json).

## One bounded pass

Each case receives one call with a 3-second solver setting, four workers,
seed zero and the `fj` subsolver excluded. The aggregate settings total 96 s;
the entire child process has a 120-second bound. All 32 calls complete in
**85.249128 s shared time**. Aggregate reported solver time is 83.401531 s.
Small solver-return overruns are preserved; the largest is **0.034838 s**.
There is no timeout, retry, reseed, extension or adaptive second pass.

| Brackets / inserts / cogs | Terminal status | Returned seconds |
|---|---|---:|
| 8 / 7 / 0 | UNKNOWN | 3.025100 |
| 7 / 4 / 1 | OPTIMAL | 0.358303 |
| 7 / 9 / 0 | UNKNOWN | 3.030865 |
| 6 / 8 / 1 | UNKNOWN | 3.031333 |
| 6 / 11 / 0 | UNKNOWN | 3.031539 |
| 5 / 8 / 2 | UNKNOWN | 3.029704 |
| 5 / 10 / 1 | UNKNOWN | 3.028919 |
| 5 / 13 / 0 | UNKNOWN | 3.031643 |
| 4 / 7 / 3 | INFEASIBLE | 0.987886 |
| 4 / 10 / 2 | UNKNOWN | 3.032797 |
| 4 / 12 / 1 | UNKNOWN | 3.032040 |
| 4 / 15 / 0 | UNKNOWN | 3.020265 |
| 3 / 9 / 3 | UNKNOWN | 3.030930 |
| 3 / 12 / 2 | UNKNOWN | 3.023940 |
| 3 / 14 / 1 | UNKNOWN | 3.023840 |
| 3 / 17 / 0 | UNKNOWN | 3.034838 |
| 2 / 9 / 4 | INFEASIBLE | 0.274491 |
| 2 / 11 / 3 | UNKNOWN | 3.025640 |
| 2 / 14 / 2 | UNKNOWN | 3.019153 |
| 2 / 16 / 1 | UNKNOWN | 3.022104 |
| 2 / 19 / 0 | UNKNOWN | 3.017747 |
| 1 / 8 / 5 | INFEASIBLE | 0.032944 |
| 1 / 11 / 4 | UNKNOWN | 3.026934 |
| 1 / 13 / 3 | UNKNOWN | 3.024504 |
| 1 / 16 / 2 | UNKNOWN | 3.019095 |
| 1 / 18 / 1 | UNKNOWN | 3.030735 |
| 1 / 21 / 0 | UNKNOWN | 3.026612 |
| 0 / 10 / 5 | INFEASIBLE | 0.048635 |
| 0 / 13 / 4 | UNKNOWN | 3.025469 |
| 0 / 15 / 3 | UNKNOWN | 3.023512 |
| 0 / 18 / 2 | UNKNOWN | 3.024899 |
| 0 / 20 / 1 | UNKNOWN | 3.016324 |

All raw responses, logs, parameters and opened-call records are preserved and
independently compared. Only the four terminal INFEASIBLE results remove count
vectors. Their subset/upward closure removes four previously surviving rows.
The remaining 448 vectors still have 32 maxima; newly exposed maxima were not
searched in this pass.

The single OPTIMAL result is a satisfaction-model solution for **7/4/1**,
already known to have valid source controls. Every one of its 143 variables
and 4,104 constraints passes independent evaluation. A second sweep rebuilt
from the source inputs verifies 41 active rectangles and all 66 original pairs,
with 2,979 µm of minimum vertical-capacity slack. This assignment contains only
reference X and mode: it is not a new source layout. All 27 UNKNOWN cases remain
allowed. No full66 infeasibility, native validation or H5 completion is claimed.

## Next construction and publication

The current source-valid 64-part layout still lacks two brackets. Inspect the
remaining 8/6/0 short-sheet allocation using full original orthogonal geometry
in both coordinates; transferring one extra insert could free first-sheet
space. Any such construction needs an audited new model and a declared bounded
call, followed by actual source checks. A valid short14 alone would still leave
the complete first-sheet construction and full66 validation to do. The closed
32-case screen and failed 17/24-mover searches will not be restarted.

The previous checkpoint `f9629063` passes all six jobs in
[CI 40693544095](https://github.com/skulitom/Nestbolt/actions/runs/40693544095).
Production, READMEs and upstream heads/releases are unchanged. H2 and H5 remain
open at **60% completed milestone weight**, all 22 reserved H2 vectors remain
unopened, and no new release qualifies.

[Model checks](h5-short-count-x-screen-20261028/model-checks.json),
[response checks](h5-short-count-x-screen-20261028/response-checks.json),
[complete allocation list](h5-short-count-x-screen-20261028/updated-allocations.json),
[next step](h5-short-count-x-screen-20261028/next-step.json),
[byte-verified archive](h5-short-count-x-screen-20261028/raw-manifest.json).
The archive retains 326 canonical files and
334 identical-byte aliases in 1,721,650
compressed bytes, including all models, inputs, helper sources, responses and
the preceding main-push receipt.
