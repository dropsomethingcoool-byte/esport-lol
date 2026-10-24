#!/usr/bin/env python3
"""Met à jour le contenu suite au tirage au sort du swiss stage Worlds 2026."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")
TODAY = "2026-10-18"

def load(p):
    with open(os.path.join(CONTENT, p), encoding="utf-8") as f:
        return json.load(f)

def save(p, d):
    with open(os.path.join(CONTENT, p), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# 1. Article « tirage au sort du swiss stage »
# ---------------------------------------------------------------------------
article = {
    "slug": "tirage-au-sort-worlds-2026",
    "type": "article",
    "silo": "blog",
    "title": "Tirage au sort du swiss stage — Worlds 2026",
    "meta_title": "Tirage au sort du swiss stage Worlds 2026",
    "meta_description": "Le tirage au sort du swiss stage des Worlds 2026 : les 8 affiches de la première journée et le calendrier de la phase, du 23 au 31 octobre.",
    "h1": "Tirage au sort du swiss stage des Worlds 2026",
    "intro": "<p class=\"lead\">Le <strong>tirage au sort du swiss stage des Worlds 2026</strong> a eu lieu ce 18 octobre : voici les huit affiches de la première journée, programmée le vendredi 23 octobre.</p>",
    "body": (
        "<h2>Le tirage au sort</h2>"
        "<h3>Le principe des chapeaux</h3>"
        "<p>Les seize équipes qualifiées ont été réparties en quatre chapeaux selon leur niveau. Le tirage oppose les équipes du <strong>chapeau 1</strong> à celles du <strong>chapeau 4</strong>, et celles du <strong>chapeau 2</strong> à celles du <strong>chapeau 3</strong>, sans confrontation entre deux équipes d'une même région.</p>"
        "<p><strong>Karmine Corp</strong>, vainqueur du play-in, intégrait le chapeau 4 et devait donc hériter d'une tête de série du chapeau 1.</p>"
        "<h3>Les huit affiches du Round 1</h3>"
        "<p><strong>Gen.G</strong> vs <strong>Invictus Gaming</strong></p>"
        "<p><strong>Team Liquid</strong> vs <strong>CTBC Flying Oyster</strong></p>"
        "<p><strong>Anyone's Legend</strong> vs <strong>Karmine Corp</strong></p>"
        "<p><strong>G2 Esports</strong> vs <strong>Dplus Kia</strong></p>"
        "<p><strong>Hanwha Life Esports</strong> vs <strong>Top Esports</strong></p>"
        "<p><strong>Los Grandes</strong> vs <strong>T1</strong></p>"
        "<p><strong>Team Secret Whales</strong> vs <strong>LYON</strong></p>"
        "<p><strong>Bilibili Gaming</strong> vs <strong>Movistar KOI</strong></p>"
        "<h2>Karmine Corp face à Anyone's Legend</h2>"
        "<h3>Un premier gros test</h3>"
        "<p>En s'imposant en finale du play-in, <strong>Karmine Corp</strong> a hérité de l'un des morceaux les plus lourds du chapeau 1 : <strong>Anyone's Legend</strong>, champion de Chine. Un premier test d'envergure pour la formation française.</p>"
        "<h3>Le déroulé de la phase</h3>"
        "<p>Au swiss stage, chaque équipe enchaîne jusqu'à cinq rondes. Trois victoires qualifient pour les quarts de finale, trois défaites éliminent. Les matchs de qualification et d'élimination se jouent en <strong>Bo3</strong>, les autres en <strong>Bo1</strong>.</p>"
        "<h2>Le calendrier du swiss stage</h2>"
        "<h3>La première journée</h3>"
        "<p>La swiss stage se déroule à <strong>Allen (Texas)</strong> du 23 au 31 octobre. La première journée se joue le <strong>vendredi 23 octobre à partir de 19h</strong> (heure de Paris).</p>"
        "<h3>Suivre la compétition</h3>"
        "<p>Le calendrier complet est sur la page <a href=\"/planning/\">planning des Worlds</a>. Les scores seront mis à jour en direct sur les <a href=\"/resultats/\">résultats</a> et le <a href=\"/classement/\">classement</a> au fil des matchs.</p>"
    ),
    "related": [
        {"slug": "planning", "anchor": "planning des Worlds"},
        {"slug": "classement", "anchor": "classement des Worlds"},
        {"slug": "resultats", "anchor": "résultats en direct"},
        {"slug": "blog", "anchor": "tous les résumés"},
    ],
    "date_modified": TODAY,
    "date_published": TODAY,
}
save("tirage-au-sort-worlds-2026.json", article)
print("✓ article tirage-au-sort-worlds-2026.json")

# ---------------------------------------------------------------------------
# 2. Blog : ajouter une section « Actualités des Worlds » en tête
# ---------------------------------------------------------------------------
blog = load("blog.json")
news = ('<h2>Actualités des Worlds</h2>'
        '<p><a href="/tirage-au-sort-worlds-2026/">Tirage au sort du swiss stage</a>'
        ' — les 8 affiches de la première journée du 23 octobre.</p>')
body = blog["body"]
anchor = '<h2>Résumés de matchs</h2>'
if news not in body:
    body = body.replace(anchor, news + anchor, 1)
blog["body"] = body
blog["date_modified"] = TODAY
save("blog.json", blog)
print("✓ blog.json (section Actualités)")

# ---------------------------------------------------------------------------
# 3. Planning : passer au swiss stage
# ---------------------------------------------------------------------------
planning = load("planning.json")
planning["body"] = (
    "<h2>Play-ins — du 15 au 18 octobre 2026</h2>"
    "<p>Le play-in s'est achevé le 18 octobre : <strong>Karmine Corp</strong> a validé son billet pour le swiss stage en dominant MVK Esports en finale.</p>"
    "<h2>Système suisse — du 23 au 31 octobre 2026</h2>"
    "<p>Le <strong>swiss stage</strong> réunit les 16 équipes qualifiées du <strong>23 au 31 octobre</strong> à Allen (Texas). La première journée se joue le <strong>vendredi 23 octobre à partir de 19h</strong> (heure de Paris).</p>"
    "<div id=\"live-matches\" class=\"match-list\"></div>"
    "<p>Les affiches du Round 1 : <strong>Gen.G – Invictus Gaming</strong>, <strong>Team Liquid – CTBC Flying Oyster</strong>, <strong>Anyone's Legend – Karmine Corp</strong>, <strong>G2 Esports – Dplus Kia</strong>, <strong>Hanwha Life Esports – Top Esports</strong>, <strong>Los Grandes – T1</strong>, <strong>Team Secret Whales – LYON</strong> et <strong>Bilibili Gaming – Movistar KOI</strong>.</p>"
    "<h2>Phase finale — à partir du 3 novembre 2026</h2>"
    "<p>Les <strong>quarts de finale</strong> débutent le <strong>mardi 3 novembre 2026</strong> ; les huit équipes qualifiées seront déterminées à l'issue du swiss stage.</p>"
    "<p><a class=\"pill\" href=\"/resultats/\">Voir les résultats <span class=\"arrow\">→</span></a><a class=\"pill\" href=\"/classement/\">Voir le classement <span class=\"arrow\">→</span></a><a class=\"pill\" href=\"/parier-worlds-lol/\">Parier sur les Worlds <span class=\"arrow\">→</span></a></p>"
)
planning["date_modified"] = TODAY
save("planning.json", planning)
print("✓ planning.json")

# ---------------------------------------------------------------------------
# 4. Index : hero → swiss stage
# ---------------------------------------------------------------------------
index = load("index.json")
b = index["body"]
b = b.replace("Worlds 2026 · Play-in", "Worlds 2026 · Système suisse")
b = b.replace(
    '<span class="stat-value">15 oct.</span><span class="stat-label">Début du play-in</span>',
    '<span class="stat-value">23 oct.</span><span class="stat-label">Début du swiss stage</span>',
)
index["body"] = b
index["date_modified"] = TODAY
save("index.json", index)
print("✓ index.json (hero swiss stage)")

# ---------------------------------------------------------------------------
# 5. Resultats + classement : mention suisse
# ---------------------------------------------------------------------------
resultats = load("resultats.json")
resultats["body"] = (
    "<p>Le play-in est terminé. La prochaine phase, le <strong>swiss stage</strong>, démarre le <strong>vendredi 23 octobre</strong>.</p>"
    "<div id=\"live-results\" class=\"match-list\"></div>"
    "<p><a class=\"pill\" href=\"/planning/\">Voir le planning <span class=\"arrow\">→</span></a><a class=\"pill\" href=\"/classement/\">Voir le classement <span class=\"arrow\">→</span></a><a class=\"pill\" href=\"/parier-worlds-lol/\">Parier sur les Worlds <span class=\"arrow\">→</span></a></p>"
)
resultats["date_modified"] = TODAY
save("resultats.json", resultats)
print("✓ resultats.json")

classement = load("classement.json")
classement["body"] = (
    "<p>Le <strong>swiss stage</strong> débute le 23 octobre : le classement (victoires, défaites, éliminations) se remplira au fil des matchs.</p>"
    "<div id=\"live-standings\" class=\"standings\"></div>"
    "<p>Le classement des Worlds 2026 est mis à jour <strong>en temps réel</strong> au fil des matchs, phase par phase.</p>"
    "<p><a class=\"pill\" href=\"/planning/\">Voir le planning <span class=\"arrow\">→</span></a><a class=\"pill\" href=\"/resultats/\">Voir les résultats <span class=\"arrow\">→</span></a><a class=\"pill\" href=\"/parier-worlds-lol/\">Parier sur les Worlds <span class=\"arrow\">→</span></a></p>"
)
classement["date_modified"] = TODAY
save("classement.json", classement)
print("✓ classement.json")

print("\nContenu mis à jour.")
