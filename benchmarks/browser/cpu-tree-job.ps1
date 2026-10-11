param([Parameter(Mandatory = $true)][int]$ControllerId, [UInt64]$Mask = 4)
if ($Mask -eq 0 -or ($Mask -band ($Mask - 1)) -ne 0) { throw 'Mask must select exactly one logical CPU' }
$ErrorActionPreference = 'Stop'
# A job-wide affinity remains enforced for future browser children, including
# processes that try to reset their own mask. It ends when this process tree ends.
# No breakaway or kill-on-close flags: unrelated processes are never assigned.
Add-Type -TypeDefinition @'
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
public static class NestboltCpuJob {
    [StructLayout(LayoutKind.Sequential)]
    public struct Limits {
        public long ProcessTime, JobTime;
        public uint Flags;
        public UIntPtr MinWorkingSet, MaxWorkingSet;
        public uint ActiveProcesses;
        public UIntPtr Affinity;
        public uint Priority, Scheduling;
    }
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern IntPtr CreateJobObject(IntPtr attributes, string name);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool SetInformationJobObject(IntPtr job, int info, ref Limits limits, uint size);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern IntPtr OpenProcess(uint access, bool inherit, int pid);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);
    [DllImport("kernel32.dll", SetLastError=true)]
    static extern bool CloseHandle(IntPtr handle);
    public static void Apply(int pid, ulong mask) {
        IntPtr job = CreateJobObject(IntPtr.Zero, null);
        if (job == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
        IntPtr process = IntPtr.Zero;
        try {
            Limits limits = new Limits { Flags = 0x10, Affinity = new UIntPtr(mask) };
            if (!SetInformationJobObject(job, 2, ref limits, (uint)Marshal.SizeOf(typeof(Limits))))
                throw new Win32Exception(Marshal.GetLastWin32Error());
            process = OpenProcess(0x101, false, pid); // SET_QUOTA | TERMINATE, as required for assignment.
            if (process == IntPtr.Zero || !AssignProcessToJobObject(job, process))
                throw new Win32Exception(Marshal.GetLastWin32Error());
        } finally {
            if (process != IntPtr.Zero) CloseHandle(process);
            CloseHandle(job); // Windows retains the job until its associated processes exit.
        }
    }
}
'@
# Apply after Electron's windows and native modules are loaded. This snapshot is
# limited to the supplied controller and its descendants; no other app is added.
if ((Get-Process -Id $ControllerId).ProcessName -ne 'node') { throw 'Expected the owned Node controller' }
$nestRows = @(Get-CimInstance Win32_Process | Select-Object ProcessId, ParentProcessId)
$nestIds = [System.Collections.Generic.List[int]]::new()
$nestIds.Add($ControllerId)
do {
    $nestAdded = $false
    foreach ($nestRow in $nestRows) {
        if ($nestIds.Contains([int]$nestRow.ParentProcessId) -and -not $nestIds.Contains([int]$nestRow.ProcessId)) {
            $nestIds.Add([int]$nestRow.ProcessId)
            $nestAdded = $true
        }
    }
} while ($nestAdded)
# Parent-before-child assignment makes subsequently spawned processes inherit the
# same job. Children that already exist are explicitly assigned too.
# Chromium descendants may already belong to sandbox jobs. Separate nested
# affinity jobs avoid trying to reparent those jobs into one shared hierarchy.
foreach ($nestId in $nestIds) { [NestboltCpuJob]::Apply($nestId, $Mask) }
(Get-Process -Id $ControllerId).ProcessorAffinity.ToInt64()
