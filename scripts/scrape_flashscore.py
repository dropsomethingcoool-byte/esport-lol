#!/usr/bin/env python3
"""Scraping best-effort des résultats League of Legends sur flashscore.fr.

Usage : python3 scripts/scrape_flashscore.py [--match <id>]
Affiche un JSON avec planning / résultats / classement si disponible.

NOTE : flashscore est protégé (anti-bot, JS). Ce script fait un best-effort ;
en cas d'échec, l'agent doit utiliser web_extract comme fallback et ne jamais
inventer de score. Ne stocke AUCUNE donnée inventée.
"""
import json
import sys
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

URLS = [
    "https://www.flashscore.fr/esports/league-of-legends/championnat-du-monde/",
    "https://www.flashscore.fr/esports/league-of-legends/",
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def main():
    out = {"source": "flashscore.fr", "status": "ok", "matches": [], "note": ""}
    fetched = False
    for url in URLS:
        try:
            html = fetch(url)
            fetched = True
            # Extraction naïve : on cherche des fragments structurés. Flashscore charge
            # le contenu en JS, donc le HTML brut contient surtout des placeholders.
            if "Championnat" in html or "League" in html:
                out["note"] = "HTML récupéré mais contenu dynamique (JS) non parsable ici."
            else:
                out["note"] = "Page inaccessible ou contenu vide."
            break
        except Exception as e:
            out["note"] = f"Échec {url}: {e}"
    if not fetched:
        out["status"] = "error"
        out["note"] = "Impossible de joindre flashscore. Utiliser web_extract en fallback."
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
