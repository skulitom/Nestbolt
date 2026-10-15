# H4 curve scale: initial-packing baseline

H4 remains open. The required letters/gears workload now has a frozen fixture
and a browser harness that records failures, memory and responsiveness across
import, nesting and export. This is development evidence, not a new published
quality claim or a final held-out run. Production code and defaults are unchanged.

## Browser outcomes

The [original run summary and raw archive](h4-curve-scale-20261015T154705Z/summary.json) pins
commit `c6ec635`, product sources, native validator, built site, fixture and both
harness files. Source guards pass at completion. All four shapes import, then
both browsers display: “no complete layout within 60 s: these parts are many or
detailed; allow more time.” Neither reaches export.

| Browser | Import | Peak working set | Peak private | Longest recorded task | Largest heartbeat gap | Scale |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Chrome 155.0.8059.41 | 0.291 s | 0.867 GB | 0.620 GB | 0 ms observed | 38.9 ms | Fail: initial packing |
| Firefox 157.0 | 0.700 s | 0.923 GB | 0.813 GB | Unsupported | 99 ms | Fail: initial packing |

Chrome's zero means no Long Tasks entry was observed, not zero processing time.
Responsiveness and memory only cover the reached phases; they provide no claim
about the unfinished preview/export phases. Process wall times of 603.56 and
603.49 seconds include the harness's delayed error detection described below.

## Workload and method

The [fixture](../datasets/browser-curves/manifest.json) uses 500 copies each of
two quadratic-curve letters and two dense-polyline gears from the shipped,
licensed examples. Its SHA-256 is
`f95f04ab7ab8a077e78da706aabb29aac85c978351944eff752ec80b7b2e04f2`.
The four outer proxies have 527, 224, 792 and 792 vertices, with 0, 2, 1 and 1
holes. Original source paths are retained. No held-out geometry is read.

The actual browser app imports the SVG, sets quantities to 500 and nests on
1250 × 2500 mm sheets with 5 mm margins, 1.5 mm part/edge spacing, quarter turns,
no mirror and 60 seconds. The default four-worker selection becomes two workers
for this quantity. Chrome and Firefox run sequentially, with each browser's
whole process tree restricted to physical cores 0 and 2. Memory samples every
0.2 seconds sum browser process working sets and private bytes; shared working
set pages can therefore count more than once. Both must stay below 1.5 GB.

Chrome Long Tasks entries and a 20 ms event-loop heartbeat cover the entire
workflow. Firefox does not support Long Tasks, so its missing measurement is
recorded as null, not zero; heartbeat gaps conservatively require at most 200 ms.
A completed case must download the Project ZIP containing all sheet SVG/DXF
files and pass fresh native validation of all 2,000 placements and metrics.
This tests the public workflow rather than injecting a layout into the app.

The first harness waits up to 600 seconds for a successful summary even when
the app has already reported a search failure. Its raw output is retained;
this wait must not be interpreted as 600 seconds of solver work. The next
harness revision records a visible app error immediately. Its
[same-workload verification](h4-curve-scale-20261015T160804Z/summary.json) captures
the same failures after 59.865 seconds in Chrome and 59.942 seconds in Firefox
from pressing Nest. Whole process times fall to 62.33 and 62.51 seconds. Memory
peaks are 0.857/0.895 GB working set and 0.626/0.781 GB private; heartbeat maxima
are 33.3/67 ms. Product, binary, built-site and fixture hashes are identical
between the two batches. Only harness error detection and success-path request
assertions change. The original delayed observations remain intact.

## Diagnosis

The unchanged native CLI also fails the same job at 60 seconds (59.803 seconds
process wall time), with the actionable message that many or detailed parts
need more time. A separate zero-rotation shelf construction demonstrates
feasibility: all 2,000 original parts fit three sheets and pass the independent
validator, including requested spacing and margins. This manually assembled
diagnostic is not a solver result or an H4 pass.

The [60-second native failure](h4-curve-native-diagnostic-20261015T155538Z/result.json)
and [shelf validation](h4-curve-shelf-diagnostic-20261015T155839Z/validate-stdout.json)
retain their inputs and original output. Shelf normalized material is
2.4630180004; geometry validation takes 5.02 seconds. Shelf assembly takes about
0.003 seconds in this diagnostic, excluding import and validation, and uses
1.52 mm bounding-box gaps to cover the requested spacing plus curve tolerance.

A 300-second native diagnostic is retained separately from the 60-second gate.
Its logs show grouping at 0.53 seconds and model preparation at 0.97 seconds.
Initial construction takes about 129 seconds, validation about 133 seconds,
and the first offered warm layout arrives at 138.21 seconds. This separates
slow placement construction from import/model preparation.

The longer run finishes with 2,000 valid placements on three sheets, including
500 hole riders, and normalized material 2.2468772308. The search reports
306.77 seconds including final geometry checks; the complete CLI process with
exports takes 322.06 seconds. A fresh native validation takes 6.60 seconds and
matches every saved metric exactly. All six SVG/DXF exports are retained in a
24.4 MB [verified archive](h4-curve-native-diagnostic-20261015T155742Z/exports.zip),
with member hashes in the [verification record](h4-curve-native-diagnostic-20261015T155742Z/verification.json).
These longer-run results do not satisfy the failed 60-second scale case.

The existing conservative rectangle packer currently runs only after the
ordinary constructor has completed. A bounded early incumbent is therefore a
testable next hypothesis. It must preserve original-geometry validation,
rotation permissions, stock caps and existing layouts that already fit. Any
change affecting benchmark defaults stays behind an explicit option under the
plan's stop rule. No such solver change is integrated at this checkpoint.

The complete original browser records are retained in each run’s `raw.zip`,
including every telemetry sample, screenshot, log, original result and harness.
Each `summary.json` omits duplicated telemetry arrays and lists the archive and
every member hash. Archiving changes no outcome or measurement. The
[integrity record](h4-curve-scale-baseline-20261015.json) covers both archives.
