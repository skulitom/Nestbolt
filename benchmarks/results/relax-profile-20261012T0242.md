# Indexed blocker search: timing diagnostic

Single-core development diagnostic, CPU10, seed0, four passes, 1000-part frozen development job. Two interleaved before/after pairs; all attempts retained. No G4 claim.

Keep indexed blocker lookup and dynamic collection cutoff. Completed output and every query count are identical. Both pairs are faster, but unrelated stage timing changes show changing host conditions; do not extrapolate to the full matrix.

| Pair | Version | Wall seconds | CPU seconds | Repair stage seconds |
| --- | --- | ---: | ---: | ---: |
| 1 | Before | 39.828 | 39.328 | 7.984 |
| 1 | After | 27.422 | 27.281 | 3.109 |
| 2 | Before | 30.421 | 30.344 | 6.062 |
| 2 | After | 27.328 | 27.297 | 3.079 |

Map hazard keys to source indices once per receiver, restore source order by sorting. Stop collision collection when blocker count exceeds the worst retained proposal, since it cannot enter the sorted bounded list. No random-stream or candidate-order change.

All four layouts pass the independent checker and have identical full output and layout hashes. The original 60-second pilot timeout remains in its separate report. These four profiles use a 90-second hard watchdog; their actual durations are shown above.

[Full precision and audited profile files](relax-profile-20261012T0242.json).
