from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/diagnose_h5_concave_gaps.py').read_text(encoding='utf-8')
s=s.replace("OUT = ROOT / 'output/h5-concave-gap-diagnosis-20261018'", "OUT = ROOT / 'output/h5-source-gap-diagnosis-20261018'")
s=s.replace('One deterministic greedy pass over original last-sheet copies by decreasing original top, then area, then id/index.', 'One deterministic greedy pass over original last-sheet copies above the saved conditional material target, by decreasing original top, then area, then id/index. Construct at most four moves into that lower prefix on the SAME sheet, with no neighbour changed. This is a post-hoc sequence, not runtime acceptance.')
s=s.replace('Only the selected part moves to an earlier sheet; every other pose stays exact.', 'Only the selected part moves within its existing last sheet; every other pose stays exact. The placement domain limits the selected part to the saved conditional target height, while other parts may still cross that height. Full original stock and cutting settings remain the validation authority.')
s=s.replace('This follows the retained convex-hull diagnosis with zero transfers; its four original layouts are reused unchanged.', 'This follows two retained fixed-earlier-sheet diagnoses with zero transfers; the four original layouts are reused unchanged. Lowering selected source copies tests a different move domain, without another solver run.')
old="""            moved=set(); attempts=[]; transfers=[]; last=baseline; cache={}
            for i in order:
                p=layout['placements'][i]; family=p['part_id']; chosen=None
                for target in ids[:-1]:
                    fixed=[pose(shapes[q['part_id']],q['transform']) for q in layout['placements'] if q['sheet_id']==target]
                    for t in orientations(parts[family],p['transform']):
                        k=(len(moved),family,target,t['rotation_radians'],t['mirrored'])
                        if k not in cache:
                            local=pose(shapes[family],t)
                            free=regions(local,fixed,stock_by_sheet[target],job['edge_clearance'],job['clearance'])"""
new="""            boundary=next(b for b in load(PRIOR/'final-boundaries.json')['records'] if b['archive']==row['archive'])
            assert boundary['layout_sha256']==row['layout_sha256']
            target_stock=copy.deepcopy(stock_by_sheet[source]); target_stock['height']=boundary['required_used_height_mm']
            order=[i for i in order if pose(shapes[original['placements'][i]['part_id']],original['placements'][i]['transform']).bounds[3] > boundary['required_outline_top_mm']+2e-6]
            write(folder/'conditional-target.json',boundary)
            moved=set(); attempts=[]; transfers=[]; last=baseline; cache={}
            for i in order:
                if len(moved)>=4:break
                p=layout['placements'][i]; family=p['part_id']; chosen=None
                for target in [source]:
                    fixed=[pose(shapes[q['part_id']],q['transform']) for j,q in enumerate(layout['placements']) if q['sheet_id']==target and j!=i]
                    for t in orientations(parts[family],p['transform']):
                        k=(len(moved),i,family,target,t['rotation_radians'],t['mirrored'])
                        if k not in cache:
                            local=pose(shapes[family],t)
                            free=regions(local,fixed,target_stock,job['edge_clearance'],job['clearance'])"""
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("'copies_considered':len(order),'orientation_attempts':len(attempts),", "'copies_crossing_target':len(order),'copies_considered':len({(a['part_id'],a['copy_index']) for a in attempts}),'orientation_attempts':len(attempts),")
s=s.replace("'receiver_transfers':len(moved)", "'earlier_source_moves':len(moved)")
(root/'output/diagnose_h5_source_gaps.py').write_text(s,encoding='utf-8',newline='\n')
