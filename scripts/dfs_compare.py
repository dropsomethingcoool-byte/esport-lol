#!/usr/bin/env python3
"""Comparaison de mots-clés Worlds par langue via DataForSEO : FR vs EN vs PT-BR vs ES-LatAm."""
import base64
import json
import os
import sys
import urllib.request
import urllib.error

ENDPOINT = "https://api.dataforseo.com/v3/keywords_data/google/keywords_for_keywords/live"

# (label, location_code, language_code, seeds)
MARKETS = [
    ("FR  (France)",  2250, "fr", ["mondial lol", "worlds lol", "planning worlds lol", "classement worlds lol", "resultats worlds lol"]),
    ("EN  (US)",      2840, "en", ["lol worlds schedule", "lol worlds standings", "league of legends worlds", "worlds schedule lol"]),
    ("PT-BR (Brasil)", 2076, "pt", ["mundial lol", "mundial de lol", "mundial lol 2026", "calendario mundial lol", "cblol"]),
    ("ES  (Mexique)", 2484, "es", ["mundial lol", "mundial de lol", "mundial lol 2026", "calendario mundial lol", "clasificacion mundial lol"]),
]

def load_creds():
    env = dict(os.environ)
    candidates = [
        "/Users/charlesploteau/.hermes/profiles/esport-lol/.env",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".dataforseo.env"),
    ]
    for p in candidates:
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env.setdefault(k, v)
    return env.get("DATAFORSEO_LOGIN"), env.get("DATAFORSEO_PASSWORD")

def query(login, password, seeds, loc, lang, limit=20):
    auth = base64.b64encode(f"{login}:{password}".encode()).decode()
    payload = [{"keywords": seeds, "location_code": loc, "language_code": lang,
                "limit": limit, "include_serp_info": False}]
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    login, password = load_creds()
    if not login or not password:
        print("ERREUR: DATAFORSEO_LOGIN/PASSWORD introuvables")
        sys.exit(2)

    for label, loc, lang, seeds in MARKETS:
        try:
            data = query(login, password, seeds, loc, lang)
        except urllib.error.HTTPError as e:
            print(f"\n{label}: ERREUR HTTP {e.code} — {e.read().decode('utf-8','ignore')[:200]}")
            continue
        except Exception as e:
            print(f"\n{label}: ERREUR {e}")
            continue

        tasks = data.get("tasks", [])
        kws = []
        if tasks:
            for r in tasks[0].get("result", []):
                if "keyword" in r:
                    kws.append(r)
                elif "keywords" in r:
                    kws.extend(r.get("keywords", []))
        # dédoublonner
        seen, uniq = set(), []
        for kw in kws:
            k = kw.get("keyword")
            if k and k not in seen:
                seen.add(k)
                uniq.append(kw)
        uniq.sort(key=lambda x: (x.get("search_volume") or 0), reverse=True)
        top = uniq[:15]
        total_vol = sum(x.get("search_volume") or 0 for x in top)
        comps = [x.get("competition") for x in top if x.get("competition") is not None]
        avg_comp = sum(comps) / len(comps) if comps else 0

        print(f"\n{'='*60}\n{label}  (top {len(top)} mots-clés)\n{'='*60}")
        print(f"Volume total (top): {total_vol}   |   competition moyenne: {avg_comp:.2f}")
        for x in top:
            vol = x.get("search_volume")
            comp = x.get("competition")
            print(f"  {x.get('keyword'):45s} vol={str(vol):>6s}  comp={comp if comp is not None else 'n/a'}")

if __name__ == "__main__":
    main()
