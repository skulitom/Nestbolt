# Balanced-pair identities and immediate effects — 2026-10-18

**All four diagnostic layouts validate.** The observer records which
original part types move between sheets, repair stages and immediate
material/last-sheet extent. These are new observations, not a reconstruction
of the failed 72-outcome pilot or a quality comparison.

[The committed plan](h5-balanced-stage-20261018/plan.json) uses the two
mechanical development jobs, kerfs 0.2 and 1.5 mm, seed zero, 60 seconds
and serial physical CCD0 CPU 8. All original algorithm settings remain.
Instrumentation can perturb wall timing. Production stays unchanged.

| Job | Kerf mm | Attempts | Accepted pairs | Same-inventory accepted | Outcomes |
| --- | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | 1 | 0 | 0 | accepted: 1 |
| m-mechanical-large-plates | 1.5 | 8 | 0 | 0 | material_guard_failed: 1, source_repair_failed: 7 |
| m-mechanical-panel-hardware | 0.2 | 1 | 1 | 1 | accepted: 1 |
| m-mechanical-panel-hardware | 1.5 | 1 | 1 | 1 | accepted: 1 |

Of 3 accepted exchanges, 2 return the same original
part types and quantities as they take. This preserves inventory, not
necessarily positions or orientations. Immediate validated material
decreases in 0 accepted exchanges; last-sheet occupied
extent decreases in 0. These observations do not establish
a later benefit or harm from rearrangement.

There are 30 retained proposals across the observed calls;
12 preserve inventory. Retained proposals are not necessarily
attempted, and these counts are not all sampled configurations.

The session took 4.077 minutes. All archive CRCs/member hashes,
trace references, solver counters, original quantities, public exports and
independently recomputed metrics pass. Source, input and binary guards match.
[Every attempt](h5-balanced-stage-20261018/observed-exchanges.json) and
[verification](h5-balanced-stage-20261018/verification.json) are retained.

No original failed result, gate, production implementation or held-out file
is changed. **H2/H5 remain open; completed weight stays 60%.**


The independent filled-outer audit additionally checks all
18,569 same-sheet pairs, keeping hole interiors reserved.
Minimum clearance slack is 9.99999701878e-07 mm,
within the unchanged 1e-7 mm audit tolerance. No new searches are run.

## Next implementation question

Source inspection also confirms that accepting an exchange short-circuits
the following gap-fill and relocation calls in that window. The next isolated
change should test whether gap filling after an accepted exchange can use its
new arrangement, while preserving the total search limit and normal-mode
behavior. This identifies a missed execution path, not a measured quality gain.

The [source review](h5-balanced-stage-20261018/control-flow-review.json) records
the exact call site and source hash. The original experiment is preserved.
