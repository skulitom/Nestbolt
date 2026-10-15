# H4 early initial layout — 2026-10-15

An opt-in rectangle start gives the frozen 2,000-part letters/gears job a valid
initial native layout in **7.379682 seconds**, versus 138.213 seconds in the
earlier 300-second diagnostic. Both browsers now finish and export all 2,000
parts, but **H4 still fails memory and responsiveness**. The browser runner also
retains a failed validator-binary guard; its saved outputs were checked again
separately. Overall v1.1 completion stays **20%** (H1 and H6).

Baseline commit: `e14973b`. [Machine-readable record](h4-quick-start-20261015.json),
[frozen fixture](../datasets/browser-curves/README.md),
[earlier failure and native diagnosis](h4-curve-scale-baseline-20261015.md).
No held-out geometry, published v1 results, gate thresholds or defaults change.

## Isolated hypothesis

[Six original-geometry-validated trials](h4-rectangle-probe-20261015T161910Z/results.json)
run the existing rectangle packer before ordinary construction, with its existing
3% operation allocation from a 60-second budget, seeds 0–2. Without hole grouping,
initial packing plus validation takes 6.441–8.548 seconds and material is
2.4267092368. With the existing grouping, 500 hole riders are retained, totals are
9.969–10.901 seconds, and material is 2.2468772308 in every seed. Packing itself
takes 0.360–0.488 seconds; original-geometry validation dominates. Every layout
also passes a fresh public CLI check, with zero metric difference. These are
isolated incumbent probes, not complete solver or H4 quality results.

The retained implementation exposes **Quick initial layout** in Advanced,
`--quick-start` for CLI nesting and sheets, and `quick_start: true` in shared
requests, including MCP. It is false by default and saved with the project.
Successful rectangle starts skip ordinary initial construction and continue
through the usual search. Unsupported stocks, rotations or unsuccessful trials
fall back to construction. Source preflight, stock caps, rotation/mirror rules,
original-geometry validation and work-budget reporting remain in force.
The option can change material quality; published default schedules and work
coefficients are unchanged.

## Complete native run

The [public CLI run](h4-quick-native-20261015T163504Z/result.json) uses the frozen
job, seed 0 and a 60-second search budget on CCD0 physical core 0. It returns
2,000 valid placements on three sheets, including 500 hole riders, material
2.2468772308. Reported solve time is **69.287 seconds**, including final checks;
the complete process with SVG/DXF exports takes **90.719 seconds**. This is not
a claim of a strict 60-second end-to-end finish. Fresh validation takes 9.320
seconds and agrees exactly. Product sources stay unchanged throughout this run.
The six large cutting files are retained in a hash/CRC-checked
[export archive](h4-quick-native-20261015T163504Z/exports.zip).

## Actual browser workflow

The [browser record](h4-curve-scale-20261015T164016Z/summary.json) uses the same
immutable geometry and settings as the baseline: 1250 × 2500 mm sheets, 5 mm
margins, 1.5 mm spacing/edge gap, quarter turns, no mirrors, a 60-second search
budget and the default two effective workers. The only workflow change is
checking Quick initial layout. The complete browser tree is pinned to physical
cores 0 and 2; independent native checks use a separate core. Builds and tests
use CCD1.

| Measurement | Chrome 155.0.8059.41 | Firefox 157 |
| --- | ---: | ---: |
| Import | 0.537 s | 1.633 s |
| Nest button to final result | 159.730 s | 115.973 s |
| Export and saved download | 87.776 s | 89.726 s |
| Peak process-tree working set | 2.190 GB | 2.123 GB |
| Peak process-tree private memory | 3.197 GB | 2.023 GB |
| Maximum main-thread Long Task | 2,856 ms | API unavailable |
| Maximum 20 ms heartbeat gap | 2,861.8 ms | 1,620 ms |
| Saved project ZIP | 139,495,128 bytes | 139,495,125 bytes |
| Layout | 2,000/2,000 valid, three sheets | 2,000/2,000 valid, three sheets |

Both layouts have the native material 2.2468772308, with identical saved layout
hashes and zero difference on independent metrics. All sheet SVG/DXF entries
exist and ZIP CRC checks pass. Neither browser meets the 1.5 GB / 200 ms limits.
The measured button-to-result times include substantial work beyond the nominal
search budget; no interval is excluded to improve the result.

The original runner ended nonzero at its final guard because concurrent
optimized CLI feature tests rebuilt `target/release/nestbolt.exe`. The
[guard failure](h4-curve-scale-20261015T164016Z/guard-failure.json) records the two
binary hashes. Product sources, browser assets, fixture and both runners were
unchanged. Original case outcomes and the failed overall run are preserved;
there is no original passing `results.json`. A
[separate recheck](h4-curve-scale-20261015T164016Z/validation-recheck.json), after
all builds ended, pins one executable copy and validates both saved layouts
again with unchanged source/binary guards and zero metric difference. That
confirms the saved geometry, not an H4 pass or a replacement browser run.
Future measured runs must start after optimized CLI tests have finished, as
those tests can rebuild the standalone executable.

Chrome records repeated roughly 0.5-second tasks during the live preview, a
1.608-second task around the final preview and a 2.856-second task at download
assembly. Source inspection identifies repeated full-vertex extent calculations,
per-placement SVG path construction and synchronous ZIP assembly as the next
testable causes. Caching exact preview geometry and moving download assembly
off the main thread remain hypotheses, to be measured separately. Worker memory
also needs attention. The H4 browser quality and 195-run native matrix remain
outstanding.

## Verification and retained failures

[Checks](h4-quick-start-checks-20261015/checks.json): 287 workspace tests pass
(one existing ignored), followed by two focused core tests on the final source
preflight addition; all 24 optimized CLI feature tests and 60 enabled Chromium /
Firefox tests pass (four opt-in cases skipped). MCP uses a real stdio child;
browser tests cover opt-in defaults, nesting, saved requests, ZIPs and reopening.
Strict Clippy, formatting, generated schema consistency, TypeScript test checking,
release CLI/MCP and final WASM/browser builds pass. The earlier compile failure
and undersized authored test fixture remain recorded. The frozen scale fixture
was not adjusted. The shop manifest checksum remains
`02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`.

The native and browser archives preserve original outputs, failures, telemetry,
screenshots and hashes. Agent-facing documentation now also reflects the already
published v0.1.0 and completed G7 evidence. No new final acceptance, release or
registry publication occurred.
