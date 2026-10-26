"""Seal sufficient compact cog geometry and its sole closed bounded search."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-compact-cog-bin-planes-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'flat':'h5-compact-cog-bin-guards-20261026','slopes':'h5-compact-cog-bin-planes-20261026','probe':'h5-compact-cog-plane-probe-20261026','cost':'h5-compact-cog-remaining-cost-20261026','review':'h5-compact-cog-checkpoint-review-20261026','previous_sync':'h5-eight-phase-main-sync-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']==review['main_head']=='7271cc8beb5caae3a3dced77d129ffcdcb1ec7ed'
assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
assert review['main_ci_id']==40290567078 and review['main_ci_status']=='in_progress' and review['main_ci_successful_jobs']==3
audits=[('flat','audit/checks.json'),('slopes','audit/checks.json'),('probe','model-audit/checks.json'),('probe','response-audit/checks.json')];assert all(load(base[k]/n)['passed'] for k,n in audits)
r=load(base['probe']/'search/000/result.json');process=load(base['probe']/'search/process.json');assert r['status']=='UNKNOWN' and process['exit_code']==0 and not process['timeout'] and process['seconds']<=60 and len(list(base['probe'].rglob('opened.json')))==1
assert not list(base['flat'].rglob('opened.json')) and not list(base['slopes'].rglob('opened.json'))
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
copies=[('flat','result.json','flat-guard-summary.json'),('flat','audit/implication.json','flat-source-implication.json'),('slopes','result.json','sloping-guard-summary.json'),('slopes','audit/implication.json','sloping-source-implication.json'),('probe','inventory.json','compact-model.json'),('probe','model-audit/implication.json','model-source-implication.json'),('cost','cost.json','remaining-model-cost.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-7271cc8b-in-progress.json'),('previous_sync','receipt.json','previous-main-sync.json')]
for k,n,d in copies:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'closed-call.json',{'closed':True,'solver_calls':1,'status':r['status'],'solver_seconds':r['seconds'],'shared_seconds':process['seconds'],'solver_limit_seconds':45,'shared_limit_seconds':60,'soft_overrun_seconds':r['solver_soft_overshoot_seconds'],'shared_budget_honored':True,'full_target_witness':False,'exclusion_inferred':False})
cost=load(base['cost']/'cost.json');next_step=cost['next_work']+' The current85699-variable/103151-constraint compact call is CLOSED UNKNOWN with a1.077775second soft overrun and47.517578seconds shared elapsed. Do not restart/reseed/extend it. All2191 cog-bin guard records and2407 undominated sloping requirements are independently proved sufficient for the original source face clauses. Their flat-bound variant was never modelled or called. The proposed next two-direction reduction targets59376 bracket/cog and20328 insert/cog shared planes, retaining2198 bracket/bracket and1811 bracket/insert planes. Complete interval/profile coverage and full original-source implication must be independently audited. Do not assume a fixed x order for nonidentical shapes. All66 original identities still require full placement:55 checked on first stock, nine second-sheet originals21/22/25/26/37/53/63/64/65, pending first-sheet brackets28/29. Full native/material checks, production integration under60seconds and the complete H5 matrix remain required. Main7271cc8b CI40290567078 has3successful jobs and3in progress at the recorded review. Queue this checkpoint until that live run succeeds, then push normally after verifying ancestry. No new production/quality/release claim. H2 remains open under its unchanged gate; all22 reserved vectors untouched.'
write(OUT/'next-step.json',{'action':next_step,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60})
write(OUT/'scope.json',{'compact_witness_implies_full_source':True,'reverse_implication_claimed':False,'negative_excludes_full_source_family':False,'actual_result':'UNKNOWN','full_target_witness':False,'all66_originals_required':True})
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
for n in ['h5-eight-phase-geometry-and-spacing-20261026','h5-two-phase-band-and-spacing-exclusions-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pattern in ['*compact_cog*.py','*compact_checkpoint*.py'] for p in (ROOT/'output').glob(pattern)]+[Path(__file__),ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':4,'closed_solver_calls':1,'terminal_status':'UNKNOWN','shared_budget_honored':True,'soft_overrun_seconds':r['solver_soft_overshoot_seconds'],'flat_guard_solver_calls':0,'source_face_implications_proved':150952,'retained_sloping_requirements':2407,'removed_auxiliary_variables':148074,'compact_variables':85699,'compact_constraints':103151,'original_source_forward_implication_verified':True,'reverse_equivalence_claimed':False,'new_profile_family_exclusions':0,'all66_original_identity_obligations_preserved':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: compact cog bin planes — 2026-10-26

**A verified sufficient cog-pair representation removes 148,074 auxiliary
variables while preserving the implication to every original source collision
clause. Its sole bounded search remains UNKNOWN. No full-source exclusion or
H5 acceptance follows; H2/H5 remain open at 60% completed milestone weight.**

## Whole-bin source proof

The previous complete model contains 231,787 shared planes, of which 148,074
belong to cog/cog pairs. All four cogs share the same eight allowed angles and
can be x-sorted with their profile choices. Use their complete relative-Y
domain, partitioned into 35 disjoint 2 mm integer bins.

For each of the **2,191** nonempty ordered-profile/bin intersections, choose
an actual rounded outside-plane edge for every source convex-face clause.
Positive-X edges give an exact integer lower-X threshold. Other edges are
usable without restriction only if they hold on the full stock-difference
rectangle. Taking the largest per-face threshold gives a sufficient right
rectangle. The independent audit checks all **150,952** face proofs at
**603,808** exact corners, plus whole-rectangle separation from the original
guarded collision geometry. No flat-bound model or solver call is created.

Flattening every edge over its bin would waste room. Retain its sloping source
inequality instead. Exact normalized-line comparisons at both Y endpoints
prove dominance throughout the interval. Remove only lines dominated by
another retained line, preserving a named implication for every source face.
Independent rational arithmetic checks all records. **44,588** unique positive
source edges reduce to **2,407** sloping requirements, with at most three per
profile/bin. **106,089** face edges already hold throughout their full stock
rectangle. Every one of the 150,952 face implications is accounted for.

These constraints are sufficient for the original source clauses. The reverse
implication is not proved: choosing one edge across a whole bin may exclude
some original source points. Even an INFEASIBLE result could therefore exclude
only this compact construction, not the complete eight-angle source family.

## Complete compact model audit

Remove exactly **148,074** cog-only plane flags and their implications, and
**3,660** corresponding face OR clauses. Independently reconstruct the exact
removed constraints as multisets. Retain all other **85,489** parent variables
and **88,493** parent constraints with exact index remapping and field equality.
All original coordinates, angle choices, stock bounds, mandatory counts, cog
ordering, non-cog pair clauses, vertical cells, area limits and existing
spacing bounds remain.

Add **210** complete relative-bin selectors, six exact-one sums and **14,442**
conditional sloping constraints across the six physical cog pairs. The final
model has **85,699 variables / 103,151 constraints**, compared with the full
source's 233,563 / 240,227. All **744** source orientation modes remain covered:
360 by retained source clauses and 384 by proved compact cog implications.
No coordinate is fixed, original omitted, angle separately ordered or hint added.

The full model is independently reconstructed and checked through actual solver
import/export. Every compact witness can extend to the full original source
model by assigning removed plane flags from plane truth. A positive would still
require independent original geometry and full-job validation.

## Closed search and next reduction

The sole 45-second, four-worker, seed-0 call returns **UNKNOWN** after
**{r['seconds']:.6f} solver seconds**, with **{process['seconds']:.6f} shared seconds**.
The **{r['solver_soft_overshoot_seconds']:.6f}-second soft overrun** is preserved;
the declared 60-second shared budget is honored. No watchdog termination,
restart, reseed, extension or profile-family exclusion occurs. All four audits
pass. Earlier full-source UNKNOWN calls also remain closed and inconclusive.

Read-only inspection identifies the remaining shared planes:

| Pair type | Shared planes | Physical modes |
|---|---:|---:|
| bracket / bracket | 2,198 | 24 |
| bracket / insert | 1,811 | 16 |
| bracket / cog | 59,376 | 256 |
| insert / cog | 20,328 | 64 |

Next investigate compact bracket/cog and insert/cog requirements with complete
relative-Y bins and **both left/right alternatives**. Those nonidentical parts
cannot be assigned a fixed x order. Derive actual source difference boxes,
prove every chosen directional edge over its full bin, retain sloping planes,
and prune only exactly dominated lines. Keep bracket/bracket and bracket/insert
clauses. No new solve is justified until full coverage and the original-source
implication independently pass. Negative scope remains conservative and narrow.

All **66** originals remain required: 55 checked first-sheet originals,
nine short-sheet IDs **21/22/25/26/37/53/63/64/65**, and pending first-sheet
brackets **28/29**. Full native/material validation, production integration
under 60 seconds and the complete H5 matrix remain open.

At **{review['utc']}**, main and local HEAD are **7271cc8b**. Its
[CI run](https://github.com/skulitom/Nestbolt/actions/runs/40290567078) has three
successful jobs and three still running. The prior two checkpoints were pushed
normally after all six checks on their previous main passed. Commit and queue
this checkpoint until the current live run succeeds, without cancelling it.
Production, READMEs and upstream stop-rule state remain unchanged. H2 retains
its original gate; all 22 reserved vectors remain untouched. No new release
is qualified.

[Checks]({NAME}/checks.json), [closed call]({NAME}/closed-call.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). All {archive['archive_members']:,} canonical
files and {archive['verified_aliases']:,} aliases are byte/SHA-256/CRC checked
across {archive['archive_parts']} archive parts.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''

**N4 compact cog bin planes, 2026-10-26:** [the evidence]({link})
proves 150,952 original source-face implications across 2,191 complete cog
profile/relative-Y bins. Exact dominance reduces 44,588 positive source edges
to 2,407 sloping requirements. The compact model removes 148,074 auxiliary
variables while retaining every other parent field exactly; its 85,699-variable /
103,151-constraint model implies the full source on a positive. Reverse
equivalence is not claimed. Its sole bounded call is UNKNOWN at 46.077775 solver /
47.517578 shared seconds; the 1.077775-second soft overrun is preserved. All four
audits pass; no full-source exclusion follows. Next investigate both directional
alternatives for bracket/cog and insert/cog pairs with independent full-bin
proofs. All 66 originals and full H5 validation remain required. Main 7271cc8b
has three successful CI jobs and three running, so queue this checkpoint for a
later normal push. H2/H5 remain open at 60%; production, READMEs, releases and
all 22 reserved vectors remain unchanged.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
