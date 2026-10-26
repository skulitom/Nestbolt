"""Seal exact count exclusion and an original-geometry eight-part short sheet."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-short-sheet-count-bound-and-original-eight-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'stem':'h5-stem-ordered-nine-decision-20261026','partition':'h5-core-count-partition-20261026','bands':'h5-last-count-bands-20261026','sequence':'h5-core-sequence-bound-20261026','original':'h5-six-bracket-short-sheet-20261026','review':'h5-core-count-review-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==review['source_head']==review['main_head']=='9842e4c1d5953970a8698d7f9600a713f154554b';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
ci=json.loads(subprocess.check_output(['gh','run','view','40305808059','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT,text=True));assert ci['headSha']==head;write(base['review']/'main-ci-preseal.json',{'utc':datetime.now(timezone.utc).isoformat(),'ci':ci})
audits=[('stem','model-audit/checks.json'),('stem','response-audit/checks.json'),('partition','model-audit/checks.json')]+[('partition',f'case-{i:03d}/{kind}/checks.json') for i in range(4) for kind in ['model-audit','response-audit']]+[('bands','model-audit/checks.json'),('bands','response-audit/checks.json'),('sequence','audit/checks.json'),('original','checks.json'),('original','audit/checks.json')]
assert len(audits)==16 and all(load(base[k]/n)['passed'] for k,n in audits)
seq=load(base['sequence']/'audit/checks.json');orig=load(base['original']/'audit/checks.json');assert seq['all_four_count_cases_excluded'] and seq['checked55_maximum_short_count']==8 and orig['short_originals_verified']==8 and orig['mandatory_first_sheet_additions']==[63,64,65]
calls=[]
for key,sub,status in [('stem','','UNKNOWN'),('partition','case-000','INFEASIBLE'),('partition','case-001','INFEASIBLE'),('partition','case-002','UNKNOWN'),('partition','case-003','INFEASIBLE'),('bands','','UNKNOWN')]:
    folder=base[key]/sub;r=load(folder/'search/000/result.json');proc=load(folder/'search/process.json');inv=load(folder/'inventory.json')[0];assert r['status']==status and proc['exit_code']==0 and not proc['timeout'] and proc['seconds']<=30 and len(list((folder/'search').rglob('opened.json')))==1
    calls.append({'experiment':names[key]+('/'+sub if sub else ''),'status':status,'variables':inv['variables'],'constraints':inv['constraints'],'solver_seconds':r['seconds'],'shared_seconds':proc['seconds'],'solver_limit_seconds':20,'shared_limit_seconds':30,'soft_overrun_seconds':r['solver_soft_overshoot_seconds'],'closed':True,'full_target_witness':False})
OUT.mkdir()
for key,n in audits:shutil.copyfile(base[key]/n,OUT/(key+'-'+n.replace('/','-')))
for key,n,d in [('partition','model-audit/necessity-proof.json','core-partition-necessity.json'),('sequence','audit/necessity-proof.json','exact-count-bound-proof.json'),('sequence','pair-distance-bounds.json','necessary-pair-distances.json'),('sequence','audit/independent-forbidden-unions.json','independent-integer-forbidden-unions.json'),('sequence','states.json','forward-earliest-states.json'),('sequence','audit/backward-latest-states.json','backward-latest-states.json'),('original','partial63-placements.json','partial63-placements.json'),('original','short-sheet-placements.json','original-short-eight.json'),('original','mandatory-first-additions.json','mandatory-first-additions.json'),('review','review.json','source-review.json'),('review','main-ci-preseal.json','main-ci-preseal.json')]:shutil.copyfile(base[key]/n,OUT/d)
write(OUT/'closed-calls.json',calls)
write(OUT/'scope.json',{'checked55_continuation_maximum_short_parts':8,'original_short_eight_constructed':True,'first55_unchanged':True,'all66_originals_accounted_once':True,'originals_placed_on_both_sheets':63,'mandatory_first_sheet_additions':[63,64,65],'all_real_cog_angles_and_continuous_source_anchors_in_negative_proof':True,'six_bracket_two_cog_subset_excluded_at_same_short_target':True,'global_full66_infeasibility_claimed':False,'other_first_sheet_arrangements_unexcluded':True,'native_full_job_checked':False,'H5_complete':False})
next_action='All six bounded calls are CLOSED and must not be retried, reseeded or extended. The independently verified exact integer forward/backward projection excludes six brackets plus two cogs at this short-strip target. Together with the complete count partition, every checked55 continuation selects at most8 short-sheet parts. A new original-geometry strip constructs exactly8: brackets21/22/25/26/28/29,insert37,cog53; the unchanged checked55 plus these8 form a verified63-original partial. Cogs63/64/65 are mandatory first-sheet additions, all66 identities accounted for. Next examine original-geometry placement space for these three cogs against the saved first55, using necessary all-angle geometry to reject impossible fixed arrangements before any bounded source search. If fixed55 cannot accommodate them, explicitly release/rearrange first-sheet originals or evaluate other <=8-part family allocations; the new bound does not exclude other first arrangements. Never validate a partial as a complete native job. A full66 source layout must pass native geometry/material validation, then production integration under60seconds and the full H5 matrix. H2 retains the original gate and22 reserved vectors are untouched. Queue this checkpoint while main CI40305808059 is active; perform a normal push only after all six checks pass. No new release is qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
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
for n in ['h5-all-angle-continuous-composition-exclusion-20261026','h5-complete-composition-selection-and-support-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*h5_stem_order*.py','*h5_core_count*.py','*h5_core_sequence*.py','*h5_last_count*.py','*h5_six_bracket*.py'] for p in (ROOT/'output').glob(pat)]+[Path(__file__),ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
print({'archive_input_members':len(members)},flush=True);archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'audits_passed':16,'closed_solver_calls':6,'terminal_statuses':[r['status'] for r in calls],'all_shared_budgets_honored':True,'soft_overruns_seconds':[r['soft_overrun_seconds'] for r in calls],'exact_integer_pair_bounds':81,'guaranteed_y_rectangle_pairs':768,'forward_states':149,'forward_transitions':1159,'backward_states':149,'checked55_maximum_short_count':8,'original_short_eight_verified':True,'originals_placed':63,'remaining_first_sheet_cogs':[63,64,65],'all66_originals_required':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full66_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
table='\n'.join(f"| {r['experiment']} | {r['variables']:,} / {r['constraints']:,} | {r['status']} | {r['solver_seconds']:.6f} / {r['shared_seconds']:.6f} |" for r in calls)
passed=sum(j['conclusion']=='success' for j in ci['jobs']);report=f'''# H5: an eight-part short-sheet bound and original construction — 2026-10-26

**For the checked 55-part first-sheet arrangement, at most eight of the eleven
remaining originals can go on the target short sheet. A new original-geometry
construction achieves eight on that sheet. Three cogs still need first-sheet
positions, so there is no complete 66-part witness and H2/H5 remain open at 60%.**

## Complete count coverage

The stem-ordered nine-or-more decision replaces the five old bracket bounding-box
orders with stem ordering; its audit checks all retained fields and 46,080
presence/rank cases. Its sole call is UNKNOWN.

The existing all-angle four-bracket/four-cog exclusion leaves exactly four
families with nine or more short-sheet parts among the six brackets, one insert
and four cogs still required: **(5,1,3), (6,0,3), (6,1,2), (6,1,3)**, in
bracket/insert/cog order. Enumerate all 70 family allocations to prove coverage;
no part-dropping or rounded-area monotonicity assumption is used.

Each exact-count model retains the full 122-variable stem model and adds 52
optional horizontal intervals, one global no-overlap and three count equalities.
Bracket intervals represent their full-height stems. Cog intervals have width
245.034 mm. These cog intervals are propagation devices, not asserted subsets
of the source. Their separation from every other interval follows from the
retained stem ordering, six cog gaps and 192 original-support direction bounds.
Independent reconstruction and actual solver import/export pass for all cases.

Three exact cases are INFEASIBLE; **(6,1,2)** remains UNKNOWN. Restoring every
universal-angle vertical cell and band to that last case gives 2,422 variables
and 3,415 constraints, but its sole call is also UNKNOWN. The inverse-index
audit verifies all 2,300 restored variables and 2,417 restored constraints,
including 54 profile groups and 63 capacity rows. These UNKNOWN results are
preserved and do not themselves exclude anything.

| Experiment | Variables / constraints | Result | Solver / shared seconds |
|---|---:|---|---:|
{table}

All six calls are closed. Each had one declared 20-second solver / 30-second
shared limit, four workers and seed 0. All shared limits pass. Soft overruns
are recorded in [closed calls]({NAME}/closed-calls.json); no retries occurred.

## Independent exact exclusion of the last family

Omit the insert and keep six brackets plus two cogs. Use each bracket's stem
start and each cog's center as its horizontal coordinate. All are strictly
ordered in any valid source layout, by the previously proved support and
spacing bounds.

For each of the 64 ordered bracket profile pairs, compare all inset rectangle
pairs plus the verified full-height stems. **768 rectangle pairs overlap in Y
throughout the full allowed anchor ranges.** Each therefore contributes an
open forbidden X interval. Convert those intervals to closed integer sets,
merge them independently, and find the smallest permitted stem distance
starting at the first stem's width. Touching endpoints remain permitted.
Add original-support bracket/cog gaps and the cog/cog gap, giving **81** exact
necessary distance bounds across nine profile types.

A complete finite dynamic program records the earliest feasible coordinate
for each count/last-profile state. Earlier coordinates dominate later ones:
all retained constraints are lower differences and fixed coordinate domains.
It checks **149 reachable states and 1,159 transitions**, with no terminal
state containing six brackets and two cogs. An independently implemented
backward latest-coordinate program also has **149 states and no terminal**.
All forward records, transitions and witness prefixes are independently checked.

The projection omits the insert and all nonadjacent exclusions, so it is weaker
than the original packing problem. Its negative result excludes the six-bracket,
two-cog subset for this stock target at every real cog angle and continuous
source anchor, with conservative integer rounding already covered by the
source proxy proofs. Combined with the three audited exact-case negatives,
this proves **at most eight short-sheet parts for the checked55 continuation**.
It does not prove the full job impossible or exclude other first-sheet arrangements.

## An actual eight-part short sheet

Construct three mirrored quarter-turn bracket pairs, followed by one original
cog and one original insert, using 0.225 mm construction separation. The short
sheet contains original brackets **21/22/25/26/28/29**, insert **37** and cog **53**.
The prior first-sheet 55 placements remain exactly unchanged. Cogs **63/64/65**
are explicit mandatory first-sheet additions; all 66 identities are accounted for.

The resulting **63-part partial** passes **1,513 original filled-outer pair
checks and 252 stock-edge checks**. Its **87 cutouts and 9,426 cutout vertices**
are preserved. Minimum pair distance is 0.212500 mm against the required native
guarded distance of 0.211708673 mm; minimum extra stock margin is 0.012500 mm.
A separate auditor directly transforms every original vertex, verifies allowed
rotations/mirrors, cutout coordinates and areas, and repeats all pairs/edges.
The achieved short-sheet count matches the proved upper bound for this branch.
This is a useful different allocation, not a claim of more placed parts than
every earlier partial or a valid full-job result.

Next investigate original cog placement space on the first sheet. If the fixed
55 cannot accept three cogs, release/rearrange first-sheet parts or evaluate
other eight-part allocations. Full66 native/material validation, production
integration within 60 seconds and the complete H5 matrix remain required.

## Repository and evidence

Source review at **{review['utc']}** finds local HEAD and main at **9842e4c1**,
with unchanged production/README digests and upstream stop-rule state. At the
preseal check, [CI40305808059](https://github.com/skulitom/Nestbolt/actions/runs/40305808059)
has **{passed}/6 jobs passed**, overall **{ci['status']}**. Queue this checkpoint
until all six checks pass before a normal push. H2 retains its original gate;
the 22 reserved vectors remain untouched. No new release is qualified.

All **16 audits pass**. [Checks]({NAME}/checks.json),
[exact bound]({NAME}/exact-count-bound-proof.json),
[original short sheet]({NAME}/original-short-eight.json),
[partial63]({NAME}/partial63-placements.json), [scope]({NAME}/scope.json),
[next step]({NAME}/next-step.json), [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']:,} canonical files and
{archive['verified_aliases']:,} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note=f'''\n\n**N4 exact short-sheet count bound and original eight, 2026-10-26:** [the evidence]({{link}})
proves at most eight remaining parts can fit the target short sheet for the
checked55 continuation. Three of four exhaustive >=9 count cases are INFEASIBLE;
the remaining six-bracket/one-insert/two-cog case is excluded by an independent
exact horizontal projection, even with the insert omitted. All81 pair bounds,
768 guaranteed-Y rectangle pairs,149 forward states,1,159 transitions and149
backward states are verified. The six bounded solver calls are closed; all
shared limits pass and UNKNOWN results remain preserved. A new original
eight-part strip contains all six remaining brackets,insert37 and cog53.
Together with the unchanged first55, the63-part partial passes1,513 original
pairs,252 stock edges and preservation of87 cutouts/9,426 hole vertices.
Cogs63/64/65 remain mandatory first-sheet additions; all66 identities are
accounted for. This bound does not exclude other first-sheet arrangements.
All16 audits pass. Main9842e4c1 has{passed}/6 checks passed and is{ci['status']};
queue this checkpoint until CI succeeds. H2/H5 remain open at60%; production,
READMEs, releases and all22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
