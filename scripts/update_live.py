#!/usr/bin/env python3
"""Met à jour live.json (scrape lolesports) puis le déploie sur o2switch.

Déploiement : FTP d'abord (fonctionne quand le VPN est coupé), SFTP en
fallback (fonctionne quand le VPN est actif — SSH 22 reste ouvert).

Sortie volontairement VIDE en cas de succès (cron silencieux) et message
d'erreur + code de sortie != 0 en cas d'échec (alerte remontée à l'utilisateur).
"""
import os
import shlex
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(ROOT, "data", "live.json")


def load_env():
    d = dict(os.environ)
    p = os.path.join(ROOT, ".ftp.env")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    d[k.strip()] = v.strip()
    return d


def deploy_ftp(env):
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "deploy_live.py")],
        env=env, capture_output=True, text=True, timeout=120,
    )
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def deploy_sftp(env):
    host = env["FTP_HOST"]           # même serveur o2switch
    user = env["FTP_USER"]
    pw = env["FTP_PASSWORD"]
    path = (env.get("FTP_PATH") or "public_html").strip("/")
    batch = f"cd {shlex.quote(path)}\nput {shlex.quote(LIVE)} live.json\nbye\n"
    r = subprocess.run(
        ["sshpass", "-p", pw, "sftp",
         "-oBatchMode=no",
         "-oStrictHostKeyChecking=accept-new",
         "-oConnectTimeout=20",
         f"{user}@{host}"],
        input=batch, capture_output=True, text=True, timeout=120,
    )
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def main():
    env = load_env()
    if not all(env.get(k) for k in ("FTP_HOST", "FTP_USER", "FTP_PASSWORD")):
        print("ERREUR update_live : identifiants FTP/SFTP manquants (.ftp.env)")
        return 1

    # 1. Scrape
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "scrape_live.py")],
        env=env, capture_output=True, text=True, timeout=180,
    )
    if r.returncode != 0:
        print("ERREUR update_live (scrape) :", (r.stderr or r.stdout).strip())
        return 1

    # 2. Déploiement : FTP puis SFTP en fallback
    ok, msg = deploy_ftp(env)
    if ok:
        return 0  # silencieux
    ok, msg2 = deploy_sftp(env)
    if ok:
        return 0  # silencieux
    print(f"ERREUR update_live (deploy) : FTP échoué ({msg}) ; SFTP échoué ({msg2})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
