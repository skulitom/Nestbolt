"""Seal expanded original angles, proven spacing and all closed bounded calls."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-eight-phase-geometry-and-spacing-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'screen':'h5-eight-phase-cog-screen-20261026','preflight':'h5-eight-phase-screen-preflight-20261026','capacity':'h5-eight-phase-band-capacity-20261026','capacity_model':'h5-eight-phase-band-model-20261026','capacity_search':'h5-eight-phase-band-search-20261026','source':'h5-eight-phase-balanced-source-20261026','full':'h5-eight-phase-balanced-probe-20261026','spacing':'h5-relative-y-cog-spacing-20261026','relative':'h5-relative-y-spacing-probe-20261026','review':'h5-eight-phase-checkpoint-review-20261026','cost':'h5-eight-phase-model-cost-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']=='6927ae7d5fcc18e2a6b7dbf16c041fb54dbe2bd0'
assert review['main_head']=='50cdc07ecf823e0e02b0c256b41d026de1427b41' and review['main_ci_id']==40284102018 and review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6
assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('screen','audit-verified/checks.json'),('capacity','audit/checks.json'),('capacity_model','audit/checks.json'),('capacity_search','audit/checks.json'),('source','audit/checks.json'),('full','model-audit/checks.json'),('full','response-audit/checks.json'),('spacing','audit/checks.json'),('relative','model-audit/checks.json'),('relative','response-audit/checks.json')]
assert len(audits)==10 and all(load(base[k]/n)['passed'] for k,n in audits)
assert not (base['screen']/'audit/checks.json').exists()
assert load(base['preflight']/'recovery.json')['solver_calls']==load(base['preflight']/'audit-recovery.json')['solver_calls']==0
calls=[]
for key in ['full','relative']:
    r=load(base[key]/'search/000/result.json');p=load(base[key]/'search/process.json');a=load(base[key]/'response-audit/checks.json');assert r['status']=='UNKNOWN' and p['exit_code']==0 and not p['timeout'] and p['seconds']<=60 and a['shared_budget_honored'] and len(list(base[key].rglob('opened.json')))==1
    calls.append({'name':key,'status':r['status'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_limit_seconds':45,'shared_limit_seconds':60,'soft_overrun_seconds':r['solver_soft_overshoot_seconds'],'closed':True})
r=load(base['capacity_search']/'result.json');p=load(base['capacity_search']/'process.json');assert r['status']=='OPTIMAL' and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and len(list(base['capacity_search'].rglob('opened.json')))==1
calls.insert(0,{'name':'capacity','status':'OPTIMAL','solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_limit_seconds':20,'shared_limit_seconds':30,'soft_overrun_seconds':r['solver_soft_overrun_seconds'],'closed':True})
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
copies=[('screen','result.json','angle-screen.json'),('screen','pair-summary.json','pair-summary.json'),('capacity','result.json','band-capacity.json'),('capacity_model','result.json','capacity-model.json'),('capacity_search','audit/profile-totals.json','capacity-profile-totals.json'),('source','result.json','source-geometry.json'),('source','audit/spacing-case-checks.json','source-spacing-cases.json'),('full','inventory.json','full-model.json'),('full','strengthening.json','full-model-strengthening.json'),('full','model-audit/cog-order-proof.json','cog-order-proof.json'),('full','model-audit/source-extension-proof.json','full-source-extension.json'),('spacing','result.json','relative-spacing.json'),('relative','inventory.json','relative-model.json'),('relative','model-audit/extension-proof.json','relative-source-extension.json'),('preflight','recovery.json','screen-preflight-recovery.json'),('preflight','audit-recovery.json','screen-audit-recovery.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-50cdc07e-success.json'),('cost','cost.json','model-cost.json')]
for k,n,d in copies:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'closed-calls.json',{'calls':calls,'all_calls_closed':True,'all_shared_budgets_honored':True,'exclusion_from_unknown':False,'new_conditional_exclusions':0,'native_calls':0})
next_step=load(base['cost']/'cost.json')['next_research']+' All3 calls in this checkpoint are CLOSED. Current balanced source allows all8 sampled cog angles with at least one profile12..17, both insert choices and all mirrors within bracket groups0/4,2/6,1/7,3/5. Its two coordinate results are UNKNOWN; no balanced-family exclusion may be added. At most a compact sufficient-source formulation may be investigated, with independently proved full-domain separation and clearly narrower negative scope. Original complete model has148074 cog-cog shared planes and83713 other planes. No previous two-angle exclusions transfer. Keep all66 originals:55 checked first-sheet originals, nine short-sheet IDs21/22/25/26/37/53/63/64/65 and pending first-sheet brackets28/29. Full original/native/material validation, production60second integration and complete H5 matrix remain. Main50cdc07e has all6 checks passed, so commit then normally push6927ae7d and this checkpoint after byte/ancestry checks. H2 retains its original gate and22 reserved vectors remain untouched; production/READMEs unchanged, no new release qualified.'
write(OUT/'next-step.json',{'action':next_step,'pending_first_sheet_originals':[28,29],'full_target_witness':False,'H5_complete':False})
write(OUT/'scope.json',{'statement':'Eight sampled original cog rotations, full original outlines and cutouts preserved. Necessary area allocation is positive; both full balanced-family coordinate calls are UNKNOWN. No additional profile-family exclusion, continuous packing theorem or H5 acceptance follows. The earlier closed two-angle negative remains valid only in its recorded scope.','new_solver_calls':3,'new_negative_results':0,'full_target_witness':False,'completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs={}
for folder in base.values():
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for field in ['inputs','input_hashes','additional_inputs']:
            for n,h in load(p).get(field,{}).items():
                if n in inputs:assert inputs[n]==h,n
                inputs[n]=h
for n,h in inputs.items():
    p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
for n in ['h5-two-phase-band-and-spacing-exclusions-20261026','h5-mixed-cog-rotations-and-capacity-20261026','h5-aligned-profile-family-exclusions-20261026','h5-aligned-cog-capacity-and-cover-limit-20261026','h5-thirteen-part-selection-and-sheet-exclusion-20261026','h5-seven-part-obstruction-and-broader-source-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pattern in ['*eight_phase*.py','*relative_y*.py'] for p in (ROOT/'output').glob(pattern)]+[Path(__file__),ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p;s=p.read_text(encoding='utf-8')
    for n in re.findall(r"['\"](?:output/)?([A-Za-z0-9_.-]+\.py)['\"]",s):
        q=ROOT/'output'/n
        if q.is_file():helpers.append(q)
    for node in ast.walk(ast.parse(s)):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
print({'archiving_members_before_deduplication':len(members)},flush=True)
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':10,'closed_solver_calls':3,'unknown_coordinate_responses':2,'all_shared_budgets_honored':True,'soft_overrun_calls':2,'maximum_soft_overrun_seconds':max(r['soft_overrun_seconds'] for r in calls),'preserved_preparation_failures':2,'preparation_failure_solver_calls':0,'new_conditional_exclusions':0,'all66_original_identity_obligations_preserved':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
table='\n'.join(f"| {r['name']} | {r['status']} | {r['solver_seconds']:.6f} | {r['shared_seconds']:.6f} | {r['soft_overrun_seconds']:.6f} |" for r in calls)
report=f'''# H5: eight-phase geometry and spacing — 2026-10-26

**All eight sampled cog angles now have verified original geometry, exact band
capacity and full-domain spacing evidence. The necessary capacity allocation
is positive; both balanced-family coordinate searches remain UNKNOWN within
their shared budgets. No new exclusion or H5 acceptance follows. H2/H5 remain
open at 60% completed milestone weight.**

## Original rotations and complete pair geometry

Keep all 12 previous profiles unchanged and add six full-original rotations.
The 20-tooth cog is sampled at **56.25°, 58.5°, 60.75°, 63°, 65.25°, 67.5°,
69.75° and 72°**, covering one 18-degree tooth period at 2.25-degree steps.
Every profile retains the actual 80 outer vertices and 200-vertex cutout.
This finite screen is not a continuous-rotation theorem.

All **64** ordered cog pairs are independently reconstructed from **389,376**
unmerged original triangle-pair hulls. The audit checks **11,804** boundary
samples, 64 actual two-part grid placements and 64 complete full-height
forbidden rectangles. The original pair gaps exceed the required native guard.
The best same-angle pair spans **536.270484 mm**, about **0.135316 mm** less
than the previous aligned pair. It occurs at 58.5° (and effectively at 72°);
this small two-part improvement does not establish a full layout.

## Exact capacity and expanded balanced source

All **18** profiles have **909** complete vertical cells and **57,267** exact
cell/band coefficients over 63 stock bands. An independent edge-integral audit
recomputes every coefficient and checks 703 stationary candidates. The
**909-variable / 67-constraint** necessary master requires four brackets,
one insert and four cogs, including at least one newly added profile 12–17.
It copies no earlier profile-family exclusion. Its OPTIMAL allocation selects
balanced bracket groups, a horizontal insert, three 56.25° cogs and one 67.5°
cog. Horizontal positions and collisions remain absent from that master.

The complete source broadens this to one bracket each from **0/4, 2/6, 1/7,
3/5**, either insert **8/10**, and four independent choices among all eight
cog angles with at least one new profile. All nine original identities and
all 18 coordinates remain mandatory. **184** ordered collision cases, including
64 exact reused cases, yield **744** physical modes over all 36 part pairs.
Independent reconstruction checks **412,352** triangle-pair hulls,
**6,716** guarded faces and **271,642** exact outside planes. It separately
proves all 64 spacing rectangles lie inside these actual source obstacles.

The shared-plane model includes **1,716** complete vertical-cell selectors,
42 profile-cell sums, 63 band inequalities and **390** uniform/phase-conditional
cog spacing bounds. The audit reconstructs every field, covers **1,704,720**
part/profile integer Y values and verifies **108,108** cell/band coefficients.
All four identical cog copies may be x-sorted together with their angle
choices: **97,920** phase/order cases verify that no separate phase ordering
was introduced. No unstrengthened model is called.

The **233,563-variable / 240,227-constraint** call returns UNKNOWN.

## Relative-height spacing implications

Cover the complete relative-Y domain with **35** disjoint 2 mm bins. For every
ordered angle pair, intersect each bin with its complete source stock domain.
Independently certify **2,191** whole forbidden rectangles, covering
**4,262,736** pair-relative integer Y values and checking 15,982 boundary
samples. Whole-rectangle containment is the proof; sampled minima alone are
not treated as proof. Minimum boundary margin is **0.000158 mm**.

**2,119** bounds improve on uniform spacing, by up to **23.002 mm**. Add 210
relative-bin flags, six exact-one sums and **13,146** valid conditional spacing
inequalities. Exact parent restoration and unique witness extension verify
that all original source coordinate/angle choices remain represented.
The **233,773-variable / 253,589-constraint** call also returns UNKNOWN.

| Call | Result | Solver seconds | Shared seconds | Soft overrun |
|---|---|---:|---:|---:|
{table}

All **three** calls are closed. The coordinate calls exceed their 45-second
soft limits by **0.256623** and **0.249901 seconds**, respectively, while both
remain inside the declared 60-second shared budget. The necessary master uses
20 / 30 seconds. No watchdog, restart, reseed or extension occurs. All **10**
independent audits pass; neither UNKNOWN supports a profile-family exclusion.

## Preserved preparation failures and next step

A generated duplicate quote causes a screen helper to fail parsing before
geometry or solver work. Its original is preserved before the one-character
repair. The first independent screen audit then stops because a stock-bounds
variable shadows a newly imported rectangle constructor. Its partial output
and helper are retained. A separate corrected audit reconstructs all 64 cases
from scratch into a new directory. No solver call occurs in either failure.

Read-only model inspection attributes **148,074** shared planes to cog/cog
pairs and **83,713** to other pairs. Next investigate a smaller sufficient
cog-pair formulation using certified upper bounds on the whole forbidden
boundary within complete relative-Y bins. Prove full-domain separation before
considering any new bounded call. This changes conservative geometry: a
negative would not exclude the present complete source family. Both current
large calls remain closed, and no balanced-family exclusion may be added.

All **66** originals remain required: 55 checked first-sheet originals,
nine short-sheet IDs **21/22/25/26/37/53/63/64/65**, and pending first-sheet
brackets **28/29**. Full original/native/material validation, production
integration under 60 seconds and the complete H5 matrix remain open.

At **{review['utc']}**, queued checkpoint **6927ae7d** descends from main
**50cdc07e**, whose [CI run](https://github.com/skulitom/Nestbolt/actions/runs/40284102018)
has all six jobs successful. Commit this checkpoint and normally push both
after staged-byte and ancestry verification. Production, READMEs and upstream
stop-rule state are unchanged. H2 retains its original gate; all 22 reserved
vectors remain untouched. No new release is qualified.

[Checks]({NAME}/checks.json), [closed calls]({NAME}/closed-calls.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). All {archive['archive_members']:,} canonical
files and {archive['verified_aliases']:,} aliases are byte/SHA-256/CRC checked
across {archive['archive_parts']} archive parts.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''

**N4 eight-phase geometry and relative-height spacing, 2026-10-26:** [the evidence]({link})
adds six exact original cog rotations, sampling one tooth period at 2.25-degree
steps. All 64 ordered cog pairs and 184 balanced-family source cases verify;
the full source retains 744 physical orientation modes. A 909-variable necessary
capacity allocation is positive. Complete band links and proven spacing give
a 233,563-variable source model; 2,191 additional full-domain rectangle proofs
add relative-height spacing, reaching 233,773 variables. Both bounded coordinate
calls return UNKNOWN. All 10 audits pass and all three calls close within shared
budgets; the two coordinate soft overruns (0.256623 / 0.249901 seconds) and two
preparation failures with separate recoveries are preserved. No new exclusion
follows. Next investigate a compact sufficient cog-pair representation with
full-domain separation proof; current large calls remain closed. All 66 originals
and full H5 validation remain required. Main 50cdc07e passes all six checks,
allowing queued 6927ae7d and this checkpoint to be pushed normally after review.
H2/H5 remain open at 60%; production, READMEs, releases and 22 reserved vectors
remain unchanged.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
