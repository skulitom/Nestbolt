from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-return-capacity-diagnosis-20261017'
load=lambda p:json.loads(p.read_bytes())
audit=load(out/'independent-capacity-audit.json');summary=load(out/'summary.json');verification=load(out/'verification.json')
rows=audit['records']
assert summary['all_valid'] and verification['valid']==4 and verification['all_original_archives_and_traces_verified']
assert audit['attempts']==25 and audit['outcomes']=={'source_repair_failed':25}
assert audit['overfull_shortened_search_assignments']==audit['overfull_physical_full_sheet_assignments']==0
assert audit['results_sha256']==load(out/'records-integrity.json')['members']['results.json']['sha256']
assert audit['source_sha256']==sha256((out/'audit-capacity.py').read_bytes()).hexdigest()
assert all(r['frame_mode']=='reciprocal' for r in rows)
for row in rows:
    receiver=row['states']['receiver_repaired']['search_collision_polygons']
    assert receiver['pair_intersection_sum_mm2']==receiver['outside_area_sum_mm2']==0
    assert row['states']['source_repaired']['search_collision_polygons']['pair_intersection_sum_mm2']>1000
for figure in load(out/'figures.json')['figures']:
    assert sha256((out/figure['path']).read_bytes()).hexdigest()==figure['sha256']
source_overlap=[r['states']['source_repaired']['search_collision_polygons']['pair_intersection_sum_mm2'] for r in rows]
review={'all_25_attempts_complete_reciprocal_and_source_repair_failed':True,
    'independent_receiver_overlap_and_outside_zero_for_every_attempt':True,
    'source_repaired_pair_intersection_sum_range_mm2':[min(source_overlap),max(source_overlap)],
    'source_search_area_occupancy_percent_range':[100*v for v in audit['source_search_area_ratio_range']],
    'full_stock_filled_outer_area_occupancy_percent_range':[100*v for v in audit['source_full_stock_area_ratio_range']],
    'area_only_infeasibility_established':False,'assignment_feasibility_established':False,
    'next_scope':'Test a complete repack of fixed saved source assignments with the exact original shortened boundary, all parts and legal orientations. Preserve a precommitted selection and every outcome; require independent geometric validation before calling any packing a feasibility witness. A failed finite search cannot prove impossibility.',
    'visual_review':'All four corrected first-attempt figures inspected. Initial returns are identified by unchanged identity/pose multisets; repaired copies are deliberately unlabelled. Original mistaken cross-snapshot key coloring is preserved with its review. Numeric audits and geometry are unaffected.',
    'production_changed':False,'quality_claim':False,'H5_complete':False,'completed_weight_percent':60}
