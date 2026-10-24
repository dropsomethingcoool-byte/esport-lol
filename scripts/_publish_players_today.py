#!/usr/bin/env python3
"""Publie les 2 premières fiches joueurs (Faker, Caliste) + maillage + nav.
Idempotent : n'écrase pas une fiche déjà présente, n'injecte pas un lien en double."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")
NAV = os.path.join(ROOT, "data", "nav.json")

PLAYERS = [
    {
        "slug": "joueur-faker",
        "pseudo": "Faker",
        "role": "Midlane",
        "country": "Corée du Sud",
        "team_code": "T1",
        "team_name": "T1",
        "team_slug": "equipe-t1",
        "title": "Faker — Joueur League of Legends (T1)",
        "meta_title": "Faker : le midlaner légendaire de T1 | esport-lol",
        "meta_description": "Faker, quintuple champion du monde de League of Legends. Profil, palmarès, style de jeu et son parcours aux Worlds 2026 avec T1.",
        "h1": "Faker",
        "intro": '<p class="lead">Faker est le <strong>midlaner</strong> légendaire de T1 et le quintuple champion du monde de League of Legends. Palmarès, style de jeu et rôle aux Worlds 2026.</p>',
        "body": (
            '<h2>Profil de Faker</h2>'
            '<h3>Le midlaner légendaire de T1</h3>'
            '<p>Faker évolue au poste de <strong>midlane</strong> au sein de T1, l\'organisation qu\'il représente sans interruption depuis 2013. Le joueur sud-coréen est considéré comme le plus grand de l\'histoire de League of Legends.</p>'
            '<p>Sa <strong>longévité</strong> au plus haut niveau est sans équivalent. Là où la plupart des champions déclinent, Faker a su se réinventer pour rester compétitif saison après saison.</p>'
            '<h3>Un palmarès hors norme</h3>'
            '<p>Faker est le seul joueur à avoir remporté les Worlds à <strong>cinq reprises</strong>, en 2013, 2015, 2016, 2023 et 2024. Un record que personne n\'a jamais approché.</p>'
            '<p>À ces titres mondiaux s\'ajoutent de nombreux sacres en <strong>LCK</strong> et deux victoires au Mid-Season Invitational. Son armoire à trophées est la plus fournie de la discipline.</p>'
            '<h2>Son style de jeu</h2>'
            '<h3>Une mécanique d\'exception</h3>'
            '<p>Faker est réputé pour sa <strong>mécanique</strong> irréprochable, même après plus d\'une décennie de carrière. Ses réflexes et sa précision restent la référence absolue au poste de midlaner.</p>'
            '<p>Il excelle sur des champions exigeants comme <strong>Azir</strong>, Ryze ou Orianna. Sa capacité à renverser un teamfight sur une action individuelle est sa signature.</p>'
            '<h3>Un stratège et un leader</h3>'
            '<p>Au-delà de la mécanique, Faker est un <strong>leader</strong> naturel qui structure tout le jeu de son équipe. Sa prise de décision influence l\'ensemble de la carte.</p>'
            '<p>Sa lecture du jeu lui permet d\'<strong>anticiper</strong> les rotations adverses et de sécuriser les objectifs. C\'est ce sens stratégique qui le rend si difficile à contrer.</p>'
            '<h2>Sa carrière en dates</h2>'
            '<h3>Des débuts fracassants</h3>'
            '<p>Faker fait ses débuts professionnels en <strong>2013</strong> sous les couleurs de SK Telecom T1. Dès sa première saison, il remporte les Worlds avec un niveau jamais vu auparavant.</p>'
            '<p>Ce titre inaugural pose les bases d\'une <strong>dynastie</strong>. T1 devient rapidement l\'organisation la plus titrée de l\'histoire de League of Legends.</p>'
            '<h3>Le retour au sommet</h3>'
            '<p>Après une longue traversée du désert, Faker remporte de nouveau les Worlds en <strong>2023</strong>, puis conserve le titre en 2024. Un retour triomphal qui a marqué toute une génération.</p>'
            '<p>Ces deux sacres consécutifs ont <strong>consacré</strong> définitivement son statut de légende absolue de la discipline.</p>'
            '<h2>Faker aux Worlds 2026</h2>'
            '<h3>Un nouveau défi avec T1</h3>'
            '<p>T1 aborde les Worlds 2026 avec le statut de <strong>troisième</strong> représentant de la LCK. Faker guide une équipe qui ne part pas favorite mais reste redoutable à tout moment.</p>'
            '<p>Retrouvez l\'historique et les attentes de T1 sur la <a href="/equipe-t1/">fiche équipe de T1</a>, ainsi que le détail de son parcours dans ce tournoi.</p>'
            '<h3>Les stars de cette édition</h3>'
            '<p>Faker croisera peut-être la route des autres grands noms de la compétition. Consultez notre sélection des <a href="/joueurs-a-suivre-worlds-2026/">joueurs à suivre aux Worlds 2026</a>.</p>'
            '<p>Des joueurs comme <strong>Chovy</strong> ou ShowMaker rêvent de faire tomber la légende. Le swiss stage promet des duels de très haut niveau.</p>'
            '<h2>Les champions signature de Faker</h2>'
            '<h3>Azir, l\'arme absolue</h3>'
            '<p>Azir est sans doute le champion le plus <strong>emblématique</strong> de Faker. Son « Shuffle de l\'empereur » a produit certains des plus grands moments de l\'histoire des Worlds.</p>'
            '<p>Maîtriser Azir exige une <strong>précision</strong> chirurgicale, que Faker démontre à chacune de ses sorties sur le champion.</p>'
            '<h3>Ryze et Orianna, les classiques</h3>'
            '<p>Ryze est historiquement associé à Faker, qui l\'a porté lors de ses plus grands <strong>succès</strong>. Le champion et le joueur sont devenus indissociables.</p>'
            '<p>Orianna complète un trio de <strong>mages</strong> qui définit son style de contrôle de la midlane depuis plus de dix ans.</p>'
        ),
        "related": [
            {"slug": "joueurs", "anchor": "Tous les joueurs des Worlds"},
            {"slug": "equipe-t1", "anchor": "Fiche équipe T1"},
            {"slug": "joueurs-a-suivre-worlds-2026", "anchor": "Joueurs à suivre aux Worlds 2026"},
            {"slug": "joueur-caliste", "anchor": "Caliste, le prodige français"},
        ],
    },
    {
        "slug": "joueur-caliste",
        "pseudo": "Caliste",
        "role": "ADC",
        "country": "France",
        "team_code": "KC",
        "team_name": "Karmine Corp",
        "team_slug": "equipe-karmine-corp",
        "title": "Caliste — Joueur League of Legends (Karmine Corp)",
        "meta_title": "Caliste : le prodige français de la KC | esport-lol",
        "meta_description": "Caliste, jeune ADC français de la Karmine Corp. Parcours, style de jeu et sa première grande scène internationale aux Worlds 2026.",
        "h1": "Caliste",
        "intro": '<p class="lead">Caliste est le <strong>prodige</strong> français de la Karmine Corp, titulaire au poste d\'ADC. Découvrez son parcours et son rôle aux Worlds 2026.</p>',
        "body": (
            '<h2>Profil de Caliste</h2>'
            '<h3>Le prodige français de la Karmine Corp</h3>'
            '<p>Caliste évolue au poste d\'<strong>ADC</strong> au sein de la Karmine Corp. Le jeune Français est l\'un des talents les plus scrutés de la scène européenne.</p>'
            '<p>Sa <strong>progression</strong> fulgurante, de l\'académie à l\'équipe première, a fait de lui le visage de la nouvelle génération tricolore.</p>'
            '<h3>Un parcours formé à la maison</h3>'
            '<p>Caliste a été formé au sein de la <strong>Karmine Corp Blue</strong>, la structure académique du club. Il y a fait ses armes avant de rejoindre l\'effectif de la LEC.</p>'
            '<p>Cette formation interne lui a permis de <strong>s\'imposer</strong> progressivement comme le titulaire du poste d\'ADC de l\'équipe fanion.</p>'
            '<h2>Son style de jeu</h2>'
            '<h3>Un ADC agressif et créatif</h3>'
            '<p>Caliste se distingue par un style <strong>agressif</strong> et spectaculaire. Il n\'hésite pas à prendre des risques pour créer des avantages en lane.</p>'
            '<p>Sa <strong>créativité</strong> et sa mécanique en font un tireur capable de renverser une partie sur une seule action individuelle.</p>'
            '<h3>Un joueur sous les projecteurs</h3>'
            '<p>Porté par l\'immense communauté de la Karmine Corp, Caliste évolue sous une <strong>pression</strong> médiatique rare en Europe. Un défi qu\'il semble gérer avec maturité.</p>'
            '<p>Chacune de ses performances est <strong>scrutée</strong> par des milliers de supporters français. Cette exposition a contribué à forger son mental.</p>'
            '<h2>Sa carrière</h2>'
            '<h3>De l\'académie à la LEC</h3>'
            '<p>Le parcours de Caliste illustre le <strong>modèle</strong> de formation de la Karmine Corp. Il a gravi tous les échelons avant de briller au plus haut niveau.</p>'
            '<p>Son ascension rapide a fait de lui l\'un des <strong>espoirs</strong> les plus prometteurs du poste d\'ADC en Europe.</p>'
            '<h3>La reconnaissance du public</h3>'
            '<p>Caliste est rapidement devenu l\'un des joueurs les plus <strong>populaires</strong> de la communauté française de League of Legends.</p>'
            '<p>Son charisme et son jeu spectaculaire ont séduit un public qui voit en lui le <strong>futur</strong> de l\'esport tricolore.</p>'
            '<h2>Caliste aux Worlds 2026</h2>'
            '<h3>Une première grande scène</h3>'
            '<p>Les Worlds 2026 représentent la première grande <strong>scène</strong> internationale de Caliste. Une occasion de se mesurer aux meilleurs ADC du monde.</p>'
            '<p>Retrouvez le parcours de la Karmine Corp sur la <a href="/equipe-karmine-corp/">fiche équipe de la Karmine Corp</a>.</p>'
            '<h3>Les joueurs à suivre</h3>'
            '<p>Caliste figure logiquement dans notre sélection des <a href="/joueurs-a-suivre-worlds-2026/">joueurs à suivre aux Worlds 2026</a>.</p>'
            '<p>Il y côtoie d\'autres <strong>stars</strong> françaises comme Hans Sama, ainsi que les légendes du circuit.</p>'
            '<h2>Les champions signature de Caliste</h2>'
            '<h3>Les tireurs de la meta</h3>'
            '<p>Caliste s\'illustre sur les ADC de la <strong>meta</strong> actuelle, des hyper-carry aux tireurs plus utilitaires selon le patch du tournoi.</p>'
            '<p>Sa capacité d\'<strong>adaptation</strong> aux changements de patch sera un atout précieux pour la Karmine Corp.</p>'
            '<h3>Un style spectaculaire</h3>'
            '<p>Le Français est réputé pour ses <strong>outplays</strong> et ses mécaniques de grande classe en phase de lane.</p>'
            '<p>Ces actions d\'éclat nourrissent sa <strong>réputation</strong> et celle de son équipe auprès du public.</p>'
        ),
        "related": [
            {"slug": "joueurs", "anchor": "Tous les joueurs des Worlds"},
            {"slug": "equipe-karmine-corp", "anchor": "Fiche équipe Karmine Corp"},
            {"slug": "joueurs-a-suivre-worlds-2026", "anchor": "Joueurs à suivre aux Worlds 2026"},
            {"slug": "joueur-faker", "anchor": "Faker, la légende de T1"},
        ],
    },
]


def write_players():
    for p in PLAYERS:
        path = os.path.join(CONTENT, p["slug"] + ".json")
        if os.path.exists(path):
            print("·", p["slug"], "déjà présent (skip)")
            continue
        page = {
            "slug": p["slug"],
            "type": "article",
            "silo": "joueurs",
            "pseudo": p["pseudo"],
            "role": p["role"],
            "country": p["country"],
            "team_code": p["team_code"],
            "team_name": p["team_name"],
            "team_slug": p["team_slug"],
            "title": p["title"],
            "meta_title": p["meta_title"],
            "meta_description": p["meta_description"],
            "h1": p["h1"],
            "intro": p["intro"],
            "body": p["body"],
            "related": p["related"],
            "date_modified": "2026-10-24",
            "date_published": "2026-10-24",
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(page, f, ensure_ascii=False, indent=2)
        print("✓", p["slug"] + ".json")


def link_pilier():
    """Ajoute les liens Faker/Caliste dans l'article pilier."""
    p = os.path.join(CONTENT, "joueurs-a-suivre-worlds-2026.json")
    with open(p, encoding="utf-8") as f:
        b = json.load(f)
    body = b["body"]
    changed = False
    # Faker -> /joueur-faker/
    if "/joueur-faker/" not in body:
        body = body.replace(
            "Faker reste la plus grande légende de <strong>League of Legends</strong>",
            '<a href="/joueur-faker/">Faker</a> reste la plus grande légende de <strong>League of Legends</strong>',
            1,
        )
        changed = True
    # Caliste -> /joueur-caliste/
    if "/joueur-caliste/" not in body:
        body = body.replace(
            "<p>Caliste incarne la nouvelle génération <strong>française</strong>",
            '<p><a href="/joueur-caliste/">Caliste</a> incarne la nouvelle génération <strong>française</strong>',
            1,
        )
        changed = True
    if changed:
        b["body"] = body
        with open(p, "w", encoding="utf-8") as f:
            json.dump(b, f, ensure_ascii=False, indent=2)
        print("✓ pilier : liens Faker + Caliste injectés")
    else:
        print("· pilier : liens déjà présents")


