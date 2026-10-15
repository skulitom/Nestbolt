# H4: automatic worker selection — 2026-10-15

**Both browsers pass the frozen curve-heavy scale workflow with automatic
worker selection.** The original G5 scale job also passes, retaining two search
workers and leaving Quick initial layout off. H4 remains incomplete on quality
and native development comparisons; completed milestone weight stays **20%**.

[Measurements and integrity](h4-worker-policy-20261015.json),
[H4 scale](h4-curve-scale-20261015T183542Z/summary.json),
[original G5 scale regression](h4-g5-scale-20261015T184142Z/summary.json),
[cutting-file comparison](h4-curve-scale-20261015T183542Z/export-comparison.json),
[checks](h4-worker-policy-checks-20261015/checks.json).

## Change and scope

Baseline `5adf8ad` reduced collision-layout lifetimes, but the unchanged default
two-worker curve-heavy run still exceeded memory limits. Browser worker selection
now counts polygon vertices across requested copies, including every component
and hole. At 500,000 vertices it caps the portfolio at one search worker. Below
that threshold, the existing cap of two workers above 1,000 copies remains;
smaller jobs retain their requested count. Unused library parts are excluded.
The app explains the effective worker count when it is below the requested count.

The frozen H4 drawing has 1,418,500 vertices across its 2,000 copies; original G5
has 190,500. The threshold is a conservative heuristic, not a universal memory
guarantee. Reducing portfolio workers can affect search quality, which still
requires the separate H4 quality gates. Native sources, WASM bytes, per-worker
solver defaults and work coefficients are unchanged. The requested Workers field
remains four on this machine; actual worker lifetimes confirm one search worker
for H4 and two for G5, plus the persistent utility worker.

## Actual browser workflows

Chrome 155.0.8059.41 and Firefox 157 import, nest and export through the actual app.
Both workloads use 500 copies of each of four parts, 1250 × 2500 mm sheets, 5 mm
margins, 1.5 mm part/edge gaps, quarter turns, no mirror and a 60-second search
budget. The H4 run enables the previously recorded Quick initial layout and
downloads Project ZIP. G5 keeps that option off and downloads all sheets ZIP.
Its SVG is byte-identical to published `75cbb32`, SHA-256
`64275515a7fdf12c57eca0f0a4da1aeae264e7495c87c36abd1d4b1948aaa966`.

| Workload / browser | Search workers | Peak working set GB | Peak private GB | Maximum heartbeat ms | Maximum Long Task ms |
|---|---:|---:|---:|---:|---:|
| H4 / Chrome | 1 | 1.198 | 1.261 | 68.1 | no entry |
| H4 / Firefox | 1 | 1.350 | 1.276 | 176 | unavailable |
| G5 / Chrome | 2 | 0.998 | 0.822 | 47.1 | no entry |
| G5 / Firefox | 2 | 1.030 | 0.927 | 81 | unavailable |

GB is decimal. Every workflow passes the unchanged 1.5 GB and 200 ms limits.
Chrome records no Long Tasks entry (the API reports tasks of at least 50 ms);
Firefox's unsupported API remains null. The conservative 20 ms heartbeat and
whole process-tree memory include every phase. G5 additionally uses the actual
Save button and captures that local project for independent validation; memory
and responsiveness include this step, while import/nest/export timings end at
their respective original boundaries. No upload is involved. This stronger
harness does not claim timing-method identity with the original G5 report.

H4 Nest-to-result / export walls are 79.859 / 58.009 seconds in Chrome and
81.982 / 62.553 in Firefox. G5 walls are 61.663 / 6.448 and 61.902 / 7.305 seconds.
These are single-run development observations, not statistical speed claims.
Browser trees are pinned to CCD0 cores 0/2; native validation uses core 4.
Builds, tests and archive preparation use CCD1. Product, runner, built-site,
fixture and pinned-executable guards pass.

## Fidelity and checks

Both H4 layouts contain all 2,000 parts on three sheets, including 500 hole
riders, with normalized material 2.2468772308. Layout bytes match the prior
explicit-one-worker run, SHA-256
`e63e6ed152da3526feee8a9297c21c7c3b96f12ec14abf0e5e5ab9a26bc82873`.
All twelve SVG/DXF comparisons also match byte-for-byte. Both G5 layouts validate
all 2,000 placements on three sheets with 500 hole riders; normalized material
is 2.1121886828 / 2.1144437608. Fresh native metrics agree exactly in all four
cases. G5 stochastic layouts are not claimed identical to earlier runs.

All **80 enabled browser tests pass**, with four opt-in skips. Six new browser
cases cover multipart/hole complexity, unused parts, the existing simpler-job
policy, the actual UI notice, worker launch count and cancellation cleanup.
Product/test TypeScript and production build pass. No native changes require
repeating the preceding 287-test workspace check.

Two raw archives preserve 62 members and five original check logs remain in
their own archive, all CRC/SHA-256 verified. An initial postprocessing step used
the wrong manifest directory after successfully archiving both runs; report
assembly was corrected from the unchanged archives. No measurement or outcome
was changed. The frozen shop manifest remains
`02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`.
Earlier failed runs remain failed and retained. No held-out geometry was read.

Keep the worker policy. Next run the eleven-job H4 browser/native quality subset,
the full G5 development comparison and the 195-run native matrix against the
published development baseline. No gate threshold, final acceptance, release,
registry publication or published v1 result changes.
