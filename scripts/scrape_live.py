#!/usr/bin/env python3
"""
Scraper live — Worlds 2026 (League of Legends).
Sources : API lolesports (getStandings = bracket + résultats + classement,
getSchedule = heures de match).

Produit : data/live.json  (rechargé par le front toutes les 60s)
  - stages[]   : bracket complet (matchs + résultats + scores)
  - next_match : prochain match (compte à rebours)
  - upcoming[] : matchs à venir (triés par heure)
  - results[]  : matchs terminés (résultats)
  - standings[]: classement par phase/groupe (wins/losses)

Aucune donnée inventée : si une info manque, le champ reste null.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://esports-api.lolesports.com/persisted/gw"
KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
TID = "115660540725177488"          # Worlds 2026
LEAGUE = "98767975604431411"        # LoL esports (toutes saisons)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "live.json")


def get(path):
    req = urllib.request.Request(API + path, headers={"x-api-key": KEY, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_standings():
    d = get(f"/getStandings?hl=fr-FR&tournamentId={TID}")
    return d["data"]["standings"]


def fetch_schedule_times():
    """Retourne {(code1, code2): startTime_utc} depuis getSchedule (best-effort)."""
    times = {}
    pages = [None, "bmV3ZXI6OjExNTY2MDU0MDcyNjA5NTA5Nw=="]
    queries = []
    for p in pages:
        q = f"/getSchedule?hl=fr-FR&leagueId={LEAGUE}"
        if p:
            q += "&pageToken=" + urllib.parse.quote(p)
        queries.append(q)
    queries.append(f"/getSchedule?hl=fr-FR&tournamentId={TID}")

    seen = set()
    for q in queries:
        try:
            d = get(q)
        except Exception:
            continue
        for e in d.get("data", {}).get("schedule", {}).get("events", []):
            m = e.get("match") or {}
            teams = m.get("teams") or []
            codes = sorted(t.get("code", "") for t in teams if t.get("code") not in ("TBD", "", None))
            if len(codes) == 2 and tuple(codes) not in seen:
                seen.add(tuple(codes))
                times[tuple(codes)] = e.get("startTime")
    return times


def parse_team(t):
    res = t.get("result") or {}
    rec = t.get("record") or {}
    return {
        "name": t.get("name"),
        "code": t.get("code"),
        "slug": t.get("slug"),
        "image": t.get("image"),
        "outcome": res.get("outcome"),       # win / loss / null
        "gameWins": res.get("gameWins", 0),
        "record": {                           # bilan série (wins/losses) si fourni par l'API
            "wins": rec.get("wins"),
            "losses": rec.get("losses"),
        },
    }


def parse_standings_team(t):
    """Équipe d'une table de classement (rankings)."""
    rec = t.get("record") or {}
    return {
        "code": t.get("code"),
        "name": t.get("name"),
        "wins": rec.get("wins"),
        "losses": rec.get("losses"),
    }


def compute_standings_from_matches(matches):
    """Fallback : calcule le bilan W/L d'une phase depuis les matchs terminés."""
    recs = {}
    for m in matches:
        if m.get("state") != "completed":
            continue
        for t in m.get("teams", []):
            code = t.get("code")
            if code in ("TBD", "", None):
                continue
            r = recs.setdefault(code, {"code": code, "name": t.get("name"), "wins": 0, "losses": 0})
            if t.get("outcome") == "win":
                r["wins"] += 1
            elif t.get("outcome") == "loss":
                r["losses"] += 1
    # tri : le plus de victoires d'abord, puis le moins de défaites
    return sorted(recs.values(), key=lambda r: (-r["wins"], r["losses"]))


