"""Protect benchmark provenance, conversion semantics and tamper detection."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import datasets


class DatasetTests(unittest.TestCase):
    def test_all_sheet_variants_preserve_every_source_vertex_and_copy(self):
        manifest = json.loads(datasets.MANIFEST.read_bytes())
        strips = {}
        for row in manifest["instances"]:
            if row["set"] == "S":
                strips[row["source"]] = json.loads((datasets.DEST / row["path"]).read_bytes())
        self.assertEqual(len(strips), 13)
        self.assertEqual(sum(r["set"] == "B" for r in manifest["instances"]), 35)
        for row in manifest["instances"]:
            job = json.loads((datasets.DEST / row["path"]).read_bytes())
            original = strips[row["source"]]
            self.assertEqual(len(job["parts"]), len(original["parts"]))
            self.assertEqual(row["part_count"], sum(p["quantity"] for p in job["parts"]))
            for part, source in zip(job["parts"], original["parts"]):
                self.assertEqual(part["id"], source["id"])
                self.assertEqual(part["quantity"], source["quantity"])
                self.assertEqual(part["geometry"], source["geometry"])
                self.assertFalse(part["allow_mirror"])
            self.assertEqual(job["clearance"], 0)
            self.assertEqual(job["edge_clearance"], 0)
            self.assertEqual(job["units"], "unitless")

    def test_paper_constraints_and_source_constraints_remain_distinct(self):
        def job(group, name):
            return json.loads((datasets.DEST / group / f"{name}.json").read_bytes())
        mao_s = job("S", "s-mao-strip")
        mao_paper = job("B", "b-mao-nest-mb-given")
        self.assertEqual(mao_s["parts"][0]["rotations"]["degrees"], [0, 90, 180, 270])
        self.assertTrue(all(p["rotations"]["degrees"] == [0, 180] for p in mao_paper["parts"]))
        shapes_s = job("S", "s-shapes0-strip")
        shapes_paper = job("B", "b-shapes0-nest-mb-given")
        self.assertEqual(shapes_s["parts"][0]["rotations"]["degrees"], [0])
        self.assertTrue(all(p["rotations"]["degrees"] == [0, 90, 180, 270] for p in shapes_paper["parts"]))
        swim = job("B", "b-swim-nest-mb-free")
        self.assertEqual(swim["stocks"][0]["width"], 2909.4677415)
        self.assertTrue(all(p["rotations"] == {"kind": "free"} for p in swim["parts"]))
        self.assertEqual(job("B", "b-shirts-nest-mb-given")["stocks"][0]["width"], 19.5)

    def test_bad_source_types_fail_and_empty_angles_are_fixed(self):
        item = {"id": 7, "demand": 2, "allowed_orientations": [],
                "shape": {"type": "simple_polygon", "data": [[0, 0], [2, 0], [0, 1]]}}
        source = {"items": [item]}
        self.assertEqual(datasets.source_parts(source)[0]["rotations"], {"kind": "list", "degrees": [0]})
        item["allowed_orientations"] = None
        self.assertEqual(datasets.source_parts(source)[0]["rotations"], {"kind": "free"})
        item["shape"]["type"] = "polygon"
        with self.assertRaises(ValueError):
            datasets.source_parts(source)

    def test_changed_or_unlisted_job_is_rejected_offline(self):
        with tempfile.TemporaryDirectory(prefix="nestbolt-datasets-") as temp:
            dest = Path(temp) / "datasets"
            shutil.copytree(datasets.DEST, dest)
            with patch.object(datasets, "DEST", dest), patch.object(datasets, "MANIFEST", dest / "academic.json"):
                datasets.check_frozen()
                path = next((dest / "S").glob("*.json"))
                original = path.read_bytes()
                value = json.loads(original)
                value["parts"][0]["quantity"] += 1
                path.write_bytes(datasets.serialized(value))
                with self.assertRaisesRegex(ValueError, "Frozen job changed"):
                    datasets.check_frozen()
                path.write_bytes(original)
                (dest / "B/unlisted.json").write_bytes(original)
                with self.assertRaisesRegex(ValueError, "unlisted"):
                    datasets.check_frozen()


if __name__ == "__main__":
    unittest.main()
