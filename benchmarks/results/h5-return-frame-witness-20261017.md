# Return-group orientation witness — 2026-10-17

The original six-part layout and an authored quarter-turn exchange both pass
the independent validator with **identical metrics and 19,500 mm² material**.
Returning the same three squares by translation alone produces overlaps and
out-of-bounds geometry. Rotating the group into the incoming part's vacated
orientation fits, preserving all quantities and allowed orientations.

The initial script correctly validated these three outcomes, then failed a
hardcoded 19,700 mm² expectation. That bookkeeping error assumed the last listed
sheet supplies the offcut. The validator selects the largest reusable offcut:
sheet-0 saves 500 mm², so both valid layouts use 20,000 - 500 = 19,500 mm².
The separate review uses the original saved reports without rerunning validation,
changing geometry or relaxing any tolerance. The original script and failure remain.

This supports testing reciprocal rigid-frame initialization for returned groups,
with an all-or-nothing legality check and the previous translation fallback when
any part disallows the new orientation. Both repairs, independent whole-job
material/geometry acceptance and deadlines must remain. It proves no improvement
on the mechanical development jobs. No optimizer runs or production changes;
H2/H5 remain open at 60%.
