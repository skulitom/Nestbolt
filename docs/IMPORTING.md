# Import options and repair reports

Curve precision controls how closely nesting polygons follow the exact source
curves. It does not permit larger gaps to close: the silent endpoint join limit
is always **0.005 mm**.

To repair larger gaps, opt in to **Close larger gaps** and enter a maximum from
0 to 1 mm. Import the drawing, or use **Apply import options** to re-read the most
recent files with the new setting. Re-reading replaces those files' parts and
messages; it does not leave parts from an earlier import behind. The option is
off by default and resets when another project is opened.

The equivalent CLI command is:

```powershell
nestbolt import drawing.dxf --output library.json --close-gaps 0.05
```

MCP `import_parts` accepts `close_gaps_mm: 0.05`. Omit the parameter to leave
larger-gap repair off. Values over 1 mm, negative values and non-finite values
are rejected with a corrective message.

Every repaired gap over 0.005 mm is recorded with its source, endpoints and size
in millimetres. Repair inserts a straight bridge so the original neighbouring
curve endpoints remain intact. Open contours that remain unimported report their
endpoints, endpoint gap and a suggested repair tolerance when it is within the
1 mm limit. Larger gaps require editing the source drawing. Review these reports
before using the cutting geometry; a partial import is not a claim that every
source contour was included.

Libraries and CLI/MCP responses include an `imports` entry per file:

```json
{
  "file": "drawing.dxf",
  "report": {
    "silent_join_mm": 0.005,
    "close_gaps_mm": 0.05,
    "closed_gaps": [
      {
        "source": "CUT:LINE",
        "from_mm": [0, 0.05],
        "to_mm": [0, 0],
        "size_mm": 0.05
      }
    ],
    "open_contours": []
  }
}
```

The browser can expand its import messages to show every warning. Its worker
uses the same native import options and report model. The existing WebAssembly
`import_files` entry point remains available; new integrations can pass JSON
options to `import_files_with_options`.

This is the first N1 capability. Layer/colour selection, cleanup, full corpus
fidelity, 10,000-case property testing and native LightBurn export checks still
need their H2 evidence. The frozen corpus and held-out partition must not change
in response to these tests.
