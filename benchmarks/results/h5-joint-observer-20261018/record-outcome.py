"""Record the verified diagnostic and a concrete frontier-target hypothesis."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from datetime import datetime,timezone
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-joint-observer-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
v=load(out/'verification.json');g=load(out/'geometry-checks/checks.json')
e=load(out/'observed-exchanges.json');r=load(out/'results.json');front=load(out/'source-frontiers.json')
assert v['valid']==4 and v['all_traces_verified'] and v['all_original_archives_verified']
assert g['all_checks_passed'] and g['all_material_values_exact'] and front['all_saved_selected_copy_checks_passed']
s=e['summary'];assert s['attempts']==15 and s['accepted']==s['committed']==5
panel=[p for p in g['source_lowering'] if p['archive'].startswith('m-mechanical-panel-hardware')]
assert len(panel)==6 and all(p['source_top_reduction_mm']==0 for p in panel)
tiny=[a for a in e['attempts'] if a['material_gain_mm2'] is not None and -0.01<a['material_gain_mm2']<0]
assert len(tiny)==2 and all(not a['net_source_changes_from_baseline'] for a in tiny)
panel_front=[x for x in front['records'] if x['job']=='m-mechanical-panel-hardware' and x['exposed_band_height_mm']>1e-7]
assert len(panel_front)==4 and all(x['exposed_band_height_mm']==10.9013671875 for x in panel_front)
followup=(
    "The next distinct hypothesis is a source boundary derived from the actual selected copies. "
    "When removing the selected top copies exposes a lower boundary, use the existing fitted-container calculation on that remaining source as an explicit target for joint repair. "
    "Displaced return members must fit below that target or migrate to the receiver, with both exact containers and the original whole job validated. "
    "The current joint helper receives the original window crop and can finish immediately after returning equal inserts to the just-vacated top band. "
    "In the panel traces, the selected top pair exposes a 10.901367 mm band, but all six lowering stages leave the source top unchanged. "
    "This motivates a target; it does not prove the returned parts fit or that the search will find a packing. "
    "First author or capture a case where existing repair restores the top band and actual targeted joint repair finds an independently valid lower layout. "
    "Preserve the short phase, total deadline, validation reserve, cap, exact crop checks, quantity/orientation accounting, frozen sheets, reserved holes, strict final material guard and rollback. "
    "Qualify that changed policy before another matched pilot. Do not relax the material guard for the tiny increases, repeat the unchanged quality pilot or increase the cap blindly.")
interpretation={'results_sha256':digest(out/'results.json'),'observations_sha256':digest(out/'observed-exchanges.json'),
    'geometry_checks_sha256':digest(out/'geometry-checks/checks.json'),'source_frontiers_sha256':digest(out/'source-frontiers.json'),
    'actual_extra_net_migration_observed':True,'completed_pair_repairs':10,'completed_with_extra_net_migration':8,
    'accepted_steps':5,'all_accepted_steps_committed':True,'accepted_with_extra_net_migration':5,
    'panel_lowering_stages':6,'panel_lowering_stages_with_height_reduction':0,
    'tiny_material_increase_trials':[{'archive':a['archive'],'attempt_id':a['attempt_id'],
        'material_increase_mm2':-a['material_gain_mm2'],'source_inventory_unchanged':True} for a in tiny],
    'selected_panel_pair_exposed_band_mm':10.9013671875,'followup':followup,
    'packing_feasibility_proven':False,'quality_claim':False,'earlier_pilot_trajectory_reconstructed':False,
    'source_files':{p:digest(root/p) for p in [
        'output/h5-joint-repair-probe-20261018/candidate/crates/core/src/sheets/vstrip.rs',
        'output/h5-joint-repair-probe-20261018/candidate/crates/core/src/sheets/vstrip/exchange.rs']}}
write(out/'interpretation.json',interpretation)
ci=json.loads(subprocess.check_output(['gh','run','view','39124897846','--json','status,conclusion,headSha,jobs,url'],cwd=root))
assert ci['headSha']=='e0945cd811259086fe3791a97c91cc86550b8abf'
assert ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in ci['jobs'])
write(out/'main-ci-e0945cd.json',{'observed_utc':datetime.now(timezone.utc).isoformat(),'run':ci})
lines=['# Actual joint-repair diagnosis — 2026-10-18','',
    '**Extra-member migration works, but most observed gains are small and panel lowering does not reduce height.**','',
    'Four serial diagnostics retain the two mechanical development jobs, both',
    'kerfs, seed zero, 60 seconds and physical CCD0 CPU 8. The qualified observer',
    'preserves decision logic, deadlines and charged work. Logging can change wall',
    'trajectories; these are diagnostic observations, not a quality or speed comparison.',
    f"The session takes {r['wall_seconds']/60:.3f} minutes. All four final layouts and public exports validate.",'',
    '## What happened','',
    'Fifteen joint attempts produce ten completed repairs and five expiries:',
    'three during separation and two during source lowering. Five completed',
    'repairs commit; five are rejected because whole-job material increases.',
    'The material increase itself is observed; concurrent expiry is not sampled',
    'separately on that short-circuit branch. Eight completed repairs change the',
    'source inventory beyond the initial swap, including all five accepted repairs.',
    'Net part-type counts can miss same-family copy swaps that cancel.','',
    '| Job | Kerf | Attempts | Completed | Committed | Material-increase rejection | Expired |',
    '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for job in ['m-mechanical-large-plates','m-mechanical-panel-hardware']:
    for kerf in [0.2,1.5]:
        rows=[a for a in e['attempts'] if a['job']==job and a['kerf_mm']==kerf]
        lines.append(f"| {job} | {kerf} | {len(rows)} | {sum(a['pair_outcome']=='completed' for a in rows)} | {sum(a['committed'] for a in rows)} | {sum(a['resolved_reason']=='material_increase' for a in rows)} | {sum(a['pair_outcome'].endswith('_expired') for a in rows)} |")
lines += ['', 'The five committed step gains are **455.576, 33,589.956, 124.047,',
    '512.421 and 982.543 mm²**. They are individual before/after differences,',
    'not a claim about final pilot improvement or an additive whole-job saving.',
    'All six observed panel lowering stages leave the source top unchanged, even',
    'though four change between four and eleven source poses. Two other lowering',
    'stages expire without moving a source pose.','',
    'Two panel trials with unchanged source inventories increase material by only',
    '0.00375 and 0.0025 mm². Independent reconstruction reproduces the exact',
    'validator values. They remain rejections; no tolerance or scoring exception',
    'is introduced. Their selected and returned groups are both pairs of inserts.',
    'The same-part swap by itself does not demonstrate useful inventory progress.','',
    '## Verified geometry and next target','',
    f"All {g['CLI_checks']} unique saved baselines, trials, repaired pairs and final layouts",
    f"independently validate. The filled-outer audit checks {g['filled_outer_pairs']:,} pairs",
    f"at the unchanged 1e-7 mm tolerance. All {g['whole_job_material_recomputations']} whole-job material values are",
    'recomputed exactly from original transformed outer vertices and stock dimensions.',
    'Nonselected and frozen sheets remain exact. Component pair checks use selected',
    'quantities and full original stock geometry; original whole-job availability',
    'and the native exact-crop checks remain separately authoritative.','',
    'Exact physical-pose matching identifies the selected copies. Twelve of the',
    'fifteen selections expose a lower source boundary when removed, ranging from',
    '0.082271 to 22.456299 mm. Four panel selections expose 10.901367 mm.',
    'These are conditional geometric opportunities before returned members are',
    'placed, not constructed layouts or proof of achievable saving.','',followup,'',
    '[All observations](h5-joint-observer-20261018/observed-exchanges.json),',
    '[independent geometry](h5-joint-observer-20261018/geometry-checks/checks.json),',
    '[selected-copy frontiers](h5-joint-observer-20261018/source-frontiers.json),',
    '[interpretation](h5-joint-observer-20261018/interpretation.json) and',
    '[original archive verification](h5-joint-observer-20261018/verification.json).','',
    'All six hosted checks on main `e0945cd` pass, including Windows, Linux,',
    'browsers and both maker rebuilds. That confirms the pushed checkpoint,',
    'not the quality of this isolated experiment. [Hosted checks](h5-joint-observer-20261018/main-ci-e0945cd.json).',
    'Production and v0.2.0-alpha.1 remain unchanged. All three READMEs remain',
    'accurate; no new qualified application build is ready to release.',
    'H2/H5 remain open, with completed milestone weight 60%.','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
note=f'''**N4 actual joint-repair diagnosis, 2026-10-18:** [all four serial diagnostics validate](../benchmarks/results/h5-joint-observer-20261018.md).
Fifteen attempts yield ten completed repairs, five committed steps, five
material-increase rejections and five expiries. Eight completed repairs move
extra members beyond the proposed swap, including all five accepted repairs.
Independent checking validates 40 saved layouts and 173,333 filled-outer pairs;
all 21 whole-job material values reconstruct exactly. Panel lowering never
reduces the source top in six observed stages. Four selected panel top pairs
expose a 10.901367 mm band when removed, before returns are placed. This motivates
an explicit source-boundary target, subject to an actual valid witness and full
qualification; it does not establish feasibility. Original limits, failures and
production remain unchanged. All six checks on pushed main `e0945cd` pass.
No quality/release claim or H5 credit; H2/H5 remain open at 60%.
'''
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/')+'\n'+followup+'\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n'+note)
status=root/'docs/STATUS.md';old=status.read_text(encoding='utf-8')
a=old.index('**N4 joint-repair observation plan, 2026-10-18:**');b=old.index('**N4 joint-repair outcome, 2026-10-18:**',a)
status.write_text(old[:a]+note+'\n'+old[b:],encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
write(out/'source-review.json',interpretation|{'integrated':False,'H5_complete':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'record-outcome.py')
print(json.dumps({'valid_diagnostics':4,'completed_repairs':10,'committed_steps':5,'main_ci_all_six_passed':True,'next':'Authored witness for explicit source-frontier target'}))
