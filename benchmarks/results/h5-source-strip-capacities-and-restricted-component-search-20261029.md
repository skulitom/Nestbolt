# H5 source-strip capacities and restricted component search — 2026-10-29

**24 independently verified strip certificates eliminate 50 count distributions
and four complete fixed cog-site choices.** There are now **82 distributions
across 25 site choices**. This strengthens the saved continuous source-hull
construction; it does not exclude any of the 440 overall allocation candidates.

A placement model using these reductions received one bounded call and returned
`UNKNOWN` without an assignment. The call is closed. No full66 source check or
native check ran. H5 remains open and milestone completion remains **60%**.

## Exact source-strip capacities

The previous [component model checkpoint](h5-vectorized-capacities-and-canonical-component-search-20261029.md)
retained 132 count distributions and 29 choices of two empty cog sites. The new
analysis projects every original unary hull onto X and Y, then merges overlapping
projection intervals separately for each source mode and family component. It
retains all gaps between intervals. Independent reconstruction verifies 13,880
source-hull projection intervals and their union of 1,014 intervals.

For a contained original-source rectangle, occupied area inside a fixed axis
strip is piecewise linear in translation. The sum over source pieces can attain
its minimum on a translation interval at an endpoint or where a rectangle edge
meets a strip boundary. Enumerating all those exact rational breakpoints gives a
lower bound for every source position in the unary hulls. Taking the minimum
over every legal source mode preserves that necessary condition.

For each mixed-family subset of possible occupied-material components, the
count-weighted mandatory area must fit inside the subset's conservative grid-cell
area in that strip. The complete preparation screens 16,375 grid-aligned strips
for each of 425 mixed subsets: **6,959,375 strip inequalities**. Floating estimates
only screen possible violations; 491 strips are recomputed exactly, using 10,995
source-breakpoint cases. The complete preparation takes **3.747314 s**, with no
partial scan or discovery-cap overrun.

The [independent proof reader](h5-source-strip-capacities-and-restricted-component-search-20261029/strip-audit.json) reconstructs interval
unions with an event sweep and verifies every recorded certificate using polygon
clipping instead of the builder's rectangle-length formula. The 24 positive
certificates require 615 exact breakpoint evaluations and 1,952 clipping
operations. All coefficients, available areas and excluded count distributions
match. The reader takes 2.536186 s. Unrecorded screening values are not all
independently recomputed; every claimed exclusion is.

The completely excluded empty-site pairs are **[0,9], [5,9], [9,11], [9,12]**.
Their complete count lists are exhausted by verified certificates. These bring
the total restricted-site exclusions to 80 of 105, leaving 25. The
[full strip table](h5-source-strip-capacities-and-restricted-component-search-20261029/all29-strip-bounds.json) preserves every witness and
every remaining count distribution, and the
[excluded-site list](h5-source-strip-capacities-and-restricted-component-search-20261029/excluded-empty-site-pairs.json) identifies the four
new exclusions. None is a claim about freely moving cog placements or the entire
allocation frontier.

## Filtered source model and one closed call

The [filter audit](h5-source-strip-capacities-and-restricted-component-search-20261029/filtered-count-audit.json) verifies that only proved
exclusions are removed. All source components and mode attributions for retained
choices are unchanged: 6,299 source-mode attributions and 4,164 unique
family/geometry/region attributions remain, with aliases agreeing on membership.
The filter takes 0.030156 s and its independent readback 1.807196 s.

The strengthened model keeps all 13 moving original parts, all 80 per-copy
source modes, 7,403 unary region selectors and 30,208 local-grid source planes.
All 20 source-piece rectangles remain rigid; all 183 different-owner rectangle
pairs retain the audited clearance construction. The model includes 25 site-pair
selectors, 82 count-distribution selectors, 100 component count equalities,
325 canonical owner-component equalities and 740 within-component ordering
constraints. Copy relabelling preserves every feasible placement in this model's
source domain. The [complete model audit](h5-source-strip-capacities-and-restricted-component-search-20261029/model-audit.json) verifies all
8,443 variables and 44,837 constraints, every source mapping, the binary/text
model equivalence and all preparation charges.

The sole call uses four workers, seed zero, no objective or hint and a four-second
source-validation reserve. The **40.333346 s preparation charge** includes the
saved short-sheet shared time, all reused source/geometry stages, generic count
construction, the complete new strip construction, filtering and the new model
build. No required preparation stage is silently omitted.

| Allocated solve | Returned solve | Algorithm total | Shared total | Result |
| ---: | ---: | ---: | ---: | --- |
| 14.920722 s | 14.997324 s | 56.091057 s | 56.165995 s | UNKNOWN |

The internal solve slice overruns by **0.07660160050727427 s**, which is preserved.
The complete algorithm and shared totals remain below 60 and 90 seconds. There
are zero assignments, incumbents, source-checker calls and native calls. The
[response audit](h5-source-strip-capacities-and-restricted-component-search-20261029/response-audit.json) verifies the raw response, all logs,
parameters, model hash and charges, including 84,586 branches and 11,411 conflicts.
Raw LP statistics are retained without interpreting them as geometry validation.
The call is not restarted, extended or reseeded; `UNKNOWN` proves no infeasibility.

## Next work and preserved state

The [next investigation](h5-source-strip-capacities-and-restricted-component-search-20261029/next-step.json) extends necessary-area analysis to
diagonal strips. Their source-area functions are piecewise quadratic, so an exact
minimum may occur at a stationary point between breakpoints. Every new witness
must receive independent clipping verification, and any unprocessed distribution
must remain. No diagonal-strip preparation or new solver call is opened here.
Full66 original-source success must precede native/material validation,
production integration and the complete H5 matrix.

Valid short11 and valid64, all 440 overall allocation candidates, production
source and all three READMEs are preserved. H2 retains its original gate and no
reserved vectors are evaluated. Upstream Sparrow/Studio heads and releases are
unchanged. Stable Latest remains v0.1.0 and preview v0.2.0-alpha.1; no new release
qualifies from this checkpoint.

At the [publication snapshot](h5-source-strip-capacities-and-restricted-component-search-20261029/publication-review.json), all six CI jobs on
main bd68c967 pass. The prior checkpoint is committed as 1a3cf85e, with its normal
push pending this completed CI prerequisite. A combined normal push still checks
fresh remote heads and live runs; no CI run is cancelled.

The [manifest](h5-source-strip-capacities-and-restricted-component-search-20261029/raw-manifest.json) preserves 4824 canonical files and
867 identical aliases in 58311600 bytes of multipart evidence. Separate
archive verification checks every stored byte, source binding and local report
link before the checkpoint is committed.
