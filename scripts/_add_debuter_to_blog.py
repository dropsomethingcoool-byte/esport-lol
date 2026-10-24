#!/usr/bin/env python3
"""Ajoute (idempotent) la page /debuter-lol/ au hub /blog/ dans une section « Guides »."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "content", "blog.json")
TODAY = "2026-10-24"

ITEM = (
    '<p class="recap-item"><a href="/debuter-lol/">Débuter League of Legends : guide du débutant</a> '
    '<span class="recap-date">· 2026-10-24</span> — <strong>prise en main</strong> de la carte, '
    "des rôles et du farm.</p>"
)

with open(PATH, encoding="utf-8") as f:
    blog = json.load(f)

body = blog["body"]

# Réparation d'un passage antérieur : section restée fusionnée avec « Actualités ».
if "/debuter-lol/" in body and "<h2>Guides</h2>" not in body:
    if 'Guides pour progresser</h2><p class="recap-item">' in body and "Actualités</h2>" in body:
        body = body.replace(
            'Guides pour progresser</h2><p class="recap-item">',
            "<h2>Guides</h2>" + ITEM + '<h2>Actualités</h2><p class="recap-item">',
            1,
        )
        # On retire l'ancien item qui avait fuité dans la section Actualités.
        body = re.sub(
            r'(<h2>Actualités</h2>)<p class="recap-item"><a href="/debuter-lol/">.*?</p>',
            r"\1",
            body,
            count=1,
            flags=re.S,
        )
        blog["body"] = body
        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(blog, f, ensure_ascii=False, indent=2)
        print("✓ structure blog réparée")

if "/debuter-lol/" in body:
    print("déjà présent — rien à faire")
else:
    marker = '<h2>Actualités</h2><p><a href="/galions-emea-masters-2026/">'
    assert marker in body, "section Actualités introuvable"
    body = body.replace(marker, "<h2>Guides</h2>" + ITEM + marker, 1)
    blog["body"] = body
    blog["date_modified"] = TODAY
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(blog, f, ensure_ascii=False, indent=2)
    print("✓ content/blog.json : section Guides + /debuter-lol/")

# Contrôle : chaque <h2> doit être fermé et suivi d'un <p>.
for h in re.findall(r"<h2>[^<]*</h2>.{0,20}", blog["body"]):
    print("  H2 →", h.replace("\n", " ")[:90])
