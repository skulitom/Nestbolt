# N1 segment cleanup checkpoint — 2026-10-13

**H2 is not complete. Overall milestone completion stays 15%.**

Exact duplicate and zero-length segments are removed before joining. Reversed
lines/Béziers count as duplicates; circles and nonempty closed Bézier loops remain
curves. Overlapping collinear lines merge into their union, with original extreme
endpoints retained. Candidate bins are only a broad phase: both endpoints must be
collinear to numerical precision (1e-9 mm); this does not use the larger silent
join or explicit gap-repair tolerances. Reassembled pieces retain source order
where continuous, preserving the existing relief-loop handling.

All import reports include duplicate, zero-length and overlap counts. UI displays
the counts per file; CLI and MCP return them. Nonzero cleanup is also a message.
Layer/colour filtering precedes cleanup.

## Training and robustness

[Training report](h2-import-training-20261013T185545Z.json), frozen training
vectors only; no held-out reads:

| Set | Imported | Rejected | Matching part/hole counts |
| --- | ---: | ---: | ---: |
| Generated | 170 | 0 | 170/170 |
| Real | 55 | 4 | 51/59 |
| Native DXF/SVG | 24 | 4 | 24/28 |
| Total | 249 | 8 | **245/257** |

This improves the preceding 221/257 and original 165/257 count diagnostics. The
four native rejections are pre-frozen malformed negative fixtures. Remaining real
issues include two legacy-encoded DXFs, three partially imported negative fixtures
and one topology/count mismatch. Count matching is not H2 acceptance: exact cut
selection, warning quality and independent curve re-export fidelity still need
their checks. Native project files need N2.

[Robustness](h2-import-robustness-20261013T185642Z.json): 183 attempts, 82 imported,
101 rejected, no panic or timeout; slowest 0.857 s. Each native process has a
10-second limit and runs on its assigned CCD0 physical core (0/2/4/6), at most four
at once. Product and runner hashes stayed unchanged during each recorded run.

The [first cleanup diagnostic failed in the harness](h2-cleanup-harness-failure-20261013T185419Z.json)
after 224 completed rows: assigning affinity after spawn raised AccessDenied for
a PID that no longer existed when checked, consistent with a fast-exit race. Its
partial output is retained. The Windows runner now creates the owned child
suspended, sets its affinity before any import work, then resumes it. Setup
failure kills/reaps that child. The complete replacement above used the same
product executable; it was not an importer failure. Earlier after-spawn timing
diagnostics remain historical and are not final H2 timing evidence.

## Verification

- Core library suite: 34 passed, one pre-existing ignored test; all four gap and
  six layer/style/block tests pass with cleanup enabled.
- Four cleanup tests pass, including 1,024 randomized shuffled overlap/duplicate/
  zero-segment cases. These are not the full planned 10,000-case habit/fuzz gate.
- CLI cleanup and MCP stdio import/nest/export tests pass.
- Chromium and Firefox: 8/8 gap, selection, inventory and cleanup tests pass.
- Production WASM/web build and schema generation pass. Strict Clippy initially
  requested an array in the randomized test; that test-only allocation change
  resolves the lint and Clippy passes. Product code is unchanged by that fix.

Full H2 fidelity, units/encoding improvements, complete fuzz coverage, export
palette and native LightBurn evidence remain pending. Held-out scoring remains
awaiting clarification; the split and frozen files remain unchanged.
