# Tree-depth preview: integration checks — 2026-10-16

**All local integration checks pass for `aba989e`.** The only production
change lowers the separator-window base collision-tree depth from four to three.
Original geometry, leaf threshold, aspect scaling, budgets and public options
remain unchanged. No common-line exchange experiment is integrated.

[Checks](h4-depth-integration-20261016/checks.json) cover 302 workspace tests
(one existing ignored), all 75 optimized core tests, 27 optimized CLI feature
tests, strict lint, native CLI/MCP and WASM builds, TypeScript/site builds,
86 enabled Chrome/Firefox tests (four existing opt-in skips), schemas, notices,
and 23 package tests (one platform-specific skip). All run on CCD1.

The actual Windows MCPB passes tool catalog, import, nesting, independent
validation and write confinement. The original confinement inventory failed
because this task concurrently saved the H5 preparation evidence folder. The
failure is retained. With competing repository writes stopped, a controlled
verification of the same unchanged bundle passes. No source/build, functional
suite or measured search was repeated; only that interrupted confinement check.

The [isolated 99-layout pilot](h4-quadtree-depth-probe-20261016.md) passes both
browser subsets (Chrome +0.689439%, Firefox +0.639475%). This does not replace
the [fresh full comparison plan](h4-preview-depth-release-20261016/plan.json):
603 new outcomes over the 67-job union, plus 195 verified frozen-v1 baselines.
Original quality limits, inputs, three seeds and 60-second budgets remain.
Current browser scale, every exported curve and new package checks also remain.
The earlier failed full comparisons are preserved. H4 stays open; weight is 45%.

The raw archive retains 26 members / 6,313,079 bytes,
SHA-256 `8231563967210dc2f34fb21685034f662ac9071c36591bcc0cf5a6aaedfee617`. CRC, every member size and hash pass.
All original stage logs, the failed and successful bundle checks, tested source,
native/WASM snapshots, actual MCPB and helpers remain preserved. Version is
`0.2.0-alpha.1`; no preview tag/release or registry publication has occurred.
