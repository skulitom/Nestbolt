# Mixed rectangle and bracket pilot

All 72 layouts validated. Allowing rectangular groups in the existing opt-in search reduced plasma mixed-rectangle material by 4.071% versus the matched ordinary run and saved 39.569% of cutting distance. Seven of the eight job/kerf comparisons met the +1% material limit. The laser large-plate job exceeded it at +1.375%. H5 remains open. [All eight comparisons and raw runs](h5-common-rectangular-row-pilot-20261120T162524Z/README.md).

The independently reconstructed 72 layouts contain 263,979 same-sheet part pairs and 3,188 shared edges. The largest half-kerf offset error was 0.009961 mm. The reported source outlines and the SVG and DXF cutting exports agree. [Independent scores and geometry](h5-rectangular-rows-20261120/pilot.json).

The public CLI, stdio MCP, Chrome and Firefox all returned the same 90 mixed-rectangle placements. The CLI used wall timing. The other three surfaces completed their fixed-work budgets. CLI and MCP also produced four byte-identical SVG/DXF cutting files. [Surface comparison](h5-rectangular-rows-20261120/surfaces.json).

In the laser large-plate job, each of the nine runs placed 21 inserts inside holes. The bonus and ordinary medians were 1.11276 and 1.09767 sheets. Another investigation packs the frames and their inserts as rigid units. The original opt-in hole policy and all material and cutting gates continue to apply.
