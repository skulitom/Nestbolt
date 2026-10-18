from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess,sys,zipfile
import psutil
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-assignment-repack-20261018'
sys.path.insert(0,str(root/'scripts'));import h5_assignment_repack as runner
load,write,digest=runner.load,runner.write,runner.digest
result=load(out/'results.json');audit=load(out/'independent-audit.json');plan=load(out/'plan.json');opened=load(out/'opened.json');repeat=load(out/'repeated-assignments.json')
try:command=psutil.Process(opened['pid']).cmdline()
except psutil.NoSuchProcess:command=[]
assert not any('h5_assignment_repack.py' in c for c in command)
assert result['all_four_completed'] and result['guards_unchanged'] and runner.guards()==plan['guards']
assert digest(out/'plan.json')==opened['plan_sha256']
assert subprocess.check_output(['git','show','HEAD:'+(out/'plan.json').relative_to(root).as_posix()],cwd=root)==(out/'plan.json').read_bytes()
assert result['wall_seconds']<plan['session_limit_seconds'] and len(result['records'])==4
assert audit['all_four_assignments_audited'] and audit['all_original_archives_verified'] and audit['feasible_assignments']==3
assert audit['source_sha256']==digest(out/'audit.py')
assert sum(len(r['rounds']) for r in audit['records'])==9
assert repeat['attempts']==25 and repeat['distinct_assignments_within_invocations']==8 and repeat['repeated_after_first']==17
archives=[]
for r in result['records']:
    archive=out/r['archive'];assert digest(archive)==r['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,row in r['members'].items():
            data=z.read(name);assert sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes']
    archives.append({'path':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'members':len(r['members'])})
for r in audit['records']:
    for round in r['rounds']:
        folder=out/'validation'/(r['job']+'-k'+str(r['kerf_mm'])+'-round-'+str(round['index']))
        public=load(folder/'stdout.json');layout=load(folder/'layout.json');job=load(folder/'job.json')
        assert len(layout['placements'])==sum(p['quantity'] for p in job['parts'])==r['parts']
        assert public['valid']==round['CLI_valid']
        if round['feasibility_witness']:
            assert round['collision_clear'] and round['original_filled_outer_clear'] and public['valid'] and round['CLI_exit_code']==0
        else:assert not public['valid'] and round['CLI_exit_code']==1
status=root/'docs/STATUS.md';status_text=status.read_text(encoding='utf-8');marker='**N4 capacity diagnosis, 2026-10-18:**';assert status_text.count(marker)==1
verification={'all_four_original_archives_verified':True,'archives':archives,'exact_original_model_restoration':True,
    'all_nine_rounds_independently_checked':True,'feasible_source_assignments':3,'unresolved_source_assignments':1,
    'successful_repairs_all_started_from_saved_positions':True,'unsuccessful_rounds_retained':6,
    'production_input_binary_guards_unchanged':True,'same_source_inventory_and_shortened_boundary':True,
    'actual_repair_durations_are_diagnostic_not_quality_or_minimum_required_time':True,
    'whole_job_material_improvement_proven':False,'H5_complete':False,'completed_weight_percent':60}
write(out/'verification.json',verification)
lines=['# Fixed return-assignment feasibility repacking — 2026-10-18','',
    '**Three of four fixed source assignments now have independently valid packings.**',
    'Both 21-part large-plate cases and the 103-part panel case at 0.2 mm kerf fit',
    'the exact original shortened boundaries. The 103-part panel case at 1.5 mm',
    'kerf remains unresolved after all six recorded rounds.','',
    '| Saved assignment | Kerf mm | Parts | Rounds | Independent result | Successful repair seconds |',
    '| --- | ---: | ---: | ---: | --- | ---: |']
for r in audit['records']:
    success=[v for v in r['rounds'] if v['feasibility_witness']]
    duration=f"{success[0]['seconds']:.6f}" if success else '—'
    lines.append(f"| {r['job']} | {r['kerf_mm']} | {r['parts']} | {len(r['rounds'])} | {'Valid source packing' if success else 'Unresolved; all six rounds fail'} | {duration} |")
lines += ['',
    f"The complete four-case session took {result['wall_seconds']:.3f} seconds. Each",
    'case followed the committed seed-zero, serial CPU8 plan: saved positions',
    'first, then up to five full random restarts, each round bounded by a ten-second',
    'deadline within sixty seconds total. All three successes came from the first',
    'warm round; the unresolved case retained its warm failure and all five random',
    'failures. Observed round durations include a small deadline-check overrun.',
    'These are diagnostic durations, not a quality comparison or proof of minimum',
    'necessary repair time. Different search trajectories can behave differently.','',
    'All four inputs first restored through the unchanged original full-job model',
    'with exact saved f32 collision polygons and container vertices. Independent',
    'Shapely checks then verified membership, unchanged shortened boundary, no',
    'collision-polygon overlap/outside area, original allowed orientations and',
    'reflection, filled-outer separation and kerf. The three public subset layouts',
    'also pass the original CLI validator, including all quantities. Successful',
    'minimum original kerf slack is 0.012918, 0.013573 and 0.009903 mm respectively.',
    'Every unsuccessful round is retained with its failed independent and CLI checks.','',
    '[The independent audit](h5-assignment-repack-20261018/independent-audit.json)',
    'links all nine rounds; [verification](h5-assignment-repack-20261018/verification.json)',
    'binds the four immutable original archives and input/source/binary guards.',
    'This proves feasibility of those three source assignments only. It neither',
    'proves whole-job material improvement nor makes the fourth assignment impossible.','',
    'A read-only [inventory/container analysis](h5-assignment-repack-20261018/repeated-assignments.json)',
    'finds 8 distinct assignments across the earlier 25 attempts, with **17 repeats',
    'after the first occurrence within the same exchange invocation**. Identical',
    'original item indices and counts identify interchangeable copies; unstable',
    'snapshot placement keys are excluded. This motivates testing retained repair',
    'progress for compatible repeated assignments while keeping the original',
    'shared budget, acceptance checks and rollback. It is not measured reuse or',
    'evidence of a speed/quality gain. Stale collision-tracker keys must never be',
    'carried into a reconstructed layout.','',
    'Production remains unchanged. Any repair-state reuse needs authored safety',
    'checks and the original matched quality gate before integration. **H2/H5',
    'remain open; completion stays 60%.**','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Three fixed return assignments have valid packing witnesses

[The committed four-case repack](benchmarks/results/h5-assignment-repack-20261018.md)
finishes in {result['wall_seconds']:.3f} seconds. Exact original-model reconstruction
precedes every search. Independent collision-boundary, original filled-outer,
kerf, quantity and orientation checks plus public CLI validation confirm three
source packings: both 21-part large-plate cases and the 103-part 0.2 mm panel case.
Their first saved-position repair rounds take 1.048544, 2.291579 and 6.155242 seconds.
These are observed diagnostic durations, not quality comparisons or minimum
required times. The 103-part 1.5 mm panel assignment remains unresolved after its
warm round and five full random restarts; all six failures and nine audited
rounds are retained. No failed search is treated as an impossibility proof.

The earlier 25 traces contain eight distinct source-inventory/container pairs
within invocations, with 17 repetitions after the first. Test compatible repair
state reuse under the original shared budget, with full inventory/boundary,
orientation, tracker-key and rollback safeguards. This is a next hypothesis,
not measured savings. All archives/guards verify; production and original H5
limits remain unchanged. No whole-job material improvement or H5 credit. 60%.
''')
note='''

**N4 assignment feasibility, 2026-10-18:** [three independently valid source packings](../benchmarks/results/h5-assignment-repack-20261018.md)
fit the unchanged saved boundaries and quantities: both large-plate cases and
the 0.2 mm panel case. The 1.5 mm panel case remains unresolved after six retained
rounds. This proves only source-assignment feasibility, not whole-job material
improvement. Earlier traces repeat eight distinct assignments over 25 attempts
(17 repeats after first occurrence). Next test retained compatible repair progress
within the existing shared budget, preserving geometry/orientation identities,
tracker-key consistency, rollback and independent acceptance. No production change
or relaxed gate; H2/H5 remain open at 60%.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,note)
status.write_text(status_text.replace(marker,note.strip()+'\n\n'+marker),encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'finish.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print(json.dumps(verification))
