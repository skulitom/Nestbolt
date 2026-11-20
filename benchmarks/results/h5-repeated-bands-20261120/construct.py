"""Construct two sheets by repeating rectangular regions of an individual input layout."""
import argparse
from collections import Counter
import json
from math import ceil, cos, floor, pi, sin
from pathlib import Path
import subprocess
import time
from zipfile import ZipFile

import numpy as np

RESULTS = Path(__file__).resolve().parents[1]
GAP_PAD = 0.000006


def rotated_parts(placements, parts, angle):
    """Return exact outer bounds in donor coordinates and the rotated placement."""
    c, s = round(cos(angle)), round(sin(angle))
    for placement in placements:
        part = parts[placement["part_id"]]
        trans = placement["transform"]
        theta = trans["rotation_radians"]+angle
        allowed = part["rotations"]
        assert allowed["kind"] == "list"
        if not any(abs((theta-d*pi/180+pi)%(2*pi)-pi)<1e-9 for d in allowed["degrees"]):
            continue
        tx, ty = trans["translation"]
        x, y = c*tx-s*ty, s*tx+c*ty
        a, b = cos(theta), sin(theta)
        sign = -1 if trans["mirrored"] else 1
        vertices = [(x+sign*a*u-b*v,y+sign*b*u+a*v) for polygon in part["geometry"]
                    for u,v in polygon["outer"]]
        xs, ys = zip(*vertices)
        yield min(xs),max(xs),min(ys),max(ys),placement["part_id"],theta,x,y,trans["mirrored"]


def patterns(job, layout, width, height, gap, padding):
    parts = {p["id"]:p for p in job["parts"]}
    names = list(parts)
    index = {key:i for i,key in enumerate(names)}
    quantities = tuple(p["quantity"] for p in parts.values())
    found = {}
    for sheet in layout["sheets"]:
        placed = [p for p in layout["placements"] if p["sheet_id"]==sheet["id"]]
        for angle in (0,pi/2):
            boxes = sorted(rotated_parts(placed,parts,angle),key=lambda p:p[3])
            if not boxes:
                continue
            smallest = min(r[1]-r[0] for r in boxes)
            for repeats in range(1,1+floor((width+gap)/(smallest+gap))):
                tile_width = (width+gap)/repeats-gap
                # Identical horizontal windows produce identical band candidates.
                windows = {tuple(i for i,b in enumerate(boxes) if b[0]>=x and b[1]-x<=tile_width)
                           for x in {b[0] for b in boxes}}
                for window in sorted(windows):
                    available = [boxes[i] for i in window]
                    for bottom in sorted({r[2] for r in available}):
                        selected = []
                        counts = [0]*len(parts)
                        low = float("inf")
                        for r in available:
                            if r[2]<bottom:
                                continue
                            low = min(low,r[2])
                            selected.append(r)
                            counts[index[r[4]]] += repeats
                            span = r[3]-low+padding
                            if span>height:
                                continue
                            key = tuple(min(a,b) for a,b in zip(counts,quantities))
                            if key not in found or span < found[key][0]:
                                found[key] = span,repeats,tuple(selected)
    return quantities,found


def minimum_heights(quantities, found, gap, height):
    """Cover all subinventories by bands. Surplus copies in a region may be omitted."""
    dims = tuple(q+1 for q in quantities)
    cost = np.full(dims,np.inf)
    for key,(span,_,_) in found.items():
        cost[key] = span
    reverse = tuple(slice(None,None,-1) for _ in dims)
    cheapest = cost[reverse].copy()
    for axis in range(len(dims)):
        np.minimum.accumulate(cheapest,axis=axis,out=cheapest)
    cheapest = cheapest[reverse]
    patterns = []
    for key,(span,_,_) in sorted(found.items()):
        if any(key[i] < quantities[i] and cheapest[key[:i]+(key[i]+1,)+key[i+1:]] <= span
               for i in range(len(dims))):
            continue
        patterns.append((key,span+gap))
    dp = np.full(dims,np.inf)
    dp[(0,)*len(dims)] = 0
    parent = np.full(dims,-1,dtype=int)
    axes = np.indices(dims).reshape(len(dims),-1)
    indices = [np.ravel_multi_index(np.maximum(0,axes-np.asarray(key)[:,None]),dims) for key,_ in patterns]
    # Only solutions within one physical sheet height can participate in the two-sheet layout.
    for _ in range(floor((height+gap)/min(c for _,c in patterns))):
        old = dp.ravel().copy()
        changed = False
        for i,((key,c),prior) in enumerate(zip(patterns,indices)):
            candidate = (old[prior]+c).reshape(dims)
            improves = (candidate < dp-1e-10) & (candidate <= height+gap)
            if np.any(improves):
                dp[improves] = candidate[improves]
                parent[improves] = i
                changed = True
        if not changed:
            break
    return dp,parent,patterns


