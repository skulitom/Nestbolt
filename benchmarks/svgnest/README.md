# Pinned SVGnest comparison runner

This drives Jack Qiao's unmodified [SVGnest revision 1248dc2](https://github.com/Jack000/SVGnest/tree/1248dc21efd3f90d1aa52ba5785e27e5217ed2c9)
in a real local Chromium browser. Keep `UPSTREAM_LICENSE` (MIT). Its original
dependency source headers remain intact in the pinned checkout; Clipper includes
Boost-licensed code and Tom Wu's JSBN attribution. No competitor code is copied
into Nestbolt's product. Playwright's Apache-2.0 notices are retained separately
in `../browser/THIRD_PARTY_NOTICES`.

```powershell
python scripts/svgnest.py setup
python scripts/svgnest.py run --job benchmarks/datasets/B/b-fu-nest-mb-given.json --seconds 60 --seed 0
python scripts/svgnest.py batch --count 24 --offset 0 --seconds 60 --seed 0 --settings identical
python scripts/svgnest.py batch --count 11 --offset 24 --seconds 60 --seed 0 --settings identical
python scripts/svgnest_report.py --batch output/playwright/svgnest-batches/<batch-id>/batch.json
```

Setup installs the exact Playwright dependency lock and its matched Chromium
build. Locally verified with Node 24.19.0, Playwright 1.64.0 and Chromium
156.0.8078.4 on Windows. Linux affinity support exists but has not yet been run.
Each batch selects a sorted slice of the 35 frozen B jobs, records the selection
before solving and stops if adapter sources change. Default batches contain at
most 24 sequential attempts. No unsupported or failed attempt is discarded.
Use the second configuration with `--settings expanded`. Neither configuration
has been established as the best setting; the complete M1 matrix is pending.

## Constraints and coordinates

The adapter preserves original polygon coordinates, holes, copy counts and units.
It places source copies separately in an input gallery to avoid interpreting
overlapping copies as holes, then reverses that translation on output. Returned
IDs and rigid transforms are checked; unknown/duplicate copies, missing holes,
scaling or reflection are errors. Original job geometry, not SVGnest's internally
cleaned contours, goes to the independent Clipper2 validator for every score.

Input encoding v2 uses straight `M/L/Z` paths, with 17-digit coordinates. A real
browser [parser probe](../results/svgnest-input-precision-20261011.json) found that
SVG polygon objects rounded the SWIM gallery by up to 0.0004805625 source units;
paths preserved all 1,928 coordinates exactly. Every new solve checks the actual
native parsed vertices before cleaning/search and refuses a changed coordinate.
The [unequal-edge-gap smoke](../results/svgnest-input-v2-smoke-20261011.json) and
[three affected SWIM jobs at 60 seconds](../results/svgnest-20261011T211052Z-d34e7f41.md)
all pass independent validation with this encoding. These are fresh searches;
the old failures remain unchanged. A fresh complete B pilot is in progress.

Output decoder v2 reads the exported `translate(...) rotate(...)` text directly
in double precision. Chromium's `SVGMatrix` rounded native translation values to
float32 and introduced small errors in the first pilot. `redecode_svgnest.py`
revalidates every saved export into separate correction records, without rerunning
search or changing the originals. The report auditor refuses legacy decoded scores.
The [24-job corrected pilot](../results/svgnest-correction-20261011T202304Z-3f63b428.md)
has 23 independently valid layouts; it is one provisional configuration and seed.
The [full initial-record audit](../results/svgnest-correction-20261011T202121Z-ad4dbe52.md)
also retains all preparation failures and settings changes.

SVGnest has one uniform angle grid for all parts. The adapter chooses a native
grid only if it preserves every declared discrete angle and introduces none that
are forbidden. Free rotations use a disclosed finite grid (4 or 36 samples).
Optional mirroring remains allowed by the job but is unavailable in native search.
Different part and edge clearances are represented with a virtual bin and origin
shift that account for SVGnest's half-gap offset behavior. Unequal margins work.

Default `--axis y` rigidly rotates the whole problem by 90 degrees so the native
leftward packing preference corresponds to the common trailing-Y offcut metric.
`--axis x` retains native orientation. This changes no permitted relative angles
or geometry. Axis and settings are explicit in every record.

Native identical bins support one rectangular stock type. The adapter refuses
mixed stock, defects, remnants, fill mode and disconnected components that must
remain one rigid part. Native search cannot cap the number of bins; independent
validation enforces the original stock limit. Exceeding it is an invalid outcome,
never a relaxed job or a score. These restrictions remain visible in each record.

Both provisional configurations use curve tolerance 0.005 in source units,
population 10, mutation rate 10 and holes enabled; expanded also enables concavity
exploration. The native tolerance controls cleaning and offset arcs even for
polygon inputs. It is not a promise that native cleanup is exact. An initial
1e-7 trial was too costly for even the small spacing check; those unsuccessful
trials are retained alongside the later setting, not included in a final matrix.

## Budgets and independent evidence

Each run loads local scripts only, with browser requests outside its local origin
blocked. Geometry is never uploaded. A seeded unsigned Mulberry32 generator is
installed before upstream code, and the native worker pool is restricted to one.
Browser/controller scheduling still makes a time-bounded run nondeterministic;
this is not the product's eventual deterministic work-budget API.

Windows uses a [job-wide CPU affinity limit](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
for the controller and all descendants. This matters because a Chromium process
reset its inherited affinity during preparation. Early controller-only trials
remain smoke evidence, ineligible for performance comparisons. The runner now
checks the complete observed process tree before solving and records executable
hashes. Linux uses a single allowed CPU and checks inherited process affinity.

The clock starts immediately before calling native `start`, including its
preprocessing. Both renderer and controller reject candidates arriving past the
requested 1–300 seconds. The controller closes the browser at the deadline even
if the renderer is busy. The last result selected by native fitness is validated;
the runner does not choose another candidate using the common score. The outer
process watchdog catches startup/shutdown hangs and terminates only its own tree.

Every attempt gets a new `output/playwright/svgnest` directory containing source
job, request, input SVG, native output, candidate history, independent layout and
validation when present, logs and hashes. The append-only benchmark log retains
valid, invalid, no-layout, unsupported and failed outcomes. Reports verify every
saved output, exact frozen job and configuration, independent score, deadline and
CPU evidence before producing an immutable table. Development mode refuses the
ten held-out maker IDs; no held-out job has been run.

The offline checks cover transform inversion, every input vertex/hole/copy,
independent edge clearance, disallowed constraints, malformed solver output,
evidence tampering, invented scores and missing CPU enforcement. Real smoke
checks include FU, unequal edge clearance and a stock cap deliberately too small
for the requested parts. The detailed mini-box trial has no layout within 30 s;
that outcome is retained. All are preparation evidence, not a Nestbolt quality gate.
