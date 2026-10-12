"""Generate/check the JSON Schemas from the actual Rust model."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    schemas = {}
    for package, example in [("nestbolt-validator", "schemas"), ("nestbolt-core", "public_schemas")]:
        schemas.update(json.loads(subprocess.check_output(["cargo", "run", "--quiet", "--locked", "-p", package,
            "--example", example], cwd=ROOT, text=True, encoding="utf-8")))
    for filename, schema in schemas.items():
        text = json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
        path = ROOT / "schemas" / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                raise SystemExit(f"Schema is stale: {filename}; run python scripts/schemas.py")
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
    print("Schemas match the Rust model." if args.check else "Generated schemas.")


if __name__ == "__main__":
    main()
