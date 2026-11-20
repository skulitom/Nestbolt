"""Compare public native and browser outputs, retaining the first Chrome hard-limit result."""
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED,ZipFile


ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"output"
DEST=Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_bytes())


def normalized(report):
    return report["validation"]["metrics"]["normalized_material"]


def main():
    cli=OUT/"h5-native-row-cli-fixed-20261120"
    mcp=OUT/"h5-native-row-mcp-20261120"
    layout=read(cli/"layout.json")
    a,b=read(cli/"report.json"),read(mcp/"nested/report.json")
    assert len(layout["placements"])==80 and normalized(a)<1.64
    assert a["repeatable"] and b["repeatable"] and read(mcp/"nested/layout.json")==layout
    assert {k:v for k,v in a.items() if k!="elapsed_s"}=={k:v for k,v in b.items() if k!="elapsed_s"}
    files={}
    for p in sorted(cli.glob("sheet-*")):
        assert p.read_bytes()==(mcp/"nested"/p.name).read_bytes()
        files[p.name]=sha256(p.read_bytes()).hexdigest()
    assert len(files)==4 and read(mcp/"rpc.json")["validate"]["valid"]
    browser=[
        ("first-chrome-work",OUT/"h5-native-row-surfaces-20261120/chrome.json","work",False),
        ("firefox-work",OUT/"h5-native-row-surfaces-20261120/firefox.json","work",True),
        ("chrome-work",OUT/"h5-native-row-chrome-replay-20261120/chrome.json","work",True),
        ("chrome-wall",OUT/"h5-native-row-surfaces-wall-20261120/chrome.json","wall",True),
        ("firefox-wall",OUT/"h5-native-row-surfaces-wall-20261120/firefox.json","wall",True)]
    checks=[]
    with ZipFile(DEST/"surfaces.zip","w",ZIP_DEFLATED) as z:
        for tag,folder in [("cli",cli),("mcp",mcp)]:
            for p in sorted(folder.rglob("*")):
                if p.is_file():
                    z.write(p,tag+"/"+p.relative_to(folder).as_posix())
        for name,path,mode,completed in browser:
            result=read(path)
            n=result["nested"]
            assert result["validated"]["valid"] and n["validation"]["valid"]
            same=n["layout"]==layout
            if completed:
                assert same and normalized(n)==normalized(a)
                assert n["repeatable"]==(mode=="work")
                for native,wasm in zip(a["common_line"],n["common_line"],strict=True):
                    assert native["sheet_id"]==wasm["sheet_id"]
                    assert abs(native["saved_length_mm"]-wasm["saved_length_mm"])<1e-8
            else:
                assert mode=="work" and not n["repeatable"] and n["elapsed_seconds"]>=n["seconds"]
            checks.append(dict(name=name,mode=mode,repeatable=n["repeatable"],elapsed_s=n["elapsed_seconds"],
                               material=normalized(n),valid=True,layout_equal_to_cli=same))
            z.write(path,"browsers/"+name+".json")
    summary=dict(placed_copies=len(layout["placements"]),native_material=normalized(a),
                 native_reports_equal_excluding_elapsed=True,mcp_layout_equal=True,export_sha256=files,
                 browser_checks=checks)
    (DEST/"surfaces.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8",newline="\n")
    print("Both native surfaces and four completed browser paths agree on all 80 copy transforms.")


if __name__=="__main__":
    main()
