from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'output/diagnose_h5_saved_gaps.py'
s=p.read_text(encoding='utf-8')
old=s[s.index('def obstacle('):s.index('\n\ndef regions(')]
new='''_piece_cache = {}


def convex_pieces(shape):
    key = shape.wkb
    if key in _piece_cache: return _piece_cache[key]
    if shape.equals(shape.convex_hull):
        pieces = [shape]
    else:
        pieces = list(shapely.constrained_delaunay_triangles(shape).geoms)
        assert pieces and unary_union(pieces).equals(shape)
        # Merge adjacent triangles only when their actual union is convex.
        # The exact coverage assertion below prevents any lost concave sliver.
        changed = True
        while changed:
            changed = False
            for i in range(len(pieces)):
                for j in range(i+1,len(pieces)):
                    if pieces[i].boundary.intersection(pieces[j].boundary).length == 0: continue
                    merged=pieces[i].union(pieces[j])
                    if merged.geom_type=='Polygon' and merged.equals(merged.convex_hull):
                        pieces[i]=merged;pieces.pop(j);changed=True;break
                if changed:break
        assert unary_union(pieces).equals(shape)
        assert all(p.equals(p.convex_hull) for p in pieces)
    _piece_cache[key]=pieces
    return pieces


def obstacle(fixed, moving, clearance):
    hulls=[]
    for fp in convex_pieces(fixed):
        a=np.asarray(fp.exterior.coords)[:-1]
        for mp in convex_pieces(moving):
            b=np.asarray(mp.exterior.coords)[:-1]
            hulls.append(MultiPoint((a[:,None,:]-b[None,:,:]).reshape(-1,2)).convex_hull)
    # Minkowski addition distributes over the exactly covering convex pieces.
    forbidden=unary_union(hulls)
    # Straight mitred joins over-approximate round clearance, including concave
    # part detail, without relying on a nominal polygonal arc segment angle.
    return forbidden.buffer(clearance+EPS,join_style='mitre',mitre_limit=5)
'''
assert s.count(old)==1
s=s.replace(old,new)
s=s.replace("OUT = ROOT / 'output/h5-saved-gap-diagnosis-20261018'", "OUT = ROOT / 'output/h5-concave-gap-diagnosis-20261018'")
s=s.replace('Subtract convex-hull Minkowski obstacles expanded by circumscribed clearance buffers', 'Exactly cover each filled outer contour with convex pieces, verify their union and convexity, then subtract unions of pairwise Minkowski obstacles expanded by mitred clearance buffers')
s=s.replace("'buffer_quad_segs':QUADS,", "'buffer_join_style':'mitre', 'buffer_mitre_limit':5,")
s=s.replace('Convex hulls and finite free angles can miss actual feasible regions; no-result is not an impossibility proof.', 'Finite free angles, positive construction margin and one greedy pass can miss actual feasible regions; no-result is not an impossibility proof. This follows the retained convex-hull diagnosis with zero transfers; its four original layouts are reused unchanged.')
s=s.replace("return {'narrow_gap_positive':True,'oversized_negative':True,'filled_outer_negative':True}", """concave=Polygon([(0,0),(80,0),(80,20),(20,20),(20,80),(0,80)])
    assert len(convex_pieces(concave))>1
    shaped_stock=dict(stock,width=80,height=80)
    assert not regions(box(0,0,30,30),[concave],shaped_stock,0,.2).is_empty
    assert regions(box(0,0,30,30),[concave.convex_hull],shaped_stock,0,.2).is_empty
    return {'narrow_gap_positive':True,'oversized_negative':True,'filled_outer_negative':True,'concave_gap_missed_by_hull':True}""")
(root/'output/diagnose_h5_concave_gaps.py').write_text(s,encoding='utf-8',newline='\n')
