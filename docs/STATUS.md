# Status — 2026-10-11

M0 is in progress. **Gated completion: 0%.** Only finished milestones count.

Groundwork committed as `66a3bab`. The durable goal covers the complete v1 plan.
The historical Sparrow build and two five-second adapter checks pass. All 1,300
archived results have been checked against the paper and a 39-run native quality
reproduction is frozen in [the M0 method](../benchmarks/sparrow-repro/README.md).
The full-budget experiment `published-20261011` is running in bounded batches.
At the latest checkpoint, **33/39 runs** have finished (all thirteen first and
second seeds, plus seven third seeds). All thirty-three pass independent
geometry checks; [the immutable checkpoint](../benchmarks/results/m0-first-thirty-three-20261011.json)
retains the run records and validation evidence.
The first JAKOBS2 run is about 1.02% longer than its published mean; its complete
three-run comparison now passes. ALBANO, SHAPES2, DAGLI, FU, JAKOBS1, JAKOBS2 and
MAO pass their complete comparisons; the remaining six await their third seeds.
No results have been discarded and the
original 1% pass threshold is unchanged. The next bounded batch is still running.

M1 preparation now includes an independent Clipper2 job/layout validator covering
stock, margins, defects/remnants, copies, rotations, mirroring, holes, clearance and
fill modes. It computes material scores and never scores invalid layouts. All
43 native tests pass, including a 10,000-case bounded polygon fuzz test, a
2,000-copy case and actual CLI exit behavior. The checker also compiles to WASM.
The academic and maker datasets are frozen; remaining competitor adapters and
the full baseline matrix are pending.
See [VALIDATION.md](VALIDATION.md).

The unmodified, pinned LBF sheet runner is automated. Its first provisional batch
has **70/70 independently valid layouts** across all 35 B jobs and two untuned
configurations (one seed, 60 s maximum, one constructive pass). The retained
[baseline table](../benchmarks/results/lbf-20261011T184759Z-924100e9.md) includes
full-precision scores and provenance. This is not a result for Nestbolt and does
not establish the complete competitor comparison or M1. The generated mixed-stock,
defect, margin and spacing smoke also passes; see [LBF method](../benchmarks/lbf/README.md).

The pinned [SVGnest runner](../benchmarks/svgnest/README.md) now automates local
Chromium, bounds solve time, enforces a single-core process tree, checks original
geometry independently and retains every outcome. Eleven adapter/evidence tests
pass. Actual FU and unequal-edge-gap checks pass; an insufficient stock cap is
correctly invalid with no score. The detailed mini-box trial has no result within
30 s. [All preparation attempts](../benchmarks/results/svgnest-preparation-20261011.json)
are retained, including early configuration and CPU-limit failures. One five-second
FU batch also passes the immutable report audit; this is not the full baseline.
The first 24-job B pilot (60 seconds, seed 0, identical settings) has **23 valid
layouts** after correcting an output-decoding precision loss. The remaining
invalid layout contains a genuine overlap and has no score. Original records
remain unchanged; [all 38 saved attempts were audited](../benchmarks/results/svgnest-correction-20261011T202121Z-ad4dbe52.md),
and the [24-job correction table](../benchmarks/results/svgnest-correction-20261011T202304Z-3f63b428.md)
and a fresh [decoder smoke](../benchmarks/results/svgnest-decoder-v2-smoke-20261011.json)
retain independent proof. The [remaining eleven B jobs](../benchmarks/results/svgnest-20261011T204513Z-1f07ec81.md)
have eight valid layouts and three with small boundary violations. The complete
first pilot is therefore **31/35 valid**, with every outcome retained. The full
seed/configuration matrix and settings selection are pending.
An additional native parser diagnostic found float32 rounding in SVG polygon
input. Straight paths preserve all tested coordinates exactly, now checked before
every solve. The [three affected SWIM reruns](../benchmarks/results/svgnest-20261011T211052Z-d34e7f41.md)
all pass at 60 seconds, as does an unequal-edge-gap smoke. A fresh full B pilot is
running; earlier failures remain visible. The first three expanded-setting B
trials also pass but do not establish a best configuration.

The pinned [Deepnest runner](../benchmarks/deepnest/README.md) now imports parts,
quantities and mixed rectangular stock, runs the native solver with one worker
and one CPU, and validates its original-coordinate output independently. Actual
FU, spacing-safe hole placement and capped mixed-stock smoke layouts pass.
Native half-gap behavior inside holes and incomplete stock-cap output are
correctly rejected under the original constraints. Moving the CPU restriction
after import and before solving produces four consecutive valid FU smokes with
prompt startup. [All startup trials](../benchmarks/results/deepnest-startup-20261011.json)
are retained, including failures. Eleven adapter/evidence tests pass. The complete
Deepnest baseline remains pending. The first nine B jobs at 60 seconds are all
independently valid; [first three](../benchmarks/results/deepnest-20261011T205510Z-c961f172.md)
and [next three](../benchmarks/results/deepnest-20261011T205945Z-dfbb847c.md) retain
strictly audited batch evidence, followed by [the third batch](../benchmarks/results/deepnest-20261011T211232Z-57323d69.md).
New straight-path input checks reject loss beyond double-precision rounding.
The remnant/defect input helper preserves margins and source stock identities;
four native conversion tests and actual remnant and enclosed-defect smokes pass.
The spacing-safe hole smoke also passes with the new input paths.
[All six preparation attempts](../benchmarks/results/deepnest-stock-inputs-20261011.json)
remain available, including the strict parser diagnostics and invalid hole-gap
result. Final layouts are always checked against the original job.