def link_teams():
    """Ajoute les joueurs au related des fiches équipe."""
    mapping = {"equipe-t1": "joueur-faker", "equipe-karmine-corp": "joueur-caliste"}
    anchors = {"equipe-t1": "Faker, le midlaner de T1", "equipe-karmine-corp": "Caliste, l'ADC de la KC"}
    for team_slug, player_slug in mapping.items():
        p = os.path.join(CONTENT, team_slug + ".json")
        with open(p, encoding="utf-8") as f:
            b = json.load(f)
        rel = b.get("related", [])
        if any(r.get("slug") == player_slug for r in rel):
            print("·", team_slug, "déjà lié")
            continue
        rel.insert(1, {"slug": player_slug, "anchor": anchors[team_slug]})
        b["related"] = rel
        with open(p, "w", encoding="utf-8") as f:
            json.dump(b, f, ensure_ascii=False, indent=2)
        print("✓", team_slug, "→", player_slug)


def add_nav():
    with open(NAV, encoding="utf-8") as f:
        nav = json.load(f)
    if any(s.get("slug") == "joueurs" for s in nav.get("silos", [])):
        print("· nav : silo Joueurs déjà présent")
        return
    silos = nav["silos"]
    # insérer après « Équipes »
    for i, s in enumerate(silos):
        if s.get("slug") == "equipes":
            silos.insert(i + 1, {"label": "Joueurs", "slug": "joueurs", "pages": []})
            break
    else:
        silos.append({"label": "Joueurs", "slug": "joueurs", "pages": []})
    with open(NAV, "w", encoding="utf-8") as f:
        json.dump(nav, f, ensure_ascii=False, indent=2)
    print("✓ nav.json : silo Joueurs ajouté")


write_players()
link_pilier()
link_teams()
add_nav()
print("\nTerminé.")
