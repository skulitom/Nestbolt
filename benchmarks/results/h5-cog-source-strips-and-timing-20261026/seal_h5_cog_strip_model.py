"""Archive stronger source strips, their closed search, and its explicit timing failure."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-cog-source-strips-and-timing-20261026';OUT=ROOT/'benchmarks/results'/NAME
GEO=ROOT/'output/h5-cog-source-strips-20261026';MODEL=ROOT/'output/h5-cog-strip-model-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-lazy-source-cuts-and-constructed-seed-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head.startswith('117a0e4a') and main==previous['remote_main']
assert command(['git','rev-parse','HEAD^^'])==main
assert source_digest()==previous['production_digest']
assert {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40386947038','--json','databaseId,status,conclusion,headSha,jobs,url']))
assert ci['headSha']==main and ci['status']=='completed' and ci['conclusion']=='success'
assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
    'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
    'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
    'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
audits={'source':GEO/'source-audit/checks.json','capacity':GEO/'capacity-audit/checks.json',
        'model':MODEL/'model-audit/checks.json','response':MODEL/'response-audit/checks.json'}
assert all(load(p)['passed'] for p in audits.values())
response=load(audits['response']);model=load(audits['model'])
assert response['status']=='UNKNOWN' and response['closed'] and not response['has_assignment']
assert not response['solver_60_second_budget_met'] and not response['timing_qualified_for_60_second_benchmark']
assert response['shared_90_second_budget_met'] and model['prior_model_preserved_byte_exact']
OUT.mkdir()
for n,p in audits.items():shutil.copyfile(p,OUT/(n+'-checks.json'))
for p,n in [(GEO/'prepared.json','source-strip-summary.json'),(GEO/'rectangles.json','source-contained-strips.json'),
            (GEO/'known-witness-strip-capacity.json','known-witness-strip-capacity.json'),
            (GEO/'source-strips.png','source-strips.png'),(MODEL/'built.json','model-summary.json'),
            (MODEL/'search/result.json','closed-result.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-db4d2309-success.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,
    'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],
    'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,
    'main_ci':40386947038,'main_ci_status':'completed','main_ci_successful_jobs':6,
    'push_qualified_now':True,'unpublished_prior_checkpoints':2,'completion_percent':60,
    'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,
    'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'all57_first_originals_required':True,'all9_short_originals_fixed':True,
    'whole_stock_domains':True,'fixed_first_originals':0,'fixed_source_modes':True,
    'prior_model_retained':True,'stronger_source_contained_geometry':True,
    'new_candidate_or_exclusion':False,'solver_status':'UNKNOWN','solver_60_second_budget_met':False,
    'shared_90_second_budget_met':True,'timing_qualified_for_60_second_benchmark':False,
    'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The781-strip model call is CLOSED UNKNOWN and missed its60-second solver limit by27.617085seconds; do not extend, repeat or reseed it. The log records the fj worker at1.41minutes while the three main workers end near57seconds. Do not use this attempt as a timed quality result. Both strip cumulative constraints independently reject the old invalid witness, so a different decomposition can first solve only whole-stock coordinates, the old65-rectangle non-overlap and aggregated per-original strip capacity profiles, then inspect all66 source rings and introduce detailed source cuts only for actual new violations. This avoids the additional781-rectangle global non-overlap and thousands of initial disjunction selectors. Verify profile aggregation from the source strips and inspect worker/deadline handling before any new run; preserve every original and the checked short sheet, and stop unchanged-model retries. No full source/native/material witness exists. H2 remains unchanged and22 reserved vectors stay unopened. All6 main db4d2309 checks now pass; the three verified evidence checkpoints can be pushed normally after this commit. No new release qualifies.',
    'completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs={}
for folder in [GEO,MODEL]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
prior=ROOT/'output/h5-seeded-lazy-source-cuts-20261026'
for n,h in load(prior/'plan.json')['inputs'].items():assert digest(ROOT/n)==h,n;inputs[n]=h
for p in [prior/'plan.json',prior/'search/round-00/request.json',
          ROOT/'output/h5-constructed-necessary-source-seed-20261026/model-audit/checks.json']:
    inputs[p.relative_to(ROOT).as_posix()]=digest(p)
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=[ROOT/'output'/n for n in ['prepare_h5_cog_source_strips.py','audit_h5_cog_source_strips.py',
    'audit_h5_cog_strip_capacity.py','render_h5_cog_source_strips.py','build_h5_cog_strip_model.py',
    'audit_h5_cog_strip_model.py','run_h5_cog_strip_model.py','audit_h5_cog_strip_response.py',
    'ccd1.py','pack_h5_evidence_archive.py']];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p
    for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else
              [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':4,
    'source_contained_rectangles_verified':781,'cog_strips_verified':728,
    'prior_constraints_preserved':13246,'total_constraints_verified':14811,
    'known_invalid_witness_rejected_by_both_strip_capacities':True,
    'closed_solver_status':'UNKNOWN','solver_60_second_budget_met':False,
    'timing_qualified_for_60_second_benchmark':False,'native_calls':0,
    'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: source-contained cog strips and a timing failure — 2026-10-26

**The new cog representation covers over 90% of each filled source outline, but
its one search returns UNKNOWN and misses the requested 60-second solver limit.**
There is no layout, unrestricted exclusion, native validation or timed quality
result. H2/H5 remain open at 60% by completed gate weights.

## More occupied source area

Each actual cog mode is split into 32 horizontal bands. Intersections of source
sections at band edges and every source-vertex height identify common horizontal
intervals; inward integer-micrometre rounding makes their rectangles conservative.
Direct source-polygon containment is required for every entire rectangle.

Mode 3 yields 64 disjoint strips, occupying 45,131.711335 mm², or **90.150340%**
of its filled outer outline. Mode 16 yields 60 strips, 45,440.856082 mm², or
**90.767855%**. These replace no source geometry and ignore no original: the holes
remain reserved with part-in-hole off. For the 12 first-sheet cogs, the new
representation contains 728 strips. Adding the unchanged 53 non-cog rectangles
gives 781 rectangles occupying 4,075,822.063704 mm², compared with
3,812,050.736262 mm² in the older 65-rectangle representation.

![Actual source outlines and verified inner strips]({NAME}/source-strips.png)

An independent reader reconstructs each shape from the original ring and checks
all 781 whole rectangles, all 57 owners and 21,740 within-original disjoint pairs.
It checks 282,850 cross-original rectangle pairs in the known constructed witness,
finding 1,193 overlaps involving 36 original pairs. The witness that satisfied
the old necessary model is correctly rejected by the richer geometry.

A separate exact-integer slab audit also rejects that witness through both
cumulative constraints alone. Across 1,038 X slabs, 674 exceed the 2,987 mm height
capacity, with peak demand 3,352.183 mm. Across 216 Y slabs, 102 exceed the 1,487 mm
width capacity, with peak demand 2,679.758 mm. These are sums of disjoint occupied
source strips, not the full-source layout acceptance test.

## Added source constraints

The complete prior seeded model is retained byte-for-byte as a prefix: every
whole-stock coordinate domain, all 38 source-pair disjunctions, the old
65-rectangle non-overlap/strip constraints, 47 equivalent-copy orders and 90
non-cog coordinate hints. No first-sheet original is fixed; all 57 remain
mandatory alongside the verified short nine.

The new model adds 1,562 intervals, a second NoOverlap2D and two cumulative
constraints for the 781 rectangles. It has **3,880 variables and 14,811
constraints**. An independent protobuf reader verifies the exact old model and
all 1,565 added constraints. The model hash is
`b045ec52775277c18bf7dfee6a8bf82eef99d2ff5a36053e43be73fd126c3103`.

## Closed UNKNOWN with an unqualified overrun

The single call requested 60 solver seconds within 90 shared process seconds.
Search starts after approximately 2.93 seconds. The response returns **UNKNOWN**,
20,248 branches and 5,401 conflicts, without an assignment. Solver time is
**87.617085 seconds**, returned solve time **87.625742**, shared process time
**88.877085**. The requested solver limit is exceeded by **27.617085 seconds**;
the returned solve overrun is 27.625742 seconds. The 90-second process boundary
is met, but the 60-second benchmark condition is **not**.

The log records the `fj` worker at 1.41 minutes while the three main workers each
end near 57 seconds. This observation does not identify the exact internal
propagator responsible. The raw response, log and explicit failed timing flags
are preserved. The call is CLOSED without extension, reseeding or retry.

Four independent audits pass on geometry, capacity, serialized constraints and
response integrity. Those passes do not turn the timing failure or UNKNOWN into
H5 acceptance. A different staged model could use aggregated per-original strip
capacities first, reserving detailed source cuts for actual returned violations,
without the extra global 781-rectangle non-overlap system. Profile aggregation
and deadline handling must be checked before opening such a run.

## Checkpoint and evidence

At {review['utc']}, [all six main checks pass](https://github.com/skulitom/Nestbolt/actions/runs/40386947038).
The prior two local checkpoints and this evidence checkpoint may now be pushed
normally after commit. Production, READMEs and upstream heads/releases are
unchanged; all 22 reserved H2 vectors remain unopened. No release is qualified.

[Checks]({NAME}/checks.json), [source]({NAME}/source-checks.json),
[capacity]({NAME}/capacity-checks.json), [model]({NAME}/model-checks.json),
[response and timing]({NAME}/response-checks.json), [scope]({NAME}/scope.json),
[next step]({NAME}/next-step.json) and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 source cog strips and timing failure, 2026-10-26:** [the evidence]({link})
adds 728 disjoint cog strips covering 90.150340%/90.767855% of the two actual cog
modes. With the unchanged non-cogs, 781 source-contained rectangles
add necessary constraints to the prior model, whose 13,246 constraints remain byte-exact; all
14,811 new-model constraints are independently verified. Both new cumulative
constraints alone reject the earlier constructed invalid witness. The sole
search closes UNKNOWN with 20,248 branches/5,401 conflicts and no assignment.
Its 87.617085 solver/87.625742 returned/88.877085 shared seconds exceed the
requested 60-second solver limit by 27.617085 seconds: timing is explicitly
unqualified despite the 90-second process boundary being met. Four independent
audits pass without claiming H5 acceptance, and the closed call cannot be
extended or reseeded. All six main db4d2309 checks now pass, allowing the next
normal checkpoint push. H2/H5 remain open at 60%; no native/full-quality run or
new release qualifies and all 22 reserved H2 vectors remain unopened.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,'independent_audits_passed':4,'solver_60_second_budget_met':False,
       'main_ci_successful_jobs':6,'push_qualified_now':True,**archive})
