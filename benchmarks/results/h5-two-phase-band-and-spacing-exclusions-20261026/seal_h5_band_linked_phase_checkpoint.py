"""Seal complete two-phase families, valid band/spacing implications and all closed calls."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-two-phase-band-and-spacing-exclusions-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'balanced_source':'h5-balanced-phase-choice-source-20261026','balanced_base':'h5-balanced-phase-choice-probe-20261026','balanced_link':'h5-balanced-band-link-probe-20261026','balanced_master':'h5-balanced-phase-exclusion-master-20261026','balanced_search':'h5-balanced-phase-exclusion-search-20261026','repeated_source':'h5-repeated-bracket-phase-source-20261026','repeated_base':'h5-repeated-bracket-phase-base-20261026','repeated_link':'h5-repeated-band-link-probe-20261026','spacing':'h5-cog-spacing-bounds-20261026','spacing_probe':'h5-repeated-spacing-probe-20261026','final_master':'h5-repeated-phase-exclusion-master-20261026','final_search':'h5-repeated-phase-exclusion-search-20261026','recovery':'h5-repeated-phase-runner-recovery-20261026','review':'h5-band-linked-phase-checkpoint-review-20261026','previous_sync':'h5-mixed-cog-main-sync-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']==review['main_head']=='50cdc07ecf823e0e02b0c256b41d026de1427b41'
assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
assert review['main_ci_id']==40284102018 and review['main_ci_status']=='in_progress' and review['main_ci_successful_jobs']==5
audits=[('balanced_source','audit/checks.json'),('balanced_base','model-audit/checks.json'),('balanced_base','response-audit/checks.json'),('balanced_link','model-audit/checks.json'),('balanced_link','response-audit/checks.json'),('balanced_master','audit/checks.json'),('balanced_search','audit/checks.json'),('repeated_source','audit/checks.json'),('repeated_base','model-audit/checks.json'),('repeated_link','model-audit/checks.json'),('repeated_link','response-audit/checks.json'),('spacing','audit/checks.json'),('spacing_probe','model-audit/checks.json'),('spacing_probe','response-audit/checks.json'),('final_master','audit/checks.json'),('final_search','audit/checks.json')]
assert len(audits)==16 and all(load(base[k]/n)['passed'] for k,n in audits)
calls=[]
for key,status in [('balanced_base','UNKNOWN'),('balanced_link','INFEASIBLE'),('repeated_link','UNKNOWN'),('spacing_probe','INFEASIBLE')]:
    b=base[key];r=load(b/'search/000/result.json');p=load(b/'search/process.json');a=load(b/'response-audit/checks.json');assert r['status']==status and p['exit_code']==0 and not p['timeout'] and p['seconds']<=60 and a['shared_budget_honored'] and len(list(b.rglob('opened.json')))==1
    calls.append({'name':key,'status':status,'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_cap_seconds':45,'shared_cap_seconds':60,'soft_overrun_seconds':r['solver_soft_overshoot_seconds'],'closed':True})
for key,status in [('balanced_search','OPTIMAL'),('final_search','INFEASIBLE')]:
    b=base[key];r=load(b/'result.json');p=load(b/'process.json');a=load(b/'audit/checks.json');assert r['status']==status and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and a['shared_budget_honored'] and a['all_calls_closed'] and len(list(b.rglob('opened.json')))==1
    calls.append({'name':key,'status':status,'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_cap_seconds':20,'shared_cap_seconds':30,'soft_overrun_seconds':r['solver_soft_overrun_seconds'],'closed':True})
assert not (base['repeated_base']/'search').exists() and load(base['recovery']/'recovery.json')['passed'] and load(base['recovery']/'preflight-failure.json')['solver_calls_opened']==0
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
copies=[('balanced_base','inventory.json','balanced-source-model.json'),('balanced_link','inventory.json','balanced-band-model.json'),('balanced_link','model-audit/extension-proof.json','band-link-equivalence.json'),('balanced_master','result.json','balanced-count-master.json'),('balanced_master','audit/implication.json','balanced-count-implication.json'),('balanced_search','audit/profile-totals.json','remaining-profile-totals.json'),('repeated_base','inventory.json','repeated-uncalled-base-model.json'),('repeated_link','inventory.json','repeated-band-model.json'),('spacing','result.json','cog-spacing-summary.json'),('spacing','audit/case-checks.json','cog-spacing-case-checks.json'),('spacing_probe','inventory.json','repeated-spacing-model.json'),('spacing_probe','model-audit/implication.json','spacing-implication.json'),('final_master','result.json','final-capacity-model.json'),('final_master','exclusion.json','final-count-exclusion.json'),('final_master','audit/implication.json','final-count-implication.json'),('recovery','preflight-failure.json','helper-generation-failure.json'),('recovery','recovery.json','helper-generation-recovery.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-50cdc07e-in-progress.json'),('previous_sync','receipt.json','previous-main-sync.json')]
for k,n,dest in copies:shutil.copyfile(base[k]/n,OUT/dest)
overruns=[r for r in calls if r['soft_overrun_seconds']>0]
write(OUT/'closed-calls.json',{'closed_calls':6,'terminal_responses':6,'all_shared_budgets_honored':True,'soft_overrun_calls':len(overruns),'max_soft_overrun_seconds':max(r['soft_overrun_seconds'] for r in calls),'calls':calls,'uncalled_base_models':1,'native_calls':0,'full_target_witness':False})
scope='The final721-variable/94-constraint necessary master is INFEASIBLE after two complete orientation-family exclusions. It covers four brackets with all eight allowed profiles, one insert with both orientations and four cogs independently choosing56.25/65.25degrees with at least one65.25degree cog. The earlier all56.25degree branch is already closed in its own source evidence. This exhausts the tested two-phase branch under the recorded conservative source geometry, stock margins and micrometre coordinate grid. It does not prove unrestricted original/native/continuous packing impossible, does not cover other cog rotations or compositions, and is not H5 acceptance.'
write(OUT/'scope.json',{'conclusion':scope,'continuous_native_impossibility_claimed':False,'full_target_witness':False,'H5_complete':False})
next_step='All6 calls are CLOSED, including both UNKNOWN responses; no restart/reseed/extension and no exclusion inferred from UNKNOWN. The final721/94 master is negative for the tested two-phase family with at least one profile11; the earlier all-profile9 branch is separately negative. Change the allowed geometry rather than revisit these cases. Next screen the full18degree tooth period at2.25degree samples: base56.25degree plus k*2.25 for k0..7, retaining exact current profiles9(k0) and11(k4) and appending full-original profiles for the six missing samples. This is finite allowed-angle exploration, not a continuous-rotation proof. Preserve all80 outer and200 hole vertices; do not replace the shape with a regularized tooth approximation. Construct/audit all64 ordered cog-pair raw/guarded regions or reuse only exact identical cases. For each pair use its exact stock-Y range, screen full boundary heights, verify candidate original/grid pairs and whole-height forbidden rectangles separately. Predeclare a bounded geometry build/audit with progress; no solver call is authorized by the screen alone. Compare pair span/spacing and capacity before selecting a new source family. Any expanded-angle band model must recompute affected exact coefficients and must not transfer current conditional exclusions to new angles; any required newly added-angle count should be explicit. Keep all66 identities:55 checked first-sheet originals, nine short-sheet IDs21/22/25/26/37/53/63/64/65, pending first-sheet brackets28/29. Full original/native/material validation, production integration within60seconds and full H5 matrix remain required. Main50cdc07e CI40284102018 has five passing jobs while Windows runs; commit/queue this evidence and normally push only after the current run succeeds. Production/READMEs/H2 remain unchanged;22 reserved vectors untouched; no new release qualifies.'
write(OUT/'next-step.json',{'action':next_step,'next_solver_call_opened':False,'pending_first_sheet_originals':[28,29],'mandatory_second_sheet_originals':[21,22,25,26,37,53,63,64,65],'H5_complete':False})
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
for n in ['h5-mixed-cog-rotations-and-capacity-20261026','h5-aligned-profile-family-exclusions-20261026','h5-aligned-cog-capacity-and-cover-limit-20261026','h5-thirteen-part-selection-and-sheet-exclusion-20261026','h5-seven-part-obstruction-and-broader-source-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*balanced_phase*.py','*balanced_band_link*.py','*repeated_bracket_phase*.py','*repeated_band_link*.py','*cog_spacing*.py','*repeated_spacing*.py','*repeated_phase*.py','*band_linked_phase*.py'] for p in (ROOT/'output').glob(pat)]+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':16,'closed_solver_calls':6,'terminal_solver_responses':6,'unknown_responses':2,'all_shared_budgets_honored':True,'soft_overrun_calls':len(overruns),'max_soft_overrun_seconds':max(r['soft_overrun_seconds'] for r in calls),'preserved_preflight_failures':1,'preflight_failure_solver_calls':0,'final_capacity_status':'INFEASIBLE','final_capacity_variables':721,'final_capacity_constraints':94,'all66_original_identity_obligations_preserved':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
table='\n'.join(f"| {r['name']} | {r['status']} | {r['solver_seconds']:.6f} | {r['shared_seconds']:.6f} | {r['soft_overrun_seconds']:.6f} |" for r in calls)
report=f'''# H5: two-phase band and spacing exclusions — 2026-10-26

**The tested two-angle branch is exhausted within its conservative source
geometry and micrometre coordinate grid. Complete family models become
INFEASIBLE after independently verified area and spacing implications are
made explicit. Their conditional exclusions leave the final capacity master
INFEASIBLE. No unrestricted packing-impossibility or H5 acceptance claim follows;
H2/H5 remain open at 60% completed milestone weight.**

## Balanced bracket family: complete choices and band links

Use one bracket each from **0/4, 2/6, 1/7, 3/5**, either insert **8/10**, and
four cogs independently choosing **9/11** (56.25° / 65.25°), with at least one
profile-11 cog. All nine originals remain mandatory and all 18 coordinates
range across the full guarded short stock.

The source includes **64** ordered collision cases and **144** physical
orientation modes over **36** part pairs. Independent geometry reconstruction
checks **30,464** unmerged triangle-pair hulls, **945** guarded faces and
**39,535** planes. All four cog copies have the same allowed choices, so they
can be x-sorted together with their chosen phases; the audit checks **360**
phase/order cases. No separate phase order restricts their spatial sequence.

The **31,797-variable / 32,646-constraint** shared-plane model returns UNKNOWN.
Its exact result remains preserved; no exclusion is inferred from it.

Add **916** Boolean vertical-cell selectors. For every original/profile choice,
the complete disjoint cell cover spans its entire permitted integer Y domain.
Each selector implies its interval, and each of **18** cell sums equals the
existing profile flag. All **63** independently verified band-area bounds are
then linked to the actual selections. No capacity cell is fixed or preferred.
The audit checks **909,760** permitted part/profile Y values through exact
contiguous coverage and all **57,708** cell/band coefficients.

Every parent coordinate witness extends to its unique cells and respects the
necessary occupied-area limits; conversely the new model retains every parent
constraint. This preserves source-coordinate feasibility while exposing useful
implications. The **32,713-variable / 33,643-constraint** model is INFEASIBLE.

Its checked four-count exclusion removes balanced bracket counts from the
mixed-angle master. Independent relabelling checks cover 384 bracket cases,
360 cog phase/order cases and both insert choices—their **276,480** Cartesian
combinations. Exact parent restoration, 10,000 count/flag truth cases and real
solver import pass. The **718-variable / 87-constraint** master remains OPTIMAL,
selecting one bracket each from **0/4** and **2/6**, two from **3/5**, a horizontal
insert, three profile-9 cogs and one profile-11 cog.

## Repeated bracket family: all phases and provable spacing

Broaden that family immediately to both insert choices and all independent
cog 9/11 choices with at least one 11. Its **48** collision cases, **29,056**
triangle-pair hulls, **796** faces and **32,886** planes independently verify.
The two repeated bracket slots may be x-sorted with their profile choices;
other bracket types remain unordered. All 144 orientation modes are retained.

The **31,892-variable / 32,746-constraint** shared-plane base is audited but
never called. Add the complete area channeling first. Its sole
**32,808-variable / 33,743-constraint** call returns UNKNOWN, also preserved.

Next derive cog-spacing bounds from the full original collision envelopes.
For each ordered phase pair, certify a whole forbidden rectangle covering
**every** stock-permitted relative Y, with X from zero through one integer
unit below the proposed bound. Strict containment, with minimum boundary
margin **0.001153 mm**, proves the implication; sampled boundary minima alone
are not used as proof. Independent reconstruction checks **24,336** original
triangle-pair hulls and **704** boundary samples, then every complete rectangle.

| Cog profiles | Required minimum horizontal center separation |
|---|---:|
| 9 / 9 | 257.862 mm |
| 9 / 11 or 11 / 9 | 260.232 mm |
| 11 / 11 | 258.046 mm |

Global cog x ordering makes each difference nonnegative. Add **six** universal
pair bounds at the smallest threshold and **24** bounds conditional on the
actual phase-choice flags. All original variables, clauses, stock choices and
band links remain unchanged. The **32,808-variable / 33,773-constraint** model
is INFEASIBLE in about **19.1 solver seconds**.

## Final conditional capacity result

Exclude exactly **(p0+p4, p2+p6, p3+p5) = (1,1,2)**, independently of insert
orientation or cog phase counts allowed by the master. The audit checks
**9,216** bracket identity/mirror/x-order cases, **360** cog cases and both
insert choices, covering **6,635,520** Cartesian combinations. It verifies
the complete area/spacing implications, actual negative response, unchanged
parent, exact three-count logic and real solver import.

The resulting **721-variable / 94-constraint** master is **INFEASIBLE**.
Together with the earlier separately closed all-profile-9 branch, this leaves
no candidate in the tested two-angle guarded-source/grid branch. Other angles,
compositions and continuous original layouts remain outside that conclusion.

## Preserved calls and preparation failure

| Call | Result | Solver seconds | Shared seconds | Soft overrun |
|---|---|---:|---:|---:|
{table}

All **six** calls are closed with terminal responses and all **16** audits pass.
The two UNKNOWN calls exceed their 45-second soft limits by **0.113378** and
**1.477276 seconds**, respectively; both remain inside the declared 60-second
shared budget. Necessary calls use 20 / 30 seconds. No watchdog termination,
restart, reseed or extension occurs. Unknown results support no exclusions.

One helper-generation attempt fails after generating the final model builder
and auditor, before creating its runner or opening any solver call. A suffix
test mistakenly routes the runner template through audit-specific replacement
logic. The original helper and failure are preserved; a separate recovery
creates only the two missing helpers. The already prepared model/audit remains
unchanged, and the final master is called exactly once.

## Next work and repository state

Next screen the full 18-degree tooth period at 2.25-degree samples, retaining
the exact existing profiles and adding the six missing original rotations.
Compare original-pair span, certified spacing and band capacity before choosing
a new source family. This finite screen is not a continuous-rotation theorem;
current conditional exclusions cannot transfer to newly added angles.

The full job still requires all **66** originals: **55** checked first-sheet
originals, nine short-sheet IDs **21/22/25/26/37/53/63/64/65**, and pending
first-sheet brackets **28/29**. Full native/material validation, production
integration under the original budget and the full H5 matrix remain required.

At **{review['utc']}**, main and local HEAD are **50cdc07e**. The
[main CI run](https://github.com/skulitom/Nestbolt/actions/runs/40284102018)
has five successful jobs while Windows checks run. Commit and queue this
checkpoint until that run succeeds, without cancelling it. Upstream releases,
production and the accurate READMEs are unchanged. H2 retains its original gate;
all 22 reserved vectors remain untouched. No new release is qualified.

[Checks]({NAME}/checks.json), [closed calls]({NAME}/closed-calls.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[preparation failure]({NAME}/helper-generation-failure.json),
[raw manifest]({NAME}/raw-manifest.json). All {archive['archive_members']:,}
canonical files and {archive['verified_aliases']:,} aliases are byte/SHA-256/CRC
checked in {archive['archive_parts']} archive parts.
'''
(ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
note='''

**N4 two-phase band and spacing exclusions, 2026-10-26:** [the evidence]({link})
closes the tested 56.25°/65.25° source branch. Complete 144-mode balanced and
repeated-bracket families include both insert choices and every cog-angle mix
with at least one new-phase cog. Exact vertical-cell area links preserve all
source-coordinate choices; certified full-height forbidden rectangles add
necessary cog spacing of 257.862–260.232 mm. Both strengthened coordinate
families are INFEASIBLE, and audited conditional exclusions leave the final
721-variable / 94-constraint capacity master INFEASIBLE. This conclusion is
limited to the conservative source geometry and micrometre grid. All 16 audits
pass and six calls are closed within shared budgets; two UNKNOWN calls retain
soft overruns of 0.113378 and 1.477276 seconds. One helper-generation failure
before any solver call is preserved with its separate recovery. Next screen
additional original cog rotations across the tooth period; no current exclusion
transfers to changed angles. All 66 identities and full H5 validation remain
required. Main 50cdc07e has five passing checks while Windows CI runs, so queue
this checkpoint for a later normal push. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved vectors remain unchanged.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
