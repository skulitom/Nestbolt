# Pinned deepnest-next desktop comparator

This controls the unmodified [deepnest-next revision 1e7ba6e](https://github.com/deepnest-next/deepnest/tree/1e7ba6e2382557f337ad481ca3251fc22032ca0f)
through its public SVG import and solver API in its own Electron application.
The native run is separate from the Nestbolt product. Root MIT does **not** cover
every component: `main/deepnest.js` declares GPLv3, and the loaded Rust SVG
preprocessor declares AGPL-3.0-only. Upstream licence tables/text, GPLv3 text and
native dependency notices are retained alongside this file. No engine code is
copied into Nestbolt.

```powershell
python scripts/deepnest.py setup
# Run this command inside Anode on Windows to keep the GUI off the working desktop:
python scripts/deepnest.py run --job benchmarks/datasets/B/b-fu-nest-mb-given.json --seconds 60 --seed 0
python scripts/deepnest.py run --job benchmarks/fixtures/svgnest-edge-gap.json --seconds 5 --settings clearance-safe
```

The exact upstream revision and dependency Git-blob checksum are in `tool.json`.
Setup uses its locked dependencies, compiles TypeScript and downloads that lock's
Electron version. The observed local runtime is Electron 40.10.2 / Chromium
144.0.7559.236. Node controller dependencies share the exact Playwright lock with
the SVGnest runner. Windows execution uses the hidden Anode session. The current
loaded-process-tree CPU control is Windows-only; Linux execution is explicitly
refused pending equivalent controls.

## Current verification and remaining work

The first five-second FU result is independently valid. The native spacing trial
demonstrates a hole-clearance issue: with a requested 4 mm gap the insert lands
about 2 mm from the frame's inner edge, so the checker rejects it. The separately
declared `clearance-safe` setting requests twice the interpart spacing and produces
an independently valid result on that original job. Both outcomes are retained.
An insufficient stock cap produces an incomplete native layout and no score.
A mixed-stock trial with unequal margins, one capped small sheet and unlimited
large sheets produces a valid two-sheet layout. All eleven preparation attempts,
including startup failures, are [retained](../results/deepnest-preparation-20261011.json).
Six conversion tests and three evidence-audit tests pass.

Startup was intermittent with a CPU limit applied before launching Electron. Stage timing
and initialization diagnostics are retained. Applying the limit after import and
before solving produced four consecutive valid FU smokes with prompt startup.
[Every startup trial](../results/deepnest-startup-20261011.json) remains available,
including the failed shared-job experiment before separate nested jobs were used.
The startup allowance is bounded separately from the solve clock. Initialization failures are failures,
not unsupported jobs or discarded attempts. A stable full baseline batch,
nonrectangular stock conversion and settings selection remain pending. This is
not a completed M1 comparison or a Nestbolt quality result.

## Conversion and constraints

Each original part type is imported as one SVG containing its original polygon
and holes. Native quantities represent copies; there is no gallery translation.
Every imported source, hole count and quantity is checked. Original polygons
are used for independent validation, including after native simplification.
The native output's numeric source/copy IDs are mapped back to the original IDs;
unknown or duplicate IDs, changed source identities, non-finite values and
unexpected scaling/reflection are rejected.

Rectangular stocks keep their sizes, individual margins and limits. Unlimited
stock becomes one possible sheet per part copy, sufficient for any complete
solution. Mixed stock order follows the original job; native fitness and common
material scoring remain distinct. The original checker determines stock usage,
feasibility and the trailing offcut. The provisional adapter explicitly refuses
defects/remnants, disconnected rigid parts and fill mode; those conversions are
still pending rather than silently relaxed.

The pinned engine inflates outer part contours by half its spacing, but its
recursive offset skips negative sheet/hole offsets. A virtual rectangular bin
and origin account for this behavior at the outer edge, preserving independent
edge clearance and margins. The identical setting retains the requested native
gap, including the observable hole-clearance failure. `clearance-safe` uses a
disclosed multiplier of two: it is conservative between outer contours and does
not change the original job or validation threshold. The expanded configuration
instead tries native box placement, line merging and a finer free-angle grid.
None has been declared the best setting.

One uniform rotation grid is shared by all native parts. The adapter refuses any
grid that drops an allowed discrete angle or adds a forbidden one. Free angles
use a recorded finite grid. Optional mirrors remain allowed by the original job
but are unavailable in native search. Default axis Y rigidly rotates the whole
problem to align the native packing direction with the offcut metric; original
coordinates are restored on output, independently for each stock size.

## Isolation, time limits and records

Every attempt has its own user-data and import directories. Notifications and
external browser requests are disabled; only generated local SVG polygons enter
the app. The seeded JS random generator and one-worker environment load before
upstream scripts. GPU acceleration and background throttling are disabled for
the hidden test window. After import, Windows affinity jobs constrain the controller
and every existing descendant to logical CPU 2; later children inherit those
limits. Separate nested jobs accommodate Chromium's existing sandbox jobs.
SVGnest uses CPU 0, avoiding overlap between the timed solvers.
The process tree is inspected before solving. Actual loaded native add-ons,
Electron, generated application JS, lockfile and adapter hashes are recorded.

The solve clock starts immediately before native `start`, including solver
preprocessing. Renderer and controller reject candidates arriving after the
declared 1–300 seconds. Only the latest native-fitness winner is scored. Closing
uses Electron's immediate exit to avoid renderer unload handlers waiting behind
native geometry work; a watchdog can terminate only that owned process tree.
Startup/shutdown allowance is at most 210 seconds beyond the solve limit; source
contract and final independent validation each have their own bounded checks.

`output/playwright/deepnest` retains each source job, SVGs, settings, candidate
history, full native result, independent layout/report, logs and immutable run
record. `deepnest_report.py --record ... --sha256 ...` checks saved bytes, original
job identity, validator score, worker/seed/CPU controls, native binary provenance
and result timing. Earlier partial provenance records remain preparation evidence.
All outcomes are appended to `BENCHMARKS.md`. The ten held-out maker jobs remain
excluded from development runs.
