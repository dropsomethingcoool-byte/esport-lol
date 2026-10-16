#!/usr/bin/env python3
"""Déploie uniquement data/live.json vers le serveur (mise à jour live sans rebuild).
Usage : python3 scripts/deploy_live.py
"""
import ftplib
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "data", "live.json")


def _load_ftp_env():
    p = os.path.join(ROOT, ".ftp.env")
    d = {}
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    d[k.strip()] = v.strip()
    return d


def main():
    if not os.path.exists(LIVE):
        print("ERREUR : data/live.json introuvable. Lancer scrape_live.py d'abord.")
        return 1
    env = dict(os.environ)
    env.update(_load_ftp_env())
    host = env.get("FTP_HOST")
    user = env.get("FTP_USER")
    pw = env.get("FTP_PASSWORD")
    path = (env.get("FTP_PATH") or "public_html").strip("/")
    if not (host and user and pw):
        print("ERREUR : identifiants FTP manquants.")
        return 1

    ftp = ftplib.FTP(host, timeout=60)
    ftp.login(user, pw)
    ftp.encoding = "utf-8"
    try:
        ftp.cwd(path)
    except Exception:
        ftp.mkd(path)
        ftp.cwd(path)
    with open(LIVE, "rb") as f:
        ftp.storbinary("STOR live.json", f)
    ftp.quit()
    print("live.json déployé ✓")


if __name__ == "__main__":
    raise SystemExit(main())
