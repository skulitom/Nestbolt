# H5: frame capacity and joint small-part construction — 2026-10-20

**All 18 frames can fit around the selected 21 inserts.** Two such frame
arrangements pass original geometry checks, but independent finite-pool bounds
allow at most eight and six cogs alongside them, below the required fifteen.
A changed joint search improves its own seed from 16 to 21 small parts,
retaining all 18 frames, 12 brackets, 21 inserts and nine cogs. Six cogs are
still missing. This is not a complete or overall better packing result.
H2/H5 remain open at 60%.

## Necessary frame capacity

The [preceding construction](h5-insert-blockers-and-frame-contacts-20261020.md)
fixes 21 insert positions and supplies an expanded pool with 240 new frame
contacts. A necessary relaxation removes bracket/cog restrictions, keeps
all 1719 compatible frame choices and their conflicts, and maximizes frames
from the feasible 16 through the original required 18. Every model field and
complete feasible hint is reconstructed.

One declared 10-second, eight-worker, seed-zero call finishes `OPTIMAL` in
**0.776407200 seconds**, reaching 18 frames. All three callbacks and the
distinct final selection pass original geometry and frozen CLI geometry
checks; their deliberate missing bracket/cog quantities remain failures.
There are two distinct complete 18-frame sets.

## Diagnose what those frames leave for brackets and cogs

Each complete frame set and all 21 inserts are fixed in turn. Every compatible
original bracket/cog pose and projected conflict remains. The diagnostic
allows at most the original 12 brackets and 15 cogs, maximizing their combined
count, then rounded filled area. A count-dominating integer weight makes the
ordering exact. Complete feasible hints use compatible old small-part poses.
Both models and all filters are independently reconstructed.

Each case declares one 20-second limit, eight workers and seed zero. Both
finish `OPTIMAL` quickly:

| Frame case | Seconds | Brackets at optimum | Cogs at optimum | Small-part count | Independent cog upper bound |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.457994200 | 11 | 5 | 16 | 8 |
| 1 | 0.431435800 | 12 | 1 | 13 | 6 |

The bracket/cog columns describe the selected best count and area tie; they
are not separate maximum cog counts. All six returned layouts pass original
geometry and fail the frozen CLI only for their actual missing quantities.
Independent geometry checks **228,448** small-part/fixed-part pairs and
reproduces every eligibility decision.

Separate saved clique covers bound cogs at **8** and **6**, and combined small
parts at **23** and **18**. Every cover entry is verified against an original
pairwise-conflicting clique or singleton. These certificates independently
exclude the required 15 cogs for both fixed frame arrangements. They do not
exclude other frame arrangements or new continuous positions.

## Select frames and small parts together

The expanded parent model is changed to require all **18 frames**, preserve
the **21 fixed inserts**, and jointly choose 0–12 brackets and 0–15 cogs.
It requires at least the best audited seed's 16 small parts, maximizing their
actual count and then rounded filled area. All 5316 variables and 15,132
constraints are reconstructed against the audited parent; every original
and new conflict remains. A complete feasible hint contains 18 frames,
11 brackets, five cogs and 21 inserts.

Its single declared 30-second, eight-worker, seed-zero call returns `FEASIBLE`
after **30.091457300 seconds**. Seven retained callbacks progress through
small-part counts 16, 17, 17, 18, 19, 20 and 21. The final arrangement has
all 12 brackets and nine of the required 15 cogs. The final objective bound
still permits all 27 small parts, so no optimum or impossibility is proved.
There is no retry or extended search.

All seven callbacks and the distinct final selection receive original
geometry checks. Seven frozen CLI calls are fresh; one reuses an exact,
hash-recorded prior layout and result. Every result fails only its original
quantity shortfall. The final minimum geometric clearance is 0.201000 mm
and material charge is 4,985,103.45 mm², within the unchanged target.
Neither is native-margin qualification.

The final 60-part partial contains **4,181,364.4704 mm²** of filled outer area,
below the previously documented 58-part partial's **4,323,340.7841 mm²**.
The gain over this changed model's seed is therefore not reported as a new
best overall partial or H5 improvement. It supplies a new arrangement of all
required non-cog parts for a different cog-contact construction.

## Remote changes and README

Remote main advanced to **abeb2739**, adding a static comparison page about
nesting tools for AI agents, its v0.1.0 records, navigation/index links and a
three-line README link. Its push cancelled the older f321537 workflow:
four jobs passed and the Windows/Linux checks were cancelled. This is not
reported as a successful complete check run.

The disjoint changes merge locally as **09f59894**. The merge audit compares
every incoming file with its exact remote parent and every local evidence
file with its local parent: **11 remote files and 25 local files are preserved**,
and the working tree matches the merged Git blobs. Core source retains its
reviewed digest. English README changes come only from the remote addition;
Japanese and Chinese README hashes remain unchanged. Existing preview,
stable-release and v1 benchmark descriptions are preserved.

The abeb2739 hosted checks are still running in the saved snapshot; the local merge is not pushed over them. No release is made, and these comparison-page changes receive no
v1.1 benchmark credit.

## Next work

Do not repeat the frame-only relaxation, the two fixed-frame completions or the joint30-second model unchanged. The joint final layout supplies all18 frames,12 brackets and21 inserts but only9 cogs. Next hold its51 non-cog poses fixed and construct conservative original-outline free translation regions for cog phases 0,4.5,9,13.5 degrees on both target sheets. Keep every compatible original cog pose and the nine audited seed cogs. Add bounded, declared free-region boundary contact samples; independently verify every new pose and every cog-pair conflict before one changed cog-only completion model capped at the original15. Record incomplete regions or generation limits without an impossibility claim. This is a new conditional construction, not an extension of the expired search. Only all66 copies passing original geometry, frozen CLI, native margins and unchanged H5 material/cutting gates can qualify H5. H2 remains open under Artem’s original-denominator decision.

No reserved held-out evaluation, native packing or quality run occurs.
All original acceptance rules and published benchmark results remain intact.

[Checks](h5-frame-capacity-and-joint-small-parts-20261020/checks.json), [frame outputs](h5-frame-capacity-and-joint-small-parts-20261020/frame-layout-audit.json),
[small-part capacity and outputs](h5-frame-capacity-and-joint-small-parts-20261020/small-layout-and-capacity-audit.json),
[joint outputs](h5-frame-capacity-and-joint-small-parts-20261020/joint-layout-audit.json), [merge verification](h5-frame-capacity-and-joint-small-parts-20261020/merge-audit.json),
[cancelled earlier workflow](h5-frame-capacity-and-joint-small-parts-20261020/main-ci-f321537-cancelled.json),
[current remote CI](h5-frame-capacity-and-joint-small-parts-20261020/main-ci-abeb2739.json), [source review](h5-frame-capacity-and-joint-small-parts-20261020/source-review.json),
[all models, certificates, layouts and logs](h5-frame-capacity-and-joint-small-parts-20261020/raw.zip),
and [manifest](h5-frame-capacity-and-joint-small-parts-20261020/raw-manifest.json).
All 183 archive members, CRCs and byte hashes verify.
