"""Preserve the all-copy count frontier and a new independently checked source core."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-global-short-frontier-and-eight-brackets-20261026';OUT=ROOT/'benchmarks/results'/NAME;FRONT=ROOT/'output/h5-global-short-frontier-20261026';CORE=ROOT/'output/h5-eight-bracket-short-core-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-mixed-rows-source-contacts-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head=='d09d5011521270cdc687bd4113dcd89f01d181f1' and command(['git','rev-parse','HEAD^'])==main=='e158daa2b8f0c51399a26769cd05f6d470d664ec'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40365489221','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))};assert all(upstream[k]==previous[k] for k in upstream)
audits={'frontier':FRONT/'audit/checks.json','source-core':CORE/'audit-horizontal-mode-repaired/checks.json'};assert all(load(p)['passed'] for p in audits.values());fc=load(audits['frontier']);cc=load(audits['source-core']);assert fc['all_allocations_verified']==4576 and fc['necessary_survivors']==454 and cc['all66_originals_accounted_once'] and cc['mandatory_moving_counts']=={'bracket':4,'insert':5,'cog':15}
OUT.mkdir()
for label,p in audits.items():shutil.copyfile(p,OUT/(label+'-checks.json'))
for p,name in [(FRONT/'frontier.json','necessary-frontier.json'),(FRONT/'pareto-necessary-counts.json','pareto-necessary-counts.json'),(FRONT/'audit/necessity-proof.json','necessity-proof.json'),(FRONT/'audit/maximum-cog-counts.json','maximum-cog-counts.json'),(FRONT/'cog-spacing.json','stronger-horizontal-spacing.json'),(FRONT/'area-proof.json','exact-area-proof.json'),(CORE/'audit-horizontal-mode-repaired/next-neighborhood.json','all66-inventory.json'),(CORE/'short-sheet-placements.json','short-sheet-placements.json'),(CORE/'visual/core.png','core.png'),(CORE/'audit/failure.json','preserved-checker-failure.json')]:shutil.copyfile(p,OUT/name)
write(OUT/'main-ci-e158daa2-passed.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40365489221,'main_ci_successful_jobs':6,'queued_previous_checkpoint':head,'next_push_commits':2,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
next_action='Use the verified eight-bracket/five-insert short sheet as a new allocation option. Its current first core is18 unturned frames plus11 vertical inserts, with originals26..29,46..50 and51..65 all mandatory (4 brackets,5 inserts,15 cogs). No source search has opened for this42-core/24-mover inventory. Old paired-strip and mixed-row calls remain CLOSED; their exclusions and poses do not transfer. Any new work must use current owners and real original geometry, preserve all66 identities, and justify its hypothesis using this geometry rather than rerun an unchanged pool. The global short frontier excludes4122 count allocations for the declared target independently of the first layout;454 surviving allocations are necessary-only, not source fits. The frontier is not a whole-job impossibility proof. Preserve both64-part partials and the other source cores. Full66 source/native/material evidence is still required before production integration within60 seconds and the fullH5 matrix. Main e158daa2 now passes all six checks; push the queued d09d5011 checkpoint and this evidence normally after staging and ancestry verification. H2 keeps its original gate and22 reserved vectors remain unopened.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'frontier_first_sheet_fixed':False,'short_target_outer_top_mm':319.42699,'all_original_family_counts_considered':{'bracket':12,'insert':21,'cog':15},'frames_cannot_fit_short_target':True,'excluded_allocations':4122,'necessary_survivors':454,'survivors_are_source_fits':False,'new_source_core_fixed_originals':42,'mandatory_first_movers':24,'source_witness_complete':False,'whole_job_excluded':False,'solver_calls':0,'native_calls':0,'H5_complete':False})
members={};inputs={}
for folder in [FRONT,CORE]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
# Direct dependencies of the independent geometry reader, also bound by the
# retained core-sequence plan; no whole old experiment is reopened.
oldplan=load(ROOT/'output/h5-core-sequence-bound-20261026/plan.json')
for n,h in oldplan['inputs'].items():assert digest(ROOT/n)==h;inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=list((ROOT/'output').glob('*h5_global_short*.py'))+list((ROOT/'output').glob('*h5_eight_bracket_short*.py'))+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
checks={'passed':True,'independent_audits_passed':2,'failed_checker_attempts_preserved':1,'pair_bounds_recomputed':81,'guaranteed_y_pairs':768,'forward_states_verified':222,'backward_states_verified':222,'transitions_verified':1998,'all_count_pairs_verified':208,'all_allocations_verified':4576,'excluded_ordered_projection':3850,'excluded_filled_outer_area':272,'necessary_survivors':454,'pareto_necessary_count_vectors':32,'all66_count_complements_verified':True,'new_source_core_originals':42,'new_core_pairs':484,'new_core_stock_edges':168,'new_core_cutouts':58,'new_core_cutout_vertices':4952,'short_filled_area_increase_mm2':800,'mandatory_first_movers':24,'solver_calls':0,'native_calls':0,'source_witness_complete':False,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: global short-sheet count frontier and eight-bracket construction — 2026-10-26

**Exact necessary bounds exclude 4,122 of 4,576 short-sheet allocations without
fixing the first-sheet layout.** A separate original-geometry construction fits
eight brackets and five inserts on that short sheet. Its new 42-original core
still needs 24 first-sheet placements. There is no complete target witness;
H2/H5 remain open at 60% by completed gate weights.

## All available counts, without a fixed first layout

The declared usable short stock is [6.5, 6.5, 1493.5, 319.42699] mm. The upper
edge is slightly outward of the retained target; another 0.020 mm outward
relaxation covers quantization. Recomputed floor-anchor bounds exactly match
the previously proved source domains. Fresh transverse support checks retain
positive margins for every bracket stem. Frames have at least 350 mm height
in every allowed orientation, so all eighteen remain on the first sheet for
this two-sheet target.

Reuse intrinsic, source-contained stem/rectangle and mixed-pair necessities,
without importing any fixed first-sheet positions. The full-circle cog proof
gives at least 254.297 mm between rounded centers. Their entire vertical range
is 34.426 mm, so exact integer square-root arithmetic strengthens the necessary
horizontal gap from **245.034 mm to 251.956 mm**.

The complete ordered projection considers all eight bracket modes, arbitrary
real cog angles and all available counts: 0–12 brackets and 0–15 cogs. The
forward earliest-position recurrence has **222 states and 1,998 transitions**.
An independently implemented backward latest-position recurrence has 222
states and exactly the same surviving count pairs. The auditor independently
reconstructs all **81 pair bounds**, including **768 guaranteed-Y rectangle
overlap relations**, and checks every saved forward witness and transition.

| Brackets on short sheet | Maximum cogs allowed by this necessary bound |
| --- | ---: |
| 0 or 1 | 5 |
| 2 | 4 |
| 3 or 4 | 3 |
| 5 | 2 |
| 6 or 7 | 1 |
| 8 | 0 |
| 9–12 | No placement survives, even with zero cogs |

Exact rational triangulation of the original filled outlines supplies a
separate area bound for every 0–21 insert count. Holes remain reserved; omitting
clearance only weakens this necessary bound. All **4,576 allocations** and their
first-sheet complementary counts are checked: **3,850** fail the ordered
projection, another **272** fail filled-outer area, and **454** remain unresolved.
Their 32 componentwise maximal count vectors are archived. None of these
positive necessary results is presented as a source fit. This is not a proof
that the full job is impossible.

## A concrete alternative short allocation

Four source bracket-pair patterns, each with an insert between separate filled
outers, plus one vertical insert on the right fit **eight brackets and five
inserts**. Originals18–25 and30–34 are on the short sheet. Their filled area is
**419,000 mm²**, which is 800 mm² more than the earlier verified six-bracket/
nine-insert arrangement. Its outer top is 319.0 mm and right edge 1,439.225 mm.
This is an allocation tradeoff, not a complete-layout improvement.

The first-sheet core uses eighteen unturned frames in three columns by six rows,
with eleven vertical inserts35–45 beside them. All **four brackets26–29, five
inserts46–50 and fifteen cogs51–65** remain mandatory. Every one of the 66 source
identities is accounted for exactly once. No search is opened for this new core.

Independent source readback checks **42 originals, 484 same-sheet pairs, 168
stock edges and 58 cutouts with 4,952 vertices**. All 42 anchors are reconstructed
from rational formulas. Minimum pair gap is 0.225 mm; minimum extra stock margin
is 0.025 mm, above the native guards. The first fixed top is 2,107.65 mm. No
part-in-hole packing is used. Earlier 64-part partials and other cores remain
preserved, and old neighborhood exclusions do not transfer.

![New checked core; 24 original parts remain mandatory]({NAME}/core.png)

## Repository and evidence

Both independent audits pass. One initial checker failure remains preserved:
it incorrectly expected a 180° horizontal insert where the saved original
profile uses 0°. The repaired expectation validates the unchanged geometry.
There are **no solver calls, native calls or full quality runs** in this work.

At {review['utc']}, [all six checks on main e158daa2](https://github.com/skulitom/Nestbolt/actions/runs/40365489221)
pass, allowing a normal two-commit push with the queued d09d5011 checkpoint.
Production, READMEs, upstream heads/releases and all 22 reserved H2 vectors
are unchanged. No new release qualifies. The next source construction must
retain all 24 movers and pass full66 source/native/material checks before
production integration within 60 seconds and the complete H5 matrix.

[Checks]({NAME}/checks.json), [frontier audit]({NAME}/frontier-checks.json),
[necessity proof]({NAME}/necessity-proof.json), [source audit]({NAME}/source-core-checks.json),
[inventory]({NAME}/all66-inventory.json), [scope]({NAME}/scope.json),
[next step]({NAME}/next-step.json), and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 global short-sheet frontier and eight-bracket construction, 2026-10-26:** [the evidence]({link})
uses the full-circle cog certificate to strengthen short-sheet horizontal
spacing to 251.956 mm. Independent forward/backward recurrences check 222 states,
1,998 transitions and all 81 pair bounds without fixing a first-sheet layout.
All 4,576 bracket/insert/cog allocations are covered: 3,850 fail the necessary
ordering and 272 more fail exact filled-outer area; 454 remain necessary-only.
A new actual eight-bracket/five-insert short sheet carries 800 mm² more filled
area than the former six-bracket/nine-insert option. Its 42-original core passes
484 pairs, 168 stock edges and all 58 cutouts; four brackets, five inserts and
fifteen cogs stay mandatory. Both independent audits pass, with one repaired
checker expectation preserved. No solver/native call or full target witness.
All six main e158daa2 checks pass, allowing the queued two-commit push. H2/H5
remain open at 60%; production, READMEs, releases and all 22 reserved H2 vectors
are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'independent_audits_passed':2,'main_ci_successful_jobs':6,'next_push_commits':2})
