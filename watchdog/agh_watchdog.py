#!/usr/bin/env python3
"""Watchdog for AdGuard Home (DNS + web UI) and the pfSense GUI.

Hosts and ports come from the environment so no infrastructure addresses live in
the repo:

    AGH_HOST          AdGuard Home address            (required)
    AGH_DNS_PORT      DNS port                       (default 53)
    AGH_WEB_PORT      web UI port                    (default 80)
    PFSENSE_HOST      pfSense GUI address            (required)
    PFSENSE_WEB_PORT  GUI port                       (default 443)

Prints a message only when something is DOWN (empty stdout = all good), so it can
be wired straight into cron or a notifier.
"""
import datetime
import os
import socket
import sys
import urllib.error
import urllib.request

def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.exit(f"missing required environment variable: {name}")
    return value


AGH_HOST = _required("AGH_HOST")
AGH_DNS_PORT = int(os.getenv("AGH_DNS_PORT", "53"))
AGH_WEB_PORT = int(os.getenv("AGH_WEB_PORT", "80"))
PFSENSE_HOST = _required("PFSENSE_HOST")
PFSENSE_WEB_PORT = int(os.getenv("PFSENSE_WEB_PORT", "443"))


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except Exception:
        return False


msgs = []

if not port_open(AGH_HOST, AGH_DNS_PORT):
    msgs.append(f"AdGuard Home {AGH_HOST}:{AGH_DNS_PORT} (DNS) not responding!")

# Any HTTP response (200/302/401...) means the web UI is alive; only transport
# failures count as down.
try:
    urllib.request.urlopen(f"http://{AGH_HOST}:{AGH_WEB_PORT}/control/health", timeout=5)
except urllib.error.HTTPError:
    pass
except Exception as e:  # noqa: BLE001
    msgs.append(f"AdGuard web UI (port {AGH_WEB_PORT}) unreachable: {e}")

if not port_open(PFSENSE_HOST, PFSENSE_WEB_PORT):
    msgs.append(f"pfSense {PFSENSE_HOST}:{PFSENSE_WEB_PORT} (GUI) not responding!")

if msgs:
    print(f"[{datetime.datetime.now().isoformat()}] ALERT:\n" + "\n".join(msgs))
