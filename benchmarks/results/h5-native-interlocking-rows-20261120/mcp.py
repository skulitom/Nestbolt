"""Nest and independently revalidate the mixed brackets through the public stdio MCP server."""
import argparse
import json
import os
from pathlib import Path
import subprocess


def run(binary,source,output):
    output.mkdir(exist_ok=True,parents=True)
    (output/"library.json").write_bytes((source/"library.json").read_bytes())
    request=json.loads((source/"request.json").read_bytes())
    with subprocess.Popen([binary],cwd=output,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL,env={**os.environ,"NESTBOLT_WORKSPACE":str(output)}) as proc:
        def call(method,params,sequence=None):
            msg=dict(jsonrpc="2.0",method=method,params=params)
            if sequence is not None:
                msg["id"]=sequence
            proc.stdin.write((json.dumps(msg)+"\n").encode())
            proc.stdin.flush()
            if sequence is None:
                return
            for line in proc.stdout:
                reply=json.loads(line)
                if reply.get("id")==sequence:
                    assert "error" not in reply,reply
                    return reply["result"]
            raise RuntimeError(f"MCP closed before {method} completed")
        try:
            call("initialize",dict(protocolVersion="2025-03-26",capabilities={},
                                   clientInfo=dict(name="nestbolt-dev-check",version="1")),1)
            call("notifications/initialized",{})
            args=dict(library_path="library.json",request=request)
            result=call("tools/call",dict(name="nest",arguments=dict(**args,out_dir="nested",seed=0,time_budget_s=30)),2)
            reply=result["structuredContent"]
            copies=sum(p["quantity"] for p in request["parts"])
            assert reply["validation"]["valid"] and reply["validation"]["metrics"]["placed_parts"]==copies
            checked=call("tools/call",dict(name="validate_layout",arguments=dict(**args,layout_path="nested/layout.json")),3)
            assert checked["structuredContent"]["valid"]
            (output/"rpc.json").write_text(json.dumps(dict(nest=reply,validate=checked["structuredContent"]),indent=2)+"\n",
                                           encoding="utf-8",newline="\n")
            print(reply["validation"]["metrics"]["normalized_material"],flush=True)
        finally:
            proc.stdin.close()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.terminate()
                proc.wait(timeout=10)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary",type=Path)
    parser.add_argument("source",type=Path)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    run(args.binary.resolve(),args.source.resolve(),args.output.resolve())
