# Short-sheet cog transfer — 2026-10-28

The proposed short-sheet allocation of **seven brackets, five inserts and one
cog** was not constructed. The bounded finite enumeration is closed; its failure
does not prove the allocation impossible. It does independently validate a
different allocation with **seven brackets, four inserts and one cog**, which
can support further structural work. Neither result closes H5.

## Construction and independent readback

Nine original placements remain fixed: three bracket-pair/insert groups from
the source-valid short sheet. The remaining one bracket, one cog and two inserts
are mandatory. Preparation uses all8 allowed bracket modes,36 finite cog phases
and both insert outer classes, with380 moving-pair configuration obstacles.
Every obstacle derives from the original filled source outlines and a
conservative mitred clearance buffer. The46 free-region representative checks
pass. Independent preflight verifies all46 source modes and3,420 direct pair
samples before the construction call.

The declared search enumerates legal-region vertices and representative points:
47 bracket poses,115 bracket/cog combinations,635 first-insert poses and1,270
second-insert region checks. It exhausts those candidates in0.152079 seconds,
0.565650 shared seconds, below60/90 limits. No second-insert region with positive
area remains. There is no source13 candidate, retry, restart or native call.
This is a diagnostic construction, not a timed H5 quality run. The finite
angles, anchor selection and conservative buffer prevent any unrestricted
infeasibility claim.

The independent reader replays the entire declared enumeration. All635
12-part prefixes pass original-ring readback:41,910 source-pair checks and
30,480 stock-edge checks, with minimum gap0.2243086725mm and extra stock0.0126mm.
These exceed the unchanged required0.2117086725mm gap and0.0114440918mm stock
guard. The first source-valid prefix is retained in full; original cog copy14
moves to the short sheet without any geometry or quantity change.

Reconciliation with the unchanged50 first-sheet originals gives a valid
62-part inventory:18 frames,9 brackets,20 inserts and all15 cogs. All1,291
source pairs,248 stock edges,80 holes and8,806 hole vertices pass. Bracket
copies7/10/11 and insert4 remain explicitly mandatory. This is not a better
part count than the earlier valid64 and is not a complete66-part witness.

## Main CI and next action

The reconciled main head `f4f6f1fe` now
[passes all six jobs](https://github.com/skulitom/Nestbolt/actions/runs/40668367016),
including the formerly pending Windows checks. This allows the next normal main
push after checking the remote refs and live runs again. The queued checkpoints
change evidence and documentation only; production, READMEs and upstream
Sparrow/Studio heads and releases remain unchanged.

The next structural question is whether the13-part short allocation can fit
when all its placements are free. Its existing necessary projection/area
frontier survives. A new bounded necessary model must cover all bracket modes,
insert classes and real cog angles before any exclusion could be claimed.
An assignment would still need source reconstruction and independent validation.
H2/H5 remain open at **60% completed milestone weight**. All22 reserved H2 vectors
remain unopened, and no new release qualifies.

[Preflight](h5-short-cog-transfer-20261028/preflight-checks.json),
[closed search](h5-short-cog-transfer-20261028/search-result.json),
[independent replay](h5-short-cog-transfer-20261028/replay-checks.json),
[retained short12](h5-short-cog-transfer-20261028/short-source12.json),
[full inventory checks](h5-short-cog-transfer-20261028/inventory-checks.json),
[main CI](h5-short-cog-transfer-20261028/prior-main-ci-jobs.json),
[next step](h5-short-cog-transfer-20261028/next-step.json),
[complete archive](h5-short-cog-transfer-20261028/raw-manifest.json).
The byte-verified archive contains469 canonical files
and447 identical-content aliases,
totalling674,425 compressed bytes.
