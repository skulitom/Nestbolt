# H5: expanded full-source search — 2026-10-26

**The full 12-mover model passes independent reconstruction, but its one bounded
call is terminated by the outer budget without a saved solution or solver
status.** All 66 originals remain mandatory. H2/H5 stay open at **60%**.

## Fresh necessary capacity and model

The original cog/cog collision boundary has 228 segments. Exact binary-rational
segment-distance checks and a separate endpoint/cross-product/ray-parity audit
confirm a strictly interior **258.082 mm** collision disk. All 32 fresh
second-sheet cog domains lie within integer anchor bounds
`[1094689,146489,1353511,179438]` on the micrometre grid. Two adjacent,
disjoint x bins cover those bounds. Each bin's squared diagonal is below the
necessary integer squared separation **66,606,318,725**. Hence at most two of
the nine moving cogs can select sheet 2. This is a new certificate for the
54-fixed construction; no old fixed57 regional certificate is transferred.

The new model includes all **12 mandatory movers / 54 unchanged fixed parts**,
**24 anchor coordinates**, **52 query modes**, **12,688 domain-choice flags**,
and all **538 same-sheet modes over 66 physical pairs**. It contains
**214,901 variables**, **281,731 constraints**, **201,575 shared direction flags**
and **54 advisory hints** from the repaired nine-cog partial. No hint becomes
a coordinate lock. No copy-order symmetry or old fixed57 conditional exclusion
is added.

The full guarded source relations account for **13,794 convex-face uses**:
5,630 are whole-box tautologies, two force their mode inactive, five have a
single possible outside edge and 8,157 retain complete disjunctions. Direction
normalization is exact integer gcd/ceiling division. Flags are shared only for
the same ordered physical pair and identical normalized inequality, imply
their own plane and occur positively in source-face disjunctions.

Two necessary filled-area inequalities are recomputed from exact original
binary-rational polygons and stock rectangles. Lower charges for the 54 fixed
parts are **3,681,713,590 / 249,662,718** units of 0.001 mm². The integer stock
upper limits are **4,441,669,000 / 465,322,303**. The second upper limit is one
unit tighter than an earlier outward-ceiling bound: integer lower-area sums
cannot exceed the floor of the exact available area. This changes no stock or
material target. Part-in-hole/common-line remain off for this job.

An independent audit verifies **119 committed source inputs**, reconstructs
every variable and constraint, evaluates all face simplifications using a
separate signed-interval calculation, verifies the existential shared-flag
projection, all hints and original IDs, and checks actual solver import/export.
The model digest is `f002eb9b01e28b4f8f488f6222e7c19208fc623c60b8bcbe6bfa8d3dc5d8ca50`. Offline preparation and audit do not
qualify the production budget.

## Preserved hard timeout

Declare one call with eight workers, seed zero, a **45-second solver soft
limit**, a **60-second shared outer budget**, and ten seconds reserved for
shutdown. The actual imported model and parameter bytes match their audits.
Loading/verification takes **2.318658 seconds**. The solver log reaches search
at **16.54 solver seconds**, after preparation, then records no final response.

The parent terminates the process at the shared deadline and returns after
**60.029781 seconds**, including **0.029781 seconds** beyond the outer budget.
This budget miss is preserved. There is no saved solver response, terminal
solver status, candidate or native validation; the result is **process timeout**,
not `UNKNOWN` or `INFEASIBLE`. The log does not establish which worker or
shutdown operation caused the delay. The process is absent at the subsequent
independent audit. The call is closed and must not be retried, extended or reseeded.

The first readback auditor expected a normal solver completion and failed on
the missing result file. Its original script, plan and traceback remain.
A separate timeout-specific audit verifies the preserved result, absence of a
candidate/response/process, actual parameters/model and timing. It does not
convert the failed run into a successful result.

## Evidence for a distinct next formulation

A deterministic census finds that the **201,575** direction definitions use
only **16,082 distinct exact normals per ordered physical pair**, with up to
75 thresholds sharing one normal. Their definitions contain **777,018**
nonzero coordinate terms. Introducing an integer projection
`z = A*(xb-xa) + B*(yb-ya)` once per group, then expressing each flag as
`flag => z >= C`, would reduce those definitions plus projection equalities
to **281,457** terms: **495,561 fewer**. It would add 16,082 variables and
equalities, producing 230,983 variables and 297,813 constraints.

This is a census and proposed exact reformulation, with **no demonstrated
performance benefit or additional solver call**. All source-face clauses,
domains, area/capacity rules, mandatory parts and hints must remain unchanged.
Every replacement, finite projection bound, complete parent recovery and actual
solver import/export must be independently checked before a distinct call.
Any eventual candidate still needs all 66 original outlines/cutouts, original
pair/stock/material checks and native validation, then production integration
and the complete 13-job/two-kerf benchmark matrix.

## Main, release and remaining gates

All six jobs of [main d1645404 CI 40256286467](https://github.com/skulitom/Nestbolt/actions/runs/40256286467)
passed before the normal push of **d85f2b2a**. The remote commit and push receipt
are verified. At 02:31 UTC, [its CI 40258687459](https://github.com/skulitom/Nestbolt/actions/runs/40258687459)
is running with four jobs passed. Preserve that run before the next main push.
Upstream heads/releases, production and READMEs are unchanged. These diagnostic
changes do not qualify another release; preview v0.2.0-alpha.1 and stable
v0.1.0 remain appropriate. H2 keeps its original gate and all 22 reserved vectors
remain untouched.

Evidence: [model audit](h5-expanded-source-search-20261026/model-audit.json),
[fresh capacity audit](h5-expanded-source-search-20261026/fresh-capacity-audit.json),
[timeout audit](h5-expanded-source-search-20261026/timeout-audit.json),
[factorization census](h5-expanded-source-search-20261026/factorization-census.json),
[checks](h5-expanded-source-search-20261026/checks.json) and [raw manifest](h5-expanded-source-search-20261026/raw-manifest.json).
**186** canonical files and **46**
exact-content aliases are size/SHA-256/CRC verified in **1**
independently readable archive part(s).
