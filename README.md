# Nestbolt

Free, open-source fixed-sheet nesting for makers, with a local browser app and
native tools for people and agents. **Groundwork and the baseline are complete; the optimiser is in development.**

Nestbolt aims to arrange irregular parts across fixed sheets for laser cutting,
CNC routing, plasma, waterjet and fabric. The engine builds on
[jagua-rs](https://github.com/JeroenGar/jagua-rs) and the research behind
[sparrow](https://github.com/JeroenGar/sparrow), by Jeroen Gardeyn and collaborators.
The [M1 audit](docs/M1_BASELINE.md) covers all 1,878 development baseline slots and
freezes the final median-improvement target at 10.77231474%. Nestbolt has not yet
passed the optimisation-quality gates.

## What works today

- A Rust workspace with core, CLI, WebAssembly and native stdio MCP entry points.
- `nestbolt construct`: builds a first fixed/mixed-sheet layout, including holed
  and multipart parts through conservative collision proxies. All 30 development
  maker jobs produce independently valid layouts in the [current diagnostic](benchmarks/results/construct-maker-20261011T230206Z-b7a21810.md).
- `nestbolt improve`: deterministic repacking passes over shared prepared geometry,
  retaining independently valid improvements and recording failed sheet-removal
  attempts. Repair can displace blocking parts and separate overlapping groups.
  At six or more passes, bounded finishing trials compress the last sheet at
  each completed block of 64 passes and at the requested final pass. Successful
  compression can repeat, up to 15 trials per block.
  The full [35 sheet](benchmarks/results/repack-sheet-20261012T035142Z-a7b22154.md)
  and [30 maker](benchmarks/results/repack-maker-20261012T035142Z-54130739.md)
  diagnostics produce valid layouts on every development job. This
  experimental command supports a deterministic collision-query allowance and a
  cooperative deadline, keeping its last independently checked layout.
  Longer search supports up to 1,024 passes. A [four-job development pilot](benchmarks/results/placement-diversity-20261012T045248Z.md)
  combines the original placement strategy with shuffled allowed orientations
  and alternating left/right anchors. Blaz1 drops from 12 sheets to 10; Bruce
  uses 2.99% less material; Jakobs1 and Marques retain their preceding best scores.
- `nestbolt compact`: refines an existing valid layout without opening stock.
  Translation sweeps preserve its angles; `--relocate` also tries other positions
  and permitted orientations. The current [sheet](benchmarks/results/compact-b-20261012T012839Z-c2a42aba.md)
  and [maker](benchmarks/results/compact-m-20261012T012843Z-dac4bd32.md) diagnostics
  keep all 65 layouts valid and improve material on 17. This separate experimental
  step is not yet scheduled inside `improve`.
- `nestbolt strip`: a native strip diagnostic using the pinned, unmodified Sparrow
  library and independent checks of every accepted candidate. All 39 development
  runs pass validation and the development parity thresholds. See the
  [comparison and supported input scope](docs/STRIP_PARITY.md).
- `nestbolt inspect`: reads upstream jagua-rs BPP JSON, imports the geometry and
  reports quantities, original area, sheet stock and declared units.
- `nestbolt validate`: independently checks a polygon job/layout, including stock,
  margins, holes, defects, quantities, rotations, mirroring and fill mode. Invalid
  layouts receive no score. `validate-sparrow` adapts historical strip results.
- The same inspection function exposed through `wasm-bindgen` for a future Worker.
- An MCP connection scaffold using the official Rust SDK. It advertises **no tools**
  until their implementations exist.
- Native integration/property tests, Windows/Linux CI definitions, a WASM build
  check, locked dependency notices and two generated Sparrow smoke jobs.

Stronger layout improvement, SVG/DXF imports and exports, browser interface and five
MCP tools are still to be built. The independent validator currently operates on
polygon benchmark files; see [its scope and tests](docs/VALIDATION.md). The inspection
command is not a solver, fit test or independent layout validator. Its upstream
BPP format rejects item holes; the new constructor uses Nestbolt polygon jobs,
preserves their source outlines and reserves holes until part-in-part is added.

## Start developing

Install Rust through rustup and Python 3.11+. The repository selects Rust 1.98.1
and the WebAssembly target automatically. Windows requires the MSVC build tools.

```sh
cargo run -p nestbolt-cli -- inspect --input examples/sheet-job.json --units mm
python scripts/check.py
python scripts/smoke.py
cargo run -p nestbolt-cli -- validate --job examples/validation-job.json --layout examples/validation-layout.json
cargo run --release -p nestbolt-cli -- construct --job benchmarks/datasets/M/m-box-mini.json --output box-layout.json
cargo run --release -p nestbolt-cli -- improve --job benchmarks/datasets/M/m-box-mini.json --output improved-box-layout.json --passes 6
cargo run --release -p nestbolt-cli -- compact --job benchmarks/datasets/M/m-box-mini.json --layout improved-box-layout.json --output compact-box-layout.json --relocate
cargo run --release -p nestbolt-cli -- strip --job benchmarks/datasets/S/s-fu-strip.json --output fu-strip-layout.json --seconds 60 --seed 0
```

`construct --refine` adds bounded translation refinement; adding `--contacts`
tries outline contacts to interlock concave parts. `improve` compares both methods
with its initial layout before exploring other orders, and keeps the
best valid result. Finishing trials share the search controls and appear separately
in `polishing`; `completed_passes` counts only the requested repacking passes.
The first three finishing trials try 3%, 1% and 0.3% height reductions. If any
succeeds, up to twelve further trials repeat reductions, decreasing the step after
failure. If all three fail, finishing stops.
For more than 64 requested passes, finishing repeats after each block and at the
last pass, retaining the best independently checked layout throughout. The
default remains four passes; longer searches need an explicit `--passes` value.
After the original 64-pass block, successive seeds each receive an original
and a diversified pass. The latter varies the first feasible orientation on an
empty region and the preferred horizontal edge, while retaining all geometry
and rotation constraints. Each attempt counts against the requested passes and
the shared collision quota; twice the passes does not imply the same runtime.
It reports each completed trial on stderr and the final result
on stdout. It tests placements in stable cost order and stops sheet-removal
trials after an unplaced copy that the trial cannot revisit. Existing output
files are never overwritten.

`improve --max-checks 1000000` limits total collision queries across all passes;
the same job, seed, options and allowance give repeatable work. Add
`--timeout-ms 15000` for a cooperative deadline (at most 300,000 ms). The deadline
can return an earlier incumbent as machine speed varies. Individual geometry
operations and independent checks finish before yielding, so this is not a hard
wall-clock cap. Stopping before the first complete construction returns an error
and writes no layout. The result reports the stop reason, completed passes and
total queries, including work spent on an interrupted pass.

The sample reports six parts with a total area of 16,800 mm² and two available
300 × 200 mm sheets. Units must be specified (`mm`, `inch` or `unitless`); no
coordinate conversion is performed by inspection. See [the input notes](schemas/README.md).

The first smoke run downloads and builds a pinned Sparrow checkout. It runs two
five-second jobs sequentially and saves logs and provenance under `output/runs/`.
It checks executable integration only. Full quality benchmarks remain local.

The separate [M0 reproduction](benchmarks/sparrow-repro/README.md) freezes the
historical Sparrow version, all 1,300 published lengths and a 39-run native check.
All 39 runs pass independent geometry checks, and all 13 instance means are within
1% of the published means. See [the complete results and scope](benchmarks/results/m0-published-20261011T215820Z-10a30c6f.md).
This reproduces historical Sparrow quality; it does not establish Nestbolt quality.

## Use from agents

MCP is a **v1 requirement**, including agent-readable job/result schemas, progress,
bounded replies, reproducibility, release archives and an MCPB bundle. The five
planned tools are `import_parts`, `nest`, `validate_layout`, `export_layout` and
`estimate_sheets`. [Connection notes for Claude Code, Codex and Claude Desktop](docs/AGENT_INTERFACE.md)
describe the current scaffold and the remaining acceptance test.

```sh
cargo build -p nestbolt-mcp --locked
```

The executable is `target/debug/nestbolt-mcp` (`.exe` on Windows). It runs over
stdio without an HTTP server. No release, registry entry or client configuration
has been published or installed by this setup.

## Project map

| Path | Purpose |
| --- | --- |
| `crates/core` | Shared geometry adapter; future problem model and optimiser |
| `crates/cli` | Native command-line interface |
| `crates/wasm` | Single-Worker WebAssembly boundary |
| `crates/mcp` | Native stdio MCP server |
| `crates/validator` | Independent Clipper2 geometry kernel and strip-result checker |
| `benchmarks` | Frozen original smoke fixtures and upstream tool lock |
| `scripts` | Repeatable checks, fixture generation, notices and smoke runs |
| `schemas` | Current inspection formats; future canonical job/result schemas |
| `docs/PLAN.md` | Artem's full plan, including MCP in v1 |
| `docs/STATUS.md` | Milestone evidence and next steps |
| `docs/ARCHITECTURE.md` | Boundaries and questions to resolve before benchmarking |
| `docs/UPSTREAM_REVIEW.md` | Dated competitor review and pinned revisions |

## Progress and licence

**20% of gated milestones completed: M0 and M1 have passed.** The native
reproduction meets the original 1% threshold, and the development baseline is
complete. M2–M5 remain in progress or pending; see
[current evidence and next work](docs/STATUS.md).

Nestbolt's original code and generated fixtures are [MIT](LICENSE). jagua-rs is
an unmodified MPL-2.0 dependency. [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) records
the locked dependency graph and supplied licence texts. Changes to upstream
geometry code should be contributed upstream. See [CONTRIBUTING.md](CONTRIBUTING.md).
The isolated historical benchmark adapter is MPL-2.0, with its own notices.
