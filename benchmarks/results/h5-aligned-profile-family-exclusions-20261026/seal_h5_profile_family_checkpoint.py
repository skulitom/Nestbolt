"""Seal the full aligned-angle profile-family exclusion chain and its limits."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-aligned-profile-family-exclusions-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={
 'exact_model':'h5-profile-exclusion-master-20261026','exact_search':'h5-profile-exclusion-search-20261026',
 'alternate_source':'h5-aligned-alternate-strip-source-20261026','alternate_probe':'h5-aligned-alternate-strip-probe-20261026',
 'group_source':'h5-profile-group-strip-source-20261026','group_probe':'h5-profile-group-shared-probe-20261026',
 'group_model':'h5-group-exclusion-master-20261026','group_search':'h5-group-exclusion-search-20261026',
 'balanced_source':'h5-balanced-group-strip-source-20261026','balanced_probe':'h5-balanced-group-shared-probe-20261026',
 'balanced_model':'h5-balanced-exclusion-master-20261026','balanced_search':'h5-balanced-exclusion-search-20261026',
 'horizontal_source':'h5-balanced-horizontal-strip-source-20261026','horizontal_probe':'h5-balanced-horizontal-shared-probe-20261026',
 'union_model':'h5-balanced-union-master-20261026','union_search':'h5-balanced-union-search-20261026',
 'review':'h5-profile-family-checkpoint-review-20261026','previous_sync':'h5-aligned-cog-main-sync-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']==review['main_head']=='88e1dc19c23eb9c5aa01b57d9537d66d87a841fb'
assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
assert review['main_ci_id']==40277918871 and review['main_ci_status']=='in_progress' and review['main_ci_successful_jobs']==5
audits=[]
for stem in ['exact','group','balanced','union']:
    audits.extend([(stem+'_model','audit/checks.json'),(stem+'_search','audit/checks.json')])
for stem in ['alternate','group','balanced','horizontal']:
    audits.extend([(stem+'_source','audit/checks.json'),(stem+'_probe','model-audit/checks.json'),(stem+'_probe','response-audit/checks.json')])
assert len(audits)==20 and all(load(base[k]/n)['passed'] for k,n in audits)
calls=[]
for stem,expected in [('exact','OPTIMAL'),('group','OPTIMAL'),('balanced','OPTIMAL'),('union','INFEASIBLE')]:
    b=base[stem+'_search'];r=load(b/'result.json');p=load(b/'process.json');a=load(b/'audit/checks.json')
    assert r['status']==expected and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and a['shared_budget_honored'] and a['all_calls_closed'] and r['solver_soft_overrun_seconds']==0
    assert len(list(b.rglob('opened.json')))==1
    calls.append({'name':stem+'_master','kind':'necessary allocation with conditional exclusions','status':r['status'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'soft_cap_seconds':20,'shared_cap_seconds':30,'closed':True})
for stem in ['alternate','group','balanced','horizontal']:
    b=base[stem+'_probe'];r=load(b/'search/000/result.json');p=load(b/'search/process.json');a=load(b/'response-audit/checks.json')
    assert r['status']=='INFEASIBLE' and p['exit_code']==0 and not p['timeout'] and p['seconds']<=60 and a['shared_budget_honored'] and r['solver_soft_overshoot_seconds']==0
    assert len(list(b.rglob('opened.json')))==1
    calls.append({'name':stem+'_coordinates','kind':'complete guarded source coordinates for nine originals','status':r['status'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'soft_cap_seconds':45,'shared_cap_seconds':60,'closed':True})
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k in ['exact_model','group_model','balanced_model','union_model']:
    for n in ['result.json','exclusion.json','audit/implication.json']:
        if (base[k]/n).exists():shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k in ['alternate_probe','group_probe','balanced_probe','horizontal_probe']:shutil.copyfile(base[k]/'inventory.json',OUT/(k+'-inventory.json'))
for k in ['exact_search','group_search','balanced_search']:shutil.copyfile(base[k]/'audit/profile-totals.json',OUT/(k+'-profile-totals.json'))
shutil.copyfile(base['union_model']/'audit/source-proof-cover.json',OUT/'balanced-two-insert-proof-cover.json')
shutil.copyfile(base['review']/'review.json',OUT/'source-review.json');shutil.copyfile(base['review']/'main-ci.json',OUT/'main-ci-88e1dc19-in-progress.json');shutil.copyfile(base['previous_sync']/'receipt.json',OUT/'previous-main-sync.json')
write(OUT/'closed-calls.json',{'closed_calls':8,'terminal_responses':8,'all_shared_budgets_honored':True,'soft_overruns':0,'calls':calls,'native_calls':0,'full_target_witness':False})
scope='For the short-sheet composition4brackets/1insert/4cogs with every cog fixed at56.25degrees, all eight bracket profiles and both insert profiles remain represented in the necessary band master. Four audited conditional exclusions, derived from complete whole-stock guarded coordinate models and identical-copy relabelling, leave the692-variable/104-constraint master INFEASIBLE. This closes that guarded-source/micrometre-grid candidate branch only. It is not a theorem about unrestricted original geometry, continuous coordinates, other cog angles/compositions or the full66-original target.'
write(OUT/'scope.json',{'conclusion':scope,'full66_target_witness':False,'native_impossibility_claimed':False,'continuous_impossibility_claimed':False,'H5_complete':False})
next_step='All8 calls are CLOSED; no extension/reseed/retry. Change the source geometry choices rather than revisiting these fixed-angle patterns: screen original cog-to-cog clearance for independently selectable rotations, beginning with56.25degrees and a half-tooth-phase offset derived from the actual original vertices. This is a geometric hypothesis only. Preserve every outer/cutout vertex and independently reconstruct any added profile; no current conditional exclusion transfers to a changed cog choice. If the screening supports a different model, rebuild affected exact band coefficients/collision cases and independently audit a newly declared bounded model before calling it. All66 originals remain mandatory:55 checked first-sheet originals, nine short-sheet originals21/22/25/26/37/53/63/64/65, and first-sheet brackets28/29 pending. Any candidate still needs full original/native/material validation, production integration under60seconds and the full H5 matrix. No release qualifies. Main88e1dc19 CI40277918871 has five successful jobs and Windows checks still running; commit this checkpoint and queue its normal main push until that run is terminal successful, without cancelling it. H2 remains unchanged and22 reserved vectors untouched.'
write(OUT/'next-step.json',{'action':next_step,'next_call_opened':False,'pending_first_sheet_originals':[28,29],'mandatory_second_sheet_originals':[21,22,25,26,37,53,63,64,65],'H5_complete':False})
members={};inputs={}
for folder in base.values():
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for field in ['inputs','input_hashes','additional_inputs']:
            for n,h in load(p).get(field,{}).items():
                if n in inputs:assert inputs[n]==h,n
                inputs[n]=h
for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
for n in ['h5-aligned-cog-capacity-and-cover-limit-20261026','h5-thirteen-part-selection-and-sheet-exclusion-20261026','h5-seven-part-obstruction-and-broader-source-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*profile_exclusion*.py','*alternate_strip*.py','*profile_group*.py','*group_exclusion*.py','*balanced*.py','*profile_family*.py'] for p in (ROOT/'output').glob(pat)]+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p;s=p.read_text(encoding='utf-8')
    for n in re.findall(r"['\"]([A-Za-z0-9_.-]+\.py)['\"]",s):
        q=ROOT/'output'/n
        if q.is_file():helpers.append(q)
    for node in ast.walk(ast.parse(s)):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':20,'closed_solver_calls':8,'terminal_solver_responses':8,'watchdog_terminations':0,'all_shared_budgets_honored':True,'soft_overruns':0,'final_necessary_model_status':'INFEASIBLE','final_necessary_model_variables':692,'final_necessary_model_constraints':104,'all66_original_identity_obligations_preserved':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
call_table='\n'.join(f"| {r['name']} | {r['status']} | {r['solver_seconds']:.6f} | {r['shared_seconds']:.6f} |" for r in calls)
report=f'''# H5: aligned-angle profile-family exclusions — 2026-10-26

**The fixed 56.25-degree cog branch is closed within its guarded source models
and micrometre coordinate grid. After full coordinate checks exclude the
remaining orientation families, the strengthened capacity model is INFEASIBLE.
This is a conditional diagnostic result, not a complete-layout result or an
unrestricted packing-impossibility claim. H2/H5 stay open at 60%.**

## Preserved composition and scope

Every case retains four brackets, one insert and four cogs on the short sheet:
original IDs **21/22/25/26/37/53/63/64/65**. The verified first-sheet exchange
retains 55 other originals; brackets **28/29** still require first-sheet positions.
All 66 identities and original cutouts remain required. No native validator is
called on a partial layout.

The parent capacity model has 675 cell variables and 66 constraints. Its exact
band bounds and original counts remain unchanged. No selected vertical cell
is locked in the coordinate models: all 18 coordinates range across the full
guarded short stock, with every one of the 36 physical pairs represented.

## Conditional exclusions and full coordinate checks

1. The previous fixed-profile rejection adds the exact count exclusion
   **p4=1, p5=2, p6=1, p10=1**, giving 679 variables / 75 constraints.
   A necessary allocation remains: **0/2/5/5/10/9/9/9/9**. Its independently
   checked 8,955-variable / 9,140-constraint coordinate model is INFEASIBLE.
2. Broaden that orientation family to all mirrors: one bracket from **0/4**,
   one from **2/6**, two from **3/5**, insert **10**, four cogs **9**.
   The shared-plane model has **13,267 variables / 13,605 constraints** and
   retains all **74** physical orientation modes. It is INFEASIBLE.
   Its aggregate exclusion yields a 683-variable / 84-constraint capacity
   model, which selects the balanced family with insert **8**.
3. Balanced brackets mean one each from **0/4, 2/6, 1/7, 3/5**. All mirror
   alternatives are available; distinct bracket slots are never ordered.
   Only identical cog copies are ordered by x. With insert **8**, the
   **12,367-variable / 12,674-constraint** coordinate model is INFEASIBLE.
   Five count reifications produce the 688-variable / 95-constraint master,
   which selects balanced brackets with insert **10** instead.
4. The separate horizontal-insert model has **13,242 variables / 13,578
   constraints** and is also INFEASIBLE. Together the two balanced models
   cover both allowed insert profiles. Four bracket-count reifications and
   their not-all clause exclude balanced counts independently of insert
   orientation. The final **692-variable / 104-constraint** capacity model
   returns **INFEASIBLE**.

Every extension restores its entire parent exactly, retaining earlier
coefficients, domains, family counts and exclusions. Actual solver imports
and returned models/parameters/responses are checked. Count equalities are
reified in both directions; truth-table audits include 40,000 cases for the
five-count exclusion and 10,000 for the final four-count exclusion.

The final two-case implication audit enumerates **768** bracket identity and
mirror assignments, checks all **148** modes / **72** physical pairs across
the two source models, and verifies from the parent cells that insert **8/10**
is exhaustive. Identical family copies can be relabelled into source slots;
the bracket slots have no extra ordering restriction. This conditional
argument applies only to these guarded source representations and grid.

Independent geometry reconstruction uses the original polygons and unmerged
triangle-pair hulls. The balanced vertical and horizontal cases each check
**42** collision cases from **9,184** hulls. They retain respectively **395 /
397** guarded faces and **17,914 / 17,926** exact outside planes. Both minimum
guards are **0.2126 mm**, above the required native **0.211709 mm**. No simplified
cog, missing cutout, fixed prior second-sheet pose or optional part supplies
the result. A shared-plane flag always implies its complete original plane;
each source face retains its OR and inactive-orientation literals.

## Closed calls

| Call | Result | Solver seconds | Shared seconds |
|---|---|---:|---:|
{call_table}

All **eight** calls are closed, all have terminal responses, and all remain
inside their declared shared limits with **zero soft overruns**. Necessary
calls use at most 20 solver / 30 shared seconds; coordinate calls use at most
45 / 60. Every call uses four workers and seed zero. No retry is opened.
All **20** independent model, geometry and response audits pass.

## Remaining work and repository state

This branch now offers no surviving candidate under its tested restrictions.
It does not rule out independent cog rotations, a different composition,
continuous original layouts, or the complete target. Next screen neighboring
cogs at different angles using their full original geometry, then audit any
changed profiles and collision model. Current exclusions cannot be reused
for changed cog-angle choices. The two first-sheet brackets, full native and
material checks, production integration and full H5 matrix remain required.

At **{review['utc']}**, local HEAD and main are **88e1dc19**. The
[main CI run](https://github.com/skulitom/Nestbolt/actions/runs/40277918871)
has five passing jobs while Windows checks still run. Commit this evidence
and queue the normal push until the prior run succeeds; do not cancel it.
Upstream heads/releases, production code and the accurate READMEs are
unchanged. H2 keeps its original gate; the 22 reserved vectors stay untouched.
No new release is qualified.

[Checks]({NAME}/checks.json), [closed calls]({NAME}/closed-calls.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). The archive contains
{archive['archive_members']:,} canonical files and {archive['verified_aliases']:,}
aliases in {archive['archive_parts']} parts, all byte/SHA-256/CRC checked.
'''
(ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
note='''

**N4 aligned profile-family exclusions, 2026-10-26:** [the evidence]({link})
closes the tested branch with all four short-sheet cogs fixed at 56.25 degrees.
Full-stock coordinate checks reject the selected fixed pattern, its broader
mirror family, and balanced brackets with each of the two insert orientations.
Exact conditional count exclusions preserve the parent capacity model; the
final 692-variable / 104-constraint master is INFEASIBLE. This result is limited
to the guarded source representations and micrometre grid, not unrestricted
original packing. All 20 audits pass and eight calls close within their declared
budgets without overruns. All 66 original identities remain required, including
pending first-sheet brackets 28/29. Next examine independently rotated cogs;
no current exclusion transfers to that changed geometry. Full native/material
validation, production integration and the H5 matrix remain open. Main
88e1dc19 has five successful checks while Windows CI runs, so this checkpoint
is queued for a normal push after that run succeeds. H2/H5 remain open at 60%;
production, READMEs, releases and all 22 reserved H2 vectors are unchanged.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
