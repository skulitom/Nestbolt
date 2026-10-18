# Varied pairs and productive exchanges — preparation, 2026-10-18

The [identity diagnosis](h5-balanced-stage-20261018.md) found accepted swaps
of the same part inventory with no material/extent reduction. Continuing
[gap filling](h5-post-exchange-fill-pilot-20261018.md) helped some authored
and bracket cases but all four mechanical comparisons still failed the
original material limit. Both results remain preserved.

This isolated candidate distributes at most twelve anchors and six nearby
same-original-item pairs across part types in stable order. It rejects a
validated swap of equal original-item multisets unless material strictly
decreases. Swaps changing sheet inventory retain the nonincrease rule.
Original-item pointer identity and multiplicities distinguish inventories;
geometry, source/receiver repairs, phase/total budgets and post-exchange
gap filling remain. An omitted-zero counter records neutral rejections.
This is a candidate policy, not evidence that neutral swaps can never help.

Two new authored regressions fail on the unchanged runtime: it only reaches
one of three available pair families and accepts a swap saving no material.
A third test protects same-inventory swaps that save material. Its first
fixture passed on a 0.0006 mm2 rounding difference; original source, logs,
and independent checks are retained. Adding a receiver ceiling makes the
authored swap save 100 mm2, independently validated. The strengthened test
requires more than 99.9 mm2; the unchanged runtime passes that positive
case and still fails the two target regressions before any runtime edit.

All 101 optimized core tests pass, including all 98 previous tests. Sixteen
public CLI validations cover before/after geometry and quantities for eight
actual authored outcomes across four seeds: no-op swaps reject with exact
internal-state rollback, useful same-inventory swaps remain accepted.
Strict lint/build, ten public fixed-work observer outcomes, four public CLI
comparisons and five adversarial paired-harness checks also pass. Normal
output and common fixed-work replays stay exact except for wall duration.
Original sources, binaries, archive CRC and every member hash verify.
The first witness checker incorrectly indexed an omitted zero-valued
exchange counter; its source, error review and partial validations remain.
Reading the absent counter as zero fixes the checker without changing any
candidate result, material assertion or positive-counter requirement.

The paired pilot retains four jobs, two kerfs, three seeds, three sequential
rotating arms per block, eight physical CCD0 cores and 60-second searches.
Block, scoring, case and measurement functions are AST-identical to the
previous pilot. The original +1% material limit and full 13-job gate remain.
No production integration or measured quality claim; H2/H5 stay open at 60%.
