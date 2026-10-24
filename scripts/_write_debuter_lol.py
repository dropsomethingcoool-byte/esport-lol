#!/usr/bin/env python3
"""Écrit content/debuter-lol.json — page evergreen « débuter League of Legends ».

Sujet 100 % evergreen : aucune donnée chiffrée susceptible de varier (prix,
tiers, notes) — rien n'est inventé, uniquement les mécaniques de base du jeu.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "content", "debuter-lol.json")

KW = "débuter league of legends"
TODAY = "2026-10-24"

page = {
    "slug": "debuter-lol",
    "type": "article",
    "title": f"Débuter League of Legends : guide du débutant",
    "meta_title": "Débuter League of Legends : guide du débutant",
    "meta_description": (
        "Comment débuter League of Legends : rôles, carte, champions faciles, "
        "rune et sorts de base, erreurs à éviter et plan de progression semaine après semaine."
    ),
    "h1": "Débuter League of Legends",
    "intro": (
        '<p class="lead">Pour <strong>débuter League of Legends</strong>, il faut accepter de ne '
        "pas tout comprendre la première semaine : la carte, les cinq rôles, les objets et la "
        "draft s'apprennent par étapes. Ce guide propose un ordre de priorité réaliste, du premier "
        "match en coopération jusqu'aux parties classées.</p>"
    ),
    "silo": "blog",
    "body": "",
    "related": [
        {"slug": "lexique-lol", "anchor": "Lexique League of Legends"},
        {"slug": "guide-champions-lol", "anchor": "Guide des champions LoL"},
        {"slug": "builds-lol", "anchor": "Guide des builds LoL"},
    ],
    "date_modified": TODAY,
    "date_published": TODAY,
    "faq": [
        {
            "question": "Quel niveau faut-il pour commencer les parties classées en LoL ?",
            "answer": (
                "Le mode classé s'ouvre une fois le compte arrivé à un certain niveau de jeu et un "
                "nombre minimal de champions possédés. L'essentiel reste de maîtriser une dizaine de "
                "champions et deux rôles avant de s'y lancer."
            ),
        },
        {
            "question": "Quel rôle choisir quand on débute League of Legends ?",
            "answer": (
                "Le support est souvent le poste le plus accessible : pas de gestion du farm, "
                "davantage de vision à poser et un impact direct sur le tireur. Le mid et le top "
                "demandent plus de rigueur dans les échanges de coups."
            ),
        },
        {
            "question": "Combien de temps faut-il pour progresser sur LoL ?",
            "answer": (
                "Compter plusieurs semaines pour comprendre la carte et les objets, et plusieurs mois "
                "pour maîtriser un rôle. La régularité pèse plus que la durée des sessions : trois "
                "parties analysées valent mieux que dix parties enchaînées."
            ),
        },
        {
            "question": "Faut-il jouer en coopération contre l'IA avant le PvP ?",
            "answer": (
                "Oui. Les parties contre l'IA permettent d'apprendre les contrôles, les sorts du "
                "champion et les achats sans pénaliser d'autres joueurs. Une poignée de parties "
                "suffit avant de passer au joueur contre joueur."
            ),
        },
    ],
    "cover": "/assets/img/covers/debuter-lol.webp",
}

B = []


def h2(t):
    B.append(f"<h2>{t}</h2>")


def h3(t):
    B.append(f"<h3>{t}</h3>")


def p(t):
    B.append(f"<p>{t}</p>")


B.append(
    '<img class="article-cover" src="/assets/img/covers/debuter-lol.webp" '
    'alt="Guide pour débuter League of Legends" loading="lazy" width="1200" height="630">'
)

# ---------------------------------------------------------------- H2 1
h2("Par où commencer pour débuter League of Legends")
h3("Les premières parties en mode coopération")
p(
    "Le mode coopération oppose cinq joueurs à cinq bots. Les parties y sont plus lentes et "
    "laissent le temps de <strong>lire</strong> les sorts de son champion, de tester les achats "
    "et de comprendre le rythme des vagues de sbires sans pression."
)
p(
    "Objectif de ces premières parties : terminer des parties complètes sans se perdre sur la "
    "carte. Le score importe peu, la <strong>mémoire</strong> des trajets entre les lignes compte "
    "beaucoup plus."
)

h3("Choisir un seul champion et le garder")
p(
    "Un débutant change souvent de champion après chaque défaite. C'est l'erreur la plus coûteuse : "
    "chaque changement réinitialise l'apprentissage des <strong>portées</strong> de sorts et des "
    "temps de recharge."
)
p(
    "Mieux vaut jouer cinq à dix parties avec le même personnage. Vous apprenez alors à reconnaître "
    "ses limites, et la <a href=\"/guide-champions-lol/\">guide des champions LoL</a> aide à "
    "comprendre à quoi sert <strong>chaque</strong> rôle dans une équipe."
)

# ---------------------------------------------------------------- H2 2
h2("Comprendre la carte et les objectifs")
h3("Les trois lignes et la jungle")
p(
    "La Faille de l'Invocateur se divise en trois lignes : top en haut, mid au milieu et bot en bas. "
    "La jungle relie ces lignes par un réseau de <strong>camps</strong> de monstres neutres que "
    "seul le jungler farm."
)
p(
    "Chaque ligne a son rythme. La mid est la plus <strong>courte</strong>, donc la plus exposée "
    "aux rotations. La bot accueille deux joueurs et concentre souvent les combats à quatre. Le "
    "<a href=\"/planning/\">calendrier des Worlds</a> montre ces rotations à l'œuvre en compétition."
)

h3("Les objectifs qui font gagner une partie")
p(
    "Détruire le Nexus adverse termine la partie, mais les objectifs neutres préparent cette "
    "victoire. Les dragons donnent des <strong>bonus</strong> permanents à toute l'équipe, et "
    "quatre d'entre eux transforment la carte."
)
p(
    "Le Baron donne un bonus temporaire qui accélère la poussée des sbires. Les tourelles, elles, "
    "ouvrent la carte : chaque tour détruite réduit la <strong>vision</strong> de l'adversaire et "
    "rapproche du Nexus."
)

# ---------------------------------------------------------------- H2 3
h2("Choisir son rôle pour ses premières parties")
h3("Le support, poste le plus accessible")
p(
    "Le support accompagne le tireur sur la bot. Il ne farm pas les sbires et consacre son or aux "
    "objets de <strong>vision</strong> et de soutien, ce qui retire une mécanique complexe de "
    "l'équation pour un débutant."
)
p(
    "Son impact passe par les balises posées dans la rivière et par les combats déclenchés au bon "
    "moment. C'est le rôle qui enseigne le plus vite la <strong>lecture</strong> de la carte."
)

h3("Le mid et le top, plus exigeants")
p(
    "Le mid dépend du farm et des rotations vers les autres lignes. Le top impose des duels longs "
    "et une gestion prudente des retours en base, sous peine de perdre plusieurs "
    "<strong>vagues</strong> de sbires."
)
p(
    "Ces deux postes restent accessibles si vous acceptez de perdre du farm au début. Le jungler, "
    "en revanche, cumule lecture de carte et gestion de <strong>tempo</strong> : il est souvent "
    "conseillé en second rôle."
)

# ---------------------------------------------------------------- H2 4
h2("Les bases à travailler avant tout le reste")
h3("Le farm des sbires")
p(
    "Le farm désigne le fait de porter le coup fatal aux sbires pour récolter de l'or. C'est la "
    "première source de revenus d'une partie, bien avant les <strong>éliminations</strong>."
)
p(
    "Un joueur qui rate une vague entière perd son or et son expérience. S'entraîner seul en "
    "partie personnalisée à atteindre un bon nombre de sbires en dix minutes reste l'exercice le "
    "plus <strong>rentable</strong>."
)

h3("La page de runes et les sorts d'invocateur")
p(
    "La page de runes modifie les statistiques du champion et se choisit avant la partie. Les "
    "<a href=\"/runes-league-of-legends/\">runes League of Legends</a> se résument, pour un "
    "débutant, à une <strong>branche</strong> principale et une secondaire."
)
p(
    "Les sorts d'invocateur sont deux boutons fixes : Flash pour se repositionner et un sort "
    "défensif ou offensif selon le rôle. Ces deux <strong>choix</strong> se gardent sur plusieurs "
    "parties pour être maîtrisés."
)

# ---------------------------------------------------------------- H2 5
h2("Apprendre les objets sans se noyer")
h3("Un build simple au départ")
p(
    "Le client propose des builds recommandés qui conviennent aux premières parties. Ils évitent "
    "de comparer des dizaines d'objets et laissent le joueur se concentrer sur ses "
    "<strong>déplacements</strong>."
)
p(
    "Le <a href=\"/builds-lol/\">guide des builds League of Legends</a> explique ensuite comment "
    "adapter cette liste à la composition adverse, notamment face à un soigneur ou à plusieurs "
    "menaces <strong>magiques</strong>."
)

h3("Les composantes avant l'objet terminé")
p(
    "Un objet terminé se construit à partir de composantes achetées progressivement. Revenir en "
    "base avec une somme modeste permet déjà d'acheter une <strong>composante</strong> utile "
    "plutôt que de garder son or inutilisé."
)
p(
    "Les objets défensifs bon marché rendent immédiatement plus solide. C'est souvent la "
    "différence entre une <strong>lane</strong> subie et une lane qui tient jusqu'au milieu de "
    "partie."
)

# ---------------------------------------------------------------- H2 6
h2("Les erreurs classiques du débutant")
h3("Poursuivre un ennemi trop loin")
p(
    "Une élimination obtenue ne justifie pas de traverser la carte sans vision. Beaucoup de "
    "défaites viennent d'une poursuite qui se termine sous une <strong>tourelle</strong> ou dans "
    "un piège tendu par le jungler adverse."
)
p(
    "La règle simple : après un échange gagné, revenir en base ou prendre un objectif proche. "
    "Chaque sort utilisé pour fuir aura ensuite couté <strong>plus</strong> qu'un sbire manqué."
)

h3("Jouer seul face à cinq")
p(
    "League of Legends reste un jeu d'équipe : engager un combat sans ses coéquipiers revient à "
    "donner une élimination gratuite. Attendre le <strong>groupe</strong> est presque toujours la "
    "bonne option."
)
p(
    "Le chat et les balises servent à ça. Un simple signal de repli évite des morts que le "
    "<strong>stress</strong> du direct ne permet pas d'anticiper seul."
)

# ---------------------------------------------------------------- H2 7
h2("Progresser sans se décourager")
h3("Analyser une partie sur trois")
p(
    "Relire toutes ses parties prend du temps et n'apprend pas grand-chose. Mieux vaut choisir "
    "une partie sur trois et identifier une seule <strong>erreur</strong> récurrente à corriger."
)
p(
    "Les replays du client suffisent pour repérer un mauvais placement ou un retour en base "
    "tardif. Cette méthode progressive donne des <strong>résultats</strong> bien plus rapides "
    "qu'un enchaînement de parties sans recul."
)

h3("Suivre la scène pour comprendre le jeu")
p(
    "Regarder les compétitions aide à voir les bons <strong>réflexes</strong> : vision posée avant "
    "un objectif, rotation après une tourelle détruite, repli coordonné. Le <a "
    "href=\"/classement/\">classement des Worlds</a> donne le contexte des affiches à suivre."
)
p(
    "Les <a href=\"/equipes/\">fiches des équipes</a> présentent les structures et leurs styles "
    "de jeu. C'est une façon de <strong>relier</strong> ce que vous voyez à l'écran à une "
    "stratégie identifiable."
)

# ---------------------------------------------------------------- H2 8
h2("Quand passer aux parties classées")
h3("Les conditions raisonnables")
p(
    "Avant le mode classé, il faut posséder un nombre suffisant de champions et maîtriser deux "
    "rôles. Jouer une seule partie par rôle dans la <strong>faille</strong> donne déjà une idée "
    "des responsabilités."
)
p(
    "Le classé ouvre un système de ligues et de points. Ce système mesure un niveau, pas la "
    "valeur d'un joueur : une série de défaites en début de saison reste <strong>normale</strong>."
)

h3("La routine qui fait monter")
p(
    "Trois parties consécutives avec un seul champion battent souvent dix parties dispersées. La "
    "mémoire musculaire du <strong>champion</strong> se construit sur la répétition, pas sur la "
    "variété."
)
p(
    "Fixez un objectif mesurable par session, comme poser des balises ou terminer les vagues avant "
    "de rejoindre le groupe. Pour le vocabulaire employé par vos coéquipiers, le <a "
    "href=\"/lexique-lol/\">lexique League of Legends</a> traduit chaque terme en <strong>action</strong> "
    "concrète."
)

page["body"] = "\n".join(B)

# ---- contrôle qualité interne (avant validate_seo.py) ---------------------
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
