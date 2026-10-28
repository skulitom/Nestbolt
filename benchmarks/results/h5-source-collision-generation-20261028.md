# Source collision generation — 2026-10-28

Two different bounded policies produced **three complete 66-part candidates**.
All three fail original-source collision checks and remain rejected. Both
sequences are closed; neither produces a valid full layout, an infeasibility
proof or H5 completion credit. H2/H5 remain open at **60% milestone weight**.

The first policy removes exactly 2,942 rectangle interval constraints and two
cumulative constraints from the previous relaxation. All 342 variables, 1,073
remaining constraints, mandatory-part requirements and hints are preserved.
This allows a complete candidate before the large capacity system is imposed;
the original-source acceptance tests remain unchanged. An intentionally
overlapping 66-part diagnostic passes the relaxed model and is correctly
rejected for **68 collisions**, with no stock failures.

The first solve returns a relaxation assignment in **0.302964 s**, retaining
all 15 hinted cog poses. Source readback finds **43 collisions**: three bracket
pairs, 12 bracket/cog pairs, seven cog/insert pairs and 21 insert pairs. The
next model adds all legal mode combinations for those 43 owner pairs:
**386 groups, 8,452 variables and 31,193 constraints**. Search begins only at
**13.26 s** and the call returns UNKNOWN without a candidate at **15.034608 s**.
The preserved solve soft overrun is **0.034608 s**. The whole sequence takes
**16.418178 s algorithm / 17.172596 s shared** and stops immediately.

The second policy changes the granularity: it constrains only the owner/mode
combinations actually observed colliding. Its first model already contains
those 43 cases from the saved rejected candidate; the old initial solve is
not repeated. Independent reading verifies **1,424 variables and 5,066
constraints**, all 43 exclusions, retained mandatory constraints and a valid
partial56 control. A complete diagnostic using unobserved bracket/insert modes
passes the relaxation and is correctly rejected for **65 source collisions**.
This demonstrates why every changed mode still needs full source validation.

| Mode-policy model | Cases | Variables / constraints | Source result | Returned solve |
|---|---:|---:|---|---:|
| 0 | 43 | 1,424 / 5,066 | Rejected: 20 collisions | 1.654828 s |
| 1 | 63 | 2,274 / 8,126 | Rejected: 48 collisions | 4.847328 s |
| 2 | 111 | 5,871 / 20,824 | UNKNOWN; no candidate | 15.014759 s |

Every newly observed case adds all conservative relative cells for that mode
combination. Unseen mode combinations stay unconstrained until source readback
exposes them. The independent reader verifies all saved model fields, unchanged
prefixes, every assignment and every new case; each new case excludes its
previous violating candidate. A no-solve preflight exercises all 66 intrinsic
mode domains, including reversed displacements and appending both a new mode
to an existing owner pair and a new owner pair.

The second sequence freezes at most 32 distinct models because its cuts are
finer, but retains **one 60-second algorithm budget, a 90-second shared limit
and at most 15 seconds per solve**. It stops at the third call, after
**22.995023 s algorithm / 23.688067 s shared**. Final presolve lasts to the
logged **11.94 s** search transition; the **0.014759 s solve soft overrun** is
preserved. Neither unused time nor an UNKNOWN response starts another call.
Solver OPTIMAL statuses apply only to the corresponding collision relaxation;
they do not certify a physically valid layout or optimal nesting.

Independent saved-ring readback checks all five invalid layouts: the two
negative diagnostics and three runtime candidates. Each retains **66 originals,
1,380 same-sheet pair checks, 264 stock edges, 90 holes and 10,026 hole vertices**.
All stock checks pass; the collision counts are respectively 68, 65, 43, 20
and 48. Every collision is between moving originals. No source-valid full66,
native validation, production integration or new H5 matrix result exists.

The current evidence points to substantial Boolean/cell preprocessing cost.
The next investigation is a direct continuous-rational formulation using the
same conservative halfplanes and all 111 observed mode cases. The official
[Z3 arithmetic guide](https://microsoft.github.io/z3guide/docs/theories/Arithmetic/)
describes its linear-real arithmetic engine; the
[Python guide](https://microsoft.github.io/z3guide/programming/Z3%20Python/Introduction/)
documents exact rational values. Its upstream MIT notice is saved in the raw
evidence. This is research only: **no Z3 dependency has been installed for this experiment and no Z3 solve
has run**. A pinned dependency, serialized-formula audit, rational readback,
float-conversion/source checks and one fixed budget are prerequisites.

The previous two checkpoints were pushed normally and atomically to main
**a0d6f9af** after all six prior checks passed.
[CI 40753599821](https://github.com/skulitom/Nestbolt/actions/runs/40753599821)
currently has four passing jobs; Linux and Windows checks remain live. This
checkpoint waits for all six jobs and fresh remote guards before pushing.
Production, READMEs and upstream heads/releases are unchanged. The valid64,
444 necessary allocations, original H2 gate and 22 unopened vectors remain
preserved. No new release qualifies.

Evidence: [owner-policy model audit](h5-source-collision-generation-20261028/owner-model-audit.json),
[owner-policy response](h5-source-collision-generation-20261028/owner-response-audit.json),
[mode-policy model audit](h5-source-collision-generation-20261028/mode-model-audit.json),
[mode-policy response](h5-source-collision-generation-20261028/mode-response-audit.json),
[independent original-ring readback](h5-source-collision-generation-20261028/mode-originals-audit.json),
[continuous-arithmetic review](h5-source-collision-generation-20261028/continuous-arithmetic-review.json),
[next step](h5-source-collision-generation-20261028/next-step.json), [raw manifest](h5-source-collision-generation-20261028/raw-manifest.json).
The verified archive contains 392 canonical files and
533 identical-byte aliases in 3,089,713
compressed bytes, including every candidate, failure, model, assignment, source
readback, generated case, solver log/response and input dependency.
