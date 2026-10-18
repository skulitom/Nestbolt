# H5: joint repair of saved partial constructions — 2026-10-18

Four deliberately overlapping complete proposals call the existing native joint
repair helper once each. **All four expire; none returns a complete target layout.**
This is a mechanism diagnosis, not a new quality comparison or evidence of geometric
infeasibility. H2/H5 remain open at 60%.

The [previous independent construction](h5-outline-construction-20261018.md)
provided physically legal partial layouts. Every original pose is preserved in
the new inputs. Missing original copies are restored using the original allowed
rotations/reflections: free parts sample 15-degree angles; positions come from an
11×11 legal translation grid and alignments with neighbours. All **308,326** scores
are saved, and the selected lexicographic minima are independently checked.
The original public library/request validator rejects all four complete proposals
only for overlap/clearance, including the aggregate `total_overlap` code.

The native observer measures each saved partial before calling repair, using a
separate clock and no separation. Every placed part already has positive native
collision loss. These loss values are internal scores, **not overlap areas**.

| Saved case | Partial inventory | Restored copies | Partial items with native loss | Partial joined loss | Complete proposal loss | Repair |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| large-plates-k0.2 | 63/66 | 3 | 63/63 | 1,304,395.125 | 1,480,147.625 | expired |
| large-plates-k1.5 | 58/66 | 8 | 58/58 | 1,222,450.750 | 1,403,029.625 | expired |
| panel-hardware-k0.2 | 147/178 | 31 | 147/147 | 1,349,541.125 | 1,724,299.000 | expired |
| panel-hardware-k1.5 | 146/178 | 32 | 146/146 | 1,308,518.375 | 1,665,826.875 | expired |

Each actual helper call keeps seed 0, the pre-existing authored allowance of 12
work seconds, the exact target containers (rounded down to f32) and the original
conversion guard. Runs are serial on logical CPU 8 (CCD0). They stop at 12.009–12.057
charged seconds due to the existing work-check granularity; actual process times
are 13.505–18.899 seconds, below the 60-second hard limit. No budget, four-step
runtime cap or quality gate changes. Expiry returns no repaired layout, so the
failed internal best placements and final losses are unavailable from this helper.

Independent filled-outer checks cover **32,527** original partial/proposal pairs
and **5,395** selected-insertion comparisons. All missing quantities are restored,
all original partial poses remain exact, and both target stock bounds hold.
The complete proposals' overlaps are retained and never counted as valid results.
The native JSON echoes are also checked with original coordinates and unchanged
geometry tolerances.

The initial input checker omitted the expected aggregate overlap code; its first
proposal and all scores were reused unchanged. The first native build failed
because the appended test tried to clone a non-Clone report; a fresh isolated
source and target fix only that test initializer. The audit initially assumed
exact cross-language float equality and explicit zero counters. Native JSON
echoes have one-ULP differences (at most 4.55×10⁻¹³), and the declared serializer
omits zero counters. Every difference is enumerated and bounded to one ULP;
original files and target values remain authoritative. Three audit failures and
the intermediate generator's predicate-name error are preserved. **No search or
native repair was repeated during these corrections.** Runtime source and all
171 prior test bodies remain exact. The diagnostic itself passes four times by
correctly recording four failed repairs.

All 289 archived files, CRCs and SHA-256 digests verify. The archive
includes the compiled diagnostic's source, failed source, inputs, logs, outputs
and auditors; the binary is retained locally and identified by SHA-256.

[Checks](h5-pattern-joint-diagnosis-20261018/checks.json),
[raw evidence and source](h5-pattern-joint-diagnosis-20261018/raw.zip),
[manifest](h5-pattern-joint-diagnosis-20261018/raw-manifest.json),
[source review](h5-pattern-joint-diagnosis-20261018/source-review.json).

Do not integrate this offline constructor or rerun the quality pilot. First export the exact native inflated polygons, container bounds and per-item collision partners for the already-saved partials, without calling separation. Independently compare native vertices with the original transformed outer contours, decompose pair and static losses, and distinguish the known conversion margins from any transform or observer mismatch. The partial layouts have only 0.0011 mm added part clearance, while conversion_guard is 0.011444091796875 mm for large plates and 0.0095367431640625 mm for panel hardware. This makes margin-driven collisions plausible, but the current aggregate losses alone do not prove their sole cause. Only after that diagnosis should a native-compatible initial construction be considered, retaining the original physical geometry, conversion guard, containers, quantities and target. The helper does not return a failed best snapshot here, so no final overlap or distance-to-feasibility claim is supported. Original budgets, four-step cap, hole reservation, thresholds and reserved-input isolation remain unchanged.

[All six hosted jobs on preceding main `912cd5b` pass](h5-pattern-joint-diagnosis-20261018/main-ci-912cd5b.json),
including Windows, Linux, browser tests and maker rebuilds. This confirms that
specific checkpoint, not subsequent commits. Production, v0.2.0-alpha.1 release
assets and the accurate English/Japanese/Chinese READMEs remain unchanged.
There is no newly qualified release candidate.
