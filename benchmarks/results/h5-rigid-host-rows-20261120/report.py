"""Render the per-job gate and comparison tables after verifying the full archived run."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from statistics import median
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent


def read(path):
    return json.loads(path.read_bytes())


def rows_and_inserts(folder, raw):
    accepted = Counter()
    for row in raw["rows"]:
        with ZipFile(folder / row["archive"]) as archive:
            messages = archive.read("nest-stderr.log").decode().splitlines()
        used_rows = any(json.loads(line).get("stage") == "common-line-rows" for line in messages if line.startswith("{"))
        if used_rows:
            assert row["arm"] == "bonus"
            accepted[row["job"]] += 1
        for job, count in (("m-mechanical-large-plates", 21), ("m-mechanical-panel-hardware", 49)):
            if row["job"] == job:
                assert row["parts_in_holes"] == count
    return accepted


def write_report():
    audit = read(HERE / "confirmation.json")
    folder = RESULTS / audit["measurement"]
    raw = read(folder / "results.json")
    assert audit["source"] == raw["product_commit"] and len(raw["jobs"]) == 13
    assert audit["geometry"]["checked_layouts"] == raw["valid"] == raw["total"] == 234
    gates = audit["gates"]
    assert [g["kerf_mm"] for g in gates] == [0.2, 1.5]
    assert all(len(g["pairs"]) == 13 for g in gates)
    pairs = {(p["job"], g["kerf_mm"]): p for g in gates for p in g["pairs"]}
    passed = all(g["median_saved_percent"] >= 10 and all(p["within_material"] for p in g["pairs"]) for g in gates)
    assert passed == audit["passed"]
    accepted = rows_and_inserts(folder, raw)
    outcome = ("The opt-in search met the material and cut-length requirements at both kerfs." if passed
               else "The opt-in search missed at least one material or cut-length requirement. H5 remains open.")
    lines = ["# Common-line cutting with inserts carried by their frames", "", outcome + " "
             "All 234 layouts passed validation. Each run used one physical core for 60 seconds. The three arms were "
             "ordinary nesting, common-line detection, and common-line search. They used identical stock, parts, spacing and seeds 0–2. "
             "Both common-line arms allowed parts inside holes. The default common-line policy reserves holes. "
             f"[Raw runs and three-arm scores]({folder.name}/README.md).", "",
             "| Kerf | Median cutting saved | Largest material increase vs ordinary | Within +1% |",
             "| --- | ---: | ---: | ---: |"]
    for g in gates:
        worst = max(g["pairs"], key=lambda p: p["material_change_percent"])
        count = sum(p["within_material"] for p in g["pairs"])
        lines.append(f"| {g['kerf_mm']} mm | {g['median_saved_percent']:.3f}% | "
                     f"{worst['material_change_percent']:+.3f}% ({worst['job']}) | {count}/13 |")
    lines += ["", "## Material and cutting distance", "",
              "Material change is the ratio of the three-seed bonus median to the ordinary median, minus one. "
              "Cutting savings are the three-seed median of the fraction saved by replacing separate exterior cuts with compensated shared cuts. "
              "The 10% cutting threshold applies to the median across all 13 jobs at each kerf. The +1% material ceiling applies separately to every job.", "",
              "| Job | Laser material | Laser cut saved, bonus off | Laser cut saved, bonus on | Plasma material | Plasma cut saved, bonus off | Plasma cut saved, bonus on |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for job in raw["jobs"]:
        cells = []
        for kerf in (0.2, 1.5):
            p = pairs[job, kerf]
            cells += [f"{p['material_change_percent']:+.3f}%", f"{p['cut_saved_percent']['off']:.3f}%",
                      f"{p['cut_saved_percent']['bonus']:.3f}%"]
        lines.append("| " + " | ".join([job, *cells]) + " |")
    geo = audit["geometry"]
    lines += ["", "## Geometry and application checks", "",
              f"The independent replay checked {audit['archive_members']:,} archived files, "
              f"{geo['pair_distances']:,} same-sheet part pairs and {geo['shared_edges']:,} shared edges against the original source. "
              f"The maximum CUT vertex difference was {geo['max_cut_vertex_error_mm']:.9f} mm. The maximum half-kerf offset difference was "
              f"{geo['max_offset_difference_mm']:.6f} mm against the 0.01 mm tolerance. "
              f"[Independent geometry and matched-input checks]({HERE.name}/confirmation.json).", "",
              f"The solver accepted a row construction in {sum(accepted.values())} of the 78 bonus runs, including "
              f"{accepted['m-mechanical-large-plates']}/6 large-plate and {accepted['m-mechanical-panel-hardware']}/6 panel-hardware runs. "
              "All mechanical runs retained 21 large-plate inserts or 49 panel-hardware inserts in holes. On the 66-part large-plate job, "
              "the CLI, MCP and Firefox completed the same work budget with identical placements. Chrome returned a valid earlier placement "
              "at the 30-second wall limit on both its first run and isolated replay. "
              "Given the completed placement, all four surfaces produced byte-identical SVG and DXF exports. "
              f"[Pilot and controls](h5-rigid-host-pilot-20261120.md), [surface evidence]({HERE.name}/surfaces.json).", "",
              "The laser SVG and plasma DXF were opened in native LightBurn 2.1.01 in October. The current export produced the same four files as the "
              "previous verified build. Its R2007 DXFs agree with the native-checked originals in units, layers and all nine cutting entities. "
              "The line and arc lead reservations also reproduced their previous validations. "
              "[Native measurements and screenshots](h5-commonline-checkpoint-20261014.md#native-lightburn-evidence).", "",
              "The workspace passed 312 tests. Both release Sparrow tests passed, including one skipped in debug. "
              "The release CLI passed 28 end-to-end tests and the core passed all seven common-line geometry tests. "
              "The browser suite passed 88 tests with four optional checks skipped. "
              f"[Test logs and combined-PR checks]({HERE.name}/functional.json).", "",
              "## Deepnest comparison", "",
              "Deepnest used its required zero spacing. Its native merged length and the saving measured from its SVG are reported separately in millimetres. "
              "The 39 runs yielded 35 layouts and four no-layout outcomes. Medians below require all three seeds. "
              "[Independent archive replay](h5-opt-in-hole-audit-20261120/deepnest-replay.json).", "",
              "| Job | Nestbolt laser saved, mm | Nestbolt plasma saved, mm | Deepnest native merged, mm | Deepnest SVG saved, mm |",
              "| --- | ---: | ---: | ---: | ---: |"]
    deep = read(RESULTS / "h5-opt-in-hole-audit-20261120/deepnest-replay.json")
    assert sha256((RESULTS / deep["source"]).read_bytes()).hexdigest() == deep["sha256"]
    for job in raw["jobs"]:
        values = []
        for kerf in (0.2, 1.5):
            lengths = [r["cut_without_common_mm"] - r["cut_with_common_mm"] for r in raw["rows"]
                       if r["job"] == job and r["kerf_mm"] == kerf and r["arm"] == "bonus"]
            assert len(lengths) == 3
            values.append(f"{median(lengths):,.1f}")
        competitor = deep["jobs"][job]
        for key in ("native_merged_length_mm", "export_saved_length_mm"):
            values.append(f"{competitor[key]['median']:,.1f}" if competitor["valid"] == 3 else f"{competitor['valid']}/3 valid")
        lines.append("| " + " | ".join([job, *values]) + " |")
    (RESULTS / (HERE.name + ".md")).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_report()
