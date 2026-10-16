#!/usr/bin/env python3
"""Déploie le dossier site/ vers un hébergement cPanel (O2 Switch) via FTP.

Identifiants lus depuis les variables d'environnement (sinon demandés) :
  FTP_HOST, FTP_USER, FTP_PASSWORD, FTP_PATH (racine web, défaut: public_html)

Usage :
  FTP_HOST=ftp.ariege-malin.fr FTP_USER=... FTP_PASSWORD=... python3 scripts/deploy.py
"""
import os
import ftplib
import getpass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")


def _load_ftp_env():
    """Charge .ftp.env (KEY=VALUE) du projet, si présent."""
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


def load_creds():
    env = dict(os.environ)
    env.update(_load_ftp_env())  # .ftp.env sert de fallback
    host = env.get("FTP_HOST") or input("Hôte FTP : ")
    user = env.get("FTP_USER") or input("Utilisateur FTP : ")
    pw = env.get("FTP_PASSWORD") or getpass.getpass("Mot de passe FTP : ")
    path = (env.get("FTP_PATH") or "public_html").strip("/")
    return host, user, pw, path


def upload(ftp, local_dir, remote_dir):
    for name in sorted(os.listdir(local_dir)):
        if name == "live.json":
            continue  # géré par le cron serveur (live-update.py) — ne jamais écraser
        lp = os.path.join(local_dir, name)
        rp = f"{remote_dir}/{name}".lstrip("/")
        if os.path.isdir(lp):
            try:
                ftp.mkd(rp)
            except Exception:
                pass
            upload(ftp, lp, rp)
        else:
            with open(lp, "rb") as f:
                ftp.storbinary(f"STOR {rp}", f)
            print(f"  ✓ {rp}")


def main():
    host, user, pw, path = load_creds()
    print(f"Connexion FTP à {host} (utilisateur {user}) ...")
    ftp = ftplib.FTP(host, timeout=60)
    ftp.login(user, pw)
    ftp.set_pasv(True)
    ftp.encoding = "utf-8"
    try:
        ftp.cwd(path)
    except Exception:
        ftp.mkd(path)
        ftp.cwd(path)
    print(f"Déploiement de site/ vers /{path}/ ...")
    upload(ftp, SITE, ".")
    ftp.quit()
    print("Déploiement terminé.")


if __name__ == "__main__":
    main()
