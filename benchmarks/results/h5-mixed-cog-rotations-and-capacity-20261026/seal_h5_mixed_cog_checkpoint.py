"""Seal mixed cog geometry, conditional allocation and both full coordinate results."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-mixed-cog-rotations-and-capacity-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'screen':'h5-mixed-cog-angle-screen-20261026','bands':'h5-mixed-cog-band-capacity-20261026','model':'h5-mixed-cog-band-model-20261026','search':'h5-mixed-cog-band-search-20261026','group_source':'h5-mixed-cog-group-strip-source-20261026','group_probe':'h5-mixed-cog-group-shared-probe-20261026','exclusion_model':'h5-mixed-cog-exclusion-master-20261026','exclusion_search':'h5-mixed-cog-exclusion-search-20261026','three_source':'h5-three-one-cog-strip-source-20261026','three_probe':'h5-three-one-cog-shared-probe-20261026','review':'h5-mixed-cog-checkpoint-review-20261026','prior_queue':'h5-profile-family-main-sync-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']=='1299e16bd461f17ef73af2bf33160c2200632a59' and review['main_head']=='88e1dc19c23eb9c5aa01b57d9537d66d87a841fb'
assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
assert review['main_ci_id']==40277918871 and review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6
audits=[('screen','audit/checks.json'),('bands','audit/checks.json'),('model','audit/checks.json'),('search','audit/checks.json'),('group_source','audit/checks.json'),('group_probe','model-audit/checks.json'),('group_probe','response-audit/checks.json'),('exclusion_model','audit/checks.json'),('exclusion_search','audit/checks.json'),('three_source','audit/checks.json'),('three_probe','model-audit/checks.json'),('three_probe','response-audit/checks.json')]
assert len(audits)==12 and all(load(base[k]/n)['passed'] for k,n in audits)
calls=[]
for key in ['search','exclusion_search']:
    r=load(base[key]/'result.json');p=load(base[key]/'process.json');a=load(base[key]/'audit/checks.json');assert r['status']=='OPTIMAL' and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and a['shared_budget_honored'] and r['solver_soft_overrun_seconds']==0 and len(list(base[key].rglob('opened.json')))==1
    calls.append({'name':key,'status':r['status'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_cap_seconds':20,'shared_cap_seconds':30,'closed':True})
for key in ['group_probe','three_probe']:
    r=load(base[key]/'search/000/result.json');p=load(base[key]/'search/process.json');a=load(base[key]/'response-audit/checks.json');assert r['status']=='INFEASIBLE' and p['exit_code']==0 and not p['timeout'] and p['seconds']<=60 and a['shared_budget_honored'] and r['solver_soft_overshoot_seconds']==0 and len(list(base[key].rglob('opened.json')))==1
    calls.append({'name':key,'status':r['status'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_cap_seconds':45,'shared_cap_seconds':60,'closed':True})
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
copies=[('screen','result.json','angle-screen.json'),('screen','pair-summary.json','pair-comparison.json'),('bands','result.json','band-summary.json'),('model','result.json','mixed-band-model.json'),('search','audit/profile-totals.json','initial-profile-totals.json'),('group_probe','inventory.json','two-two-coordinate-model.json'),('exclusion_model','result.json','conditional-master.json'),('exclusion_model','exclusion.json','conditional-count-exclusion.json'),('exclusion_model','audit/implication.json','conditional-projection.json'),('exclusion_search','audit/profile-totals.json','next-profile-totals.json'),('three_probe','inventory.json','three-one-coordinate-model.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-88e1dc19-success.json'),('prior_queue','receipt.json','prior-checkpoint-queue.json')]
for k,n,dest in copies:shutil.copyfile(base[k]/n,OUT/dest)
write(OUT/'closed-calls.json',{'closed_calls':4,'terminal_responses':4,'all_shared_budgets_honored':True,'soft_overruns':0,'calls':calls,'native_calls':0,'full_target_witness':False})
erratum={'file':'output/h5-mixed-cog-band-search-20261026/plan.json','field':'method','retained_description':'709-variable/66-constraint','correct_actual_model':'709-variable/67-constraint','explanation':'The copied prose retained66 for the original three count plus63 band constraints. The actual model adds the required profile11 sum1..4, giving67. Preparation, independent whole-model/import audit, actual solver export and response audit all use/check67. Preserve the original description and all model/result bytes; this corrects documentation only and does not authorize another call.'}
assert '709-variable/66-constraint' in load(base['search']/'plan.json')['method'] and load(base['model']/'audit/checks.json')['constraints']==67 and load(base['search']/'audit/checks.json')['returned_constraints_checked']==67
write(OUT/'run-description-erratum.json',erratum)
next_step='All4 calls are CLOSED. Do not restart/reseed/extend them or treat necessary allocations/two-part samples as layouts. The two/two phase bracket family is excluded only at counts(p0+p4,p2+p6,p3+p5,p10,p11)=(1,1,2,1,2); its714/78 master remains positive. The separate balanced/vertical-insert three/one source is also closed INFEASIBLE, but its exclusion has not been added. Broaden the next source model instead of testing each fixed count separately: balanced bracket slots[0,4],[2,6],[1,7],[3,5], insert[8,10], and each of four cog slots[9,11], with at least one profile11. This is144 physical orientation modes over36 pairs and64 ordered profile collision cases. Reuse only identical audited source cases; rebuild missing11/9 and audit every original region/plane. All18 coordinates remain free;18 choice flags make36 base variables. Nine exact-one choices plus36 conditional stock bounds, three cog x orders and at-least-one11 constraint give49 base constraints. Global cog x ordering is valid here because all four identical original copies have identical allowed[9,11] choices; never add an independent phase ordering that would restrict their spatial sequence. Independently audit complete geometry, mode clauses, flag sharing, symmetry argument and actual import before at most one45solver/60shared4worker seed0 call. No previous single-angle exclusion transfers. A negative could later justify an audited balanced-count exclusion only within this new two-phase guarded/grid family; UNKNOWN permits no exclusion. Keep all66 identities:55 checked first-sheet originals, second9 IDs21/22/25/26/37/53/63/64/65 and pending first-sheet brackets28/29. Full original/native/material validation, production integration and full H5 matrix still required. Main88e1dc19 CI40277918871 now passes all6 jobs; normally push queued1299e16b and this checkpoint after staged/ancestry checks. H2 unchanged;22 reserved vectors untouched; no new release qualified.'
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
for n in ['h5-aligned-profile-family-exclusions-20261026','h5-aligned-cog-capacity-and-cover-limit-20261026','h5-thirteen-part-selection-and-sheet-exclusion-20261026','h5-seven-part-obstruction-and-broader-source-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*mixed_cog*.py','*three_one_cog*.py'] for p in (ROOT/'output').glob(pat)]+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':12,'closed_solver_calls':4,'terminal_solver_responses':4,'all_shared_budgets_honored':True,'soft_overruns':0,'all66_original_identity_obligations_preserved':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
table='\n'.join(f"| {r['name']} | {r['status']} | {r['solver_seconds']:.6f} | {r['shared_seconds']:.6f} |" for r in calls)
report=f'''# H5: mixed cog rotations and capacity — 2026-10-26

**Independent cog rotations restore necessary capacity, but the selected
two-and-two and three-and-one orientation families both fail complete
coordinate checks. These are scoped diagnostic negatives. No full 66-part
target layout or H5 completion is claimed; completed milestone weight is 60%.**

## Original geometry and angle screen

The original cog has **20 teeth**, with four vertices per tooth. Checking the
actual radii and angular repetition establishes an 18-degree pitch, so the
half-tooth phase shift is **9 degrees**. Append profile **11 at 65.25 degrees**
to the existing **profile 9 at 56.25 degrees**. All 11 parent profiles retain
their exact values. The new width and height are approximately **279.576947 mm**;
the original 80 outer vertices and 200-vertex hole are retained.

For all four ordered angle pairs, construct the original filled-outline
Minkowski collision region and its conservative 0.2126 mm clearance envelope.
Screen the rightmost forbidden x over stock-permitted relative y using all
boundary vertex heights and endpoints. Selected offsets are rounded to the
micrometre grid and checked against original outlines, cutouts and stock.

The independent audit reconstructs all **12 profiles**, **24,336** unmerged
triangle-pair hulls, all four guarded regions, **708** boundary samples and all
four two-original placements. The minimum original pair gap is **0.212800 mm**,
above the native requirement **0.211709 mm**. Maximum profile reconstruction
error is 8.04×10⁻¹⁴ mm.

The best checked same-phase pair spans **536.405800 mm**; the best mixed pair
spans **539.292373 mm**, about **2.886574 mm wider**. Thus alternating this
half-tooth phase does not improve the screened two-part span. This local
comparison does not exclude arrangements with brackets, inserts or other
angles. It supplies no full-layout acceptance evidence.

## New necessary capacity and full coordinate checks

Rebuild and independently recompute **44,667** exact band-area coefficients
over **709** vertical cells and **63** stock bands. The new capacity model
retains all eight bracket profiles, both insert profiles and both cog angles.
Four brackets, one insert and four cogs remain mandatory, with **at least one
cog at profile 11**. No previous fixed-angle exclusion is transferred.

The actual **709-variable / 67-constraint** model is independently reconstructed
and imported. Its first bounded call is OPTIMAL, selecting bracket profiles
**4/5/5/6**, insert **10**, two cogs **9** and two **11**. The original run
description accidentally says 66 constraints; the actual model and both
independent audits include the 67th new-phase count constraint. Original bytes
are retained with a [documentation erratum]({NAME}/run-description-erratum.json).

Broaden the selected bracket types to all mirrors: one each from **0/4** and
**2/6**, two from **3/5**, with horizontal insert **10**. Both cog phases have
two mandatory copies. All 18 coordinates range over the full guarded stock;
no selected capacity cell or prior position is fixed. Only identical bracket
slots are profile-ordered, and cog x ordering applies separately within each
same-phase pair.

Independent geometry checks cover **39** collision cases, **22,612** unmerged
triangle-pair hulls, **655** guarded faces and **27,254** outside planes. The
**14,433-variable / 14,812-constraint** shared-plane model retains all **74**
physical orientation modes over all **36** pairs. Its only call is INFEASIBLE.

An exact conditional count exclusion removes only
**(p0+p4, p2+p6, p3+p5, p10, p11) = (1,1,2,1,2)**. The audit checks **9,216**
joint bracket/cog identity permutations, all six assignments of two cog phases,
40,000 count/flag truth cases, exact parent restoration and actual solver import.
The resulting **714-variable / 78-constraint** master remains OPTIMAL and
selects balanced bracket types, vertical insert **8**, three cogs **9** and
one **11**.

The next coordinate model allows one bracket each from **0/4, 2/6, 1/7, 3/5**,
including every mirror choice. Distinct bracket slots are unordered. Only the
three identical profile-9 cogs are x-ordered. Independent reconstruction checks
**52** collision cases, **17,920** triangle-pair hulls, **733** guarded faces and
**30,814** planes. Its **12,721-variable / 13,047-constraint** model also retains
all 74 modes / 36 pairs and returns INFEASIBLE. Its exclusion has not yet been
added to the master; the result remains preserved in full.

## Closed calls and next step

| Call | Result | Solver seconds | Shared seconds |
|---|---|---:|---:|
{table}

All **four** calls are closed with terminal responses. Necessary calls use
20 solver / 30 shared seconds; coordinate calls use 45 / 60, four workers and
seed zero. There are no overruns or retries. All **12** independent audits pass.

Next combine the remaining balanced families in one broader source model:
each cog independently chooses **9/11**, and the insert chooses **8/10**, with
at least one profile-11 cog. This covers **144** physical orientation modes
and **64** ordered collision cases. Global cog x ordering is then valid because
all four identical original copies have the same allowed choices; do not add
a separate phase ordering that would constrain their spatial sequence.
Audit every original region, stock bound, source clause, shared plane and
actual import before a newly declared bounded call. Existing fixed-phase
negatives do not by themselves exclude the broader family.

All identities remain explicit: **55** checked first-sheet originals, mandatory
second-sheet **21/22/25/26/37/53/63/64/65**, and pending first-sheet brackets
**28/29**. Full original/native/material checks, production integration under
the existing budget and the complete H5 matrix remain necessary.

At **{review['utc']}**, [main CI40277918871](https://github.com/skulitom/Nestbolt/actions/runs/40277918871)
for **88e1dc19** passes all six jobs. Queued **1299e16b** and this checkpoint can
be pushed normally after staging and ancestry verification. Production,
READMEs, upstream heads/releases and all 22 reserved H2 vectors remain unchanged.
H2 keeps its original gate. No new release is qualified.

[Checks]({NAME}/checks.json), [pair comparison]({NAME}/pair-comparison.json),
[closed calls]({NAME}/closed-calls.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). All {archive['archive_members']:,}
canonical files and {archive['verified_aliases']:,} aliases are byte/SHA-256/CRC
verified in {archive['archive_parts']} archive parts.
'''
(ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
note='''

**N4 mixed cog rotations, 2026-10-26:** [the evidence]({link})
verifies the original 20-tooth geometry and a second cog angle of 65.25 degrees,
9 degrees beyond 56.25. Four original-pair screens show no local width benefit
from this half-tooth phase, but a new 709-variable / 67-constraint capacity model
with at least one new-angle cog is positive. Complete coordinate models reject
the selected two/two and three/one cog-phase families with all bracket mirrors.
A checked conditional exclusion preserves the first negative without copying
old single-angle cuts. All 12 audits pass; all four calls close within declared
budgets without overruns. The original run-description 66-constraint typo is
preserved with an erratum; the actual initial model and audits use 67. Next test
balanced bracket types with both insert choices and independent 9/11 cog choices
in one audited 144-mode model. All 66 identities remain mandatory; first-sheet
brackets 28/29, full native/material checks and the H5 matrix remain open.
Main 88e1dc19 passes all six CI checks, so queued 1299e16b and this checkpoint may
be pushed normally after verification. H2/H5 remain open at 60%; production,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
