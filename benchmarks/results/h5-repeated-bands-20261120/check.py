"""Check offline row constructions against original paths, stock and exported cutting layers."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile

from construct import RESULTS
sys.path[:0] = [str(RESULTS/"h5-bracket-axis-compaction-20261120"),str(RESULTS/"h5-opt-in-hole-audit-20261120")]
from verify import check
from audit import audit_sheet


def main(binary,output,measurements):
    rows = []
    with ZipFile(output/"source-rows.zip","w",ZIP_DEFLATED) as bundle:
        for measurement in measurements:
            records = json.loads((measurement/"results.json").read_bytes())
            bundle.write(measurement/"results.json",measurement.name+"/results.json")
            for record in records:
                path = Path(record["source"])
                folder = measurement/path.stem
                layout,report,library,request = [json.loads((folder/n).read_bytes()) for n in
                    ("layout.json","validation.json","library.json","request.json")]
                with ZipFile(path) as z:
                    job,baseline = [json.loads(z.read("nested/"+n+".json")) for n in ("job","layout")]
                pairs,gap = check(layout,baseline,library,request,report)
                out = folder/"nested"
                subprocess.run([binary,"export","--library",folder/"library.json","--request",folder/"request.json",
                                "--layout",folder/"layout.json","--out-dir",out],capture_output=True,check=True)
                class Exports:
                    def read(self,name):
                        return (folder/name).read_bytes()
                sheets = [audit_sheet(Exports(),s["sheet_id"],job["stocks"][0]["height"],job,layout,s)
                          for s in report["common_line"]]
                rows.append(dict(source=path.name,size=record["maximum_size"] if "maximum_size" in record else 2,
                                 pairs=pairs,min_gap=gap,sheets=sheets,material=record["material"],
                                 saved_fraction=record["saved_fraction"]))
                for item in sorted(p for p in folder.rglob("*") if p.is_file()):
                    bundle.write(item,measurement.name+"/"+str(item.relative_to(measurement)))
    (output/"geometry.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(len(rows),"layouts,",sum(r["pairs"] for r in rows),"pair distances")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary",type=Path)
    parser.add_argument("out",type=Path)
    parser.add_argument("measurements",nargs="+",type=Path)
    args = parser.parse_args()
    main(args.binary.resolve(),args.out.resolve(),args.measurements)
