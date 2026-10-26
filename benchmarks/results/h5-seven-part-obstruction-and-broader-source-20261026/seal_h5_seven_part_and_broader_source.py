"""Archive the resolved seven-mover model and fresh thirteen-mover geometry."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-seven-part-obstruction-and-broader-source-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'regions59':'h5-partial59-fixed-regions-20261026','domains59':'h5-partial59-joint-prepared-20261026','source59':'h5-partial59-source-model-20261026','search59':'h5-partial59-source-search-20261026','conflicts':'h5-partial59-domain-conflicts-20261026','master':'h5-partial59-domain-master-20261026','master_search':'h5-partial59-domain-master-search-20261026','implication':'h5-partial59-master-implication-20261026','generator_failure':'h5-partial59-master-generator-failure-20261026','regions53':'h5-free-bracket27-fixed-regions-20261026','domains53':'h5-free-bracket27-joint-prepared-20261026','capacity53':'h5-free-bracket27-second-sheet-capacity-20261026','early_review':'h5-partial59-source-review-20261026','review':'h5-partial59-final-review-20261026','queue':'h5-focused-checkpoint-queue-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='fec3cd72205e16d3522a181bf4f29680b9e768e5';assert review['main_head']=='679e97e0d7fca4798ba2a1d690c044d72b8f72e2'
    assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
    audits=[('regions59','audit/checks.json'),('domains59','audit/checks.json'),('source59','audit/checks.json'),('search59','search-audit/checks.json'),('conflicts','audit/checks.json'),('conflicts','groups/audit/checks.json'),('conflicts','copy-symmetry/checks.json'),('master','audit/checks.json'),('master_search','selection-audit/checks.json'),('implication','checks.json'),('regions53','audit/checks.json'),('regions53','scope-audit/checks.json'),('domains53','audit/checks.json'),('capacity53','audit/checks.json')]
    assert all(load(base[k]/n)['passed'] for k,n in audits);assert load(base['search59']/'search-audit/checks.json')['terminal_status']=='UNKNOWN' and load(base['master_search']/'selection-audit/checks.json')['terminal_status']=='INFEASIBLE';assert load(base['implication']/'checks.json')['finite59_fixed_source_construction_excluded'];OUT.mkdir()
    for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
    for k,n,dest in [('source59','result.json','seven-part-source-model.json'),('search59','shared-search/solve/result.json','seven-part-source-result.json'),('conflicts','result.json','fresh59-conflict-census.json'),('conflicts','groups/result.json','fresh59-conflict-groups.json'),('master','result.json','necessary-master-model.json'),('master_search','shared-search/solve/result.json','necessary-master-result.json'),('regions53','result.json','broader53-region-result.json'),('regions53','scope-audit/query-containment-checks.json','broader53-region-containment.json'),('domains53','result.json','broader53-domain-result.json'),('capacity53','certificate.json','broader53-capacity-certificate.json'),('generator_failure','failure-record.json','generator-failure.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-679e97e0-snapshot.json'),('queue','queue.json','prior-checkpoint-queue.json')]:shutil.copyfile(base[k]/n,OUT/dest)
    next_action=('Both calls are CLOSED: the full59-fixed seven-mover source remains historically UNKNOWN; the separately audited necessary master is INFEASIBLE and the implication audit excludes that finite source construction. Do not retry either model or transfer its exclusions to the new geometry. Fresh53-fixed/13-mover regions and inward domains are complete and independently audited; moving originals are27,28,29,50,53,54,56,57,58,61,62,64,65. This releases upper-right bracket27 from the old54-fixed source and six additional originals from the focused59 arrangement. All shared fixed transforms,66 original identities, guards and material bounds remain. All10 profiles/20queries/82 mutual cases are used;3599 inward domains cover3601 raw faces with2 retained discards and no uncovered raw area. Ten prior partial anchors remain represented. The second-sheet capacity2 is independently rederived for new cog parts4..12; it is not silently inherited. Next rebuild every new domain-pair raw-original conflict bit (all164 unique query pairs,78 physical pairs,954 modes), audit the complete census and lossless groups, and independently verify necessary-master copy sorting for bracket parts0..2 and cog parts4..12. Derive the fresh original area rules (fixed lower charges3641713590/249662718, total moving590364462 in1000/mm2 units), include the rechecked new capacity2, preserve insert part3 hint and sort only the nine cog hints. Build and independently audit the whole necessary master before one separately declared bounded call; no call is opened yet. A positive domain selection then requires a separate exact-coordinate model with every source clause, followed by full66/90cutout/10026vertex original geometry/native checks, production integration and the full13-job/two-kerf H5 matrix. Never treat a compatible domain tuple as a layout. Main679e97e0 CI40267513191 remains live with4jobs passed at04:25UTC; queuedfec3cd72 and this checkpoint should be pushed normally only after terminal checks and remote ancestry review. H2 original gate remains open;22reserved vectors untouched.')
    write(OUT/'next-step.json',{'action':next_action,'new_region_source':base['regions53'].relative_to(ROOT).as_posix(),'new_domain_source':base['domains53'].relative_to(ROOT).as_posix(),'new_capacity':base['capacity53'].relative_to(ROOT).as_posix(),'mandatory_moving_originals':[27,28,29,50,53,54,56,57,58,61,62,64,65],'fixed_originals':53,'required_originals':66,'new_source_solver_calls':0,'H5_complete':False})
    members={};inputs={}
    for folder in base.values():
        assert folder.is_dir(),folder
        for p in folder.rglob('*'):
            if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
        for p in folder.rglob('plan.json'):
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in load(p).get(field,{}).items():
                    if n in inputs:assert inputs[n]==h,n
                    inputs[n]=h
    for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-focused-partial-obstruction-20261026','h5-conditional-selection-and-partial64-20261026','h5-domain-selection-and-triple-certificate-20261026','h5-expanded-cog-neighborhood-20261026','h5-full-original-joint-20261025','h5-source-area-and-direction-sharing-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    helpers=['make_h5_partial59_geometry_helpers.py','build_h5_partial59_fixed_regions.py','audit_h5_partial59_fixed_regions.py','build_h5_partial59_joint_domains.py','audit_h5_partial59_joint_domains.py','make_h5_partial59_model_helpers.py','prepare_h5_partial59_source_model.py','audit_h5_partial59_source_model.py','make_h5_partial59_search_helpers.py','run_h5_partial59_source_search.py','audit_h5_partial59_source_search.py','make_h5_partial59_review_helper.py','review_h5_partial59_checkpoint.py','make_h5_partial59_conflict_helpers.py','build_h5_partial59_domain_conflicts.py','audit_h5_partial59_domain_conflicts.py','make_h5_partial59_group_helpers.py','prepare_h5_partial59_conflict_groups.py','audit_h5_partial59_conflict_groups.py','audit_h5_partial59_master_copy_symmetry.py','make_h5_partial59_master_helpers.py','repair_h5_partial59_master_generator.py','make_h5_partial59_master_helpers_repaired.py','prepare_h5_partial59_domain_master.py','audit_h5_partial59_domain_master.py','make_h5_partial59_master_runner.py','run_h5_partial59_domain_master.py','audit_h5_partial59_domain_selection.py','audit_h5_partial59_master_implication.py','make_h5_free_bracket27_geometry.py','build_h5_free_bracket27_fixed_regions.py','audit_h5_free_bracket27_fixed_regions.py','build_h5_free_bracket27_joint_domains.py','audit_h5_free_bracket27_joint_domains.py','make_h5_free_bracket27_capacity.py','certify_h5_free_bracket27_second_sheet_capacity.py','audit_h5_free_bracket27_second_sheet_capacity.py','audit_h5_free_bracket27_scope.py','make_h5_partial59_final_review.py','review_h5_partial59_final.py','record_h5_focused_checkpoint_queue.py','pack_h5_evidence_archive.py','ccd1.py'];pending=[ROOT/'output'/n for n in helpers]+[Path(__file__)];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);assert p.is_file(),p;members['helpers/'+p.name]=p;source=p.read_text(encoding='utf-8')
        for name in re.findall(r"['\"]([A-Za-z0-9_.-]+\.py)['\"]",source):
            q=ROOT/'output'/name
            if q.is_file():pending.append(q)
        for node in ast.walk(ast.parse(source)):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members);write(OUT/'checks.json',{'passed':True,'independent_audits_passed':14,'new_closed_solver_calls':2,'full_source59_status_retained':'UNKNOWN','necessary_master59_status':'INFEASIBLE','finite59_source_implication_verified':True,'fresh_raw_original_conflict_bits':2369711,'new53_geometry_domains_and_capacity_audited':True,'new53_solver_calls':0,'all_shared_budgets_honored':True,'full_source59_soft_overrun_seconds':.719084299984388,'generator_failure_preserved':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: seven-part obstruction and broader original source — 2026-10-26

**The finite 59-fixed arrangement is now excluded by an independently audited
necessary model. A broader 53-fixed, 13-mover construction is ready for a fresh
search. No complete target layout or H5 pass is claimed; H2/H5 remain open at 60%.**

## Seven original movers

Release upper-right bracket27 and cog58 from the previous five-mover setup.
All 66 originals remain mandatory: **59 fixed and seven movable** (brackets
27/28/29 and cogs53/54/58/61). Bracket27 is explicitly freed from its earlier
source-orientation restriction to all four quarter turns and both mirror states
allowed by the original job; the old mode IDs remain recorded separately.

Fresh fixed-geometry and reverse-subtraction audits verify **1,261 fixed pairs,
236 stock edges, 77 cutouts and 8,128 hole vertices**. All 100 original cached
orientation/guard obstacles are reverified. All 20 queries finish, with **2,785
raw convex faces / 2,783 inward domains / two retained discards** and no uncovered
raw area or cap. Every prior cog anchor remains represented. The physical
inventory is 21 pairs / 588 query combinations, including 294 empty-query modes
whose selectors are forced false.

Independent whole-model reconstruction and actual solver import verify
**88,210 variables / 121,712 constraints / 24 advisory hints**, with all fourteen
coordinates free and fresh original-area charges. The one full-source call is
**UNKNOWN in 45.719084 solver / 47.245034 shared seconds**. Its 0.719084-second
soft overrun is preserved; the 60-second shared budget passes. Its result remains
UNKNOWN and the call stays closed.

## Fresh necessary incompatibility model resolves this arrangement

Rebuild every conflict from the new domains. All **3,644,823** pairs across 146
unique query combinations are examined; **2,369,711** pairs have their complete
outward-padded difference rectangle strictly inside an inset original collision
region. Independently rebuild all 82 raw obstacles using **9,824 unmerged
triangle-pair hulls**, then recheck every stored bit and every marked whole
rectangle against that independent raw geometry. No old conditional table is used.

Lossless row grouping preserves all **11,983,416 physical conflict uses** in
1,326 groups, using 1,104 auxiliary flags and 232,752 exclusion literals. Exact
bitwise replay verifies grouping and its Boolean equivalence. A separate audit
compares **2,883,845 transpose bits**, finds no asymmetry, and verifies five
within-family choice orders for the necessary master only. No copy ordering is
added to the full coordinate model.

The necessary master deliberately omits coordinates and retains only mandatory
domain selection, original area rules, the certified conflicts and proved copy
ordering. It has **7,937 variables / 2,514 constraints / 16 advisory hints**.
Complete reconstruction and import pass. Its single call returns **INFEASIBLE
in 1.725327 solver / 2.518526 shared seconds**, with no overrun. Readback checks
the exact model, parameters, response and timings.

An additional implication audit maps all **6,763 source-domain selectors** and
checks that any full-source solution would yield a necessary-master solution,
including the permitted family reordering. Thus the negative excludes this
finite 59-fixed construction even though its earlier detailed search timed out.
This is a scoped solver result, not a formal UNSAT certificate or unrestricted
continuous-packing proof. Both solver calls in this checkpoint remain closed.

An initial helper generator caught a stale capacity-input path before writing
any model helper. Its failure is preserved. The separate repaired generator and
subsequent full audits confirm that no inherited capacity entered this master.

## Broader physical construction prepared

Release bracket27 from the earlier broad 54-fixed arrangement. This yields
**53 fixed originals and 13 movers**: three brackets27/28/29, insert50 and nine
cogs53/54/56/57/58/61/62/64/65. Relative to the focused 59-fixed construction,
this also releases originals50/56/57/62/64/65. An explicit scope audit verifies
the exact fixed-set differences, all shared transforms and all **40 physical
free-region containment comparisons**. Maximum uncovered numerical area is
**2.43549e-13 mm²**. Differently triangulated inward domain sets are not asserted
to nest, and no prior exclusion is transferred.

Independent original reconstruction verifies **1,056 fixed pairs, 212 stock
edges, 71 cutouts and 7,006 hole vertices**. All 20 queries complete. The fresh
decomposition contains **3,601 raw faces / 3,599 inward domains / two retained
discards**, with no uncovered raw area or cap, and 12,154 verified inside planes.
All ten source profiles and all 82 mutual cases are used; the complete moving
inventory is **78 physical pairs / 954 same-sheet query combinations**. All ten
previous moving anchors remain represented.

The second-sheet capacity is rederived from the new 32 cog domains. Independent
exact-rational checks of all 228 raw collision boundary segments and two integer
bins establish capacity **two** for the nine current cog IDs, now parts4..12.
This fresh certificate is ready for the next necessary model. No solver has
been called on this broader construction.

Next rebuild its domain-conflict census and group/symmetry proofs, derive fresh
area rules and audit the complete necessary master before one bounded call.
A positive domain selection still needs exact source coordinates, all 66 original
outlines, 90 cutouts and 10,026 hole vertices, native/material validation,
production integration and the full 13-job/two-kerf H5 matrix.

## Repository and gate state

At {review['utc']}, main **679e97e0** has four checks passed and both platform
checks still live in [CI40267513191](https://github.com/skulitom/Nestbolt/actions/runs/40267513191).
The prior checkpoint **fec3cd72** is committed and queued. Preserve the live run
before a normal push. Upstream heads/releases and production/README hashes are
unchanged. No new release is qualified. H2 retains the original gate and all
22 reserved vectors remain unevaluated.

Evidence: [scope implication]({NAME}/implication-checks.json),
[new broader scope]({NAME}/regions53-scope-audit-checks.json),
[capacity]({NAME}/broader53-capacity-certificate.json), [checks]({NAME}/checks.json),
[next step]({NAME}/next-step.json), [raw manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}** aliases
are size/SHA-256/CRC verified across **{archive['archive_parts']}** archive parts.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 seven-part obstruction and broader source, 2026-10-26:** [the evidence]({link})
retains the full 59-fixed/seven-mover call as UNKNOWN (47.245034 shared seconds,
0.719084-second solver soft overrun). A new independently reconstructed census
checks all 3,644,823 domain pairs and certifies 2,369,711 raw-original conflicts.
Lossless grouping and verified family ordering yield a necessary master, which
is INFEASIBLE in 2.518526 shared seconds. The complete implication audit excludes
that finite source arrangement; it does not claim unrestricted impossibility.
Both calls stay closed. A distinct broader construction now fixes 53 originals
and moves 13, including all nine previously moving cogs and the insert. Its
geometry, 3,599 inward domains, 78-pair/954-mode inventory, physical-region
broadening and freshly derived second-sheet capacity pass independent checks.
No broader-source solver call is opened yet. Next rebuild its conflict tables
and necessary master; no old conditional exclusions transfer. Main679e97e0 has
four checks passed and two live; fec3cd72 is queued. H2/H5 remain open at 60%,
with production, READMEs, releases and all 22 reserved vectors unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
