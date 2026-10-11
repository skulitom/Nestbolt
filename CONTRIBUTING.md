# Contributing

Read [the plan](docs/PLAN.md), [status](docs/STATUS.md) and [architecture](docs/ARCHITECTURE.md)
before changing scope. The initial development path is Windows, with Linux checks
in CI. Python scripts use only the standard library.

Run `python scripts/check.py`. Add `--smoke` when changing the geometry adapter,
benchmark runner or upstream versions. Regenerate dependency notices after any
lockfile change with `python scripts/notices.py`. Commit Cargo.lock and the exact
Sparrow benchmark lock. Never edit files in Cargo's registry or the upstream cache.

Original smoke geometry can be regenerated with `python scripts/generate_smoke.py`.
Review both the fixture changes and checksums. Imported benchmark datasets need
their own source and licence records before inclusion. Do not tune on held-out jobs.

Keep computational geometry in `core`, transport handling in `cli`/`mcp`/`wasm`,
and the independent validator separate from jagua-rs. Tests should target failure
modes and geometric invariants. Keep performance claims tied to frozen results.

Workflows and bundle scripts are ordinary source files. There is no extension
allowlist; any future repository guard must allow `.github/workflows/*.yml`, MCPB
scripts/manifests, schemas and notices. Never publish releases or registry entries
without Artem's instruction. Do not add telemetry or remote geometry processing.
