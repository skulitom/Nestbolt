# H4 current-build scale confirmation — 2026-10-15

**All four browser workflows pass.** The retained bounded-score build imports,
nests and exports 2,000 parts in Chrome and Firefox on both the required
curve-heavy drawing and the original G5 scale drawing. This confirms scale;
H4 remains open on the complete development comparisons and requirement review.
Completed milestone weight remains **45%**.

[Checks and exact hashes](h4-current-scale-20261015/checks.json),
[curve-heavy results](h4-curve-scale-20261015T222652Z/summary.json),
[original G5 results](h4-g5-scale-20261015T223221Z/summary.json).

## Build and unchanged method

The product is the retained `a977279` implementation, measured after plan
commit `b000052`. Product source SHA-256 is
`921ad6f59b0dae0b243ba9cd8e98a03dd4d6a3b6404d4e4251414105f26beb7c`;
the combined CLI/MCP build supplies validator
`5e07f350761f3b5dfb820e404c85982dacd039d0789b8bfca63f66e76bf20bf7`.
WASM remains `ac41d7d205813df71c9a5b8648877b1c5170da2654c312a6e3cf5dcc19474cf8`.
No product, runner, built-site, executable or input guard changed during either run.

Both fixtures request 500 copies of four parts, 1250 × 2500 mm sheets, 5 mm
margins, 1.5 mm part/edge spacing, quarter turns, no mirror and a 60-second
search budget. Curve-heavy scale enables Quick initial layout, uses one
automatically selected search worker and downloads Project ZIP. Original G5
keeps quick start off, uses two search workers and downloads all sheets ZIP,
then captures the actual saved UI project for independent validation. The
requested Workers field remains four; maximum simultaneous workers of two/three
include the persistent utility worker.

Chrome 155.0.8059.41 and Firefox 157.0 use physical CCD0 CPUs 0/2; standalone
validation uses CPU 4. Runs are sequential and record zero affinity deviations.
Report preparation and archive verification use CCD1. Browser process-tree
working set and private memory are sampled every 200 ms throughout the workflow.
The 20 ms UI heartbeat includes import, nesting, export and the G5 save step.

## Outcomes

| Workload / browser | Peak working set GB | Peak private GB | Maximum heartbeat ms | Maximum Long Task ms | Nest / export seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Curves / Chrome | 1.257 | 1.223 | 87.8 | no entry | 80.723 / 60.398 |
| Curves / Firefox | 1.352 | 1.275 | 175 | unavailable | 83.188 / 62.811 |
| G5 / Chrome | 1.013 | 0.843 | 62.6 | no entry | 61.585 / 6.269 |
| G5 / Firefox | 1.033 | 0.922 | 99 | unavailable | 61.968 / 7.358 |

GB is decimal. Every peak is below 1.5 GB and every measured heartbeat gap is
below 200 ms. Chrome reports no Long Tasks entry; Firefox does not support that
API, so its result remains null and the heartbeat provides the conservative
responsiveness check. The displayed nest durations include work around the
requested search budget and are not claimed to be 60-second end-to-end walls.
These single observations establish no statistical speed claim or general
memory guarantee for other geometry.

All four layouts contain exactly 2,000 placements on three sheets and pass the
standalone validator, with exact metric agreement. Both curve-heavy layouts have
normalized material 2.2468772308 and retain all original curves and dense gear
polygons. Their layout bytes and all twelve SVG/DXF files are identical to the
previous passing worker-policy measurement. G5 material is 2.1193699332 in Chrome
and 2.1152312608 in Firefox; no identity claim is made for those stochastic layouts.

[Chrome curve-heavy screenshot](h4-curve-scale-20261015T222652Z/chrome/screen.png),
[Firefox curve-heavy screenshot](h4-curve-scale-20261015T222652Z/firefox/screen.png),
[Chrome G5 screenshot](h4-g5-scale-20261015T223221Z/chrome/screen.png),
[Firefox G5 screenshot](h4-g5-scale-20261015T223221Z/firefox/screen.png).

## Preservation and remaining work

Two archives preserve all 68 raw members, including the original full telemetry,
exports, layouts, validation results, plans and runner snapshots. Every member's
size/SHA-256 and each archive's CRC were verified before consolidating loose files.
The curve-heavy archive is 50,323,711 bytes,
SHA-256 `5f309ac2365747bef0d441ad639e5a8f6b3e81732f031ad39f5e945c39454904`;
the G5 archive is 3,220,582 bytes,
SHA-256 `5e93390519c97253fea78e114ba51d600a992fb5a8d6377bcfad0d1a0958ee9b`.
Frozen shop manifest and previous failures remain unchanged.

The [complete development comparison](h4-full-development-20261015/plan.json)
was committed before measurement and has now started: 699 new attempts plus
81 verified matching subset results, with all original thresholds retained.
Its [environment record](h4-full-development-20261015/session-environment.json)
records unavailable temperature telemetry: ACPI access was denied and neither
hardware-monitor provider was present. The reported 4201 MHz clock is not a
temperature reading. No held-out geometry, published v1 result, release or
registry publication is part of this checkpoint.
