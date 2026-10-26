# H5: full-stock source-cell feasibility — 2026-10-26

**The new model removes every local movement limit, but its bounded search
returns UNKNOWN without a layout or an impossibility proof.** All 57 first-sheet
originals may use the entire legal stock; the verified nine-part short sheet is
retained. H2/H5 remain open at 60% by completed gate weights.

## Beyond the proved local obstruction

The preceding source certificate rules out the mixed candidate's five-part
configuration within 180 mm vertically. This experiment therefore discards
every local anchor bound. It keeps the original source modes and the checked
short-sheet allocation, but fixes no first-sheet position. An independent model
reader checks that all 114 coordinate bounds equal the full legal stock domains.
This is a different global-domain feasibility model, not a continuation of the
closed local solver or any source-sliding run.

All **1,596 first-sheet pair domains** are reconstructed. Their conservative
configuration-space complements yield **38,287 convex cells** and **136,401
exact integer halfplanes**. The same additional 0.002 mm obstacle expansion
precedes nearest-micrometre rounding; 456 rounded cells are discarded by the
conservative checks and no pair has an empty disjunction. Preparation takes
45.060182 seconds. The minimum retained cell distance to its already conservative
obstacle is 0.001355144 mm.

Independent geometry checking covers all cells, all pairs, 912 stock-edge corner
checks and **174,688 original-source clearance samples**. This takes 15.189268
seconds. The retained cells remain a sufficient subset: full-stock coordinate
bounds do not turn the rounded conservative representation into an exact
enumeration of every source layout. No exclusion is inferred from UNKNOWN.

## Source-based strip constraints

The model also uses **65 rectangles contained in the 57 source filled outlines**:
one inset outer rectangle for each frame and insert, two disjoint stem/foot
rectangles per bracket, and a 153 mm square about each cog's source-center
anchor. Each rectangle is inset in micrometres and independently checked against
the original transformed outer ring. Components of the same original remain
disjoint. Holes remain reserved under part-in-hole off.

These source-contained rectangles provide necessary NoOverlap2D constraints
and cumulative width/height limits across the usable stock. They strengthen
propagation without replacing any detailed source-pair constraint. Eight groups
of identical-source, identical-mode copies with equal stock domains add 47
nondecreasing-Y ordering constraints. No prior positions are supplied as hints.

The serialized model has **38,401 variables and 138,177 constraints**: 114
coordinates, 38,287 cell selectors, 1,596 exactly-one choices, 136,401 cell
halfplanes, 130 interval constraints, one NoOverlap2D, two cumulative constraints
and 47 source-copy ordering constraints. An independent reader reconstructs
every variable domain and serialized constraint, confirms whole-stock coverage,
all 57 mandatory first originals, and the absence of objectives and hints.

## One closed call

The sole 60-second search within 90 shared seconds returns **UNKNOWN** after
search begins. It records **179,798 branches and 5,060 conflicts** in the returned
response. Solver time is **60.078208 seconds**, returned solve time **60.089808
seconds**, and shared process time **61.906913 seconds**. The 0.078208/0.089808
second soft overruns are preserved. There is no assignment, native call or full
quality run. The search is CLOSED without retry, extension or reseeding.

Four independent audits pass. The next distinct hypothesis is constraint
generation: begin with the smaller necessary source-rectangle model, inspect
every pair in each returned candidate, and add complete source-cell disjunctions
only for newly violated pairs. Every original must stay mandatory, every later
solver model must contain new constraints, and total work must have a declared
bound. UNKNOWN or an unchanged model must stop that pipeline. No such run has
opened in this checkpoint, and no necessary-model candidate may be called a
valid source layout without full independent readback.

## Repository and evidence

All six checks on prior main f2322ccd passed, allowing the normal one-commit push
of db4d2309 at 2026-10-26T19:27:44.861319+00:00. The push and remote main were verified. At
2026-10-26T19:39:45.572163+00:00, [db4d2309 checks](https://github.com/skulitom/Nestbolt/actions/runs/40386947038):
4 of six checks pass; the remaining jobs are still live. Preserve CI40386947038 and wait for all six before the next push.

Production, READMEs, upstream heads/releases and all 22 reserved H2 vectors
remain unchanged. No release is qualified. [Checks](h5-full-stock-source-cell-feasibility-20261026/checks.json),
[source geometry](h5-full-stock-source-cell-feasibility-20261026/source-cells-checks.json),
[source rectangles](h5-full-stock-source-cell-feasibility-20261026/source-rectangles-checks.json),
[model audit](h5-full-stock-source-cell-feasibility-20261026/model-checks.json), [response](h5-full-stock-source-cell-feasibility-20261026/response-checks.json),
[scope](h5-full-stock-source-cell-feasibility-20261026/scope.json), [next step](h5-full-stock-source-cell-feasibility-20261026/next-step.json) and
[raw manifest](h5-full-stock-source-cell-feasibility-20261026/raw-manifest.json). The archive verifies
242 canonical files and 35
aliases by bytes, SHA-256 and CRC.
