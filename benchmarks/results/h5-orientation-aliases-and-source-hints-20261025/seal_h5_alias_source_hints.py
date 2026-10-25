"""Seal exact aliases, audited source hints, the bounded result and main sync."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-orientation-aliases-and-source-hints-20261025';BASE=ROOT/'output/h5-alias-source-hints-20261025';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    generation=load(BASE/'generation.json');audit=load(BASE/'audit/checks.json');model=load(BASE/'solve/model-audit.json');hint=load(BASE/'solve/hint-audit.json');result=load(BASE/'solve/result.json');census=load(BASE/'next-source-orientations/census.json');push=load(BASE/'source-sync/push-result.json');oldci=load(BASE/'source-sync/completed-main-ci.json');prior=load(ROOT/'benchmarks/results/h5-global-propagation-and-compound-proxy-20261025/source-review.json');assert all(v['passed'] for v in [audit,model,hint,census]);assert result['status']=='UNKNOWN' and result['solver_calls']==1 and not result['incumbents'] and not result['has_full_relaxation_solution'];assert not(BASE/'solve/relaxed-positions.json').exists();log=(BASE/'solve/solver.log').read_text(encoding='utf-8');assert 'Starting search at 0.11s' in log and 'The solution hint is incomplete: 923 out of 1074 non fixed variables hinted.' in log and 'status: UNKNOWN' in log;assert not re.findall(r'^#Done',log,re.M)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head==mainhead==push['new_main'] and head.startswith('247e823a');assert push['completed'] and push['commits_pushed']==5 and oldci['status']=='completed' and oldci['conclusion']=='success' and len(oldci['jobs'])==6 and all(j['conclusion']=='success' for j in oldci['jobs']);assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items());ci=json.loads(subprocess.check_output(['gh','run','view','40233299884','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==head
    action='The exact-alias/source-hint global call remains UNKNOWN and is complete; do not repeat it or extend its allowance. Investigate a different finite constructive formulation derived from the byte-bound known64-part layout: all18 frames use its normalized horizontal orientation; inserts retain the audited eight horizontal/thirteen vertical orientation counts; the ten existing brackets retain their audited five orientation/mirror groups; two additional mandatory brackets retain every original orientation and mirror option. All15 cog centers, every part position and every allowed sheet assignment remain free. Do not hold the excluded core0 positions fixed. Order interchangeable copies only within a shared orientation-option group, never across unequal fixed-orientation groups. Map the64 source poses as nonbinding hints with complete group/copy audits. This restricts orientation inventories for a construction attempt and is not a necessary relaxation of every original arrangement: any negative result has no unrestricted implication. Declare fresh finite construction/audit limits and one bounded call before running. Any positive66-part proxy still needs larger disk/outline diagnosis, original cog angles, original clearance/native checks, material limit, production budget and all13jobs/two kerfs. Keep H2 open as instructed, preserve held-out isolation and stop rules. Main now contains the five earlier checkpoints; poll its new CI40233299884 without restarting or cancelling it, and push further checkpoints normally once that run is terminal.'
    OUT.mkdir();write(OUT/'next-step.json',{'action':action,'H5_complete':False,'full_target_witness':False})
    for rel,name in [('plan.json','plan.json'),('generation.json','generation.json'),('aliases.json','aliases.json'),('audit/checks.json','geometry-and-hint-audit.json'),('audit/provenance.json','provenance.json'),('audit/original-stock-violations.json','source-target-violations.json'),('solve/plan.json','model-plan.json'),('solve/model-audit.json','model-audit.json'),('solve/hint-audit.json','hint-encoding-audit.json'),('solve/result.json','solver.json'),('next-source-orientations/census.json','next-orientation-inventory.json'),('source-sync/completed-main-ci.json','previous-main-ci.json'),('source-sync/push-result.json','push-result.json')]:shutil.copyfile(BASE/rel,OUT/name)
    write(OUT/'main-ci.json',ci);write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,'earlier_checkpoints_pushed':5,'previous_main_all_six_checks_passed':True,'current_main_ci_id':40233299884,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for row in load(BASE/'audit/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    pending=[ROOT/'output'/n for n in ['prepare_h5_alias_source_hints.py','audit_h5_alias_source_hints.py','h5_verified_source_hints.py','prepare_h5_alias_hint_solver.py','solve_h5_alias_source_hints.py','solve_h5_compound_proxy.py','h5_compound_proxy_encoding.py','census_h5_next_orientation_inventory.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members);checks={'passed':True,'every_original_mode_has_exact_representative_and_inverse_map':True,'all_bracket_modes_retained':True,'source_original66_counts_and_geometry_audited':True,'all_seven_source_target_violations_preserved':True,'all59_hint_poses_and1482_hint_values_independently_verified':True,'hint_values_nonbinding_and_no_fixed_parts':True,'one_bounded_call_unknown_without_incumbent':True,'next_source_orientation_inventory_checked_without_search':True,'five_prior_commits_pushed_normally_after_all_six_checks_passed':True,'production_source_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,'H5_complete':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: exact orientation aliases and audited source hints — 2026-10-25

**The source-guided all-parts-movable proxy search remains `UNKNOWN`.**
Exact duplicate modes are removed without losing their packing placements;
59 compatible original poses guide the search without fixing any part.
No complete arrangement or impossibility proof is returned. H2/H5 stay open
at **60%** completed milestone weight. Five earlier evidence checkpoints have
now been pushed to main after all six previous hosted checks passed.

## Exact equivalence and reconstruction

Compare complete ordered normalized rectangle components and sheet bounds,
not just bounding-box dimensions. The 28 original sheet/orientation modes
reduce to **22** representatives: two frame modes, 16 bracket modes and four
insert modes. All 16 original orientation/reflection classes remain recorded.
Every original mode has an explicit representative and inverse reconstruction
map. The eight bracket orientation/reflection cases remain distinct on both
sheets. Exact component equality and independent polygon symmetric-difference
checks establish each alias.

For any alias, preserve the normalized anchor and subtract that original
class's zero-position bounding-box minimum to reconstruct its translation.
Its allowed original rotation/mirror restores the same filled outer region.
This equivalence applies to holes-reserved packing; original part geometry is
retained. All previous material bounds, quantities and global proxy constraints
remain. The number of per-copy modes falls from 462 to **342**.

## Full source layout and omitted hints

The original 66-part production layout is matched to its committed manifest
and target-file hash. Its quantities and copy indices check exactly. Independent
affine transforms verify all **1,456** same-sheet original polygon pairs, with
minimum gap 0.20000099999970186 mm. The maximum exact-quarter-turn difference
is 1.14e-13 mm. All **6,292** same-sheet inner-proxy component pairs also pass.
This verifies the source's geometry for this diagnostic; it does not confer
new native-margin qualification.

The original source exceeds the material target. The independent audit recovers
the same **seven** target-crossing parts recorded earlier: one frame, two
brackets, two inserts and two cogs. In particular, no frame orientation fits
the target second-sheet height. Every incompatible source pose and its reasons
remain recorded. The source's second-sheet original-area lower charge is
566,688,154 units, above the target capacity of 465,322,304 units.

Only **59** compatible poses become nonbinding hints. They contain 121 inner
rectangles and pass all **5,952** same-sheet component-pair checks, both partial
area bounds and four complete sweep profiles. Copies are relabelled by the
full source's family/sheet/y/x order, preserving the model's interchangeable
copy ordering. These partial hints do not remove the seven required parts;
all 66 remain mandatory and every position/sheet choice remains free.

Preparation takes 0.011156 seconds and independent geometry/hint auditing
takes 0.098033 seconds. Seven input files are matched to committed evidence.

## Complete model and hint encoding

Every field of **1,686 variables and 2,584 constraints** is independently
reconstructed. The same 138 inner rectangles, 552 optional intervals, two
NoOverlap2D constraints, four cumulative profiles and two original-area bounds
remain. Every one of **1,482** hinted variable values is independently rebuilt
by variable name from the audited source poses, checked against its domain,
and matched to the serialized partial assignment. No hint becomes a constraint;
the parameter that fixes variables to hints is verified false.

Construction takes 0.044779 seconds and encoding audit 0.027784 seconds,
within declared 120-second caps. One declared 60-second, eight-worker,
seed-zero call reaches search at **0.11 seconds**. The presolved model records
an incomplete hint covering 923 of 1,074 nonfixed variables. It returns
**`UNKNOWN` in {result['seconds']:.6f} seconds**, with 131,509 branches,
108,595 conflicts and no incumbent. The small soft-limit overrun is preserved.
The call is not repeated or extended, and no absent layout is reported as
an original-outline or native result.

## A different constructive direction

A read-only census of the committed 64-part target layout supplies an explicit
next orientation inventory: 18 horizontal frames; eight horizontal and thirteen
vertical inserts; ten brackets in five recorded orientation/mirror groups;
and all 15 cogs. Two additional brackets remain mandatory with every original
orientation available. That proposal keeps all positions and allowed sheet
assignments free, including the frame/cog arrangement already excluded when
held fixed. It would reduce orientation choices for a finite construction
attempt; any negative result would not exclude other original orientations.
No search on that proposed inventory occurs in this checkpoint.

{action}

## Main sync and evidence

The previous main run **40229962984** finished with all **six** jobs successful.
A normal fast-forward push then advanced main from 8f941426 to **247e823a**,
including five evidence commits. New run **40233299884** is captured as
`{ci['status']}` / `{ci['conclusion'] or 'pending'}`. Its unfinished checks are
not called a pass, and the run is not cancelled or restarted here.

Engine source, all three accurate READMEs and releases remain unchanged.
No native packing, production-budget run, full H5 matrix or held-out evaluation
occurs. Evidence-only changes do not require repeating production tests, and
no new release is qualified.

Evidence: [plan]({NAME}/plan.json), [alias map]({NAME}/aliases.json),
[source and geometry audit]({NAME}/geometry-and-hint-audit.json),
[target violations]({NAME}/source-target-violations.json),
[model audit]({NAME}/model-audit.json), [hint audit]({NAME}/hint-encoding-audit.json),
[solver]({NAME}/solver.json), [next inventory]({NAME}/next-orientation-inventory.json),
[completed previous CI]({NAME}/previous-main-ci.json), [push result]({NAME}/push-result.json),
[source review]({NAME}/source-review.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All {archive['archive_members']} canonical
members and {archive['verified_aliases']} aliases retain exact bytes with CRC
and SHA-256 checks, including all source poses, model/hints, omissions and logs.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 exact orientation aliases and audited source hints, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) checks exact representative and
inverse maps for all 28 original modes, retaining 22 representatives and all
16 original orientation/reflection classes. All bracket cases stay distinct.
The original 66-part layout passes 1,456 polygon-pair checks but exceeds the
target at the same seven recorded parts. Only 59 compatible poses supply
nonbinding hints; all 66 parts remain required and every position stays free.
Every field of the 1,686-variable/2,584-constraint model and all 1,482 hint values
verify independently. One bounded call returns UNKNOWN in 60.101281 seconds
without an incumbent or proof. A source census prepares a different finite
orientation-inventory construction, with two additional brackets mandatory;
no search of that inventory occurs yet. After all six previous main checks
passed, five checkpoints were pushed normally through 247e823a. Its new CI
40233299884 remains distinct from the completed previous run. Source, accurate
READMEs and releases are unchanged; H2/H5 remain open at 60%.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
