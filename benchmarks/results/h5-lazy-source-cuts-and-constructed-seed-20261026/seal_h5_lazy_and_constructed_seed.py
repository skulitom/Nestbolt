"""Preserve two closed source-cut attempts and the independently checked construction."""
from pathlib import Path
from datetime import datetime, timezone
import ast, json, shutil, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack, digest
NAME = 'h5-lazy-source-cuts-and-constructed-seed-20261026'
OUT = ROOT / 'benchmarks/results' / NAME
A = ROOT / 'output/h5-lazy-source-cuts-20261026'
B = ROOT / 'output/h5-constructed-necessary-source-seed-20261026'
C = ROOT / 'output/h5-seeded-lazy-source-cuts-20261026'
load = lambda p: json.loads(p.read_bytes())

def write(p, v):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(v, f, indent=2); f.write('\n')

def append(p, s):
    with p.open('a', encoding='utf-8', newline='\n') as f: f.write(s)

def command(a): return subprocess.check_output(a, cwd=ROOT, text=True).strip()

previous = load(ROOT / 'benchmarks/results/h5-full-stock-source-cell-feasibility-20261026/source-review.json')
head = command(['git', 'rev-parse', 'HEAD'])
main = command(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
assert head.startswith('f010d74c') and main == previous['remote_main']
assert command(['git', 'rev-parse', 'HEAD^']) == main
assert source_digest() == previous['production_digest']
assert {n: digest(ROOT/n) for n in previous['current_readmes']} == previous['current_readmes']
ci = json.loads(command(['gh', 'run', 'view', '40386947038', '--json', 'databaseId,status,conclusion,headSha,jobs,url']))
assert ci['headSha'] == main and len(ci['jobs']) == 6
success = sum(j['conclusion'] == 'success' for j in ci['jobs'])
ready = ci['status'] == 'completed' and ci['conclusion'] == 'success' and success == 6
upstream = {
    'sparrow_head': command(['gh', 'api', 'repos/JeroenGar/sparrow/commits/main', '--jq', '.sha']),
    'studio_head': command(['gh', 'api', 'repos/JeroenGar/sparrow-studio/commits/main', '--jq', '.sha']),
    'sparrow_release': command(['gh', 'api', 'repos/JeroenGar/sparrow/releases/latest', '--jq', '.tag_name']),
    'studio_latest_release': json.loads(command(['gh', 'api', 'repos/JeroenGar/sparrow-studio/releases', '--jq', 'map(.tag_name)']))}
assert all(upstream[k] == previous[k] for k in upstream)
audits = {'unseeded-response': A/'result-audit/checks.json',
          'constructed-model': B/'model-audit/checks.json',
          'constructed-source': B/'source-audit/checks.json',
          'seeded-response': C/'result-audit/checks.json'}
assert all(load(p)['passed'] for p in audits.values())
aa, bb, cc, dd = [load(p) for p in audits.values()]
assert aa['status'] == dd['status'] == 'UNKNOWN' and aa['closed'] and dd['closed']
assert aa['rounds_attempted'] == dd['rounds_attempted'] == 1
assert aa['source_candidates_returned'] == dd['source_candidates_returned'] == 0
assert bb['all180_serialized_constraints_satisfied'] and cc['source_valid_partial_originals'] == 54
assert cc['full_pair_failures'] == 38 and not cc['actual_full_source_valid']
assert dd['initial_source_pair_cuts'] == 38 and dd['new_source_pair_cuts_added'] == 0
OUT.mkdir()
for n, p in audits.items(): shutil.copyfile(p, OUT/(n+'-checks.json'))
for p,n in [(A/'search/result.json','unseeded-closed-result.json'),
            (B/'constructed.json','construction.json'), (B/'anchors-um.json','constructed-anchors-um.json'),
            (B/'partial54-placements.json','partial54-placements.json'),
            (B/'source-audit/initial-source-pair-cuts.json','initial-source-pair-cuts.json'),
            (C/'search/result.json','seeded-closed-result.json')]: shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-db4d2309-snapshot.json', ci)
review = {'utc': datetime.now(timezone.utc).isoformat(), 'source_head':head, 'remote_main':main,
          'production_digest':previous['production_digest'], 'current_readmes':previous['current_readmes'],
          'production_and_readmes_unchanged':True, **upstream, 'upstream_heads_and_releases_unchanged':True,
          'main_ci':40386947038,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,
          'push_qualified_now':ready,'unpublished_prior_checkpoints':1,'completion_percent':60,
          'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,
          'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json', {'all57_first_originals_required':True,'all9_short_originals_fixed':True,
      'full_stock_domains':True,'fixed_source_modes':True,'solver_calls':2,'closed_unknown_calls':2,
      'solver_candidates_returned':0,'constructed_candidate_source_pair_failures':38,
      'source_valid_partial_originals':54,'remaining_cogs_present_and_required':12,
      'new_best_partial_claimed':False,'no_exclusion_claimed':True,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json', {'action':'Both lazy source-cut pipelines are CLOSED UNKNOWN in their first round; do not extend, reseed or repeat them. The direct assignment proves the old necessary model feasible but exposes that its single153mm cog square is too weak. A materially different geometry model can replace each cog square with multiple disjoint horizontal rectangles contained in that actual transformed source outline. Derive and independently verify containment and within-original disjointness before any bounded solve; retain whole-stock domains, every original, the checked short sheet, and detailed final source readback. This is a proposed geometry change, not a reopened solver call. No complete source/native/material witness exists, so integration, the full H5 matrix and another release remain unqualified. Keep H2 unchanged and22 reserved vectors unopened. Await all6 passing checks on main db4d2309 CI40386947038 before a normal checkpoint push.',
      'completion_percent':60,'H2_complete':False,'H5_complete':False})
members = {}; inputs = {}
for folder in [A,B,C]:
    for p in folder.rglob('*'):
        if p.is_file(): members[folder.name+'/'+p.relative_to(folder).as_posix()] = p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            assert digest(ROOT/n) == h, (p,n)
            inputs[n] = h
for n in inputs: members['source-inputs/'+n] = ROOT/n
write(OUT/'source-bindings.json', inputs)
helpers = [ROOT/'output'/n for n in [
    'h5_lazy_source_model.py','h5_lazy_source_model_audit.py','prepare_h5_lazy_source_search.py',
    'h5_lazy_source_round.py','run_h5_lazy_source_search.py','audit_h5_lazy_source_search.py',
    'construct_h5_necessary_source_seed.py','audit_h5_necessary_source_seed_model.py',
    'audit_h5_necessary_source_seed_geometry.py','h5_seeded_lazy_source_model.py',
    'prepare_h5_seeded_lazy_source_search.py','h5_seeded_lazy_source_round.py',
    'run_h5_seeded_lazy_source_search.py','audit_h5_seeded_lazy_source_search.py',
    'ccd1.py','pack_h5_evidence_archive.py']]
seen = set()
while helpers:
    p = helpers.pop()
    if p in seen: continue
    seen.add(p); members['helpers/'+p.name] = p
    for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
        mods = ([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else
                [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q = ROOT/'output'/(mod+'.py')
            if q.is_file(): helpers.append(q)
archive, manifest = pack(ROOT, OUT, NAME, members)
write(OUT/'checks.json', {'passed':True,'independent_audits_passed':4,
      'closed_unknown_solver_calls':2,'source_candidates_from_solver':0,
      'constructed_all180_necessary_constraints_satisfied':True,
      'constructed_full_source_pair_failures':38,'source_valid_partial_originals':54,
      'all_frames_brackets_inserts_in_valid_partial':True,'remaining12_cogs_mandatory':True,
      'new_best_partial_claimed':False,'native_calls':0,'completion_percent':60,
      'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text = ('All six checks pass, so the queued checkpoints may be pushed normally.' if ready else
           f'{success} of six checks pass. The remaining main checks are still running; no checkpoint push is attempted.')
report = f'''# H5: source-cut attempts and a constructive necessary-model witness — 2026-10-26

**A direct construction satisfies every constraint in the simpler model, but the
complete source layout still has 38 colliding pairs.** Its valid 54-original
portion includes every frame, bracket and insert plus the three short-sheet
cogs. Both distinct source-cut searches close UNKNOWN in their first round.
H2/H5 remain open at 60% by completed gate weights.

## Two closed attempts

The first pipeline starts with all 114 whole-stock coordinates, 65 source-contained
rectangles, NoOverlap2D, both cumulative strip constraints and 47 equivalent-copy
orders: 180 serialized constraints, no hints or objective. All 57 first-sheet
originals remain mandatory, alongside the fixed verified short nine. Its declared
algorithm allows at most six rounds within 60 search/90 shared seconds, with a
15-second first solve and eight-second later caps. Any later round must add every
newly failing source pair; UNKNOWN stops the pipeline immediately.

Only round zero runs. It returns UNKNOWN after 390,943 branches and 26,682 conflicts.
Solver time is 15.013275 seconds, returned solve 15.014221, algorithm 16.570634 and
shared process 16.716055. No assignment, source candidate or new pair cut exists.
The small soft overruns are recorded. The run is closed without retry or extension.

## What the direct construction proves

Without a solver call, the construction places 12 turned and six wide frames,
eight first-sheet brackets and 19 inserts. Each bracket receives one insert in
its exterior concave notch; this is not nesting inside a hole. The remaining
inserts occupy strips beside and above the frame/bracket rows. Twelve cog inner
squares occupy six columns by two rows within the full-source stock domains.
Equivalent copies are assigned in nondecreasing Y order.

An independent serialized-model reader verifies all 114 coordinates, every one
of the 180 constraints, 2,080 rectangle pairs, 111 cumulative events and all
47 copy orders. Thus the closed search's UNKNOWN result is not a proof that
these necessary conditions are impossible.

An independent original-ring reader checks all 66 originals, 90 cutouts and
10,026 hole vertices, all 1,632 same-sheet pairs and 264 stock edges. It finds
38 pair failures and zero stock failures. Removing only the 12 first-sheet cogs
from the partial-layout view leaves **54 source-valid originals**, checked through
1,026 pairs and 216 stock edges, with 78 cutouts/7,626 hole vertices. Minimum gap
is 0.224308672487 mm and minimum extra stock clearance is 0.012600000000 mm.
All 12 excluded cogs remain present in the complete failed candidate and
mandatory in further work. This does not improve the older preserved 64-part
partial count and is not a full job fit.

Original 31 moves vertically by 1,531.493812 mm relative to the earlier mixed
candidate, escaping its independently proved 180 mm obstruction. The construction
therefore supplies a different configuration while showing why the single
153 mm inner square is an inadequate representation of each complete cog.

## Source-informed initialization

The second pipeline starts with all **38 actual failing-pair disjunctions** and
90 coordinate hints for the 45 first-sheet non-cogs. No first-sheet position is
fixed; the 12 first-sheet cogs have full domains and no hints. The new model has
3,880 variables, 13,246 constraints and 13,028 integer halfplanes. Its independent
reader checks all constraints and every hint. It shares the same declared bounded
round policy, but is a different model from the closed empty-cut attempt.

Again only round zero runs: UNKNOWN, 20,144 branches and 6,155 conflicts. Solver
time is 15.043030 seconds, returned solve 15.056194, algorithm 18.150153 and shared
process 18.386994. The 38 initial cuts remain; **zero new cuts** and zero source
candidates are generated. Soft overruns are preserved. No later round, unchanged
retry, exclusion claim, native call or full quality run occurs.

Four independent audits pass. The next distinct hypothesis is to replace each
single cog square with several disjoint rectangles contained in its actual
source outline, independently checking their coverage and disjointness. This
changes the necessary geometry model. It does not reopen either closed search
or qualify a source/native/material witness.

## Repository and evidence

At {review['utc']}, [main checks](https://github.com/skulitom/Nestbolt/actions/runs/40386947038):
{ci_text} The preceding f010d74c checkpoint remains queued locally. Production,
READMEs and upstream heads/releases are unchanged. The 22 reserved H2 vectors
remain unopened, and no new release is qualified.

[Checks]({NAME}/checks.json), [unseeded response]({NAME}/unseeded-response-checks.json),
[construction model]({NAME}/constructed-model-checks.json),
[construction source]({NAME}/constructed-source-checks.json),
[seeded response]({NAME}/seeded-response-checks.json), [scope]({NAME}/scope.json),
[next step]({NAME}/next-step.json) and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f: f.write(report)
note = '''\n\n**N4 source-cut attempts and constructive seed, 2026-10-26:** [the evidence]({link})
records two distinct pipelines, each CLOSED UNKNOWN in its first round without
returning a candidate or adding new source cuts. The first uses 114 variables/
180 necessary constraints; a separate direct construction satisfies all of them
but has 38 actual source collisions. Its 54-source-valid partial contains every
frame, bracket and insert plus the short three cogs; the other 12 cogs remain
present and mandatory. This is not a new best partial count or full source fit.
The second starts with the 38 actual failing-pair disjunctions and 90 non-cog
hints, fixes no first original, and closes UNKNOWN with 3,880 variables/13,246
constraints. Returned/shared times are 15.014221/16.716055 and
15.056194/18.386994 seconds; small soft overruns are preserved. Four independent
audits pass. A stronger source-contained cog representation is the next distinct
hypothesis; neither closed search may be extended or reseeded. H2/H5 remain open
at 60%; no native/full-quality run or release qualifies and all 22 reserved H2
vectors remain unopened. Wait for all six main CI40386947038 checks before the
next normal checkpoint push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,'independent_audits_passed':4,**archive,'main_ci_successful_jobs':success,'push_qualified_now':ready})
