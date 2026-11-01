"""Run every ornament nest for the page and collect the metrics.

Usage: python -I runall.py <run-dir>   (the run dir holds library.json and the requests from gen.py)
"""
import json
import subprocess
import sys
import time
from pathlib import Path

NB = "nestbolt"  # path to the nestbolt command-line tool
RUN = Path(sys.argv[1]).resolve()
DESIGNS = ["bauble", "star", "tree", "bell", "snowflake", "stocking"]
SEEDS = [0, 1, 2, 3, 4]


def nest(request, out, seconds, seed):
    out = RUN / out
    if out.exists():
        raise SystemExit(f"{out} exists")
    t = time.perf_counter()
    r = subprocess.run([NB, "nest", "--library", "library.json", "--request", request, "--out-dir", str(out),
                        "--seconds", str(seconds), "--repeatable", "--seed", str(seed)],
                       cwd=RUN, capture_output=True, text=True)
    wall = time.perf_counter() - t
    if r.returncode != 0:
        raise SystemExit(f"{request} seed {seed}: {r.stderr}")
    rep = json.loads((out / "report.json").read_text(encoding="utf-8"))
    m = rep["validation"]["metrics"]
    return {"request": request, "seed": seed, "seconds": seconds, "out": out.name,
            "valid": rep["validation"]["valid"], "repeatable": rep.get("repeatable"),
            "elapsed_s": round(rep.get("elapsed_s", 0), 2), "wall_s": round(wall, 2),
            "placed": m["placed_parts"], "requested": m["requested_parts"], "sheets": m["sheets_used"],
            "utilization": round(m["utilization"], 4), "parts_in_holes": rep.get("parts_in_holes")}


results = []
for d in DESIGNS:
    for s in SEEDS:
        res = nest(f"fill-{d}-request.json", f"out-fill-{d}-s{s}", 30, s)
        res["design"] = d
        results.append(res)
        print(d, s, res["placed"], res["valid"], res["elapsed_s"], flush=True)

for name in ("mixed-18", "mixed-24"):
    res = nest(f"{name}-request.json", f"out-{name}-s0", 60, 0)
    res["design"] = name
    results.append(res)
    print(name, res["placed"], res["sheets"], res["utilization"], res["valid"], res["elapsed_s"], flush=True)

(RUN / "results.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8", newline="\n")
