#!/usr/bin/env python3
"""Maillage interne : injecte des liens contextuels à ancres optimisées
vers /joueur-faker/, /joueur-caliste/ et /joueurs/ depuis les pages existantes."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

# (fichier, ancien_texte, nouveau_texte)
INJECTIONS = [
    # 1) Faker : fiche équipe T1 -> joueur-faker
    ("equipe-t1.json",
     "capitaine emblématique Faker, T1",
     'capitaine emblématique <a href="/joueur-faker/">Faker</a>, T1'),
    # 2) Faker : pronostics -> joueur-faker
    ("pronostics-worlds-lol.json",
     "avec Faker, et",
     'avec <a href="/joueur-faker/">Faker</a>, et'),
    # 3) Caliste : fiche équipe KC -> joueur-caliste (phrase ajoutée)
    ("equipe-karmine-corp.json",
     "fédérer une communauté immense.</p>",
     'fédérer une communauté immense.</p><p>Portée par <a href="/joueur-caliste/">Caliste</a>, son <strong>prodige</strong> au poste d\'ADC, la formation tricolore mise sur sa nouvelle génération pour exister au plus haut niveau.</p>'),
    # 4) hub joueurs : equipes.json
    ("equipes.json",
     "à surveiller tout au long du tournoi.</p>",
     'à surveiller tout au long du tournoi.</p><p>Consultez aussi les <a href="/joueurs/">fiches joueurs des Worlds 2026</a> : profil, palmarès et style de jeu des <strong>stars</strong> de la compétition.</p>'),
    # 5) hub joueurs : planning.json
    ("planning.json",
     "outsiders du swiss stage.</p>",
     'outsiders du swiss stage. Retrouvez leurs <a href="/joueurs/">fiches joueurs détaillées</a>.</p>'),
    # 6) hub joueurs : article pilier
    ("joueurs-a-suivre-worlds-2026.json",
     'Retrouvez aussi les <a href="/equipes/">fiches des 19 équipes des Worlds</a>.',
     'Retrouvez aussi les <a href="/equipes/">fiches des 19 équipes des Worlds</a> et les <a href="/joueurs/">fiches joueurs</a>.'),
]

for fn, old, new in INJECTIONS:
    p = os.path.join(CONTENT, fn)
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    body = d["body"]
    if new.split(">")[0] in body or 'href="/joueur-' in body and fn.startswith("equipe") and "joueur-" in body:
        # heuristique : si le lien cible est déjà présent, on saute
        pass
    if old not in body:
        print(f"✗ {fn}: ancre introuvable -> {old[:40]}")
        continue
    if 'href="/joueur-faker/"' in body or 'href="/joueur-caliste/"' in body or 'href="/joueurs/"' in body:
        # vérifier si le lien cible est déjà présent dans ce fichier
        pass
    # injection idempotente : ne rien faire si l'URL cible est déjà présente
    if fn == "equipe-t1.json" and 'href="/joueur-faker/"' in body:
        print(f"· {fn}: lien déjà présent")
        continue
    if fn == "pronostics-worlds-lol.json" and 'href="/joueur-faker/"' in body:
        print(f"· {fn}: lien déjà présent")
        continue
    if fn == "equipe-karmine-corp.json" and 'href="/joueur-caliste/"' in body:
        print(f"· {fn}: lien déjà présent")
        continue
    if fn in ("equipes.json", "planning.json", "joueurs-a-suivre-worlds-2026.json") and 'href="/joueurs/"' in body:
        print(f"· {fn}: lien /joueurs/ déjà présent")
        continue
    d["body"] = body.replace(old, new, 1)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"✓ {fn}: lien injecté")
