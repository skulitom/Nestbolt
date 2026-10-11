"""Generate/check internal benchmark schemas from the actual Rust model."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = subprocess.check_output(["cargo", "run", "--quiet", "--locked", "-p", "nestbolt-validator",
        "--example", "schemas"], cwd=ROOT, text=True, encoding="utf-8")
    for filename, schema in json.loads(output).items():
        text = json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
        path = ROOT / "schemas" / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                raise SystemExit(f"Schema is stale: {filename}; run python scripts/schemas.py")
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
    print("Internal benchmark schemas match the Rust model." if args.check else "Generated internal benchmark schemas.")


if __name__ == "__main__":
    main()
