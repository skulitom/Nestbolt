from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,subprocess,zipfile,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
OUT=ROOT/'benchmarks/results/h5-outline-contact-direction-20261018';PROP=ROOT/'output/h5-ragged-propagation-cpsat-20261018';SEARCH=[ROOT/'output'/n for n in ['h5-ragged-outline-beam-20261018','h5-ragged-outline-cached-20261018','h5-ragged-outline-adaptive-20261018']];DIRECT=ROOT/'output/h5-contact-direction-20261018';SCAN=ROOT/'output/h5-minimum-contact-grids-20261018';load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
def main():
    OUT.mkdir();assert source_digest()=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88';prop=load(PROP/'result.json');pa=load(PROP/'model-audit.json');assert prop['status']=='UNKNOWN' and pa['model_bytes_exact'];results=[load(p/'results.json') for p in SEARCH];audits=[load(SEARCH[0]/'audit-recovered/checks.json'),*[load(p/'audit/checks.json') for p in SEARCH[1:]]];cache=[load(p/'cache-audit.json') for p in SEARCH[1:]];contact=load(SCAN/'audit.json');scan=load(SCAN/'result.json')
    assert all(not r['full_witness'] for r in results) and all(not a['complete_witness'] for a in audits);assert contact['scanned_pair_checks']==13860 and contact['scanned_minimum_distance_mm']>.225 and scan['valid_components']==324 and not scan['expired'];assert all(a['maximum_hausdorff_difference_mm']==0 and a['maximum_symmetric_difference_area_mm2']==0 for a in cache)
    assert load(SEARCH[0]/'audit-recovered/recipe-0-command.json')['exit_code'] is None
    ci=json.loads(subprocess.check_output(['gh','run','view','39146239813','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));write(OUT/'main-ci-f825cab.json',ci)
    next_step=('The tighter original-cog geometry changes the next investigation. Use the verified '
        'phase-0 contact-aligned grid from output/h5-minimum-contact-grids-20261018: pitch '
        '258.79424409546664 mm, common angle -2.2428996024478143 radians and actual minimum '
        'distance 0.2251234420919754 mm. Its 15-cog rectangle is 1315.1261869914774 by '
        '797.5376988005441 mm, 5.680423591715256% smaller than the earlier sampled-angle group. '
        'First construct finite uniform staggered rows from this contact-aligned orientation, '
        'including five cogs in every row: the earlier unaligned stagger overhung stock width, '
        'but the new smaller horizontal pitch may change that. Predeclare row-offset fractions '
        'and derive vertical pitches from actual same-orientation Minkowski intersections; '
        'verify every original pair and original stock width. Then attempt the complete original '
        '66-part job with the new square/staggered components and all three retained aspect '
        'variants of the two-bracket/one-insert pattern, allowing different variants among the '
        'six bracket groups rather than forcing the smallest-area one everywhere. Preserve '
        'stock, margins, quantity, allowed rotations and the original material target. Do not '
        'repeat unchanged propagation flags or fixed/adaptive beams: the broad adaptive '
        'enumeration timed out at only 19-22 of 33-44 component depths and was not an improvement. '
        'The primitive-translation cache is available and audited for future actual-outline '
        'construction. Component area savings are not a whole-job quality claim. Only all 66 '
        'copies passing frozen original CLI and independent filled-outer target checks form a '
        'witness. Native-margin validation, production budgets, the four-step repair cap and '
        'full H5 matrix remain required before integration.')
    previous=load(ROOT/'benchmarks/results/h5-ragged-pockets-20261018/source-review.json');readmes={n:digest(ROOT/n) for n in previous['readmes_unchanged']};assert readmes==previous['readmes_unchanged']
    write(OUT/'source-review.json',{'next_investigation':next_step,'production_digest':source_digest(),'runtime_changed':False,'native_packing_calls':0,'quality_runs':0,'public_CLI_calls':18,'full_target_witnesses':0,'previous_63_part_partial_not_improved':True,'failed_audit_and_assumed_exit_metadata_preserved':True,'first_original_CLI_return_code_unknown':True,'new_component_bounding_area_reduction_percent':contact['rectangle_area_reduction_percent'],'not_whole_job_material_savings':True,'native_margin_qualification_not_claimed':True,'readmes_unchanged':readmes,'H5_complete':False,'completion_percent':60});shutil.copyfile(SCAN/'comparison.png',OUT/'comparison.png')
    members={}
    for root in [PROP,*SEARCH,DIRECT,SCAN]:
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    helpers=['prepare_h5_propagation_model.py','solve_h5_ragged_propagation.py','audit_h5_propagation_model.py','construct_h5_ragged_outlines.py','audit_h5_ragged_outlines.py','recover_h5_outline_audit.py','audit_h5_ragged_outlines_recovered.py','prepare_h5_cached_outlines.py','construct_h5_cached_outlines.py','audit_h5_cached_outlines.py','audit_h5_primitive_cache.py','construct_h5_adaptive_outlines.py','prepare_h5_adaptive_audits.py','audit_h5_adaptive_outlines.py','audit_h5_adaptive_cache.py','diagnose_h5_contact_direction.py','construct_h5_minimum_contact_grids.py','audit_h5_contact_grids.py','plot_h5_contact_direction.py','construct_h5_pattern_layouts.py','construct_h5_outline_beam.py','diagnose_h5_concave_gaps.py','audit_h5_cog_lattices.py','solve_h5_ragged_normal.py']
    for name in helpers:members['helpers/'+name]=ROOT/'output'/name
    for p in [ROOT/'output/h5-ragged-pockets-20261018/components.json',ROOT/'output/h5-ragged-pockets-20261018/selected-recipes.json',ROOT/'output/h5-cog-lattices-20261018/all-patterns.json',ROOT/'output/h5-cog-lattices-20261018/generation.json',ROOT/'output/h5-cog-lattices-20261018/patterns.json']:
        members['source-inputs/'+p.relative_to(ROOT/'output').as_posix()]=p
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest});write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'propagation_result':prop,'propagation_audit':pa,'outline_search_results':results,'outline_audits':audits,'cache_audits':cache,'contact_direction_audit':contact,'contact_scan':scan,'archive_members':len(manifest),'archive_sha256':digest(archive),'production_digest':source_digest(),'H5_complete':False,'completion_percent':60});shutil.copyfile(__file__,OUT/'seal_h5_outline_contact_direction.py')
    table='\n'.join(f"| {name} | {sum(len(r['runs']) for r in result['recipes'])} | {sum(r['candidates'] for r in result['recipes']):,} | {sum(r['expired'] for r in result['recipes'])}/6 | {result['best']['placed_count']}/66 | {result['best']['filled_area']:.3f} |" for name,result in zip(['Original compound exclusions','Cached primitive exclusions','Adaptive remaining-inventory ordering'],results))
    doc=f'''# H5: actual-outline search, reusable exclusions and contact direction — 2026-10-18

**A better cog component is verified; no complete target layout is established.**
Choosing the global rotation from an actual contact boundary yields a 15-cog
rectangle **5.6804% smaller** than the earlier sampled-angle component, with
all original gaps above 0.225 mm. This is a component bounding-area result,
not whole-job material savings. The earlier 63/66 partial remains the best
retained whole-job partial. H2/H5 remain open at **60%**.

![Old and contact-aligned original cog groups](h5-outline-contact-direction-20261018/comparison.png)

## Controlled propagation check

Following the [ragged-pocket study](h5-ragged-pockets-20261018.md), one controlled
run enables the installed cumulative, energetic and area-energetic NoOverlap2D
flags. Independent parsing confirms that **only those three flags** change.
The saved normal-coordinate model is byte-identical, as are the original
inputs, integer domains, inventory and material target. Seed 0, eight offline
CCD1 workers and the 120-second limit remain fixed. The result is **UNKNOWN**
after **{prop['seconds']:.6f} seconds**, returning no complete selection.
The unsuccessful result is retained; no parameter sweep follows.

## Actual outlines and repeated geometry work

The next construction uses actual unions of filled-outer exclusions for rigid
groups and remaining parts. All **six** original-inventory recipes are included,
including the two previously excluded by their enclosing rectangles' area.
Each has a separately declared twenty-second search ceiling. The original
construction tries frame-first, mixed-first and cog-first family orders, with
eight retained states, three contacts per orientation and diversity in leading
group orientation and second-sheet allocation. Source cog rotations are sampled
only for this finite diagnostic; original free-rotation permission is unchanged.

The first recipe consumes its allowance after only two component placements.
Inspection finds that translated repetitions of the same cog recompute primitive
geometry. A fresh implementation caches each exact unrounded rotation/reflection
pair at zero translation, translates its obstacle by the difference of member
translations, then unions the compound terms. Every accepted candidate still
passes direct original-outline distance and stock checks. No shape, tolerance,
recipe, fixed order, contact count or per-recipe ceiling changes.

The geometric identity is `(A+a)−(B+b)=(A−B)+(a−b)`. All **336** cached primitive
obstacles recompute identically, with zero Hausdorff and symmetric-difference
area error; **7,369** compound translation terms are checked against their
original members. The union outputs are not separately serialized; their exact
term provenance and every retained layout are preserved. All eighteen fixed-order
searches now finish within their individual allowances. This is a local diagnostic
observation, not a native-speed or quality claim.

A separately recorded adaptive construction preloads the audited primitives,
branches over every remaining component kind, and retains sixteen states with
orientation and last-kind diversity. The same twenty-second ceiling applies to
each recipe. Its broad enumeration expires at depths **19–22 of 33–44**, returning
less filled area. Its **391** final primitive obstacles and **8,341** translated
terms also audit exactly. This failed direction is retained, not presented as
an improvement or repeated with a longer allowance.

| Construction | Orders/inventory roots attempted | Candidate events | Recipes expired | Greatest filled-area partial | Filled area, mm² |
| --- | ---: | ---: | ---: | ---: | ---: |
{table}

The original construction records soft-cap overruns explicitly, including
**21.193015 seconds** for its first recipe; it is not rounded down to twenty.
Across the three constructions, independent audits reconstruct all retained
states from their candidate parents, original component transforms and actual
inventory consumption. Retained-layout pair checks total **30,621**; all original
orientations, stock bounds and the unchanged material target pass. The frozen
public CLI rejects every best partial for missing quantities, with an additional
empty-second-sheet failure in the short original first recipe. Rejected candidate
geometry is not claimed to have been exhaustively independently audited.

The first audit incorrectly expected quantity-only errors and stopped at that
legitimate empty-sheet error. Its source, failure and original CLI output remain.
A fresh audit reuses that output under exact hashes and validates the remaining
partials once. An assumed return-code field in the first recovery record is
preserved and superseded by **null/unknown**: the original failed auditor did not
save the CLI return code. No layout or validator result is altered or accepted.

## Contact direction explains a tighter component

The earlier checkerboard varied offsets between alternating parity classes and
sampled global angles. A saved tight two-cog contact has a small nonzero vertical
centre offset. Aligning that **directed** contact to the grid axis rotates both
cogs together and avoids imposing the worse opposite-slope contact.

A predeclared probe checks exactly three saved pairs, with a fixed positive
centre-distance increment. All three 15-cog patches pass their **315** original
pair checks. Their minimum gap is only about **0.20893 mm**, so this initial
probe is not native-margin qualification.

A second, separately declared construction uses conservative **0.225 mm** spacing
and scans **36 relative phases**, in half-degree steps. It projects the origin
onto every exterior segment of each actual filled-outer Minkowski obstacle,
chooses the closest contact direction, rotates both orientations together, and
derives the pitch from all four axis intersections. No rotational symmetry is
assumed. Nine patch sizes/aspects per phase produce **324 valid components** in
**{scan['seconds']:.6f} seconds**, below its 120-second generation cap.

Independent nearest-boundary queries agree within **5.7×10⁻¹⁴ mm**. Independent
ray intersections in the unrotated obstacles verify the chosen pitches, and
every unrounded member transform is reconstructed. All **13,860** original
component pairs pass, with minimum distance
**{contact['scanned_minimum_distance_mm']:.9f} mm**.

The best finite 15-cog, five-column group uses identical cog orientations at
**−2.242899602448 radians**, with pitch **258.794244095467 mm**. Its rectangle is
**1,315.126187 × 797.537699 mm**, area **1,048,862.712806 mm²**, versus
**1,112,030.771073 mm²** for the earlier sampled-angle group. The original cogs,
quantities and acceptance rules are unchanged. The 5.6804% rectangle-area saving
does not prove that the full job fits, that common-line quality improved, or that
native geometry qualification passes.

[Checks](h5-outline-contact-direction-20261018/checks.json),
[raw searches, geometry, failures, models, scripts and audits](h5-outline-contact-direction-20261018/raw.zip),
[manifest](h5-outline-contact-direction-20261018/raw-manifest.json),
[next investigation](h5-outline-contact-direction-20261018/source-review.json).
All **{len(manifest)}** archive members, CRCs and byte hashes verify. The comparison
figure has been visually inspected.

{next_step}

The [main f825cab check snapshot](h5-outline-contact-direction-20261018/main-ci-f825cab.json)
records its actual status at sealing; pending jobs are not counted as successes.
Production source, original gate limits, preview release assets and all three
accurate READMEs remain unchanged. No native packing, quality run, production
integration or gate credit is claimed. H2/H5 remain open at **60%**.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 contact direction and outline construction, 2026-10-18:** [actual-outline investigations](../benchmarks/results/h5-outline-contact-direction-20261018.md)
retain the unchanged-model propagation timeout and all unsuccessful fixed/adaptive
constructions. Caching exact primitive exclusions lets all eighteen fixed-order
searches finish their original allowances; cached primitives and translation terms
audit exactly. Retained-layout checks cover 30,621 pairs; all best layouts remain
incomplete. The empty-sheet audit failure and corrected unknown return-code
metadata are preserved. A directed-contact probe exposes a better global rotation.
The subsequent declared 36-phase scan gives 324 verified components and 13,860
pair checks at minimum 0.225123442 mm. Its 15-cog rectangle is 5.6804% smaller than
the earlier sampled-angle component; this is not whole-job material savings.
Next use contact-aligned staggered rows and the retained bracket-pattern aspect
choices in a complete original-inventory construction. No native packing, quality
run, runtime integration, release, README change or gate credit; H2/H5 remain 60%.
'''
    before=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==before;append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 ragged cog pockets, 2026-10-18:**';assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n');append(ROOT/'.gitattributes','\nbenchmarks/results/h5-outline-contact-direction-20261018/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'main_CI_status':ci['status'],'main_CI_conclusion':ci['conclusion']}))
if __name__=='__main__':main()
