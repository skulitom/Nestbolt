# Legal-mode source repair — 2026-11-07

The new orientation-change construction closes after **one changed-mode
optimization and 159 mode evaluations**. Its candidate remains invalid:
independent original-source replay finds **39 failing pairs**, with all stock
checks passing. No remaining single-owner bracket/insert change improves the
model objective at that candidate. This is a local heuristic result, not a
packing impossibility proof. Four fixed arrangements and all 440 allocations
remain. H2/H5 stay open at **60% completed milestone weight**.

## Audited legal-mode geometry

[The complete model preflight](h5-mixed-mode-source-repair-20261107/mode-model-audit.json) checks **108 owner/mode
options**: eight brackets with eight quarter-turn/mirror modes each, eight
inserts with four modes each, and twelve cogs with one declared 7-degree phase.
The original job allows free cog rotation; the 108 options are the current
construction's finite modes, not every possible legal cog orientation.

All four certified region classes, **1,340 vertices, 2,350 planes and 760 exact
rational projection comparisons** pass independent readback. The full cog-pair
union retains both reflected halves. Every rigid rectangle pair retains all
four axis directions. Every mode-specific stock bound, affine pose, canonical
matrix and offset is coupled to its original owner.

Controls cover all 108 source pose reconstructions, **81 distinct mode vectors**,
168 analytic derivatives, cog-identity reversal and [six deliberately corrupted
dynamic models](h5-mixed-mode-source-repair-20261107/negative-controls.json). The initial energy and gradient
reproduce the previous invalid candidate. Pinned SciPy 1.17.1 controls and tool
hashes are retained. [Complete preparation](h5-mixed-mode-source-repair-20261107/preparation-process.json)
takes **0.321369 s**; the separate complete preflight audit takes **3.211676 s**.

## Closed bounded pipeline

The pipeline fully scores every unvisited single-owner legal orientation
change, clamps only that owner to its new source stock bounds, and independently
reads back every dynamic model. Only an objective improvement greater than
0.000001 mm² can open a call, using objective/identity/mode tie-breaking.
The initial closed vector and every previously optimized full vector are
excluded. A chosen model is serialized and read back before its sole call.

[Independent selection replay](h5-mixed-mode-source-repair-20261107/mode-selection-audit.json) verifies all
**80 first-round options** and the selected change: original bracket copy 4 moves
to mode 5. The surrogate energy falls from **22,384.710841 to 17,611.290512 mm²**
before optimization. One L-BFGS-B call then reaches **16,524.058157 mm²**, with
26 iterations, 29 evaluations and 27 retained improving points. All points,
gradients, bounds, selected modes and serialized model fields replay.

The second round checks **79 unvisited alternatives**, with no strict
improvement. It opens no optimizer call and stops the whole pipeline. The
maximum of eight calls is a ceiling, not permission to restart or continue
after this stop. This pipeline and its complete mode vector stay closed.

[All 66 original source parts are reconstructed and checked](h5-mixed-mode-source-repair-20261107/response-audit.json):
**1,632 same-sheet pairs, 264 stock edges, 90 holes and 10,026 hole vertices**.
[The 39 failing original pairs are preserved](h5-mixed-mode-source-repair-20261107/source-failures.json).
No native or material-validity call follows an invalid candidate. Numerical
convergence and reduced penalty give no H5 credit or allocation exclusion.

Charged preparation is **33.228634 s**, including the entire consumed
32.907266 s warm-start process and new all-mode preparation exactly once.
Algorithm/shared totals are **35.911924/35.983540 s**, within 60/90 s, with no
optimizer-slice or algorithm overrun. [All five processes close](h5-mixed-mode-source-repair-20261107/closed-process.json)
with **97,972,224 bytes** peak committed memory, below 2 GiB. Every evaluated
mode, selected model, incumbent and failed source result remains preserved.

## Coverage diagnostic and remaining geometric freedom

[A deterministic diagnostic](h5-mixed-mode-source-repair-20261107/coverage-diagnostic.json) reconciles all
**526 surrogate terms** with original-source pair checks. At this candidate,
every actually source-safe pair has zero penalty; there are no false-safe cog
terms. It identifies no missing safe region to add here. This is a statement
about this candidate only, not a global completeness proof of the safe union.
Its [complete bounded process](h5-mixed-mode-source-repair-20261107/coverage-process.json) takes **0.329765 s**;
the checkpoint audit independently reads back every diagnostic field.

[The next specification](h5-mixed-mode-source-repair-20261107/next-step.json) investigates original cog
phases **7 and 16 degrees**, a half-tooth phase apart, for the current first57
and valid short9 construction. This would add 12 options for 120 total.
It requires fresh original-source geometry, stock bounds, aliases and ordered
phase interactions before any new model or call. Earlier October 26 mixed-angle
short-sheet calls remain closed; their exclusions and search states do not
transfer. The new geometry and model are **not prepared or run**.

[A wording correction](h5-mixed-mode-source-repair-20261107/next-step-correction.json) preserves the first
next-step text and corrects its overstrong symmetry sentence: differing phases
do not by themselves rule out central symmetry. Ordered pair mappings and
rounding must be proved from source geometry; no computation used that sentence.

If the invalid warm start and diagnostic are consumed, the next construction
starts with **36.313304 s** already charged before fresh preparation. Validation
of all 66 parts, native/material checks, production integration, UI/CLI/MCP parity
and the unchanged H5 matrix remain necessary. H2 retains its original gate
and unopened reserved vectors. Production, README and releases are unchanged.

[The prior checkpoint reached main 4ca0d8cd normally](h5-mixed-mode-source-repair-20261107/prior-main-push-receipt.json)
after all six prior checks passed, preserving 52 remote files. [Current main CI
at review](h5-mixed-mode-source-repair-20261107/main-ci-at-review.json) is retained; no run is cancelled.

[Raw evidence](h5-mixed-mode-source-repair-20261107/raw-manifest.json) stores 102
canonical members and 742,441 ZIP bytes. [Historical
references](h5-mixed-mode-source-repair-20261107/external-evidence.json) and [source bindings](h5-mixed-mode-source-repair-20261107/source-bindings.json)
preserve the complete consumed source graph. Independent byte-level readback
passes for every new member, 5,923 historical references and 5,945 source bindings.
