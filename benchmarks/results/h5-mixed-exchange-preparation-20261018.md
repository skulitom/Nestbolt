# Bounded mixed-part exchanges — preparation, 2026-10-18

The [latest diagnosis](h5-productive-stage-20261018.md) found a singleton
largest source item excluded from same-item pairing, twenty single attempts
returning more item area than they remove, and eight inventory-preserving
paired attempts. The [mixed-dimension witness](h5-mixed-exchange-witness-20261018.md)
proves a scoped two-for-three assignment that needs distinct incoming parts.

This isolated candidate interleaves the existing six same-item pair choices
with at most six mixed-item pairs, using at most twelve stable area-ranked
anchors and two nearest different-item neighbours each. Pair deduplication
uses stable placement indices and original item pointer identity. Existing
pair-phase, repair and whole-job budgets, complete obstruction sets, returned
area bounds, per-member orientations, strict whole-job validation/material
checks, productive inventory guard and post-exchange fill remain.

The unchanged runtime fails the mixed-dimension exchange regression while
disabled/expired and per-member pose checks pass. The first implementation
passes 106 of 107 tests: seeds zero and one move the pair, but seed two finds
no paired proposal. Its area-ranked first member lies below the other part;
first-member corner anchors can miss the combined group corner. The complete
failure, initial source/test binary and ten independent validations remain.
Additional mixed-group minimum-corner anchors fix this without weakening the
four-seed test. Original samples remain; extra transforms are charged.

All 107 optimized core tests pass, retaining all 101 previous tests. Six new
tests cover actual mixed exchanges, disabled/expired rollback, each member's
rotation/reflection, bounded deterministic singleton choices, frozen sheets
and failed returns. Twelve public validations cover six actual before/after
outcomes. Strict lint/build, ten public observer outcomes, four CLI comparisons
and five adversarial pilot checks pass. Normal output and common fixed-work
replays are exact apart from wall time. Two omitted-zero counters record mixed
attempts/acceptances as subsets of paired attempts/acceptances.

The committed pilot preserves four jobs, both kerfs, three seeds, three
sequential rotating arms per block, eight physical CCD0 cores and 60-second
searches. Block, scoring, case and measurement functions are AST-identical
to the preceding pilot. Source/binary guards and every archive member verify.
No quality claim, integration or reserved-input access. The +1% material
limit and full 13-job H5 gate remain; H2/H5 stay open at 60%.
