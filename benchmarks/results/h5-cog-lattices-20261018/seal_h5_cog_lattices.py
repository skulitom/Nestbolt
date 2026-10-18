from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,subprocess,zipfile,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
OUT=ROOT/'benchmarks/results/h5-cog-lattices-20261018';RUN=ROOT/'output/h5-cog-lattices-20261018';BACK=ROOT/'output/h5-cog-lattice-backfill-20261018';CP=ROOT/'output/h5-lattice-rectangle-cpsat-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
def main():
    OUT.mkdir();assert source_digest()=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    gen=load(RUN/'generation.json');result=load(RUN/'result.json');audit=load(RUN/'audit/checks.json');back=load(BACK/'results.json');ba=load(BACK/'audit/checks.json');cp=load(CP/'result.json');ca=load(CP/'model-audit.json')
    assert not result['complete'] and not back['full_witness'] and cp['status']=='UNKNOWN' and not cp['feasible'] and cp['model_sha256']==ca['model_sha256']
    assert gen['variant_count']==162 and gen['pair_checks']==45360 and result['attempts']==504000 and not result['expired'] and not back['expired'] and ba['filled_outer_pairs']==10915
    for local,saved in [('construct_h5_cog_lattices.py',RUN/'construct.py'),('backfill_h5_cog_lattices.py',BACK/'backfill.py'),('solve_h5_lattice_rectangles.py',CP/'solve.py')]:assert digest(ROOT/'output'/local)==digest(saved)
    ci=json.loads(subprocess.check_output(['gh','run','view','39143540906','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));write(OUT/'main-ci-67e77b1.json',ci)
    next_step=('Coherent rectangular checkerboards are valid but have not produced a full target witness. '
        'Do not rerun these unchanged searches or raise their time limits. The best previous partial still '
        'has 63/66 parts, missing three cogs; these new partials do not improve it. Next test ragged '
        'staggered cog rows with alternating row lengths, especially 5/4/5 (14 cogs) plus one on the '
        'other sheet, and 5/4/4 (13) plus two. This differs from the earlier uniform staggered grid '
        'whose five-cog shifted middle row overhangs the usable width. Predeclare the finite phases, '
        'row offsets, decomposition and time limits. Derive horizontal same-row pitch and vertical '
        'cross-row pitch from actual Minkowski contacts, check every original pair, then fit all '
        'frames, brackets and inserts without fixing frame columns. Only an original 66-copy layout '
        'passing frozen CLI and filled-outer target checks is a witness. If new geometry supplies '
        'no useful whole-job arrangement, inspect nonrectangular contact structure rather than '
        'repeating identical CP-SAT seeds. Native-margin compatibility, production-budget qualification, '
        'four-step repair cap and full H5 matrix remain separate requirements before integration.')
    review={'next_investigation':next_step,'production_digest':source_digest(),'runtime_changed':False,'native_packing_calls':0,'quality_runs':0,'full_target_witnesses':0,'previous_63_part_partial_not_improved':True,'CP_SAT_UNKNOWN_is_not_infeasibility':True,'new_cog_component_minimum_distance_mm':audit['minimum_component_distance_mm'],'reused_mixed_patterns_minimum_distance_mm':min(r['minimum_distance_mm'] for r in ba['cases']),'native_clearance_not_qualified':True,'readmes_unchanged':{n:digest(ROOT/n) for n in ['README.md','README.ja.md','README.zh-CN.md']},'H5_complete':False,'completion_percent':60}
    write(OUT/'source-review.json',review);shutil.copyfile(RUN/'overview.png',OUT/'overview.png')
    members={}
    for root in [RUN,BACK,CP]:
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for name in ['construct_h5_cog_lattices.py','audit_h5_cog_lattices.py','backfill_h5_cog_lattices.py','audit_h5_lattice_backfill.py','solve_h5_lattice_rectangles.py','audit_h5_lattice_rectangle_model.py','plot_h5_cog_lattices.py','construct_h5_pattern_layouts.py','construct_h5_outline_beam.py','diagnose_h5_concave_gaps.py']:
        members['helpers/'+name]=ROOT/'output'/name
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest});write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'generation':gen,'rectangle_construction':result,'geometry_audit':audit,'backfill':back,'backfill_audit':ba,'rectangle_CP_SAT':cp,'rectangle_model_audit':ca,'archive_members':len(manifest),'archive_sha256':digest(archive),'production_digest':source_digest(),'H5_complete':False,'completion_percent':60});shutil.copyfile(__file__,OUT/'seal_h5_cog_lattices.py')
    doc=f'''# H5: coordinated cog groups and free frame placement — 2026-10-18

**No complete target layout is found.** All newly constructed cog components
validate, but neither fixed-column rectangle packing, outline-gap continuation,
nor a bounded free-placement rectangle model returns all 66 original parts.
The earlier 63-part partial, missing three cogs, remains better than these new
partials. H5 stays open and total completion remains **60%**.

The [previous contact-pool study](h5-contact-selection-20261018.md) left exact
inventory selection unresolved. This investigation constructs coordinated cog
positions directly instead of asking a selector to discover an arrangement from
unrelated poses. It uses the same saved large-plates development job at 0.2 mm
kerf, original 1,500 × 3,000 mm stock, margins, rotations and full inventory.
The original conditional material target remains **4,988,890.353495 mm²**, with
last-sheet used height no more than **325.92690233 mm**. All holes remain reserved.

![Verified cog group and incomplete layouts](h5-cog-lattices-20261018/overview.png)

## Geometry construction

The recorded finite catalogue has base angles 0°, 4.5° and 9°; relative phases
0°, 3°, 6°, 9°, 12° and 15°; and alternating x/y offsets −6, 0 and 6 mm.
For each of the **162 variants**, pitches come from horizontal and vertical
intersections of the actual filled-outer Minkowski obstacle. Rotations use the
original cog's centroid, approximately (139.723742, 139.723742) mm. No rotational
symmetry or circular surrogate is assumed. Conservative 0.22 mm construction
clearance and a positive pitch increment leave the 0.2 mm acceptance rule intact.

Seven components per variant contain 15, 12, 10, 9, 6, 5 or 3 cogs. All **1,134
components** pass **45,360** independent pair checks, with minimum distance
**0.22012005 mm**. The independent audit reconstructs every unrounded transform
from original vertices and checks all bounds and component pairs. Catalogue
generation takes **{gen['seconds']:.6f} seconds**, below its 120-second ceiling.
The smallest full 15-cog rectangle is **1,357.901348 × 818.933402 mm**.

## Whole-job construction and gap continuation

The twelve best full-group variants supply five complete cog decompositions:
15; 10+5; 9+6; 12+3; and 5+5+5. Each is combined with all 25 retained frame-column
configurations, 28 original bracket/insert pattern inventories, four sort orders
and three rectangle-fit rules. All **504,000 attempts** finish in
**{result['seconds']:.6f} seconds**, without the 120-second limit firing.
Every attempted placed-plus-unplaced inventory independently totals the original
66 parts. Pair validation of every rejected attempt is not claimed.

The greatest filled-area rectangle result has **52/66 parts**, including all cogs,
frames and brackets, but lacks fourteen inserts. It uses three separate five-cog
rows, not the full 15-cog rectangle shown on the left of the figure. Its original
CLI check rejects only quantity; all 1,050 filled-outer pairs and target bounds pass.

A separately recorded continuation chooses eight partials by frame configuration
and per-sheet cog count, ranking each group's best filled-area result. Actual
outline gaps allow **15 additions total** across those eight layouts in
**{back['seconds']:.6f} seconds**. None becomes complete. The largest count is
60/66, missing two brackets and four cogs. All **144** proposed additions are
independently checked against their accepted prefixes. All **10,915** final
same-sheet pairs pass, every initial placement is byte-for-byte preserved, and
the original CLI rejects each result only for missing quantities. Conservative
empty-region observations do not prove arbitrary placement impossible.

The new cog components have extra construction space; reused mixed bracket
patterns retain minimum distance about **0.2011 mm**. This is valid original
geometry but is **not native-margin qualification**. No native packing call is
made or implied by these checks.

## Freely placed rectangle groups

A distinct CP-SAT model removes the fixed frame-column restriction. All eighteen
frames, six verified two-bracket/one-insert groups, fifteen remaining inserts and
one of the five complete cog decompositions may translate on a 0.001 mm grid,
choose sheets and rotate by a quarter-turn when they fit. Padded sizes round
outward and target capacities round inward. Each alternative requires exactly
the original inventory, with no partial objective. Only interchangeable identical
copies are ordered to remove symmetry.

The exported model has **471 variables, 517 constraints and 139 optional
rectangles**. A separate protobuf parser verifies every variable domain, every
interval, all per-sheet overlap constraints, all five exact inventories, rounding,
and absence of hidden constraints or objectives. OR-Tools 9.15.6755 uses the
already verified isolated standard CPython runtime, seed 0, eight offline CCD1
workers and a 120-second allowance. It returns **UNKNOWN** after
**{cp['seconds']:.6f} seconds**, with 1,532,756 branches and 17,023 conflicts,
and no complete selection. This is not an infeasibility proof or a runtime
comparison. The unchanged model is not rerun.

[Checks](h5-cog-lattices-20261018/checks.json),
[all inputs, scripts, components, attempts, models, logs and audits](h5-cog-lattices-20261018/raw.zip),
[byte manifest](h5-cog-lattices-20261018/raw-manifest.json),
[next investigation](h5-cog-lattices-20261018/source-review.json).
All {len(manifest)} archived members, CRCs and hashes verify; the figure has been
visually inspected. Existing failed attempts and all original inputs remain.

{next_step}

The [main 67e77b1 check snapshot](h5-cog-lattices-20261018/main-ci-67e77b1.json)
records its actual status at sealing; unfinished jobs are not counted as passes.
Production source, original gate limits, preview assets and the three accurate
READMEs are unchanged. No native quality run, production integration, new release
qualification or gate credit is claimed. H2 and H5 remain open.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 coherent cog groups, 2026-10-18:** [162 alternating lattices](../benchmarks/results/h5-cog-lattices-20261018.md)
produce 1,134 verified components and pass 45,360 independent pair checks.
All 504,000 fixed-column whole-job constructions finish without a full layout;
the greatest filled-area result is 52/66, missing fourteen inserts. Eight distinct
outline-gap continuations add fifteen parts total but remain partial; all 144
proposed additions and 10,915 final pairs independently check, with original CLI
quantity failures only. A separate exact-inventory rectangle model frees all
frame positions and chooses one of five full cog decompositions. Independent
parsing verifies all 471 variables and 517 constraints. The one 120-second search
ends UNKNOWN, not infeasible, without a full selection. The earlier 63/66 partial
remains better. Next investigate ragged staggered cog rows with actual contact
pitches; preserve all quantities, stock targets and full-layout validation.
No native packing, quality run, production, gate, release or README change;
H2/H5 remain open at 60%.
'''
    before=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==before;append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 expanded contact selection, 2026-10-18:**';assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-cog-lattices-20261018/** -text -whitespace\n');print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'CI_status':ci['status'],'CI_conclusion':ci['conclusion']}))
if __name__=='__main__':main()
