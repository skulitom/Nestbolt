"""Guard against false benchmark passes and silently incomplete placements."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from m0 import check_output, score_widths


class ReproductionEvidence(unittest.TestCase):
    def test_partial_failed_and_smoke_cannot_pass(self):
        for widths, smoke in [([], False), ([100, 100], False), ([100, 100, 100], True)]:
            self.assertFalse(score_widths(widths, 3, 100, .01, smoke)[1])
        self.assertTrue(score_widths([99.9, 100, 100.1], 3, 100, .01, False)[1])
        self.assertFalse(score_widths([98, 98, 98], 3, 100, .01, False)[1])
        self.assertFalse(score_widths([102, 102, 102], 3, 100, .01, False)[1])

    def test_invalid_metrics_are_not_results(self):
        for value in [float("nan"), float("inf"), 0, -1]:
            with self.assertRaises(ValueError):
                score_widths([100, 100, value], 3, 100, .01, False)

    def test_output_integrity(self):
        instance = {"name": "test", "strip_height": 10}
        placed = [{"item_id": 0, "transformation": {"rotation": 0, "translation": [0, 0]}}]
        data = {**instance, "solution": {"strip_width": 20, "density": .5,
            "layout": {"placed_items": placed}}}
        finish = {"strip_width": 20, "density": .5}
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "input.json"
            source.write_text(json.dumps({"items": [{"id": 0, "demand": 1}]}), encoding="utf-8")
            with patch("m0.materialize_input", return_value=source):
                self.assertEqual(check_output(data, instance, finish)["placed_count"], 1)
                variants = []
                missing = deepcopy(data); missing["solution"]["layout"]["placed_items"] = []; variants.append(missing)
                duplicate = deepcopy(data); duplicate["solution"]["layout"]["placed_items"] *= 2; variants.append(duplicate)
                wrong = deepcopy(data); wrong["name"] = "other"; variants.append(wrong)
                metric = deepcopy(data); metric["solution"]["strip_width"] = 30; variants.append(metric)
                nonfinite = deepcopy(data); nonfinite["solution"]["layout"]["placed_items"][0]["transformation"]["rotation"] = float("nan"); variants.append(nonfinite)
                for changed in variants:
                    with self.assertRaises(ValueError):
                        check_output(changed, instance, finish)


if __name__ == "__main__":
    unittest.main()
