"""The most engraved ornaments that all-parts mode places on one offcut (repeatable, seed 0).

Usage: python maxfit.py <run-dir> <stock: traced-offcut | partly-used> <start N> [seconds, default 30]
N ornaments cycle through the six designs in project order (bauble, star, tree, bell, snowflake, stocking).
Stops at the first N that fails. A failure shows the limit of this search at this budget, not an impossible count.
"""
import json
import subprocess
import sys
from pathlib import Path

NB = "nestbolt"  # the v0.2.0-alpha.1 nestbolt executable, on PATH or as a full path
RUN = Path(sys.argv[1]).resolve()
stock, n = sys.argv[2], int(sys.argv[3])
SECS = sys.argv[4] if len(sys.argv) > 4 else "30"
base = json.loads((RUN / f"{stock}-request.json").read_text(encoding="utf-8"))
log, best = [], None
while True:
    req = json.loads(json.dumps(base))
    req.pop("mode", None)
    req["name"] = f"{n} engraved ornaments, all-parts mode, on one offcut ({stock})"
    for i, p in enumerate(req["parts"]):
        p["quantity"] = n // 6 + (1 if i < n % 6 else 0)
    rp = RUN / f"all-{stock}-{n}-request.json"
    rp.write_text(json.dumps(req, indent=1) + "\n", encoding="utf-8", newline="\n")
    od = RUN / f"out-all-{stock}-{n}"
    r = subprocess.run([NB, "nest", "--library", "engraved-ornaments.lbrn2", "--request", rp.name, "--out-dir",
                        str(od), "--seconds", SECS, "--repeatable", "--seed", "0"], cwd=RUN, capture_output=True,
                       text=True)
    if r.returncode != 0:
        res = {"n": n, "error": r.stderr.strip()[:300]}
    else:
        rep = json.loads((od / "report.json").read_text(encoding="utf-8"))
        m = rep["validation"]["metrics"]
        res = {"n": n, "valid": rep["validation"]["valid"], "placed": m["placed_parts"], "sheets": m["sheets_used"],
               "utilization": round(m["utilization"], 4), "placed_area_mm2": round(m["placed_area"], 1),
               "elapsed_s": round(rep["elapsed_s"], 1)}
    log.append(res)
    print(json.dumps(res), flush=True)
    if res.get("valid") and res.get("placed") == n:
        best = n
        n += 1
    else:
        break
(RUN / f"maxfit-{stock}.json").write_text(json.dumps({"best": best, "attempts": log}, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
print("best", best)
