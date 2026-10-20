# H5: full-insert blockers and new frame contacts — 2026-10-20

**At least two saved core poses must be removed to fit all 21 inserts within
the retained insert pool.** Original-geometry checks verify a concrete
21-insert arrangement after removing two frames. This is a diagnostic partial,
not a complete or better packing result. Restoring the required frames remains
unresolved after two bounded searches, including one with 240 new frame
positions. H2/H5 remain open at 60%.

## Diagnose the complete insert requirement

Following the [two-move limits](h5-seeded-search-and-move-bounds-20261020.md),
the diagnostic selects exactly 21 mutually compatible insert positions from
the 686 retained choices. Each of the saved 45 frames/brackets/cogs may stay
or be temporarily omitted. It introduces no replacement core poses.
The objective first maximizes retained core count, then retained rounded
filled-outer area. A coefficient exceeding the sum of every area tie makes
that order exact. Every field of the 731-variable, 3100-constraint model is
independently reconstructed.

One declared 20-second, eight-worker, seed-zero call finishes `OPTIMAL` in
**0.101566800 seconds**. Its five callbacks and distinct final selection are
all retained. The final arrangement has 16 frames, 12 brackets, 15 cogs and
21 inserts. Its missing frames are two adjacent 350 × 450 mm rectangles at
the lower left of sheet zero, with original candidate indices 178 and 192.

Independent geometry reproduces every insert/core blocker set over **21,759**
same-sheet pairs. All six returned partials pass original outline, rotation,
stock, clearance and material checks; six fresh frozen CLI checks reject only
their actual missing core quantities. The final result has exactly the two
reported frame blockers and no unnecessarily omitted core poses.

Although this has 64 parts, it contains **4,166,740.7841 mm²** of filled outer
area, less than the known 58-part partial's **4,323,340.7841 mm²**. Part count
alone does not establish progress in material packing. The original job still
requires both missing frames.

## Independent deletion certificates

A separate enumeration covers all **1036** ways to omit zero, one or two of
the 45 seed core poses while keeping the others fixed. It derives **910**
distinct available-insert sets and partitions each into original conflict
cliques or singletons. Explicit-set reconstruction verifies every deletion,
every available-insert set and all **15,626** cover entries.

With zero or one deletion, every insert upper bound is at most **20**.
Together with the geometry-verified 21-insert witness after two deletions,
this independently proves that the diagnostic minimum deletion count is two.
It is a statement about this seed and finite insert pool, not unrestricted
continuous placement.

The covers leave **89** two-deletion cases unresolved for 21 inserts: 65 frame
pairs, 15 frame/cog pairs and nine frame/bracket pairs. Their lower area cost
is weaker than the solver's reported optimum. The secondary rounded-area
optimum therefore remains solver-reported; the independent cover proof
establishes only the primary two-deletion count.

## Attempt to restore both frames

The next model fixes the final 21 inserts and allows every compatible
previously retained frame, bracket and cog pose to move. It requires all
12 brackets and 15 cogs, maximizing frames from the known feasible 16 up to
the original required 18. All 3988 variables, 12,533 constraints and the
complete feasible hint are reconstructed. One declared 20-second call returns
`FEASIBLE` after **20.086176900 seconds**, with 16 frames and upper bound 18.
The callback and distinct final layout are checked; one exact seed CLI result
is reused and the other receives a fresh quantity-only rejection.

## Add new frame positions aligned to the inserts

For both distinct rectangular frame orientations, the changed construction
crosses all feasible horizontal and vertical contacts with the fixed insert
rectangles and stock boundaries. Transforms retain their original floating
point values; only exact transform duplicates are discarded. The insert gap
is clearance + 0.001 mm and stock contact inset is 0.0001 mm. Neither choice
claims native-margin qualification.

Of **799** declared contact events, 557 conflict with fixed inserts, two are
exact existing transforms and **240** add new frame positions. All 9059 old
candidates and indices remain unchanged. Every original compatible core pose
is restored, including poses removed by the earlier dominance reduction:
new frame positions can invalidate old dominance relationships.

This produces 5076 original compatible core poses plus 240 new frames.
The graph is explicitly conditional on the fixed 21 inserts. It cannot be
reused for movable inserts without computing those missing edges.

Independent checks reconstruct every event, check **132,955** original
core/insert filter pairs, examine all **1,117,560** new same-sheet pairs and
reproduce **179,683** new conflicts. All 2061 new cliques are pairwise valid
and cover every new edge. Compression finishes without reaching its limit
and leaves no residual pair constraints.

The expanded model has 5316 variables (1719 frames, 1303 brackets, 2294 cogs),
15,131 constraints and a complete feasible 16-frame hint. All fields are
reconstructed before its single declared 30-second call. It returns `FEASIBLE`
after **30.097629300 seconds**, again with 16 frames and upper bound 18.
Both returned layouts pass original geometry and fail only the two missing
frames; one exact seed CLI result is reused and one validation is new.
This timeout does not prove an 18-frame completion impossible. No expired
search is restarted, and every result and soft cleanup overrun remains.

## Next work and repository state

Do not repeat the fixed-insert completion calls or extend their limits. First test the necessary frame-only capacity of this fixed21-insert arrangement in the expanded pool, with all bracket/cog restrictions temporarily removed. Preserve its feasible16-frame seed and original18-frame cap. If even that relaxation cannot reach18, construct a different full insert arrangement instead of adding unchanged searches. If18 frames fit, diagnose the surviving bracket/cog capacity of the returned arrangement before a changed completion attempt. Temporary diagnostic omissions never satisfy original quantities. A full66-copy candidate still requires original geometry, frozen CLI, native margins and unchanged H5 material/cutting gates. H2 remains open under Artem’s original-denominator decision.

All six hosted checks for **56f818a** now pass. The saved **f321537** checkpoint
was then pushed normally to main and its remote hash is confirmed. The f321537 checks are running in the saved snapshot; this later evidence remains local while they finish.
Production source and the three READMEs retain their reviewed hashes.
No held-out evaluation, native packing, quality run or new release occurs.
The existing preview description remains accurate.

[Checks](h5-insert-blockers-and-frame-contacts-20261020/checks.json), [diagnostic outputs](h5-insert-blockers-and-frame-contacts-20261020/blocker-layout-audit.json),
[deletion certificate audit](h5-insert-blockers-and-frame-contacts-20261020/blocker-certificates.json),
[original completion](h5-insert-blockers-and-frame-contacts-20261020/fixed-results.json), [new contact audit](h5-insert-blockers-and-frame-contacts-20261020/contact-audit.json),
[expanded completion](h5-insert-blockers-and-frame-contacts-20261020/expanded-results.json),
[source review](h5-insert-blockers-and-frame-contacts-20261020/source-review.json), [passing main checks](h5-insert-blockers-and-frame-contacts-20261020/main-ci-56f818a.json),
[push confirmation](h5-insert-blockers-and-frame-contacts-20261020/push-confirmation.json), [current CI snapshot](h5-insert-blockers-and-frame-contacts-20261020/main-ci-f321537.json),
[all models, logs, layouts and certificates](h5-insert-blockers-and-frame-contacts-20261020/raw.zip), and [manifest](h5-insert-blockers-and-frame-contacts-20261020/raw-manifest.json).
All 138 archive members, CRCs and byte hashes verify.
