# Nestbolt

Free, open-source fixed-sheet nesting for makers, with a local browser app and
native tools for people and agents. **Groundwork is complete; baseline and optimiser work are in progress.**

Nestbolt aims to arrange irregular parts across fixed sheets for laser cutting,
CNC routing, plasma, waterjet and fabric. The engine builds on
[jagua-rs](https://github.com/JeroenGar/jagua-rs) and the research behind
[sparrow](https://github.com/JeroenGar/sparrow), by Jeroen Gardeyn and collaborators.
No optimisation-quality claims have been established yet.

## What works today

- A Rust workspace with core, CLI, WebAssembly and native stdio MCP entry points.
- `nestbolt construct`: builds a first fixed/mixed-sheet layout, including holed
  and multipart parts through conservative collision proxies. All 30 development
  maker jobs produce independently valid layouts in the [first diagnostic](benchmarks/results/construct-maker-20261011T223817Z-32654739.md).
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

Layout improvement, SVG/DXF imports and exports, browser interface and five
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
```

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

**5% of gated milestones completed: M0 has passed.** The complete native
reproduction meets the original 1% threshold. M1's full baseline and M2–M5 remain
in progress or pending; see [current evidence and next work](docs/STATUS.md).

Nestbolt's original code and generated fixtures are [MIT](LICENSE). jagua-rs is
an unmodified MPL-2.0 dependency. [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) records
the locked dependency graph and supplied licence texts. Changes to upstream
geometry code should be contributed upstream. See [CONTRIBUTING.md](CONTRIBUTING.md).
The isolated historical benchmark adapter is MPL-2.0, with its own notices.
