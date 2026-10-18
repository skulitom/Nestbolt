from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess,sys,zipfile
import numpy,scipy,shapely
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h5-pattern-construction-20261018'
PHASES=['h5-pattern-construction-20261018','h5-mixed-pattern-catalog-20261018',
    'h5-mixed-pattern-placement-20261018','h5-radial-angle-diagnosis-20261018',
    'h5-pattern-audit-20261018','h5-angle-pattern-placement-20261018']
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest


def write(p,value):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n')


def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)


def main():
    OUT.mkdir();sources={name:ROOT/'output'/name for name in PHASES}
    simple=load(sources[PHASES[0]]/'results.json');mixed=load(sources[PHASES[1]]/'results.json')
    placed=load(sources[PHASES[2]]/'results.json');radial=load(sources[PHASES[3]]/'results.json')
    audit=load(sources[PHASES[4]]/'checks.json');angle=load(sources[PHASES[5]]/'results.json')
    more=load(sources[PHASES[5]]/'independent-checks.json')
    assert all(d['complete'] for d in [simple,mixed,placed,radial,angle])
    assert audit['all_checks_passed'] and more['all_checks_passed']
    assert all(c['attempts']==0 and not c['constructed_complete'] for c in simple['cases'])
    assert sum(c['area_possible'] for c in mixed['cases'])==1
    assert sum(c['attempts'] for c in placed['cases'])==300 and not any(c['complete_layout_found'] for c in placed['cases'])
    assert sum(c['area_possible'] for c in angle['cases'])==2
    assert sum(c['attempts'] for c in angle['cases'])==648 and not any(c['complete_layout_found'] for c in angle['cases'])
    assert audit['unique_component_CLI_checks']==446 and audit['partial_placement_attempts']==300 and more['partial_placement_attempts']==648
    assert source_digest()=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    originals=load(ROOT/'benchmarks/results/h5-source-frontier-pilot-20261018/results.json')
    inputs=[]
    for row in originals['records']:
        if row['arm']!='candidate' or row['seed']!=0 or not row['job'].startswith('m-mechanical'):continue
        path=ROOT/'benchmarks/results/h5-source-frontier-pilot-20261018'/row['archive']
        assert digest(path)==row['archive_sha256'];inputs.append({'archive':row['archive'],'sha256':digest(path)})
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,folder in sources.items():
            for p in sorted(folder.rglob('*')):
                if p.is_file():
                    relative=name+'/'+p.relative_to(folder).as_posix();z.write(p,relative)
                    manifest.append({'path':relative,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={r['path'] for r in manifest}
        for r in manifest:assert sha256(z.read(r['path'])).hexdigest()==r['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    compound=[]
    for r in mixed['cases']:
        cat=load(sources[PHASES[1]]/r['case']/'patterns.json');p=cat['mix-2-0-1-0']
        compound.append({'case':r['case'],'width_mm':p['width'],'height_mm':p['height'],
            'filled_outer_area_mm2':p['area'],'rectangle_fill_fraction':p['area']/(p['width']*p['height'])})
    table=[]
    for s,m,a,rotation in zip(simple['cases'],mixed['cases'],angle['cases'],radial['cases']):
        assert s['case']==m['case']==a['case']==rotation['case']
        table.append({'case':s['case'],'simple_pattern_area_possible':False,'mixed_catalog_area_possible':m['area_possible'],
            'with_free_angle_pairs_area_possible':a['area_possible'],'final_padded_area_mm2':a['padded_area'],
            'available_padded_area_mm2':a['available_area'],'final_rectangle_attempts':a['attempts'],
            'best_remaining_filled_area_mm2':a['best_unplaced_filled_area_mm2'],
            'free_angle_pair_box_reduction_percent':100*rotation['relative_rectangle_reduction'],'complete_layout_found':False})
    followup=('The mixed-cluster contact construction supplies valid compact components, including two brackets and one insert, '
        'but no complete target layout is constructed. Do not integrate a runtime candidate or repeat a matched pilot on component results. '
        'The finite catalog minimum rules out only those conservative rectangle allocations for the panel jobs; it does not prove '
        'the original polygon problem infeasible. Next test whole-outline placement of the verified components, with joint sheet '
        'assignment and interleaving of their free exterior space, while preserving the original stock, quantities, rotations, '
        'kerf and reserved holes. Keep the quarter-turn failures, free-angle refinement and all incomplete layouts. '
        'A complete independently validated whole-job witness is required before bounded runtime work; then unchanged budgets, '
        'four-step repair cap, prior qualifications and a new matched pilot still apply.')
    checks={'verified_utc':datetime.now(timezone.utc).isoformat(),'all_checks_passed':True,'cases':table,'compact_components':compound,
        'public_component_CLI_checks':446,'component_references':audit['pattern_references'],
        'component_filled_outer_pairs':audit['component_pairs'],'partial_placement_attempts':948,
        'partial_filled_outer_pairs':audit['partial_placement_pairs']+more['filled_outer_pairs'],
        'component_stock_may_be_enlarged':True,'component_quantities_are_only_pattern_members':True,
        'component_checks_do_not_prove_original_stock_or_whole_job_feasibility':True,
        'whole_job_complete_layouts':0,'absolute_clearance_tolerance_mm':1e-7,
        'new_Nestbolt_searches':0,'offline_geometry_and_integer_optimization_performed':True,
        'production_unchanged':True,'production_digest':source_digest(),'original_sources':inputs,
        'raw_members':len(manifest),'raw_archive_sha256':digest(archive),
        'environment':{'numpy':numpy.__version__,'scipy':scipy.__version__,'shapely':shapely.__version__,'GEOS':shapely.geos_version_string},
        'H5_complete':False,'completion_percent':60,'followup':followup}
    write(OUT/'checks.json',checks)
    write(OUT/'interpretation.json',{'followup':followup,'scope':'Four original seed-0 development jobs only. Deterministic restricted offline constructions, finite free-angle sampling and finite pattern catalogs; no benchmark quality/speed evidence and no global impossibility claim. Counts of incomplete attempts are descriptive, not independent statistical trials.',
        'no_runtime_candidate_integrated':True,'whole_job_witness_missing':True,'H5_complete':False})
    for name in ['seal_h5_pattern_constructions.py','audit_h5_angle_placement.py']:
        shutil.copyfile(ROOT/'output'/name,OUT/name)
    lines='\n'.join(f"| {r['case'].replace('m-mechanical-','').replace('-s0-candidate','')} | {r['final_padded_area_mm2']:,.3f} | {r['available_padded_area_mm2']:,.3f} | {'yes' if r['with_free_angle_pairs_area_possible'] else 'no'} | {r['final_rectangle_attempts']} |" for r in table)
    doc=f'''# Mixed-part construction diagnosis — 2026-10-18

The [saved-gap diagnosis](h5-saved-gap-diagnosis-20261018.md) found only small local gains.
This follow-up uses the same four saved seed-0 mechanical jobs to construct groups
of several parts. It runs offline geometry and integer optimization on CCD1;
**no Nestbolt search, timing comparison, original pilot or gate is rerun**.

The simple catalog combines corner/rectangle pairs, corner pairs and staggered
round-part grids. All four inventories exceed their usable target rectangle area,
so no placement is attempted. The retained mixed catalog adds groups of two to
four parts and contact points where enclosing-box extrema change owner. This
matters: checking only forbidden-region vertices missed compact arrangements.
Two brackets and one insert fill **97.31%** of their 310.4022 × 330.4022 mm box in
the large-plate 0.2 mm case. These are component geometry results only.

An integer coverage model chooses the smallest padded rectangle total within each
finite catalog. It preserves all original quantities. Only the large-plate 1.5 mm
case initially passes that necessary area check; 300 attempted column-based
placements leave parts unplaced. A separate 15-degree free-angle check reduces
round-pair boxes by **0.7075–1.9875%**. Adding those verified pairs admits both
large-plate inventories to the area check. The following additional placement
attempts include both fixed large-rectangle columns and unpinned rectangles:

| Saved case | Selected padded area (mm²) | Available padded area (mm²) | Area check | Additional attempts |
| --- | ---: | ---: | :---: | ---: |
{lines}

**No complete target layout is found.** Every one of the **948** attempted partial
layouts retains an explicit missing-parts list. The best final large-plate attempts
still leave 217,800.000 mm² / 446,862.719 mm² of filled part area unplaced. The panel
jobs fail even the finite catalog area check. These are restrictions of this
construction, not global infeasibility proofs.

The frozen public CLI validates **446 distinct component layouts**. Their component
quantities contain only pattern members, and the component stock is enlarged when
needed to test a large pattern. Those checks must not be cited as full-job or
original-stock validation. A separate vertex-transform audit checks **3,668**
component pairs and **526,094** pairs across all 948 partial placements. Quantities
including missing copies, allowed rotations/mirrors, original margins, target sheet
height and reserved holes all verify at the unchanged 1e-7 mm clearance tolerance.
All {len(manifest)} raw members, CRCs and byte hashes verify; the original pilot and
production digest are unchanged.

[Checks](h5-pattern-construction-20261018/checks.json),
[raw plans, catalogs, partial layouts, failures and CLI checks](h5-pattern-construction-20261018/raw.zip),
[manifest](h5-pattern-construction-20261018/raw-manifest.json),
[interpretation](h5-pattern-construction-20261018/interpretation.json).

{followup}

H2/H5 remain open at **60%**. This does not create a new qualified release.
The published preview and all three README descriptions remain unchanged and accurate.
'''
    # Derive the displayed dimensions from the actual pattern; do not retain an
    # assumed rounding if the constructive coordinates differ.
    first=compound[0]
    doc=doc.replace('97.31%',f"{first['rectangle_fill_fraction']*100:.2f}%")
    doc=doc.replace('310.4022 × 330.4022',f"{first['width_mm']:.4f} × {first['height_mm']:.4f}")
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 mixed-pattern diagnosis, 2026-10-18:** [verified component constructions](../benchmarks/results/h5-pattern-construction-20261018.md)
find compact two-bracket/one-insert groups and smaller free-angle round-part pairs.
All 446 component CLI checks and independent checks of 948 incomplete placement
attempts pass their stated scope. The component checks use subset quantities and
may enlarge stock; they do not validate a whole original job. Both large-plate
cases pass the refined finite-catalog area check, but no complete target placement
is found; the panel catalogs still exceed available area. Keep all failures and
test actual-outline placement and joint assignment before any runtime proposal.
No global infeasibility, quality or speed claim follows. Production, budgets,
repair cap, material limits and the preview remain unchanged; completion is 60%.
'''
    prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==prior
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 saved-gap diagnosis, 2026-10-18:**'
    assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-pattern-construction-20261018/** -text -whitespace\n')
    print(json.dumps({k:checks[k] for k in ['all_checks_passed','public_component_CLI_checks','partial_placement_attempts','partial_filled_outer_pairs','raw_members']}),flush=True)


if __name__=='__main__':main()
