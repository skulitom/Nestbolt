# Independent checker speed diagnostic

Boundary-distance checks skip segment pairs only when their bounding-box separation is already greater than the closest known distance, including a conservative integer-grid allowance. Full precision, exact topology checks, scoring and search work remain unchanged.

| Job | Validation before / after CPU s | Reduction | Full search before / after CPU s | Reduction |
| --- | ---: | ---: | ---: | ---: |
| m-public-gear-3 | 1.242188 / 0.835938 | 32.70% | 44.046875 / 36.671875 | 16.74% |
| m-mechanical-batch-1000 | 0.500000 / 0.453125 | 9.38% | 41.359375 / 41.296875 | 0.15% |

Validation timing uses two interleaved attempts per binary on CPU 12. The full searches are one pair per job, on CPUs 8 and 10 respectively, with the same seed 0, 6 passes and a 40M collision-query allowance. Operating-system load varies. The 1,000-part search difference is too small to establish a speedup. These are diagnostics, not the equal-budget G4 population.

Both complete solver outputs (including layouts, histories, work counters and reports) are byte-identical before and after. The new checker also reproduces all 104 saved development validation reports exactly: 35 sheet, 30 maker, 39 strip. No held-out maker solve was used.

An earlier edge-sort shortcut preserved results but gave no measured speedup and was reverted. Its full timings and source patch remain in the record.

Two new tests compare the distance calculation with the exhaustive reference: 3,000 fixed-seed cases in both directions, plus curved/multipart boundaries, one-grid gaps, touching and large coordinates. The existing 10,000-case adversarial fuzz test also passes.

[All timing attempts, profiles and source hashes](validator-speed-20261012T0420.json). [104-report replay](validator-replay-20261012T041750Z-d3c8167a.json).
