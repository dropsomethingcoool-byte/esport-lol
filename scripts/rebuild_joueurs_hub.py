#!/usr/bin/env python3
"""Reconstruit le hub « Joueurs » (content/joueurs.json) à partir des
content/joueur-*.json existants — grille annuaire avec portrait."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")


def main():
    players = []
    for fn in sorted(os.listdir(CONTENT)):
        if fn.startswith("joueur-") and fn.endswith(".json") and fn != "joueurs.json":
            with open(os.path.join(CONTENT, fn), encoding="utf-8") as f:
                players.append(json.load(f))

    if not players:
        print("· aucun joueur, hub non écrit")
        return

    items = []
    for p in players:
        pseudo = p.get("pseudo") or p.get("h1", "")
        role = p.get("role", "")
        team = p.get("team_name", "")
        photo = p.get("photo", "")
        img = (
            f'<img src="{photo}" alt="{pseudo}, {role} de {team}" loading="lazy">'
            if photo else ""
        )
        items.append(
            f'<a class="player-tile" href="/{p["slug"]}/">{img}'
            f'<span class="pt-name">{pseudo}</span>'
            f'<span class="pt-meta">{role} · {team}</span></a>'
        )

    body = (
        f"<p>Les <strong>fiches joueurs</strong> des Worlds 2026 : profil, palmarès, "
        f"style de jeu et rôle dans leur équipe.</p>"
        f'<div class="players-grid">{"".join(items)}</div>'
    )
    hub = {
        "slug": "joueurs",
        "type": "hub",
        "silo": "joueurs",
        "title": "Joueurs des Worlds 2026 — League of Legends",
        "meta_title": "Joueurs des Worlds LoL 2026 | esport-lol",
        "meta_description": "Fiches des joueurs des Worlds League of Legends 2026 : profil, palmarès et style de jeu des stars du tournoi.",
        "h1": "Joueurs des Worlds 2026",
        "intro": '<p class="lead">Les <strong>joueurs des Worlds 2026</strong> : profil, palmarès et style de jeu des stars de la compétition.</p>',
        "body": body,
        "date_modified": "2026-10-24",
        "date_published": "2026-10-24",
        "related": [
            {"slug": "equipes", "anchor": "Toutes les équipes des Worlds"},
            {"slug": "joueurs-a-suivre-worlds-2026", "anchor": "Joueurs à suivre aux Worlds 2026"},
            {"slug": "planning", "anchor": "Planning des Worlds LoL"},
        ],
    }
    with open(os.path.join(CONTENT, "joueurs.json"), "w", encoding="utf-8") as f:
        json.dump(hub, f, ensure_ascii=False, indent=2)
    print(f"✓ hub joueurs.json ({len(players)} joueurs, avec portraits)")


if __name__ == "__main__":
    main()
