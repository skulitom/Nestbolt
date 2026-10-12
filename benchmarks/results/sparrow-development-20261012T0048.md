# Sparrow development coverage

All 528 frozen development Sparrow slots, both budgets and settings, three seeds. Unsupported capability/area proofs are recorded without spending solver time. Not a final seed comparison or completion of M1.

528/528 slots accounted for: 43 invalid, 358 unsupported, 127 valid.

| Dataset | Seconds | Settings | Outcomes | Table |
| --- | ---: | --- | --- | --- |
| S | 60 | identical | 39 valid | [three seeds](comparison-batches-20261012T000734Z-b8960d59.md) |
| S | 60 | upstream-default | 39 valid | [three seeds](comparison-batches-20261012T000738Z-c8a95335.md) |
| B | 60 | identical | 30 invalid, 60 unsupported, 15 valid | [three seeds](comparison-batches-20261012T003110Z-83b933da.md) |
| B | 60 | upstream-default | 90 unsupported, 15 valid | [three seeds](comparison-batches-20261012T000852Z-599890ec.md) |
| M | 60 | identical | 8 invalid, 76 unsupported, 6 valid | [three seeds](comparison-batches-20261012T003104Z-58217447.md) |
| M | 60 | upstream-default | 5 invalid, 78 unsupported, 7 valid | [three seeds](comparison-batches-20261012T003101Z-1ef96148.md) |
| B | 300 | identical | 15 unsupported, 3 valid | [three seeds](comparison-batches-20261012T004455Z-7ae22fb7.md) |
| M | 300 | identical | 12 unsupported | [three seeds](comparison-batches-20261012T004455Z-aef16b3a.md) |
| B | 300 | upstream-default | 15 unsupported, 3 valid | [three seeds](comparison-batches-20261012T004455Z-ec1e0666.md) |
| M | 300 | upstream-default | 12 unsupported | [three seeds](comparison-batches-20261012T004456Z-d7048476.md) |

Earlier actual runs that were invalid before the area-bound guard are retained as invalid. Later structurally unsupported cases carry their capability or exact area proof. None receives a fabricated score. The two settings each have one applicable long-budget job, b-jakobs2-strip-sheet; all six layouts pass the independent checker.

[Machine-readable table links and hashes](sparrow-development-20261012T0048.json).
