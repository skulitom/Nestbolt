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

## Use the Rust crates from a small checkout

For an application that uses Nestbolt as a Rust library, clone the release
beside your application and check out the crates directory. Git's blob filter
and sparse checkout let the benchmark archives stay on the server.

```sh
git clone --filter=blob:none --sparse --depth 1 --branch v0.2.0-alpha.1 https://github.com/skulitom/Nestbolt.git nestbolt-src
git -C nestbolt-src sparse-checkout set crates
git -C nestbolt-src rev-parse HEAD
```

For this release, verify that the last command prints
`c36baa8145e9e7b51e5667f4e4eaa0242256fc6e`. Record the revision in your
build setup so teammates and CI use the same source. With the application
and `nestbolt-src` in sibling directories, declare these path dependencies in the application’s `Cargo.toml`.

```toml
[dependencies]
nestbolt-core = { path = "../nestbolt-src/crates/core" }
nestbolt-validator = { path = "../nestbolt-src/crates/validator" }
```

Include the crates your application imports directly. Cargo resolves their
dependencies normally. On Windows the checkout for this tag used 876 KiB of
Git packs and 3.55 MiB of working files before compiling. Rust dependencies
and build outputs take additional space. A new development revision can be
pinned by fetching its full commit and then checking it out in the same clone.

```sh
git -C nestbolt-src fetch --depth 1 --filter=blob:none origin <full-commit>
git -C nestbolt-src checkout --detach FETCH_HEAD
```
