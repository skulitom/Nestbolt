"""Try to insert the last original cog by translating all receiver parts together."""
import argparse
from copy import deepcopy
import json
from math import cos, hypot, radians, sin
from pathlib import Path
import sys
import time

import numpy as np
import shapely
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from shapely.affinity import affine_transform
from shapely.geometry import Polygon, box

from receiver import JOB, RESULTS, read, validate, write
from compact import PAD, RADIUS, Region, polygon_at, separating_lines


def contacts(moving, fixed, center, scale, kerf):
    seg = shapely.shortest_line(moving.hull, fixed.hull)
    dist = seg.length
    if dist > 0 and (dist >= kerf-1e-5 or len(moving.parts) == len(fixed.parts) == 1):
        (x,y),(u,v) = seg.coords
        nx,ny = (u-x)/dist,(v-y)/dist
        # The closest point on a convex set maximizes its support in the
        # direction of the other set. This coefficient is linear in scale.
        support = ((x-center[0])*nx+(y-center[1])*ny)/scale
        yield nx,ny,support,dist
    elif len(moving.parts) >= len(fixed.parts) and len(moving.parts) > 1:
        for c in moving.split():
            yield from contacts(c,fixed,center,scale,kerf)
    elif len(fixed.parts) > 1:
        for c in fixed.split():
            yield from contacts(moving,c,center,scale,kerf)
    else:
        raise ValueError("Intersecting convex pieces at the beginning of a growth step")


def growth_step(chain, prepared, cog_pieces, usable, kerf):
    first, center, scale = chain["first"],chain["center"],chain["scale"]
    fixed = [Region([polygon_at(s,p) for s in prepared[p["part_id"]]]) for p in first]
    c,s = cos(chain["angle"]),sin(chain["angle"])
    full = [affine_transform(p,[c,-s,s,c,0,0]) for p in cog_pieces]
    unscaled = shapely.union_all(full)
    moving = Region([affine_transform(p,[scale,0,0,scale,*center]) for p in full])
    n = len(first)
    ix,iy = 2*n,2*n+1
    size = iy+1
    rows,cols,values,rhs = [],[],[],[]
    def add(terms, bound):
        for k,v in terms:
            rows.append(len(rhs))
            cols.append(k)
            values.append(v)
        rhs.append(bound)
    xlow,ylow,xhigh,yhigh = usable.bounds
    bounds = []
    for i,node in enumerate(fixed):
        x0,y0,x1,y1 = node.bounds
        bounds += [(max(-RADIUS,xlow+PAD-x0),min(RADIUS,xhigh-PAD-x1)),
                   (max(-RADIUS,ylow+PAD-y0),min(RADIUS,yhigh-PAD-y1))]
        for j in range(i):
            for nx,ny,d in separating_lines(fixed[j],node,kerf):
                add([(2*j,nx),(2*j+1,ny),(2*i,-nx),(2*i+1,-ny)], d-kerf-PAD)
        for nx,ny,support,d in contacts(moving,node,center,scale,kerf):
            add([(ix,nx),(iy,ny),(2*i,-nx),(2*i+1,-ny),(size,support)],d-kerf-PAD)
    bounds += [(-RADIUS,RADIUS),(-RADIUS,RADIUS),(0,1-scale)]
    lx,ly,hx,hy = unscaled.bounds
    for axis, base, lo, hi, amin, amax in (
        (ix,center[0],lx,hx,xlow,xhigh),(iy,center[1],ly,hy,ylow,yhigh)):
        add([(axis,1),(size,hi)],amax-PAD-base-scale*hi)
        add([(axis,-1),(size,-lo)],base+scale*lo-amin-PAD)
    bounds += [(0,RADIUS)]*size
    for i in range(size):
        add([(i,1),(size+1+i,-1)],0)
        add([(i,-1),(size+1+i,-1)],0)
    matrix = coo_matrix((values,(rows,cols)),shape=(len(rhs),len(bounds))).tocsr()
    def solve(cost):
        return linprog(cost,A_ub=matrix,b_ub=rhs,bounds=bounds,method="highs",
                       options={"threads":1,"time_limit":2,"primal_feasibility_tolerance":1e-8})
    cost = np.zeros(len(bounds))
    cost[size] = -1
    maximized = solve(cost)
    info = {"constraints":len(rhs),"scale_status":maximized.message}
    if not maximized.success:
        return None,info
    best = maximized.x[size]
    floor = best if best >= 1-scale-1e-9 else max(0,best-1e-8)
    bounds[size] = (min(floor,1-scale),1-scale)
    cost[:] = 0
    cost[size+1:] = 1
    tied = solve(cost)
    info["motion_status"] = tied.message
    if not tied.success:
        return None,info
    result = deepcopy(chain)
    for i,p in enumerate(result["first"]):
        xy = p["transform"]["translation"]
        p["transform"]["translation"] = [xy[k]+tied.x[2*i+k] for k in (0,1)]
    result["center"] = [center[0]+tied.x[ix],center[1]+tied.x[iy]]
    result["scale"] = min(1,scale+tied.x[size])
    return result,info


