"""Replay geometry and SVG/DXF offsets for every box-job arm while the other jobs run."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from math import cos, dist, sin
from pathlib import Path
import sys
from zipfile import ZipFile

from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.polygon import orient

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"h5-opt-in-hole-audit-20261120"))
from audit import audit_archive


def straight_ring(coords):
    # Anchor at a genuine corner so the author's choice of starting vertex
    # cannot divide a straight side into two short pieces.
    vertices = coords[:-1]
    n = len(vertices)
    corner = max(range(n), key=lambda i: Point(vertices[i]).distance(
        LineString([vertices[(i-1) % n], vertices[(i+1) % n]])))
    ordered = vertices[corner:] + vertices[:corner+1]
    original = LineString(ordered)
    simplified = original.simplify(1e-9, preserve_topology=False)
    assert simplified.is_ring and original.hausdorff_distance(simplified) <= 1e-9
    assert abs(original.length - simplified.length) <= 1e-8
    # Verify cyclic order and original straight-side coverage for each segment.
    index = 0
    reduced = list(simplified.coords)
    for start, end in zip(reduced, reduced[1:]):
        stop = ordered.index(end, index+1)
        section = ordered[index:stop+1]
        assert abs(sum(dist(a,b) for a,b in zip(section,section[1:])) - dist(start,end)) <= 1e-9
        index = stop
    assert index == len(ordered)-1
    return reduced


def check(path):
    try:
        return dict(archive=path.name, sheets=audit_archive(path, straight_ring))
    except Exception as error:
        return dict(archive=path.name, error=repr(error))


def original_rejection(path):
    try:
        audit_archive(path)
    except AssertionError as exc:
        owner, original_error, sheet, start, end = exc.args[0]
    else:
        raise AssertionError("expected the historical single-segment oracle to reject this span")
    with ZipFile(path) as archive:
        job,layout=[json.loads(archive.read(f"nested/{name}.json")) for name in ("job","layout")]
    part_id, index=owner.split("#")
    t=next(p["transform"] for p in layout["placements"] if p["part_id"]==part_id and p["copy_index"]==int(index))
    outline=next(p["geometry"][0]["outer"] for p in job["parts"] if p["id"]==part_id)
    c,s=cos(t["rotation_radians"]),sin(t["rotation_radians"])
    polarity=-1 if t["mirrored"] else 1
    x,y=t["translation"]
    polygon=Polygon([(x+c*polarity*a-s*b,y+s*polarity*a+c*b) for a,b in outline])
    coords=list(orient(polygon,sign=1.0).exterior.coords)
    target=LineString([start,end])
    def supporting(ring):
        matches=[]
        for a,b in zip(ring,ring[1:]):
            length=dist(a,b)
            if not length:
                continue
            dx,dy=(b[1]-a[1])*job["clearance"]/(2*length),(a[0]-b[0])*job["clearance"]/(2*length)
            line=LineString([(a[0]+dx,a[1]+dy),(b[0]+dx,b[1]+dy)])
            if line.intersection(target.buffer(1e-8)).length > 1e-6:
                matches.append(dict(offset=list(line.coords),length_mm=length,
                                    endpoint_error_mm=max(line.distance(Point(p)) for p in (start,end))))
        return matches
    raw,merged=supporting(coords),supporting(straight_ring(coords))
    assert len(raw)>1 and min(r["endpoint_error_mm"] for r in raw)==original_error
    assert len(merged)==1 and merged[0]["endpoint_error_mm"] < 1e-8
    return dict(archive=path.name,owner=owner,sheet=sheet,reported_endpoints=[start,end],
                first_oracle_error_mm=original_error,individual_source_offsets=raw,continuous_source_offset=merged[0])


def main(folder,out):
    paths=sorted(folder.glob("m-box-*.zip"))
    assert len(paths)==108
    first=original_rejection(folder/"m-box-batch-500-k0.2-s0-bonus.zip")
    (out.parent/"box-offset-first-rejection.json").write_text(json.dumps(first,indent=2)+"\n",encoding="utf-8",newline="\n")
    with ProcessPoolExecutor(3) as pool:
        results=list(pool.map(check,paths))
    out.write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8",newline="\n")
    failures=[r for r in results if "error" in r]
    assert not failures, failures[:3]
    print(len(results),"layouts;",sum(s["pair_distances"] for r in results for s in r["sheets"]),"part distances")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder",type=Path)
    parser.add_argument("out",type=Path)
    args=parser.parse_args()
    main(args.folder,args.out)
