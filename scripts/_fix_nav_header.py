#!/usr/bin/env python3
"""Menu header : retire le silo « Joueurs », l'ajoute comme page sous « Équipes »,
et bascule le silo des fiches joueur vers « equipes » (fil d'Ariane cohérent)."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
NAV = os.path.join(ROOT, "data", "nav.json")
CONTENT = os.path.join(ROOT, "content")

with open(NAV, encoding="utf-8") as f:
    nav = json.load(f)

silos = nav["silos"]
joueurs = next((s for s in silos if s.get("slug") == "joueurs"), None)
if joueurs:
    silos.remove(joueurs)
for s in silos:
    if s.get("slug") == "equipes":
        pages = s.get("pages", [])
        if not any(p.get("slug") == "joueurs" for p in pages):
            pages.append({"label": "Joueurs", "slug": "joueurs"})
        s["pages"] = pages
        break
nav["silos"] = silos
with open(NAV, "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=2)
print("✓ nav.json : Joueurs sous Équipes ; Accueil conservé dans home (non rendu)")

for slug in ["joueur-faker", "joueur-caliste"]:
    p = os.path.join(CONTENT, slug + ".json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    d["silo"] = "equipes"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"✓ {slug} silo -> equipes")
