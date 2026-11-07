# Four-row contact phase and companion spaces — 2026-11-07

A source-derived cog phase removes all ten diagonal contacts and gives a valid
**48-part core**. The complete 66-part arrangement still fails **29 pairs**.
The conservative regions generated for the remaining companions can contain
at most **three of the six required brackets**, so this particular construction
is rejected without a solver call. This is not an unrestricted packing exclusion.
H2/H5 remain open at **60% completed milestone weight**.

[The source derivation](h5-four-row-contact-phase-and-companion-spaces-20261107/phase-derivation.json) aligns a tooth-gap bisector
with the two diagonal contact directions of the existing 4/4/4/3 centers. It
produces one common phase, **2.250000000056°**, without an
angle/offset/seed sweep. All centers, non-cog coordinates, modes, weights and fixed
33 rows remain unchanged. The observed 20-tooth pattern is slightly rounded;
no exact rotational symmetry or optimal phase is assumed.

[Independent phase readback](h5-four-row-contact-phase-and-companion-spaces-20261107/phase-audit.json) derives the gap bisector
using normalized vertex-vector sums and checks all 81 scalar gradients, with
maximum error **7.461e-14**. It reconstructs
all 66 original parts and validates the [48-part core](h5-four-row-contact-phase-and-companion-spaces-20261107/valid48-source.json)
with **633 same-sheet pairs and 192 stock edges**. Its minimum pair gap is
**0.230000000000 mm**, above the retained source requirement.
[Original core checks](h5-four-row-contact-phase-and-companion-spaces-20261107/valid48-source-checks.json) preserve every pair.

A separate implementation uses segment intersection, ray containment and
endpoint projection, without GEOS distance/intersection, for all **105 cog pairs**
and **672,000 edge pairs**. [Six analytic controls](h5-four-row-contact-phase-and-companion-spaces-20261107/distance-fixtures.json)
pass. [Direct pair checks](h5-four-row-contact-phase-and-companion-spaces-20261107/direct-cog-pair-controls.json) give minimum cog
gap **1.381413112177 mm**, with maximum difference from GEOS
**1.199e-13 mm**. This is floating-point
validation with positive margins, not an exact all-angle theorem.

[Full66 source checks](h5-four-row-contact-phase-and-companion-spaces-20261107/full66-source-checks.json) have zero stock failures
but 29 pair failures. The fresh objective is **333398.809985 mm²**,
below the failed four-row state's **334586.901596 mm²**
but above original A/W's **244577.060782 mm²**. The
[mathematical key](h5-four-row-contact-phase-and-companion-spaces-20261107/phase-source-state.json) was already closed; changing
continuous angles does not permit another optimizer call.

[Companion construction](h5-four-row-contact-phase-and-companion-spaces-20261107/companion-space-plan.json) covers all 16 declared
bracket/insert center cells. It forms nonconvex forbidden geometry from the
verified clearance outlines via all Cartesian convex-piece vertex differences,
then translates each template to the 15 cogs. The inherited center rectangles
are safe around the fixed frames. Subtracting the forbidden unions leaves
**18 polygon components**. These conservative safe regions are not a complete
necessary cover of all possible original placements.

[Independent geometry readback](h5-four-row-contact-phase-and-companion-spaces-20261107/companion-audit.json) verifies **12 templates,
5,928 convex Minkowski hulls and all 16 regions**. All **227 representative/vertex
proposals** pass independent original **49-part checks**, including the full
48-part core: [proposal controls](h5-four-row-contact-phase-and-companion-spaces-20261107/original-proposal-controls.json).
Individual compatibility does not establish simultaneous placement of six
brackets and twelve inserts. [The complete census](h5-four-row-contact-phase-and-companion-spaces-20261107/companion-space-summary.json)
retains zero-region orientations and every generated proposal.

[The exact envelope bound](h5-four-row-contact-phase-and-companion-spaces-20261107/bracket-envelope-capacity.json) places every
possible original bracket in these recorded constructive regions inside
**[1132.746100, 2560.307234]
to [1493.474998, 2993.474998] mm**.
Exact rational interval sums include 1e-6 mm outward numerical padding. Envelope
area is **156256.130137 mm²**; each bracket requires at least
**39,999 mm²**, a conservative bound below its original 40,000 mm² area with an
explicit rounding allowance. Four brackets already exceed the envelope, so at
most three fit. Six are required. No selection or optimizer is justified within
these regions. The bound does not exclude source-safe positions outside them.

The first region process [fails during serialization](h5-four-row-contact-phase-and-companion-spaces-20261107/four-row-companion-spaces-process.json)
because a NumPy boolean reaches the JSON writer. Complete queries 00–02, the
28,411-byte truncated query03, templates and stderr are preserved. The
[failure record](h5-four-row-contact-phase-and-companion-spaces-20261107/serialization-failure.json) binds the exact malformed bytes.
A separate version converts only the persisted validity flag to a built-in bool;
[its process](h5-four-row-contact-phase-and-companion-spaces-20261107/four-row-companion-spaces-v2-process.json) completes all queries.
The initial correction command's wrong assumption about the failed query number
is also recorded; no geometry process was launched by that command.

[Phase preparation](h5-four-row-contact-phase-and-companion-spaces-20261107/four-row-contact-phase-preparation-process.json) costs
**0.606996 s**, for a retained lineage of
**41.540944 s**. Consuming the failed and corrected
region preparations adds **0.536151 + 0.974325 s**, giving
**43.051420 s** before further work.
[Phase audit](h5-four-row-contact-phase-and-companion-spaces-20261107/four-row-contact-phase-audit-process.json) and
[region audit](h5-four-row-contact-phase-and-companion-spaces-20261107/four-row-companion-spaces-audit-process.json) close under the
same CCD1/one-thread/2 GiB controls. Every process is terminal; no search ran.

[Next](h5-four-row-contact-phase-and-companion-spaces-20261107/next-step.json), compare these conservative regions with a certified
source-necessary outer cover before deciding whether the fixed core itself is
excluded. All [25 mathematical keys](h5-four-row-contact-phase-and-companion-spaces-20261107/closed-problems.json) remain closed;
four earlier arrangements and all 440 whole-job allocations remain unresolved.
Full66/native/material checks, parity and the original H5 matrix are still needed.

[Three preceding checkpoints reached main bf239548 normally](h5-four-row-contact-phase-and-companion-spaces-20261107/prior-main-push-receipt.json)
after all six prior checks passed, preserving all 52 protected files. Fresh main
CI has 5 passed / 1 live jobs in [this snapshot](h5-four-row-contact-phase-and-companion-spaces-20261107/main-ci-at-review.json).
Product code, README and releases are unchanged.

[Archive checks](h5-four-row-contact-phase-and-companion-spaces-20261107/archive-checks.json), [raw manifest](h5-four-row-contact-phase-and-companion-spaces-20261107/raw-manifest.json),
[source bindings](h5-four-row-contact-phase-and-companion-spaces-20261107/source-bindings.json), [historical references](h5-four-row-contact-phase-and-companion-spaces-20261107/external-evidence.json)
and [runtime pins](h5-four-row-contact-phase-and-companion-spaces-20261107/runtime-bindings.json) retain the evidence, including the
expected malformed JSON failure.
