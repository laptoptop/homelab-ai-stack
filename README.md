# homelab-ai-stack

Self-hosted AI infrastructure I run daily — Proxmox VE, segmented networking, GPU
inference, and agent orchestration. This is the lab I use for LLM red-team research;
every technique I publish is tested here first.

## Architecture (10.10.8.0/24 server subnet, 192.168.8.0/24 LAN)

```
Internet ─ pfSense (firewall, 2-subnet routing) ──┬─ Proxmox VE host
                                                  │   ├─ LXC: Hermes agent runtime
                                                  │   ├─ LXC: AdGuard Home (DNS filtering)
                                                  │   └─ VM: ComfyUI / GPU inference
                                                  └─ LAN (desktops, mobile)
WireGuard mesh for remote access — no exposed management interfaces.
```

## Components
- **Hypervisor**: Proxmox VE, containers for services, dedicated VM for GPU work.
- **GPU inference**: RTX 4090 24GB — llama.cpp / GGUF quantized models, ComfyUI for
  generative pipelines (image/video/audio/3D), served as systemd units.
- **Agent layer**: custom agent runtime with sub-agents, MCP tool servers, and
  human-in-the-loop gates. Offensive-capable profiles are scope-gated (SOUL.md +
  workspace SCOPE.md required before any action).
- **Network security**: pfSense inter-VLAN routing, AdGuard DNS blocking, WireGuard
  only remote path, SMB allowlists limited to trusted subnets.

## Why publish this
AI security work without infrastructure experience is paper auditing. Running your
own GPU serving, agent runtimes, and network segmentation means you understand the
systems you're attacking — and the exact egress paths a prompt injection abuses.

## Contents
- `watchdog/` — DNS-level watchdog scripts
- (more coming: systemd units, ComfyUI workflow hardening, agent sandbox configs)

> Work in progress — documented publicly as part of a build-in-public series on
> LinkedIn (link in profile).
