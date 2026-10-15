# Repeatable search contract

The v1 MCP promise is that the same original job, engine version, seed and budget
produce the same successful layout. A seed combined with a wall-clock cutoff
does not satisfy that promise: scheduling changes how many search steps finish.

## Two timings

`nestbolt sheets` and the core search take `Timing::Wall` or `Timing::Work`.

- **Wall** (benchmarks, the CLI default): real seconds. Every tool gets the same
  60/300-second opportunity. Results depend on machine speed and scheduling and
  are never reported as repeatable.
- **Work** (MCP `nest`, CLI `--repeatable`): the search clock is charged with
  deterministic work counts converted to reference seconds by fixed coefficients
  (`crates/core/src/clock.rs`, version `nestbolt-work-v2`): sample evaluations,
  evaluated vertices, collision-tracker items and vertices, re-registered items,
  container builds, constructor collision checks (weighted by the square root of
  the mean outline vertex count), validated vertices and bounding-rectangle
  packing steps. The search is single-
  threaded with seeded streams, so the same inputs replay the same steps.

A work budget converts `WORK_SHARE` (0.5) of `time_budget_s` to work. The full
`time_budget_s` stays a hard real-time limit. If it arrives first, the search
stops at a cooperative checkpoint, returns its best checked layout and reports
`repeatable: false`; the MCP reply suggests a larger budget. The CLI's
`--time-limit` raises that real-time limit (never below the budget) without
changing the work, so a slower machine can still finish it and get the same layout.

The opt-in `quick_start` request field (CLI `--quick-start`, browser **Quick
initial layout**) tries the existing conservative rectangle packer before the
ordinary constructor. Its rectangle operations and original-geometry validation
are charged to the same clock. A valid incumbent enters the usual sheet search;
unsupported or unsuccessful rectangle attempts fall back to construction.
The option is off by default. It changes the search schedule and can change
material use, so retain it as part of the input when comparing or replaying runs.
The published v1 benchmark defaults and work coefficients remain unchanged.

## Calibration

The coefficients were fitted on 16 development jobs (20-second wall-clock runs on
the reference AMD Ryzen 9 7950X3D, one core). Predicted/real search time ranged
from 0.72 to 1.23 per job. Detailed outlines with many interlocking contacts
(public gears) cost more per evaluated vertex than the model assumes and can
reach the real limit at short budgets. Changing a coefficient changes repeatable
results, so it requires a new `WORK_VERSION`.

## Scope and limits

- Repeatability covers placements, scores and exports on the same build and
  platform. Floating-point libraries may differ between operating systems and
  WebAssembly, so cross-platform equality is not promised.
- Wall-clock and work runs with the same seed are different searches.
- Cancellation and the hard limit always return either a checked layout or an
  explicit error; no unchecked layout escapes.

## Evidence

Repeated work-mode CLI runs gave identical layouts on fu, jakobs1 strip, sign 2,
frame inserts, box batch 500 and Shapes0 (15–20 s budgets). Two public-gear runs
were identical but flagged not repeatable because they reached the real limit.
The MCP integration test nests twice with the same seed and requires identical
layouts whenever both runs report `repeatable: true`.
