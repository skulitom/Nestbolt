"""Run a command with CPU affinity on the second CCD (logical CPUs 16-31)."""
import subprocess, sys, psutil
p = subprocess.Popen(sys.argv[1:])
try:
    psutil.Process(p.pid).cpu_affinity(list(range(16, 32)))
except Exception:
    pass
sys.exit(p.wait())
