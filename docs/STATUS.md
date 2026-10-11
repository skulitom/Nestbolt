# Status — 2026-10-11

M0 is in progress. **Gated completion: 0%.** Only finished milestones count.

Groundwork committed as `66a3bab`. The durable goal covers the complete v1 plan.
The historical Sparrow build and two five-second adapter checks pass. All 1,300
archived results have been checked against the paper and a 39-run native quality
reproduction is frozen in [the M0 method](../benchmarks/sparrow-repro/README.md).
The full-budget experiment `published-20261011` is running in bounded batches.
At the latest checkpoint, **18/39 runs** have finished (all thirteen first seeds,
plus ALBANO, SHAPES2, DAGLI, FU and JAKOBS1 second seeds). All eighteen pass independent
geometry checks; [the immutable checkpoint](../benchmarks/results/m0-first-eighteen-20261011.json)
retains the run records and validation evidence.
JAKOBS2 is about 1.02% longer than its published mean; the required three-seed
comparison is pending for every instance. No results have been discarded and the
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
geometry independently and retains every outcome. Eight adapter/evidence tests
pass. Actual FU and unequal-edge-gap checks pass; an insufficient stock cap is
correctly invalid with no score. The detailed mini-box trial has no result within
30 s. [All preparation attempts](../benchmarks/results/svgnest-preparation-20261011.json)
are retained, including early configuration and CPU-limit failures. One five-second
FU batch also passes the immutable report audit; this is not the full baseline.
The full B batches, settings selection and remaining competitor runners are pending.
Deepnest opens in an isolated profile on the hidden desktop; its solve adapter is
still being prepared.

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
| M1 — Baseline | 15% | Validator, S/B/M freezes, LBF and SVGnest runners ready; remaining competitors and full matrix pending |
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
dependency-notice/schema consistency, twenty-seven Python harness/conversion/evidence tests,
88 source-contract checks and fixture checksums. Four additional curve-conversion
tests pass in the isolated maker environment. Two original five-second
Sparrow jobs completed; records are appended to [BENCHMARKS.md](../BENCHMARKS.md).
The schema was also checked against real CLI output locally. None of these checks
establishes the independent geometry validity or published quality gates.
