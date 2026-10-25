# H5: proved guarded cog displacement cells — 2026-10-25

**A smaller guarded separation representation is ready for a new full search.**
Independent exact proofs show that every retained allowed cell satisfies every
full original guarded cog/cog clause. No new solver runs in this checkpoint,
and no full target layout is found. H2/H5 remain open at **60%**.

## Exact source-clause complement

The previous fully guarded model used 59 forbidden pieces and 2,636 separating
directions per physical pair. Its simpler 71-piece raw-core relaxation omitted
moving-pair clearance and still returned UNKNOWN. The alternative prepared here
represents allowed displacement regions directly, while proving full guarded
separation for every retained integer displacement.

For an integer relative position, failure of a source outside inequality
`A*dx + B*dy >= bound` is exactly `A*dx + B*dy <= bound - 1`.
For each of the 61 complete guarded source clauses, exact rational clipping
constructs that clause's entire convex failure polygon inside each complete
same-sheet difference box. This accounts for **122 bounded failure regions**.
Outward dyadic vertex boxes enclose each rational polygon before geometric union
and complement operations. The first sheet has 59 nonempty failure regions;
the second sheet has five.

The initial decomposition retains **1,245 first-sheet cells and four second-sheet
cells**, with 11 explicitly retained inset/grid discards. It covers the complete
raw prepared free region but is too large for the intended reduction. All raw
faces and discarded records remain preserved.

## Conservative first-sheet simplification

Four declared sub-micrometre simplification candidates still leave at least
1,158 first-sheet cells. A separate bounded preparation measures five additional
representations. Each simplifies the whole failure union and pads it outward by
twice the tolerance; the complete original failure union must remain covered.
The second-sheet representation is copied unchanged.

| Simplification tolerance | Outward failure padding | First-sheet cells |
|---:|---:|---:|
| 0.001 mm | 0.002 mm | 464 |
| **0.005 mm** | **0.010 mm** | **229** |
| 0.010 mm | 0.020 mm | 183 |
| 0.025 mm | 0.050 mm | 143 |
| 0.050 mm | 0.100 mm | 112 |

The declared rule selects the smallest tolerance producing at most 352 total
cells, including the unchanged four second-sheet cells. Thus the selected
representation has **229+4=233 cells and 831 inward halfplanes**. No selected raw
face is discarded and both raw prepared free regions are fully covered. This
does not remove the explicit boundary loss from outward enclosure, first-sheet
simplification/padding, allowed-face insets and integer rounding.

The 0.010 mm first-sheet padding is a **conservative construction restriction**.
It can exclude feasible placements; a negative result cannot establish
unrestricted packing impossibility. It never weakens the original guard,
material target or 66-part requirement. Selection concerns representation size,
not benchmark success. All nine measured candidates remain available as evidence.

## Independent whole-cell safety proof

The independent audit reconstructs every source failure polygon with rational
arithmetic and checks its complete vertex set and outward enclosure. It verifies
the selected complete free regions, all 233 convex cells and all 831 sufficient
inward halfplanes, including exact signed-coordinate coefficient-error bounds.

For every retained cell and every nonempty failure polygon, a strict separating
axis proves the **whole cell** disjoint from that source-clause failure region.
Floating calculations only nominate an axis; exact rational projections of all
vertices must verify its strictly positive gap. The audit then reads back and
rechecks all **13,531 certificates**. Integer displacement points in any retained
cell therefore satisfy every complete original guarded source clause, provided
the model enforces the declared same-sheet difference bounds.

All **five previously verified second-sheet pair witnesses** remain in retained
cells and satisfy their exact integer halfplanes. The independent audit takes
**6.908532s**. Preparation times are **1.669301s** for the
initial complement, **2.902190s** for the first four candidates, and
**0.699605s** for the next five. Every declared 120-second bound is met.

Across 15 physical cog pairs, the new representation needs at most **3,495 cell
flags**, compared with **39,540 outside-direction variables** in the earlier full
guarded model, or 5,280 in the weaker raw-core model. These counts do not establish
a runtime improvement; the new solver model is not constructed or run yet.

Next bind the full master to sheet-conditional allowed displacement cells,
retaining all original domain, area, occupancy and pair constraints. Same-sheet
pairs must choose a sufficient cell; different-sheet pairs require none. Verify
every model field and Boolean implication before one distinct shared 60-second
pipeline with a 45-second master cap and two-second shutdown reserve. Any positive
still needs the remaining full original-pair coordinates, all 66-original/native
checks, production integration and unchanged 13-job/two-kerf H5 matrix.

## Repository and evidence

Main 61359456 and its offcut page remain preserved. Its own
[CI40242602102](https://github.com/skulitom/Nestbolt/actions/runs/40242602102) is **in_progress**, with **5/6** successful jobs
at the saved snapshot. This checkpoint is local; the normal push awaits terminal
CI to avoid cancelling the Windows check. Production source and all three
accurate READMEs are unchanged. Preview v0.2.0-alpha.1 and stable Latest v0.1.0
remain unchanged; no release is qualified. No solver, native packing, quality
run or reserved H2 vector evaluation occurs. All 22 reserved vectors stay untouched.

Evidence: [exact cell audit](h5-cog-displacement-cells-20261025/cell-audit.json),
[per-sheet certificate counts](h5-cog-displacement-cells-20261025/cell-query-checks.json),
[all coarse candidates](h5-cog-displacement-cells-20261025/coarse-candidates.json),
[retained witnesses](h5-cog-displacement-cells-20261025/retained-witnesses.json), [archive](h5-cog-displacement-cells-20261025/raw-001.zip)
and [manifest](h5-cog-displacement-cells-20261025/raw-manifest.json). The archive retains **49**
canonical files and **40** exact-content aliases, including
all source polygons, candidates, halfplanes and exact certificates, with verified
length, SHA-256 and ZIP CRC.
