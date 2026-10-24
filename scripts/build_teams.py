#!/usr/bin/env python3
"""Construit le silo « Équipes » du site esport-lol :
- 19 pages équipe (content/equipe-*.json)
- 1 hub (content/equipes.json)
- met à jour data/nav.json

Relançable sans risque (écrase les pages équipe et reconstruit le hub).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
NAV = os.path.join(ROOT, "data", "nav.json")

# code: (nom, région, seed, logo, historique, attentes)
TEAMS = [
 ("GEN", "Gen.G", "Corée du Sud · LCK", "#1 LCK",
  "https://static.lolesports.com/teams/1773829250929_GENGLOGO_GOLD.png",
  "Gen.G est l'équipe dominante de la LCK ces dernières saisons. Portée par un effectif de stars (Kiin, Canyon, Chovy, Ruler), elle a enchaîné les titres domestiques et s'impose comme la référence coréenne du moment.",
  "Tête de série numéro 1 de Corée, Gen.G arrive aux Worlds 2026 avec le statut de grand favori. L'objectif est clair : le titre mondial, rien de moins."),
 ("HLE", "Hanwha Life Esports", "Corée du Sud · LCK", "#2 LCK · champion MSI 2026",
  "https://static.lolesports.com/teams/1631819564399_hle-2021-worlds.png",
  "Hanwha Life Esports a changé de dimension en 2026 en remportant le MSI. Autour de Zeus, Kanavi, Zeka et Gumayusi, l'équipe dispose de l'un des effectifs les plus talentueux au monde.",
  "Championne du MSI, Hanwha Life est l'un des principaux prétendants au titre. Sa marge sur le haut de tableau en fait un adversaire redouté de tous."),
 ("T1", "T1", "Corée du Sud · LCK", "#3 LCK",
  "https://static.lolesports.com/teams/1726801573959_539px-T1_2019_full_allmode.png",
  "T1 est l'organisation la plus titrée de l'histoire de League of Legends, avec Faker comme capitaine emblématique. Habituée des phases finales internationales, elle reste redoutable quelle que soit sa forme en saison régulière.",
  "Troisième représentant coréen, T1 aborde les Worlds sans pression du statut de favori mais avec l'expérience et le pedigree d'un champion. Elle peut battre n'importe qui un bon jour."),
 ("DK", "Dplus Kia", "Corée du Sud · LCK", "#4 LCK",
  "https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/5/55/Dplus_Kialogo_std.png",
  "Dplus Kia, héritière de DAMWON Gaming (championne du monde 2020), reste une place forte de la LCK. Autour de ShowMaker, elle vise à retrouver les sommets après des saisons irrégulières.",
  "Quatrième seed coréen, Dplus Kia est une équipe au plafond élevé mais irrégulière. Sa capacité à passer le swiss stage dépendra de sa constance."),
 ("AL", "Anyone's Legend", "Chine · LPL", "#1 LPL",
  "https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/4/44/Anyone%27s_Legendlogo_std.png",
  "Anyone's Legend a remporté la LPL 2026 et s'affirme comme la meilleure équipe chinoise du moment. Son effectif mêle jeunes talents et joueurs confirmés.",
  "Championne de Chine, Anyone's Legend est attendue au sommet. Elle représente la plus grande menace chinoise pour les équipes coréennes."),
 ("BLG", "Bilibili Gaming", "Chine · LPL", "#2 LPL",
  "https://static.lolesports.com/teams/1682322954525_Bilibili_Gaming_logo_20211.png",
  "Bilibili Gaming est un cador de la LPL depuis plusieurs années, avec des joueurs comme Bin, Knight et Viper. Passée tout près du titre mondial par le passé, elle est rompue aux grands rendez-vous.",
  "Deuxième seed chinoise, Bilibili Gaming est un candidat sérieux au titre. Son expérience des phases finales est un atout majeur."),
 ("TES", "Top Esports", "Chine · LPL", "#3 LPL",
  "https://static.lolesports.com/teams/1592592064571_TopEsportsTES-01-FullonDark.png",
  "Top Esports est une écurie historique de la LPL, emmenée par JackeyLove. Solide collectivement, elle a souvent joué les trouble-fêtes lors des compétitions internationales.",
  "Troisième seed chinoise, Top Esports arrive avec un statut d'outsider capable de créer la surprise face aux favoris."),
 ("IG", "Invictus Gaming", "Chine · LPL", "#4 LPL",
  "https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/7/72/Invictus_Gaminglogo_std.png",
  "Invictus Gaming, championne du monde 2018, a réuni un effectif expérimenté autour de TheShy et Rookie. Son vécu des grandes scènes est un atout.",
  "Quatrième seed chinoise, Invictus Gaming mise sur l'expérience pour déjouer les pronostics. Un adversaire piégeux en swiss stage."),
 ("TL", "Team Liquid", "Amérique du Nord · LCS", "#1 LCS",
  "https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/b/bf/Team_Liquidlogo_std.png",
  "Team Liquid est l'organisation la plus titrée d'Amérique du Nord. Autour de CoreJJ et d'un noyau solide, elle domine la scène nord-américaine.",
  "Premier seed nord-américain, Team Liquid porte les espoirs de sa région. Passer le swiss stage serait déjà un bel accomplissement."),
 ("LYN", "LYON", "Amérique du Nord · LCS", "#2 LCS",
  "https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/7/78/LYON_%282024_American_Team%29logo_std.png",
  "LYON est une formation nord-américaine en progression, qui a décroché sa place aux Worlds via les playoffs LCS 2026.",
  "Deuxième seed nord-américain, LYON aborde les Worlds sans pression. Une victoire ou deux suffiraient à marquer les esprits."),
 ("G2", "G2 Esports", "EMEA · LEC", "#1 LEC",
  "https://static.lolesports.com/teams/G2-FullonDark.png",
  "G2 Esports est l'organisation européenne la plus titrée, habituée aux finales internationales. Avec BrokenBlade, Perkz et Hans Sama, elle reste la référence EMEA.",
  "Championne d'Europe, G2 vise au minimum les quarts de finale et espère retrouver une finale mondiale. Le porte-drapeau de l'EMEA."),
 ("MKOI", "Movistar KOI", "EMEA · LEC", "#2 LEC",
  "https://static.lolesports.com/teams/1734012609283_MKOI_FullColor_Blue.png",
  "Movistar KOI, née de la fusion KOI–MAD Lions, est une structure espagnole ambitieuse. Son effectif mêle talents ibériques et recrues étrangères.",
  "Deuxième seed EMEA, Movistar KOI veut confirmer son statut de dauphin européen et viser une qualification pour les phases finales."),
 ("TSW", "Team Secret Whales", "APAC · LCP", "#1 LCP",
  "https://static.lolesports.com/teams/1774598000328_White_EyeText_600p.png",
  "Team Secret Whales domine la scène vietnamienne et la LCP. Elle incarne le renouveau de l'Asie-Pacifique sur la scène internationale.",
  "Premier seed APAC, Team Secret Whales espère créer la surprise face aux grosses écuries et sortir du swiss stage."),
 ("CFO", "CTBC Flying Oyster", "APAC · LCP", "#2 LCP",
  "https://static.lolesports.com/teams/1656307849320_CFO_Logo.png",
  "CTBC Flying Oyster est une formation taïwanaise régulière de la LCP, souvent présente aux compétitions internationales.",
  "Deuxième seed APAC, CTBC Flying Oyster part avec un statut d'outsider. Chaque victoire en swiss stage sera une performance."),
 ("LOS", "Los Grandes", "Brésil · CBLOL", "#1 CBLOL",
  "https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/3/3c/L%C3%98Slogo_std.png",
  "Los Grandes a remporté le CBLOL 2026 et représente la meilleure équipe brésilienne. Elle porte les espoirs de la scène sud-américaine.",
  "Premier seed brésilien, Los Grandes vise à exister face aux cadors et à offrir une belle histoire à sa région."),
 ("C9", "Cloud9 Kia", "Amérique du Nord · LCS", "#3 LCS · play-in",
  "https://static.lolesports.com/teams/1736924120254_C9Kia_IconBlue_Transparent_2000x2000.png",
  "Cloud9 est une organisation emblématique nord-américaine, présente au plus haut niveau depuis des années. Elle passe par le play-in cette année.",
  "Cloud9 Kia doit d'abord sortir du play-in pour rejoindre le swiss stage. Une fois qualifiée, elle peut jouer les trouble-fêtes."),
 ("KC", "Karmine Corp", "EMEA · LEC", "#3 LEC · play-in",
  "https://static.lolesports.com/teams/1704714951336_KC.png",
  "Karmine Corp est l'organisation française au plus grand public d'Europe. Portée par une communauté passionnée, elle dispute le play-in des Worlds 2026.",
  "Karmine Corp vise la qualification pour le swiss stage, puis une belle campagne. Son public et son agressivité en font un adversaire à part."),
 ("MVK", "MVK Esports", "APAC · LCP", "#3 LCP · play-in",
  "https://static.lolesports.com/teams/1767089709161_White_Logo.png",
  "MVK Esports est une formation vietnamienne issue de la scène de la LCP. Elle décroche sa place aux Worlds via le play-in.",
  "MVK Esports doit passer le play-in pour rejoindre le swiss stage. Une qualification serait déjà un succès pour la structure."),
 ("FUR", "FURIA", "Brésil · CBLOL", "#2 CBLOL · play-in",
  "https://static.lolesports.com/teams/FURIA---black.png",
  "FURIA est une organisation brésilienne reconnue, présente dans plusieurs esports. Sa section League of Legends dispute le play-in des Worlds 2026.",
  "FURIA doit sortir du play-in pour rejoindre le swiss stage. Une qualification marquerait un jalon pour l'organisation."),
]

REGIONS_ORDER = [
    ("Corée du Sud · LCK", "Corée du Sud (LCK)"),
    ("Chine · LPL", "Chine (LPL)"),
    ("EMEA · LEC", "EMEA (LEC)"),
    ("Amérique du Nord · LCS", "Amérique du Nord (LCS)"),
    ("APAC · LCP", "APAC (LCP)"),
    ("Brésil · CBLOL", "Brésil (CBLOL)"),
]

def slugify(name):
    s = name.lower().replace("ø", "o").replace("'", "").replace("&", "and")
    s = "".join(c if c.isalnum() else "-" for c in s)
    return "-".join([p for p in s.split("-") if p])


def build_team_page(code, name, region, seed, logo, history, expect):
    slug = "equipe-" + slugify(name)
    title = f"{name} — Équipe Worlds 2026"
    meta_title = f"{name} : effectif, historique et attentes aux Worlds 2026"
    meta_description = f"Fiche équipe {name} aux Worlds 2026 : {region}, seed {seed.split(' ·')[0]}. Historique, effectif et attentes pour la compétition."
    h1 = name
    intro = (f'<p class="lead"><strong>{name}</strong> représente la {region.lower().replace(" · lck","").replace(" · lpl","").replace(" · lec","").replace(" · lcs","").replace(" · lcp","").replace(" · cblol","")} aux <strong>Worlds 2026</strong> (seed {seed.split(" · ")[0]}).</p>')
    hero = (f'<div class="team-hero"><img class="team-logo" src="{logo}" alt="Logo {name}" loading="lazy">'
            f'<div class="team-hero-meta"><span class="team-region">{region}</span>'
            f'<span class="team-seed">Seed : {seed}</span></div></div>')
    body = hero + f'<h2>Historique</h2><p>{history}</p><h2>Attentes pour les Worlds 2026</h2><p>{expect}</p>'
    related = [
        {"slug": "equipes", "anchor": "toutes les équipes des Worlds"},
        {"slug": "planning", "anchor": "planning des Worlds"},
        {"slug": "blog", "anchor": "résumés de matchs Worlds"},
    ]
    return {
        "slug": slug, "type": "article", "silo": "equipes",
        "code": code, "region": region, "seed": seed, "logo": logo,
        "title": title, "meta_title": meta_title, "meta_description": meta_description,
        "h1": h1, "intro": intro, "body": body, "related": related,
        "date_modified": "2026-10-16", "date_published": "2026-10-16",
    }


def build_hub():
    sections = []
    for region_key, region_label in REGIONS_ORDER:
        tiles = []
        for code, name, region, seed, logo, history, expect in TEAMS:
            if region == region_key:
                slug = "equipe-" + slugify(name)
                tiles.append(
                    f'<a class="team-tile" href="/{slug}/"><img src="{logo}" alt="{name}" loading="lazy">'
                    f'<span><span class="tt-name">{name}</span><br><span class="tt-region">{seed}</span></span></a>'
                )
        sections.append(f'<div class="team-section-title">{region_label}</div><div class="teams-grid">{"".join(tiles)}</div>')

    body = ("<p>Les <strong>19 équipes</strong> des Worlds 2026, des favorites du swiss stage aux "
            "formations issues du play-in. Cliquez sur une équipe pour découvrir son historique et ses "
            "attentes pour cette édition.</p>" + "".join(sections))
    return {
        "slug": "equipes", "type": "hub", "silo": "equipes",
        "title": "Équipes des Worlds 2026 — League of Legends",
        "meta_title": "Équipes des Worlds 2026 | esport-lol",
        "meta_description": "Toutes les équipes des Worlds League of Legends 2026 : effectifs, historiques et attentes. Du swiss stage au play-in.",
        "h1": "Équipes des Worlds 2026",
        "intro": '<p class="lead">Les <strong>équipes des Worlds 2026</strong>, de la Corée au Brésil : historiques, effectifs et attentes.</p>',
        "body": body,
        "date_modified": "2026-10-16", "date_published": "2026-10-16",
    }


def update_nav():
    nav = json.load(open(NAV, encoding="utf-8"))
    if not any(s.get("slug") == "equipes" for s in nav.get("silos", [])):
        nav["silos"].insert(1, {"label": "Équipes", "slug": "equipes", "pages": []})
    with open(NAV, "w", encoding="utf-8") as f:
        json.dump(nav, f, ensure_ascii=False, indent=2)
    print("✓ nav.json mis à jour (silo Équipes ajouté)")


def main():
    for code, name, region, seed, logo, history, expect in TEAMS:
        page = build_team_page(code, name, region, seed, logo, history, expect)
        with open(os.path.join(CONTENT, page["slug"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(page, f, ensure_ascii=False, indent=2)
    print(f"✓ {len(TEAMS)} pages équipe créées")

    hub = build_hub()
    with open(os.path.join(CONTENT, "equipes.json"), "w", encoding="utf-8") as f:
        json.dump(hub, f, ensure_ascii=False, indent=2)
    print("✓ hub equipes.json créé")

    update_nav()


if __name__ == "__main__":
    main()
