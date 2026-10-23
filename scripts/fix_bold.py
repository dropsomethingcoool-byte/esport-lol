#!/usr/bin/env python3
"""Ajoute le gras manquant (1 par paragraphe) sur la page parier-worlds-lol."""
import json
import os

PATH = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir/content/parier-worlds-lol.json"

FIXES = [
    ("Cette méthode aide à repérer une cote supérieure à votre propre estimation du résultat.",
     "Cette méthode aide à repérer une <strong>cote supérieure</strong> à votre propre estimation du résultat."),
    ("Le pari en direct demande de décider vite, car la cote bouge à chaque objectif pris.",
     "Le pari en direct demande de décider vite, car la cote bouge à chaque <strong>objectif pris</strong>."),
    ("Le gain se calcule en multipliant la mise par la cote.",
     "Le gain se calcule en multipliant la mise par <strong>la cote</strong>."),
    ("La bankroll est le budget total réservé aux paris, séparé de vos dépenses courantes.",
     "La bankroll est le <strong>budget total</strong> réservé aux paris, séparé de vos dépenses courantes."),
    ("Le cash out permet de clôturer un pari avant la fin et de récupérer une partie du gain.",
     "Le cash out permet de clôturer un pari avant la fin et de récupérer <strong>une partie du gain</strong>."),
    ("pour repérer les équipes en forme.",
     "pour repérer les <strong>équipes en forme</strong>."),
    ("Le même pari peut afficher une cote différente selon le bookmaker. Comparer augmente le gain.",
     "Le même pari peut afficher une <strong>cote différente</strong> selon le bookmaker. Comparer augmente le gain."),
    ("Suivre les changements de patch aide à anticiper les compositions probables d'un match.",
     "Suivre les changements de patch aide à anticiper les <strong>compositions probables</strong> d'un match."),
    ("Miser sur son équipe favorite fausse le jugement. La passion ne remplace pas l'analyse.",
     "Miser sur son équipe favorite <strong>fausse le jugement</strong>. La passion ne remplace pas l'analyse."),
    ("Après une défaite, gardez la même mise ou réduisez-la. Ne pariez pas pour compenser une perte.",
     "Après une défaite, gardez la <strong>même mise</strong> ou réduisez-la. Ne pariez pas pour compenser une perte."),
    ("Ces promotions sont soumises à des conditions générales. Lisez-les avant de vous inscrire.",
     "Ces promotions sont soumises à des <strong>conditions générales</strong>. Lisez-les avant de vous inscrire."),
    ("Nous recommandons de comparer BetNinja avec d'autres bookmakers avant de choisir. Les cotes et les bonus changent.",
     "Nous recommandons de <strong>comparer</strong> BetNinja avec d'autres bookmakers avant de choisir. Les cotes et les bonus changent."),
    ("Ne pariez jamais pour récupérer une perte.",
     "Ne pariez jamais pour <strong>récupérer une perte</strong>."),
]

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)

body = d["body"]
for old, new in FIXES:
    if old not in body:
        print("!! introuvable :", old[:50])
    body = body.replace(old, new, 1)

d["body"] = body
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# vérif finale
import re
paras = re.findall(r'<p(?:\s[^>]*)?>(.*?)</p>', body, re.DOTALL)
n0 = sum(1 for p in paras if '<strong>' not in p and 'cta-disclosure' not in p)
print("OK. Paragraphes éditoriaux sans gras restants:", n0)
