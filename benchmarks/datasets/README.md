# Academic benchmark freeze

There are **13 S strip jobs and 35 B sheet jobs**, all unitless, with the original
part contours and quantities from the pinned, MIT-declared OR-Datasets collection.
Every entry in `academic.json` records its source URL/hash, licence scope,
construction, output hash, metric and any rotation changes. Retain
[the collection licence](../sources/OR_DATASETS_LICENSE) with these files.

```powershell
python scripts/datasets.py --check  # offline integrity check
python scripts/datasets.py         # fetch pinned sources and reproduce the files
```

The converter itself is checksummed. Rebuilding refuses to overwrite changed
files, and freezing refuses an existing manifest. A future necessary dataset
correction requires an explicit new version and disclosure in results; it must
not silently replace cases after tuning. This academic freeze precedes any
optimiser tuning. The maker set and its ten held-out jobs remain separate work.

## S: original strips

All 13 strip families retain the source's angles and nominal strip height along
Y. For the common polygon contract, one sheet gives a finite X envelope equal to
the sum of initial part bounding-box widths times quantities, plus one model
unit. Every initial part height fits, so this is a safe envelope for a consecutive
placement. It is **not the score**: the strip score is the greatest occupied X
coordinate after transformation. Any leading gap counts. The source part geometry
must be independently contained in the original height and envelope.

The G3 comparator and Nestbolt receive the same nominal height. This is distinct
from the historical M0 reproduction, which retains the paper's 0.01% height
inflation in six cases. M0 inputs and its already-running experiment are unchanged.

## B: 22 published-construction jobs plus 13 declared derivatives

The 22 `nest-mb-given` and `nest-mb-free` jobs reconstruct the eleven families
shared by our sources and the Nest-MB set in
[Martínez-Sykora et al. (2017)](https://doi.org/10.1016/j.ejor.2016.09.043),
section 6.1 and Tables 1/5. The
[author manuscript](https://eprints.whiterose.ac.uk/139290/1/BCP-EJOR.pdf)
was read directly; its checksum is in the manifest. Each sheet is square with
side **1.5 times the greatest initial bounding-box dimension of any part**.
The given-angle variant uses Table 1's angles; the free variant uses Table 5's
free rotations. Stock is unlimited, mirroring disabled, gaps and margins zero.

The source and paper differ in two rotation lists: MAO changes from four angles
to 0/180, while SHAPES0 changes from 0 only to four quarter turns. These changes
apply only to the published-construction B jobs. BLAZ1 is named SHAPES2 in the
paper; SWIM is named SWIMM. Counts and dimensions match the printed table at its
precision. SWIM keeps the exact formula result, 2909.4677415, without rounding
the sheet to the printed 2909.47. SHIRTS has transposed small/large dimensions in
the manuscript's Table 1; the unambiguous medium dimension is 19.5 and is used here.

These are **reconstructions from a pinned conversion**, not a claim that the
paper supplied matching geometry hashes. We retain its Table 5 PBP bin counts and
mean squared utilisation as historical context. Those are neither verified global
best-known results nor Nestbolt's offcut material metric. The final quality gate
uses fresh equal-budget runs against the actual frozen polygons. The remaining
12 paper families and the López-Camacho jigsaw collections are not included.

The 13 `strip-sheet` jobs are explicitly **Nestbolt derivatives**: original strip
Y height, finite X length twice the largest initial part bounding-box dimension,
unlimited stock and original rotations. The formula does not depend on solver
results. These provide the plan's fixed-sheet variants of S without passing off
new sheet sizes as published instances.

## Verification and limits

All 48 job source contracts pass the independent Rust validator. This checks
polygon topology and job constraints, not a feasible packing or optimiser quality.
Conversion tests check that every vertex, copy and ID survives, paper-specific
rotations stay separate, and changed/unlisted files fail the integrity check.
`scripts/check.py` runs these checks offline in CI.

The frozen files are benchmark polygons. They do not replace the later SVG/DXF
curve fixtures, maker jobs, fidelity tests, competitor settings or seed matrix.
