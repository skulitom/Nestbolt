"""Independently validate every saved neutral pair; inspect exact public poses."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import ast,itertools,json,math,shutil,subprocess,sys,traceback,zipfile
import shapely
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exact-state-20261018'
sys.path.insert(0,str(root/'scripts'));import h5_exact_state as runner
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
assert load(out/'verification.json')['all_original_archives_verified']
cli=root/'target/release/nestbolt.exe';expected='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b';assert digest(cli)==expected
tolerance=1e-7
prior=root/'output/check_h5_larger_stage_layouts.py'
tree=ast.parse(prior.read_text(encoding='utf-8'));function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='filled_geometry')
exec(compile(ast.Module(body=[function],type_ignores=[]),str(prior),'exec'))
folder=out/'saved-layouts';folder.mkdir();records=[];pairs=[];finals=[];timings=[]
def check(job,view,name,expected_material=None):
    case=folder/name;case.mkdir();write(case/'job.json',job);write(case/'layout.json',view)
    args=[str(cli),'validate','--job',str(case/'job.json'),'--layout',str(case/'layout.json')]
    r=subprocess.run(args,capture_output=True,timeout=60)
    (case/'stdout.json').write_bytes(r.stdout);(case/'stderr.log').write_bytes(r.stderr)
    write(case/'command.json',{'command':args,'exit_code':r.returncode});assert r.returncode==0
    checked=json.loads(r.stdout);assert checked['valid'];material=checked['metrics']['material_area']
    if expected_material is not None:assert material==expected_material
    geometry=filled_geometry(job,view)
    row={'path':case.relative_to(out).as_posix(),'material':material,**geometry};records.append(row);return row
try:
    for row in load(out/'results.json')['records']:
        archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None;job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
        assert job['clearance']==row['kerf_mm'];finals.append({'archive':row['archive'],**filled_geometry(job,layout)})
        for invocation,t in enumerate(row['diagnosis']['traces']):
            attempts=t['attempts'];neutral=[a for a in attempts if a['outcome']=='neutral_inventory_rejected']
            timings.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'invocation':invocation,
                'all_attempts':len(attempts),'neutral_rejections':len(neutral),
                'exact_state_true':sum(a['exact_state'] is True for a in attempts),
                'exact_state_false':sum(a['exact_state'] is False for a in attempts),
                'neutral_validation_seconds':sum(a['validation_elapsed'] for a in neutral),
                'identity_seconds':sum(a['identity_elapsed'] or 0 for a in attempts),
                'invocation_seconds':t['total_elapsed'],'accepted':sum(a['outcome']=='accepted' for a in attempts)})
            for attempt,a in enumerate(attempts):
                if a['neutral_layouts'] is None:continue
                views=a['neutral_layouts'];name=f"k{row['kerf_mm']}-i{invocation}-a{attempt}"
                checked=[check(job,views[stage],name+'-'+stage,a['before_material']) for stage in ['incumbent','trial']]
                left=runner.public_signature(views['incumbent']);right=runner.public_signature(views['trial'])
                if a['exact_state']:assert left==right
                pairs.append({'kerf_mm':row['kerf_mm'],'invocation':invocation,'attempt':attempt,
                    'internal_exact_state':a['exact_state'],'public_pose_multisets_exact':left==right,
                    'public_incumbent_unmatched_poses':sum((left-right).values()),'public_trial_unmatched_poses':sum((right-left).values()),
                    'validation_seconds':a['validation_elapsed'],'identity_seconds':a['identity_elapsed'],
                    'layouts':checked,'proposal':t['proposals'][a['proposal_index']]})
            for view in t['layouts']:
                check(job,view['layout'],f"k{row['kerf_mm']}-i{invocation}-"+view['stage'])
    assert digest(cli)==expected and len(finals)==2
    assert len(pairs)==sum(t['neutral_rejections'] for t in timings)
    result={'all_checks_passed':True,'final_layouts':len(finals),'saved_layouts':len(records),'neutral_pairs':len(pairs),
        'internal_exact_pairs':sum(p['internal_exact_state'] for p in pairs),
        'public_exact_pairs':sum(p['public_pose_multisets_exact'] for p in pairs),
        'same_sheet_pairs':sum(r['same_sheet_pairs'] for r in records+finals),'absolute_clearance_tolerance_mm':tolerance,
        'shapely_version':shapely.__version__,'CLI_sha256':expected,'finals':finals,'saved':records,'pairs':pairs,'timings':timings,
        'filled_geometry_function_AST_reused_from':str(prior.relative_to(root)),'prior_source_sha256':digest(prior),
        'signed_zero_or_equivalent_internal_angles_can_fail_identity':True,'quality_claim':False,'new_searches':0}
    write(out/'layout-checks.json',result);shutil.copyfile(__file__,out/'check-layouts.py')
    print(json.dumps({k:v for k,v in result.items() if k not in ['finals','saved','pairs']}))
except BaseException:
    write(out/'layout-check-failure.json',{'error':traceback.format_exc(),'completed':records});raise
