# Collision-guided repair screening experiment

Matched-CPU diagnostic of a surrogate early-rejection prefix for collision-guided two-blocker repair. CPU 4, seed 0, four passes, frozen 1000-part development job; two interleaved before/after pairs, every attempt retained. Not a G4 result.

Not adopted: final layouts and complete stdout are identical, but elapsed/CPU timing does not show a consistent benefit across pairs. Production remains at the pre-experiment implementation.

| Variant | Seconds | CPU seconds | Layout SHA-256 |
| --- | ---: | ---: | --- |
| before | 32.672 | 32.016 | `c01add99d4a2289699ec7794be5267e4e1d57c8a6ed6ec266b9a8776140c251a` |
| after | 32.000 | 31.250 | `c01add99d4a2289699ec7794be5267e4e1d57c8a6ed6ec266b9a8776140c251a` |
| before | 30.219 | 29.844 | `c01add99d4a2289699ec7794be5267e4e1d57c8a6ed6ec266b9a8776140c251a` |
| after | 30.360 | 29.922 | `c01add99d4a2289699ec7794be5267e4e1d57c8a6ed6ec266b9a8776140c251a` |

[Both source/binary hashes and all raw timing evidence](displace-profile-20261012T0219.json).
