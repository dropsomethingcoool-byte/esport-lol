#!/usr/bin/env python3
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(ROOT, "content", "patch-notes-lol.json")
p = json.load(open(path, encoding="utf-8"))
body = p["body"]

repl = [
    ("Un patch remplace le précédent sur les serveurs live : les valeurs ci-dessous sont celles en vigueur sur la Faille depuis cette date.",
     "Un patch remplace le précédent sur les serveurs live : les valeurs ci-dessous sont <strong>celles en vigueur</strong> sur la Faille depuis cette date."),
    ("Les champions forts en compétition sont bridés, les profils trop faibles reçoivent des buffs ciblés, et les objets polyvalents sont réorientés vers un usage plus risqué.",
     "Les champions forts en compétition sont bridés, les profils trop faibles reçoivent des buffs ciblés, et les <strong>objets polyvalents</strong> sont réorientés vers un usage plus risqué."),
    ("Les guides d'analyse comme notre <a href=\"/tier-list-lol/\">tier list LoL</a> se réévaluent à chaque patch, car la position d'un champion dépend directement de ces valeurs.",
     "Les guides d'analyse comme notre <a href=\"/tier-list-lol/\">tier list LoL</a> se réévaluent à chaque patch, car la position d'un champion dépend <strong>directement</strong> de ces valeurs."),
    ("Le choix des <strong>arbres de runes</strong> doit suivre cette logique.",
     "Le choix des <strong>arbres de runes</strong> suit alors une logique simple : garder l'arbre principal et déplacer les points les moins rentables."),
    ("<p>Pendant cette période, les notes officielles restent la <strong>seule source fiable</strong> sur les valeurs réellement appliquées.</p>\n<p>Pour suivre l'actualité du jeu et des Worlds, retrouvez nos analyses sur le <a href=\"/blog/\">blog League of Legends</a>, <strong>actualisé</strong> à chaque phase du tournoi.</p>",
     "<p>Pendant cette période, les notes officielles restent la <strong>seule source fiable</strong> sur les valeurs appliquées. Pour suivre l'actualité du jeu et des Worlds, retrouvez nos analyses sur le <a href=\"/blog/\">blog League of Legends</a>.</p>"),
]
for old, new in repl:
    assert old in body, old[:70]
    body = body.replace(old, new, 1)

p["body"] = body
json.dump(p, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("mots:", len(re.sub(r"<[^>]+>", " ", body).split()))
