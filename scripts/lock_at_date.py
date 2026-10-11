"""Reconstruct a Cargo lock using releases available at a declared historical date.

This cannot recover an unarchived original lock. It supplies a documented,
repeatable replacement, then the resulting Cargo.lock must be committed.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import tomllib
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--before", required=True)
    parser.add_argument("--toolchain", required=True)
    parser.add_argument("--allow-yanked", action="append", default=[],
                        help="Explicit historical-only exception for a named crate")
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    cutoff = datetime.fromisoformat(args.before).replace(tzinfo=timezone.utc)
    cache = ROOT / ".cache/crate-history"
    cache.mkdir(parents=True, exist_ok=True)
    cargo = ["cargo", f"+{args.toolchain}"]

    def versions(name):
        path = cache / f"{name}.json"
        if not path.exists():
            request = Request(f"https://crates.io/api/v1/crates/{name}", headers={"User-Agent": "Nestbolt-reproduction/0.1"})
            with urlopen(request, timeout=60) as response:
                path.write_bytes(response.read())
        return json.loads(path.read_text(encoding="utf-8"))["versions"]

    history = {}
    for iteration in range(200):
        packages = tomllib.loads(manifest.with_name("Cargo.lock").read_text(encoding="utf-8"))["package"]
        registry = [p for p in packages if p.get("source", "").startswith("registry+")]
        missing = sorted({p["name"] for p in registry} - history.keys())
        with ThreadPoolExecutor(max_workers=4) as pool:
            history.update(zip(missing, pool.map(versions, missing)))
        candidates = []
        for package in registry:
            releases = history[package["name"]]
            current = next(v for v in releases if v["num"] == package["version"])
            if datetime.fromisoformat(current["created_at"].replace("Z", "+00:00")) <= cutoff:
                continue
            eligible = [v for v in releases if (not v["yanked"] or package["name"] in args.allow_yanked)
                        and "-" not in v["num"].split("+")[0]
                        and datetime.fromisoformat(v["created_at"].replace("Z", "+00:00")) <= cutoff]
            eligible.sort(key=lambda v: tuple(int(x) for x in v["num"].split("+")[0].split(".")), reverse=True)
            if eligible:
                candidates.append((package, eligible))
        if not candidates:
            # Ensure no post-cutoff package slipped through merely because it has no old release.
            late = [p for p in registry if datetime.fromisoformat(next(v for v in history[p['name']] if v['num']==p['version'])["created_at"].replace("Z", "+00:00")) > cutoff]
            if late:
                raise RuntimeError(f"Packages with no release before cutoff remain: {late}")
            print(f"Historical lock complete: {len(registry)} registry packages before {args.before}.")
            return
        errors = []
        for package, eligible in candidates:
            # Try the compatible historical release family first. Parent downgrades
            # in subsequent iterations remove packages introduced after the cutoff.
            prefix = package["version"].split(".")[:2 if package["version"].startswith("0.") else 1]
            matched = [v for v in eligible if v["num"].split(".")[:len(prefix)] == prefix]
            if not matched:
                errors.append(f"No compatible historical release for {package['name']} {package['version']}")
                continue
            version = matched[0]["num"]
            result = subprocess.run(cargo + ["update", "--manifest-path", str(manifest), "-p",
                f"{package['name']}@{package['version']}", "--precise", version], cwd=ROOT, text=True, capture_output=True)
            if result.returncode == 0:
                print(f"Pinned {package['name']} {package['version']} -> {version}", flush=True)
                break
            errors.append(result.stderr[-1400:])
        else:
            raise RuntimeError("Cannot reconstruct further without changing constraints:\n" + "\n".join(errors))
    raise RuntimeError("Historical lock reconstruction exceeded iteration limit")


if __name__ == "__main__":
    main()
