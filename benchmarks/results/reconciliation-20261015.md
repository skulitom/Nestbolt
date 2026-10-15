# Repository reconciliation — 2026-10-15

Artem asked for a fresh review of changes made while this goal was idle, before
continuing. The primary checkout and `origin/main` were at `6c462c2`; no remote
main commits were missing. There were two independent local developments:

- `fix/separator-weight-cap`: `83aa089` caps Nestbolt's guided-search weights;
  `d740ac0` adds an upstream Sparrow issue draft. The active branch fast-forwarded
  to both commits, preserving their authorship. The draft has not been posted.
- `spike/jagua-2`: `7b8f7cb`, `ef1b83a`, `c691aed` contain an experimental engine
  port and its evidence. Only its Markdown/JSON report was copied byte-for-byte
  into this checkpoint, so existing references resolve. The local Sparrow copy,
  Cargo changes and solver port remain on the experimental branch. The separate
  worktree and unrelated untracked files were left alone.

## Release and registry

[Nestbolt v0.1.0](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0) was
published on 2026-10-14 at 09:08:47 UTC, tagged at `6c462c2`. The
[registry workflow](https://github.com/skulitom/Nestbolt/actions/runs/38540517654)
succeeded. A fresh read of the registry confirms version 0.1.0 is active, with
the Windows MCPB and SHA-256
`bf7d4235156f0325861a82ee771a0e8f3e9002a2672cde3796c161b34c8ce4b6`.
The [saved response](reconciliation-20261015/registry.json) records its
2026-10-14 09:12:25 UTC publication. Stale unpublished statements in STATUS.md
are corrected. This checkpoint creates no release or registry entry. The
published v1 benchmark remains build `75cbb32`, distinct from the software tag.

## Review and verification

The weight report's raw rows confirm 138 valid, repeatable development outputs,
64/65 identical layouts at 60 work-seconds, and four changed layouts at 300
work-seconds with unchanged sheet counts. The original 300-work-second runs used
CCD1, as documented; they are overflow diagnostics, not speed evidence. The cap
does not patch delegated upstream Sparrow. Its documented loss bound concerns
shop-scale geometry, not every extreme accepted by the public validator.

Fresh checks on the integrated code, using CCD1:

- Workspace: **238 passed**, zero failed, one existing ignored.
- Optimized CLI features: **21 passed**.
- Optimized Sparrow integration: **2 passed**.
- Strict workspace Clippy, formatting and `nestbolt-wasm` build: passed.
- Frozen shop inventory: **1,181 hashes unchanged**, original manifest SHA-256
  `02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`.

[Check records and logs](reconciliation-20261015/checks.json) retain source and
report hashes. No held-out geometry, labels or final results were read for tuning.
The previous checkpoint's [six CI jobs](https://github.com/skulitom/Nestbolt/actions/runs/38509975333)
all passed. Fresh CI for this checkpoint is separate from those results.

Work then resumed with [native lead-length calibration](h6-lead-native-calibration-20261015.md),
which found the arc-radius specification mismatch and led to Artem's approved
plan correction. N0/H1 remains the only completed v1.1 milestone: **15%**.
