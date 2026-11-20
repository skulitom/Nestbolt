"""Bounded one-worker CP-SAT check of joint moves of the highest four or eight parts."""
import argparse
from copy import deepcopy
import json
from math import ceil, floor, pi
from pathlib import Path
import subprocess
from zipfile import ZipFile

from ortools.sat.python import cp_model
from replay import MATRICES, oriented, rectangles, saved


GRID = 10000


def cover(boxes):
    """Cover the union of integer rectangles once, including any kerf expansion."""
    xs = sorted({x for l,r,b,t in boxes for x in (l,r)})
    result = []
    active = {}
    for x,u in zip(xs,xs[1:]):
        spans = sorted((b,t) for l,r,b,t in boxes if l <= x and r >= u)
        merged = []
        for b,t in spans:
            if merged and merged[-1][1] >= b:
                merged[-1] = (merged[-1][0],max(merged[-1][1],t))
            else:
                merged.append((b,t))
        next_active = {}
        for b,t in merged:
            if (b,t) in active:
                index = active[(b,t)]
                result[index][1] = u
            else:
                index = len(result)
                result.append([x,u,b,t])
            next_active[b,t] = index
        active = next_active
    return result


def windows(fixed,local,left,right,bottom,top):
    """Integer translations whose kerf-expanded rectangles miss every fixed obstacle."""
    if left > right or bottom > top:
        return []
    events = {left:[],right+1:[]}
    for l,r,b,t in fixed:
        for a,z,c,w in local:
            x0,x1 = max(left,l-z+1),min(right,r-a-1)
            y0,y1 = max(bottom,b-w+1),min(top,t-c-1)
            if x0 <= x1 and y0 <= y1:
                events.setdefault(x0,[]).append((y0,y1,1))
                events.setdefault(x1+1,[]).append((y0,y1,-1))
    active = {}
    boxes = []
    previous = {}
    xs = sorted(events)
    for x,u in zip(xs,xs[1:]):
        for b,t,delta in events[x]:
            key = b,t
            active[key] = active.get(key,0)+delta
            if active[key] == 0:
                del active[key]
        floor_y = bottom
        free = []
        for b,t in sorted(active):
            if b > floor_y:
                free.append((floor_y,b-1))
            floor_y = max(floor_y,t+1)
            if floor_y > top:
                break
        if floor_y <= top:
            free.append((floor_y,top))
        current = {}
        for b,t in free:
            if (b,t) in previous:
                i = previous[b,t]
                boxes[i][1] = u-1
            else:
                i = len(boxes)
                boxes.append([x,u-1,b,t])
            current[b,t] = i
        previous = current
    return boxes


