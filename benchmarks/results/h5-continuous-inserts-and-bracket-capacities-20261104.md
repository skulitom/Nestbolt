# Continuous inserts and exact bracket capacities — 2026-11-04

Independent original-source proofs reduce the restricted first-sheet construction
from **14 site choices / 24 count distributions to 9 choices / 13 distributions**.
The 440 whole-job allocations and H5 gate remain open. No full 66-part placement
or native validation was produced.

## A valid continuous two-insert block

The [domain audit](h5-continuous-inserts-and-bracket-capacities-20261104/two-insert-domain-audit.json) reconstructs all 14 source
options shared by five distributions over four choices. Of 105 option pairs,
98 fail exact necessary directional bounds and seven remain. An initial 0.1 mm
grid construction failed before any solver call: conservative rounding at a
sharp region tip removes a valid continuous interval. Its failure is preserved.

Direct rational hull slicing places the two inserts at lower-left coordinates
(6.53,2308.128) and (6.53,2490.319) mm. [Original contour checks](h5-continuous-inserts-and-bracket-capacities-20261104/continuous-source55.json)
validate four partial layouts of **55 parts total across both sheets**, each
with 1,001 same-sheet pair checks, 220 stock-edge checks and 65 cutouts. These
contain 44 first-sheet parts and the already validated short-sheet 11; they are
not complete first-sheet layouts. Eleven original parts remain to place.
The [companion input audit](h5-continuous-inserts-and-bracket-capacities-20261104/companion-input-audit.json) verifies all 894
mode/region assignments and the source-support separation from the fixed inserts.

## Two distinct, closed companion constructions

Both models have 2,813 variables and 12,294 constraints. Every field, original
mode, 18 rigid rectangles and 146 different-owner rectangle pairs passes
independent readback. Each received exactly one bounded call, without a restart.

| Construction | Grid / outward rectangle gap | Charged preparation | Algorithm / shared time | Result |
|---|---|---:|---:|---|
| [Coarse model](h5-continuous-inserts-and-bracket-capacities-20261104/coarse-model-audit.json) | 0.1 mm / 0.3 mm | 42.698448 s | 47.138130 / 47.211093 s | [INFEASIBLE](h5-continuous-inserts-and-bracket-capacities-20261104/coarse-response-audit.json) |
| [Fine model](h5-continuous-inserts-and-bracket-capacities-20261104/fine-model-audit.json) | 0.01 mm / 0.23 mm | 42.986673 s | 47.265134 / 47.330650 s | [INFEASIBLE](h5-continuous-inserts-and-bracket-capacities-20261104/fine-response-audit.json) |

The [fine geometry audit](h5-continuous-inserts-and-bracket-capacities-20261104/fine-geometry-audit.json) verifies 4,559 exact
halfplane implications for unchanged source hulls. Maximum normal approximation
error falls to 0.007398 mm. Physical source spacing is unchanged; the finer
construction still exceeds its requirement. Both calls have no assignment or
overrun. These grid results have no independent unsat certificate and **do not
prove continuous infeasibility**. A response audit initially invoked in the
default runtime failed to import OR-Tools before creating output; its successful
execution uses the pinned CP-SAT runtime. No solver call was repeated.

## Continuous bracket capacity proofs

The [triple audit](h5-continuous-inserts-and-bracket-capacities-20261104/triple-capacity-audit.json) reconstructs 153 source
options across six small bracket domains, checks 1,963 incompatible pairs, and
verifies 578 complete disjunction trees with independent rational Floyd closure.
Three domains cannot contain three brackets. Applying those proofs removes
eight distributions and site choices [5,12], [5,13], [10,14] and [11,14], leaving
[10 choices / 16 distributions](h5-continuous-inserts-and-bracket-capacities-20261104/triple-filter-audit.json).

The [higher-count audit](h5-continuous-inserts-and-bracket-capacities-20261104/higher-capacity-audit.json) directly enumerates
992,858 multisets and checks every required triple subset against audited
survivors. It proves capacities three and four for two other bracket domains.
No new difference-constraint exclusions are needed at these higher counts.
The [final filtering audit](h5-continuous-inserts-and-bracket-capacities-20261104/final-filter-audit.json) removes three more
distributions, including site choice [9,13], and verifies all 2,613 retained
source-mode attributions. [The authoritative table](h5-continuous-inserts-and-bracket-capacities-20261104/all9-filtered-bounds.json)
contains **9 site choices and 13 count distributions**. Every other field of
each retained source row is unchanged. These proofs concern the specified
fixed-cog construction, not whole-job infeasibility.

The archive contains 157 new canonical members and
3,954,695 compressed bytes. [Its manifest](h5-continuous-inserts-and-bracket-capacities-20261104/raw-manifest.json),
[external evidence map](h5-continuous-inserts-and-bracket-capacities-20261104/external-evidence.json), and [source bindings](h5-continuous-inserts-and-bracket-capacities-20261104/source-bindings.json)
preserve every new attempt and bind reused historical bytes to the previously
committed full archive. An independent archive reader verifies both bundles.

[Next work](h5-continuous-inserts-and-bracket-capacities-20261104/next-step.json) applies exact capacities to the larger
remaining bracket regions. H2/H5 remain open at **60%**. No product change or
release claim follows, and the original gates and reserved H2 vectors remain intact.
