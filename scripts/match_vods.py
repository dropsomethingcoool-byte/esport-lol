#!/usr/bin/env python3
"""Extrait les VODs (YouTube/Twitch) d'un match Worlds via l'API lolesports.

Usage :
  python3 scripts/match_vods.py <matchId> [--html] [--lang fr-FR,en-US]

Sortie : JSON (défaut) listant, par manche, la VOD préférée (fr-FR puis en-US),
ou HTML (--html) prêt à coller dans un article.
"""
import json
import sys
import urllib.request

API = "https://esports-api.lolesports.com/persisted/gw"
KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
PREFERRED = ["fr-FR", "en-US", "en-GB"]


def get(path):
    req = urllib.request.Request(API + path, headers={"x-api-key": KEY, "Accept": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())


def pick_vod(game, langs):
    vods = game.get("vods") or []
    for lang in langs:
        for v in vods:
            if v.get("locale") == lang and v.get("provider") == "youtube":
                return {"game": game.get("number"), "locale": lang,
                        "provider": "youtube",
                        "url": f"https://www.youtube.com/watch?v={v.get('parameter')}"}
    # fallback : première VOD youtube dispo
    for v in vods:
        if v.get("provider") == "youtube":
            return {"game": game.get("number"), "locale": v.get("locale"),
                    "provider": "youtube",
                    "url": f"https://www.youtube.com/watch?v={v.get('parameter')}"}
    return None


def main():
    if len(sys.argv) < 2:
        print("usage: match_vods.py <matchId> [--html] [--lang fr-FR,en-US]", file=sys.stderr)
        return 1
    mid = sys.argv[1]
    as_html = "--html" in sys.argv
    langs = PREFERRED
    for a in sys.argv:
        if a.startswith("--lang="):
            langs = a.split("=", 1)[1].split(",")

    d = get(f"/getEventDetails?hl=fr-FR&id={mid}")
    games = ((d.get("data", {}).get("event", {}) or {}).get("match") or {}).get("games") or []

    vods = []
    for g in games:
        if g.get("state") == "completed":
            v = pick_vod(g, langs)
            if v:
                vods.append(v)

    if as_html:
        if not vods:
            print("<p class=\"muted\">Aucune VOD disponible pour ce match.</p>")
            return 0
        urls = sorted({v["url"] for v in vods})
        if len(urls) == 1:
            # VOD complète du match (même vidéo pour toutes les manches)
            loc = vods[0]["locale"]
            print(f'<p><a href="{urls[0]}" rel="noopener">▶ Revivre le match en intégralité (VOD {loc})</a></p>')
        else:
            items = [f'<li>Manche {v["game"]} — <a href="{v["url"]}" rel="noopener">VOD ({v["locale"]})</a></li>' for v in vods]
            print("<ul>" + "".join(items) + "</ul>")
    else:
        json.dump({"match_id": mid, "vods": vods}, sys.stdout, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