def optimize(job,layout,sheet,count,use_windows=False,material_limit=None):
    stock, = job["stocks"]
    assert not stock["outline"] and not stock["defects"]
    parts = {p["id"]:p for p in job["parts"]}
    pieces = {key:[r for g in p["geometry"] for r in rectangles(g)] for key,p in parts.items()}
    placed = [p for p in layout["placements"] if p["sheet_id"] == sheet]
    half = ceil(job["clearance"]*GRID/2)+1
    def expand(key,transform):
        for r in pieces[key]:
            l,u,b,t = oriented(r,transform,"down")
            yield floor(l*GRID)-half,ceil(u*GRID)+half,floor(b*GRID)-half,ceil(t*GRID)+half
    original = [list(expand(p["part_id"],p["transform"])) for p in placed]
    tops = [max(r[3] for r in rs) for rs in original]
    order = sorted(range(len(placed)), key=tops.__getitem__,reverse=True)
    moving = order[:count]
    fixed = cover([r for i in order[count:] for r in original[i]])
    model = cp_model.CpModel()
    xs, ys = [],[]
    for l,u,b,t in ([] if use_windows else fixed):
        xs.append(model.new_fixed_size_interval_var(l,u-l,""))
        ys.append(model.new_fixed_size_interval_var(b,t-b,""))
    edge,margins = job["edge_clearance"],stock["margins"]
    left = ceil((margins["left"]+edge)*GRID)-half+1
    right = floor((stock["width"]-margins["right"]-edge)*GRID)+half-1
    bottom = ceil((margins["bottom"]+edge)*GRID)-half+1
    cap = min(floor((stock["height"]-margins["top"]-edge)*GRID)+half-1,
              max(tops)+GRID//2)
    fixed_top = max(t for l,u,b,t in fixed)
    if material_limit is not None:
        # Same-stock complete layout. All earlier sheets count at their full
        # area. The defining last-sheet height includes edge spacing and top margin.
        h = (material_limit-(len(layout["sheets"])-1))*stock["height"]
        cap = min(floor((h-edge-margins["top"])*GRID)+half,cap)
        if fixed_top > cap:
            return None,dict(status="FIXED_ABOVE_TARGET",fixed_top_mm=fixed_top/GRID,
                             ceiling_mm=cap/GRID)
    elif use_windows:
        # Prove or find a one-percent reduction in last-sheet height in this
        # bounded model. An immovable part can fix the attainable upper bound.
        cap = max(fixed_top,max(tops)-ceil((max(tops)-bottom)*0.01))
    height = model.new_int_var(fixed_top,cap,"height")
    variables = []
    previous = {}
    domains = {}
    for i in moving:
        p = placed[i]
        key = p["part_id"]
        x,y = model.new_int_var(left,right,"x"),model.new_int_var(bottom,cap,"y")
        # Copies of the same shape are interchangeable within this group.
        if key in previous:
            model.add(previous[key] <= y)
        previous[key] = y
        choices = []
        for degrees in parts[key]["rotations"]["degrees"]:
            tf = dict(translation=[0,0],rotation_radians=degrees*pi/180,mirrored=p["transform"]["mirrored"])
            box = cover(list(expand(key,tf)))
            l,u = min(r[0] for r in box),max(r[1] for r in box)
            b,t = min(r[2] for r in box),max(r[3] for r in box)
            if use_windows:
                # x,y are the lower-left of the expanded, rotated copy.
                if (key,degrees,tf["mirrored"]) not in domains:
                    local = [(a-l,z-l,c-b,w-b) for a,z,c,w in box]
                    domains[key,degrees,tf["mirrored"]] = windows(fixed,local,left,right-(u-l),bottom,cap-(t-b))
                possible = domains[key,degrees,tf["mirrored"]]
                if not possible:
                    continue
            use = model.new_bool_var("rotation")
            if use_windows:
                alternatives = []
                for xmin,xmax,ymin,ymax in possible:
                    win = model.new_bool_var("window")
                    model.add_linear_constraint(x,xmin,xmax).only_enforce_if(win)
                    model.add_linear_constraint(y,ymin,ymax).only_enforce_if(win)
                    alternatives.append(win)
                model.add(sum(alternatives)==use)
            model.add(x+u-l <= right).only_enforce_if(use)
            model.add(y+t-b <= height).only_enforce_if(use)
            choices.append((use,degrees,l,b))
            for a,z,c,w in box:
                xs.append(model.new_optional_fixed_size_interval_var(x+a-l,z-a,use,""))
                ys.append(model.new_optional_fixed_size_interval_var(y+c-b,w-c,use,""))
        model.add_exactly_one(v[0] for v in choices)
        variables.append((i,x,y,choices))
    model.add_no_overlap_2d(xs,ys)
    if not use_windows:
        model.minimize(height)
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.max_deterministic_time = 0.65
    solver.parameters.max_time_in_seconds = 8
    status = solver.solve(model)
    record = dict(status=solver.status_name(status),rectangles=len(xs),
                  wall_seconds=solver.wall_time,deterministic_time=solver.response_proto.deterministic_time,
                  model_variables=len(model.proto.variables),best_bound=solver.best_objective_bound,
                  translation_windows=sum(map(len,domains.values())),ceiling_mm=cap/GRID)
    if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        return None,record
    trial = deepcopy(layout)
    active = [p for p in trial["placements"] if p["sheet_id"] == sheet]
    for i,x,y,choices in variables:
        _,degrees,l,b = next(c for c in choices if solver.value(c[0]))
        active[i]["transform"].update(translation=[(solver.value(x)-l)/GRID,(solver.value(y)-b)/GRID],
                                      rotation_radians=degrees*pi/180)
    return trial,record


def run(binary,output,matrix,seed,use_windows,matched=False):
    results = Path(__file__).resolve().parents[1]
    material_limit = None
    if matched:
        pair, = [p for p in json.loads((results/matrix/"results.json").read_bytes())["pairs"]
                 if p["job"] == "c-bracket-mixed" and p["kerf_mm"] == 0.2]
        material_limit = pair["normal_material"]*1.01
    for arm in ("off","bonus"):
        stem = f"c-bracket-mixed-k0.2-s{seed}-{arm}"
        folder = output/matrix/stem
        with ZipFile(results/matrix/f"{stem}.zip") as archive:
            job,layout,source = [json.loads(archive.read(name)) for name in
                                 ("nested/job.json","nested/layout.json","validate-stdout.json")]
        for count in ((4,8,12) if matched else (4,8)):
            trial,row = optimize(job,layout,source["metrics"]["last_sheet_id"],count,use_windows,material_limit)
            tag = f"{'matched' if matched else 'window' if use_windows else 'joint'}-{count}"
            row.update(matrix=matrix,seed=seed,arm=arm,variant=tag,original=source["metrics"]["normalized_material"],
                       original_saved_mm=saved(source))
            if trial is not None:
                path = folder/f"{tag}.json"
                path.write_text(json.dumps(trial),encoding="utf-8")
                p = subprocess.run([binary,"validate","--library",folder/"library.json",
                                    "--request",folder/"request.json","--layout",path],capture_output=True)
                (folder/f"{tag}-validation.json").write_bytes(p.stdout)
                check = json.loads(p.stdout)
                row["valid"] = p.returncode == 0 and check["valid"]
                if row["valid"]:
                    row.update(material=check["metrics"]["normalized_material"],saved_mm=saved(check))
            (folder/f"{tag}-result.json").write_text(json.dumps(row,indent=2)+"\n",encoding="utf-8")
            print(stem,tag,row["status"],row.get("material"),flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("matrix",type=int,choices=range(len(MATRICES)))
    parser.add_argument("seed",type=int,choices=range(3))
    parser.add_argument("--windows",action="store_true")
    parser.add_argument("--matched",action="store_true")
    args = parser.parse_args()
    run(args.binary.resolve(),args.output,MATRICES[args.matrix],args.seed,args.windows or args.matched,args.matched)
