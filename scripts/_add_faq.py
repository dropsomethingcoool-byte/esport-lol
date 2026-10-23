#!/usr/bin/env python3
"""Ajoute une section FAQ (visible) + champ `faq` (pour JSON-LD FAQPage)
aux guides builds / compteurs / lexique. Idempotent."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

FAQ = {
    "builds-lol": [
        ("Qu'est-ce qu'un build dans League of Legends ?",
         "Un build est la liste d'objets, de bottes et de composants qu'un champion achète au fil de la partie pour maximiser son efficacité."),
        ("Quelle est la différence entre un build et une page de runes ?",
         "Le build concerne les objets achetés en cours de partie, tandis que la page de runes se règle avant le lancement de la partie."),
        ("Comment adapter son build en cours de partie ?",
         "Il faut lire la composition adverse, ajuster selon l'avance ou le retard d'or et acheter les objets adaptés à la situation."),
        ("Pourquoi les builds changent-ils à chaque patch ?",
         "Riot Games rééquilibre régulièrement les objets et les champions, ce qui rend certains builds plus ou moins efficaces d'un patch à l'autre."),
    ],
    "compteurs-lol": [
        ("Qu'est-ce qu'un counter dans League of Legends ?",
         "Un counter est un champion, une classe ou une stratégie qui réduit fortement l'efficacité d'un adversaire donné."),
        ("Un counter garantit-il la victoire sur sa lane ?",
         "Non. Un counter donne un avantage, mais il faut encore savoir l'exécuter : le matchup favorable ne remplace pas la maîtrise du champion."),
        ("Comment identifier le bon counter pour un champion ?",
         "En analysant ses trois sorts, ses forces de début de partie et en croisant le matchup avec le plan de jeu de l'équipe."),
        ("Où trouver les statistiques de matchup dans le client ?",
         "Le client de League of Legends affiche des statistiques de victoire par matchup, à pondérer selon le niveau de jeu."),
    ],
    "lexique-lol": [
        ("Que signifie CC dans League of Legends ?",
         "CC signifie crowd control, c'est-à-dire tout contrôle de foule : ralentissement, étourdissement, immobilisation ou suppression."),
        ("C'est quoi le split push en LoL ?",
         "Le split push consiste à pousser une ligne seul pendant que le reste de l'équipe occupe l'ennemi ailleurs sur la carte."),
        ("Que veut dire Bo5 ?",
         "Bo5 signifie best of five : une série au meilleur des cinq manches, le format des phases finales des grandes compétitions."),
        ("Qu'est-ce que la méta en League of Legends ?",
         "La méta désigne l'ensemble des champions, stratégies et objets dominants à un moment donné, en fonction des équilibrages du patch."),
    ],
}


def build_faq_html(faq):
    parts = ['<h2>Questions fréquentes</h2>']
    for q, a in faq:
        parts.append(f"<h3>{q}</h3><p><strong>{a}</strong></p>")
    return "".join(parts)


for slug, faq in FAQ.items():
    p = os.path.join(CONTENT, f"{slug}.json")
    d = json.load(open(p, encoding="utf-8"))
    body = d["body"]
    if "Questions fréquentes" not in body:
        # insérer la FAQ avant la source-line si présente, sinon en fin
        src = body.find('class="source-line"')
        if src != -1:
            j = body.rfind("<h2", 0, src)
            if j == -1:
                j = src
            body = body[:j] + build_faq_html(faq) + "\n" + body[j:]
        else:
            body = body.rstrip() + "\n" + build_faq_html(faq)
        d["body"] = body
    # champ faq pour le JSON-LD
    d["faq"] = [{"question": q, "answer": a} for q, a in faq]
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  ✓ {slug}: FAQ ajoutée ({len(faq)} questions)")
