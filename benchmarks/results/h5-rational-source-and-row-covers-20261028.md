# Real arithmetic and compact cog-row covers — 2026-10-28

The real-arithmetic trial is closed after one timeout. A separate exact
certificate proves that both closed relaxations have satisfying assignments,
but that assignment has **68 physical collisions**. No valid full layout or
H5 completion follows. H2/H5 remain open at **60% milestone weight**.

## Pinned local dependency and formula

[Z3 5.3.2](https://github.com/Z3Prover/z3/releases/tag/z3-5.3.2) was installed
in an isolated local environment from the verified Windows wheel for
`z3-solver==5.3.2.0`. The wheel is 16,870,592 bytes with SHA-256
`ea23baa055caf4a470ee6335140dfd617f4082750161a1fdbf23d24259f385e3`.
The full upstream MIT notice, official metadata, installation receipt and
hashes of 23 runtime files are preserved. The wheel lacked a separate notice;
the verified upstream notice was copied into its local distribution directory.
No production dependency or lockfile changed. The archive records how to
reproduce this dependency; it does not republish the virtual environment.

The QF_LRA formula uses **50 real coordinates, 78 Boolean variables and 352
assertions**. It keeps all 25 remaining originals mandatory around the same
fixed 41 and preserves all **111 observed owner/mode cases**. Independent
reading verifies every formula field, legal mode, free-cell disjunction,
relative-cell condition and ordering constraint. The partial 56-part control
fails exactly ten mandatory assertions; a separate control-only formula
negating those ten presences passes. It is not a complete-layout witness.

An exact rational error bound verifies all **4,129 halfplanes in 1,138 cells
across 77 domains** for continuous coordinates in their declared bounds.
The source audit does not depend on integer coordinates. Z3's parsed assertion
trees are checked before and after adding them: **660,958 AST nodes** match
the independent reader. Seventy initial-value preferences leave assertions
unchanged. Separate conversion fixtures retain their expected 20, 48 and 20
collision failures, including a submicrometre rational displacement with a
maximum anchor conversion error of about **1.33e-13 mm**.

## Closed response and exact SAT certificate

One frozen sequence allows at most 60 seconds of total algorithm work,
90 seconds shared, and 15 seconds per symbolic check, with one thread and seed
zero. Its first check returns **UNKNOWN / timeout** after **15.579044 s**.
The **0.579044 s soft overrun** is preserved. Total time is **17.218299 s
algorithm / 17.460927 s shared**. The stop-after-no-candidate rule closes the
sequence immediately; unused time is not reassigned. No model assignment,
source candidate or native validation is produced by this solve.

A subsequent construction uses no search: retain the 15 control cog poses,
put the three brackets in legal mode 3, and the seven inserts in legal mode 10.
Those repeated poses satisfy all **352 assertions exactly**. Only **21 cog/cog
cases are active**; the other **90 cases** concern different selected modes
and therefore impose no separation. Substitution and ground simplification
confirm all Z3 assertions without a symbolic check. An independent assignment
reader also verifies **all 5,871 variables and 20,824 constraints** of the
closed CP relaxation using this same construction.

Thus both relaxations are demonstrably satisfiable despite their UNKNOWN
responses. This is a certificate about the relaxed constraints, not physical
packing. Original-source readback correctly rejects it for **68 collisions**.
All four diagnostic layouts retain **66 originals, 1,380 pair checks, 264 stock
edges, 90 holes and 10,026 hole vertices**, with no stock failures. No original
geometry is removed to improve those results.

## Geometry study for the next construction

The next approach would move the whole first sheet: **18 frames, six brackets,
12 inserts and three rigid rows of five cogs**. These 39 blocks represent all
51 originals on that sheet; the verified short-sheet 15 remain fixed. The old
26-part rectangular core would no longer be fixed. Original identities and
holes remain intact, and common-line part-in-hole placement remains off.

Each row uses the original phase-7-degree cogs at a **258.9 mm pitch**, with an
independently checked internal minimum gap of **0.230499 mm**. The convex hull
of the row, expanded by a 112-micrometre square and covered with 5 mm slabs,
needs **58 disjoint rectangles**. Independent original-vertex reconstruction
checks the hull and clearance-disc coverage. This is a conservative cover of
the originals, not a replacement for final source checks.

The declared covers total **4,375,673.541486 mm²** in a usable
**4,441,669 mm²** rectangle, leaving **65,995.458514 mm²**. A stronger bound
enumerates **9,114 horizontal-section patterns** across all 16 orthogonal
modes and the row profile. One bounded linear program proposes nonnegative
weights; exact rational normalization and an independent sweep/enumerator
verify a required span of at least **2,978.159551 mm**. Compared with the
2,987 mm rectangle, only **8.840449 mm** remains. Neither bound excludes this
cover model, and neither proves that it fits.

This section bound applies when the expanded covers themselves stay inside
that rectangle. A future model must state its stock treatment explicitly:
requiring all covers inside is a conservative restriction, while source stock
checks remain authoritative. The study has built no new packing model or
called a packing solver. Next steps are a complete serialized-model audit,
honest partial controls, one newly frozen budget and full original-source
validation before any native/material claim.

The previous collision-generation checkpoint was pushed normally and
atomically to main **571738d8** after all six prior checks passed.
[CI 40758320213](https://github.com/skulitom/Nestbolt/actions/runs/40758320213)
has five passing jobs and the Windows check still live in this snapshot.
This checkpoint waits for all six before a fresh guarded push. Production,
READMEs and upstream heads/releases are unchanged. The valid 64-part layout,
444 necessary allocations, original H2 gate and 22 unopened vectors remain
preserved. No new release qualifies.

Evidence: [formula audit](h5-rational-source-and-row-covers-20261028/model-audit.json),
[real-domain proof checks](h5-rational-source-and-row-covers-20261028/real-domain-audit.json),
[closed response](h5-rational-source-and-row-covers-20261028/response-audit.json),
[SAT certificate](h5-rational-source-and-row-covers-20261028/satisfiable-relaxation-certificate.json),
[CP certificate audit](h5-rational-source-and-row-covers-20261028/cp-certificate-audit.json),
[independent original readback](h5-rational-source-and-row-covers-20261028/originals-audit.json),
[row-cover audit](h5-rational-source-and-row-covers-20261028/row-cover-audit.json),
[exact section bound](h5-rational-source-and-row-covers-20261028/section-bound-audit.json),
[bound scope and proof](h5-rational-source-and-row-covers-20261028/section-bound-proof.json),
[next step](h5-rational-source-and-row-covers-20261028/next-step.json), [raw manifest](h5-rational-source-and-row-covers-20261028/raw-manifest.json).
The verified archive holds 386 canonical files and
554 identical-byte aliases in
1,874,197 compressed bytes, including all failed results,
formula and engine audits, dependency notices, source rings, certificates,
study data, helpers and recursively bound source inputs.