(out/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
report=out.parent/(out.name+'.md');s=report.read_text(encoding='utf-8')
s=s.replace('# Return-sheet capacity and repair diagnosis — 2026-10-17','# Return-sheet capacity and repair diagnosis — 2026-10-18')
report.write_text(s,encoding='utf-8',newline='\n')
lines=['\n\n## Independent capacity and geometry review','',
    'All 25 complete-set attempts use allowed reciprocal frames and fail at',
    'return-sheet repair. The saved geometry independently confirms zero overlap',
    'and zero outside area on every repaired receiver. Every repaired return sheet',
    f'still has substantial pairwise intersection area ({min(source_overlap):,.3f}–{max(source_overlap):,.3f} mm²).','',
    'Summed collision-polygon area is **75.281–85.554%** of the actual shortened',
    'container area. Original filled outer-ring area is **15.962–47.573%** of full',
    'usable physical stock. **Neither area bound establishes infeasibility.**',
    'These bounds also do not establish that the shapes can be packed. All initial',
    'source assignments have both overlap and outside area; the final snapshots',
    'retain overlap even when outside area reaches zero.','',
    '| Job | Kerf mm | Attempts | Shortened-area occupancy | Repaired source pairwise overlap sum (mm²) |',
    '| --- | ---: | ---: | ---: | ---: |']
for job in ['m-mechanical-large-plates','m-mechanical-panel-hardware']:
    for kerf in [.2,1.5]:
        selected=[r for r in rows if r['job']==job and r['kerf_mm']==kerf]
        fill=[r['source_search_area_ratio']*100 for r in selected]
        overlap=[r['states']['source_repaired']['search_collision_polygons']['pair_intersection_sum_mm2'] for r in selected]
        lines.append(f'| {job} | {kerf} | {len(selected)} | {min(fill):.3f}–{max(fill):.3f}% | {min(overlap):,.3f}–{max(overlap):,.3f} |')
lines+=['',
    'The [independent audit](h5-return-capacity-diagnosis-20261017/independent-capacity-audit.json)',
    'uses Shapely 2.1.2 on saved polygons and original filled outer rings, including',
    'public transforms. Exact analytic checks cover mirrored rotation, outside',
    'area, ignored area hints and an overfull overlap example. Raw positive',
    'intersections and outside areas remain available; these diagnostic magnitudes',
    'do not change the public validator or any acceptance tolerance.','',
    'The next step is a separately planned complete repack of fixed saved source',
    'assignments, keeping their boundary, parts and allowed orientations. A valid',
    'packing would supply an actual feasibility witness before modifying repair.',
    'A failed bounded search would still not prove impossibility. The balanced',
    'two-to-three authored witness remains useful but proves no mechanical gain.','',
    'Complete expanded records total 328 MB and are retained byte-for-byte in',
    '[original-records.zip](h5-return-capacity-diagnosis-20261017/original-records.zip),',
    'with [member hashes and CRC verification](h5-return-capacity-diagnosis-20261017/records-integrity.json).',
    'The [compact index](h5-return-capacity-diagnosis-20261017/summary.json) points',
    'to each immutable original attempt archive and full stderr trace. Extract',
    '`records.json` and `results.json` here before using the retained reproduction',
    'helpers; the exact expanded files remain locally and are ignored by Git.','',
    'The first attempted exchange in each of the four cases is plotted with equal',
    'axes. Orange marks returned parts only in the initial view; repaired copies',
    'are unlabelled because snapshot keys are not stable copy identities. An',
    'initial coloring mistake is preserved in `figure-key-review/` with its',
    'correction; it never affected geometry or numeric conclusions. All corrected',
    'figures have been inspected.','',
    '![Large plates, 0.2 mm, first return assignment](h5-return-capacity-diagnosis-20261017/m-mechanical-large-plates-0p2-first-attempt.png)','',
    '![Panel hardware, 0.2 mm, first return assignment](h5-return-capacity-diagnosis-20261017/m-mechanical-panel-hardware-0p2-first-attempt.png)','',
    'No production change, repeated quality pilot, relaxed threshold or H5 credit.',
    '**60% complete; H2 and H5 remain open.**','']
append(report,'\n'.join(lines))
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Return-sheet area bounds do not explain the failed repairs

[Four diagnostic outcomes](benchmarks/results/h5-return-capacity-diagnosis-20261017.md)
validate in {summary['wall_seconds']:.3f} seconds, with unchanged inputs/source/binary,
all quantities/metrics/exports, matching traces and immutable archive hashes.
All 25 complete-set attempts use permitted reciprocal frames; every receiver
repairs, and every return sheet retains substantial overlap. Independent Shapely
checks confirm zero receiver overlap/outside area and source pairwise overlap
sums of {min(source_overlap):,.3f}–{max(source_overlap):,.3f} mm² after repair.

Source collision-area occupancy is 75.281–85.554% of the actual shortened sheet;
original filled outer area is 15.962–47.573% of full usable stock. No assignment
exceeds either simple area bound. This proves neither feasibility nor global
impossibility. Next seek an independently valid full repack of fixed saved
assignments before changing repair. A failed bounded repack cannot prove
impossibility. Trace overhead may perturb deadlines; no quality claim is made.

Complete expanded records are archived byte-for-byte with CRC/member hashes;
the compact index links to all full traces. Four first-attempt figures were
inspected; an initial snapshot-key coloring mistake is retained and corrected
without changing geometry or numeric analysis. Production and original failed
pilots remain unchanged. H2/H5 remain open at 60%.
''')
note='''

**N4 capacity diagnosis, 2026-10-18:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-capacity-diagnosis-20261017.md)
record 25 complete reciprocal attempts. Independent geometry checks confirm
clear repaired receivers and overlapping repaired return sheets. Source area
occupancy is 75.281–85.554% of the actual shortened search boundary: area alone
does not prove infeasibility, and occupancy alone does not prove a packing exists.
Next seek a complete, independently valid repack of fixed saved assignments with
their original boundary and legal orientations before changing repair. Preserve
all failed outcomes; no production change, relaxed limit or H5 credit. 60% complete.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 balanced-group witness, 2026-10-17:**';assert s.count(needle)==1
s=s.replace(needle,note.strip()+'\n\n'+needle).replace('# Status — 2026-10-17','# Status — 2026-10-18')
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print(json.dumps(review))
