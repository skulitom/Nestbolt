"""Seal the paired-strip source core and three distinct necessary capacity models."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-paired-strip-clearance-capacity-20261026';OUT=ROOT/'benchmarks/results'/NAME
CORE=ROOT/'output/h5-paired-strip-core-20261026';SUP=ROOT/'output/h5-paired-strip-support-domains-20261026';REF=ROOT/'output/h5-paired-strip-refined-domains-20261026';CAP=ROOT/'output/h5-paired-strip-capacity-cells-20261026';OB=ROOT/'output/h5-paired-strip-oblique-capacity-20261026';CLR=ROOT/'output/h5-paired-strip-clearance-capacity-20261026';SRC=ROOT/'output/h5-paired-strip-source-cell-proposals-20261026';OBSRC=ROOT/'output/h5-paired-strip-oblique-source-cell-proposals-20261026';SCREEN=ROOT/'output/h5-paired-strip-cog-space-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-staggered-frame-core-and-joint-contacts-20261026/source-review.json')
upstream_previous=load(ROOT/'benchmarks/results/h5-compact-joint-model-and-nine-insert-core-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head==main=='4e3b316c68b1db4ad5fb94358549ce1d844fa593'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40350260165','--json','databaseId,status,conclusion,headSha,jobs,url']))
assert ci['headSha']==main and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==upstream_previous[k] for k in upstream)
audits={'core-builder':CORE/'checks.json','core-independent':CORE/'audit/checks.json','support-domains':SUP/'audit/checks.json','refined-domains':REF/'audit/checks.json','capacity-cells':CAP/'audit/checks.json','capacity-model':CAP/'model/checks.json','capacity-response':CAP/'response-audit/checks.json','source-samples':SRC/'audit/checks.json','oblique-cuts':OB/'audit/checks.json','oblique-model':OB/'model/checks.json','oblique-response':OB/'response-audit/checks.json','oblique-source-samples':OBSRC/'audit/checks.json','clearance-cuts':CLR/'audit/checks.json','clearance-model':CLR/'model/checks.json','clearance-response':CLR/'response-audit/checks.json'}
assert len(audits)==15 and all(load(p)['passed'] for p in audits.values())
core=load(audits['core-independent']);assert core['originals_verified']==49 and core['remaining_first_filled_demand_reduction_mm2']==219000 and core['all66_originals_accounted_once']
calls=[load(folder/'search/result.json') for folder in [CAP,OB,CLR]]
assert [r['status'] for r in calls]==['OPTIMAL','OPTIMAL','UNKNOWN'] and all(r['closed'] and r['solver_calls']==1 for r in calls)
assert load(SRC/'result.json')['empty_cell_groups']==[2,12] and load(OBSRC/'result.json')['empty_cell_groups']==[2]
assert not load(SRC/'result.json')['solver_eligible'] and not load(OBSRC/'result.json')['solver_eligible']
OUT.mkdir()
for label,p in audits.items():shutil.copyfile(p,OUT/(label+'-checks.json'))
for p,name in [(CORE/'placements.json','core49-placements.json'),(CORE/'visual/core.png','core.png'),(CORE/'audit/next-neighborhood.json','next-fixed34-neighborhood.json'),(CLR/'audit/necessity-proof.json','clearance-necessity-proof.json'),(CLR/'new-excluded-cells.json','five-new-clearance-exclusions.json'),(CLR/'search/result.json','closed-clearance-call-result.json'),(CLR/'search/process.json','closed-clearance-call-process.json'),(CLR/'search/solver.log','closed-clearance-call-solver.log'),(CLR/'response-audit/worker-stats.json','clearance-worker-stats.json')]:shutil.copyfile(p,OUT/name)
write(OUT/'main-ci-4e3b316c-passed.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'upstream_rechecked_this_seal':True,'main_ci':40350260165,'main_ci_successful_jobs':6,'normal_checkpoint_push_allowed':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
next_action='Keep the source-verified paired-strip49 core as an alternative, with34 originals fixed on the first sheet and15 unchanged on the short sheet. All15 original cogs51..65 and both inserts48/49 remain mandatory. The three capacity models and both source samplers are CLOSED: no unchanged retry, reseed, extension or selected-cell resampling. The first two necessary positives are not source layouts; their finite source samples have empty mandatory groups. The strongest model additionally enforces required-clearance union exclusions and closes UNKNOWN after search, so neither existence nor impossibility is proved. Future work must materially change the formulation or core. A joint continuous model including both inserts and original cog geometry, or a stronger independently certified geometric separation/capacity argument, must preserve the complete current-owner domain coverage and exact quantities. Do not transfer older owner domains to this core or treat sampling failures as all-angle exclusions. Preserve the earlier64 partial. Full66 source/native/material validation, integration in the production60-second budget and the completeH5 matrix remain required. Main4e3b316c now passes all six checks, so this checkpoint may be pushed normally after exact staging and ancestry checks. H2 retains the original gate,22 reserved vectors remain untouched, and no new release is qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'fixed_first_originals':34,'fixed_short_originals':15,'core_originals':49,'mandatory_moving_counts':{'insert':2,'cog':15},'all66_originals_required':True,'remaining_first_filled_demand_reduction_mm2':219000,'highest_fixed_first_y_mm':2528.325,'earlier64_partial_preserved':True,'cell_models_are_necessary_only':True,'continuous_positions_and_all_angles_covered':True,'source_samples_are_finite_only':True,'closed_solver_statuses':[r['status'] for r in calls],'unrestricted_neighborhood_excluded':False,'part_in_hole_used':False,'full66_target_witness':False,'H5_complete':False})
members={};inputs={}
for folder in [CORE,SUP,REF,CAP,OB,CLR,SRC,OBSRC,SCREEN]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
helpers=list((ROOT/'output').glob('*h5_paired_strip*.py'))+[ROOT/'output/prepare_h5_oblique_source_readback.py',ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p
    for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members)
checks={'passed':True,'audits_passed':15,'failed_checker_attempts':0,'finite_source_preflight_failures_preserved':2,'core_originals':49,'same_sheet_pairs':666,'stock_edges':196,'cutouts':73,'cutout_vertices':6782,'filled_demand_reduction_mm2':219000,'current_source_rectangles':46,'refined_domains':54,'capacity_cells':1111,'capacity_conflicts':127947,'capacity_cliques':1815,'oblique_exclusions':61,'additional_clearance_exclusions':5,'retained_capacity_cells':1045,'exact_clearance_union_atoms':833,'merged_clearance_rectangles':24,'source_sample_events_checked':9828,'closed_solver_calls':3,'closed_statuses':[r['status'] for r in calls],'final_status':'UNKNOWN','final_returned_solve_seconds':calls[-1]['returned_solve_seconds'],'final_shared_process_seconds':load(CLR/'search/process.json')['seconds'],'final_returned_soft_overrun_seconds':calls[-1]['returned_soft_overrun_seconds'],'full66_target_witness':False,'production_and_readmes_unchanged':True,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive}
write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: paired bracket strip and required-clearance capacity — 2026-10-26

**A different checked core places all twelve brackets and nineteen of twenty-one
inserts alongside the eighteen frames.** It accounts for 49 originals across
the two sheets, leaving both inserts and all fifteen cogs mandatory. The strongest
necessary capacity test closes UNKNOWN; there is no complete layout or H5 pass.
H2/H5 remain open at 60% by completed milestone weights.

## Source construction

Preserve the fifteen short-sheet originals. Keep twelve turned frames in the
first three columns and the two adjacent upper unturned frames. Space the fourth
column at 670.675 mm, opening three gaps that each contain two bracket feet and
two inserts. Opposite bracket stems occupy the narrow side strip. Four vertical
inserts fill the opening beside the upper frames. The first sheet now fixes
eighteen frames, six brackets and ten inserts; its highest insert reaches
2,528.325 mm. This taller shape changes the remaining space.

Independent direct-vertex readback verifies **666 filled-outer pairs, 196 stock
edges, 73 cutouts and 6,782 cutout vertices**. Minimum pair clearance is 0.225 mm
against 0.211708673 mm required for native tolerance, with 0.025 mm extra stock
margin. The short sheet is unchanged. All 66 quantities are accounted once and
holes remain reserved. Remaining first-sheet filled demand decreases by
219,000 mm² relative to the preceding staggered core. This is a different starting
arrangement, not an improvement over the preserved 64-original partial count.

![Checked paired-strip core]({NAME}/core.png)

## Complete necessary domains

Fresh exact bounds cover every continuous cog center and every original rotation
against the 34 current fixed owners. Forty-six source-contained rectangles pass
184 exact corner checks and 736 interval edge checks. All-angle support exclusions
leave 188 closed grid cells. Refinement against 1,874 fresh fixed source points
retains 325 atoms, merged without gaps into **54 domains** covering
489,155.167020 mm². Unresolved regions remain included.

Split these domains on a 25 mm grid into **1,111 occupancy cells**. The previously
verified all-angle cog separation gives a conservative floor-rounded separation
of 254.297 mm, greater than every cell diameter. Each cell can therefore hold at
most one center. Two cells conflict only if even their farthest corners cannot
meet that separation. Independent enumeration verifies all 616,605 pairs,
**127,947 conflicts** and their complete coverage by **1,815 cliques**. The model
requires fifteen occupied cells. Both inserts are relaxed for this necessary
test only; they remain required for a full layout.

## Three distinct models, each called once

| Necessary model | Added exclusions | Constraints | Status | Returned / shared seconds |
| --- | ---: | ---: | --- | ---: |
| Complete occupancy graph | 0 | 1,816 | OPTIMAL, necessary positive only | 1.220399 / 1.995181 |
| Exact oblique support cuts | 61 | 1,817 | OPTIMAL, necessary positive only | 0.982586 / 1.754775 |
| Required-clearance union cuts | 5 more | 1,818 | UNKNOWN | 20.026862 / 20.772295 |

Every model retains the same 1,111 variables and all fifteen required cogs.
The added models are exactly the independently checked parent plus one zero-sum
exclusion row each, without objectives or hints. All three calls are closed;
there was no retry, reseed or extension. Each had a 20-second solver allowance
inside a 30-second shared-process allowance. The final solver's internal time
was 20.022295 seconds; its internal and returned soft overruns of 0.022295 and
0.026862 seconds are recorded. The shared limit was honored.

The final call advances beyond presolve. Worker branch counts are 17,072 for
`default_lp`, 41,452 for `max_lp` and 279,521 for `no_lp`; the returned response
contains the first worker's 855 conflicts. UNKNOWN proves neither a feasible
selection nor impossibility. No formal unsat certificate is claimed.

## Source samples and exact clearance proof

The first two necessary selections each receive a finite source preflight:
a 3 × 3 grid per cell and 36 actual angles from 0 to 17.5 degrees, plus 54 insert
proposals. No exact rotational symmetry is assumed. Independent readback checks
all **9,828 events**. Two mandatory cog groups are empty in the first preflight,
and one is empty in the second. Consequently no joint source solver is opened.
These sample failures are not continuous-position or all-angle exclusions.

The subsequent cuts instead use separate exact geometric proofs. Twenty-eight
rational unit normals bound an original support vertex for every rotation;
1,288 floor-safe boxes and the original inscribed disk exclude 61 whole cells.
This includes both troublesome cells from the first preflight, independently
of the sampled angles.

The final strengthening uses the original **0.2 mm required clearance**. Expand
each source-contained rectangle by 140 micrometres per axis. Every added point
is within sqrt(2) × 140 < 200 micrometres of actual fixed material, so a moving
part cannot enter it. Exact partitioning gives **833 closed union atoms**, merged
into **24 rectangles** with complete equal-area, disjoint-interior coverage.
The overlaps bridge some 0.225 mm gaps between adjacent parts. These rectangles
describe forbidden clearance regions; the physical artwork is unchanged.

Another 506 support boxes and 1,914 clearance points prove **five additional
whole-cell exclusions**, with exact rounding margins. One is the remaining
empty preflight cell. All **1,045 retained cells** still cover every valid rounded
center for arbitrary original rotations and continuous positions. The independent
audit checks 28,163 atom pairs and 2,024 rounding margins. Sampling failures play
no role in this proof.

## Checkpoint and next work

All **15 audits pass**, with both negative source preflights preserved and no
failed checker attempts. Continue only with a materially changed joint geometry
model, a stronger independent necessary proof, or a different core. Both inserts
and all fifteen cogs remain required. A complete 66-part source/native/material
witness, production integration within 60 seconds, and the full H5 matrix are
still needed.

At {review['utc']}, [all six main checks](https://github.com/skulitom/Nestbolt/actions/runs/40350260165)
pass on 4e3b316c, permitting a normal checkpoint push. Upstream Sparrow/Studio
heads and releases are unchanged. Production and READMEs are unchanged; no new
release is qualified. H2 retains its original gate and all 22 reserved vectors
remain untouched.

[Checks]({NAME}/checks.json), [source core]({NAME}/core-independent-checks.json),
[clearance proof]({NAME}/clearance-necessity-proof.json),
[clearance audit]({NAME}/clearance-cuts-checks.json),
[model]({NAME}/clearance-model-checks.json),
[response]({NAME}/clearance-response-checks.json), [scope]({NAME}/scope.json),
[next inventory]({NAME}/next-fixed34-neighborhood.json),
[next step]({NAME}/next-step.json), and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 paired bracket strip and clearance capacity, 2026-10-26:** [the evidence]({link})
verifies a changed 49-original core: all twelve brackets and nineteen inserts
fit beside eighteen frames, leaving two inserts and fifteen cogs mandatory.
Independent checks cover 666 pairs, 196 stock edges and 73 cutouts/6,782 vertices.
Fresh continuous all-angle domains yield 1,111 capacity cells and 127,947 verified
conflicts. Two distinct necessary positives fail their finite source preflights;
all 9,828 sampled events are independently checked. Separate exact oblique-support
proofs exclude 61 cells. Using the required 0.2 mm clearance joins fixed exclusion
regions through 833 audited union atoms and proves five further cell exclusions.
The stronger 1,818-constraint model closes UNKNOWN after search in 20.026862
returned/20.772295 shared seconds, with its 0.026862-second soft overrun recorded.
All three calls are closed, without retries. No full layout or unrestricted
exclusion is claimed. All fifteen audits pass. Main 4e3b316c passes all six checks,
allowing the next normal checkpoint push. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'audits_passed':15,'closed_calls':3,'final_status':'UNKNOWN'})
