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

# Terminologie : l'API lolesports (hl=fr-FR) renvoie des noms de phase français.
STAGE_NAMES = {"Système suisse": "Swiss stage", "Play-ins": "Play-in"}


def tr_stage(name):
    return STAGE_NAMES.get(name, name)

# Ordre d'affichage du classement : swiss d'abord (phase en cours), puis play-in, knockouts.
STAGE_ORDER = {"swiss": 0, "play_ins": 1, "knockouts": 2}


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
            # l'outcome est niché sous 'result' dans les matchs bruts de l'API
            outcome = (t.get("result") or {}).get("outcome")
            if outcome == "win":
                r["wins"] += 1
            elif outcome == "loss":
                r["losses"] += 1
    return sorted(recs.values(), key=lambda r: (-r["wins"], r["losses"]))


def build_standings(standings_raw):
    """Corrigé : itère standings_raw -> stages -> sections (rankings ou matches)."""
    standings = []
    for s in standings_raw:
        for st in s.get("stages", []):
            stage_slug = st.get("slug")
            stage_name = tr_stage(st.get("name") or stage_slug)
            for sec in st.get("sections", []):
                rankings = sec.get("rankings") or []
                sec_name = tr_stage(sec.get("name") or "")
                matches = sec.get("matches", [])
                if rankings:
                    for i, rk in enumerate(rankings):
                        teams = [parse_standings_team(t) for t in (rk.get("teams") or [])]
                        teams = [t for t in teams if t["code"] not in ("TBD", "", None)]
                        group_title = stage_name if sec_name == stage_name else f"{stage_name} — {sec_name}".strip(" —")
                        if len(rankings) > 1 and rk.get("ordinal") is not None:
                            group_title = f"{stage_name} — {sec_name} #{rk.get('ordinal') + 1}".strip(" —")
                        standings.append({
                            "stage": stage_slug, "stage_name": stage_name,
                            "title": group_title or stage_name, "teams": teams,
                        })
                else:
                    teams = compute_standings_from_matches(matches)
                    if teams:
                        title = stage_name if sec_name == stage_name else f"{stage_name} — {sec_name}".strip(" —")
                        standings.append({
                            "stage": stage_slug, "stage_name": stage_name,
                            "title": title or stage_name,
                            "teams": teams,
                        })
    standings.sort(key=lambda e: STAGE_ORDER.get(e.get("stage"), 9))
    return standings


def annotate_elimination(standings, stages_out):
    """Marque 'eliminated: True' les équipes d'une phase terminée qui
    n'apparaissent dans aucune phase ultérieure (donc éliminées du tournoi)."""
    slugs = [st["slug"] for st in stages_out]
    by_slug = {st["slug"]: st.get("matches", []) for st in stages_out}
    for entry in standings:
        slug = entry.get("stage")
        if slug not in slugs:
            continue
        idx = slugs.index(slug)
        stage_matches = by_slug.get(slug, [])
        # phase terminée ? (tous les matchs completed)
        if not stage_matches or any(m.get("state") != "completed" for m in stage_matches):
            continue
        # codes des équipes présentes dans les phases suivantes
        later = set()
        for later_slug in slugs[idx + 1:]:
            for m in by_slug.get(later_slug, []):
                for t in m.get("teams", []):
                    c = t.get("code")
                    if c not in ("TBD", "", None):
                        later.add(c)
        if not later:
            continue
        for t in entry.get("teams", []):
            c = t.get("code")
            t["eliminated"] = c not in later


def enrich_standings_images(standings, all_matches):
    """Propage l'image (logo) des équipes vers le classement, par code."""
    img = {}
    for m in all_matches:
        for t in m.get("teams", []):
            c = t.get("code")
            if c and c not in ("TBD", "") and t.get("image") and c not in img:
                img[c] = t["image"]
    for entry in standings:
        for t in entry.get("teams", []):
            if not t.get("image") and t.get("code") in img:
                t["image"] = img[t["code"]]


# Tirage au sort du Round 1 suisse (18/10/2026) — override tant que l'API renvoie TBD.
# match_id -> ((code, name), (code, name), startTime_utc)
SWISS_R1_DRAW = {
    "115660540726095005": (("GEN", "Gen.G"), ("IG", "Invictus Gaming"), "2026-10-23T17:00:00Z"),
    "115660540726095007": (("TL", "Team Liquid"), ("CFO", "CTBC Flying Oyster"), "2026-10-23T18:00:00Z"),
    "115660540726095009": (("AL", "Anyone's Legend"), ("KC", "Karmine Corp"), "2026-10-23T19:00:00Z"),
    "115660540726095011": (("G2", "G2 Esports"), ("DK", "Dplus Kia"), "2026-10-23T20:00:00Z"),
    "115660540726095013": (("HLE", "Hanwha Life Esports"), ("TES", "Top Esports"), "2026-10-23T21:00:00Z"),
    "115660540726095015": (("LOS", "Los Grandes"), ("T1", "T1"), "2026-10-23T22:00:00Z"),
    "115660540726095017": (("TSW", "Team Secret Whales"), ("LYN", "LYON"), "2026-10-23T23:00:00Z"),
    "115660540726095019": (("BLG", "Bilibili Gaming"), ("MKOI", "Movistar KOI"), "2026-10-24T00:00:00Z"),
}


def _draw_team(code, name):
    return {"name": name, "code": code, "slug": None, "image": None,
            "outcome": None, "gameWins": 0,
            "record": {"wins": None, "losses": None}}


def apply_swiss_draw(matches):
    """Injecte le tirage du Round 1 suisse sur les matchs encore TBD."""
    for m in matches:
        mid = m.get("id")
        if mid not in SWISS_R1_DRAW:
            continue
        # ne pas écraser si l'API a déjà publié de vraies équipes
        if any(t.get("code") not in ("TBD", "", None) for t in m.get("teams", [])):
            continue
        a, b, start = SWISS_R1_DRAW[mid]
        m["teams"] = [_draw_team(a[0], a[1]), _draw_team(b[0], b[1])]
        m["startTime"] = start


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
            stages_out.append({"slug": st.get("slug"), "name": tr_stage(st.get("name")),
                               "matches": matches_out})

    apply_swiss_draw(all_matches)

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

    standings = build_standings(standings_raw)
    annotate_elimination(standings, stages_out)
    enrich_standings_images(standings, all_matches)

    live = {
        "updated_at": now.isoformat(),
        "source": "lolesports",
        "tournament_id": TID,
        "next_match": next_match,
        "upcoming": upcoming,
        "results": results,
        "standings": standings,
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
