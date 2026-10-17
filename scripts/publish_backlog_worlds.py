#!/usr/bin/env python3
"""P6 — publication des pages backlog « Worlds » : format-worlds-lol + meilleurs-champions-worlds.
(equipes-worlds-lol est déjà couvert par /equipes/ → retiré du backlog sans nouvelle page.)"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026-10-17"

pages = [
    {
        "slug": "format-worlds-lol",
        "type": "article",
        "title": "Format des Worlds — League of Legends",
        "meta_title": "Format des Worlds LoL 2026 : phases et règles | esport-lol",
        "meta_description": "Le format des Worlds League of Legends 2026 : play-ins, système suisse et phase finale. Les règles de qualification et les dates, expliquées simplement.",
        "h1": "Format des Worlds LoL 2026",
        "intro": '<p class="lead">Le <strong>format des Worlds</strong> League of Legends 2026 se joue en trois phases : les play-ins, le système suisse et la phase finale éliminatoire.</p>',
        "body": (
            '<h2>Les trois phases du format des Worlds</h2>'
            '<h3>Les play-ins, la porte d\'entrée</h3>'
            '<p>Le <strong>play-in des Worlds</strong> ouvre la compétition du 15 au 18 octobre 2026. Les équipes concernées jouent leurs premiers matchs pour décrocher une place au tour suivant.</p>'
            '<p>Cette phase sert de <strong>tremplin vers le système suisse</strong>. Les vainqueurs rejoignent les équipes déjà qualifiées pour la suite du tournoi.</p>'
            '<h3>Le système suisse, du 23 au 31 octobre</h3>'
            '<p>Le <strong>système suisse des Worlds</strong> oppose seize équipes à partir du 23 octobre. Chaque équipe enchaîne des rondes jusqu\'à atteindre trois victoires ou trois défaites.</p>'
            '<p>Ce format garantit des <strong>affiches équilibrées</strong>, car les équipes au même bilan s\'affrontent à chaque ronde. Le calendrier précis est sur la page <a href="/planning/">planning des Worlds</a>.</p>'
            '<h2>Le système suisse en détail</h2>'
            '<h3>Trois victoires pour se qualifier</h3>'
            '<p>Une équipe se qualifie pour la phase finale dès sa <strong>troisième victoire</strong>. Elle ne joue alors plus aucun match de la phase suisse.</p>'
            '<p>À l\'inverse, une équipe qui concède <strong>trois défaites</strong> est éliminée. Le bilan de chaque équipe est visible dans le <a href="/classement/">classement des Worlds</a>.</p>'
            '<h3>Le tirage selon les bilans</h3>'
            '<p>Chaque ronde rapproche des équipes au <strong>bilan identique</strong> : 0-0, 1-0, 0-1, et ainsi de suite. Ce principe évite les matchs déséquilibrés.</p>'
            '<p>Ce fonctionnement rend le <strong>système suisse</strong> imprévisible jusqu\'au bout, avec des qualifiés déterminés seulement lors des dernières rondes.</p>'
            '<h2>La phase finale et le titre</h2>'
            '<h3>Des quarts de finale dès le 3 novembre</h3>'
            '<p>La <strong>phase finale des Worlds</strong> débute le 3 novembre 2026. Les huit équipes qualifiées s\'affrontent en élimination directe, au meilleur des cinq manches.</p>'
            '<p>Quarts, demi-finales et finale se jouent <strong>sans filet de sécurité</strong> : la moindre défaite met fin au parcours. Suivez les scores dans les <a href="/resultats/">résultats en direct</a>.</p>'
            '<h3>Le sacre du champion du monde</h3>'
            '<p>Le vainqueur de la <strong>grande finale</strong> est sacré champion du monde de League of Legends. C\'est l\'aboutissement d\'un mois de compétition.</p>'
            '<p>Chaque équipe engagée vise ce <strong>titre mondial</strong>, le plus prestigieux de l\'esport LoL. Retrouvez toutes les équipes sur la page <a href="/equipes/">équipes des Worlds</a>.</p>'
            '<h2>Les règles de qualification</h2>'
            '<h3>Comment les équipes accèdent aux Worlds</h3>'
            '<p>Chaque <strong>ligue régionale</strong> envoie ses meilleures équipes aux Worlds, selon son classement de fin de saison. Les championnes sont qualifiées d\'office.</p>'
            '<p>Les autres places se jouent via des <strong>tournois de qualification</strong> régionaux, qui déterminent les derniers billets pour la phase de play-in.</p>'
            '<h3>Le seeding, du play-in à la phase finale</h3>'
            '<p>Le <strong>seeding des Worlds</strong> répartit les équipes selon la force de leur région. Les têtes de série évitent de se rencontrer trop tôt dans le tournoi.</p>'
            '<p>Ce classement influence le <strong>tirage des rondes</strong> et garantit que les meilleures équipes se retrouvent plutôt en phase finale.</p>'
            '<h2>Pourquoi ce format des Worlds</h2>'
            '<h3>Un format conçu pour le spectacle</h3>'
            '<p>Le <strong>format actuel des Worlds</strong> favorise les affiches de haut niveau dès les premières rondes, avec peu de matchs sans enjeu.</p>'
            '<p>Chaque série compte, car une <strong>défaite rapproche de l\'élimination</strong>. Cette tension maintient l\'intérêt de bout en bout.</p>'
            '<h3>Un format lisible pour tous</h3>'
            '<p>Malgré sa richesse, le <strong>format des Worlds</strong> reste simple à suivre : trois phases, un objectif clair et des règles identiques pour toutes les équipes.</p>'
            '<p>Cette lisibilité aide les <strong>nouveaux spectateurs</strong> à entrer dans la compétition sans connaître tous les détails du jeu.</p>'
            '<h2>Questions fréquentes sur le format des Worlds</h2>'
            '<h3>Combien de matchs compte le système suisse</h3>'
            '<p>Le <strong>système suisse des Worlds</strong> compte trente-trois rencontres au total, réparties sur cinq rondes de seize équipes.</p>'
            '<p>Ce volume de matchs permet de <strong>déterminer précisément</strong> les huit qualifiés pour la phase finale, sans rencontre à élimination directe.</p>'
            '<h3>Le format a-t-il changé ces dernières années</h3>'
            '<p>Le <strong>format des Worlds</strong> a évolué avec l\'introduction du système suisse, qui a remplacé les anciens groupes pour plus d\'équité.</p>'
            '<p>Cette évolution rend la <strong>course à la qualification</strong> plus lisible et plus serrée jusqu\'à la dernière ronde.</p>'
        ),
        "related": [
            {"slug": "planning", "anchor": "planning des Worlds"},
            {"slug": "classement", "anchor": "classement des Worlds"},
            {"slug": "equipes", "anchor": "équipes des Worlds"},
        ],
        "date_modified": TODAY,
        "date_published": TODAY,
    },
    {
        "slug": "meilleurs-champions-worlds",
        "type": "article",
        "title": "Meilleurs champions Worlds — League of Legends",
        "meta_title": "Meilleurs champions des Worlds LoL 2026 | esport-lol",
        "meta_description": "Les meilleurs champions des Worlds LoL 2026 : les archétypes et les picks qui dominent la meta, rôle par rôle, du play-in jusqu'à la finale.",
        "h1": "Meilleurs champions des Worlds LoL 2026",
        "intro": '<p class="lead">Les <strong>meilleurs champions Worlds</strong> 2026 sont ceux qui dominent la meta du tournoi : flexibles, fiables et décisifs dans chaque rôle.</p>',
        "body": (
            '<h2>Ce qui fait un champion fort aux Worlds</h2>'
            '<h3>La stabilité avant la performance</h3>'
            '<p>Aux Worlds, les équipes privilégient les <strong>champions fiables</strong>, testés pendant toute la saison. La prise de risque est limitée sur les matchs à enjeu.</p>'
            '<p>Un champion dominant à ce niveau est souvent un <strong>pick sûr</strong>, qui apporte de la valeur même sans avantage en début de partie.</p>'
            '<h3>La flexibilité, clé du draft</h3>'
            '<p>Les <strong>champions flexibles</strong>, jouables sur plusieurs rôles, compliquent le draft adverse. Ils donnent un avantage stratégique avant même le début de la partie.</p>'
            '<p>Cette flexibilité explique pourquoi certains <strong>picks sont très disputés</strong> tout au long du tournoi, de la phase de draft aux combats d\'équipe.</p>'
            '<h2>Les rôles qui dominent la meta</h2>'
            '<h3>La midlane, moteur des Worlds</h3>'
            '<p>Historiquement, la <strong>midlane des Worlds</strong> porte les champions de contrôle. Leur capacité à sécuriser les objectifs et à rythmer la partie est précieuse.</p>'
            '<p>Un midlaner solide peut <strong>dicter le rythme</strong> des parties et verrouiller les combats autour du Baron et des Dragons.</p>'
            '<h3>Le jungle et le top, les pivots stratégiques</h3>'
            '<p>Le <strong>jungler des Worlds</strong> oriente les prises d\'objectifs et les ganks. Les champions engagés et mobiles y sont très recherchés.</p>'
            '<p>Sur la <strong>toplane</strong>, les champions résistants et capables de split-push offrent des options tactiques précieuses en fin de partie.</p>'
            '<h2>L\'ADC et le support, la paire décisive</h2>'
            '<h3>L\'ADC, la force de frappe de fin de partie</h3>'
            '<p>L\'<strong>ADC des Worlds</strong> concentre les dégâts en fin de partie. Les tireurs à forte portée et au scaling tardif sont des valeurs sûres.</p>'
            '<p>En phase finale, un <strong>ADC bien protégé</strong> fait souvent la différence dans les combats d\'équipe décisifs.</p>'
            '<h3>Le support, l\'architecte invisible</h3>'
            '<p>Le <strong>support des Worlds</strong> pose la vision et initie les engagements. Les supports d\'engage et de protection sont indispensables à la composition.</p>'
            '<p>Un bon support <strong>crée les opportunités</strong> tout en protégeant ses carries, un rôle souvent sous-estimé mais décisif.</p>'
            '<h2>Des champions incontournables à chaque poste</h2>'
            '<h3>Les classiques de la midlane et du jungle</h3>'
            '<p>Certains champions reviennent <strong>édition après édition</strong> aux Worlds, comme les mages de contrôle à la midlane. Leur fiabilité les rend indémodables.</p>'
            '<p>Au <strong>jungle</strong>, les champions capables d\'engager un combat restent les plus recherchés, car ils dictent le tempo des prises d\'objectifs.</p>'
            '<h3>Les valeurs sûres de la botlane et du top</h3>'
            '<p>En <strong>botlane</strong>, les ADC au scaling tardif dominent souvent les phases finales, où les parties s\'étirent et se décident sur un combat d\'équipe.</p>'
            '<p>Au <strong>top</strong>, les champions solides en lane et utiles en teamfight sont privilégiés, car ils offrent à la fois sécurité et impact collectif.</p>'
            '<h2>Suivre la meta des Worlds 2026</h2>'
            '<h3>Une meta qui évolue avec les patchs</h3>'
            '<p>La <strong>meta des Worlds</strong> évolue au fil du tournoi, car les équipes s\'adaptent aux patchs et aux tendances des autres régions.</p>'
            '<p>Les champions forts du play-in ne sont pas toujours ceux de la <strong>phase finale</strong>. Les drafts s\'affinent de semaine en semaine.</p>'
            '<h3>Où trouver les meilleurs champions par rôle</h3>'
            '<p>Pour un <strong>classement détaillé</strong> des champions, consultez la <a href="/tier-list-lol/">tier list LoL</a> du site, mise à jour régulièrement.</p>'
            '<p>Les <a href="/runes-league-of-legends/">runes League of Legends</a> complètent le sujet pour <strong>optimiser chaque champion</strong> selon son rôle.</p>'
            '<h2>Comment les équipes préparent leurs drafts</h2>'
            '<h3>Le travail sur la meta avant le tournoi</h3>'
            '<p>Avant les Worlds, chaque équipe <strong>analyse la meta</strong> sur le serveur de compétition et définit sa liste de champions prioritaires.</p>'
            '<p>Les <strong>coachs et analystes</strong> construisent des compositions autour des champions les plus forts du patch en vigueur.</p>'
            '<h3>L\'adaptation en cours de tournoi</h3>'
            '<p>Les équipes <strong>ajustent leurs drafts</strong> au fil des matchs, en observant ce qui fonctionne chez leurs adversaires et dans les autres régions.</p>'
            '<p>Cette capacité d\'<strong>adaptation rapide</strong> sépare souvent les équipes qui vont loin de celles qui s\'arrêtent tôt.</p>'
            '<h2>Les champions à surveiller en phase finale</h2>'
            '<h3>Les picks qui décident des grandes séries</h3>'
            '<p>En <strong>phase finale</strong>, les équipes resserrent leurs drafts autour de leurs champions les plus confiants, au détriment des expérimentations.</p>'
            '<p>Les séries au meilleur des cinq manches récompensent les <strong>champions maîtrisés</strong> plutôt que les paris risqués.</p>'
            '<h3>Le rôle des bans dans la meta</h3>'
            '<p>Les <strong>bans ciblés</strong> retirent du draft les champions trop menaçants de l\'adversaire. Ils façonnent autant la meta que les picks eux-mêmes.</p>'
            '<p>Cette guerre des <strong>bans et des priorités</strong> rend chaque phase de draft décisive avant même la première minute de jeu.</p>'
        ),
        "related": [
            {"slug": "tier-list-lol", "anchor": "tier list LoL"},
            {"slug": "runes-league-of-legends", "anchor": "runes League of Legends"},
            {"slug": "equipes", "anchor": "équipes des Worlds"},
        ],
        "date_modified": TODAY,
        "date_published": TODAY,
    },
]

# Écriture des pages
import re
for p in pages:
    path = os.path.join(ROOT, "content", p["slug"] + ".json")
    json.dump(p, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    plain = re.sub(r"<[^>]+>", " ", p["body"])
    words = len(plain.split())
    print(f"✓ {p['slug']} — {words} mots (texte) — meta_title {len(p['meta_title'])}ch")

# Mise à jour du backlog : retirer les 3 entrées « Worlds » (equipes-worlds-lol déjà couvert par /equipes/)
bp_path = os.path.join(ROOT, "data", "backlog.json")
bp = json.load(open(bp_path, encoding="utf-8"))
done_slugs = {"format-worlds-lol", "equipes-worlds-lol", "meilleurs-champions-worlds"}
before = len(bp["pages"])
bp["pages"] = [x for x in bp["pages"] if x.get("slug") not in done_slugs]
json.dump(bp, open(bp_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nBacklog : {before} -> {len(bp['pages'])} pages (retiré : {', '.join(sorted(done_slugs))})")
print("Restant :", ", ".join(x['slug'] for x in bp['pages']))
