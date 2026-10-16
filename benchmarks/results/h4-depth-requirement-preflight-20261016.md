# H4 requirement preflight — 2026-10-16

**Current scope and the no-WASM-threads constraint are verified; H4 remains open.**
This reads existing source/builds/plans only. It performs no new search, changes
no threshold and opens no reserved geometry. [Exact checks](h4-depth-requirement-preflight-20261016/checks.json)
bind the review to candidate `aba989e` and the engine currently under measurement.

| Requirement | Evidence needed | Current finding |
| --- | --- | --- |
| Declared development subset | Exact IDs, source bytes and public example inputs | Verified: gear-1–4, sign-1–4, cog-washers, gears and letters; eleven unique cases |
| Original G5 method | Sixty seconds, seeds 0–2, one fresh worker per job, physical CCD0 cores | Committed plan and runner match; live outcomes remain pending |
| Subset material | Both browsers median at most +1%, every job at most +5% | Current full matrix must prove both; isolated subset is supporting evidence only |
| Full G5 development quality | All 65 development jobs, original browser bounds | Current full matrix must prove aggregate and each-seed median/total limits |
| Native regression | All 195 layouts valid, median within +0.5% of frozen v1 | Current full matrix must prove this against its verified archived baseline |
| No previously fitting input becomes invalid | Original jobs/requests and quantities, independent validation | All matrix outcomes must satisfy the unchanged original constraints |
| No WASM threads | Actual shipped memory declarations and application worker model | Verified: one defined, unshared WASM memory; no imported/shared memory. Separate Web Workers run independent engines |
| 2,000-part curved drawing | Actual import, nest and SVG/DXF export in both browsers | Committed curve fixture and built-site/engine hashes match; current workflow pending |
| Memory and responsiveness | Browser-process-tree RSS/private samples below 1.5 GB; heartbeat/Long Tasks at most 200 ms | Existing instrumented runner covers import, nesting and export; current measurements pending |
| Original G5 scale regression | Original simple workload, quick start off, automatic workers | Separate current Chrome/Firefox workflows are fixed in the sequence; pending |
| Preserve exact output geometry | Original curves/gear rings, independent saved-project validation and per-sheet cutting files | Current scale exports must be checked; earlier outputs cannot replace them |
| Integrated product behavior | Native/CLI/MCP/browser, schemas, package verification | Local integration passes; current hosted checks and downloaded-package verification remain pending |
| Preserve failures and v1 meaning | Frozen inputs/results, prior failed measurements and option/default disclosures | Original failed comparisons remain sealed; the README identifies the frozen v1 build; no new competitor claim |

The memory check parses the measured WASM binary's import and memory sections,
including limits flags; it does not infer thread behavior from a filename or
source comment. The automatic browser worker count is separate from WASM shared
memory. The current fixed scale runners measure process-tree memory every 200 ms,
a 20 ms main-thread heartbeat and Long Tasks where supported. These are the
precommitted observations, not a universal memory/latency guarantee.

The final review must inspect the complete original matrix, saved raw layouts,
all scale outcomes/exports and their unchanged guards. A failed comparison or
missing scale outcome keeps H4 open. Until that review passes, completion stays
45%; H2 and H5 remain independently open.
