# H5: local area capacities and fixed cog relaxations — 2026-10-20

**All six continuous relaxations retain an exact upper bound of 21 inserts.
The proposed capacities do not tighten the bound or produce a physical layout.**
The original eight-insert gap remains unresolved, and H2/H5 remain open at 60%.

The [audited contact model](h5-coordinated-contact-selection-20261020.md) supplies
the unchanged 6,786 binary variables, four alternative complete cog arrangements,
original candidate poses, conflicts, family quantities and stock target.
No integer packing search is repeated. No new placement is generated.

## Necessary geometric constraints

For each original usable sheet, take its full rectangle and horizontal/vertical
partitions into two, four and eight equal bands: **58 regions** in total.
Every selected part contributes the area of its original filled outer outline
inside the region. Frames continue to reserve their holes. Each cog choice
contributes the sum over its fifteen original cog placements.

Coefficients round area downward to whole mm² after subtracting 0.000001 mm²;
capacities round upward after adding that amount. An independent rational
half-plane clip and shoelace calculation checks **all 75,957 positive
coefficients** against exact binary64-vertex geometry. Zero coefficients are
trivially conservative. Every capacity is checked above the exact rational
rectangle area. The maximum discrepancy from the floating geometry calculation
is **1.74623×10⁻¹⁰ mm²**. The complete 58-part hint remains feasible, with at least
**1,730 mm²** of integer slack in every new capacity. Preparation takes
**11.231468900 seconds**.

The saved CP model is independently parsed in full into 24,748 linear
inequalities and three equalities. Splitting its two-sided insert limit explains
the extra linear row. Objective, domains and complete hint match exactly;
only integrality is relaxed. The strengthened version appends the 58 audited
necessary capacities.

## Bounded relaxation results

| Relaxation | Seconds | Fractional variables | Exact insert upper bound |
| --- | ---: | ---: | ---: |
| Original relaxation | 0.890160200 | 302 | 21 |
| With area capacities | 3.538749300 | 421 | 21 |
| Fixed cog arrangement 0 | 2.858993900 | 361 | 21 |
| Fixed cog arrangement 1 | 9.111654600 | 386 | 21 |
| Fixed cog arrangement 2 | 1.549831600 | 342 | 21 |
| Fixed cog arrangement 3 | 3.632592100 | 379 | 21 |

Each relaxation declares a 120-second limit, eight offline solver threads and
seed zero before execution. All finish optimally within that limit.
SciPy's warning that the thread and seed options are forwarded to HiGHS is
preserved in each result. These are construction diagnostics, not native quality
measurements.

The area-augmented relaxation initially mixes three mutually exclusive cog
arrangements. Four further declared cases fix one arrangement at a time; each
retains 342–386 fractional variables and 21 inserts. Each saved primal vector
passes all original linear constraints and applicable area/fixing rows within
the recorded numerical residuals. None is interpreted or exported as a layout.

All six upper bounds are independently reconstructed using exact rational
arithmetic. For a minimization objective with inequalities, equalities and unit
variable bounds, the audit evaluates the dual row totals plus the minimum
reduced cost over each unit interval. It does not trust the rounded solver
objective. **The only nonzero inequality multiplier in every bound is the
explicit 21-insert cap.** The new capacities do not close the gap between the
fractional and whole-placement problems. These results neither prove a full
physical arrangement exists nor prove the original geometry impossible.

The first preparation script has an unmatched bracket and fails before any
preparation or solve starts. Its original source and failure are retained.
The corrected preparation uses the same declared geometric method; no successful
measurement is repeated to replace a failed search.

The explicit 21-insert quantity cap remains the sole active dual inequality in every saved optimal bound. All four fixed-cog cases retain 21 inserts fractionally, so neither local area cuts nor disaggregating the cog choice provides a smaller finite-pool bound. Do not repeat these relaxations or the prior timed-out integer models unchanged. Next investigate a bounded LP-guided binary construction using the saved fractional solutions: choose actual whole placement variables, propagate their original conflict cliques and exact family quotas, and retain both accepted and failed branch decisions. Declare the finite node/time limits before any new branch solves. A fractional solution, branch failure or a restricted finite-pool result cannot count as a physical layout or unrestricted impossibility. Any full 66-copy selection must pass the frozen original CLI, independent filled-outer checks and native-margin qualification before a runtime proposal; full unchanged H5 material/cutting gates remain required. H2 stays open under Artem’s explicit original-denominator decision.

## Repository and hosted browser reconciliation

Remote main advanced to **36edfbd** while local work was paused. Its 29 changed
landing-page, example, metadata and README files are disjoint from the 21 local
evidence files. The first ordinary push was rejected non-fast-forward; no remote
content changed. Merge **8a81205** preserves every changed file exactly from its
own parent, keeps both histories and verifies the benchmark log's original prefix.
The [merge audit](h5-area-capacity-relaxations-20261020/reconciliation.json) confirms the core-source digest
is unchanged. That merged checkpoint is now pushed to main.

All six checks on [c824e5a](h5-area-capacity-relaxations-20261020/main-ci-c824e5a.json), all six checks on
[36edfbd](h5-area-capacity-relaxations-20261020/main-ci-36edfbd.json), and its
[Pages deployment](h5-area-capacity-relaxations-20261020/pages-36edfbd.json) pass. The merged checkpoint's
separate CI state is retained in source review without assuming completion.
The current English, Japanese and Chinese READMEs correctly describe a hosted
preview from main. Earlier records describing hosted v0.1.0 refer to their
historical deployment. No release tag, asset or frozen benchmark claim changes.
Artem's decision to retain H2's original gate remains in force.

[Checks](h5-area-capacity-relaxations-20261020/checks.json), [source review](h5-area-capacity-relaxations-20261020/source-review.json),
[all raw coefficients, fractional solutions, certificates, scripts and failures](h5-area-capacity-relaxations-20261020/raw.zip),
and [verified archive manifest](h5-area-capacity-relaxations-20261020/raw-manifest.json).
All 67 archive members, CRCs and byte hashes verify. No held-out
evaluation, native packing, quality run, production change or milestone credit.
