from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/diagnose_h5_source_gaps.py').read_text(encoding='utf-8')
s=s.replace("OUT = ROOT / 'output/h5-source-gap-diagnosis-20261018'", "OUT = ROOT / 'output/h5-incremental-gap-diagnosis-20261018'")
s=s.replace('One deterministic greedy pass over original last-sheet copies above the saved conditional material target, by decreasing original top, then area, then id/index. Construct at most four moves into that lower prefix on the SAME sheet, with no neighbour changed.', 'One deterministic greedy pass over all original last-sheet copies by decreasing original top, then area, then id/index. Construct at most four moves on the SAME sheet, lowering each selected outline top by at least 0.001 mm, with no neighbour changed.')
s=s.replace('and its lowest representative interior point.', 'and its lowest verified near-boundary interior point. For each polygon, interpolate each exterior vertex toward its representative interior point at fractions 1e-6, 1e-4, 0.01, 0.1 and 1; retain only contained points and choose the lowest y then x.')
s=s.replace('The placement domain limits the selected part to the saved conditional target height, while other parts may still cross that height.', 'The placement domain limits each selected part to 0.001 mm below its prior outline top, while other parts may still cross that height. The saved +1% target remains a reference only; smaller improvements are allowed in this diagnosis.')
s=s.replace('This follows two retained fixed-earlier-sheet diagnoses with zero transfers;', 'This follows two retained fixed-earlier-sheet diagnoses and a direct-target source-gap diagnosis with no material gains;')
line="            order=[i for i in order if pose(shapes[original['placements'][i]['part_id']],original['placements'][i]['transform']).bounds[3] > boundary['required_outline_top_mm']+2e-6]\n"
assert s.count(line)==1;s=s.replace(line,'')
line="                p=layout['placements'][i]; family=p['part_id']; chosen=None\n"
assert s.count(line)==1;s=s.replace(line,line+"                target_stock['height']=min(stock_by_sheet[source]['height'],pose(shapes[family],p['transform']).bounds[3]+job['edge_clearance']+target_stock['margins']['top']-0.001)\n")
old="                            pts=sorted((list(g.representative_point().coords)[0] for g in pieces if g.area>0), key=lambda xy:(xy[1],xy[0]))"
new="""                            pts=[]
                            for g in pieces:
                                rep=g.representative_point();rx,ry=rep.x,rep.y
                                for vx,vy in list(g.exterior.coords)[:-1]:
                                    for f in [1e-6,1e-4,.01,.1,1.]:
                                        pt=shapely.Point(vx+(rx-vx)*f,vy+(ry-vy)*f)
                                        if g.contains(pt):pts.append((pt.x,pt.y))
                            pts.sort(key=lambda xy:(xy[1],xy[0]))"""
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("'copies_crossing_target':len(order),", "'original_source_copies':len(order),")
(root/'output/diagnose_h5_incremental_gaps.py').write_text(s,encoding='utf-8',newline='\n')
