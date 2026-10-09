import os
from bcc import BPF
from typing import Callable, Any

class eBPFSandboxMonitor:
    """Deploys eBPF kernel hooks to monitor syscalls made by the AI REPL sandbox for WAF/Security testing."""
    
    def __init__(self):
        # Basic eBPF C program to trace execve syscalls
        self.bpf_text = """
        #include <uapi/linux/ptrace.h>
        #include <linux/sched.h>
        
        struct data_t {
            u32 pid;
            char comm[TASK_COMM_LEN];
        };
        
        BPF_PERF_OUTPUT(events);
        
        int syscall__execve(struct pt_regs *ctx) {
            struct data_t data = {};
            data.pid = bpf_get_current_pid_tgid() >> 32;
            bpf_get_current_comm(&data.comm, sizeof(data.comm));
            events.perf_submit(ctx, &data, sizeof(data));
            return 0;
        }
        """
        self.bpf: Any = None

    def attach(self):
        """Compiles and attaches the eBPF program to the kernel."""
        if os.geteuid() != 0:
            raise PermissionError("eBPF monitoring requires root privileges.")
            
        self.bpf = BPF(text=self.bpf_text)
        execve_fnname = self.bpf.get_syscall_fnname("execve")
        self.bpf.attach_kprobe(event=execve_fnname, fn_name="syscall__execve")

    def poll_events(self, callback: Callable[[Any, Any, Any], None]):
        """Opens the perf ring buffer and polls for process execution events."""
        if not self.bpf:
            return
        self.bpf["events"].open_perf_buffer(callback)
        while True:
            try:
                self.bpf.perf_buffer_poll()
            except KeyboardInterrupt:
                break
