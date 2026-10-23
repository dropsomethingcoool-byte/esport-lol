#!/usr/bin/env python3
"""Réseau : HTTPS 443 vs FTP 21 (canal de contrôle) vs SSH 22 — diagnostic VPN."""
import socket
import time

TARGETS = [("esport-lol.com", 443), ("ftp.ariege-malin.fr", 21), ("ftp.ariege-malin.fr", 22)]

for host, port in TARGETS:
    t0 = time.time()
    try:
        s = socket.create_connection((host, port), timeout=8)
        banner = b""
        try:
            s.settimeout(4)
            banner = s.recv(200)
        except Exception:
            pass
        s.close()
        print(f"{host}:{port} OUVERT ({(time.time()-t0)*1000:.0f} ms) {banner[:60]!r}")
    except Exception as e:
        print(f"{host}:{port} FERMETURE/TIMEOUT ({(time.time()-t0)*1000:.0f} ms) {e}")
