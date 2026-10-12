"""Between benchmark sessions (plan section 5.4): the readable heat signals on
this PC, appended to output/heat-log.jsonl. Windows exposes only an ACPI thermal
zone (kelvin, coarse); the current CPU clock is a second signal, since thermal
throttling lowers it. Prints one JSON line.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

import psutil

ROOT = Path(__file__).resolve().parents[1]


def zones():
    command = ('Get-CimInstance -ClassName Win32_PerfFormattedData_Counters_ThermalZoneInformation '
               '| Select-Object Name,HighPrecisionTemperature | ConvertTo-Json')
    try:
        out = subprocess.run(['powershell.exe', '-NoProfile', '-Command', command], capture_output=True,
                             text=True, timeout=30).stdout
        rows = json.loads(out) if out.strip() else []
        rows = rows if isinstance(rows, list) else [rows]
        return {r['Name']: round(r['HighPrecisionTemperature'] / 10 - 273.15, 1) for r in rows}
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return {}


def main():
    freq = psutil.cpu_freq()
    record = {'at': datetime.now(timezone.utc).isoformat(), 'acpi_celsius': zones(),
              'cpu_mhz': round(freq.current) if freq else None, 'cpu_max_mhz': round(freq.max) if freq else None,
              'cpu_percent': psutil.cpu_percent(interval=1.0)}
    log = ROOT/'output/heat-log.jsonl'
    log.parent.mkdir(exist_ok=True)
    with log.open('a', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(record) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
