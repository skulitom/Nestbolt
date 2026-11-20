"""Check every matched input triple and reconstruct the scores from saved CLI output."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from math import isclose
from pathlib import Path
from zipfile import ZipFile


def verify(folder):
    result = json.loads((folder/"results.json").read_bytes())
    groups = defaultdict(dict)
    common_sheets = 0
    for row in result["rows"]:
        job, kerf, seed, arm = (row[k] for k in ("job", "kerf_mm", "seed", "arm"))
        with ZipFile(folder/row["archive"]) as archive:
            request = json.loads(archive.read("request.json"))
            job_hash = sha256(archive.read("nested/job.json")).hexdigest()
            library_hash = sha256(archive.read("library.json")).hexdigest()
            assert request["spacing_mm"] == kerf
            if arm == "normal":
                assert "common_line" not in request
            else:
                assert request.pop("common_line") == {
                    "kerf_mm":kerf, "search_bonus":arm=="bonus", "allow_part_in_hole":True
                }
            reference = (request, job_hash, library_hash)
            triple = groups[job,kerf,seed]
            assert arm not in triple
            triple[arm] = reference
            report = json.loads(archive.read("nested/report.json"))
            checked = json.loads(archive.read("validate-stdout.json"))
            assert row["status"]=="valid" and report["validation"]["valid"] and checked["valid"]
            assert checked["metrics"]["normalized_material"] == row["material"]
            assert report["parts_in_holes"] == row["parts_in_holes"]
            assert report["seed"]==seed and report["time_budget_s"]==60
            assert not report["repeatable"]
            if arm != "normal":
                for field in ("cut_length_without_common_mm","cut_length_with_common_mm"):
                    length = sum(s[field] for s in checked["common_line"])
                    stored = row["cut_without_common_mm" if field=="cut_length_without_common_mm" else "cut_with_common_mm"]
                    assert isclose(stored,length,abs_tol=1e-8,rel_tol=0)
                common_sheets += len(checked["common_line"])
    for triple in groups.values():
        assert set(triple)=={"normal","off","bonus"} and triple["normal"]==triple["off"]==triple["bonus"]
    return dict(measurement=folder.name,rows=len(result["rows"]),identical_triples=len(groups),
                revalidated_cutting_sheets=common_sheets)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out",type=Path)
    parser.add_argument("folders",nargs="+",type=Path)
    args=parser.parse_args()
    rows=[verify(f) for f in args.folders]
    args.out.write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(rows)
