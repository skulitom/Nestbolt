from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h5-outline-construction-20261018'
BEAM=ROOT/'output/h5-outline-beam-20261018';FILL=ROOT/'output/h5-outline-backfill-20261018'
AUDIT=ROOT/'output/h5-outline-audit-recovery-20261018';FAILED=ROOT/'output/h5-outline-audit-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest


def write(p,value):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(value,f,indent=2);f.write('\n')


def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)


def main():
    OUT.mkdir();beam=load(BEAM/'results.json');fill=load(FILL/'results.json');audit=load(AUDIT/'checks.json')
    assert beam['complete'] and fill['complete'] and audit['all_checks_passed']
    assert audit['whole_layouts_complete']==0 and len(audit['public_checks'])==8
    assert all(not r['CLI_valid'] and r['only_expected_quantity_rejections'] for r in audit['public_checks'])
    assert sum(r['reused_original_output'] for r in audit['public_checks'])==1
    assert sum(r['candidate_additions'] for r in beam['cases'])==159819
    assert sum(r['candidate_attempts'] for r in fill['cases'])==573
    assert sum(r['added_parts'] for r in fill['cases'])==74
    assert sum(r['expired'] for r in beam['cases'])==2
    assert not any(r['complete_layout_found'] for r in beam['cases']+fill['cases'])
    assert source_digest()=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
    helper=ROOT/'output/h5-frontier-probe-20261018/candidate/crates/core/src/sheets/vstrip/exchange.rs'
    model=ROOT/'output/h5-frontier-probe-20261018/candidate/crates/core/src/sheets.rs'
    construct=ROOT/'output/h5-frontier-probe-20261018/candidate/crates/core/src/construct.rs'
    assert 'fn joint_repair_pair(' in helper.read_text(encoding='utf-8')
    records=[]
    for b,f in zip(beam['cases'],fill['cases']):
        assert b['case']==f['case']
        folder=FILL/f['case'];job=load(folder/'job.json');layout=load(folder/'layout.json')
        magnitude=max([abs(x) for p in job['parts'] for g in p['geometry'] for point in g['outer'] for x in point]+[v for st in job['stocks'] for v in [st['width'],st['height']]])
        guard=max(magnitude*32*2**-23,.00002)
        records.append({'case':f['case'],'beam_orders_started':len(b['runs']),'beam_expired':b['expired'],
            'beam_additions':b['candidate_additions'],'added_without_moving_existing':f['added_parts'],
            'remaining':f['remaining'],'remaining_filled_area_mm2':f['remaining_filled_area_mm2'],
            'placed_parts':len(layout['placements']),'requested_parts':sum(p['quantity'] for p in job['parts']),
            'partial_layout_sha256':digest(folder/'layout.json'),'native_conversion_guard_mm':guard})
    # The original public rejection is reused, not replaced with a new result.
    old=FAILED/'beam-m-mechanical-large-plates-k0.2-s0-candidate'
    recovered=AUDIT/old.name
    assert (old/'stdout.json').read_bytes()==(recovered/'stdout.json').read_bytes()
    assert (old/'layout.json').read_bytes()==(recovered/'layout.json').read_bytes()
    failure=load(FAILED/'failure.json');assert 'NoneType' in failure['error']
    recovery={'original_failure':'Audit expected metrics on a correctly rejected incomplete layout; the validator returns metrics=null for quantity violations.',
        'original_failure_sha256':digest(FAILED/'failure.json'),'original_rejection_sha256':digest(old/'stdout.json'),
        'original_rejection_reused_byte_for_byte':True,'correction':'Require only the exact original quantity rejections and independently audit geometry; do not treat incomplete layouts as valid complete results.',
        'new_packing_searches':0,'original_search_results_unchanged':True}
    write(OUT/'audit-recovery.json',recovery)
    followup=('The closest saved construction places 63/66 large-plate parts and is missing three cogs; all four still fail '
        'the original quantity requirement. Do not integrate the constructor or run another quality pilot. The current '
        'diagnosis keeps every placed neighbour fixed during backfill, so it cannot resolve the remaining obstructions '
        'through collective movement. Next prepare an isolated real-job witness using the existing joint_repair_pair '
        'helper on these saved layouts, with all original quantities restored in explicitly overlapping provisional poses '
        'and both original target containers enforced. First measure model conversion/collision loss separately: these '
        'physical-geometry placements have only 0.0011 mm extra separation, while native conversion_guard is '
        '0.011444091796875 mm / 0.0095367431640625 mm for these stocks. Do not assume that independently legal partial '
        'geometry starts with zero native proxy loss or shrink that guard. Preserve provisional overlaps and every '
        'failed/expired repair. Use the existing authored witness allowance and seed as a mechanism test, not a changed '
        'H5 budget or quality comparison. Only a fully populated result that passes original library/request, filled-outer '
        'and exact target-material checks can establish feasibility. Production budgets, four-step repair cap, hole '
        'reservation, material limits and held-out isolation remain unchanged.')
    review={'followup':followup,'runtime_changed':False,'whole_job_feasibility_proven':False,'H5_complete':False,
        'native_helper':str(helper.relative_to(ROOT)),'native_helper_sha256':digest(helper),
        'model_source':str(model.relative_to(ROOT)),'model_source_sha256':digest(model),
        'conversion_source':str(construct.relative_to(ROOT)),'conversion_source_sha256':digest(construct),
        'limits':'Finite contact candidates, six beam states, four ordering heuristics, compound orientation constraints, and two retained diagnostic timeouts. Standalone mirrored parts are added only in backfill. These results do not prove geometric infeasibility, runtime quality or a speed ranking.'}
    write(OUT/'source-review.json',review)
    phases=[BEAM,FILL,FAILED,AUDIT];manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for folder in phases:
            for p in sorted(folder.rglob('*')):
                if p.is_file():
                    rel=folder.name+'/'+p.relative_to(folder).as_posix();z.write(p,rel)
                    manifest.append({'path':rel,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={r['path'] for r in manifest}
        for r in manifest:assert sha256(z.read(r['path'])).hexdigest()==r['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest})
    summary={'verified_utc':datetime.now(timezone.utc).isoformat(),'all_stated_scope_checks_passed':True,
        'cases':records,'beam_candidate_additions':159819,'beam_cross_pairs':sum(r['candidate_pairs'] for r in audit['beam']),
        'backfill_candidate_additions':573,'backfill_cross_pairs':sum(r['candidate_pairs'] for r in audit['backfill']),
        'total_saved_final_pairs':sum(r['saved_best_pairs'] for r in audit['beam'])+sum(r['saved_final_pairs'] for r in audit['backfill']),
        'original_public_completeness_rejections':8,'complete_layouts':0,'backfilled_parts':74,
        'absolute_clearance_tolerance_mm':1e-7,'all_existing_backfill_poses_exact':True,
        'production_digest':source_digest(),'raw_archive_sha256':digest(archive),'raw_members':len(manifest),
        'new_Nestbolt_searches':0,'H5_complete':False,'completion_percent':60}
    write(OUT/'checks.json',summary)
    shutil.copyfile(FILL/records[0]['case']/'layout-map.png',OUT/'closest-partial.png')
    for name in ['seal_h5_outline_constructions.py','prepare_h5_outline_audit_recovery.py','plot_h5_outline_backfill.py']:
        shutil.copyfile(ROOT/'output'/name,OUT/name)
    rows='\n'.join(f"| {r['case'].replace('m-mechanical-','').replace('-s0-candidate','')} | {r['placed_parts']}/{r['requested_parts']} | {', '.join(f'{n} {k}' for k,n in r['remaining'].items())} | {r['remaining_filled_area_mm2']:,.3f} |" for r in records)
    doc=f'''# Actual-outline construction and backfill — 2026-10-18

The [mixed-pattern diagnosis](h5-pattern-construction-20261018.md) tested enclosing
rectangles. This follow-up places the actual filled outer contours, using the same
four saved development jobs and unchanged stock/material targets. A six-state
constructive beam tests mixed and single-part inventories, four ordering heuristics,
three distinct contact points per orientation/sheet, quarter-turn compound rotation
and 15-degree free single-part angles. Every candidate addition keeps original
geometry and checks actual clearance. This is offline geometry work on CCD1;
no Nestbolt search or quality/timing comparison is rerun.

The two large-plate cases finish all eight ordering attempts without a full layout.
Both panel cases reach the explicit 120-second diagnostic ceiling during their
seventh attempt; those interruptions and skipped final orders are retained. The
ceiling does not change any runtime or H5 budget. All **159,819 candidate additions**
and **{summary['beam_cross_pairs']:,}** cross-part pairs replay from original-source vertices.

The fixed ordering stops at its first unplaceable part. A separate continuation
keeps every placed pose exact, ungroups missing compound copies, includes permitted
mirrors, and tries smaller remaining families when a larger family has no location.
It adds **74 parts** across 573 considered additions and {summary['backfill_cross_pairs']:,}
cross-part checks. Final partial outcomes are:

| Saved case | Parts placed | Still missing | Missing filled area (mm²) |
| --- | ---: | --- | ---: |
{rows}

**No complete target layout is found.** All eight saved beam/backfill outputs are
submitted to the original public library/request validator. It rejects each with
exactly the expected quantity violations and no geometry violations. Independent
all-pair checks of the saved outputs cover {summary['total_saved_final_pairs']:,} additional
pairs; every hole stays reserved at the unchanged 1e-7 mm clearance tolerance.
Geometrically legal partial layouts do not satisfy the original quantity gate.

The first audit incorrectly expected metrics on a rejected incomplete layout and
stopped on `metrics: null`. Its failure, source and rejection are preserved. The
corrected audit checks the exact quantity rejections, reuses that first validator
output byte-for-byte and verifies all candidates independently. No packing search
is repeated. All {len(manifest)} raw archive members, CRCs and byte hashes verify.

![Closest partial construction: three cogs remain unplaced](h5-outline-construction-20261018/closest-partial.png)

[Checks](h5-outline-construction-20261018/checks.json),
[raw attempts, partial layouts and validator output](h5-outline-construction-20261018/raw.zip),
[manifest](h5-outline-construction-20261018/raw-manifest.json),
[audit recovery](h5-outline-construction-20261018/audit-recovery.json),
[source review and next investigation](h5-outline-construction-20261018/source-review.json).

{followup}

H2/H5 remain open at **60%**. Production, release assets and all three READMEs
remain unchanged; this creates no new release candidate.
'''
    (OUT.parent/(OUT.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note='''**N4 actual-outline construction, 2026-10-18:** [the retained beam and backfill](../benchmarks/results/h5-outline-construction-20261018.md)
test actual filled outer contours. All 159,819 beam additions replay; both panel
diagnostic timeouts remain explicit. Backfill adds 74 parts without moving existing
poses. The closest case places 63/66 parts, missing three cogs; every case remains
incomplete. Eight original public checks reject exactly the missing quantities.
The audit's null-metrics handling failure is preserved and repaired without new
packing searches. Next investigate collective repair of these saved partials,
first accounting for the native conversion guard, rather than treating physical
clearance as proof of zero native proxy loss. No runtime, gate limit or release
change; H2/H5 remain open at 60%.
'''
    prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT)
    assert (ROOT/'BENCHMARKS.md').read_bytes()==prior
    append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/name,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 mixed-pattern diagnosis, 2026-10-18:**'
    assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes','\nbenchmarks/results/h5-outline-construction-20261018/** -text -whitespace\n')
    print(json.dumps({k:summary[k] for k in ['all_stated_scope_checks_passed','beam_candidate_additions','beam_cross_pairs','backfill_candidate_additions','backfill_cross_pairs','raw_members']}),flush=True)


if __name__=='__main__':main()