The [current Sparrow comparator](../benchmarks/sparrow-benchmark/README.md) now calls
the pinned, unmodified public solver API with one worker and an overall candidate
deadline that includes initial construction. Original polygons determine validation
and strip scores. Real strip and unequal-edge-gap sheet smokes pass; a strip that
does not fit one fixed sheet is invalid and unscored. [All three trials](../benchmarks/results/sparrow-preparation-20261011.json)
are retained. Seven Python adapter/evidence tests and one native deadline test
pass. Its [first 13 S jobs at 60 seconds](../benchmarks/results/sparrow-20261011T210336Z-74491a27.md)
are all independently valid. Remaining budget/seed/settings comparisons are pending.

The [matrix coverage freeze](../benchmarks/MATRIX.md) fixes all 88 jobs, the
12-job long-budget subset, development/final seeds and both settings roles before
Nestbolt search tuning. Exact tool settings and the full one-command executor
remain pending. Initial competitor pilots preceded this coverage freeze; no
held-out optimiser results informed it.

All 13 OR-Datasets strip sources now have frozen URLs/checksums and a retained
MIT collection licence; every part, demand and allowed angle matches the historical
M0 input. The canonical freeze now includes **13 S and 35 B jobs**: 22 reconstructions
of published Nest-MB cases and 13 explicitly derived fixed-sheet variants. All
48 pass source-contract checks and reproduce byte for byte; four additional
Python tests protect conversion and tamper detection. See
[the dataset method](../benchmarks/datasets/README.md) and
[source provenance](../benchmarks/sources/README.md).

The maker freeze adds **40 M jobs with 10 held-out reservations**, spanning all
five planned source categories, requested sheet sizes and 500–2,000-copy jobs.
All forty source contracts and full one-copy-per-sheet feasibility witnesses pass
independently. Original curves, generation parameters, licence evidence and
checksums are retained. A fresh isolated installation rebuilds all files exactly;
four curve-bound/topology tests and three freeze/coverage tests pass. Development
SVGnest trials now include the non-held-out mini-box. The ten held-out jobs have
never been run through an optimiser. See [maker method](../benchmarks/makers/README.md).

| Milestone | Weight | State |
| --- | --- | --- |
| M0 — Groundwork | 5% | Workspace/check infrastructure in place; published strip reproduction pending |
| M1 — Baseline | 15% | Validator, S/B/M freezes, LBF/SVGnest pilots and Deepnest smoke evidence; complete competitors and full matrix pending |
| M2 — Sheet optimiser | 25% | Not started |
| M3 — Part-in-part and import/export | 15% | Not started |
| M4 — Browser app and MCP server | 20% | Entry-point scaffolding only |
| M5 — Final gate | 20% | Not started |

## Next work, in order

1. Freeze the exact published Sparrow runs, historical source, toolchain, seed and
   expected lengths (done); run the frozen matrix, reproduce within 1% and attach
   evidence to BENCHMARKS.md.
2. Mixed-stock scoring is implemented and repeatable search semantics documented;
   freeze the exact M2 work-budget mapping before public solve-result schemas.
3. Complete the competitor adapters/runners against the common validator and
   frozen S/B/M datasets. Keep the ten held-out maker jobs out of tuning.
4. Build sheet optimisation against those measurements. Expose completed core
   capabilities through CLI, Workers and the five MCP tools as they become usable.

MCP is part of v1 in the refreshed plan. A protocol handshake test is not the G7
Claude Code import/nest/export/independent-validation acceptance test. Release
packaging, MCPB validation, registry metadata and explicit publication remain M4 work.

GitHub workflows are prepared locally; hosted CI is not yet run. There is no
configured remote, hosted repository, release, registry publication or Pages deployment.

## Local setup verification

On Windows with Rust 1.98.1, `python scripts/check.py` passed: formatting, Clippy
with warnings treated as errors, 43 Rust tests (including the bounded geometry fuzz
test and an actual MCP subprocess handshake), both WebAssembly builds,
four additional stock-conversion tests, dependency-notice/schema consistency,
fifty-five Python harness/conversion/evidence tests,
88 source-contract checks and fixture checksums. Four additional curve-conversion
tests pass in the isolated maker environment. Two original five-second
Sparrow jobs completed; records are appended to [BENCHMARKS.md](../BENCHMARKS.md).
The schema was also checked against real CLI output locally. None of these checks
establishes the independent geometry validity or published quality gates.
