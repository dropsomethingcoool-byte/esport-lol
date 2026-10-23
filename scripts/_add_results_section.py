#!/usr/bin/env python3
import json

p = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir/content/index.json"
d = json.load(open(p, encoding="utf-8"))
body = d["body"]

section = ('<section class="home-section reveal"><h2 class="section-title">Derniers résultats</h2>'
           '<div id="live-results" class="match-list"></div>'
           '<p><a class="pill" href="/resultats/">Voir tous les résultats <span class="arrow">→</span></a></p></section>')

if 'id="live-results"' in body:
    print("Déjà présent, skip.")
else:
    anchor = '<section class="home-section reveal"><h2 class="section-title">Classement</h2>'
    if anchor in body:
        body = body.replace(anchor, section + anchor, 1)
        d["body"] = body
        d["date_modified"] = "2026-10-23"
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("OK section Derniers résultats insérée.")
    else:
        print("ANCRE introuvable.")
        for l in body.split("<section"):
            if "Classement" in l or "matchs du moment" in l:
                print("  ", l[:80])
