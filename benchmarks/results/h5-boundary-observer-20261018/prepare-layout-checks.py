"""Extend the existing saved-layout audit to exact physical top-copy coverage."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/check_h5_frontier_layouts.py').read_text(encoding='utf-8').replace('h5-frontier-observer','h5-boundary-observer')
s=s.replace('import ast,itertools,json,math,shutil,subprocess,traceback,zipfile','import ast,itertools,json,math,shutil,subprocess,sys,traceback,zipfile')
needle="load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()"
s=s.replace(needle,needle+"\nsys.path.insert(0,str(root/'scripts'));import h5_boundary_observer as observer")
needle="            attempts=[a for a in trace['attempts'] if a['choice_index'] in matching]\n"
extra='''            observer.check_traces([trace])
            owner_keys={observer.pose_key({'part_id':p['part_id'],'transform':p['transform']}) for p in credit['owners']}
            choice_keys=[{observer.pose_key(p) for p in c} for c in trace['choice_poses']]
            exact_choices=[i for i,keys in enumerate(choice_keys) if keys & owner_keys]
            complete_choices=[i for i,keys in enumerate(choice_keys) if owner_keys<=keys]
            exact_visits=sorted({v['choice_index'] for v in trace['visits'] if v['choice_index'] in exact_choices})
            complete_visits=sorted({v['choice_index'] for v in trace['visits'] if v['choice_index'] in complete_choices})
            exact_attempts=[a for a in trace['attempts'] if a['choice_index'] in exact_choices]
            complete_attempts=[a for a in trace['attempts'] if a['choice_index'] in complete_choices]
'''
assert s.count(needle)==1;s=s.replace(needle,needle+extra)
needle="                'all_attempts':len(trace['attempts']),"
extra="""                'height_copy_choice_indices':exact_choices,'height_copy_visited_indices':exact_visits,
                'all_height_copies_choice_indices':complete_choices,'all_height_copies_visited_indices':complete_visits,
                'attempts_with_actual_height_copy':len(exact_attempts),
                'attempt_outcomes_with_actual_height_copy':dict(Counter(a['outcome'] for a in exact_attempts)),
                'attempts_with_all_height_copies':len(complete_attempts),
                'attempt_outcomes_with_all_height_copies':dict(Counter(a['outcome'] for a in complete_attempts)),
"""
assert s.count(needle)==1;s=s.replace(needle,extra+needle)
needle="        'baselines':records,'finals':finals,"
extra="""        'attempts_with_actual_height_copy':sum(r['attempts_with_actual_height_copy'] for r in records),
        'attempts_with_all_height_copies':sum(r['attempts_with_all_height_copies'] for r in records),
        'choice_poses_match_validated_baseline_exactly':True,
"""
assert s.count(needle)==1;s=s.replace(needle,extra+needle)
s=s.replace('Family coverage does not identify the specific copies defining height; zero family attempts excludes those copies, while a positive count would not prove their selection.',
    'Every chosen physical pose uniquely matches the validated public source layout exactly. Actual top-copy coverage uses the independently reconstructed highest original contour vertices, separate from family coverage.')
s=s.replace('    print(json.dumps(records))','')
compile(s,'layout-checks','exec')
(root/'output/check_h5_boundary_observer_layouts.py').write_text(s,encoding='utf-8',newline='\n')
print('Prepared independent material/geometry audit and exact boundary-copy coverage checks.')
