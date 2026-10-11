# Status — 2026-10-11

M0 is in progress. **Gated completion: 0%.** Only finished milestones count.

Groundwork committed as `66a3bab`. The durable goal covers the complete v1 plan.
The historical Sparrow build and two five-second adapter checks pass. All 1,300
archived results have been checked against the paper and a 39-run native quality
reproduction is frozen in [the M0 method](../benchmarks/sparrow-repro/README.md).
The full-budget experiment `published-20261011` is running in bounded batches.
At the latest checkpoint, **9/39 runs** have finished (ALBANO, SHAPES2, DAGLI, FU,
JAKOBS1, JAKOBS2, MAO, MARQUES and SHAPES0, first seed). All nine pass independent
geometry checks; [the immutable checkpoint](../benchmarks/results/m0-first-nine-20261011.json)
retains the run records and validation evidence.
JAKOBS2 is about 1.02% longer than its published mean; the required three-seed
comparison is pending for every instance. No results have been discarded and the
original 1% pass threshold is unchanged. The next bounded batch is still running.

M1 preparation now includes an independent Clipper2 job/layout validator covering
stock, margins, defects/remnants, copies, rotations, mirroring, holes, clearance and
fill modes. It computes material scores and never scores invalid layouts. All
43 native tests pass, including a 10,000-case bounded polygon fuzz test, a
2,000-copy case and actual CLI exit behavior. The checker also compiles to WASM.
The academic datasets are frozen; maker jobs, remaining competitor adapters and
the full baseline matrix are pending.
See [VALIDATION.md](VALIDATION.md).

The unmodified, pinned LBF sheet runner is automated. Its first provisional batch
has **70/70 independently valid layouts** across all 35 B jobs and two untuned
configurations (one seed, 60 s maximum, one constructive pass). The retained
[baseline table](../benchmarks/results/lbf-20261011T184759Z-924100e9.md) includes
full-precision scores and provenance. This is not a result for Nestbolt and does
not establish the complete competitor comparison or M1. The generated mixed-stock,
defect, margin and spacing smoke also passes; see [LBF method](../benchmarks/lbf/README.md).

All 13 OR-Datasets strip sources now have frozen URLs/checksums and a retained
MIT collection licence; every part, demand and allowed angle matches the historical
M0 input. The canonical freeze now includes **13 S and 35 B jobs**: 22 reconstructions
of published Nest-MB cases and 13 explicitly derived fixed-sheet variants. All
48 pass source-contract checks and reproduce byte for byte; four additional
Python tests protect conversion and tamper detection. See
[the dataset method](../benchmarks/datasets/README.md) and
[source provenance](../benchmarks/sources/README.md).

| Milestone | Weight | State |
| --- | --- | --- |
| M0 — Groundwork | 5% | Workspace/check infrastructure in place; published strip reproduction pending |
| M1 — Baseline | 15% | Validator, S/B freeze and LBF runner ready; M jobs and other competitor runners pending |
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
3. Complete the licensed S/B/M datasets and competitor adapters/runners against
   the common validator. Freeze the ten held-out maker jobs before any tuning.
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
dependency-notice/schema consistency, sixteen Python harness/conversion/evidence tests,
48 academic source-contract checks and fixture checksums. Two original five-second
Sparrow jobs completed; records are appended to [BENCHMARKS.md](../BENCHMARKS.md).
The schema was also checked against real CLI output locally. None of these checks
establishes the independent geometry validity or published quality gates.
