#!/usr/bin/env python3
"""Rédige content/guide-champions-lol.json (guide champion League of Legends)."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = ("<p>", "</p>")


def p(text):
    return f"{P[0]}{text}{P[1]}"


body = "\n".join([
    "<h2>Qu'est-ce qu'un champion dans League of Legends</h2>",

    "<h3>Une fiche, un kit, un rôle</h3>",
    p("Chaque champion de League of Legends possède un <strong>kit de quatre sorts</strong> : trois compétences de base (A, Z, E) et un ultime (R)."),
    p("Ce kit définit sa <strong>façon de jouer</strong> : engager, poke, soutenir, farmer ou burst. Un guide champion part toujours de là."),

    "<h3>Les cinq rôles du jeu</h3>",
    p("La toplane, la jungle, la midlane, la botlane et le support structurent une équipe. Chaque rôle a son <strong>économie de ressources</strong> propre."),
    p("Un champion n'est pas jouable partout : sa <strong>portée</strong>, sa mobilité et son utilité décident du rôle où il performe."),

    "<h3>Pourquoi lire un guide champion</h3>",
    p("Un <strong>guide champion league of legends</strong> sert à comprendre le kit avant de le jouer, pas seulement à copier une build."),
    p("Il évite les erreurs de départ : mauvais rôle, mauvais ordre de sorts, <strong>timings</strong> ratés en début de partie."),

    "<h2>Lire la fiche d'un champion</h2>",

    "<h3>Les statistiques de base</h3>",
    p("Points de vie, mana, armure, résistance magique, dégâts d'attaque et vitesse de déplacement forment le <strong>socle</strong> du champion."),
    p("Une <strong>faible armure</strong> de base rend la toplane risquée contre un adversaire physique, même avec un bon kit."),

    "<h3>Le passif et les sorts</h3>",
    p("Le passif donne souvent l'identité du champion : stacks permanents, bouclier, dégâts bonus ou <strong>soin</strong> conditionnel."),
    p("Les sorts ont un <strong>coût en mana</strong> et un délai de récupération. Les connaître par cœur évite de gaspiller une ouverture."),

    "<h3>La courbe de puissance</h3>",
    p("Certains champions dominent en <strong>early game</strong> et s'éteignent ensuite. D'autres ne deviennent dangereux qu'après deux ou trois objets."),
    p("Situer cette <strong>courbe</strong> change toute la stratégie : jouer agressif tôt ou farmer jusqu'au late game."),

    "<h2>Choisir son champion selon son rôle</h2>",

    "<h3>Toplane et jungle</h3>",
    p("La toplane privilégie le <strong>duel</strong> et la pression de vague. Un champion qui gagne le 1v1 peut prendre la tour rapidement."),
    p("En jungle, le <strong>clear</strong>, les ganks et le contrôle des objectifs comptent plus que les dégâts bruts."),

    "<h3>Midlane et botlane</h3>",
    p("La midlane demande de la <strong>poussée de vague</strong> pour aider la jungle et les couloirs latéraux."),
    p("La botlane se joue en <strong>duo</strong> : l'ADC apporte les dégâts à distance, le support engage ou protège selon la composition."),

    "<h3>Support et compositions d'équipe</h3>",
    p("Le support choisit selon la <strong>synergie</strong> avec son ADC : engage dur, peel ou poke soutenu."),
    p("Une équipe équilibrée combine dégâts physiques, dégâts magiques et <strong>contrôle de foule</strong> pour couvrir les faiblesses."),

    "<h2>Les grandes familles de champions</h2>",

    "<h3>Tanks, bruisers et assassins</h3>",
    p("Les tanks absorbent les dégâts et ouvrent les combats. Les <strong>bruisers</strong> tiennent la ligne en mêlée prolongée."),
    p("Les assassins cherchent une <strong>cible isolée</strong> à supprimer vite. S'ils ratent leur combo, ils paient cher."),

    "<h3>Mages, tireurs et supports</h3>",
    p("Les mages apportent du burst ou du poke à <strong>distance</strong>. Les tireurs scalent sur les dégâts d'attaque et les objets."),
    p("Les <strong>enchanters</strong> soignent et renforcent leurs alliés, tandis que les supports d'engage initient le combat."),

    "<h3>Champions simples et champions techniques</h3>",
    p("Un <strong>champion simple</strong> se joue correctement en quelques parties, ce qui libère l'attention pour la carte."),
    p("Un champion technique exige des <strong>centaines de parties</strong> pour être rentable. Le gain vient ensuite de la maîtrise, pas du kit seul."),

    "<h2>Construire et ajuster son champion</h2>",

    "<h3>Runes et sorts de summoner</h3>",
    p("Les runes complètent le kit : dégâts, survie ou <strong>vitesse</strong>. Leur choix dépend du rôle et du matchup."),
    p("Les sorts de summoner varient selon la menace : <strong>Flash</strong> presque toujours, puis Ignite, Teleport, Heal ou Cleanse."),

    "<h3>Objets et ordre d'achat</h3>",
    p("Un premier objet mal choisi retarde toute la <strong>courbe de puissance</strong> du champion, surtout en couloir."),
    p("L'ordre d'achat s'adapte à l'adversaire direct. Contre une équipe très <strong>magique</strong>, la résistance magique arrive plus tôt."),

    "<h3>Adapter selon le patch</h3>",
    p("Chaque patch ajuste des ratios et des coûts. Un <strong>guide champion</strong> doit donc être revérifié après chaque mise à jour majeure."),
    p("Suivre les <a href=\"/tier-list-lol/\">tier list LoL</a> et les <a href=\"/runes-league-of-legends/\">runes League of Legends</a> aide à repérer les <strong>champions forts</strong> du moment."),

    "<h2>Progresser avec un champion</h2>",

    "<h3>Le nombre de parties pour maîtriser un kit</h3>",
    p("La maîtrise vient de la <strong>répétition</strong> : le même champion, sur le même rôle, dans des matchups variés."),
    p("Changer de champion à chaque partie empêche d'<strong>ancrer</strong> les automatismes de combo et les timings de sorts."),

    "<h3>Choisir un pool de champions</h3>",
    p("Un <strong>pool réduit</strong> de deux ou trois champions par rôle suffit pour grimper en ranked."),
    p("Mieux vaut un champion <strong>maîtrisé</strong> qu'un champion tier S joué pour la première fois en classée."),

    "<h3>Analyser ses parties</h3>",
    p("Revoir une <strong>replay</strong> après une défaite révèle les erreurs de position et les sorts gaspillés."),
    p("Le <a href=\"/planning/\">planning des Worlds</a> et le <a href=\"/classement/\">classement</a> donnent des <strong>repères concrets</strong> sur les picks de la scène compétitive."),

    "<h2>Ressources pour aller plus loin</h2>",

    "<h3>Guides et tier lists</h3>",
    p("Un guide champion se consulte <strong>avant</strong> de jouer, pas après. Une lecture rapide du kit suffit souvent à éviter l'erreur."),
    p("Les <a href=\"/tier-list-lol/\">tier list LoL</a> situent le champion dans la <strong>méta</strong>, sans remplacer la lecture de ses sorts."),

    "<h3>Suivre la méta et les équipes</h3>",
    p("Regarder les <a href=\"/equipes/\">équipes des Worlds</a> jouer montre comment les pros exploitent un kit au <strong>plus haut niveau</strong>."),
    p("Le <a href=\"/blog/\">blog League of Legends</a> regroupe les guides transversaux : <strong>builds</strong>, compteurs et bases du jeu."),

    "<h3>Un guide champion n'est pas une recette</h3>",
    p("Copier une build sans comprendre le <strong>pourquoi</strong> ne rend pas meilleur. Le contexte de partie décide toujours."),
    p("Le guide donne les <strong>bases vérifiables</strong> ; l'adaptation au matchup reste la vraie compétence à travailler."),
])

page = {
    "slug": "guide-champions-lol",
    "type": "article",
    "title": "Guide champion League of Legends : lire sa fiche et le jouer",
    "meta_title": "Guide champion League of Legends : fiche et rôle",
    "meta_description": "Guide champion League of Legends : lire une fiche, comprendre le kit, choisir son rôle, ses runes et ses objets, et progresser sur un champion.",
    "h1": "Guide champion League of Legends",
    "intro": "<p class=\"lead\">Ce <strong>guide champion league of legends</strong> explique comment lire une fiche, situer le kit dans un rôle et utiliser le champion sans copier une build au hasard.</p>",
    "body": body,
    "related": [
        {"slug": "tier-list-lol", "anchor": "Tier List LoL"},
        {"slug": "runes-league-of-legends", "anchor": "Runes League of Legends"},
        {"slug": "blog", "anchor": "Blog League of Legends"},
    ],
    "date_modified": "2026-10-19",
    "date_published": "2026-10-19",
}

out = os.path.join(ROOT, "content", "guide-champions-lol.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(page, f, ensure_ascii=False, indent=2)
print("écrit:", out)
