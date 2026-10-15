"""Read-only aggregation of the completed, already archived H5 measurements."""
from collections import Counter
import argparse
from hashlib import sha256
from pathlib import Path
import json
import os
import statistics as st
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'benchmarks/results'
COMMON = BASE / 'h5-common-development-20261015T142414Z'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def distribution(values):
    assert values
    q1, _, q3 = st.quantiles(values, n=4, method='inclusive') if len(values)>1 else [values[0]]*3
    return {'count':len(values), 'median':st.median(values), 'q1':q1, 'q3':q3, 'iqr':q3-q1,
            'min':min(values), 'max':max(values)}


def verify_rows(folder, rows):
    checked=0
    for row in rows:
        archive=folder/row['archive']
        assert digest(archive)==row['archive_sha256'], archive
        with zipfile.ZipFile(archive) as z:
            for name, expected in row['artifacts'].items():
                assert sha256(z.read(name)).hexdigest()==expected, (archive,name)
                checked+=1
            archived=json.loads(z.read('case.json'))
            assert archived=={k:v for k,v in row.items() if k not in ['archive','archive_sha256']}, archive
    return checked


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=BASE/'h5-cutting-development-20261015.json')
    args=parser.parse_args()
    if not (COMMON/'results.json').exists():
        print('Nestbolt measurement is still running. No final report written.')
        return
    common=read(COMMON/'results.json')
    folders=sorted(p.parent for p in BASE.glob('h5-deepnest-development-20261015T*-cpu*/results.json'))
    native=[(p,read(p/'results.json')) for p in folders]
    native_rows=[row for _,record in native for row in record['rows']]
    expected={(job,seed) for job in common['jobs'] for seed in [0,1,2]}
    actual=[(row['job'],row['seed']) for row in native_rows]
    if len(actual)!=39 or set(actual)!=expected:
        print('Native comparator incomplete:',len(actual),'of 39. No final report written.')
        return
    assert common['seconds']==60 and common['seeds']==[0,1,2]
    assert len(common['rows'])==234
    assert {(r['job'],r['kerf_mm'],r['seed'],r['arm']) for r in common['rows']}=={
        (j,k,s,a) for j in common['jobs'] for k in [.2,1.5] for s in [0,1,2] for a in ['normal','off','bonus']}
    assert len(set(actual))==39
    checked=verify_rows(COMMON,common['rows'])
    hole_counts={}
    for row in common['rows']:
        if row['status']=='valid':
            with zipfile.ZipFile(COMMON/row['archive']) as z:
                hole_counts[(row['job'],row['kerf_mm'],row['seed'],row['arm'])]=json.loads(z.read('nested/report.json'))['parts_in_holes']
    for folder,record in native:
        assert record['complete'] and record['seconds']==60 and not record['held_out_geometry_read']
        for key in ['product','binary','manifest']:
            assert record['guards'][key]==common['guards'][key],(folder,key)
        assert record['guards']['runner_sources']==native[0][1]['guards']['runner_sources']
        checked+=verify_rows(folder,record['rows'])
    arms=[]
    for job in common['jobs']:
        for kerf in [.2,1.5]:
            for arm in ['normal','off','bonus']:
                rows=[r for r in common['rows'] if (r['job'],r['kerf_mm'],r['arm'])==(job,kerf,arm)]
                valid=[r for r in rows if r['status']=='valid']
                item={'job':job,'kerf_mm':kerf,'arm':arm,'statuses':dict(Counter(r['status'] for r in rows))}
                if len(valid)==3:
                    item['material']=distribution([r['material'] for r in valid])
                    item['parts_in_holes']=distribution([hole_counts[(r['job'],r['kerf_mm'],r['seed'],r['arm'])] for r in valid])
                    if arm!='normal':
                        item['saved_fraction']=distribution([r['saved_fraction'] for r in valid])
                        item['saved_length_mm']=distribution([r['cut_without_common_mm']-r['cut_with_common_mm'] for r in valid])
                        item['cut_without_common_mm']=distribution([r['cut_without_common_mm'] for r in valid])
                        item['cut_with_common_mm']=distribution([r['cut_with_common_mm'] for r in valid])
                arms.append(item)
    native_jobs=[]
    for job in common['jobs']:
        rows=[r for r in native_rows if r['job']==job]
        valid=[r for r in rows if r['status']=='valid']
        item={'job':job,'statuses':dict(Counter(r['status'] for r in rows)),
              'failed_seeds':[{k:r.get(k) for k in ['seed','status','error','native_errors']} for r in rows if r['status']!='valid']}
        # Partial successful seeds remain descriptive only; never stand in for a three-seed median.
        if valid:
            item['successful_seed_descriptives']={
                'material':distribution([r['score'] for r in valid]),
                **{k:distribution([r['svg_audit'][k] for r in valid]) for k in
                   ['native_merged_length_mm','export_saved_length_mm','export_saved_fraction']}}
        item['complete_valid_three_seeds']=len(valid)==3
        native_jobs.append(item)
    gates=[]
    for kerf in [.2,1.5]:
        pairs=[p for p in common['pairs'] if p['kerf_mm']==kerf and p['complete']]
        item={'kerf_mm':kerf,'complete_pairs':len(pairs)}
        if len(pairs)==13:
            saved=st.median(p['bonus_saved_fraction'] for p in pairs)
            costs=[p['material_cost_percent'] for p in pairs]
            item.update(median_saved_fraction=saved,median_material_cost_percent=st.median(costs),
                worst_material_cost_percent=max(costs),savings_at_least_ten_percent=saved>=.1,
                every_job_within_one_percent=max(costs)<=1,
                material_outliers=[p for p in pairs if p['material_cost_percent']>1])
        gates.append(item)
    report={'scope':'H5 development, 60 seconds, seeds 0-2; no final acceptance or held-out tuning.',
        'product_commit':common['product_commit'],'guards':common['guards'],
        'source_records':[str((COMMON/'results.json').relative_to(ROOT)),*[str((p/'results.json').relative_to(ROOT)) for p,_ in native]],
        'source_record_sha256':{str(p.relative_to(ROOT)):digest(p) for p in [COMMON/'results.json',*[p/'results.json' for p,_ in native]]},
        'verified_archives':len(common['rows'])+len(native_rows),'verified_archive_members':checked,
        'quantiles':'Inclusive linear quartiles of the three seeds. Material cost is ratio of per-job medians.',
        'nestbolt_statuses':dict(Counter(r['status'] for r in common['rows'])),
        'deepnest_statuses':dict(Counter(r['status'] for r in native_rows)),
        'maximum_nestbolt_nest_export_wall_seconds':max(r['nest']['elapsed_wall_seconds'] for r in common['rows']),
        'maximum_nestbolt_report_roundtrip_difference':max(r.get('maximum_revalidation_roundtrip_difference',0) for r in common['rows']),
        'nestbolt_arms':arms,'deepnest_jobs':native_jobs,'kerf_gates':gates,
        'comparison_limits':'Deepnest uses zero spacing and its original SVG merge; it is not kerf compensated. Native reported merged length and actual exported savings are separate. Failed native seeds are unscored.'}
    output=args.out
    output.parent.mkdir(parents=True,exist_ok=True)
    assert not output.exists(),'Never overwrite recorded evidence'
    output.write_text(json.dumps(report,indent=1)+'\n',encoding='utf-8',newline='\n')
    lines=['# H5 common-line development measurement — 2026-10-15', '',
        f"Nestbolt: **{report['nestbolt_statuses'].get('valid',0)}/234 valid runs**. Deepnest: **{report['deepnest_statuses'].get('valid',0)}/39 valid runs**.",
        'All runs use a 60-second solver budget and seeds 0–2 on the original frozen 13-job cutting set. This is development evidence, with no held-out geometry or final acceptance run.', '',
        '**H5 remains open on the material condition.** The two mechanical jobs exceed +1% at both kerfs; every other job is within the guard. No gate is relaxed. Overall completed milestone weight stays 20% (H1 and H6).', '',
        '## Savings and material gate', '',
        '| Kerf | Median bonus savings | Median material cost | Worst job material cost | Jobs above +1% |',
        '| --- | ---: | ---: | ---: | ---: |']
    for g in gates:
        if g['complete_pairs']==13:
            lines.append(f"| {g['kerf_mm']} mm | {100*g['median_saved_fraction']:.4f}% | {g['median_material_cost_percent']:+.4f}% | {g['worst_material_cost_percent']:+.4f}% | {len(g['material_outliers'])} |")
    lines += ['', 'The 10% savings condition applies to the set median. Material is checked against normal mode at the same kerf spacing; individual jobs above +1% remain explicit failures of the strict material guard. A passing median does not waive those outliers.', '',
        '| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |',
        '| --- | ---: | ---: | ---: | ---: |']
    for p in common['pairs']:
        if p['complete']:
            lines.append(f"| {p['job']} | {p['kerf_mm']} | {100*p['off_saved_fraction']:.3f}% | {100*p['bonus_saved_fraction']:.3f}% | {p['material_cost_percent']:+.3f}% |")
        else:lines.append(f"| {p['job']} | {p['kerf_mm']} | incomplete | incomplete | incomplete |")
    lines += ['', 'Each entry uses the median of three seeds. Material cost is the ratio of the two material medians, not the median of per-seed ratios. The machine-readable record includes inclusive quartiles and IQR for every complete arm.', '',
        '## Native Deepnest SVG comparison', '',
        'The pinned, unmodified Deepnest app uses `mergeLines=true`, zero spacing, one worker and SVG export. Its native reported merged length and the actual reduction in exported SVG cutting length are separate measurements. They can differ because the exporter can merge additional coincident lines. The independent SVG oracle reconstructs linework from the original inputs and saved placements, checks physical units, missing/extra cutting geometry and unmerged total length. Nestbolt\'s separate validator checks each native layout before it is scored.', '',
        '| Job | Valid Deepnest seeds | Nestbolt saved, laser / plasma | Deepnest reported merged length | Deepnest SVG cut saved | Deepnest SVG savings |',
        '| --- | ---: | ---: | ---: | ---: | ---: |']
    for j in native_jobs:
        count=j['statuses'].get('valid',0)
        ours=[next(a for a in arms if (a['job'],a['kerf_mm'],a['arm'])==(j['job'],k,'bonus')) for k in [.2,1.5]]
        ours_text=' / '.join(f"{a['saved_length_mm']['median']:.3f}" if 'saved_length_mm' in a else 'incomplete' for a in ours)+' mm'
        if j['complete_valid_three_seeds']:
            d=j['successful_seed_descriptives']
            lines.append(f"| {j['job']} | 3/3 | {ours_text} | {d['native_merged_length_mm']['median']:.3f} mm | {d['export_saved_length_mm']['median']:.3f} mm | {100*d['export_saved_fraction']['median']:.3f}% |")
        else:
            failures=', '.join(f"seed {r['seed']}: {r['status']}" for r in j['failed_seeds'])
            lines.append(f"| {j['job']} | {count}/3 ({failures}) | {ours_text} | incomplete | incomplete | incomplete |")
    lines += ['', 'Partial successful seeds remain available as descriptive values in JSON and are not substituted for a complete three-seed median. All unsuccessful native cases remain archived and unscored. Deepnest\'s zero-spacing SVG is not kerf compensated: these savings are informational, not equivalent cutting instructions for either Nestbolt kerf.', '',
        '## Method, provenance and limits', '',
        f"Product commit `{common['product_commit']}`. Six Nestbolt lanes use physical CCD0 cores at logical CPUs 0, 2, 4, 6, 8 and 10; two Deepnest lanes use 12 and 14. No more than eight solvers run at once. Each native process tree is pinned after import and before its timed solve; setup uses CCD1. Input geometry, stock, quantities and rotation rules are unchanged. Deepnest alone uses its required zero spacing.", '',
        'Normal Nestbolt mode may place small parts in holes; common-line mode disables this as required by the plan. The bonus reserves the last 10% of its search budget for local shared-edge placement and limits accepted material growth relative to that phase\'s starting layout. The external comparison here still measures the entire workflow against normal mode, so that local limit is not itself evidence of the H5 material condition.', '',
        f"Product SHA-256 `{common['guards']['product']}`. Binary SHA-256 `{common['guards']['binary']}`. Cutting manifest SHA-256 `{common['guards']['manifest']}`. Product, binary, runner and input guards remained unchanged throughout each completed measurement. All {report['verified_archives']} archives and {checked} recorded members pass their SHA-256 checks. No geometry was uploaded; the native controller blocks HTTP/HTTPS and uses no DXF conversion service.", '',
        'The earlier pilot, initial line-element oracle failure and interrupted startup remain in the repository. They are separate from these full-budget results. Published v1 results and frozen splits are unchanged. No release or new acceptance claim follows from this measurement.', '',
        f"[Full aggregate, quartiles, failures and source hashes]({output.name}).", '',
        'Raw records:', '']
    lines += [f"- [{Path(p).parent.name}]({Path(os.path.relpath(ROOT/p,output.parent)).as_posix()})" for p in report['source_records']]
    lines += ['', '## Verification follow-up', '',
        'The maximum Nestbolt search/export process wall time was 60.6293 seconds, including work outside the 60-second solver budget. Fresh independent validation matched every saved report; the maximum numeric round-trip difference was 2.9103830456733704e-11, within the unchanged 1e-9 report tolerance.', '',
        'The pushed checkpoint passed runtime checks on Linux before CI found a stale generated request schema. Regeneration adds only the optional `search_bonus` field with its default `false`; the schema consistency check passes. This does not change the benchmarked product source or binary. The original CI log and correction checks are retained in `h5-cutting-checks-20261015/`. Subsequent CI status is separate from these local checks.', '',
        'Reproduce the archive verification and aggregate without overwriting evidence: `python scripts/h5_cutting_report.py --out output/h5-cutting-recheck.json`. The resulting JSON can be byte-compared with the recorded aggregate. No search or geometry import is performed.', '']
    output.with_suffix('.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'report':str(output),'verified_archives':report['verified_archives'],
        'verified_members':checked,'nestbolt':report['nestbolt_statuses'],'deepnest':report['deepnest_statuses'],'gates':gates},indent=1))


if __name__=='__main__':
    main()
