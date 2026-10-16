#!/usr/bin/env python3
"""Scraper live Worlds 2026 — version SERVEUR o2switch.

Identique à scripts/scrape_live.py, avec 3 différences :
  1. Écrit live.json DANS le répertoire du script (= document root web).
  2. Corrige le bug standings (build_standings appelé avec les données brutes
     sections/rankings, pas avec stages_out aplati → classement enfin rempli).
  3. Écriture atomique (tmp + rename) pour ne jamais servir un JSON partiel.

À exécuter par cron côté o2switch :  /usr/bin/python3 /home/plch5910/esport-lol.com/live-update.py
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
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "live.json")


def get(path):
    req = urllib.request.Request(API + path, headers={"x-api-key": KEY, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_standings():
    d = get(f"/getStandings?hl=fr-FR&tournamentId={TID}")
    return d["data"]["standings"]


def fetch_schedule_times():
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
        "outcome": res.get("outcome"),
        "gameWins": res.get("gameWins", 0),
        "record": {"wins": rec.get("wins"), "losses": rec.get("losses")},
    }


def parse_standings_team(t):
    rec = t.get("record") or {}
    return {"code": t.get("code"), "name": t.get("name"),
            "wins": rec.get("wins"), "losses": rec.get("losses")}


def compute_standings_from_matches(matches):
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
    return sorted(recs.values(), key=lambda r: (-r["wins"], r["losses"]))


def build_standings(standings_raw):
    """Corrigé : itère standings_raw -> stages -> sections (rankings ou matches)."""
    standings = []
    for s in standings_raw:
        for st in s.get("stages", []):
            stage_slug = st.get("slug")
            stage_name = st.get("name") or stage_slug
            for sec in st.get("sections", []):
                rankings = sec.get("rankings") or []
                sec_name = sec.get("name") or ""
                matches = sec.get("matches", [])
                if rankings:
                    for i, rk in enumerate(rankings):
                        teams = [parse_standings_team(t) for t in (rk.get("teams") or [])]
                        teams = [t for t in teams if t["code"] not in ("TBD", "", None)]
                        group_title = f"{stage_name} — {sec_name}".strip(" —")
                        if len(rankings) > 1 and rk.get("ordinal") is not None:
                            group_title = f"{stage_name} — {sec_name} #{rk.get('ordinal') + 1}".strip(" —")
                        standings.append({
                            "stage": stage_slug, "stage_name": stage_name,
                            "title": group_title or stage_name, "teams": teams,
                        })
                else:
                    teams = compute_standings_from_matches(matches)
                    if teams:
                        standings.append({
                            "stage": stage_slug, "stage_name": stage_name,
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
                    match = {"id": m.get("id"), "state": m.get("state"),
                             "startTime": start, "teams": teams}
                    matches_out.append(match)
                    all_matches.append(match)
            stages_out.append({"slug": st.get("slug"), "name": st.get("name"),
                               "matches": matches_out})

    now = datetime.now(timezone.utc)

    upcoming = [m for m in all_matches
                if m["state"] == "unstarted" and m.get("startTime")
                and any(t["code"] not in ("TBD", "", None) for t in m["teams"])]
    upcoming.sort(key=lambda m: m["startTime"])

    next_match = None
    for m in upcoming:
        if m["startTime"] >= now.isoformat():
            next_match = m
            break

    results = [m for m in all_matches
               if m["state"] == "completed"
               and any(t["code"] not in ("TBD", "", None) for t in m["teams"])]
    results.sort(key=lambda m: m.get("startTime") or "", reverse=True)

    live = {
        "updated_at": now.isoformat(),
        "source": "lolesports",
        "tournament_id": TID,
        "next_match": next_match,
        "upcoming": upcoming,
        "results": results,
        "standings": build_standings(standings_raw),
        "stages": stages_out,
    }

    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(live, f, ensure_ascii=False)
    os.replace(tmp, OUT)

    n = len(all_matches)
    n_live = sum(1 for m in all_matches if m["state"] == "inProgress")
    n_done = sum(1 for m in all_matches if m["state"] == "completed")
    n_standings = sum(1 for t in live["standings"] if t["teams"])
    print(f"OK matchs={n} live={n_live} termines={n_done} classements={n_standings} -> {OUT}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERREUR live-update: {e}", file=sys.stderr)
        sys.exit(1)
