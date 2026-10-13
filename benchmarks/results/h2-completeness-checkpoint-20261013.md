# N1 incomplete-drawing checkpoint — 2026-10-13

**H2 remains incomplete; overall completion stays at 15%.**

UI, CLI and MCP now reject a nesting-library import if selected cutting paths
remain open. The error gives the count, up to four endpoint locations and gap
sizes, and either an explicit Close gaps value or a source-edit instruction.
It also explains excluding score/construction layers. Low-level imports retain
partial geometry and the complete structured report for inspection. Empty or
degenerate drawings now explicitly request repaired closed, nonzero-area cuts.

Browser imports remain atomic across a selected batch. A failed re-import removes
those files' previous parts and invalidates the old layout; unrelated files stay
available. This also applies when byte decoding or XML inspection fails before
geometry import. Successful explicit repair can then restore the complete file.

## Training and robustness

[Final training diagnostic](h2-import-training-20261013T193805Z.json): 257 training
DXF/SVG files, **246 imports, 11 rejections, 245 exact part/hole-count matches**.
All 170 generated files match. All nine negative vector fixtures now reject.
The two additional rejections are `native/lb-14.dxf` and `.svg`: each contains
four selected open paths with gaps from about 0.0063 to 0.0099 mm and receives
an explicit repair instruction. The frozen labels/options were not changed.

The sole imported count mismatch is [R43's duplicate-cutout label discrepancy](h2-r43-label-discrepancy-20261013.md).
The prior diagnosis of a missing physical island was incorrect: two cutouts
differ by only 6.96e-13 mm. Source and label remain frozen; an exception is
awaiting Artem's decision, and the failure still counts. Thus this diagnostic
does not establish H2, even before the remaining cut-layer, warning, native-project
and fidelity requirements are considered.

[Final robustness diagnostic](h2-import-robustness-20261013T193814Z.json): 183
attempts, **35 imported, 148 rejected, no crash/panic/timeout**, maximum 1.331 s.
The stronger completeness rule rejects files that previously returned partial
geometry. Four processes at most, each pinned before execution to its own CCD0
physical core, with a ten-second limit. Source hashes stayed unchanged.

The [first training run](h2-import-training-20261013T193555Z.json) and
[first robustness run](h2-import-robustness-20261013T193601Z.json) remain recorded.
They preceded the final empty-drawing repair wording and have the same outcome
counts. Both final reports pin the product source and binary hashes. No held-out
geometry or label was read. The 1,181-file frozen integrity check passed.

## Checks and remaining work

- Full workspace suite: 158 tests passed, one existing test ignored. The final
  empty-drawing wording change was followed by all five focused gap tests.
- CLI and MCP exercise a file with both a complete outline and an open cut,
  reject it, then import both outlines with explicit repair.
- Chromium and Firefox: 12/12 focused import checks passed, including batch
  atomicity, malformed replacement, layer/colour selection and units.
- Strict Clippy, formatting checks and the final production WASM/web build pass.

Next requirements include complete selected-geometry/fidelity auditing, the
10,000-case habit fuzz gate, existing-nest sheet selection, export palette and
native LightBurn checks. N2 native-project support is still required for the
whole H2 corpus. The held-out negative-fixture scoring question is also pending;
no denominator, threshold or split has been changed.
