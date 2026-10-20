from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
PREFIX='h5-whole-group-diagnosis-20261020';OUT=ROOT/'benchmarks/results'/PREFIX
DIV=ROOT/'output/h5-lp-guided-diving-20261020'
PROBE=ROOT/'output/h5-highs-basis-probe-20261020'
CENSUS=ROOT/'output/h5-whole-frame-census-20261020'
GROUP=ROOT/'output/h5-whole-group-selection-20261020'
SRC=ROOT/'output/h5-skeleton-contact-selection-20261020'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();div=load(DIV/'audit/checks.json');census=load(CENSUS/'checks.json')
    model=load(GROUP/'model-audit.json');results=load(GROUP/'result-audit/checks.json')
    assert div['all_visited_states_and_decisions_verified'] and div['no_improved_partial']
    assert census['compatible_group_combinations']==6 and census['distinct_complete_frame_groups']==26
    assert model['all_six_models_reconstructed_in_full'] and results['all_returned_layouts_checked']==21
    assert not results['improved_partial'] and [r['inserts'] for r in results['cases']]==[12,12,10,11,13,13]
    core=source_digest();assert core=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    oldreview=load(ROOT/'benchmarks/results/h5-area-capacity-relaxations-20261020/source-review.json')
    readmes={p:digest(ROOT/p) for p in oldreview['current_readmes']}
    assert readmes==oldreview['current_readmes']
    inputs={}
    for run in [DIV,CENSUS,GROUP]:
        for p,h in load(run/'plan.json')['inputs'].items():
            assert digest(ROOT/p)==h;inputs[p]=h
    next_step=('The six complete frame/cog combinations from the retained layouts are exhausted within this finite pose pool; '
        'do not rerun them unchanged. Next investigate a changed model requiring whole frame placements while temporarily '
        'relaxing bracket/insert variables, with an explicit constraint excluding the 26 already reviewed exact frame sets. '
        'Fix one original cog arrangement at a time. Declare finite time/case limits before running. Only newly found complete '
        '18-frame sets should proceed to a separately bounded exact bracket/insert completion check. Fractional completion '
        'or restricted infeasibility has no original-job acceptance credit. If no new complete set appears, preserve that '
        'failure rather than retrying a suffix. Any full original 66-copy layout still needs the frozen validator, independent '
        'filled-outer geometry, native-margin qualification and unchanged H5 material/cutting gates. H2 stays open under '
        'Artem’s explicit decision to retain the original denominator.')
    ci=json.loads(subprocess.check_output(['gh','run','view','39434650389','--json','status,conclusion,headSha,url'],cwd=ROOT))
    for source,name in [(DIV/'audit/checks.json','diving-audit.json'),(CENSUS/'checks.json','frame-census.json'),
        (GROUP/'model-audit.json','model-audit.json'),(GROUP/'result-audit/checks.json','result-audit.json')]:
        shutil.copyfile(source,OUT/name)
    write(OUT/'source-review.json',{'production_digest':core,'current_readmes':readmes,
        'runtime_changed':False,'native_packing_calls':0,'quality_runs':0,'new_release_qualified':False,
        'H2_complete':False,'H5_complete':False,'completion_percent':60,'next_investigation':next_step,
        'latest_pushed_checkpoint_CI_snapshot':ci,'local_base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()})
    members={}
    for root in [DIV,PROBE,CENSUS,GROUP]:
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    helpers=['probe_h5_highs_basis.py','construct_h5_lp_diving.py','audit_h5_lp_diving.py',
        'census_h5_frame_groups.py','prepare_h5_whole_group_selection.py','audit_h5_whole_group_models.py',
        'solve_h5_whole_groups.py','audit_h5_whole_group_results.py','solve_h5_area_relaxations.py','audit_h5_cog_lattices.py']
    for name in helpers:members['helpers/'+name]=ROOT/'output'/name
    for name in inputs:
        p=ROOT/name;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for name in ['library.json','request.json','selected-layout.json']:
        members['source-inputs/'+SRC.relative_to(ROOT).as_posix()+'/'+name]=SRC/name
    archive=OUT/'raw.zip';manifest=[]
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):
            z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for r in manifest:assert sha256(z.read(r['path'])).hexdigest()==r['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),
        'all_input_hashes_verified':True,'archive_members':len(manifest),'archive_sha256':digest(archive),
        'diving_states_audited':421,'saved_fractional_vectors_audited':227,'whole_group_models_audited':6,
        'returned_physical_partials_audited':21,'full_target_witness':False,'completion_percent':60})
    shutil.copyfile(__file__,OUT/'seal_h5_diving_and_groups.py')
    table='\n'.join(f"| {r['case']} | {r['frame_group']} | {r['cog_group']} | {r['seconds']:.9f} | {r['inserts']} | {r['missing_inserts']} |" for r in results['cases'])
    report=f'''# H5: bounded branching and whole-group diagnosis — 2026-10-20

**No complete layout or improved partial was found.** Fixing complete frame and
cog arrangements reduces six previously difficult conditional problems to
sub-second solves, but each leaves 8–11 inserts missing. H2/H5 remain open at 60%.
The README already describes the published preview and the remaining work;
no product change or new release is justified by these diagnostics.

## Bounded LP-guided branching

The [previous area relaxations](h5-area-capacity-relaxations-20261020.md) leave all
four cog cases feasible only fractionally. This construction fixes actual
placement decisions, propagates conflict cliques and family quotas, and requires
all 21 inserts. It reuses the saved roots and restores each parent simplex basis.
A tiny saved probe checks the installed HiGHS API against an elementary LP before
the construction; no solver package or product dependency is changed.

The plan declares **120 seconds total**, at most **512 visited nodes**, at most
**10 seconds per LP**, eight offline threads and seed zero. Round-robin cases use
depth-first branching, selecting the highest-valued available pose in the first
unfinished family: frame, bracket, insert. The selected branch precedes exclusion.
The search stops after **120.005029800 seconds and 421 LP calls**. All inputs,
branch states, decisions, results and 41 unvisited frontier entries are retained.
No suffix is retried.

- 227 optimal fractional vectors; all independently checked against the original
  rows, area capacities, exact quantities and fixed-variable bounds.
- 193 restricted LP infeasibility reports and one final time limit, preserved as
  solver reports without an independent global infeasibility certificate.
- 417 calls restore a parent basis; the four initial branches start cold.
- Maximum fixed frames in cases 0–3: **9, 10, 12, 13**. No case completes the
  required 18 frames or reaches bracket/insert branching.

Independent set-based propagation reproduces every state, branch choice, visit
order and frontier entry. Maximum row, equality and bound residuals are
8.48654×10⁻⁷, 1.19096×10⁻¹⁰ and 3.66934×10⁻¹¹ respectively.
The existing 58-part partial is preserved exactly, with eight inserts missing.
These failures do not prove the unrestricted job impossible.

## Complete frame groups

The already audited source events contain **48 complete source frame groups**,
deduplicating to **26 exact sets of 18 original poses**. All 3,978 within-frame
pairs pass filled-outer checks; minimum distance is 0.225 mm.
Crossing these sets with the four complete 15-cog arrangements yields 104
combinations. All 20,592 same-sheet frame/cog pairs are checked, and the result
agrees with the existing candidate compatibility map. **Only six combinations
are compatible.** All six retain enough individual bracket and insert candidates
to pass a simple quantity count; that count alone does not show they can coexist.

For each compatible pair, a new finite model fixes all 18 frames and 15 cogs,
requires 12 brackets, and maximizes whole inserts from zero to the original cap
21. It projects the original conflict cliques onto every surviving candidate.
Models contain 542–964 Boolean variables and 1,804–3,069 distinct cliques.
All six protobuf models, including objective, domains, quantities and hint, are
independently reconstructed before solving. Geometry checks also cover all
101,663 same-sheet pairs within fixed groups and between each surviving pose and
the fixed parts. The matching case receives the complete known 58-part hint.

Each case declares one **20-second maximum**, eight workers and seed zero.
All six return `OPTIMAL` in less than 0.6 seconds:

| Case | Frame group | Cog group | Seconds | Inserts placed | Inserts missing |
| --- | ---: | ---: | ---: | ---: | ---: |
{table}

These are solver-reported optima for the **fixed-group finite-pose subproblems**.
They are not independent infeasibility certificates or upper bounds on arbitrary
continuous layouts. They show that recombining the retained smaller-part poses
with these six fixed groups cannot supply all 21 inserts.

All **20 callback incumbents plus one different final layout** pass independent
original filled-outer, rotation, margin, clearance and target-material checks.
The frozen original CLI rejects all 21 layouts **only for the original insert
quantity shortfall**. None is promoted to a valid full job, and native-margin
qualification has not been attempted.

## Preserved audit corrections

The first combined auditor could not start: the existing geometry environment
lacks protobuf, and the existing solver environment lacks Shapely. Both failures
and the original auditor are saved. The corrected audit uses the two existing
environments for their respective checks and binds them to identical input
hashes. No package is installed and no solve is repeated.

The first result auditor incorrectly requires the final selected indices to
equal the last callback. Case 4 returns a different layout with the same optimum.
The failure, original auditor and completed checks remain. The corrected auditor
checks this additional final layout separately and reuses the already saved CLI
checks after verifying their exact layouts and commands. No search or completed
validator measurement is repeated.

## Next investigation and repository state

{next_step}

Product digest and all three current README hashes remain unchanged. The hosted
browser continues to be a preview from main. The CI snapshot for pushed merge
8a81205 is retained without assuming completion; these new offline diagnostics
and the preceding area checkpoint are local until a subsequent recorded push.
No held-out evaluation, native packing, quality run, registry publication,
release asset or milestone credit changes.

[Checks]({PREFIX}/checks.json), [branch audit]({PREFIX}/diving-audit.json),
[census]({PREFIX}/frame-census.json), [model audit]({PREFIX}/model-audit.json),
[result audit]({PREFIX}/result-audit.json), [source review]({PREFIX}/source-review.json),
[raw inputs, models, branches, failures and layouts]({PREFIX}/raw.zip), and
[verified manifest]({PREFIX}/raw-manifest.json). All {len(manifest)} archive
members, CRCs and byte hashes verify.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''**N4 whole-group diagnosis, 2026-10-20:** [bounded branching and fixed-group completion](../benchmarks/results/{PREFIX}.md)
retain all 421 LP branches, 227 checked fractional solutions and 41 unvisited
frontier entries. No branch completes 18 frames. A separate census finds 26
retained complete frame sets, of which only six combinations with the four cog
sets are compatible. Six independently reconstructed fixed-group models solve
in under 0.6 seconds each, with solver-reported maxima of 12, 12, 10, 11, 13 and
13 inserts. All 21 returned partial layouts pass original geometry checks and
fail the frozen CLI only for missing inserts. No improvement, full-layout credit
or unrestricted impossibility claim. Original environment/auditor failures are
preserved and no solver run is repeated. Next investigate new complete frame
arrangements while relaxing only the smaller-part choices, explicitly excluding
the 26 reviewed exact frame sets before bounded completion checks. H2/H5 remain
open at 60%; runtime and README contents are unchanged.
'''
    previous=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==previous
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    path=ROOT/'docs/STATUS.md';text=path.read_text(encoding='utf-8')
    marker='**N4 local-area bounds, 2026-10-20:**';assert text.count(marker)==1
    path.write_text(text.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,
        'completion_percent':60,'latest_pushed_CI':ci['status']}),flush=True)
if __name__=='__main__':main()
