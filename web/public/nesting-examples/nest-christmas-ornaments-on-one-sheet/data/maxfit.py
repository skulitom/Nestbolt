"""Find the most copies of each design that all-parts mode places on one 12 x 12 in sheet (60 s repeatable, seed 0).

Usage: python -I maxfit.py <run-dir>
Starts one above plusone.json's quantity for each design that fitted, and stops at the first count that needs a
second sheet. A failure at seed 0 and 60 s shows the limit of that search, not that the count is impossible.
"""
import json
import subprocess
import sys
from pathlib import Path

NB = "nestbolt"  # path to the nestbolt command-line tool
RUN = Path(sys.argv[1]).resolve()
prev = json.loads((RUN / "plusone.json").read_text(encoding="utf-8"))
log = []


def attempt(d, q):
    req = json.loads((RUN / f"plusone-{d}-request.json").read_text(encoding="utf-8"))
    req["name"] = f"{q} {d} ornaments, all-parts mode, on 12 x 12 in sheets"
    req["parts"][0]["quantity"] = q
    rp = RUN / f"all-{d}-{q}-request.json"
    rp.write_text(json.dumps(req, indent=2) + "\n", encoding="utf-8", newline="\n")
    od = RUN / f"out-all-{d}-{q}"
    r = subprocess.run([NB, "nest", "--library", "library.json", "--request", rp.name, "--out-dir", str(od),
                        "--seconds", "60", "--repeatable", "--seed", "0"], cwd=RUN, capture_output=True, text=True)
    if r.returncode != 0:
        return {"design": d, "quantity": q, "error": r.stderr.strip()[:300]}
    rep = json.loads((od / "report.json").read_text(encoding="utf-8"))
    m = rep["validation"]["metrics"]
    return {"design": d, "quantity": q, "sheets": m["sheets_used"], "valid": rep["validation"]["valid"],
            "utilization": round(m["utilization"], 4), "elapsed_s": round(rep["elapsed_s"], 1),
            "repeatable": rep.get("repeatable")}


only = sys.argv[2:]
best = {}
for p in prev:
    d = p["design"]
    if only and d not in only:
        continue
    if p.get("sheets") != 1:
        best[d] = p["quantity"] - 1
        continue
    q = p["quantity"]
    best[d] = q
    while True:
        q += 1
        res = attempt(d, q)
        log.append(res)
        print(json.dumps(res), flush=True)
        if res.get("sheets") == 1 and res.get("valid"):
            best[d] = q
        else:
            break
(RUN / f"maxfit{'-' + '-'.join(only) if only else ''}.json").write_text(json.dumps({"best_one_sheet": best, "attempts": log}, indent=1) + "\n",
                                 encoding="utf-8", newline="\n")
print(json.dumps(best))
