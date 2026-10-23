#!/usr/bin/env python3
"""Génère content/compteurs-lol.json (page evergreen : compteurs League of Legends)."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "content", "compteurs-lol.json")

KW = "counter league of legends"

page = {
    "slug": "compteurs-lol",
    "type": "article",
    "title": "Counter League of Legends : trouver le compteur LoL",
    "meta_title": "Counter League of Legends : guide des compteurs LoL",
    "meta_description": (
        "Comment trouver le counter League of Legends d'un champion : leçons de "
        "matchup, classes, sorts clés et adaptation du pick en draft LoL."
    ),
    "h1": "Counter League of Legends",
    "intro": (
        '<p class="lead">Un <strong>counter league of legends</strong> désigne un champion, '
        "une classe ou une stratégie qui réduit fortement l'efficacité "
        "d'un adversaire donné. Ce guide explique comment identifier le bon compteur et "
        "l'exploiter en draft.</p>"
    ),
    "silo": "blog",
    "body": "",
    "related": [
        {"slug": "tier-list-lol", "anchor": "Tier List LoL"},
        {"slug": "guide-champions-lol", "anchor": "Guide des champions LoL"},
        {"slug": "blog", "anchor": "Blog League of Legends"},
    ],
    "date_modified": "2026-10-22",
    "date_published": "2026-10-22",
}

B = []


def h2(t):
    B.append(f"<h2>{t}</h2>")


def h3(t):
    B.append(f"<h3>{t}</h3>")


def p(t):
    B.append(f"<p>{t}</p>")


# ------------------------------------------------------------------ H2 1
h2("Qu'est-ce qu'un counter dans League of Legends")
h3("La définition du counter LoL")
p(
    "Un counter n'est pas un champion qui gagne automatiquement : c'est un champion dont "
    "le kit exploite les <strong>faiblesses</strong> d'un autre. La notion dépend du "
    "matchup, de la lane et du niveau de jeu, pas d'une liste figée."
)
p(
    "Un compteur qui domine en partie classique peut perdre son avantage en compétition. "
    "La coordination d'équipe, les <strong>rotations</strong> du jungler et la draft "
    "globale pèsent autant que le face-à-face en lane."
)

h3("Ce que le counter ne veut pas dire")
p(
    "Beaucoup de joueurs confondent counter et champion fort du moment. Un champion "
    "surreprésenté dans une <a href=\"/tier-list-lol/\">tier list LoL</a> est simplement "
    "efficace, pas forcément le <strong>compteur</strong> de son adversaire direct."
)
p(
    "Un champion peut aussi compter un adversaire sans le battre en lane. Un tank qui "
    "absorbe les dégâts d'un assassin le neutralise en combat d'équipe "
    "sans jamais l'affronter en duel. La notion varie enfin avec le patch : un changement "
    "de ratio peut faire basculer un matchup autrefois favorable, et les "
    "<a href=\"/builds-lol/\">builds LoL</a> suivent la même <strong>logique</strong> "
    "évolutive."
)

# ------------------------------------------------------------------ H2 2
h2("Les grandes classes et leurs relations de counter")
h3("Les tireurs et les combattants de mêlée")
p(
    "Les tireurs dominent à distance les combattants lents qui ne peuvent pas les "
    "atteindre. Une fois l'écart de portée exploité, le combattant subit les dégâts sans "
    "pouvoir riposter en <strong>échanges</strong>."
)
p(
    "À l'inverse, un combattant qui atteint un tireur au corps à corps gagne presque "
    "systématiquement. Les champions dotés d'une accélération ou d'un saut réduisent "
    "fortement cet <strong>écart de portée</strong>."
)

h3("Les assassins et les champions fragiles")
p(
    "Les assassins ciblent les porteurs de dégâts isolés : mages, tireurs, mais aussi "
    "certains junglers peu mobiles. Leur pic de puissance arrive au niveau six, quand "
    "l'ulti permet de <strong>tuer</strong> en un seul combo."
)
p(
    "Les champions fragiles se protègent par la vision et par la distance. Un mage qui "
    "garde ses sorts de contrôle pour le moment de l'engage survit souvent à un "
    "<strong>assassin</strong> qui a brûlé ses sorts."
)

h3("Les tanks et les contrôleurs")
p(
    "Les tanks comptent les assassins et les porteurs de dégâts continus, car ils "
    "absorbent les burst sans mourir. Leur rôle est de <strong>survivre</strong> "
    "suffisamment longtemps pour que les dégâts ennemis se dispersent."
)
p(
    "Face à un tank, les champions dotés de dégâts en pourcentage de points de vie ou de "
    "réduction d'armure sont privilégiés. Sans ces outils, un <strong>duel</strong> "
    "devient interminable."
)

h3("Les supports et les soigneurs")
p(
    "Un soigneur soutenu par des objets anti-soin perd une partie de son efficacité. Ce "
    "contre n'est pas un champion mais un <strong>achat</strong>, disponible pour "
    "presque toutes les classes."
)
p(
    "Les supports de contrôle comptent les engageurs prévisibles. Placer un sort de "
    "contrôle au bon moment annule la <strong>téléportation</strong> ou la charge "
    "annoncée de l'adversaire."
)

# ------------------------------------------------------------------ H2 3
h2("Comment identifier le bon counter pour un champion")
h3("Analyser les trois sorts du champion adverse")
p(
    "Chaque champion possède un sort principal qui conditionne son plan : un sort de "
    "contrôle, un sort de mobilité ou un sort de dégâts massifs. Identifier cette "
    "<strong>pièce maîtresse</strong> oriente tout le choix du counter."
)
p(
    "Face à un champion qui dépend d'un sort à incantation longue, les interruptions et "
    "les silences sont décisifs. Le sort annulé, l'adversaire perd son "
    "<strong>rythme</strong> de combat."
)

h3("Regarder ses forces de début de partie")
p(
    "Certains champions dominent les niveaux un à trois et perdent leur avantage ensuite. "
    "Contre eux, la bonne réponse est souvent de <strong>subir</strong> les premières "
    "vagues sans concéder de mort."
)
p(
    "D'autres champions montent en puissance après le premier objet terminé. Les "
    "affronter tôt, avec un champion fort en début de partie, transforme un "
    "<strong>matchup</strong> difficile en avantage exploitable."
)

h3("Croiser le matchup avec le plan d'équipe")
p(
    "Un counter individuel peut déséquilibrer la composition globale. Choisir un "
    "compteur qui laisse l'équipe sans tank ni <strong>engage</strong> fragilise "
    "l'ensemble du combat d'équipe."
)
p(
    "La draft se lit donc à deux niveaux : le face-à-face en lane et les besoins "
    "collectifs. Les compositions professionnelles des <a href=\"/planning/\">Worlds "
    "LoL</a> illustrent souvent ce <strong>compromis</strong>."
)

# ------------------------------------------------------------------ H2 4
h2("Jouer un matchup favorable sans gâcher son avantage")
h3("Geler la lane et priver l'adversaire d'or")
p(
    "Quand le matchup est favorable, la tentation est de pousser en permanence. Une vague "
    "gelée près de sa propre tour prive pourtant l'adversaire de <strong>farm</strong> "
    "tout en gardant le joueur hors de portée du jungler."
)
p(
    "L'avantage se construit sur l'écart de farm et de niveaux, pas forcément sur les "
    "kills. Un <strong>écart de vingt sbires</strong> vaut presque une élimination en "
    "début de partie."
)

h3("Convertir l'avantage en objectifs")
p(
    "Une lane gagnée qui reste sur sa lane ne profite pas à l'équipe. Le report de la "
    "pression vers les <strong>objectifs</strong> neutres transforme l'avantage "
    "individuel en avantage collectif."
)
p(
    "Les dragons et les hérauts exigent souvent une rotation. Gagner sa lane sans jamais "
    "bouger laisse l'adversaire <strong>gagner</strong> la partie ailleurs sur la carte."
)

h3("Éviter le piège de la surconfiance")
p(
    "Les erreurs les plus coûteuses arrivent souvent dans un matchup favorable. Un joueur "
    "qui se sent supérieur tente des plongeons sous tour et offre un "
    "<strong>retournement</strong> gratuit."
)
p(
    "Le counter réduit la difficulté, il ne supprime pas le risque. Garder la même "
    "vigilance face aux <strong>ganks</strong> reste indispensable, même avec un "
    "avantage net."
)

# ------------------------------------------------------------------ H2 5
h2("Chercher les compteurs avec les outils du client")
h3("Les statistiques de matchup dans le client")
p(
    "Le client de League of Legends ne donne pas directement les compteurs dans l'écran "
    "de sélection. Les sites de statistiques externes compilent les <strong>taux</strong> "
    "de victoire par matchup sur des millions de parties."
)
p(
    "Ces pourcentages restent des moyennes. Un champion statistiquement faible dans un "
    "matchup peut rester le meilleur choix pour un joueur qui le <strong>maîtrise</strong> "
    "parfaitement."
)

h3("Le poids du niveau de jeu")
p(
    "Les counters ne se comportent pas de la même façon selon le niveau. Un counter qui "
    "repose sur une <strong>mécanique</strong> précise sous-performe en dessous d'un "
    "certain niveau de jeu."
)
p(
    "Les champions simples et directs affichent souvent de meilleurs résultats en partie "
    "classique, alors que les <strong>compteurs</strong> techniques brillent surtout en "
    "élite."
)

h3("Tester et garder une trace")
p(
    "Le meilleur moyen de connaître ses matchups reste de les jouer. Noter les "
    "<strong>impressions</strong> après chaque partie difficile aide à repérer les "
    "schémas récurrents. Le <a href=\"/guide-champions-lol/\">guide des champions LoL</a> "
    "complète cette démarche en détaillant les sorts et les plans de jeu de chaque "
    "champion."
)
p(
    "Les <a href=\"/runes-league-of-legends/\">runes League of Legends</a> s'adaptent "
    "aussi au matchup : une branche défensive change parfois un counter subi en "
    "<strong>lane</strong> tenable."
)

# ------------------------------------------------------------------ H2 6
h2("Les erreurs fréquentes sur les counters")
h3("Choisir un counter sans le connaître")
p(
    "Jouer un champion uniquement pour contrer son adversaire, sans le maîtriser, annule "
    "presque toujours l'avantage. La <strong>connaissance</strong> du champion pèse plus "
    "que le pourcentage du matchup."
)
p(
    "Un joueur expérimenté sur son champion principal bat souvent un débutant sur le "
    "compteur théorique. Le <strong>confort</strong> mécanique reste un critère de "
    "draft à part entière."
)

h3("Oublier l'ordre de la draft")
p(
    "Le choix du counter dépend du timing. Prendre un counter en première phase de draft "
    "expose à un <strong>contre-counter</strong> immédiat de l'adversaire, comme le "
    "montrent les drafts suivies dans le <a href=\"/classement/\">classement des Worlds</a>."
)
p(
    "Garder son pick réactif pour la dernière phase maximise l'information disponible. "
    "Chaque pick adverse révélé réduit l'incertitude : <strong>le dernier pick</strong> "
    "de la draft est donc le plus informé des cinq."
)

h3("Croire qu'un counter gagne la partie à lui seul")
p(
    "Un counter ne compense jamais une mauvaise lecture de la carte. La vision, les "
    "objectifs et les rotations restent les vrais leviers d'une partie "
    "de League of Legends. Les meilleurs joueurs l'utilisent comme un "
    "<strong>bonus</strong>, pas comme un plan complet : le reste dépend de la "
    "discipline et de la communication d'équipe."
)

page["body"] = "\n".join(B)

# ---- contrôle qualité interne -------------------------------------------
plain = re.sub(r"<[^>]+>", " ", page["body"])
words = len(plain.split())
paras = re.findall(r"<p>(.*?)</p>", page["body"], re.S)
long_paras = [
    len(re.sub(r"<[^>]+>", " ", x).split())
    for x in paras
    if len(re.sub(r"<[^>]+>", " ", x).split()) >= 60
]
print(f"body={words} mots, {len(paras)} paragraphes, paras>=60mots={long_paras}")
print(f"meta_title={len(page['meta_title'])} meta_desc={len(page['meta_description'])}")
print(f"intro={len(re.sub(r'<[^>]+>', ' ', page['intro']).split())} mots")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(page, f, ensure_ascii=False, indent=2)
print("écrit", PATH)
