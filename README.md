# Nestbolt

Free, open-source fixed-sheet nesting for makers, with a local browser app and
native tools for people and agents. **Currently at the groundwork stage.**

Nestbolt aims to arrange irregular parts across fixed sheets for laser cutting,
CNC routing, plasma, waterjet and fabric. The engine builds on
[jagua-rs](https://github.com/JeroenGar/jagua-rs) and the research behind
[sparrow](https://github.com/JeroenGar/sparrow), by Jeroen Gardeyn and collaborators.
No optimisation-quality claims have been established yet.

## What works today

- A Rust workspace with core, CLI, WebAssembly and native stdio MCP entry points.
- `nestbolt inspect`: reads upstream jagua-rs BPP JSON, imports the geometry and
  reports quantities, original area, sheet stock and declared units.
- The same inspection function exposed through `wasm-bindgen` for a future Worker.
- An MCP connection scaffold using the official Rust SDK. It advertises **no tools**
  until their implementations exist.
- Native integration/property tests, Windows/Linux CI definitions, a WASM build
  check, locked dependency notices and two generated Sparrow smoke jobs.

The fixed-sheet optimiser, independent layout validator, SVG/DXF imports and
exports, browser interface and five MCP tools are still to be built. The inspection
command is not a solver, fit test or independent layout validator. Item holes are
explicitly rejected by the current geometry adapter.

## Start developing

Install Rust through rustup and Python 3.11+. The repository selects Rust 1.98.1
and the WebAssembly target automatically. Windows requires the MSVC build tools.

```sh
cargo run -p nestbolt-cli -- inspect --input examples/sheet-job.json --units mm
python scripts/check.py
python scripts/smoke.py
```

The sample reports six parts with a total area of 16,800 mm² and two available
300 × 200 mm sheets. Units must be specified (`mm`, `inch` or `unitless`); no
coordinate conversion is performed by inspection. See [the input notes](schemas/README.md).

The first smoke run downloads and builds a pinned Sparrow checkout. It runs two
five-second jobs sequentially and saves logs and provenance under `output/runs/`.
It checks executable integration only. Full quality benchmarks remain local.

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
| `benchmarks` | Frozen original smoke fixtures and upstream tool lock |
| `scripts` | Repeatable checks, fixture generation, notices and smoke runs |
| `schemas` | Current inspection formats; future canonical job/result schemas |
| `docs/PLAN.md` | Artem's full plan, including MCP in v1 |
| `docs/STATUS.md` | Milestone evidence and next steps |
| `docs/ARCHITECTURE.md` | Boundaries and questions to resolve before benchmarking |
| `docs/UPSTREAM_REVIEW.md` | Dated competitor review and pinned revisions |

## Progress and licence

**0% of gated milestones completed; M0 is in progress.** Its final requirement is
to reproduce Sparrow's published strip results natively within 1%. A scaffold or
five-second smoke run does not satisfy that requirement.

Nestbolt's original code and generated fixtures are [MIT](LICENSE). jagua-rs is
an unmodified MPL-2.0 dependency. [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES) records
the locked dependency graph and supplied licence texts. Changes to upstream
geometry code should be contributed upstream. See [CONTRIBUTING.md](CONTRIBUTING.md).
