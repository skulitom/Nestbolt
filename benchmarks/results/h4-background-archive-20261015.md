# H4: one-worker diagnosis and background archive generation — 2026-10-15

**Retain background archive generation; H4 remains open.** Both browsers export
all 2,000 parts with the same original cutting-file bytes, while the export
heartbeat gap falls from 2,614/1,621 ms to 52/51 ms. Chrome still exceeds the
1.5 GB private-memory limit during nesting. Firefox stays within both memory
limits but records a 202 ms nesting heartbeat gap, above the unchanged 200 ms
limit. Completion remains **20%** (H1 and H6).

[Measurements and integrity](h4-background-archive-20261015.json),
[one-worker diagnostic](h4-curve-scale-20261015T172452Z/summary.json),
[background archive run](h4-curve-scale-20261015T174342Z/summary.json),
[phase comparison](h4-curve-scale-20261015T174342Z/phase-comparison.json),
[checks](h4-archive-checks-20261015/checks.json).

## Two separately measured changes

Baseline `5256b78` already includes exact preview reuse and the optional Quick
initial layout. First, the actual app runs with its Workers field explicitly
set to one. The previous default was two effective search workers on this
2,000-part job. This is a recorded diagnostic override; the production worker
heuristic is unchanged. Actual worker lifetimes confirm one utility worker and
one search worker, rather than inferring the count from the field alone.

Second, with that same explicit one-worker setting, Project ZIP and Download
all sheets move to a short-lived module worker. It calls the same independently
validating WASM exporter, encodes one file at a time, and retains immutable Blob
pieces. The final ZIP is a composite Blob, avoiding a second contiguous copy of
the entire archive. The main thread receives that Blob; all output strings,
encoding and CRC work stay in the worker. The worker terminates after success,
validation failure or a messaging error. Individual-file exports retain their
existing path. LightBurn archive format selection, preserved-project naming and
separate lead cutting files are unchanged.

No native source, WASM binary, proxy geometry, search schedule, published work
coefficient or default worker setting changes in this checkpoint. Both runs use
the frozen letters/gears fixture, 500 copies of each part, 1250 × 2500 mm sheets,
5 mm margins, 1.5 mm part/edge gaps, quarter turns, no reflection and a 60-second
search budget. Quick initial layout is explicitly enabled, as in the preceding
comparison. The browser process tree uses CCD0 cores 0 and 2; independent native
validation uses core 4. Checks/builds and archive preparation use CCD1.

## Whole-workflow measurements

| Browser / configuration | Peak working set GB | Peak private GB | Nest heartbeat ms | Export heartbeat ms | Whole scale pass |
|---|---:|---:|---:|---:|---|
| Chrome, preview cache / two workers (earlier) | 2.099 | 2.569 | 209.2 | 2,801.0 | No |
| Chrome, one worker / old archive | 1.759 | 1.805 | 108.3 | 2,613.6 | No |
| Chrome, one worker / background archive | 1.419 | 1.822 | 99.4 | 51.6 | No: private memory |
| Firefox, preview cache / two workers (earlier) | 2.074 | 1.977 | 370 | 1,569 | No |
| Firefox, one worker / old archive | 1.611 | 1.539 | 308 | 1,621 | No |
| Firefox, one worker / background archive | 1.368 | 1.389 | 202 | 51 | No: responsiveness |

GB means decimal 1,000,000,000 bytes. Chrome is 155.0.8059.41; Firefox is 157.
Chrome's maximum Long Task falls from 2,588 ms in the one-worker old archive run
to 68 ms overall, with no export Long Task entry. Firefox does not expose the
Long Tasks API; its unavailable value stays null. The conservative 20 ms
heartbeat still gates both browsers without removing setup, preview or export
intervals. Firefox's 202 ms sample remains a failure, not a rounded pass.

In the new Chrome run, the private peak is at case time 33.29 seconds and the
working-set peak at 64.19 seconds, both during nesting, before export begins.
This distinguishes the remaining search/preview memory problem from archive
assembly. The retained raw samples use a different clock origin from browser
phase marks; these observations do not claim exact synchronized boundaries.

Observed Nest-to-result / export walls are 97.438 / 87.130 seconds before and
82.315 / 65.064 seconds after in Chrome; Firefox records 98.430 / 86.878 and
82.324 / 66.911 seconds. These are single-run development observations. The
nesting path did not change between these two runs, so its timing difference is
not attributed to the archive lever or presented as a statistical speed claim.

## Geometry, provenance and checks

All four saved layouts validate independently with 2,000 placements, three
sheets, 500 hole riders and normalized material 2.2468772308. Every reported
metric matches fresh native validation with zero difference. All four layout
files have SHA-256
`e63e6ed152da3526feee8a9297c21c7c3b96f12ec14abf0e5e5ab9a26bc82873`.
The six SVG/DXF files per browser are byte-identical before/after: twelve exact
cutting-file comparisons. All expected ZIP members exist and CRCs pass.

Both source/fixture/runner/site/executable guards pass. The harness now copies
the native validator to a unique run directory before measurement and guards
that exact executable. Its hash is
`fc0c7f6fbd64a4775a53781a34caae64dae9c70ac0ed0651fd3bc8a448e4a908`.
This prevents an unrelated optimized CLI test build from replacing the binary
being measured; it does not weaken the guard or relabel any earlier failure.
The runner records the source executable, copy and original hash.

All **74 enabled browser tests pass**, with four opt-in tests skipped. New
coverage compares incremental ZIP bytes with the existing encoder (Unicode,
empty files, binary views and immutable Blob ownership), checks actual Project
ZIP/all-sheet exports against individual downloads, and verifies that invalid
saved placements are rejected without a download and the worker closes.
Existing LightBurn, leads, common-line and project reopening tests also pass.
Product/test TypeScript, production build and both harness syntax checks pass.
Native sources are unchanged, so native tests were not rerun for this UI change.

Original telemetry, screenshots, project ZIPs, failed gate outcomes and native
validation records are retained in two verified raw archives. Six original
check logs are archived without newline normalization. Member SHA-256 and CRC
checks cover all 66 recorded files. The frozen shop manifest checksum is
unchanged. No held-out geometry or final acceptance data is used.

Keep the archive change. Next profile search-worker memory and the remaining
Firefox live-preview/heartbeat delay. One-worker results alone do not justify a
new production heuristic or complete the default scale gate. Browser quality,
the full G5 bounds and the 195-run native matrix still need evidence. No gate
threshold, published v1 result, release or registry status changes.
