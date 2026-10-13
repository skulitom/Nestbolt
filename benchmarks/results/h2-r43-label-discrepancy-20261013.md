# R43 training-label discrepancy — 2026-10-13

**Scoring is unchanged and H2 is not passed.** This corrects the diagnosis in
the encoding checkpoint, which described the count mismatch as a missing island.
The frozen input, label, split and earlier failing report are retained.

The file is the training-only Iris PE MX/Alps switch plate, label `R43.json`.
DXF polylines `7D` and `21A` trace the same switch cutout. They differ only in
four Y coordinates, by **6.963318810448982e-13 mm**. The independent reference's
line-network polygonization produces nearly coincident rings and classifies one
as an island inside the other. Its expected extra part has the same bounds as
the imported switch hole, not a separate physical cutout.

[Reproduction data](h2-r43-label-discrepancy-20261013.json) contains both source
polylines, their Hausdorff distance, frozen hashes and the original reference
topology. Rounding the diagnostic network to **1e-9 mm**, solely to test the
hypothesis, changes that reference result from two parts to one plate with 37
holes. The product already returns that plate. No product geometry change was
made in response to this discrepancy.

Reproduce with:

```powershell
.cache/shop-venv/Scripts/python.exe scripts/h2_label_discrepancy.py
```

The script filters manifest entries to training before reading any geometry or
label. It verifies source and label hashes and does not rewrite the corpus.
Approval for a documented scoring exception has been requested from Artem;
pending that decision, the original count mismatch remains a failure.
