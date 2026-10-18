from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,subprocess,zipfile,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
OUT=ROOT/'benchmarks/results/h5-ragged-pockets-20261018';RAG=ROOT/'output/h5-ragged-cogs-20261018';POCKET=ROOT/'output/h5-ragged-pockets-20261018';PHASES=[ROOT/'output'/n for n in ['h5-ragged-pocket-cpsat-20261018','h5-ragged-separator-cpsat-20261018','h5-ragged-normal-cpsat-20261018']]
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
def main():
    OUT.mkdir();assert source_digest()=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88';generation=load(RAG/'result.json');filled=load(POCKET/'result.json');geometry=load(POCKET/'audit/checks.json');results=[load(p/'result.json') for p in PHASES];audits=[load(p/'model-audit.json') for p in PHASES];config=load(PHASES[-1]/'parameter-review.json')
    assert all(r['status']=='UNKNOWN' and not r['feasible'] for r in results) and not generation['expired'] and not filled['expired'];assert geometry['staggered_pair_checks']==20034 and geometry['pocket_pair_checks']==6301 and geometry['pocket_candidate_checks']==1197
    assert audits[1]['baseline_model_exact_after_removing_only_proven_symmetries'] and audits[2]['all_other_model_bytes_exact'] and audits[2]['independent_boolean_array_domains_equal']
    for source,saved in [('construct_h5_ragged_cogs.py',RAG/'construct.py'),('fill_h5_ragged_pockets.py',POCKET/'fill.py'),*[(n,p/'solve.py') for n,p in zip(['solve_h5_ragged_pockets.py','solve_h5_ragged_separator.py','solve_h5_ragged_normal.py'],PHASES)]]:assert digest(ROOT/'output'/source)==digest(saved)
    ci=json.loads(subprocess.check_output(['gh','run','view','39143540906','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs']);write(OUT/'main-ci-67e77b1.json',ci)
    next_step=('The ragged components and their fillers are physically valid, and the rectangle models '
        'preserve the original inventory and target, but all three bounded searches returned UNKNOWN. '
        'No full target witness or improvement over the earlier 63/66 partial is established. Do not '
        'repeat unchanged models, seeds or longer limits. Installed OR-Tools 9.15.6755 declares '
        'use_timetabling_in_no_overlap_2d, use_energetic_reasoning_in_no_overlap_2d and '
        'use_area_energetic_reasoning_in_no_overlap_2d false by default. Their installed documentation '
        'describes additional cumulative and area reasoning. Next prepare one controlled propagation '
        'mechanism experiment on the exact saved normal-coordinate model, enabling those three flags '
        'while preserving model bytes, grid, inventories, original material target, seed 0, eight '
        'offline CCD1 workers and 120 seconds. Record parameter differences and preserve all prior '
        'UNKNOWN results; do not treat finite rectangle-model infeasibility as unrestricted outline '
        'infeasibility. If this still supplies no witness, examine the conservative enclosing '
        'rectangles and whether smaller coordinated outline groups can free their unused boundary '
        'space, rather than continuing parameter sweeps. Only a complete 66-copy layout passing the '
        'frozen original CLI and independent filled-outer target checks is a witness. Native margins, '
        'production-budget checks, the four-step repair cap and full H5 matrix remain required before '
        'integration or gate credit.')
    previous=load(ROOT/'benchmarks/results/h5-cog-lattices-20261018/source-review.json');readmes={n:digest(ROOT/n) for n in previous['readmes_unchanged']};assert readmes==previous['readmes_unchanged']
    write(OUT/'source-review.json',{'next_investigation':next_step,'production_digest':source_digest(),'runtime_changed':False,'native_packing_calls':0,'quality_runs':0,'public_CLI_calls':0,'full_target_witnesses':0,'previous_63_part_partial_not_improved':True,'all_UNKNOWN_results_preserved':True,'new_geometry_minimum_distance_mm':geometry['pocket_minimum_distance_mm'],'old_mixed_patterns_native_clearance_still_unqualified':True,'readmes_unchanged':readmes,'all_six_main_67e77b1_checks_pass':True,'H5_complete':False,'completion_percent':60})
    shutil.copyfile(POCKET/'pockets.png',OUT/'pockets.png');members={}
    for root in [RAG,POCKET,*PHASES]:
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    helpers=['construct_h5_ragged_cogs.py','fill_h5_ragged_pockets.py','audit_h5_ragged_geometry.py','prepare_h5_ragged_model.py','solve_h5_ragged_pockets.py','audit_h5_ragged_model.py','prepare_h5_separator_model.py','solve_h5_ragged_separator.py','audit_h5_separator_model.py','prepare_h5_normal_coordinates.py','solve_h5_ragged_normal.py','audit_h5_normal_model.py','inspect_h5_packing_parameters.py','plot_h5_ragged_pockets.py','construct_h5_pattern_layouts.py','construct_h5_outline_beam.py','diagnose_h5_concave_gaps.py','audit_h5_cog_lattices.py','solve_h5_lattice_rectangles.py','audit_h5_lattice_rectangle_model.py']
    for name in helpers:members['helpers/'+name]=ROOT/'output'/name
    for p in [ROOT/'output/h5-cog-lattices-20261018/all-patterns.json',ROOT/'output/h5-cog-lattices-20261018/job.json']:members['source-inputs/'+p.relative_to(ROOT/'output').as_posix()]=p
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest});write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'generation':generation,'geometry_audit':geometry,'pocket_seconds':filled['seconds'],'selected_recipes':filled['selected'],'solver_results':results,'model_audits':audits,'parameter_review':config,'archive_members':len(manifest),'archive_sha256':digest(archive),'production_digest':source_digest(),'H5_complete':False,'completion_percent':60});shutil.copyfile(__file__,OUT/'seal_h5_ragged_pockets.py')
    rows='\n'.join(f"| {name} | {r['seconds']:.6f} | {r['status']} | none |" for name,r in zip(['Original rectangle coordinates','Width-proven separator origin','Normal subset-sum coordinates'],results))
    doc=f'''# H5: staggered cog pockets and exact rectangle-domain reductions — 2026-10-18

**The new components validate, but no complete target layout is found.** Three
bounded rectangle searches end UNKNOWN; none proves infeasibility. The earlier
63/66 partial remains better than these component-only results. H5 is open and
completion remains **60%**. This is offline development diagnosis, not a quality
run, production change or new release qualification.

The [previous checkerboard study](h5-cog-lattices-20261018.md) led to ragged rows
whose short middle row avoids the extra half-pitch overhang of uniform grids.
This uses the same saved large-plates job at 0.2 mm kerf, all original quantities,
allowed rotations and filled outer geometry. The material target stays
**4,988,890.353495 mm²**, and the last-sheet used-height limit stays
**325.92690233 mm**. Frames' holes remain reserved.

![Verified ragged groups with original pocket fillers](h5-ragged-pockets-20261018/pockets.png)

## Ragged rows and real gap filling

The predeclared construction uses three base angles, six row-phase differences
and three offsets from half the horizontal pitch: **54 variants**. Each has row
counts 5/4/5, 5/4/4, 5/4/3, 5/4/2, 5/4/1 or 5/4. Horizontal pitch comes from both
actual same-orientation Minkowski obstacles. Vertical pitch checks every relevant
cross-row displacement and the two-row separation. Construction has positive
0.22 mm clearance; the original acceptance remains 0.2 mm.

All **324 components** pass **20,034** independently reconstructed original-vertex
pair checks, with minimum distance **{geometry['staggered_minimum_distance_mm']:.9f} mm**.
Generation finishes in **{generation['seconds']:.6f} seconds**, below its 120-second
ceiling. The selected 14-cog group measures **1,388.465439 × 765.549235 mm**.
The best finite phase is 4.5° with identical row orientations; no cog symmetry or
circular surrogate is assumed.

Instead of reserving every group's empty rectangular pockets, a separate finite
construction inserts original rectangles and brackets into actual inter-part
gaps. It keeps every cog pose and enclosing rectangle unchanged. Two family
orders and four corner priorities produce **48 filled components** in
**{filled['seconds']:.6f} seconds**, without its 120-second ceiling firing. Each
uses allowed rotations/reflections, three distinct contact candidates per
orientation and a declared twelve-addition cap. Holes inside parts remain closed.

The independent audit checks **1,197** proposed additions against their accepted
prefixes, **6,301** final component pairs and all **237** accepted additions across
the 48 variants. Minimum final distance is **{geometry['pocket_minimum_distance_mm']:.9f} mm**.
Every full-job recipe independently totals the original 66 parts. Examples are
fourteen cogs plus two inserts, thirteen cogs plus four inserts, and twelve cogs
plus eight inserts within unchanged component bounds. The twelve-insert variant
reaches its declared addition cap; it is not asserted to be maximally filled.

The least padded-area recipe for each row family is retained. Two exceed the
available rectangle area and are excluded from this restricted model only.
Four survive: the 14-, 13-, 12- and 9-cog components, their pocket fillers, and
all remaining original cogs, frames, brackets and inserts. Their padded area
test is necessary, not sufficient, for those rectangular recipes; it is not a
global lower bound for arbitrary original outlines.

## Three controlled rectangle models

The first model freely places every rectangle group on the original two target
sheets, including all frame positions. Shared quantities are factored across
the four alternatives; exactly one complete recipe is selected. Padded sizes
round outward and sheet capacities inward on a **0.001 mm** grid. Independent
protobuf parsing verifies all **634 variables**, **707 constraints**, **190
optional rectangles**, exact inventories, all original target bounds and the
two area exclusions. No partial objective or hidden constraints are present.

A second model adds **eight** independently verified symmetry constraints. Each
horizontal ragged group's width plus every coexisting rectangle's smallest
allowed width exceeds stock width. Thus every other rectangle lies entirely
above or below it. Moving the below rectangles upward by the group's padded
height, retaining the above rectangles, and putting the group at (0,0) preserves
nonoverlap and stock bounds. Quarter-turned groups are unchanged. Removing only
these constraints and remapping interval references reproduces the first model
exactly. This is a feasibility-preserving reduction for these rectangle groups.

A third model keeps only normal coordinates: subset sums of allowed rectangle
widths and heights. A feasible arrangement can first compact left at fixed y,
then down at fixed x. Each resulting coordinate follows a positive-size contact
chain to a stock boundary. Such a chain uses coexisting items at most once; all
its sums are included. Identical copies can be relabelled to restore their order,
and the horizontal group already at the origin cannot move farther left/down.
This preserves existence of a feasible rectangle arrangement on the same grid.

Producer integer bitsets and an independent Boolean-array enumeration agree on
**1,277 / 34,911** x/y values for the first sheet and **307 / 7** for the last.
The actual per-variable domains contain **2,706,544** values across **380**
coordinate variables. Restoring only the original interval domains reproduces
the second serialized model exactly. No geometry, inventory, budget or acceptance
threshold changes in either reduction.

Each search uses the verified isolated standard-CPython OR-Tools 9.15.6755 runtime,
seed 0, eight offline CCD1 workers and a 120-second limit. The attempts are serial,
and all logs and unsuccessful results are preserved.

| Mechanism | Actual seconds | Status | Complete selection |
| --- | ---: | --- | --- |
{rows}

The normalized-domain run records 1,442,434 branches, 187,289 conflicts and no
feasible selection. These observations do not establish runtime superiority or
unrestricted geometric impossibility. No original CLI validation is invoked for
an absent full layout. Reused bracket/insert patterns retain their prior roughly
0.2011 mm distance; native-margin compatibility remains unqualified.

[Checks](h5-ragged-pockets-20261018/checks.json),
[all source geometry, attempts, models, parameters, logs and audits](h5-ragged-pockets-20261018/raw.zip),
[manifest](h5-ragged-pockets-20261018/raw-manifest.json),
[next investigation](h5-ragged-pockets-20261018/source-review.json).
All **{len(manifest)}** archived members, CRCs and byte hashes verify. The figure
has been visually inspected. No source designs or runtime binaries are uploaded
to external testing services.

{next_step}

[All six hosted checks on main 67e77b1 pass](h5-ragged-pockets-20261018/main-ci-67e77b1.json),
including Windows, Linux and the browser. The earlier in-progress snapshot is
preserved. Production source, gate limits, release assets and all three accurate
READMEs are unchanged. H2 and H5 remain open at **60%**.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 ragged cog pockets, 2026-10-18:** [54 staggered variants](../benchmarks/results/h5-ragged-pockets-20261018.md)
produce 324 valid groups with 20,034 independently checked pairs. Filling their
actual inter-part pockets produces 48 verified components: 1,197 proposed
additions, 6,301 final pairs and 237 accepted additions across variants. Four
complete original-inventory recipes pass their restricted rectangle-area test;
two area failures remain preserved. Three serial 120-second models test free
rectangle placement, proven full-width separator symmetry, and normal subset-sum
coordinates. Independent parsing verifies exact quantities, targets and every
model difference; independent enumeration verifies all reduced coordinate domains.
All three return UNKNOWN without a full selection. The earlier 63/66 partial is
not improved. Next inspect the documented cumulative/area propagation flags with
one controlled same-model experiment, preserving all limits and failures. All six
main 67e77b1 checks pass. No native packing, quality run, production integration,
gate credit, release or README change; H2/H5 remain open at 60%.
'''
    before=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==before;append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 coherent cog groups, 2026-10-18:**';assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n');append(ROOT/'.gitattributes','\nbenchmarks/results/h5-ragged-pockets-20261018/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'main_all_six_pass':True}))
if __name__=='__main__':main()
