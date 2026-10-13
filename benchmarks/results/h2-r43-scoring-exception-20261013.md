# Approved R43 scoring exception — 2026-10-13

Artem approved “Record a documented scoring exception” in this chat. The exception
applies only to the frozen training Iris PE MX/Alps switch plate (`R43.json`),
identified by the source, label and manifest hashes in the [approval record](h2-r43-scoring-exception-20261013.json).

For part/hole-count scoring, the reviewed expectation is **one plate with 37 holes**.
The frozen reference's second part is a duplicate cutout with only 6.96e-13 mm
coordinate noise. The [original diagnosis](h2-r43-label-discrepancy-20261013.md),
frozen label, split, source and failed reports remain intact. No product geometry
was changed to implement this exception.

Applied to the retained 193805Z import observations, the raw 245/257 count matches
remain recorded, and reviewed count matches are 246/257. Eleven clear rejections
remain separate. This approval does not waive cut-layer, warning, fidelity or any
other requirement, does not apply to another file and does not change the held-out
success threshold. H2 is still incomplete.
