"""Compare existing fixed-work requests on the original and candidate CLI builds."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
MEASURED = ROOT / "benchmarks/results/h5-common-opt-in-holes-20261120T135332Z"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before",type=Path)
    parser.add_argument("after",type=Path)
    parser.add_argument("work",type=Path)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    binaries = [p.resolve() for p in (args.before,args.after)]
    hashes = [sha256(p.read_bytes()).hexdigest() for p in binaries]
    assert hashes[0] == json.loads((MEASURED/"plan.json").read_bytes())["guards"]["binary"]
    cases = []
    args.work.mkdir(exist_ok=False,parents=True)
    for job in ["c-bracket-mixed","m-mechanical-large-plates"]:
        with ZipFile(MEASURED/f"{job}-k0.2-s0-off.zip") as z:
            library = args.work/f"{job}-library.json"
            library.write_bytes(z.read("library.json"))
            request = json.loads(z.read("request.json"))
        for mode in ["ordinary","reserved","reserved-bonus"]:
            req = dict(request)
            if mode=="ordinary":
                req.pop("common_line")
            else:
                req["common_line"] = {"kerf_mm":0.2,"search_bonus":mode=="reserved-bonus"}
            path = args.work/f"{job}-{mode}.json"
            path.write_text(json.dumps(req)+"\n",encoding="utf-8",newline="\n")
            snapshots = []
            for index,binary in enumerate(binaries):
                folder = args.work/f"{job}-{mode}-{index}"
                result = subprocess.run([binary,"nest","--library",library,"--request",path,"--out-dir",folder,
                                         "--seconds","3","--seed","0","--repeatable","--time-limit","60"],capture_output=True,timeout=80)
                assert result.returncode==0,result.stderr
                report = json.loads((folder/"report.json").read_bytes())
                assert report["repeatable"] and report["validation"]["valid"]
                report.pop("elapsed_s")
                # DXF headers may include build or writer metadata. Compare
                # the actual emitted bytes too, since each writer here is fixed.
                files = {p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir()) if p.name!="report.json"}
                snapshots.append(dict(report=report,files=files))
            assert snapshots[0]==snapshots[1],(job,mode,[(k,v==snapshots[1]["files"].get(k)) for k,v in snapshots[0]["files"].items()])
            cases.append(dict(job=job,mode=mode,files=snapshots[0]["files"],report_sha256=sha256(json.dumps(snapshots[0]["report"],sort_keys=True).encode()).hexdigest()))
    args.output.write_text(json.dumps(dict(binary_sha256=hashes,cases=cases),indent=2)+"\n",encoding="utf-8",newline="\n")
    print("Identical fixed-work requests, layouts, reports (excluding elapsed time), SVGs and DXFs in",len(cases),"cases.")


if __name__=="__main__":
    main()
