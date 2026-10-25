# H5: global packing propagation and compound cog proxy — 2026-10-25

**Both new all-parts-movable searches remain `UNKNOWN`, with no incumbent.**
The first adds independently checked global constraints to the prior polygon
relaxation. The second uses a much smaller, weaker inner-rectangle model to
seek an arrangement for diagnosis. Neither result proves the original target
impossible or supplies an accepted layout. H2/H5 remain open at **60%**.

## Original area and floor-safe components

Independent exact-rational triangulation rechecks the four original filled
outer areas, retaining the holes-reserved rule. The 66 parts total
**4,481,740.784069745 mm²**. Flooring individual areas to 0.001 mm² yields
4,481,740,770 integer area units; the original usable sheet capacities round
outward to **4,441,669,000** and **465,322,304** units. Assignment of original
part areas must fit each sheet, including full cog areas even where a smaller
geometric proxy represents the cogs. These are necessary area conditions,
not material acceptance from a proxy.

Each original non-cog rectangle component is inset by 0.01 mm on every edge
after its anchor is floored to a 0.01 mm grid. Checking the four corners of the
entire floor-error square proves every inset rectangle remains inside every
corresponding original component. The audit covers all 24 orientation/component
cases with 96 error-corner checks. The bracket's own components are disjoint
and remain coupled to one position and orientation.

Each cog initially adds one centered square with half-width **77.14 mm**.
All 16 square-vertex/error-square combinations lie strictly inside the already
certified all-angle disk of radius 109.1157 mm. This gives 78 inner rectangles
for 66 parts. The two per-sheet NoOverlap2D constraints and four orthogonal
cumulative profiles therefore hold for every valid original arrangement.
Profile capacities are rounded outward from the original usable dimensions.
All original sheet/orientation modes and the material-height target remain.

Construction takes 0.010154 seconds and independent geometry auditing takes
0.115529 seconds. Eight source files match committed evidence. The inherited
continuous polygon geometry remains byte-identical to the earlier audit.

## Strengthened polygon model

The first model retains all earlier polygon/rectangle separating relations and
adds the original-area bounds and global inner-rectangle constraints. Every
field of **31,935 variables and 37,849 constraints** is independently rebuilt,
including 312 optional intervals, both NoOverlap2D constraints, all four
cumulative profiles, two area bounds and unchanged exact counts. Construction
takes 1.039861 seconds and encoding audit 0.321061 seconds, within the declared
120-second caps. Every template change and dependency hash is recorded.

One declared 60-second, eight-worker, seed-zero call starts search at
1.75 seconds and returns **`UNKNOWN` in 60.188312 seconds**. It has
163,993 branches, 2,786 conflicts and no incumbent. The solver's small soft-limit
overrun is retained. This call is not resumed, extended or repeated.

The preserved original 64-part layout satisfies all new conditions: 74 inner
rectangles, 1,908 same-sheet rectangle-pair checks, including ten same-part
bracket pairs, both original-area bounds and four complete sweep profiles.
It still lacks two brackets and is never treated as a 66-part solution or hint.

## Smaller compound cog model

Earlier rectangle models used finite recipes containing fixed cog groups.
This new model gives every original part its own movable anchor. Each cog is
represented by five coupled, mutually disjoint rectangles: a central square
and four side pieces. The audit checks all **80** vertex/error-square combinations
against the certified disk and all ten within-cog component pairs for
nonoverlap. Their total area is **31,699.5264 mm² per cog**. The original cog's
larger filled area is still charged to its assigned sheet.

This different necessary relaxation omits the pairwise polygon/rectangle
separation disjunctions and uses global constraints on all **138** inner
rectangles. It may admit overlap of the larger cog disks, full outlines or
non-inset part boundaries; a positive outcome would only be a starting point
for diagnosis. It preserves all 66 mandatory parts, permitted non-cog
orientations, both original stock domains and the target material height.
There is no fixed frame/cog arrangement, hint or partial-inventory objective.

