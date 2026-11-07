# SAT certificate pilot — 2026-11-07

The new certificate workflow is audited, but its only research call reaches
the frozen time limit without a usable result. **No arrangement is excluded.**
All 26 fixed29/current-cog choices and 440 whole-job allocations remain open;
H2/H5 remain open at **60% completed milestone weight**.

## Verified tools and encoding

The local diagnostic toolchain pins PySAT 1.9.dev21's Windows CPython 3.13 wheel,
the bundled CaDiCaL 1.9.5 source, and drat-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The selected solver, wrapper and
checker are MIT licensed. Package URLs/hashes and selected source/notices are
preserved. The multi-solver source distribution, wheel and unused solver
archives are not committed. Production dependencies are unchanged.

The first checker build fails because MinGW lacks `getc_unlocked`; the versioned
build uses standard `getc` through a compiler macro, preserving original source.
The first larger proof control then fails: Windows text-mode input treats binary
byte 0x1a as EOF. [The preserved correction](h5-sat-certificate-pilot-20261107/proof-io-correction.json)
uses a lossless binary-to-ASCII decoder and independently written inverse,
requiring an exact byte round-trip. A metadata helper's off-by-one assertion is
also retained and corrected separately.

[Versioned controls](h5-sat-certificate-pilot-20261107/tool-controls.json) pass three valid UNSAT proofs,
including a pigeonhole example, and reject absent, tampered and false proofs.
Two satisfiable controls have checked assignments. Threshold controls verify
16 local truth rows, 15,874 complete selector assignments and 483,846 prefix
counts. The four-clause gate is exactly `y <=> a or (x and b)`; its acyclic
prefix recurrence uniquely represents the number of selected cells.

## Complete pilot model

The smallest retained refined graph is arrangement `[0,5,12]`: 896 bracket
cells and 1,216 insert cells. The [model audit](h5-sat-certificate-pilot-20261107/model-audit.json) checks
all 2,229,216 graph pairs, 887,869 conflict clauses and 953,103 total clauses,
including 16,840 threshold gates over 18,952 variables. Both families require at
least 8 selected cells. A separate source-inner-rectangle proof establishes
capacity 1 for every one of the 2,112 cells. Every valid continuous completion
therefore induces a satisfying assignment; checked UNSAT could exclude only
this fixed core/current-cog arrangement at original 0.2 mm clearance.

The first audit incorrectly expects zero graph diagonals and stops before any
SAT call. [Audit-v2](h5-sat-certificate-pilot-20261107/model-audit-correction.json) requires the documented
self-conflict bits and separately proves single-cell capacity. Model bytes do
not change. Complete model preparation takes 3.085335 s; authoritative audit
takes 17.633587 s. Prior preparation and failed-control costs remain preserved;
there is no full-job 60/90-second construction claim.

## Closed bounded call

The plan freezes one 60-second search, a 1,000,000-conflict budget, a 90-second
complete-process cap, 2 GiB memory and 256 MiB binary-proof limits before execution.
The [process record](h5-sat-certificate-pilot-20261107/call-process.json) closes at the search-time limit
after 66.683245 s total, without a status or assignment. Its incomplete binary
proof is archived as evidence and is not submitted as a complete certificate.

The supervisor samples only its direct process and reports about 4 MiB RSS,
which does not establish aggregate interpreter/descendant memory usage. No
successful memory-cap claim is made. A psutil inventory helper does not finish
and is stopped; [independent Windows CIM inspection](h5-sat-certificate-pilot-20261107/worker-closure.json)
confirms no matching SAT worker remains. This call stays closed and unresolved.
Its formula, partial proof and all failed/versioned controls are preserved.

[The response audit](h5-sat-certificate-pilot-20261107/response-audit.json) records zero new exclusions,
zero source-valid placements and no native calls. There are still 429 of 455
fixed arrangements excluded at required clearance, 427 even at zero clearance.
[Next](h5-sat-certificate-pilot-20261107/next-step.json), validate process-tree resource enforcement before
considering a distinct remaining arrangement. The closed pilot is never rerun.

[The manifest](h5-sat-certificate-pilot-20261107/raw-manifest.json) contains 95 new
canonical members and 11,767,462 compressed bytes.
[Source bindings](h5-sat-certificate-pilot-20261107/source-bindings.json) and
[historical references](h5-sat-certificate-pilot-20261107/external-evidence.json) preserve the exact inputs.
Independent archive verification is required before commit.
