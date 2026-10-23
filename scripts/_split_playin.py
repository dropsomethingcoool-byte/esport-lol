#!/usr/bin/env python3
"""Sépare les infos play-in : crée une page dédiée play-in-worlds-lol,
retire la section play-in de la page planning (remplacée par un lien),
et ajoute la page au menu (nav.json)."""
import json

# 1) Créer la page play-in
playin = {
    "slug": "play-in-worlds-lol",
    "type": "page",
    "silo": "planning",
    "title": "Play-in des Worlds LoL 2026 : résultats et résumés",
    "meta_title": "Play-in Worlds LoL 2026 : résultats et résumés des matchs",
    "meta_description": "Résultats du play-in des Worlds LoL 2026 : Karmine Corp qualifiée pour le swiss stage. Retrouvez le résumé de chaque match.",
    "h1": "Play-in des Worlds LoL 2026",
    "intro": "<p class=\"lead\">Le play-in des Worlds 2026 s'est déroulé du 15 au 18 octobre. Retrouvez ici les résultats et le résumé de chaque rencontre.</p>",
    "body": (
        "<h2>Le play-in des Worlds 2026</h2>\n"
        "<p>Le play-in s'est déroulé du 15 au 18 octobre 2026. Quatre équipes s'y sont affrontées pour décrocher une place dans le swiss stage : <strong>Karmine Corp</strong>, MVK Esports, FURIA et Cloud9 Kia.</p>\n"
        "<p><strong>Karmine Corp</strong> a remporté le play-in, validant son billet pour le swiss stage après un parcours maîtrisé.</p>\n\n"
        "<h2>Les matchs du play-in</h2>\n"
        "<p>Retrouvez le résumé de chaque rencontre :</p>\n"
        "<ul>\n"
        "<li><a href=\"/karmine-corp-remporte-play-in/\">Karmine Corp remporte le play-in</a> — la qualification de KC pour le swiss stage</li>\n"
        "<li><a href=\"/kc-vs-mvk-resume/\">Karmine Corp 3-0 MVK Esports</a></li>\n"
        "<li><a href=\"/mvk-vs-fur-resume/\">MVK Esports 3-0 FURIA</a></li>\n"
        "<li><a href=\"/mvk-vs-furia-resume/\">MVK Esports 3-1 FURIA</a></li>\n"
        "<li><a href=\"/fur-vs-c9-resume/\">FURIA 3-1 Cloud9 Kia</a></li>\n"
        "<li><a href=\"/kc-vs-cloud9-resume/\">Karmine Corp 3-2 Cloud9 Kia</a></li>\n"
        "</ul>\n\n"
        "<p>Le <a href=\"/planning/\">swiss stage</a> a pris le relais à partir du 23 octobre, avec les 16 équipes qualifiées.</p>"
    ),
    "related": [
        {"slug": "planning", "anchor": "planning des Worlds"},
        {"slug": "classement", "anchor": "classement des Worlds"},
        {"slug": "resultats", "anchor": "résultats en direct"},
        {"slug": "blog", "anchor": "tous les résumés"},
    ],
    "date_modified": "2026-10-23",
    "date_published": "2026-10-23",
}
json.dump(playin, open("content/play-in-worlds-lol.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("✓ play-in-worlds-lol.json créé")

# 2) Retirer la section play-in de planning + lien
d = json.load(open("content/planning.json", encoding="utf-8"))
body = d["body"]
old = ('<h2>Play-ins — du 15 au 18 octobre 2026</h2><p>Le play-in s\'est achevé le 18 octobre : '
       '<strong>Karmine Corp</strong> a validé son billet pour le swiss stage en dominant MVK Esports en finale.</p>')
new = ('<p>Le <strong>play-in</strong> est terminé : retrouvez les résultats sur la '
       '<a href="/play-in-worlds-lol/">page dédiée au play-in</a>.</p>')
if old in body:
    body = body.replace(old, new)
    d["body"] = body
    json.dump(d, open("content/planning.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("✓ planning.json : section play-in remplacée par un lien")
else:
    print("⚠ section play-in introuvable dans planning.json (à vérifier)")

# 3) Ajouter la page au menu
nav = json.load(open("data/nav.json", encoding="utf-8"))
for silo in nav.get("silos", []):
    if silo.get("slug") == "planning":
        slugs = [p.get("slug") for p in silo.get("pages", [])]
        if "play-in-worlds-lol" not in slugs:
            silo.setdefault("pages", []).append({"label": "Play-in", "slug": "play-in-worlds-lol"})
            print("✓ nav.json : page Play-in ajoutée au menu 'Suivi des Worlds'")
        break
json.dump(nav, open("data/nav.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("Terminé.")
