# H4: collision-layout lifetime reduction — 2026-10-15

**Keep the memory reduction; H4 remains incomplete.** With one explicitly
selected search worker, both browsers now finish the frozen 2,000-part
letters/gears job inside the scale memory and responsiveness limits. The app's
unchanged default of two effective search workers still fails. Overall milestone
completion remains **20%** (H1 and H6).

[Measurements and integrity](h4-layout-lifetimes-20261015.json),
[baseline memory diagnosis](h4-curve-scale-20261015T175554Z/memory-diagnosis.json),
[one-worker result](h4-curve-scale-20261015T180917Z/summary.json),
[default-worker result](h4-curve-scale-20261015T181501Z/summary.json),
[repeatable comparisons](h4-lifetime-replay-20261015/summary.json),
[checks](h4-lifetime-checks-20261015/checks.json).

## Diagnosis and change

Baseline `52b0ecb` already has exact preview reuse and background ZIP generation.
A new Chrome diagnostic observes the memory metadata already returned by engine
workers, without parsing or copying their result strings. The browser harness
also records per-process memory and epoch timestamps, allowing memory samples to
be compared with import/nesting/export marks. Product code stays unchanged for
this diagnostic. The import utility finishes at 2,359,296 bytes of WASM memory;
the search worker finishes at 694,157,312 bytes. The 1,725,050,880-byte private
peak occurs during nesting, with 1,369,550,848 bytes in the busy renderer.
These measurements locate the remaining pressure; they do not identify every
native/browser allocation or prove that the entire peak belongs to WASM.

The sheet-window search cloned both its fixed sheets and working sheets, even
though it only read them. Each clone also cloned the collision index. It also
retained a full-width temporary layout, used only to measure the last sheet,
throughout the following search. The retained change borrows those sheet slices
and drops the temporary before constructing the search state. The fixed sheets
are still copied when a successful sheet elimination actually rebuilds the
window order. No geometry, search step, validation rule, random operation, work
coefficient, option default or production worker policy changes.

## Measurements on the same frozen job

Every browser run uses the actual app with Quick initial layout enabled, 500
copies each of the same two letters and two dense-polyline gears, 1250 × 2500 mm
sheets, 5 mm margins, 1.5 mm part/edge gaps, quarter turns, no mirror and a
60-second search budget. Explicit one-worker and default-worker runs are kept
separate. Browser trees use CCD0 cores 0/2; independent native checks use core 4.
Builds, tests and archive work use CCD1. All source/site/runner/fixture/pinned
executable guards pass. Chrome is 155.0.8059.41 and Firefox is 157.

| Browser / setting | Peak working set GB | Peak private GB | Maximum heartbeat ms | Maximum Long Task ms | Scale result |
|---|---:|---:|---:|---:|---|
| Chrome, before / one worker | 1.408 | 1.725 | 64.3 | 59 | Fail: private memory |
| Chrome, after / one worker | 1.206 | 1.228 | 106.7 | 60 | Pass at this setting |
| Firefox, after / one worker | 1.350 | 1.277 | 184 | unavailable | Pass at this setting |
| Chrome, after / default two | 1.573 | 1.789 | 130.9 | 53 | Fail: memory |
| Firefox, after / default two | 1.543 | 1.611 | 290 | unavailable | Fail: memory and responsiveness |

GB is decimal. The conservative 20 ms heartbeat includes every phase; no phase
is excluded and Firefox's unavailable Long Tasks API remains null. Native
validation and archive integrity are required in addition to these numbers.
The unchanged Workers field defaults to four on this machine, but the existing
large-job cap launches two search workers. Observed worker lifetimes confirm
three concurrent workers including the utility. The explicit one-worker runs
confirm two concurrent workers including that utility.

Chrome's completed search engine memory falls from **694,157,312 to
390,266,880 bytes**. Firefox's one search worker reports 399,310,848 bytes. The
new default two-worker run reports approximately 390/390 MB in Chrome and
399/400 MB in Firefox. These are per-engine linear-memory observations, not the
whole-process limits: the browser process totals remain the gate authority.
In the one-worker run, Chrome nesting peaks at 1.147 GB working set / 1.228 GB
private; Firefox nesting peaks at 1.078 / 0.966 GB. Export becomes the largest
working-set phase, at 1.206 GB in Chrome and 1.350 GB in Firefox.

One-worker Nest-to-result / export walls are 81.899 / 66.215 seconds in Chrome
and 83.062 / 63.743 seconds in Firefox. Default-worker walls are 80.111 / 61.783
and 83.935 / 63.791 seconds respectively. These are single-run development
observations, including final validation/serialization costs; this is not the
H4 quality matrix or a statistical speed claim.

## Geometry and repeatability

All five newly measured browser workflows finish with independently valid
2,000-part layouts on three sheets, 500 hole riders and normalized material
2.2468772308. The layouts remain byte-identical to the earlier result:
`e63e6ed152da3526feee8a9297c21c7c3b96f12ec14abf0e5e5ab9a26bc82873`.
Fresh native metrics agree exactly. Twelve SVG/DXF files across the two
one-worker browsers match their earlier baselines byte-for-byte; another twelve
in the default-worker runs match the new one-worker exports exactly.

Eight authored jobs cover discrete/free rotation with mirroring, window sizes
1/12, and seeds 0/1. Both binaries run the same 10-second repeatable-work budget
with a 60-second safety limit, on separate CCD0 physical cores (four at once).
All 16 outcomes validate independently and finish repeatably. Every one of the
eight before/after pairs has identical layout bytes, operation counts, work,
search statistics and the complete result excluding only elapsed wall time.
These bounded regression cases do not replace the 65-job/three-seed quality gate.

All **287 workspace tests pass** (one existing ignored test), and all **74
enabled browser tests pass** (four opt-in skips). Formatting, strict workspace
lint across all targets, release/WASM builds, product/test TypeScript, the Vite
build and both harness syntax checks pass. The native release binary hash is
`53c43910aee3cdc58f1e91b98c48baba1b2475aa03c2433546fbea417e1a1387`;
its per-run validator copies are independently pinned and guarded.

Three raw browser archives, the replay archive and five original check logs
preserve **181 members**, verified by CRC and SHA-256 before raw copies are
removed. Original failed outcomes remain failed, and all logs retain their raw
bytes. The frozen shop manifest hash is unchanged. No held-out geometry is read,
and no published v1 result, release or registry status changes.

Next, use the measured complexity/memory evidence to adjust the browser worker
policy and verify the original G5 workload remains unaffected. The current
one-worker success is not relabelled as a default-setting pass. H4 browser
quality, full G5 bounds and the 195-run native matrix remain outstanding.
