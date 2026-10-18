from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'output/audit_h5_outline_constructions.py').read_text(encoding='utf-8')
s=s.replace("OUT=ROOT/'output/h5-outline-audit-20261018'", "OUT=ROOT/'output/h5-outline-audit-recovery-20261018'\nOLD=ROOT/'output/h5-outline-audit-20261018'")
old="""    r=subprocess.run(command,capture_output=True,timeout=60)
    (dest/'stdout.json').write_bytes(r.stdout);(dest/'stderr.log').write_bytes(r.stderr)
    write(dest/'command.json',{'command':command,'exit_code':r.returncode});report=json.loads(r.stdout)"""
new="""    previous=OLD/name
    if (previous/'stdout.json').exists():
        assert (previous/'layout.json').read_bytes()==(dest/'layout.json').read_bytes()
        prior_command=load(previous/'command.json')
        assert prior_command['command'][:-1]==command[:-1]
        raw=(previous/'stdout.json').read_bytes();err=(previous/'stderr.log').read_bytes();code=prior_command['exit_code']
        command_record={**prior_command,'reused_original_output':True,'current_layout_bytes_match_original':True,'current_layout':str(dest/'layout.json')}
    else:
        r=subprocess.run(command,capture_output=True,timeout=60);raw=r.stdout;err=r.stderr;code=r.returncode
        command_record={'command':command,'exit_code':code,'reused_original_output':False}
    (dest/'stdout.json').write_bytes(raw);(dest/'stderr.log').write_bytes(err)
    write(dest/'command.json',command_record);report=json.loads(raw)"""
assert s.count(old)==1;s=s.replace(old,new)
old="""    count=sum(missing.values());assert report['metrics']['placed_parts']==sum(placed.values())
    assert report['metrics']['requested_parts']==sum(expected.values())
    return {'folder':dest.name,'CLI_geometry_valid':report['valid'],'CLI_exit':r.returncode,'missing':dict(missing),'missing_count':count,'complete':False}"""
new="""    count=sum(missing.values())
    assert not report['valid'] and code!=0 and report['metrics'] is None
    expected_messages={f'part {k}: expected {expected[k]}, found {placed[k]}' for k in missing}
    assert report['violation_count']==len(missing)
    assert {v['message'] for v in report['violations']}==expected_messages
    assert all(v['code']=='quantity' for v in report['violations'])
    return {'folder':dest.name,'CLI_valid':False,'CLI_exit':code,'only_expected_quantity_rejections':True,
            'missing':dict(missing),'missing_count':count,'complete':False,'reused_original_output':command_record['reused_original_output']}"""
assert s.count(old)==1;s=s.replace(old,new)
(ROOT/'output/audit_h5_outline_recovery.py').write_text(s,encoding='utf-8',newline='\n')