Every field of the resulting **1,806 variables and 2,824 constraints** is
independently checked, including 552 optional intervals and all original-area
and global propagation constraints. The metadata's zero explicit physical-pair
count denotes removed pairwise disjunctions; global NoOverlap2D still covers
every pair of inner rectangles on each sheet, including components of one cog.
Construction takes 0.039590 seconds and encoding audit 0.024321 seconds.

One separate declared 60-second call starts search at 0.13 seconds and returns
**`UNKNOWN` in 60.176534 seconds**, with 122,429 branches, 97,083
conflicts and no incumbent. A smaller encoding has not supplied an arrangement
within this bounded call. It is not an infeasibility proof, and no original
outline/native validation is manufactured from an absent solution.

The same preserved 64-part sanity check now has 134 inner rectangles and all
6,186 same-sheet pairs pass, together with both area bounds and four complete
profiles. Its 160 within-part pairs comprise ten bracket and 150 cog pairs.
The copied audit initially labelled that total as bracket pairs; an independent
recount corrects the metadata while preserving the original checks, correction
hashes and unchanged geometric evidence. No search or audit was rerun.

## Next step and repository state

Both global searches remain UNKNOWN; do not retry them unchanged, raise limits or interpret the smaller proxy as original geometry. Before another call, audit exact orientation aliases: frame and insert quarter-turn/reflection modes may share identical normalized components and stock domains, but every original orientation must retain an explicit equivalent representative and reconstruction map. Do not merge bracket modes merely because bounding boxes agree. Independently map the original66-part production layout into the all-movable model as possible source-derived hints: certify its quantities, provenance, transforms, proxy relations and stock violations against the target; retain every omitted or out-of-domain hint with its reason. Hints must never fix placements or reduce quantities. Review whether this verified data and exact alias reduction offer a materially different, bounded construction test; declare the scope and sole call before execution, retaining every prior UNKNOWN. Any positive proxy arrangement requires the larger disk/polygon conditions and original cog-outline/angle diagnosis, followed by original clearance/native guards, material target, production budget and the complete13-job/two-kerf H5 matrix. H2 stays open as instructed; do not open22 reserved vectors or repeat its denominator question. Push the committed evidence normally once the existing main CI run is terminal; no diagnostic result qualifies a new release.

Engine source, all three accurate READMEs and releases remain unchanged.
Main 8f941426's existing hosted run is captured as `in_progress` /
`pending`; four newer evidence commits remain local at
source head bf8daa5b while it finishes, avoiding cancellation by a new push.
No native packing, production-budget run, full H5 matrix or held-out evaluation
occurs here. Evidence-only changes do not require repeating production tests.

Evidence: [propagation plan](h5-global-propagation-and-compound-proxy-20261025/propagation-plan.json),
[geometry proof](h5-global-propagation-and-compound-proxy-20261025/propagation-geometry-audit.json),
[complete model audit](h5-global-propagation-and-compound-proxy-20261025/propagation-model-audit.json),
[bounded result](h5-global-propagation-and-compound-proxy-20261025/propagation-solver.json),
[compound plan](h5-global-propagation-and-compound-proxy-20261025/compound-plan.json),
[compound geometry](h5-global-propagation-and-compound-proxy-20261025/compound-geometry-audit.json),
[compound model](h5-global-propagation-and-compound-proxy-20261025/compound-model-audit.json),
[compound result](h5-global-propagation-and-compound-proxy-20261025/compound-solver.json),
[source review](h5-global-propagation-and-compound-proxy-20261025/source-review.json), [raw archive](h5-global-propagation-and-compound-proxy-20261025/raw-001.zip)
and [manifest](h5-global-propagation-and-compound-proxy-20261025/raw-manifest.json). All 68 canonical
members and 29 aliases retain exact bytes with
CRC and SHA-256 checks, including complete models, logs, templates and audits.
