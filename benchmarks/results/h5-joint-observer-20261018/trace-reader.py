"""Read diagnostic-only joint-repair forests and reject incomplete observations."""
from collections import Counter
import json
import math

MARKER='JOINT_DIAG '

def finite(value):
    assert type(value) in (int,float) and math.isfinite(value)
    return value

def pose(p):
    assert type(p['part_id']) is str
    t=p['transform'];assert type(t['mirrored']) is bool and len(t['translation'])==2
    return (p['part_id'],*(finite(x) for x in t['translation']),finite(t['rotation_radians']),t['mirrored'])

def inventory(placements):
    assert isinstance(placements,list)
    for p in placements:pose(p)
    return Counter(p['part_id'] for p in placements)

def sheet_poses(layout,sheet):
    return Counter(pose(p) for p in layout['placements'] if p['sheet_id']==sheet)

def event(trace,name):
    found=[e['data'] for e in trace['events'] if e['stage']==name]
    assert len(found)==1,(trace['kind'],name,len(found))
    return found[0]

def parse_log(text):
    return [json.loads(line.split(MARKER,1)[1]) for line in text.splitlines() if MARKER in line]

def check_traces(traces,stats=None):
    assert isinstance(traces,list)
    by_id={t['id']:t for t in traces}
    assert len(by_id)==len(traces),'Duplicate trace identity'
    children={i:[] for i in by_id}
    kinds={'pair','attempt','policy','chain'}
    for t in traces:
        assert set(t)=={'id','parent','kind','elapsed_seconds','data','events','outcome'}
        assert type(t['id']) is int and t['id']>0 and t['kind'] in kinds
        assert finite(t['elapsed_seconds'])>=0 and isinstance(t['data'],dict)
        assert t['outcome']!='unresolved','Incomplete diagnostic terminal state'
        times=[finite(e['elapsed_seconds']) for e in t['events']]
        assert times==sorted(times) and all(0<=x<=t['elapsed_seconds'] for x in times)
        if t['parent'] is not None:
            assert t['parent'] in by_id and t['parent']<t['id'],'Missing parent'
            children[t['parent']].append(t)
    for items in children.values():items.sort(key=lambda t:t['id'])
    for t in traces:
        kind=t['kind'];d=t['data'];stages=[e['stage'] for e in t['events']]
        if kind=='pair':
            assert t['parent'] is None or by_id[t['parent']]['kind']=='attempt'
            assert not children[t['id']]
            assert len(d['proposed'])==2 and finite(d['source_crop_internal'])>=0
            finite(d['absolute_until']);job=d['job'];parts={p['id']:p for p in job['parts']}
            initial=sum((inventory(p) for p in d['proposed']),Counter())
            assert set(initial)<=set(parts)
            assert all(count<=parts[name]['quantity'] for name,count in initial.items())
            expected=['attempted','separator_exit','recrop_exit','lowering_exit']
            assert stages==expected[:len(stages)] and len(stages)<=4
            outcomes={'not_started':0,'separator_expired':2,'separator_failed':2,'outside_pair':2,
                'recrop_expired':3,'recrop_failed':3,'lowering_expired':4,'lowering_failed':4,'completed':4}
            assert t['outcome'] in outcomes and len(stages)==outcomes[t['outcome']]
            if stages:assert type(event(t,'attempted')['counter']) is int and event(t,'attempted')['counter']>0
            if len(stages)>=2:
                sep=event(t,'separator_exit');assert finite(sep['loss'])>=0
                assert finite(sep['separator_seconds'])>=0
                assert inventory(sep['window'])==initial
                assert all(type(p['active_sheet']) is int and p['active_sheet']>=0 for p in sep['window'])
            for name in ['recrop_exit','lowering_exit']:
                if name not in stages:continue
                x=event(t,name);assert len(x['pair'])==2
                assert sum((inventory(p) for p in x['pair']),Counter())==initial
            if 'recrop_exit' in stages:
                x=event(t,'recrop_exit');assert len(x['losses'])==2 and all(finite(v)>=0 for v in x['losses'])
            if 'lowering_exit' in stages:
                x=event(t,'lowering_exit');assert finite(x['loss'])>=0 and finite(x['lowering_seconds'])>=0
                previous=event(t,'recrop_exit')
                assert [inventory(p) for p in previous['pair']]==[inventory(p) for p in x['pair']]
                assert Counter(pose(p) for p in previous['pair'][0])==Counter(pose(p) for p in x['pair'][0])
                assert previous['losses']==[0,0]
            if t['outcome']=='completed':assert event(t,'lowering_exit')['loss']==0
        elif kind=='attempt':
            assert t['parent'] in by_id and by_id[t['parent']]['kind']=='policy'
            policy=by_id[t['parent']]['data'];base=policy['baseline']
            assert len(children[t['id']])==1 and children[t['id']][0]['kind']=='pair'
            pair=children[t['id']][0]
            assert pair['data']['job']==policy['job']
            receiver=d['receiver_active_sheet'];source=d['source_active_sheet'];frozen=policy['frozen_count']
            assert type(receiver) is int and type(source) is int and 0<=receiver<source==policy['active_sheets']-1
            rid,sid=f'sheet-{frozen+receiver}',f'sheet-{frozen+source}'
            incoming=Counter(pose(p) for p in d['incoming']);victims=Counter(pose(p) for p in d['victims'])
            assert not incoming-sheet_poses(base,sid) and not victims-sheet_poses(base,rid)
            assert len(d['incoming'])==(2 if d['paired'] else 1)
            assert type(d['mixed']) is bool and (not d['mixed'] or d['paired'])
            bi=[inventory([p for p in base['placements'] if p['sheet_id']==s]) for s in [rid,sid]]
            i,v=inventory(d['incoming']),inventory(d['victims'])
            assert inventory(pair['data']['proposed'][0])==bi[0]-v+i
            assert inventory(pair['data']['proposed'][1])==bi[1]-i+v
            assert t['outcome'] in {'pair_unavailable','exact_state','same_material_profile','invalid_trial',
                'material_guard_or_expiry','flat_area_guard','acceptance_expired','flat_same_inventory','accepted'}
            if t['outcome']=='pair_unavailable':assert pair['outcome']!='completed' and not stages
            else:assert pair['outcome']=='completed'
            assert stages in [[],['validated_trial'],['validated_trial','accepted_step']]
            if 'validated_trial' in stages:
                trial=event(t,'validated_trial');layout=trial['layout'];report=trial['report']
                assert inventory(layout['placements'])==inventory(base['placements'])
                for sheet in base['sheets']:
                    if sheet['id'] not in [rid,sid]:assert sheet_poses(base,sheet['id'])==sheet_poses(layout,sheet['id'])
                if t['outcome']!='invalid_trial':assert report['valid']
                else:assert not report['valid']
            if t['outcome']=='accepted':
                assert stages==['validated_trial','accepted_step']
                a=event(t,'accepted_step');assert a['before']==policy['metrics']
                assert a['after']==event(t,'validated_trial')['report']['metrics']
                assert a['after']['material_area']<=a['before']['material_area']
            else:assert 'accepted_step' not in stages
        elif kind=='policy':
            assert t['parent'] is None or by_id[t['parent']]['kind']=='chain'
            assert not stages and t['outcome'] in ['accepted','exhausted']
            assert all(c['kind']=='attempt' for c in children[t['id']])
            assert sum(c['outcome']=='accepted' for c in children[t['id']])==int(t['outcome']=='accepted')
            assert inventory(d['baseline']['placements'])==Counter({p['id']:p['quantity'] for p in d['job']['parts']})
            assert type(d['frozen_count']) is int and d['frozen_count']>=0
            assert type(d['active_sheets']) is int and d['active_sheets']>=2
        else:
            assert t['parent'] is None and all(c['kind']=='policy' for c in children[t['id']])
            assert t['outcome'] in ['not_started','completed']
            if t['outcome']=='not_started':assert not stages and not children[t['id']];continue
            assert stages[-1]=='finished'
            accepted=[c for c in children[t['id']] if c['outcome']=='accepted']
            steps=[e['data'] for e in t['events'] if e['stage']=='step']
            assert len(steps)==len(accepted)
            pending=committed=0
            for step,policy in zip(steps,accepted):
                a=next(c for c in children[policy['id']] if c['outcome']=='accepted')
                metrics=event(a,'accepted_step')
                assert step['improved']==(metrics['after']['material_area']<metrics['before']['material_area'])
                pending+=1;assert step['pending']==pending
                if step['improved']:committed+=pending;pending=0
            end=event(t,'finished');assert end['committed']==committed
            initial=d['stats'];last=end['stats']
            get=lambda s,n:s.get(n,0)
            assert get(last,'joint_exchanges')-get(initial,'joint_exchanges')==committed
            assert get(last,'assignment_bridge_rolled_back')-get(initial,'assignment_bridge_rolled_back')==pending
            assert stages.count('rollback')==int(pending>0)
            if pending:
                assert event(t,'rollback')['pending']==pending
                assert event(t,'rollback')['window']==end['window']
    pairs=[t for t in traces if t['kind']=='pair'];attempted=[p for p in pairs if p['outcome']!='not_started']
    completed=sum(p['outcome']=='completed' for p in attempted)
    expired=sum(p['outcome'].endswith('_expired') for p in attempted)
    failed=len(attempted)-completed-expired
    committed=sum(event(t,'finished')['committed'] for t in traces if t['kind']=='chain' and t['outcome']=='completed')
    if stats is not None:
        actual={'joint_repair_attempts':len(attempted),'joint_repair_completed':completed,
            'joint_repair_failed':failed,'joint_repair_expired':expired,'joint_exchanges':committed}
        assert all(stats.get(k,0)==v for k,v in actual.items()),(actual,stats)
    return {'trace_count':len(traces),'kinds':dict(Counter(t['kind'] for t in traces)),
        'pair_outcomes':dict(Counter(t['outcome'] for t in pairs)),
        'attempt_outcomes':dict(Counter(t['outcome'] for t in traces if t['kind']=='attempt')),
        'committed_joint_steps':committed,'all_structural_checks_passed':True}
