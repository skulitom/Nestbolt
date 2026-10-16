# Finer-bound release candidate: integration checks — 2026-10-16

**All local integration checks pass for `7eba929`.** This candidate integrates
only the exact eight-pair collision-bound change and its explicit test coverage.
The common-line exchange experiment remains isolated after its retained failed
pilot. Version remains `0.2.0-alpha.1`; no release or tag has been created.

The [isolated subset](h4-score-chunks-probe-20261016.md) already passed with 99
valid layouts and four exact fixed-work pairs. The integrated build still needs
its own full 65-job/native and eleven-job browser comparison, plus scale checks.
The original preview's Chrome failure remains preserved. H4 stays open and
completed milestone weight stays 45%.

[Verified checks](h4-score-integration-20261016/checks.json) include formatting,
strict workspace/all-target lint, **302 workspace tests** with one existing
ignored test, three optimized score tests, **27 optimized CLI feature tests**,
native CLI/MCP builds, WASM/site/type checks, **86 Chromium/Firefox tests** with
four existing opt-in skips, dependency notices, schemas, and 23 package tests
with one platform-specific skip. The real built Windows MCPB also passes tool
catalog, import, nesting, independent validation and write-confinement checks.
All builds/tests use CCD1. No held-out geometry is evaluated.

The production source change preserves accepted-score arithmetic, summation
order, ties, infinite-bound evaluation, geometry, work charges and deadlines.
The exact tested source file matches the isolated candidate. Root production
source remains unchanged throughout the checks. All original logs and outcomes
are retained; none of these stages was repeated to obtain a pass.

The [new fixed matrix plan](h4-preview-score-release-20261016/plan.json) covers
603 new attempts: 67 union jobs in native/Chrome/Firefox, seeds 0–2, 60 seconds.
It reuses only 195 verified frozen-v1 baseline outcomes. All existing quality,
coverage and validity limits remain unchanged. The plan is committed before its
one-use measurement opens.

[Hosted checks](https://github.com/skulitom/Nestbolt/actions/runs/38840747952)
are running on the same candidate commit. Its
[tagless package workflow](https://github.com/skulitom/Nestbolt/actions/runs/38840747735)
passed for all three native targets; downloaded-artifact verification is separate.
This dry run publishes no GitHub release or registry entry.

The [raw archive](h4-score-integration-20261016/raw.zip) retains 23 members,
6,295,137 bytes, SHA-256
`2602e2a5c537c8675ef15282220483cc81298ad2e4f42b1926d2e83fe4ba2379`.
CRC, every member size and every SHA-256 were verified. It includes all stage
logs, exact source and native/WASM snapshots, the actual MCPB, metadata and the
integration/sealing helpers. All final artifact hashes are recorded in the
[checks](h4-score-integration-20261016/checks.json).
