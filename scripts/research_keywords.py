#!/usr/bin/env python3
"""Recherche de mots-clés via l'API DataForSEO.

Lit DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD depuis l'environnement (ou le .env du profil).
Usage : python3 scripts/research_keywords.py "<seed1>,<seed2>,..." [--limit 20]
Affiche les mots-clés suggérés avec volume de recherche (France, langue fr).
"""
import base64
import json
import os
import sys
import urllib.request

LOCATION_CODE = 2250  # France
LANGUAGE_CODE = "fr"

def load_env():
    env = dict(os.environ)
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".dataforseo.env")
    # fallback : profil .env (via HERMES_HOME)
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env.setdefault(k, v)
    return env

def main():
    if len(sys.argv) < 2:
        print("Usage: research_keywords.py \"seed1,seed2\" [--limit N]")
        sys.exit(1)
    seeds = [s.strip() for s in sys.argv[1].split(",") if s.strip()]
    limit = 20
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    env = load_env()
    login = env.get("DATAFORSEO_LOGIN")
    password = env.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        print("ERREUR: DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD non définis")
        sys.exit(2)

    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    payload = [{
        "keywords": seeds,
        "location_code": LOCATION_CODE,
        "language_code": LANGUAGE_CODE,
        "limit": limit,
        "include_serp_info": False,
    }]
    req = urllib.request.Request(
        "https://api.dataforseo.com/v3/keywords_data/google/keywords_for_keywords/live",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"ERREUR HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:300]}")
        sys.exit(3)
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit(4)

    tasks = data.get("tasks", [])
    if not tasks:
        print("Aucun résultat DataForSEO.")
        return
    results = tasks[0].get("result", [])
    for r in results:
        # L'API renvoie soit une liste plate de mots-clés, soit un regroupement par seed.
        if "keywords" in r:
            print(f"# seed: {r.get('seed_keyword')}")
            for kw in r.get("keywords", []):
                print(f"  {kw.get('keyword')} | volume={kw.get('search_volume')} | cpc={kw.get('cpc')}")
        elif "keyword" in r:
            print(f"  {r.get('keyword')} | volume={r.get('search_volume')} | cpc={r.get('cpc')}")

if __name__ == "__main__":
    main()
