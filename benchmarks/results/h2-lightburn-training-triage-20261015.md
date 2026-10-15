# LightBurn training labels: one remaining membership mismatch

This read-only audit compares frozen training labels with the current build's
already verified imports and writer results. It reads no held-out geometry and
does not rerun or modify the product during the H4 quality measurement.

Of 56 original training projects, 45 import and 11 reject with the previously
recorded reasons. Exact top-level unit membership matches the label for 44 of
the 45 imports. The remaining file is the MIT `k.lbrn2` fixture from
`jlucaso1/lbrn2-to-svg`, frozen as L36. Its label requires two units: the small
ellipse separately, and the outer path together with its contained Text.
Nestbolt currently returns three separate units.

The source omits CutSetting elements. The reader reports three missing-setting
warnings, but the unit builder only considers explicitly declared cutting
layers as attachment candidates. Its native reference save contains a Cut
setting for layer 0. Native behavior with omitted settings needs verification
before choosing the correction. Source review also finds the explicit-setting
lookup in cutting-sidecar classification; that path needs the same review.

The raw report also retains a preliminary comparison of labelled cutting holes
with collision-footprint holes. These measure different things: a rigid unit's
conservative collision union can fill a hole while its original editable cut
paths remain preserved. That comparison is diagnostic only, and is neither an
H2 pass nor proof of missing exported cuts. H2 needs cutting topology derived
from the original paths, alongside membership, layer and warning checks.

The earlier H3 reader, geometry and canonical-writer checks remain valid in
their measured scope. They did not prove every membership expectation, so the
training requirement audit is not yet complete. Resolve this training issue
before evaluating the three reserved native projects. All labels, files,
previous results and the held-out allocation remain unchanged.

The [machine report](h2-lightburn-training-triage-20261015.json) identifies every
label, expected/actual unit membership, rejection and original evidence hash.
