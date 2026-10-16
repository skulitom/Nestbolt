# H5 early exchange: isolated functional preparation — 2026-10-16

**The new call path works on authored tests; material improvement is unmeasured.**
The [previous pilot](h5-exchange-pilot-v2-20261016.md) failed its material limits
and recorded no exchange proposals. [Two diagnostic paths](h5-exchange-path-20261016.md)
never reached its late hook. This candidate instead tries one exchange at the
first feasible window state, before gap filling can bypass relocation. It shares
the existing ten-percent relocation opportunity, capped at 1.2 seconds, and
removes the old late hook. No overall search budget increases.

The baseline is current product `7eba929`, including the finer exact score bound.
Only `sheets.rs`, `sheets/vstrip.rs` and the isolated `exchange.rs` differ.
Both workspaces and Cargo target directories are separate; neither release
source nor measured engines change. Identical observation drivers use the public
preparation/search API and write counters only after search.

[Checks](h5-early-exchange-preparation-20261016/checks.json) record seven focused
debug tests, all 82 optimized core tests, strict core/example lint and formatting.
The added full-window test has a small part that fits an earlier gap: enabled
exchange proposes and accepts once, while disabled and expired cases do neither.
All resulting incumbents independently validate without increasing material.
Existing tests retain frozen-sheet, reflection, stock-defect, refused larger
return, failed repair and nonmutation checks.

The public API checks preserve ten observer outcomes and four CLI comparisons
on the same authored two-sheet job, seeds 0/1 and a 20-unit fixed-work budget.
Normal full results match baseline except elapsed wall time. Candidate common
results repeat exactly on replay, and standalone metrics agree exactly. These
small public cases record zero exchange proposals; they establish API consistency,
not the mechanical pilot's improvement or reachability.

Two setup failures remain preserved: the first test compile lacked an unchanged
authored example fixture, and the first public checker used the wrong field in
the cutting report. The fixture was copied unchanged into both workspaces.
The checker repair verified all completed file hashes and exact successful
commands before reusing those outcomes; it did not rerun completed searches.
No product fix or scoring exception was made for either setup error.

Baseline observer SHA-256: `74c1f44cf61d4c10c8767157efdbfc2c166ba18f4927a6ef4f29a0806a081d27`.
Candidate observer SHA-256: `ca0da4c3b9ddb9ccd70105581546dc1ed68bc3072669021f3ed66369cf3fa0b5`.

The [raw archive](h5-early-exchange-preparation-20261016/raw.zip) retains both
source trees, drivers/binaries, all checks, original failures and helpers:
478 members, 6,507,896 bytes,
SHA-256 `465aeb218d86a684194ad35298e1c20b04a069a6779398b746deb4973414fbeb`. CRC, member sizes and every hash pass.

The candidate remains unintegrated. A separately committed matched pilot must
wait until the current release comparison and scale sequence finish. No H5
quality claim, held-out input, gate threshold, release content or milestone
weight changes; completion remains 45%.
