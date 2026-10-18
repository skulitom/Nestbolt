# H5: joint selection from saved placements — 2026-10-18

Joint selection finds an independently valid **63-part partial arrangement**, but
still leaves **three of the original 15 cogs unplaced**. No complete target witness
is found. This is a finite offline construction; production and H5 remain unchanged.

The [terminal diagnosis](h5-terminal-repair-diagnosis-20261018.md) showed local
repair trapped around a fixed frame block. This follow-up chooses compatible
placements together from the previously recorded geometry instead of placing
each part greedily. It uses the closest large-plates / 0.2 mm case with its
original stock, quantities, filled holes and 325.926902 mm second-sheet target.

The pool contains **2,614 unique placements**: 500 frames, 465 brackets, 137 inserts
and 1,512 cogs. Inputs include the known zero-native-loss partial, the in-bound
rejected terminal poses, all **25** previously generated frame configurations,
and individual members of **21,873** valid saved beam candidates. Compound members
become independently selectable, retaining their actual original transforms.
The 4,000-candidate cap is not reached; one out-of-stock terminal cog is excluded.
Deduplication rounds only identity keys, retaining unrounded original coordinates.

Actual filled-outer distances define **332,265 incompatible candidate pairs**.
A binary model selects at most each original family quantity, exactly all 18
frames, and at least the known partial's filled area, maximizing covered area.
The existing 63-part partial verifies as a feasible certificate for this exact
model before solving. No frame location is fixed by the selection constraints.

The solver reaches its declared 120-second limit after **121.329742 real seconds**
and returns an incumbent, with status **time limit reached**, not optimal. It
selects all 18 frames, 12 brackets and 21 inserts, plus 12 cogs: the same original
filled area as the known partial, **4,331,552.627256 mm²**. Only 24 of its 63 selected
candidate entries are from that known partial; the others come from the terminal,
frame catalog and beam. This is a newly selected arrangement, not a fallback.

The reported finite-model upper bound is **4,347,053.331371 mm²**, below the
4,481,740.784070 mm² required for all original parts. This is an uncertified solver
bound for these discrete choices, not a global geometric infeasibility result.
The time limit, missing inventory and lack of a complete witness remain explicit.

An independent audit reconstructs **every candidate's exact source provenance**,
rebuilds each original polygon with a separate matrix transform, and checks stock,
orientation and reflection requirements. It enumerates **2,700,951** same-sheet
candidate pairs, filters by an independently implemented bounding-box distance
bound, and evaluates **393,757** original-polygon distances. The resulting conflict
graph agrees exactly with all 332,265 recorded edges, without using the producer's
spatial-index query. All **1,303** selected-part pairs pass physical clearances;
the original public CLI rejects **only the missing cog quantity**.

[Checks](h5-saved-placement-selection-20261018/checks.json),
[raw pool, conflict graph, solve, sources and audits](h5-saved-placement-selection-20261018/raw.zip),
[manifest](h5-saved-placement-selection-20261018/raw-manifest.json),
[next investigation](h5-saved-placement-selection-20261018/source-review.json).
All 32 archive members, CRCs and byte hashes verify.

The finite placement pool has been jointly selected and its full conflict graph independently checked. It still gives a 63/66 layout, missing three cogs. Do not repeat that pool, increase its solver allowance or present its reported dual bound as a global geometric proof. Its poses were generated mostly by the earlier limited beam, so joint selection does not cure missing contact locations. Next generate a materially different finite pose pool with original-outline contacts and sheet-boundary symmetry, including contact positions beyond the beam's three lowest choices. A 180-degree rotation of a candidate about its own target-sheet centre preserves this job's allowed free/quarter-turn rotations; verify each such transformed pose before adding it. Use the audited selected layout as an explicit feasible partial certificate, declare candidate and offline limits before running, and retain truncation, timeout and incomplete quantities. A complete original-stock, original-quantity witness is still required before any new runtime proposal or matched quality pilot. Native margins remain a separate qualification after physical geometry; never change reserved holes, material target, conversion guard, production budgets or the four-step repair cap.

No native packing search, quality pilot, runtime change or release qualification
is performed. Published preview assets and all three accurate READMEs remain
unchanged. H2/H5 stay open at **60%**.
