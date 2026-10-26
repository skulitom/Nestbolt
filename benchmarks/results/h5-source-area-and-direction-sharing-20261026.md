# H5: source area propagation and shared directions — 2026-10-26

**Both distinct bounded searches return UNKNOWN.** No layout or impossibility
proof is obtained. H2/H5 remain open at **60%** completed milestone weight.
All 66 originals remain required, with nine movable and 57 fixed in the
original source construction. No witness cog coordinates are locked.

| Representation | Variables | Constraints | Result | Solver / total seconds |
|---|---:|---:|---|---:|
| area-constrained | 167,044 | 376,377 | UNKNOWN | 46.532948 / 49.698399 |
| shared-direction | 111,710 | 265,709 | UNKNOWN | 48.508436 / 51.313156 |

## Verified area propagation

The first model preserves every original variable, constraint and all 72 hints,
then appends exactly 14 independently proved source-region area inequalities.
The independent reader reconstructs all 184 sheet-mode coefficients and
activations and restores the complete parent protobuf. Across all 42 count
allocations, the original global-area rules admit 23; the new necessary bounds
exclude another nine. The 14 remaining allocations are not proved feasible.

## Exact reduction in auxiliary variables

The second model replaces 156,789 mode-specific direction flags with 101,455
shared flags. Sharing is restricted to identical normalized integer inequalities
for the same ordered physical pair. Positive-gcd division and an exact ceiling
preserve every integer boundary. Each shared flag is defined by a plane and its
complement. All 394 source pair modes, active face clauses, displacement bounds,
the original base, the 14 area rules and the 72 hints are retained.

An independent audit verifies both complete auxiliary-constraint multisets,
all 158,777 direction uses and the two-way assignment proof. From a shared
assignment, each old flag becomes active-mode AND shared truth. From an old
assignment, evaluate every shared plane at the original coordinates. This
proves equal feasible projections within the original source construction.
It removes **55,334 variables (33.1%)** and **110,668 constraints (29.4%)**.
Actual solver import/export matches both audited models.

## Closed calls and limits

Each call uses eight workers, seed zero, a 45-second soft solver limit and a
60-second shared loading/audit/search budget with a ten-second shutdown reserve.
The actual soft-limit overruns are **1.532948s** and **3.508436s**; both total
budgets pass. Both calls are closed and must not be restarted, extended or
reseeded. There is no candidate for original-geometry or native validation.

The logs start search at 18.27s and 15.05s respectively. These single diagnostics
do not establish a production speed or packing improvement. Next investigate
whether the exact existential projection needs only shared flag-implies-plane
constraints, allowing removal of 101,455 complement clauses. This needs its
own independent assignment proof and actual import check before any new call.

The construction remains conditional on the recorded orientations, inward
integer domains, copy-order restrictions and fixed 57 placements. It does not
prove unrestricted packing impossible. A full original-geometry/native-valid
target, production integration and the complete 13-job/two-kerf H5 matrix remain
required. Offline work is not production-budget qualification.

## Repository and release state

The prior four-checkpoint push to main **68c82ae1** is retained with its verified
receipt. At the fresh 01:27 UTC snapshot, five of its six CI jobs have passed;
Windows checks are still running. Wait for terminal main CI before another
push so its result is preserved. Upstream Sparrow/Studio heads and release
state are unchanged. Production code and READMEs are unchanged; preview
v0.2.0-alpha.1 and stable v0.1.0 remain appropriate. No new release is qualified.
H2 retains its original gate and all 22 reserved vectors remain untouched.

Evidence: [comparison](h5-source-area-and-direction-sharing-20261026/comparison.json),
[area audit](h5-source-area-and-direction-sharing-20261026/area-constrained/model-audit.json),
[equivalence proof](h5-source-area-and-direction-sharing-20261026/equivalence-proof.json),
[shared-model audit](h5-source-area-and-direction-sharing-20261026/shared-direction/model-audit.json),
[prior push receipt](h5-source-area-and-direction-sharing-20261026/prior-main-push-receipt.json),
[checks](h5-source-area-and-direction-sharing-20261026/checks.json), and [raw manifest](h5-source-area-and-direction-sharing-20261026/raw-manifest.json).
**369** canonical files and **76**
exact-content aliases are size/SHA-256/CRC verified in
**1** independently readable archive part(s).
