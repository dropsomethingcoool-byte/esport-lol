#!/usr/bin/env python3
"""Déploie site/ vers o2switch via SFTP (sshpass) — fallback quand le FTP échoue
(VPN actif : ports hauts FTP en timeout). Ignore live.json (géré par le CRON serveur)."""
import os
import shlex
import subprocess

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
SITE = os.path.join(ROOT, "site")


def load_env():
    d = dict(os.environ)
    p = os.path.join(ROOT, ".ftp.env")
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                d[k.strip()] = v.strip()
    return d


def main():
    env = load_env()
    host, user, pw = env["FTP_HOST"], env["FTP_USER"], env["FTP_PASSWORD"]
    path = env.get("FTP_PATH", "public_html").strip("/")

    dirs = set()
    files = []
    for dirpath, dirnames, filenames in os.walk(SITE):
        rel = os.path.relpath(dirpath, SITE)
        if rel == ".":
            rel = ""
        for d in dirnames:
            dirs.add(os.path.join(rel, d).replace(os.sep, "/") if rel else d)
        for fn in filenames:
            if fn == "live.json":
                continue
            rp = (os.path.join(rel, fn) if rel else fn).replace(os.sep, "/")
            files.append((os.path.join(dirpath, fn), rp))

    lines = [f"cd {shlex.quote(path)}"]
    # créer les dossiers (dans l'ordre des plus profonds d'abord)
    for d in sorted(dirs, key=lambda x: x.count("/")):
        lines.append(f"-mkdir {shlex.quote(d)}")
    for lp, rp in files:
        lines.append(f"put {shlex.quote(lp)} {shlex.quote(rp)}")
    lines.append("bye")
    batch = "\n".join(lines) + "\n"

    r = subprocess.run(
        ["sshpass", "-p", pw, "sftp", "-oBatchMode=no",
         "-oStrictHostKeyChecking=accept-new", "-oConnectTimeout=20",
         f"{user}@{host}"],
        input=batch, capture_output=True, text=True, timeout=600,
    )
    err = (r.stdout + r.stderr).strip()
    # sftp batch : les erreurs "already exists" sur mkdir sont ignorées par -mkdir
    print(f"exit={r.returncode}")
    print(err[-2000:] if err else "(vide)")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
