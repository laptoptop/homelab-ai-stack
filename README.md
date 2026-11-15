# homelab-ai-stack

Self-hosted AI infrastructure I run daily — Proxmox VE, segmented networking, GPU
inference, and agent orchestration. This is the lab I use for LLM red-team research;
every technique I publish is tested here first.

## Topology

```
Internet
   │
pfSense ── isolated server subnet ── Proxmox VE host (pve)
   │                                    ├─ VM 100  LLM-Server   (RTX 4070 12GB)
   │                                    ├─ CT 101  database
   │                                    ├─ CT 102  n8n
   │                                    ├─ CT 103  webapp
   │                                    ├─ CT 104  proxy
   │                                    ├─ CT 105  cloudflared
   │                                    ├─ CT 106  langgraph     (stopped)
   │                                    ├─ CT 107  openwebui
   │                                    ├─ CT 108  wazuh-manager (stopped)
   │                                    ├─ CT 109  Hermes        (agent runtime)
   │                                    └─ CT 110  AdGuard Home
   │
   └── LAN ── workstations, mobile
            └─ physical workstation: ComfyUI server (RTX 4090)

Storages: local, local-lvm, nvme_backup. SDN zone: localnetwork.
WireGuard is the only remote path — no exposed management interfaces.
```

## Components

- **Hypervisor**: Proxmox VE on bare metal — one VM plus ten containers, snapshots
  and backups on a dedicated NVMe pool.
- **GPU inference (VM 100, LLM-Server)**: RTX 4070 12GB running llama.cpp with GGUF
  quantised models as systemd units, exposed as an OpenAI-compatible endpoint. One
  model resident at a time on a 12GB budget: Gemma4-12B Q4_K_M at 8.7GB or
  Qwen2.5-7B at 5.6GB, swapped on demand. This is the target box for the writeups in
  [`llm-agent-redteam`](https://github.com/laptoptop/llm-agent-redteam).
- **Generative GPU (physical workstation)**: RTX 4090 running ComfyUI for
  image/video/audio/3D pipelines — outside the Proxmox cluster so generation and
  inference workloads don't fight over the same card.
- **Agent layer (CT 109, Hermes)**: agent runtime with sub-agents, MCP tool servers
  and human-in-the-loop gates. Offensive-capable profiles are scope-gated
  (SOUL.md + workspace SCOPE.md required before any action).
- **Data / automation**: database container, n8n for scheduled flows, openwebui as
  the chat front end, langgraph container kept for graph-based agent experiments.
- **Network security**: pfSense routing between isolated subnets, AdGuard Home for
  DNS filtering, cloudflared for deliberate egress tunnels, WireGuard for the only
  remote path, SMB allowlists limited to trusted subnets. A Wazuh manager container
  is provisioned for log/SIEM work and currently stopped.
- **Monitoring**: `watchdog/` — cron-driven checks that print only when something is
  down, so they wire straight into a notifier.

## Why publish this

AI security work without infrastructure experience is paper auditing. Running your
own hypervisor, GPU serving, agent runtimes and network segmentation means you
understand the systems you're attacking — and the exact egress paths a prompt
injection abuses.

## Contents

- `watchdog/` — DNS/service watchdog; hosts and ports come from environment
  variables (see `watchdog/.env.example`)
- [`llm-agent-redteam`](https://github.com/laptoptop/llm-agent-redteam) — separate
  repo: DVLA SQLi writeup, cross-model exploit matrix, garak baseline + tooling
- (more coming: systemd units, ComfyUI workflow hardening, agent sandbox configs)

> Work in progress — documented publicly as part of a build-in-public series on
> LinkedIn (link in profile).
