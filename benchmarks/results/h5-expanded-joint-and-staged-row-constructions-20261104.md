# Expanded joint and staged cog-row constructions — 2026-11-04

Both new constructions close without a complete placement. The expanded joint
model returns **UNKNOWN**; the deterministic staged companion model returns
**grid-INFEASIBLE**. These results exclude no continuous layout or allocation.
All 440 whole-job allocations remain, and H2/H5 stay open at **60%**.

## Expanded source geometry and joint model

The [individual row-domain preflight](h5-independent-cog-rows-and-expanded-domains-20261104.md)
allows each rigid row of 5, 4 and 4 cogs to move throughout its own stock/core-safe
rectangle. Fresh interaction regions use these distinct domains; the previous
common-packet bounds and previous closed solver call are not reused as a model.

[Original-source certification](h5-expanded-joint-and-staged-row-constructions-20261104/expanded-source-region-audit.json) checks
all 12 source modes, 13 cogs and 36 row-specific mode domains. It verifies 2,198
mover/row regions and 468 row/row regions through 52,424 and 99,608 exact support
proofs. Ten degenerate regions are disabled. Minimum certified separation is
0.225999998848 mm. Fresh geometry preparation costs 3.266852 s; source certification
is an independent verification step, not hidden algorithm preparation.

[Integer readback](h5-expanded-joint-and-staged-row-constructions-20261104/expanded-integer-audit.json) verifies all 9,824 plane
implications. Normal-rounding error is bounded over 2000 × 1500 mm for mover-minus-row
coordinates and 600 × 1100 mm for row differences; the smaller prior envelopes
would not suffice. All three row ranges, 36 relative mode bounds, source identities
and 20 rigid component rectangles are checked. Maximum normal error is 0.009965010 mm.

[A fresh deterministic control](h5-expanded-joint-and-staged-row-constructions-20261104/expanded-positive-control-audit.json)
enumerates 1,324 centroid grid neighbours, orders the retained adjacent-row
differences by squared distance from zero, and finds its first combination feasible.
The selected shifts, in 0.01 mm units, are [-9156,1], [-8832,1269] and [-9303,2475].
All three integer row-pair conditions and all 53 placed originals pass independent
readback: 916 pairs, 212 stock edges, 63 holes and 6,732 hole vertices. This control
does not place the 13 orthogonal companions or claim a minimum-spread optimum.

[The full joint-model audit](h5-expanded-joint-and-staged-row-constructions-20261104/expanded-model-audit.json) verifies every
field of 16,314 variables and 58,749 constraints, including all 80 source modes,
six independent row coordinates, 14,922 mover/row selectors, 468 row-pair selectors,
55,164 mover planes, 1,696 row-pair planes, 544 rigid coordinate links and 183
different-owner rectangle pairs. Its 474-value partial hint covers only the rows.
[Complete preparation](h5-expanded-joint-and-staged-row-constructions-20261104/expanded-preparation-charges.json) costs 33.172268 s,
including the source-valid short11, individual domains, all fresh geometry/control
processes and the complete 3.326033 s model build.

[Response readback](h5-expanded-joint-and-staged-row-constructions-20261104/expanded-response-audit.json) verifies one closed UNKNOWN
call: 21.990130 s allocated, 22.166207 s returned, 2,644 branches and zero conflicts.
The **0.176077 s solve-slice overrun is preserved**. Preparation-inclusive
algorithm/shared totals are 56.195769 / 56.273224 s, within 60/90 s. There are no
incumbents, assignments, source66 checks or native calls.

## Deterministic staged construction

The separate staged method fixes the already selected row control before trying
to place companions. [Its point-domain audit](h5-expanded-joint-and-staged-row-constructions-20261104/staged-packet-audit.json)
binds all 13 cogs and the fixed29/short11 to the independently checked source53
control. It preserves every identity and source mode. The packet translation
domain is exactly X=Y=0; the two compatibility variables are constants, not
additional freedom. The closed joint model and its solver output are not inputs
to this construction.

Fresh combined no-fit regions against all 13 fixed cogs replace three independent
row disjunctions. [Source readback](h5-expanded-joint-and-staged-row-constructions-20261104/staged-source-region-audit.json) certifies
127 rounded regions using 5,602 exact support proofs, with minimum separation
0.225999999515 mm. [Integer readback](h5-expanded-joint-and-staged-row-constructions-20261104/staged-integer-audit.json) verifies
475 conservative plane implications and every original mode/rectangle.

[The staged-model audit](h5-expanded-joint-and-staged-row-constructions-20261104/staged-model-audit.json) checks all 1,756 variables
and 5,011 constraints: 13 independent orthogonal originals, all 80 modes, 836
combined region selectors, 3,127 planes, all 20 rigid components and 183
different-owner pairs. No objective, capacity table or solver hint is used.
[Its complete preparation ledger](h5-expanded-joint-and-staged-row-constructions-20261104/staged-preparation-charges.json) costs
32.388642 s and includes **every source/domain/region/integer/control process used
by stage one**, the fixed-packet preflight, fresh combined regions, integer
conversion and complete stage-two model build. Neither stage receives free cached
placement preparation.

[Response readback](h5-expanded-joint-and-staged-row-constructions-20261104/staged-response-audit.json) verifies one closed
grid-INFEASIBLE call: 22.958172 s allocated, 0.707276 s returned, 16,357 branches
and 1,638 conflicts. Algorithm/shared totals are 33.760403 / 33.819703 s, with no
solve-slice or overall overruns. It has no assignment or independent continuous
unsatisfiability certificate. This control is not retried with new seeds or time.

## Remaining work

[The next method](h5-expanded-joint-and-staged-row-constructions-20261104/next-step.json) is an independently certified reduction
of the expanded joint integer representation before considering any further
search. Both current solver calls remain closed. A fixed-cog frontier of two
choices / three distributions and all 440 whole-job allocations remain unchanged.
Full66 original-source validation, native/material checks, production integration
and the H5 matrix remain required. H2 keeps its original gate and 22 reserved
vectors remain unopened. Production, READMEs and release assets are unchanged;
no new release qualifies.

Main e47197f1 is already pushed. Its four maker/browser/smoke jobs have passed;
the two native checks remain live in
[CI41901621693](https://github.com/skulitom/Nestbolt/actions/runs/41901621693) at review.
This checkpoint waits for all six jobs and the aggregate run before another
normal push; no live run is cancelled.

[The raw manifest](h5-expanded-joint-and-staged-row-constructions-20261104/raw-manifest.json) contains 193
new canonical members and 6,155,039 compressed bytes.
[External evidence](h5-expanded-joint-and-staged-row-constructions-20261104/external-evidence.json) and
[source bindings](h5-expanded-joint-and-staged-row-constructions-20261104/source-bindings.json) preserve exact historical inputs.
An independent archive reader checks all members, aliases, parent references,
input hashes and local report links before commit.
