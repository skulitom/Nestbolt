# Directed-exchange pilot preparation — 2026-10-16

The [72-attempt plan](h5-exchange-pilot-20261016/plan.json) is prepared; no timed
pilot search has started. It compares the unchanged preview and the isolated
exchange candidate on both failing mechanical jobs, with `m-box-mini` and
`c-bracket-mixed` as controls. Both kerfs and seeds 0–2 are included. H5 remains
open on its original +1% material condition.

Each job/kerf/seed block runs ordinary baseline, common-line baseline with the
bonus on, and common-line candidate with the bonus on. All three use the same
physical CCD0 core sequentially, with arm order rotated across seeds. Eight
blocks may run concurrently, each search receiving 60 seconds. The unchanged
preview CLI independently validates and exports every result. All failures and
raw inputs, layouts, reports, counters and exports are preserved.

The observer uses the public `Request::prepare` and `PreparedRequest::optimize`
APIs, with no per-step logging. It writes the full search result and counters
after search finishes. The two builds use identical observer source. Eight
authored fixed-work observer runs match the corresponding public CLI's structured
layouts, jobs and metrics exactly and pass the unchanged independent validator.
Two additional ordinary preview CLI runs provide the baseline common-mode
references. These short inputs record zero exchange attempts; they prove API
agreement, not usefulness of the new operation. The earlier six direct operation
tests and their original failures remain [separate evidence](h5-directed-exchange-functional-20261016.md).

The setup caught a build-cache failure before any measurement: the first
candidate observer reused the baseline executable from a shared Cargo target,
despite distinct source. Its build log and incorrect executable remain preserved.
A fresh candidate-only target produces a distinct executable. Both corrected
observers then pass the CLI agreement checks. This did not change the production
build or the ongoing H4 run.

- Baseline observer SHA-256:
  `00127ab7c98145b9294e471725b255f85d293a32dffc5f52759afbe775959513`.
- Corrected candidate observer SHA-256:
  `25efd689909fa5e2d66d86fe09e6a9af39118c4c67c9c9d1e330a6a3d28c7358`.
- Shared observer source SHA-256:
  `921134696223e55239a80b2bd8723f0fcf5ea6a6723f18f64fc2a2fb6900491b`.

Five runner tests verify balanced arm order, original material failures despite
relative improvement, missing/duplicate/failed seeds, invalid scores and expired
session handling. An expired session starts no process and still archives its
failed outcome. No valid-only median or incomplete comparison is scored. All
preparation, builds and functional checks used CCD1; there is no packing-quality
or speed result here.

The runner refuses to start before the current H4 quality matrix and both current
scale fixtures pass with unchanged source/build guards. Its plan must be committed
before opening. Even a favorable pilot cannot close H5: the complete 13-job gate,
all original thresholds and required surfaces remain authoritative. Any invalid
output prevents integration; the candidate remains isolated.

[Checks](h5-exchange-observer-20261016/checks.json) and
[archive inventory](h5-exchange-observer-20261016/integrity.json) bind the matched
source, corrected and rejected executables, logs, test outputs and observer/CLI
comparisons. The raw archive contains 376 verified members, 4,976,920 bytes,
SHA-256 `139684b5764a4bfeee3b0dd5c654d9dd83db159b8a90ecd73221b13a1da27af2`.
CRC and every member hash pass. No held-out geometry was read, no production
source changed, and completed milestone weight remains 45%.
