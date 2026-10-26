"""Seal changed-composition capacity and complete eight-part orientation diagnostics."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-eight-part-composition-and-orientations-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'nine_model':'h5-nine-part-band-model-20261026','nine_search':'h5-nine-part-band-search-20261026','eight_model':'h5-eight-part-band-model-20261026','eight_search':'h5-eight-part-band-search-20261026','fixed_source':'h5-eight-part-strip-source-20261026','failed_preflight':'h5-eight-part-strip-probe-20261026','fixed_probe':'h5-eight-part-strip-probe-repaired-20261026','all_source':'h5-all-bracket-strip-source-20261026','all_probe':'h5-all-bracket-strip-probe-20261026','shared_probe':'h5-shared-bracket-strip-probe-20261026','review':'h5-eight-part-checkpoint-review-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,v):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(v)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='81cc41866306a639fa09f0db9590bb411c0c987e' and review['main_head']==review['source_head'];assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('nine_model','audit/checks.json'),('nine_search','audit/checks.json'),('eight_model','audit/checks.json'),('eight_search','audit/checks.json'),('fixed_source','audit-repaired/checks.json'),('fixed_probe','model-audit/checks.json'),('fixed_probe','response-audit/checks.json'),('all_source','audit/checks.json'),('all_probe','model-audit/checks.json'),('all_probe','response-audit/checks.json'),('shared_probe','model-audit/checks.json'),('shared_probe','response-audit/checks.json')]
assert len(audits)==12 and all(load(base[k]/n)['passed'] for k,n in audits)
calls=[{'name':k,**load(base[k]/('result.json' if k.endswith('search') else 'search/000/result.json')),'process':load(base[k]/('process.json' if k.endswith('search') else 'search/process.json'))} for k in ['nine_search','eight_search','fixed_probe','all_probe','shared_probe']]
assert [r['status'] for r in calls]==['INFEASIBLE','OPTIMAL','INFEASIBLE','UNKNOWN','UNKNOWN']
assert all(r['solver_calls']==1 and r['process']['exit_code']==0 and not r['process']['timeout'] and r['process']['seconds']<= (30 if r['name'].endswith('search') else 60) for r in calls)
assert sum(len(list(base[k].rglob('opened.json'))) for k in ['nine_search','eight_search','fixed_probe','all_probe','shared_probe'])==5
assert not list(base['failed_preflight'].rglob('opened.json')) and load(base['failed_preflight']/'preflight-failure.json')['solver_calls']==0
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
write(OUT/'closed-calls.json',{'calls':calls,'closed_calls':5,'all_shared_budgets_honored':True,'unchanged_call_retries':0,'full_target_witness':False})
for k,n,dest in [('eight_search','audit/verified-allocation.json','necessary-eight-allocation.json'),('fixed_probe','inventory.json','fixed-orientation-inventory.json'),('all_probe','prepared.json','all-orientation-model.json'),('shared_probe','prepared.json','shared-plane-model.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-81cc4186-snapshot.json'),('failed_preflight','preflight-failure.json','retained-preflight-failure.json')]:shutil.copyfile(base[k]/n,OUT/dest)
next_action='All five diagnostic calls are CLOSED. Do not extend or reseed them. The nine-part necessary band model is negative only at the recorded source profiles/grid. The eight-part band allocation is necessary only; its selected profile5/5/6/7/9/9/9/9 coordinate model is negative. All bracket orientations remain unresolved after both audited equivalent source formulations returned UNKNOWN. No original is dropped: checked first-sheet55, second-sheet8 IDs21/22/25/26/53/63/64/65, first-sheet pending28/29/37. Next examine allowed cog rotations geometrically before another coordinate search: calculate original support widths/vertical clearances over the allowed free rotation range and justify a finite changed orientation family from that geometry. Any new profiles need original reconstruction and guarded collision/capacity audits; current-angle negatives do not transfer. If changed cog angles offer no material room, investigate a genuinely different whole-job sheet composition rather than prolonging these calls. Complete66-original/native/material validation, production-budget integration and full13-job/two-kerf/three-seed H5 matrix remain required. H2 original gate stays open;22 reserved vectors untouched. Main81cc4186 CI40273506020 has five jobs passed and one live in the saved checkpoint; preserve that run before pushing this commit normally.'
write(OUT/'next-step.json',{'action':next_action,'next_call_opened':False,'pending_first_sheet_originals':[28,29,37],'mandatory_second_sheet_originals':[21,22,25,26,53,63,64,65],'H5_complete':False})
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
for n in ['h5-second-strip-capacity-and-insert-exchange-20261026','h5-thirteen-part-selection-and-sheet-exclusion-20261026','h5-seven-part-obstruction-and-broader-source-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
p=ROOT/'output/h5-coordinated-placement-selection-20261018/job.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*nine_part*.py','*eight_part*.py','*all_bracket_strip*.py','*shared_bracket_strip*.py'] for p in (ROOT/'output').glob(pat)]+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':12,'closed_solver_calls':5,'failed_preflight_solver_calls':0,'all_shared_budgets_honored':True,'all66_original_identity_obligations_preserved':True,'shared_plane_equivalence_verified':True,'repeated_flags_removed':55298,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: changed composition and all bracket orientations — 2026-10-26

**The eight-part short-sheet inventory passes a necessary capacity test, but
has no verified placement. One fixed orientation pattern is excluded; all
allowed bracket orientations remain unresolved after two equivalent bounded
searches. H2/H5 remain open at 60% completed milestone weight.**

## Original-part accounting

Keep the previously verified first-sheet exchange: insert36 occupies cog53's
old position. All55 first-sheet originals remain checked. The nine-part
second-sheet composition has originals21/22/25/26/37/53/63/64/65. Changing only
the insert count from two to one in the exact673-variable/66-constraint band
model returns **INFEASIBLE**, in0.136694 solver /0.851925 shared seconds.
Every coefficient and63 capacity rows remain unchanged and parent restoration
is independently verified. This is a scoped solver result; the earlier
ten-part continuous certificate is not transferred to these new counts.

Next require insert37 on the first sheet as well. The second-sheet originals
are **21/22/25/26/53/63/64/65**: four brackets and four cogs. The55 checked
first-sheet originals plus these eight and the pending first-sheet originals
**28/29/37** account for all66 identities exactly once. None is dropped and no
first-sheet position is asserted for the pending three.

Changing only the necessary model's insert count/bounds from one to zero
returns **OPTIMAL**, in0.060929 solver /0.747618 shared seconds. Independent
readback checks all673 values,66 constraints, family totals and63 band loads.
The selected bracket profiles are5/5/6/7, with four cogs at the recorded angle.
This allocation ignores horizontal collisions and is not a layout.

## Full coordinate checks

The selected profiles define one fresh eight-original model with all16
coordinates free throughout the guarded short stock. Band cells are not locks
or hints. All28 physical pairs are retained. Independent geometry checks
reconstruct four original profiles, eight collision cases from7,084 unmerged
triangle-pair hulls,162 guarded faces and6,960 outside planes. Complete model
and real import audits pass for6,296 variables /6,431 constraints. Its sole
call returns **INFEASIBLE**, in1.823040 solver /2.580368 shared seconds.

A preflight script mistakenly compared the45-second solver budget with the
28-pair count. That audit and its downstream preparation failures are retained;
**zero solver calls opened**. The corrected audit and model use separate paths.
Geometry, identities and the declared budget did not change. The source plan
also retains a superseded historical description; its explicit new inventory
and typed parameters define the eight-part experiment and are checked exactly.

The broader model permits **all eight bracket quarter-turn/mirror choices**
independently, retaining the current cog angle. All73 collision cases are
independently rebuilt from9,604 triangle-pair hulls, with472 guarded faces and
24,986 outside planes. Minimum source guard0.2126mm exceeds the required
native0.211709mm. The model includes all518 orientation modes across28 pairs.
Sorting identical bracket copies by profile and cog copies by x coordinate
preserves feasibility by relabelling the same original family geometry.

The entire95,748-variable/97,636-constraint model and actual import pass
independent reconstruction. Its45-second call returns **UNKNOWN**, taking
45.147155 solver /46.628652 shared seconds. The0.147155-second soft overrun is
recorded; the shared60-second budget passes. UNKNOWN excludes no placement.

## Equivalent reduction of repeated constraints

A distinct formulation shares identical physical pair-plane literals across
orientation modes. It removes **55,298 repeated flags**, reducing the model to
**40,450 variables /42,338 constraints**. It preserves all48 coordinate/profile
variables,74 count/stock/symmetry constraints and1,862 face disjunctions.

An independent audit checks every one of95,700 edge projections onto40,402
shared planes, exact inactive-mode escape literals, complete model fields and
actual import. Equivalence holds in both directions: old feasible coordinates
can set each shared flag to its plane truth; shared flags can be copied back
to every corresponding old edge flag without losing a required face clause.

Its separately bounded call also returns **UNKNOWN**, in45.114145 solver /
46.029010 shared seconds, retaining the0.114145-second soft overrun. This is a
smaller equivalent diagnostic model, with no demonstrated packing improvement.

## Remaining work and repository

All five calls are closed. Next examine permitted cog rotations and their
original geometric support widths before choosing a different placement
formulation. Current-angle exclusions do not transfer to another angle or to
the complete job. All66 originals, native/material validation, production-budget
integration and the full13-job/two-kerf/three-seed H5 matrix remain required.

At {review['utc']}, main81cc4186 has **five passed checks and one still live**
in [CI40273506020](https://github.com/skulitom/Nestbolt/actions/runs/40273506020).
Preserve that run before the next normal push. Production source, accurate
READMEs, upstream heads/releases and all22 reserved H2 vectors remain unchanged.
No new release is qualified.

[Checks]({NAME}/checks.json), [closed calls]({NAME}/closed-calls.json),
[next step]({NAME}/next-step.json), [raw manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']:,} canonical files and {archive['verified_aliases']:,}
aliases are byte/SHA-256/CRC verified across {archive['archive_parts']} archive parts.
'''
(ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
note='''

**N4 changed composition and bracket orientations, 2026-10-26:** [the evidence]({link})
checks the nine-part necessary band model (INFEASIBLE), then the eight-part
allocation (OPTIMAL). The latter is not a placement: its chosen bracket pattern
is excluded by a full guarded coordinate model. A broader model includes all
eight approved bracket orientations and518 pair modes; its single bounded call
is UNKNOWN. Independently verified sharing of repeated pair planes reduces
95,748 variables/97,636 constraints to40,450/42,338 without changing feasible
coordinates, but its separate bounded call is also UNKNOWN. All five calls are
closed; all shared budgets pass and both soft overruns remain recorded. A
preflight audit typo and downstream failures are preserved with zero opened
solver calls. All66 identities remain mandatory:55 checked first-sheet originals,
eight second-sheet originals and pending first-sheet28/29/37. Next inspect
allowed cog rotations geometrically; no full layout or global impossibility is
claimed. Main81cc4186 CI40273506020 has five checks passed and one live at05:38UTC.
H2/H5 stay open at60%; production, READMEs, releases and22 reserved vectors remain
unchanged. No new release is qualified.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
