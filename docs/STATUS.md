# Status — 2026-10-11

M0 is in progress. **Gated completion: 0%.** Only finished milestones count.

Groundwork committed as `66a3bab`. The durable goal covers the complete v1 plan.
The historical Sparrow build and two five-second adapter checks pass. All 1,300
archived results have been checked against the paper and a 39-run native quality
reproduction is frozen in [the M0 method](../benchmarks/sparrow-repro/README.md).
The full-budget experiment `published-20261011` is running in bounded batches.
At the first checkpoint, **3/39 runs** have finished (ALBANO, SHAPES2 and DAGLI,
first seed). All three pass independent geometry checks. Their lengths differ
from their published 100-run means by +0.187%, +0.544% and -0.085%, respectively.
This is an early snapshot, not the required three-seed/all-instance pass.

M1 preparation now includes an independent Clipper2 geometry kernel and a CLI
strip-layout checker. Seventeen targeted/property tests pass; two actual adapter
smoke layouts pass independent checks against their original inputs. A deliberately
incomplete layout correctly returns a failure. Full stock/fill rules, datasets,
competitor adapters and adversarial fuzzing remain outstanding. See [VALIDATION.md](VALIDATION.md).

All 13 OR-Datasets strip sources now have frozen URLs/checksums and a retained
MIT collection licence; every part, demand and allowed angle matches the historical
M0 input. Canonical benchmark conversion remains pending. See [source provenance](../benchmarks/sources/README.md).

| Milestone | Weight | State |
| --- | --- | --- |
| M0 — Groundwork | 5% | Workspace/check infrastructure in place; published strip reproduction pending |
| M1 — Baseline | 15% | Preparation underway: independent geometry kernel and strip adapter; datasets/full harness pending |
| M2 — Sheet optimiser | 25% | Not started |
| M3 — Part-in-part and import/export | 15% | Not started |
| M4 — Browser app and MCP server | 20% | Entry-point scaffolding only |
| M5 — Final gate | 20% | Not started |

## Next work, in order

1. Freeze the exact published Sparrow runs, historical source, toolchain, seed and
   expected lengths (done); run the frozen matrix, reproduce within 1% and attach
   evidence to BENCHMARKS.md.
2. Resolve mixed-stock scoring and deterministic search budget semantics before
   defining canonical job/result schemas or freezing acceptance benchmarks.
3. Implement the independent validator and adapters, then the licensed S/B/M
   datasets and competitor runners. Freeze the ten held-out maker jobs early.
4. Build sheet optimisation against those measurements. Expose completed core
   capabilities through CLI, Workers and the five MCP tools as they become usable.

MCP is part of v1 in the refreshed plan. A protocol handshake test is not the G7
Claude Code import/nest/export/independent-validation acceptance test. Release
packaging, MCPB validation, registry metadata and explicit publication remain M4 work.

GitHub workflows are prepared locally; hosted CI is not yet run. There is no
configured remote, hosted repository, release, registry publication or Pages deployment.

## Local setup verification

On Windows with Rust 1.98.1, `python scripts/check.py` passed: formatting, Clippy
with warnings treated as errors, ten Rust tests (including generated geometry
properties and an actual MCP subprocess handshake), WebAssembly compilation,
dependency-notice consistency and fixture checksums. Two original five-second
Sparrow jobs completed; records are appended to [BENCHMARKS.md](../BENCHMARKS.md).
The schema was also checked against real CLI output locally. None of these checks
establishes the independent geometry validity or published quality gates.
