#!/usr/bin/env python3
"""SEO site-wide : mots-clés (H1/meta_title) + maillage interne (related = 3 liens)
pour toutes les pages non-équipe. Relançable sans risque.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")

# slug -> (h1, meta_title) : le mot-clé principal doit y figurer
H1_META = {
    "index": ("Suivez les Worlds LoL 2026", "Worlds LoL 2026 : planning, résultats et classement | esport-lol"),
    "planning": ("Planning des Worlds LoL 2026", "Planning des Worlds LoL 2026 : calendrier et matchs | esport-lol"),
    "resultats": ("Résultats des Worlds LoL 2026", "Résultats des Worlds LoL 2026 : scores mis à jour | esport-lol"),
    "classement": ("Classement des Worlds LoL 2026", "Classement des Worlds LoL 2026 : groupes et bilans | esport-lol"),
    "equipes": ("Équipes des Worlds LoL 2026", "Équipes des Worlds LoL 2026 : toutes les équipes | esport-lol"),
    "blog": ("Blog Worlds LoL", "Blog Worlds LoL : actualités, guides et résumés | esport-lol"),
    "parier-worlds-lol": ("Parier sur les Worlds LoL", "Parier sur les Worlds LoL : guide, cotes et types de paris"),
    "tier-list-lol": ("Tier List LoL", "Tier List LoL : classement des champions par rôle"),
    "runes-league-of-legends": ("Runes League of Legends", "Runes League of Legends : le guide complet"),
    "a-propos": ("À propos d'esport-lol", "À propos d'esport-lol : suivi des Worlds League of Legends"),
    "contact": ("Contact", "Contact | esport-lol — suivi des Worlds League of Legends"),
    "confidentialite": ("Politique de confidentialité", "Politique de confidentialité | esport-lol"),
    "kc-vs-cloud9-resume": ("Karmine Corp vs Cloud9 : résumé du match", "Karmine Corp vs Cloud9 : résumé du match Worlds LoL 2026"),
    "mvk-vs-furia-resume": ("MVK Esports vs FURIA : résumé du match", "MVK Esports vs FURIA : résumé du match Worlds LoL 2026"),
}

# slug -> 3 liens internes sortants (ancres SEO)
RELATED = {
    "planning": [
        {"slug": "resultats", "anchor": "Résultats des Worlds LoL 2026"},
        {"slug": "classement", "anchor": "Classement des Worlds LoL 2026"},
        {"slug": "equipes", "anchor": "Toutes les équipes des Worlds LoL"},
    ],
    "resultats": [
        {"slug": "planning", "anchor": "Planning des Worlds LoL 2026"},
        {"slug": "classement", "anchor": "Classement des Worlds LoL 2026"},
        {"slug": "blog", "anchor": "Résumés de matchs des Worlds LoL"},
    ],
    "classement": [
        {"slug": "planning", "anchor": "Planning des Worlds LoL 2026"},
        {"slug": "resultats", "anchor": "Résultats des Worlds LoL 2026"},
        {"slug": "equipes", "anchor": "Toutes les équipes des Worlds LoL"},
    ],
    "equipes": [
        {"slug": "planning", "anchor": "Planning des Worlds LoL 2026"},
        {"slug": "classement", "anchor": "Classement des Worlds LoL 2026"},
        {"slug": "blog", "anchor": "Résumés de matchs des Worlds LoL"},
    ],
    "blog": [
        {"slug": "equipes", "anchor": "Toutes les équipes des Worlds LoL"},
        {"slug": "planning", "anchor": "Planning des Worlds LoL 2026"},
        {"slug": "parier-worlds-lol", "anchor": "Parier sur les Worlds LoL"},
    ],
    "parier-worlds-lol": [
        {"slug": "planning", "anchor": "Planning des Worlds LoL 2026"},
        {"slug": "equipes", "anchor": "Toutes les équipes des Worlds LoL"},
        {"slug": "blog", "anchor": "Résumés de matchs des Worlds LoL"},
    ],
    "tier-list-lol": [
        {"slug": "runes-league-of-legends", "anchor": "Runes League of Legends"},
        {"slug": "blog", "anchor": "Blog League of Legends"},
        {"slug": "equipes", "anchor": "Équipes des Worlds LoL"},
    ],
    "runes-league-of-legends": [
        {"slug": "tier-list-lol", "anchor": "Tier List LoL"},
        {"slug": "blog", "anchor": "Blog League of Legends"},
        {"slug": "equipes", "anchor": "Équipes des Worlds LoL"},
    ],
    "a-propos": [
        {"slug": "index", "anchor": "Suivi des Worlds LoL 2026"},
        {"slug": "equipes", "anchor": "Équipes des Worlds LoL"},
        {"slug": "contact", "anchor": "Contacter esport-lol"},
    ],
    "contact": [
        {"slug": "a-propos", "anchor": "À propos d'esport-lol"},
        {"slug": "index", "anchor": "Suivi des Worlds LoL"},
        {"slug": "planning", "anchor": "Planning des Worlds LoL"},
    ],
    "confidentialite": [
        {"slug": "index", "anchor": "Suivi des Worlds LoL 2026"},
        {"slug": "a-propos", "anchor": "À propos d'esport-lol"},
        {"slug": "contact", "anchor": "Contacter esport-lol"},
    ],
    # résumés de matchs (ancres SEO au lieu des ancres génériques)
    "kc-vs-cloud9-resume": [
        {"slug": "equipe-karmine-corp", "anchor": "Karmine Corp aux Worlds LoL"},
        {"slug": "equipe-cloud9-kia", "anchor": "Cloud9 aux Worlds LoL"},
        {"slug": "blog", "anchor": "Tous les résumés des Worlds LoL"},
    ],
    "mvk-vs-furia-resume": [
        {"slug": "equipe-mvk-esports", "anchor": "MVK Esports aux Worlds LoL"},
        {"slug": "equipe-furia", "anchor": "FURIA aux Worlds LoL"},
        {"slug": "blog", "anchor": "Tous les résumés des Worlds LoL"},
    ],
}


def main():
    updated = []
    for slug, (h1, meta) in H1_META.items():
        path = os.path.join(CONTENT, slug + ".json")
        if not os.path.exists(path):
            continue
        d = json.load(open(path, encoding="utf-8"))
        d["h1"] = h1
        d["meta_title"] = meta
        if slug in RELATED:
            d["related"] = RELATED[slug]
        json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        updated.append(slug)
    print(f"✓ {len(updated)} pages mises à jour (H1/meta/related)")
    print("  ", ", ".join(updated))


if __name__ == "__main__":
    main()
