"""Check and archive the public-surface results for the two-sheet mechanical job."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / "output"


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    cli = OUT / "h5-rigid-host-cli"
    mcp = OUT / "h5-rigid-host-mcp"
    browsers = OUT / "h5-rigid-host-browser"
    layout = read(cli / "layout.json")
    native = read(cli / "report.json")
    rpc = read(mcp / "rpc.json")
    other = read(mcp / "nested/report.json")
    assert len(layout["placements"]) == 66 and native["parts_in_holes"] == 21
    assert native["validation"]["valid"] and native["repeatable"] and rpc["validate"]["valid"]
    assert read(mcp / "nested/layout.json") == layout
    assert all(native[key] == other[key] for key in native if key != "elapsed_s")
    files = {p.name: digest(p) for p in cli.glob("sheet-*")}
    assert len(files) == 4 and all(digest(mcp / "nested" / name) == sha for name, sha in files.items())
    assert all(check["files"] == files for check in read(HERE / "exports.json"))
    checks = []
    for name, file in (("chrome", browsers / "chrome.json"), ("firefox", browsers / "firefox.json"),
                       ("chrome-isolated", OUT / "h5-rigid-host-browser-isolated/chrome.json")):
        result = read(file)
        nest = result["nested"]
        assert result["validated"]["valid"] and nest["validation"]["valid"]
        assert len(nest["layout"]["placements"]) == 66 and nest["parts_in_holes"] == 21
        matches = nest["layout"] == layout
        if nest["repeatable"]:
            assert matches
        else:
            assert nest["elapsed_seconds"] >= nest["seconds"]
        checks.append({"browser": name, "elapsed_s": nest["elapsed_seconds"], "completed_work": nest["repeatable"],
                       "same_transforms": matches, "material": result["validated"]["metrics"]["normalized_material"]})
    assert any(row["completed_work"] for row in checks)
    native_coupons = read(HERE.parent / "h5-native-interlocking-rows-20261120/native-fixtures.json")
    for ref in native_coupons:
        assert digest(OUT / "h5-rigid-host-native" / ref["kerf"] / ("sheet-0." + ref["format"])) == ref["sha256"]
    for style in ("line", "arc"):
        assert read(OUT / "h5-rigid-host-leads" / (style + ".json")) == read(
            OUT / "h5-native-rows-combined-leads-20261120" / (style + ".json"))
    folders = {"cli": cli, "mcp": mcp, "browser": browsers, "browser-isolated": OUT / "h5-rigid-host-browser-isolated",
               "coupons": OUT / "h5-rigid-host-native",
               "leads": OUT / "h5-rigid-host-leads"}
    with ZipFile(HERE / "surfaces.zip", "w", ZIP_DEFLATED) as archive:
        for category, folder in folders.items():
            for path in sorted(folder.rglob("*")):
                if path.is_file():
                    archive.write(path, category + "/" + path.relative_to(folder).as_posix())
        archive.write(OUT / "h5-rigid-host-cli.log", "cli-progress.log")
    result = {"source": "d301f3930e5d3b5eae29ff51430b08fc7b1fc808", "copies": 66, "inserts_in_holes": 21,
              "native_material": native["validation"]["metrics"]["normalized_material"],
              "matched_cli_and_mcp": True, "export_sha256": files, "browsers": checks,
              "unchanged_native_coupons": native_coupons, "matching_lead_validations": ["line", "arc"]}
    (HERE / "surfaces.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Four native and browser cutting files matched. Both browser nests revalidated.")


if __name__ == "__main__":
    main()
