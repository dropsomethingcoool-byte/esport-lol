#!/usr/bin/env python3
"""Réécrit parier-worlds-lol.json : bascule Betsson -> BetNinja + CTA verts."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
PATH = os.path.join(ROOT, "content", "parier-worlds-lol.json")

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)

CTA_TOP = ('<div class="cta-affiliate"><div class="cta-box">\n'
           '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
           '<div class="cta-box-title">Parier sur les Worlds avec BetNinja</div>\n'
           '<p>BetNinja propose des <strong>paris esport</strong> sur League of Legends : '
           'cotes en direct, marchés variés et bonus de bienvenue sur le premier dépôt. '
           'Retrouvez les principaux marchés décrits dans ce guide.</p>\n'
           '<a class="cta-btn" href="/go/lol" rel="nofollow sponsored noopener">'
           'Parier sur les Worlds <span class="cta-arrow">→</span></a>\n'
           '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire '
           '(commission perçue sans surcoût).</p>\n'
           '</div></div>')

CTA_BOTTOM = ('<div class="cta-affiliate"><div class="cta-box">\n'
              '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
              '<div class="cta-box-title">Prêt à parier sur les Worlds ?</div>\n'
              '<p>Créez votre compte BetNinja, activez votre bonus de bienvenue et '
              'retrouvez toutes les cotes des Worlds 2026 en temps réel.</p>\n'
              '<a class="cta-btn" href="/go/lol" rel="nofollow sponsored noopener">'
              'S\'inscrire sur BetNinja <span class="cta-arrow">→</span></a>\n'
              '<p class="cta-disclosure">18+ · Jouer comporte des risques · '
              'Lien partenaire (commission perçue sans surcoût).</p>\n'
              '</div></div>')

body = d["body"]

# 1. Remplacer l'ancien encart CTA (span non cliquable) par le nouvel encart vert.
OLD_CTA = ('<div class="cta-box">\n'
           '<div class="cta-box-title">Betsson — notre plateforme recommandée pour parier sur les Worlds</div>\n'
           '<p>Betsson propose des <strong>paris esport</strong> sur League of Legends, avec des cotes sur les matchs des Worlds. Retrouvez les principaux marchés décrits dans ce guide.</p>\n'
           '<span class="cta-btn">Parier sur les Worlds</span>\n'
           '</div>')
assert OLD_CTA in body, "ancien CTA introuvable"
body = body.replace(OLD_CTA, CTA_TOP, 1)

# 2. Remplacer toute la section « Betsson, la plateforme recommandée » par BetNinja.
OLD_SECTION = (
    '<h2>Betsson, la plateforme recommandée pour parier sur les Worlds</h2>\n'
    '<h3>Pourquoi Betsson pour l\'esport</h3>\n'
    '<p>Betsson est un opérateur de paris sportifs qui propose une section <strong>esport</strong>, avec League of Legends parmi les jeux couverts.</p>\n'
    '<p>La plateforme affiche les <strong>cotes des Worlds</strong> pour les principaux marchés décrits plus haut.</p>\n'
    '<h3>Bonus de bienvenue et dépôt</h3>\n'
    '<p>Betsson propose un <strong>bonus de bienvenue</strong> aux nouveaux joueurs. Les conditions exactes sont détaillées sur le site de l\'opérateur.</p>\n'
    '<p>Les <strong>dépôts et retraits</strong> se font par les moyens de paiement disponibles. Vérifiez les délais avant de vous inscrire.</p>\n'
    '<h3>S\'inscrire sur Betsson</h3>\n'
    '<p>L\'inscription demande une <strong>vérification d\'identité</strong> et la confirmation de votre majorité. Cette étape est obligatoire.</p>\n'
    '<p>Une fois le compte créé, vous déposez un premier montant puis accédez aux <strong>marchés des Worlds</strong>.</p>\n'
)
NEW_SECTION = (
    '<h2>BetNinja, la plateforme recommandée pour parier sur les Worlds</h2>\n'
    '<h3>Pourquoi BetNinja pour l\'esport</h3>\n'
    '<p>BetNinja est une plateforme de paris qui propose une section <strong>esport</strong> complète, avec League of Legends parmi les jeux couverts.</p>\n'
    '<p>La plateforme affiche les <strong>cotes des Worlds</strong> pour les principaux marchés décrits plus haut, avec des cotes boostées et des options de paris en direct.</p>\n'
    '<h3>Le bonus de dépôt hebdomadaire</h3>\n'
    '<p>BetNinja propose un <strong>bonus de dépôt hebdomadaire de 75 % jusqu\'à 500 €</strong> sur le sport. Un coup de boost régulier pour donner de l\'élan à votre bankroll tout au long des Worlds.</p>\n'
    '<p>La plateforme ajoute aussi un <strong>multiboost</strong> (jusqu\'à 30 % de gain supplémentaire sur vos combinés gagnants) et des <strong>cotes boostées du jour</strong> sur les grands matchs.</p>\n'
    '<h3>S\'inscrire sur BetNinja</h3>\n'
    '<p>L\'inscription demande une <strong>vérification d\'identité</strong> et la confirmation de votre majorité. Cette étape est obligatoire.</p>\n'
    '<p>Une fois le compte créé, vous déposez un premier montant puis accédez aux <strong>marchés des Worlds</strong>. Les conditions exactes des bonus sont détaillées sur le site de l\'opérateur.</p>\n'
)
assert OLD_SECTION in body, "section Betsson introuvable"
body = body.replace(OLD_SECTION, NEW_SECTION, 1)

# 3. Bascule globale des mentions restantes.
body = body.replace("Betsson", "BetNinja")

# 4. FAQ « meilleur site » -> BetNinja (déjà couvert par le replace global, mais on affine).
body = body.replace(
    '<p>Nous recommandons <strong>BetNinja</strong> pour sa section esport et ses cotes sur League of Legends.</p>',
    '<p>Nous recommandons <strong>BetNinja</strong> pour sa section esport, ses cotes sur League of Legends et son bonus de dépôt de 75 % jusqu\'à 500 €.</p>',
)

# 5. Ajouter un CTA de bas de page après la FAQ.
body += "\n\n" + CTA_BOTTOM

d["body"] = body
d["intro"] = d["intro"].replace("la plateforme Betsson", "la plateforme BetNinja")
d["meta_description"] = d["meta_description"].replace("plateforme Betsson", "plateforme BetNinja")
d["meta_description"] = d["meta_description"].replace("bonus et plateforme BetNinja", "bonus de dépôt et plateforme BetNinja")
d["date_modified"] = "2026-10-19"

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("OK — parier-worlds-lol.json réécrit pour BetNinja")
print("Betsson restant dans body :", body.count("Betsson"))
print("BetNinja dans body :", body.count("BetNinja"))
