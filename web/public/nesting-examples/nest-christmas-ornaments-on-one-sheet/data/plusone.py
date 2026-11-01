"""Does all-parts mode, with its improvement search, fit one more of each design than the fill pass did?

Usage: python -I plusone.py <run-dir>
For each design: quantity = the best fill count over seeds 0-4, plus one; unlimited 12 x 12 in sheets; 60 s
repeatable budget, seed 0. One sheet used means it fitted.
"""
import json
import subprocess
import sys
from pathlib import Path

NB = "nestbolt"  # path to the nestbolt command-line tool
RUN = Path(sys.argv[1]).resolve()
res = json.loads((RUN / "results.json").read_text(encoding="utf-8"))
out = []
for i, d in enumerate(["bauble", "star", "tree", "bell", "snowflake", "stocking"], start=1):
    best = max(r["placed"] for r in res if r["design"] == d)
    req = json.loads((RUN / f"fill-{d}-request.json").read_text(encoding="utf-8"))
    req["name"] = f"{best + 1} {d} ornaments, all-parts mode, on 12 x 12 in sheets"
    req["parts"][0]["quantity"] = best + 1
    req["sheets"][0].pop("count", None)
    req.pop("mode", None)
    rp = RUN / f"plusone-{d}-request.json"
    rp.write_text(json.dumps(req, indent=2) + "\n", encoding="utf-8", newline="\n")
    od = RUN / f"out-plusone-{d}"
    r = subprocess.run([NB, "nest", "--library", "library.json", "--request", rp.name, "--out-dir", str(od),
                        "--seconds", "60", "--repeatable", "--seed", "0"], cwd=RUN, capture_output=True, text=True)
    if r.returncode != 0:
        out.append({"design": d, "quantity": best + 1, "error": r.stderr.strip()[:300]})
    else:
        rep = json.loads((od / "report.json").read_text(encoding="utf-8"))
        m = rep["validation"]["metrics"]
        out.append({"design": d, "quantity": best + 1, "sheets": m["sheets_used"], "valid": rep["validation"]["valid"],
                    "elapsed_s": round(rep["elapsed_s"], 1), "repeatable": rep.get("repeatable")})
    print(json.dumps(out[-1]), flush=True)
(RUN / "plusone.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
