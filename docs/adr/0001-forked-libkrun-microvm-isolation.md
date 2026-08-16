# MicroVM isolation via a forked, owned libkrun-family stack

Every Hecate agent runs inside a microVM — a hard, hardware-virtualized boundary with
host-policed virtio devices — rather than the OS-sandbox process isolation Sylk
attempted. We build on libkrun (KVM on Linux, Hypervisor.framework on macOS) plus the
2026 WHP lineage (A3S Box / SmolVM) for Windows, **forked and maintained in-tree**: we
own the whole stack and improve it rather than depending on young upstreams. The
boundary contract stays VMM-agnostic (Linux guest, virtio-fs workspace, vsock control,
all egress through a host user-space network stack) so any per-platform leg can be
swapped for a native VM if a backend stalls.

## Considered Options

- Native VM per platform (Firecracker/CH + Virtualization.framework + Hyper-V/HCS):
  production-proven legs, but three device dialects to police forever.
- Custom three-backend rust-vmm VMM from day one: maximum control, but months of
  hypervisor work on the critical path; retained as a phase-2 option harvesting
  OpenVMM's backend code.
- OS sandboxes (seccomp/Landlock, Seatbelt, AppContainer): rejected as the default
  boundary — kernel-attack-surface class, and cannot honor the Guardian's syscall and
  network hard-block authority. Kept only as an explicitly labeled degraded mode.

## Consequences

libkrun-as-library is what makes the single-binary product shape (ADR-0004) real. The
Windows WHP backend is the risk cell; we co-maintain it and budget for the
QEMU-WHPX-class bug terrain. macOS is Apple-Silicon-only (arm64 guests); guest images
ship dual-arch.
