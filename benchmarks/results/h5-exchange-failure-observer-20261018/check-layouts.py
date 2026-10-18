"""Validate saved baselines and identify observed coverage of height-setting families."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import ast,itertools,json,math,shutil,subprocess,sys,traceback,zipfile
import shapely
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exchange-failure-observer-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(root/'scripts'));import h5_exchange_failure_observer as observer
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
assert load(out/'verification.json')['all_original_archives_verified']
cli=root/'target/release/nestbolt.exe';expected='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b';assert digest(cli)==expected
tolerance=1e-7;sources={}
for name,functions in [('output/check_h5_larger_stage_layouts.py',['filled_geometry']),('output/inspect_h5_neutral_heights.py',['rounded','heights'])]:
    p=root/name;tree=ast.parse(p.read_text(encoding='utf-8'));sources[name]=digest(p)
    for fn in functions:
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==fn)
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'))
folder=out/'baseline-layouts';folder.mkdir();records=[];finals=[]
try:
    for row in load(out/'results.json')['records']:
        archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None;job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
        assert job['clearance']==row['kerf_mm'];finals.append({'archive':row['archive'],**filled_geometry(job,layout)})
        for invocation,trace in enumerate(row['diagnosis']['traces']):
            base=trace['baseline'];assert base['job']==job;layout=base['layout'];metrics=base['metrics']
            case=folder/f"k{row['kerf_mm']}-i{invocation}";case.mkdir()
            write(case/'job.json',job);write(case/'layout.json',layout)
            args=[str(cli),'validate','--job',str(case/'job.json'),'--layout',str(case/'layout.json')]
            r=subprocess.run(args,capture_output=True,timeout=60)
            (case/'stdout.json').write_bytes(r.stdout);(case/'stderr.log').write_bytes(r.stderr);write(case/'command.json',{'command':args,'exit_code':r.returncode})
            checked=json.loads(r.stdout);assert r.returncode==0 and checked['valid'] and checked['metrics']==metrics
            geometry=filled_geometry(job,layout)
            material,highest,poses,charged=heights(job,layout);assert material==metrics['material_area']
            credit=next(s for s in charged if s['sheet']==metrics['last_sheet_id'])
            assert credit['saving']==max(s['saving'] for s in charged)
            families=sorted({o['part_id'] for o in credit['owners']})
            choices=trace['choices']
            matching=[i for i,c in enumerate(choices) if any(n in families for n in c)]
            visited=sorted({v['choice_index'] for v in trace['visits'] if v['choice_index'] in matching})
            attempts=[a for a in trace['attempts'] if a['choice_index'] in matching]
            observer.check_traces([trace])
            owner_keys={observer.pose_key({'part_id':p['part_id'],'transform':p['transform']}) for p in credit['owners']}
            choice_keys=[{observer.pose_key(p) for p in c} for c in trace['choice_poses']]
            exact_choices=[i for i,keys in enumerate(choice_keys) if keys & owner_keys]
            complete_choices=[i for i,keys in enumerate(choice_keys) if owner_keys<=keys]
            exact_visits=sorted({v['choice_index'] for v in trace['visits'] if v['choice_index'] in exact_choices})
            complete_visits=sorted({v['choice_index'] for v in trace['visits'] if v['choice_index'] in complete_choices})
            exact_attempts=[a for a in trace['attempts'] if a['choice_index'] in exact_choices]
            complete_attempts=[a for a in trace['attempts'] if a['choice_index'] in complete_choices]
            record={'kerf_mm':row['kerf_mm'],'invocation':invocation,'path':case.relative_to(out).as_posix(),
                'material_exact':material,'source_sheet':base['source_sheet'],'credited_sheet':credit['sheet'],
                'credited_is_source':credit['sheet']==base['source_sheet'],'credited_height':credit['used_height'],
                'height_owners':credit['owners'],'height_families':families,
                'matching_choice_indices':matching,'matching_visited_indices':visited,
                'attempts_with_height_family':len(attempts),'attempt_outcomes_with_height_family':dict(Counter(a['outcome'] for a in attempts)),
                'height_copy_choice_indices':exact_choices,'height_copy_visited_indices':exact_visits,
                'all_height_copies_choice_indices':complete_choices,'all_height_copies_visited_indices':complete_visits,
                'attempts_with_actual_height_copy':len(exact_attempts),
                'attempt_outcomes_with_actual_height_copy':dict(Counter(a['outcome'] for a in exact_attempts)),
                'attempts_with_all_height_copies':len(complete_attempts),
                'attempt_outcomes_with_all_height_copies':dict(Counter(a['outcome'] for a in complete_attempts)),
                'all_attempts':len(trace['attempts']),'all_visited_indices':sorted({v['choice_index'] for v in trace['visits']}),
                'all_attempted_indices':sorted({a['choice_index'] for a in trace['attempts']}),
                'all_attempted_families':sorted({n for a in trace['attempts'] for n in choices[a['choice_index']]}),
                **geometry}
            records.append(record)
    assert len(finals)==2 and digest(cli)==expected
    result={'all_checks_passed':True,'final_layouts':len(finals),'baseline_layouts':len(records),
        'same_sheet_pairs':sum(r['same_sheet_pairs'] for r in records+finals),
        'absolute_clearance_tolerance_mm':tolerance,'shapely_version':shapely.__version__,'CLI_sha256':expected,
        'all_saved_material_values_exact':True,'all_credited_sheets_are_source':all(r['credited_is_source'] for r in records),
        'attempts_with_height_family':sum(r['attempts_with_height_family'] for r in records),
        'attempts_with_actual_height_copy':sum(r['attempts_with_actual_height_copy'] for r in records),
        'attempts_with_all_height_copies':sum(r['attempts_with_all_height_copies'] for r in records),
        'choice_poses_match_validated_baseline_exactly':True,
        'baselines':records,'finals':finals,'reused_function_source_sha256':sources,
        'limits':'Height reconstruction applies to these validated rectangular mm stocks. Every chosen physical pose uniquely matches the validated public source layout exactly. Actual top-copy coverage uses the independently reconstructed highest original contour vertices, separate from family coverage. Logging may alter trajectories. No quality or optimality claim.',
        'new_searches':0,'quality_claim':False}
    write(out/'layout-checks.json',result);shutil.copyfile(__file__,out/'check-layouts.py')
    print(json.dumps({k:v for k,v in result.items() if k not in ['baselines','finals','reused_function_source_sha256']}))

except BaseException:
    write(out/'layout-check-failure.json',{'error':traceback.format_exc(),'completed':records});raise
