"""Exercise evidence corruption checks without requiring an upstream solver."""
import json
from pathlib import Path
import tempfile
import unittest

from lbf import digest
from lbf_report import audit_record, contained_file


def fixture(directory):
    metrics = {"normalized_material": 1.25}
    data = {"job.json": {"name": "evidence-test"}, "layout.json": {"placements": []},
        "solver/sol_input.json": {"solution": {}}, "validation.json": {"valid": True, "metrics": metrics}}
    for relative, value in data.items():
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
    record = {"status": "valid", "metrics": metrics, "validator_exit_code": 0,
        "job_sha256": digest(directory / "job.json"),
        "outputs": {relative: digest(directory / relative) for relative in data}}
    path = directory / "run.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    return path, record


class EvidenceTests(unittest.TestCase):
    def test_changed_layout_and_changed_record_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="nestbolt-evidence-") as temp:
            directory = Path(temp)
            path, record = fixture(directory)
            expected = digest(path)
            self.assertEqual(audit_record(path, expected)["metrics"], record["metrics"])
            (directory / "layout.json").write_text('{"changed": true}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Recorded output changed"):
                audit_record(path, expected)
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Run record changed"):
                audit_record(path, expected)

    def test_failed_layout_and_disagreeing_validation_never_have_scores(self):
        with tempfile.TemporaryDirectory(prefix="nestbolt-evidence-") as temp:
            path, record = fixture(Path(temp))
            record["metrics"] = {"normalized_material": .25}
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "disagrees"):
                audit_record(path, digest(path))
            record["status"] = "timeout"
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must not receive a score"):
                audit_record(path, digest(path))

    def test_evidence_paths_cannot_escape_the_run_directory(self):
        with tempfile.TemporaryDirectory(prefix="nestbolt-evidence-") as temp:
            directory = Path(temp)
            (directory / "outside.json").write_text("{}", encoding="utf-8")
            (directory / "run").mkdir()
            with self.assertRaisesRegex(ValueError, "Invalid evidence path"):
                contained_file(directory / "run", "../outside.json")


if __name__ == "__main__":
    unittest.main()
