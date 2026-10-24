#!/usr/bin/env python3
"""Construit l'article pilier « joueurs-a-suivre-worlds-2026 » + maillage interne.
Idempotent : n'injecte un lien que s'il n'est pas déjà présent."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

SLUG = "joueurs-a-suivre-worlds-2026"
URL = f"/{SLUG}/"

BODY = (
    '<img class="article-cover" src="/assets/img/covers/' + SLUG + '.webp" '
    'alt="Les joueurs à suivre aux Worlds 2026" loading="lazy" width="1200" height="630">'
    '<h2>Les stars attendues des Worlds 2026</h2>'
    '<h3>Faker, le quintuple champion du monde</h3>'
    '<p>Faker reste la plus grande légende de <strong>League of Legends</strong>. '
    'Avec cinq titres mondiaux, le capitaine de <a href="/equipe-t1/">T1</a> aborde chaque '
    'édition des Worlds en candidat naturel au sacre.</p>'
    '<p>Son <strong>leadership</strong> et sa science du jeu font encore la différence dans '
    'les moments décisifs. Suivre Faker, c\'est suivre l\'histoire vivante de la discipline.</p>'
    '<h3>Chovy et Ruler, le duo de Gen.G</h3>'
    '<p>Chovy est considéré comme la meilleure <strong>midlane</strong> du monde. Sa régularité '
    'mécanique et sa gestion de la vague en font le joueur le plus craint de la LCK.</p>'
    '<p>À ses côtés, Ruler apporte l\'expérience d\'un <strong>champion du monde 2017</strong>. '
    'Le tireur de <a href="/equipe-gen-g/">Gen.G</a> a déjà prouvé qu\'il savait porter une '
    'équipe jusqu\'au titre suprême.</p>'
    '<h3>Zeus et Gumayusi, les doubles champions</h3>'
    '<p>Zeus et Gumayusi ont remporté les Worlds <strong>2023 et 2024</strong> sous les couleurs '
    'de T1. Désormais chez Hanwha Life Esports, ils forment l\'un des duos les plus dangereux du tournoi.</p>'
    '<p>Zeus a été élu MVP de la finale 2023 grâce à sa <strong>toplane</strong> agressive. '
    'Gumayusi reste l\'un des tireurs les plus fiables en phase décisive.</p>'
    '<h2>Les Français à suivre de près</h2>'
    '<h3>Hans Sama, l\'expérience au service de G2</h3>'
    '<p>Hans Sama est l\'un des joueurs <strong>français</strong> les plus capés de la scène '
    'internationale. L\'ADC de <a href="/equipe-g2-esports/">G2 Esports</a> allie mécanique de '
    'haut niveau et sang-froid en équipe.</p>'
    '<p>Porté par l\'ambition de G2, il vise enfin une <strong>finale mondiale</strong> après '
    'plusieurs parcours frustrants. Sa régularité sera précieuse tout au long du swiss stage.</p>'
    '<h3>Caliste, la pépite de la Karmine Corp</h3>'
    '<p>Caliste incarne la nouvelle génération <strong>française</strong>. Formé à l\'académie de la '
    '<a href="/equipe-karmine-corp/">Karmine Corp</a>, il a gravi les échelons jusqu\'au poste de titulaire en ADC.</p>'
    '<p>Sa créativité et son agressivité en font un joueur <strong>imprévisible</strong> et '
    'spectaculaire. Pour sa première grande scène, tous les regards français se tournent vers lui.</p>'
    '<h2>Les outsiders capables de surprendre</h2>'
    '<h3>ShowMaker, l\'âme de Dplus Kia</h3>'
    '<p>ShowMaker a marqué l\'histoire en offrant à DAMWON Gaming le titre de <strong>champion '
    'du monde 2020</strong>. Le midlaner coréen reste l\'un des créateurs de jeu les plus redoutés.</p>'
    '<p>Dplus Kia arrive avec un statut <strong>d\'outsider</strong>, mais ShowMaker a déjà prouvé '
    'qu\'il pouvait porter une équipe bien au-delà des pronostics.</p>'
    '<h3>Bin et Knight, la force de frappe de Bilibili</h3>'
    '<p>Bin a disputé les finales mondiales <strong>2023 et 2024</strong> avec Bilibili Gaming. Le '
    'toplaner chinois est réputé pour ses initiations décisives et sa confiance sans limite.</p>'
    '<p>Knight, MVP de la LPL, complète un duo <strong>redoutable</strong>. Leurs performances '
    'individuelles décident souvent du sort des rencontres de BLG.</p>'
    '<h3>TheShy et Rookie, les vétérans d\'Invictus Gaming</h3>'
    '<p>TheShy et Rookie ont soulevé le trophée des Worlds en <strong>2018</strong> avec Invictus '
    'Gaming. Leur association reste l\'une des plus iconiques de l\'histoire chinoise.</p>'
    '<p>Redevenus coéquipiers, ils apportent une <strong>expérience</strong> inestimable à une '
    'équipe qui joue sans pression. Un adversaire piégeux pour n\'importe quel favori.</p>'
    '<h2>Les autres stars à surveiller</h2>'
    '<h3>JackeyLove, l\'instinct de Top Esports</h3>'
    '<p>JackeyLove a remporté les Worlds en <strong>2018</strong> avec Invictus Gaming, à tout juste 17 ans. '
    'L\'ADC de Top Esports reste l\'un des tireurs les plus imprévisibles de la scène chinoise.</p>'
    '<p>Son agressivité naturelle peut faire basculer une manche comme <strong>coûter cher</strong> à son équipe. '
    'Top Esports compte sur lui pour renverser les favoris du swiss stage.</p>'
    '<h3>Viper, le champion du monde 2021</h3>'
    '<p>Viper a décroché le titre mondial en <strong>2021</strong> avec Edward Gaming, au terme d\'une finale historique. '
    'L\'ADC de Bilibili Gaming a depuis confirmé sa place parmi les tout meilleurs.</p>'
    '<p>Sa lecture des teamfights et sa <strong>position</strong> irréprochable en font un facteur X dans chaque série. '
    'Un atout majeur pour les ambitions de BLG.</p>'
    '<h3>CoreJJ, la science du jeu de Team Liquid</h3>'
    '<p>CoreJJ a remporté les Worlds en <strong>2017</strong> avec Samsung Galaxy avant de s\'imposer en Amérique du Nord. '
    'Le support de Team Liquid est l\'un des cerveaux les plus respectés du circuit.</p>'
    '<p>Son <strong>leadership</strong> et sa vision de jeu structurent tout le plan de son équipe. '
    'Team Liquid comptera sur lui pour exister face aux cadors coréens et chinois.</p>'
    '<h3>BrokenBlade, la polyvalence de G2</h3>'
    '<p>BrokenBlade est l\'un des toplaners les plus <strong>polyvalents</strong> d\'Europe. '
    'Sa capacité à jouer une large gamme de champions complique la préparation des adversaires de G2 Esports.</p>'
    '<p>Avec Hans Sama, il forme un duo de couloir <strong>redouté</strong> à l\'international. '
    'G2 misera sur son expérience pour viser une place en phase finale.</p>'
    '<h2>Comment suivre ces joueurs en direct</h2>'
    '<h3>Le planning et les résultats des matchs</h3>'
    '<p>Pour ne rien manquer des performances de ces <strong>stars</strong>, consultez le '
    '<a href="/planning/">planning des matchs des Worlds</a>. Tous les horaires sont affichés en heure de Paris.</p>'
    '<p>Les <a href="/resultats/">résultats des Worlds LoL</a> sont mis à jour au fil des '
    'rencontres. Chaque victoire ou défaite influence directement le <strong>parcours</strong> de ces joueurs.</p>'
    '<h3>Le classement du swiss stage</h3>'
    '<p>Le <a href="/classement/">classement du swiss stage</a> permet de suivre la position de '
    'chaque équipe. Il faut engranger trois <strong>victoires</strong> pour se qualifier en phase finale.</p>'
    '<p>Retrouvez aussi les <a href="/equipes/">fiches des 19 équipes des Worlds</a>. Elles '
    'détaillent le <strong>contexte</strong> de chaque formation et son parcours dans la compétition.</p>'
)

page = {
    "slug": SLUG,
    "type": "article",
    "silo": "blog",
    "title": "Joueurs à suivre aux Worlds 2026 — League of Legends",
    "meta_title": "Joueurs à suivre aux Worlds LoL 2026 | esport-lol",
    "meta_description": "Faker, Chovy, Hans Sama, Caliste : les joueurs à suivre aux Worlds 2026. Stars, Français et outsiders du tournoi, équipe par équipe.",
    "h1": "Joueurs à suivre aux Worlds 2026",
    "intro": '<p class="lead">Les <strong>joueurs à suivre</strong> aux Worlds 2026 : Faker, Chovy, Hans Sama, Caliste et les autres stars du tournoi, rôle par rôle et équipe par équipe.</p>',
    "body": BODY,
    "related": [
        {"slug": "equipes", "anchor": "Toutes les équipes des Worlds LoL"},
        {"slug": "planning", "anchor": "Planning des Worlds LoL 2026"},
        {"slug": "classement", "anchor": "Classement des Worlds LoL 2026"},
        {"slug": "blog", "anchor": "Blog League of Legends"},
    ],
    "date_modified": "2026-10-24",
    "date_published": "2026-10-24",
    "cover": "/assets/img/covers/" + SLUG + ".webp",
}

# --- 1) écrire l'article ---
with open(os.path.join(CONTENT, SLUG + ".json"), "w", encoding="utf-8") as f:
    json.dump(page, f, ensure_ascii=False, indent=2)
print("✓ article", SLUG + ".json")

# --- 2) blog.json : insérer dans « Actualités » ---
def edit_blog():
    p = os.path.join(CONTENT, "blog.json")
    with open(p, encoding="utf-8") as f:
        b = json.load(f)
    body = b["body"]
    if SLUG in body:
        print("· blog.json : déjà présent")
        return
    marker = "<h2>Actualités</h2>"
    new = (marker + '<p><a href="' + URL + '">Les joueurs à suivre aux Worlds 2026</a>'
           ' — Faker, Chovy, Hans Sama, Caliste et les autres <strong>stars</strong>.</p>')
    b["body"] = body.replace(marker, new, 1)
    b["date_modified"] = "2026-10-24"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(b, f, ensure_ascii=False, indent=2)
    print("✓ blog.json : lien injecté (Actualités)")

# --- 3) equipes.json : lien contextuel ---
def edit_equipes():
    p = os.path.join(CONTENT, "equipes.json")
    with open(p, encoding="utf-8") as f:
        b = json.load(f)
    body = b["body"]
    if SLUG in body:
        print("· equipes.json : déjà présent")
        return
    anchor = 'Cliquez sur une équipe pour découvrir son historique et ses '
    idx = body.find(anchor)
    # injecter juste après la fin du <p> d'intro
    end_p = body.find("</p>", idx)
    new = ('<p>Retrouvez aussi les <a href="' + URL + '">joueurs à suivre aux Worlds 2026</a> : '
           'les <strong>stars</strong> et les Français à surveiller tout au long du tournoi.</p>')
    b["body"] = body[:end_p + 4] + new + body[end_p + 4:]
    b["date_modified"] = "2026-10-24"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(b, f, ensure_ascii=False, indent=2)
    print("✓ equipes.json : lien injecté")

# --- 4) planning.json : lien contextuel ---
def edit_planning():
    p = os.path.join(CONTENT, "planning.json")
    with open(p, encoding="utf-8") as f:
        b = json.load(f)
    body = b["body"]
    if SLUG in body:
        print("· planning.json : déjà présent")
        return
    anchor = 'page dédiée au play-in</a>.</p>'
    new = ('<p>Retrouvez aussi les <a href="' + URL + '">joueurs à suivre aux Worlds 2026</a>, '
           '<strong>stars</strong> et outsiders du swiss stage.</p>')
    b["body"] = body.replace(anchor, anchor + new, 1)
    b["date_modified"] = "2026-10-24"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(b, f, ensure_ascii=False, indent=2)
    print("✓ planning.json : lien injecté")

# --- 5) pronostics-worlds-lol.json : ajouter au related ---
def edit_pronostics():
    p = os.path.join(CONTENT, "pronostics-worlds-lol.json")
    with open(p, encoding="utf-8") as f:
        b = json.load(f)
    rel = b.get("related", [])
    if any(r.get("slug") == SLUG for r in rel):
        print("· pronostics : déjà présent")
        return
    rel.insert(1, {"slug": SLUG, "anchor": "Joueurs à suivre aux Worlds LoL"})
    b["related"] = rel
    b["date_modified"] = "2026-10-24"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(b, f, ensure_ascii=False, indent=2)
    print("✓ pronostics-worlds-lol.json : related ajouté")

edit_blog()
edit_equipes()
edit_planning()
edit_pronostics()
print("\nTerminé.")