def build_standings(stages):
    """Construit le classement (standings) par phase/groupe.

    1. Priorité aux tables `rankings` fournies par l'API (classement officiel).
    2. Sinon, calcule le bilan W/L depuis les matchs terminés de la phase.
    """
    standings = []
    for st in stages:
        stage_slug = st.get("slug")
        stage_name = st.get("name") or stage_slug
        for sec in st.get("sections", []):
            rankings = sec.get("rankings") or []
            sec_name = sec.get("name") or ""
            matches = sec.get("matches", [])

            if rankings:
                # Plusieurs groupes possibles (play-in : Groupe A / B) -> ordinal
                for i, rk in enumerate(rankings):
                    teams = [parse_standings_team(t) for t in (rk.get("teams") or [])]
                    teams = [t for t in teams if t["code"] not in ("TBD", "", None)]
                    group_title = f"{stage_name} — {sec_name}".strip(" —")
                    if len(rankings) > 1 and rk.get("ordinal") is not None:
                        group_title = f"{stage_name} — {sec_name} #{rk.get('ordinal') + 1}".strip(" —")
                    standings.append({
                        "stage": stage_slug,
                        "stage_name": stage_name,
                        "title": group_title or stage_name,
                        "teams": teams,
                    })
            else:
                teams = compute_standings_from_matches(matches)
                if teams:
                    standings.append({
                        "stage": stage_slug,
                        "stage_name": stage_name,
                        "title": f"{stage_name} — {sec_name}".strip(" —") or stage_name,
                        "teams": teams,
                    })
    return standings


def main():
    standings_raw = fetch_standings()
    times = fetch_schedule_times()

    stages_out = []
    all_matches = []
    for s in standings_raw:
        for st in s.get("stages", []):
            matches_out = []
            for sec in st.get("sections", []):
                for m in sec.get("matches", []):
                    teams = [parse_team(t) for t in m.get("teams", [])]
                    codes = sorted(t["code"] for t in teams if t["code"] not in ("TBD", "", None))
                    start = times.get(tuple(codes)) if len(codes) == 2 else None
                    match = {
                        "id": m.get("id"),
                        "state": m.get("state"),       # unstarted / inProgress / completed
                        "startTime": start,            # UTC ISO ou null
                        "teams": teams,
                    }
                    matches_out.append(match)
                    all_matches.append(match)
            stages_out.append({
                "slug": st.get("slug"),
                "name": st.get("name"),
                "matches": matches_out,
            })

    now = datetime.now(timezone.utc)

    # Matchs à venir (réels, avec heure)
    upcoming = [m for m in all_matches
                if m["state"] == "unstarted"
                and m.get("startTime")
                and any(t["code"] not in ("TBD", "", None) for t in m["teams"])]
    upcoming.sort(key=lambda m: m["startTime"])

    # Prochain match = le premier à venir après maintenant
    next_match = None
    for m in upcoming:
        if m["startTime"] >= now.isoformat():
            next_match = m
            break

    # Résultats (matchs terminés, réels)
    results = [m for m in all_matches
               if m["state"] == "completed"
               and any(t["code"] not in ("TBD", "", None) for t in m["teams"])]
    # plus récents d'abord (par heure si dispo, sinon ordre d'apparition inversé)
    results.sort(key=lambda m: m.get("startTime") or "", reverse=True)

    live = {
        "updated_at": now.isoformat(),
        "source": "lolesports",
        "tournament_id": TID,
        "next_match": next_match,
        "upcoming": upcoming,
        "results": results,
        "standings": build_standings([st for s in standings_raw for st in s.get("stages", [])]),
        "stages": stages_out,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(live, f, ensure_ascii=False)

    # Résumé console
    n = len(all_matches)
    n_live = sum(1 for m in all_matches if m["state"] == "inProgress")
    n_done = sum(1 for m in all_matches if m["state"] == "completed")
    n_timed = sum(1 for m in all_matches if m.get("startTime"))
    n_standings = sum(1 for t in live["standings"] if t["teams"])
    print(f"live.json OK : {n} matchs | live={n_live} terminés={n_done} | avec heure={n_timed} | classements={n_standings}")
    if next_match:
        codes = " vs ".join(t["code"] for t in next_match["teams"])
        print(f"prochain match : {codes} @ {next_match['startTime']}")
    else:
        print("prochain match : inconnu (aucune heure dispo)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERREUR scrape_live : {e}", file=sys.stderr)
        sys.exit(1)
