# Sparrow single-sheet applicability

Sparrow cannot allocate multiple fixed sheets. Exact rational shoelace area of the stored coordinates proves that 30 B jobs and two supported-feature M jobs need more part area than one entire sheet. Ignoring margins and gaps makes this a conservative bound. These cases can be labelled structurally inapplicable without running a solver; earlier attempted layouts remain in the benchmark record. Passing the area bound does not prove a layout exists.

| Set | Requires solver | Area bound | Unsupported feature |
| --- | ---: | ---: | ---: |
| S | 13 | 0 | 0 |
| B | 5 | 30 | 0 |
| M | 4 | 2 | 24 |

[Per-job reasons, exact areas and hashes](sparrow-applicability-20261011T2322.json). No result is fabricated and these skipped cases receive no numerical score.
