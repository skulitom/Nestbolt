# Common-line placement pairs on the two remaining fixed arrangements

On 20 November the independent replay confirmed **6,603 additional incompatible
pairs of candidate positions**. Four bracket positions can be removed from the
first arrangement. The second retains every position. Both arrangements remain
open and the best validated layout for the 66-part development case has 64 parts.

| Omitted cog sites | Pairs checked | Already incompatible | Newly incompatible | Positions left | Joint area upper bound (mm²) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0, 5, 10 | 119,792 | 3,398 | 4,733 | 3,756 | 497,091.028543 |
| 5, 10, 11 | 146,128 | 1,599 | 1,870 | 4,583 | 484,584.183454 |

Each case fixes 18 frames, 11 inserts and 12 cogs on the first sheet. Eight
brackets and eight more inserts must fit around them. Their combined occupied
area needs at least 478,384 mm². Both upper bounds exceed that requirement.
The other 453 of the 455 fixed cog arrangements have already been excluded.
The 440 possible allocations between the two sheets remain open.

The [previous checkpoint](h5-direct-restriction-fixed-point-20261109.md)
supplies the starting 8,343 positions. For each arrangement the frozen sample
selects 16 bracket and 16 insert positions, then pairs each with every other
eligible position. Across 64 batches, independent sums over the original
physical records verified all 797,760 family and combined area bounds.
Of the 11,600 incompatible pairs, 3,384 were already in the original graph
and 1,613 had been identified by earlier tests. The cumulative additions to
the graph now total 20,909.

The final audit checked both directions of each original conflict, every new
edge and its source pair, and every removal against the original clique cover.
It reconstructed the remaining occupied rectangles from the source geometry
and reproduced all six area bounds with a horizontal sweep. All 132 new
numerical processes closed. Cumulative preparation took 1,660.138836 seconds.
This was an offline calculation with zero new optimizer calls.

The [results](h5-direct-pair-replay-20261120/checks.json) and
[archive checksum](h5-direct-pair-replay-20261120/archive.json) accompany the
[replay archive](h5-direct-pair-replay-20261120/evidence.zip). Extract it into
an empty directory, run `python output/audit_direct_pair_frontier_20261120.py`
with Python 3.11, and compare the generated
`output/h5-direct-pair-frontier-20261109/audit/checks.json` with the linked
results. A clean extraction reproduced the result byte for byte.

The [original cutting comparison](h5-cutting-development-20261015.md) still
determines H5. Two mechanical jobs exceed the +1% material limit at both kerfs.
