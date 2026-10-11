param([Parameter(Mandatory = $true)][int]$ControllerId)
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
    public static void Apply(int pid) {
        IntPtr job = CreateJobObject(IntPtr.Zero, null);
        if (job == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
        IntPtr process = IntPtr.Zero;
        try {
            Limits limits = new Limits { Flags = 0x10, Affinity = new UIntPtr(1) };
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
[NestboltCpuJob]::Apply($ControllerId)
(Get-Process -Id $ControllerId).ProcessorAffinity.ToInt64()