def construct(job, layout, catalogue=patterns):
    stock, = job["stocks"]
    assert len(layout["sheets"])==2 and not stock["outline"] and not stock["defects"]
    assert all(s["stock_id"]==stock["id"] for s in layout["sheets"])
    margin = stock["margins"]
    pad = job["edge_clearance"]+GAP_PAD
    x0,y0 = margin["left"]+pad,margin["bottom"]+pad
    width = stock["width"]-margin["right"]-pad-x0
    height = stock["height"]-margin["top"]-pad-y0
    gap = job["clearance"]+GAP_PAD
    quantities,found = catalogue(job,layout,width,height,gap,0.0)
    dp,parent,choices = minimum_heights(quantities,found,gap,height)
    reverse = tuple(slice(None,None,-1) for _ in quantities)
    totals = np.where(dp<=height+gap,dp[reverse],np.inf)
    diagnostics = dict(catalogue=len(found),nondominated=len(choices))
    if not np.isfinite(totals).any():
        return None,diagnostics
    split = tuple(map(int,np.unravel_index(np.argmin(totals),dp.shape)))
    tail = tuple(a-b for a,b in zip(quantities,split))
    groups = []
    output = dict(layout,placements=[])
    ids = [p["id"] for p in job["parts"]]
    global_count = Counter()
    for sheet,needs in zip(layout["sheets"],(split,tail)):
        y = y0
        selected = []
        while any(needs):
            choice = parent[needs]
            assert choice>=0
            key,cost = choices[choice]
            span,repeats,tiles = found[key]
            left = min(r[0] for r in tiles)
            step = max(r[1] for r in tiles)-left+gap
            base = min(r[2] for r in tiles)
            required = {k:min(n,m) for k,n,m in zip(ids,needs,key)}
            for j in range(repeats):
                for r in tiles:
                    _,_,_,_,k,angle,tx,ty,mirrored = r
                    if required[k]==0:
                        continue
                    output["placements"].append(dict(part_id=k,copy_index=global_count[k],sheet_id=sheet["id"],
                        transform=dict(rotation_radians=angle%(2*pi),mirrored=mirrored,
                                       translation=[x0+j*step+tx-left,y+ty-base])))
                    global_count[k] += 1
                    required[k] -= 1
            assert not any(required.values())
            needs = tuple(max(0,n-m) for n,m in zip(needs,key))
            selected.append(dict(quantities=key,height_mm=span,repeat=repeats))
            y += cost
        groups.append(selected)
    assert tuple(global_count[k] for k in ids)==quantities
    diagnostics.update(first_quantities=split,last_quantities=tail,bands=groups)
    return output,diagnostics


def run(args):
    directory = args.out.resolve()
    directory.mkdir(exist_ok=True,parents=True)
    records = []
    for source in args.matrix:
        for path in sorted(source.glob("c-bracket-mixed-k*-s*-*.zip")):
            with ZipFile(path) as z:
                case = json.loads(z.read("case.json"))
                if case["arm"]=="normal":
                    continue
                job,layout,validation = [json.loads(z.read(n)) for n in
                    ("nested/job.json","nested/layout.json","validate-stdout.json")]
                folder = directory/source.name/path.stem
                folder.mkdir(parents=True,exist_ok=True)
                for n in ("library.json","request.json"):
                    (folder/n).write_bytes(z.read(n))
            start = time.monotonic()
            trial,record = construct(job,layout)
            record.update(matrix=source.name,source=path.name,seconds=time.monotonic()-start,
                          kerf=case["kerf_mm"],seed=case["seed"],arm=case["arm"],
                          original=validation["metrics"]["normalized_material"])
            if trial is not None:
                out = folder/"layout.json"
                out.write_text(json.dumps(trial),encoding="utf-8",newline="\n")
                proc = subprocess.run([args.binary.resolve(),"validate","--library",folder/"library.json",
                                       "--request",folder/"request.json","--layout",out],capture_output=True)
                (folder/"validation.json").write_bytes(proc.stdout)
                checked = json.loads(proc.stdout)
                record["valid"] = proc.returncode==0 and checked["valid"]
                if record["valid"]:
                    record["material"] = checked["metrics"]["normalized_material"]
                    record["saved_fraction"] = sum(s["saved_length_mm"] for s in checked["common_line"])/sum(
                        s["cut_length_without_common_mm"] for s in checked["common_line"])
            records.append(record)
            print(path.name,record.get("valid"),record.get("material"),round(record["seconds"],3),flush=True)
    (directory/"results.json").write_text(json.dumps(records,indent=2)+"\n",encoding="utf-8",newline="\n")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary",type=Path)
    parser.add_argument("out",type=Path)
    parser.add_argument("matrix",nargs="+",type=Path)
    run(parser.parse_args())
