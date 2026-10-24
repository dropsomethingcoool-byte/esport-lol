#!/usr/bin/env python3
"""Récupère les portraits lolesports des 16 joueurs ciblés → data/player_photos.json."""
import json
import time
import urllib.request

API = "https://esports-api.lolesports.com/persisted/gw"
KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"


def get(path):
    req = urllib.request.Request(API + path, headers={"x-api-key": KEY, "Accept": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read().decode())


# 1) team ids
d = get("/getStandings?hl=fr-FR&tournamentId=115660540725177488")
teams = {}
for s in d["data"]["standings"]:
    for st in s.get("stages", []):
        for sec in st.get("sections", []):
            for rk in (sec.get("rankings") or []):
                for t in rk.get("teams", []):
                    if t.get("code") not in (None, "TBD", ""):
                        teams[t["code"]] = {"id": t.get("id"), "name": t.get("name")}
            for m in sec.get("matches", []):
                for t in m.get("teams", []):
                    if t.get("code") not in (None, "TBD", ""):
                        teams.setdefault(t["code"], {"id": t.get("id"), "name": t.get("name")})

print("team ids:", json.dumps({c: v["id"] for c, v in teams.items()}, ensure_ascii=False))

# 2) rosters des 10 équipes utiles
WANT = ["T1", "KC", "G2", "GEN", "HLE", "DK", "IG", "TES", "BLG", "TLAW", "TL"]
players = {}
for code, info in teams.items():
    if code not in WANT:
        continue
    tid = info.get("id")
    if not tid:
        continue
    try:
        r = get(f"/getTeams?hl=fr-FR&id={tid}")
        for t in r["data"]["teams"]:
            for p in t.get("players", []):
                sn = p.get("summonerName", "")
                players[sn.lower()] = {
                    "summonerName": sn,
                    "photo": p.get("image"),
                    "role": p.get("role"),
                    "code": code,
                    "team": info.get("name"),
                }
        print(f"  ✓ {code} ({len(players)} joueurs cumulés)")
    except Exception as e:
        print(f"  ✗ {code}: {e}")
    time.sleep(0.2)

# 3) mapping cible
TARGETS = {
    "faker": "T1", "caliste": "KC", "hans sama": "G2", "chovy": "GEN",
    "ruler": "GEN", "zeus": "HLE", "gumayusi": "HLE", "showmaker": "DK",
    "theshy": "IG", "jackeylove": "TES", "perkz": "G2", "knight": "BLG",
    "viper": "BLG", "bin": "BLG", "corejj": "TL", "brokenblade": "G2",
}

out = {}
print("\n=== correspondances ===")
for target, want_code in TARGETS.items():
    hit = None
    for k, v in players.items():
        if k.replace(" ", "") == target.replace(" ", ""):
            hit = v
            break
    if not hit:
        for k, v in players.items():
            a = target.replace(" ", "")
            b = k.replace(" ", "")
            if a in b or b in a:
                hit = v
                break
    if hit:
        out[target] = hit
        print(f"  {target:14s} -> {hit['summonerName']:14s} {hit['code']:5s} {hit['photo']}")
    else:
        print(f"  {target:14s} -> INTROUVABLE")

with open(ROOT + "/data/player_photos.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\n✓ data/player_photos.json écrit")
