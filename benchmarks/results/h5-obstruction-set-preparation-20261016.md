# Atomic obstruction-set exchange preparation — 2026-10-16

**All 85 optimized core tests, strict lint and authored public checks pass.**
No development quality measurement has started, and no exchange candidate is integrated.

The [stage diagnosis](h5-exchange-diagnosis-20261016.md) observed 35 receiving-sheet
repair failures among 37 proposals, all with two or three actual blockers while
the prior algorithm evicted only one. This candidate can move the full smaller
obstruction set together. Original single-victim alternatives remain. It ranks
proposals by remaining known blockers, then returned area and stable placement
order, retaining the six-proposal cap and at most three actual blockers.

The combined returned area must be smaller than the incoming part. Multiple
returned parts initially retain their relative placement, rotations and
reflections, translated to the incoming part's old origin. Both sheets still
need repair, followed by independent whole-job geometry/material validation.
The incumbent stays intact on failure. The early call, existing shared budget,
1.2-second cap, work coefficients, original geometry and public defaults remain.

Both baseline and candidate use the new tree-depth configuration; the candidate
alone adds the isolated exchange algorithm. Unique build targets prevent shared
cache confusion. New authored tests exercise atomic two- and three-blocker
transfers and rejection of a net area increase without mutation. Existing
expired/disabled, mirrored/frozen, failed-repair and defect tests also pass.

Public checks cover ten observer outcomes and four CLI comparisons on the same
authored 24-part request. Ordinary results agree exactly apart from elapsed wall
time; common-mode replays agree, with independent metrics/quantities validated.
These fixed-work functional checks do not establish material or speed gains.

The first isolated build omitted an existing authored test fixture and failed
to compile. Its log and failed state remain. The unchanged fixture was copied
into both isolated workspaces, after which all checks passed. No geometry or
test expectation was changed to obtain a pass.

[Checks](h5-obstruction-set-preparation-20261016/checks.json),
[build](h5-obstruction-set-preparation-20261016/build-v2.json),
[raw sources/binaries/logs](h5-obstruction-set-preparation-20261016/raw.zip),
[member verification](h5-obstruction-set-preparation-20261016/integrity.json).
CRC, every member size and SHA-256 pass. Production remains unchanged by this
experiment. A separately committed paired pilot must wait for the current H4
matrix and conditional scale sequence to finish and be sealed. Original H5
failures and all thresholds remain; completion stays 45%.
