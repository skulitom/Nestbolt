"""Regenerate Nestbolt's original MIT smoke fixtures; never touch held-out data."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    sheet = json.loads((ROOT / "examples/sheet-job.json").read_text(encoding="utf-8"))
    manifest = {
        "schema_version": 1,
        "purpose": "integration_smoke_only",
        "tool": {
            "name": "sparrow", "version": "0.3.0", "license": "MIT",
            "repository": "https://github.com/JeroenGar/sparrow.git",
            "commit": "4629b22795ae6b25b3b460ccde6fb36a71292b6d",
        },
        "cases": [],
    }
    for name, items in [("rectangles", sheet["items"][:1]), ("concave", sheet["items"])]:
        identifier = f"generated-{name}"
        relative = f"benchmarks/fixtures/{identifier}.json"
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"name": identifier, "strip_height": 100, "min_item_separation": 2, "items": items}
        content = (json.dumps(data, indent=2) + "\n").encode()
        path.write_bytes(content)
        manifest["cases"].append({
            "id": identifier, "path": relative, "units": "mm", "license": "MIT",
            "source": "Original Nestbolt geometry from examples/sheet-job.json; scripts/generate_smoke.py",
            "sha256": hashlib.sha256(content).hexdigest(), "held_out": False,
        })
    (ROOT / "benchmarks/smoke.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Generated two original smoke fixtures and checksum manifest.")


if __name__ == "__main__":
    main()