def inspect(first, center, angle, scale, rings, cog, usable, kerf):
    shapes = [polygon_at(rings[p["part_id"]],p) for p in first]
    c,s = cos(angle)*scale,sin(angle)*scale
    shapes.append(affine_transform(cog,[c,-s,s,c,*center]))
    # Bound checking uses the analytic rectangle, including interior objects
    # whose polygon-to-stock distance is zero.
    x0,y0,x1,y1 = usable.bounds
    stock_slack = min(min(l-x0,b-y0,x1-r,y1-t) for l,b,r,t in [p.bounds for p in shapes])
    gap = min(p.distance(q) for i,p in enumerate(shapes) for q in shapes[:i])
    return dict(stock_slack_mm=stock_slack, minimum_pair_distance_mm=gap,
                valid=gap >= kerf-1e-7 and stock_slack >= -1e-7)


def true_layout(partial, chain, origin):
    c,s = cos(chain["angle"]),sin(chain["angle"])
    cx,cy = chain["center"]
    tx,ty = origin
    missing = dict(part_id="cog",copy_index=14,sheet_id="sheet-0",
                   transform=dict(rotation_radians=chain["angle"],mirrored=False,
                                  translation=[cx-c*tx+s*ty,cy-s*tx-c*ty]))
    return {**partial,"placements":chain["first"]+[missing]+[p for p in partial["placements"] if p["sheet_id"]=="sheet-1"]}


def main(folder, binary):
    start = time.monotonic()
    partial = read(folder/"partial.json")
    job = read(RESULTS.parent/"datasets/M"/(JOB+".json"))
    req = read(folder/"request.json")
    kerf,edge = req["spacing_mm"],req["edge_spacing_mm"]
    stock = job["stocks"][0]
    m = stock["margins"]
    usable = box(m["left"]+edge,m["bottom"]+edge,stock["width"]-m["right"]-edge,stock["height"]-m["top"]-edge)
    rings = {p["id"]:Polygon(p["geometry"][0]["outer"]) for p in job["parts"]}
    def decompose(p):
        parts = [p] if p.equals(p.convex_hull) else list(shapely.constrained_delaunay_triangles(p).geoms)
        assert shapely.union_all(parts).equals(p) and all(q.equals(q.convex_hull) for q in parts)
        return parts
    prepared = {k:decompose(v) for k,v in rings.items()}
    x0,y0,x1,y1 = rings["cog"].bounds
    origin = [(x0+x1)/2,(y0+y1)/2]
    cog = affine_transform(rings["cog"],[1,0,0,1,-origin[0],-origin[1]])
    cog_pieces = decompose(cog)
    radius = max(hypot(x,y) for x,y in cog.exterior.coords)
    first = [p for p in partial["placements"] if p["sheet_id"] == "sheet-0"]
    free = usable.difference(shapely.union_all([polygon_at(rings[p["part_id"]],p) for p in first]))
    history,chains,direct = [],[],[]
    for seed in range(3):
        segment = shapely.maximum_inscribed_circle(free,tolerance=0.1)
        center = list(segment.coords[0])
        scale = min(1,(segment.length-kerf-0.02)/radius)
        assert scale > 0
        free = free.difference(shapely.Point(center).buffer(220))
        for deg in (0,6,12):
            chain = dict(seed=seed, angle=radians(deg),center=center,scale=scale,first=first)
            initial = inspect(first, center, chain["angle"],scale,rings,cog,usable,kerf)
            assert initial["valid"], initial
            test = inspect(first, center,chain["angle"],1,rings,cog,usable,kerf)
            direct.append(dict(seed=seed,degrees=deg,center=center,void_radius_mm=segment.length,
                               initial_scale=scale,initial_check=initial,true_size_check=test))
            if test["valid"]:
                chain["scale"] = 1
            chains.append(chain)
    write(folder/"direct-insertion.json",direct)
    best = max(chains,key=lambda a:a["scale"])
    live = set(range(len(chains)))
    for round_index in range(7):
        for i in sorted(live):
            if best["scale"] >= 1-1e-9 or time.monotonic()-start >= 47:
                break
            old = chains[i]
            new,record = growth_step(old,prepared,cog_pieces,usable,kerf)
            record.update(chain=i,iteration=round_index+1,starting_scale=old["scale"])
            history.append(record)
            if new is None:
                live.remove(i)
                continue
            checked = inspect(new["first"],new["center"],new["angle"],new["scale"],rings,cog,usable,kerf)
            record.update(scale=new["scale"],check=checked)
            if not checked["valid"]:
                live.remove(i)
                continue
            chains[i] = new
            if new["scale"] > best["scale"]:
                best = new
            if new["scale"]-old["scale"] < 0.00002:
                live.remove(i)
        if best["scale"] >= 1-1e-9 or not live or time.monotonic()-start >= 47:
            break
    write(folder/"growth-history.json",history)
    write(folder/"best-growth.json", best)
    layout = true_layout(partial,best,origin)
    write(folder/"true-size.json",layout)
    full = validate(binary,folder,"request.json","true-size.json","true-size-check")
    info = dict(full66_valid=full["valid"], best_diagnostic_scale=best["scale"],seed=best["seed"],
                angle_radians=best["angle"],directions_updated=len(history),remaining_chains=sorted(live),
                seconds=time.monotonic()-start,violation_count=full["violation_count"])
    if full["valid"]:
        import subprocess
        subprocess.run([binary,"export","--library","library.json","--request","request.json","--layout","true-size.json",
                        "--out-dir","full-export"],cwd=folder,check=True,capture_output=True)
        info["metrics"] = full["metrics"]
    write(folder/"growth-result.json",info)
    print(json.dumps(info))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receiver",type=Path)
    parser.add_argument("binary",type=Path)
    args=parser.parse_args()
    main(args.receiver.resolve(),args.binary.resolve())
