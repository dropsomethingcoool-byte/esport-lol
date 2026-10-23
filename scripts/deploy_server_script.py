#!/usr/bin/env python3
"""Déploie le script serveur (live-update.py) + live.json vers o2switch.
FTP d'abord, SFTP (sshpass) en fallback.
"""
import os
import shlex
import subprocess
import sys
import ftplib

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
SRC_SCRIPT = os.path.join(ROOT, "scripts", "server_live_update.py")
SRC_LIVE = os.path.join(ROOT, "data", "live.json")


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


def upload_ftp(env):
    host, user, pw = env["FTP_HOST"], env["FTP_USER"], env["FTP_PASSWORD"]
    path = env.get("FTP_PATH", "public_html").strip("/")
    ftp = ftplib.FTP(host, timeout=60)
    ftp.login(user, pw)
    ftp.set_pasv(True)
    ftp.cwd(path)
    ftp.encoding = "utf-8"
    for local, remote in ((SRC_SCRIPT, "live-update.py"), (SRC_LIVE, "live.json")):
        with open(local, "rb") as f:
            ftp.storbinary(f"STOR {remote}", f)
        print(f"  FTP ✓ {remote}")
    ftp.quit()


def upload_sftp(env):
    host, user, pw = env["FTP_HOST"], env["FTP_USER"], env["FTP_PASSWORD"]
    path = env.get("FTP_PATH", "public_html").strip("/")
    batch = f"cd {shlex.quote(path)}\n"
    batch += f"put {shlex.quote(SRC_SCRIPT)} live-update.py\n"
    batch += f"put {shlex.quote(SRC_LIVE)} live.json\n"
    batch += "bye\n"
    r = subprocess.run(
        ["sshpass", "-p", pw, "sftp", "-oBatchMode=no",
         "-oStrictHostKeyChecking=accept-new", "-oConnectTimeout=20",
         f"{user}@{host}"],
        input=batch, capture_output=True, text=True, timeout=120,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stdout + r.stderr)
    print("  SFTP ✓ (fallback)")


def main():
    env = load_env()
    if not all(env.get(k) for k in ("FTP_HOST", "FTP_USER", "FTP_PASSWORD")):
        print("ERREUR: identifiants manquants (.ftp.env)")
        return 1
    try:
        upload_ftp(env)
    except Exception as e:
        print("FTP échoué:", repr(e))
        try:
            upload_sftp(env)
        except Exception as e2:
            print("SFTP échoué:", repr(e2))
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
