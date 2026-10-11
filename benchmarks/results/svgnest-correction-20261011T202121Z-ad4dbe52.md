# SVGnest export precision correction

All saved SVGnest preparation and pilot results. Mixed budgets/settings; this is an output-decoder audit, not a quality comparison.

Chromium SVGMatrix rounded translations to float32. Decode original native SVG transform attributes at full Python float precision.

Search was not rerun. Original run records and their outcomes remain unchanged. All selected native exports were revalidated, including previously valid ones.

| Original run | Job | Old outcome | Corrected outcome | Corrected material |
| --- | --- | --- | --- | ---: |
| 20261011T193059Z-e7f62151 | b-fu-nest-mb-given | valid | valid | 3.666666667 |
| 20261011T193107Z-84d7d464 | svgnest-hole-margin-smoke | no_layout | no_layout | — |
| 20261011T193321Z-1060b268 | svgnest-hole-margin-smoke | valid | valid | 0.135000000 |
| 20261011T193530Z-16bffdf0 | m-box-mini | no_layout | no_layout | — |
| 20261011T193539Z-700edbd3 | svgnest-hole-margin-smoke | valid | valid | 0.190000000 |
| 20261011T194221Z-d3b42bd5 | svgnest-independent-edge-gap | valid | valid | 0.195000000 |
| 20261011T194237Z-1fcb9046 | svgnest-stock-cap-failure | invalid | invalid | — |
| 20261011T194257Z-998a7ee8 | b-fu-nest-mb-given | valid | valid | 3.666666667 |
| 20261011T194407Z-b8b88baf | m-box-mini | failed | failed | — |
| 20261011T194437Z-9c7a0451 | svgnest-independent-edge-gap | failed | failed | — |
| 20261011T194515Z-8cf530ee | svgnest-independent-edge-gap | valid | valid | 0.195000000 |
| 20261011T194540Z-321e6a09 | m-box-mini | no_layout | no_layout | — |
| 20261011T194801Z-d25fa363 | b-fu-nest-mb-given | valid | valid | 3.666666667 |
| 20261011T194926Z-1fb80e38 | svgnest-stock-cap-failure | invalid | invalid | — |
| 20261011T195255Z-17bbcda0 | b-albano-nest-mb-free | invalid | valid | 2.563612393 |
| 20261011T195400Z-c515cc6c | b-albano-nest-mb-given | valid | valid | 2.902177555 |
| 20261011T195505Z-c3c40163 | b-albano-strip-sheet | valid | valid | 1.780248114 |
| 20261011T195610Z-7de05666 | b-blaz1-nest-mb-free | valid | valid | 15.533333333 |
| 20261011T195716Z-1368c5b1 | b-blaz1-nest-mb-given | valid | valid | 15.533333333 |
| 20261011T195821Z-54d68ddc | b-blaz1-strip-sheet | invalid | invalid | — |
| 20261011T195926Z-2385b1e6 | b-dagli-strip-sheet | valid | valid | 1.123333350 |
| 20261011T200032Z-4db9e465 | b-fu-nest-mb-free | valid | valid | 3.666666667 |
| 20261011T200141Z-8fe77360 | b-fu-nest-mb-given | valid | valid | 3.666666667 |
| 20261011T200246Z-b1ce9018 | b-fu-strip-sheet | valid | valid | 1.467836289 |
| 20261011T200352Z-a02eb918 | b-jakobs1-nest-mb-free | valid | valid | 4.583333333 |
| 20261011T200500Z-d821f87b | b-jakobs1-nest-mb-given | valid | valid | 4.583333333 |
| 20261011T200608Z-8b3eda3b | b-jakobs1-strip-sheet | valid | valid | 0.825000000 |
| 20261011T200714Z-68166b0f | b-jakobs2-nest-mb-free | valid | valid | 3.875000000 |
| 20261011T200821Z-1525e6d5 | b-jakobs2-nest-mb-given | valid | valid | 3.875000000 |
| 20261011T200925Z-0855f76a | b-jakobs2-strip-sheet | valid | valid | 0.883333343 |
| 20261011T201030Z-c9128f61 | b-mao-nest-mb-free | valid | valid | 1.896190239 |
| 20261011T201135Z-c37e274c | b-mao-nest-mb-given | valid | valid | 2.501777684 |
| 20261011T201241Z-5d79b847 | b-mao-strip-sheet | valid | valid | 0.893629596 |
| 20261011T201348Z-0f0a827e | b-marques-strip-sheet | valid | valid | 1.192307692 |
| 20261011T201501Z-85934d02 | b-shapes0-nest-mb-free | valid | valid | 7.809523810 |
| 20261011T201609Z-d2caf129 | b-shapes0-nest-mb-given | valid | valid | 7.809523810 |
| 20261011T201717Z-047edce1 | b-shapes0-strip-sheet | valid | valid | 2.825000000 |
| 20261011T201823Z-516669f3 | b-shapes1-nest-mb-free | valid | valid | 7.809523810 |

[Full precision, original records and independent correction evidence](svgnest-correction-20261011T202121Z-ad4dbe52.json).
