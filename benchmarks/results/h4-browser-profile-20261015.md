# H4 browser CPU profiles — 2026-10-15

Both diagnostic layouts independently validate. The letters profile identifies
collision scoring as a candidate for bounded evaluation; the gear profile is
dominated by edge/quadtree traversal. These profiles do not establish a speedup
or satisfy a browser quality, responsiveness or scale gate.

## Method and provenance

Unchanged product at `8b985b7`, source digest
`277762671b6163cf799b2d015c9fff8e94d2dd3e964555f50e8b47c60aef5ebc`;
thin-LTO WASM SHA-256
`1d3a89e263138279b6830e2b98334fa9ebc61fbc8677744b80e440f5fc83139c`.
An isolated local Chrome 155 page calls the same `nest_job` export on
`m-public-gear-1` then `example-letters`, seed 0, 60 seconds each. CDP samples
stacks at 1 ms. Both run sequentially on physical CCD0 CPU 8, with no process
affinity deviation. Main-page execution and sampling deliberately differ from
the G5 app-worker method. No reserved geometry is opened.

All original-job checks pass, including the letters' actual public
library/request. Saved and standalone metrics agree exactly. Product, executable,
binding, runner and input guards remain unchanged. The ACPI temperature query is
denied; the recorded 4201 MHz clock is not a temperature measurement.

## Sample attribution

Function shares aggregate every sampled call node with the same function name.
The complete original profiles remain available, including their timing gaps.

| Job | Profile span | Sum of sample deltas | Samples | Largest self-time shares |
| --- | ---: | ---: | ---: | --- |
| gear-1 | 60.296467 s | 42.588584 s | 13,935 | edge/quadrants 55.475709%; quadtree collection 24.320550%; Clipper execution 5.413289% |
| letters | 59.982087 s | 59.981924 s | 13,469 | weighted collision callback 54.915851%; polygon/point containment 17.074464%; quadtree collection 13.463931% |

Gear-1 has an unexplained 17.707883-second gap between its profile span and
sample deltas. The shares describe **sampled time**, not complete wall-time
attribution. Letters has a 0.000163-second difference. Profiling does not justify
changing geometry, approximation tolerances or search settings.

## Evidence

[Plan and guards](h4-browser-profile-20261015T213149Z/plan.json),
[results](h4-browser-profile-20261015T213149Z/results.json),
[all-node aggregation](h4-browser-profile-20261015T213149Z/aggregate.json),
[execution](h4-browser-profile-20261015T213149Z/execution.json),
[environment](h4-browser-profile-20261015T213149Z/environment.json).

The [raw archive](h4-browser-profile-20261015T213149Z/raw.zip) retains both full
CPU profiles, layouts, search/validation outputs, original runner snapshots and
the isolated site/bindings: 26 members, 1,319,459 bytes. SHA-256:
`d92433ab48a7a534a29cdeeb924de8ec3b47e02264b3ac0e4c5f4dbc9fb60b52`.
CRC and every member SHA-256/size were verified before consolidating the loose
raw files; [integrity inventory](h4-browser-profile-20261015T213149Z/integrity.json).

H4 remains open. Completed milestone weight stays 45%; published v1 results and
all acceptance thresholds remain unchanged.
