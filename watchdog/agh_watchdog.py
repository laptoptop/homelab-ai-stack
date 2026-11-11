#!/usr/bin/env python3
"""Watchdog: AdGuard Home (10.10.8.12, DNS :53, web UI :80) + pfSense (10.10.8.1:443).
Chi in ra thong bao khi co dich vu DOWN (empty stdout = im lang, khong gui gi).
"""
import datetime
import socket
import urllib.error
import urllib.request

AGH_HOST = "10.10.8.12"
AGH_WEB_PORT = 80
PFSENSE_HOST = "10.10.8.1"


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except Exception:
        return False


msgs = []

if not port_open(AGH_HOST, 53):
    msgs.append(f"AdGuard Home {AGH_HOST}:53 (DNS) KHONG tra loi!")

try:
    urllib.request.urlopen(f"http://{AGH_HOST}:{AGH_WEB_PORT}/control/health", timeout=5)
except urllib.error.HTTPError:
    pass  # server co tra loi (200/302/401...) = con song
except Exception as e:
    msgs.append(f"AGH web UI (port {AGH_WEB_PORT}) khong truy cap duoc: {e}")

if not port_open(PFSENSE_HOST, 443):
    msgs.append(f"pfSense {PFSENSE_HOST}:443 (GUI) KHONG tra loi!")

if msgs:
    print(f"[{datetime.datetime.now().isoformat()}] ⚠️ PHAT HIEN SU CO:\n" + "\n".join(msgs))