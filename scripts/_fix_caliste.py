#!/usr/bin/env python3
import json, os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
p = os.path.join(ROOT, "content", "joueur-caliste.json")
with open(p, encoding="utf-8") as f:
    d = json.load(f)

add = (
    "<h3>Un profil encore en construction</h3>"
    "<p>Caliste reste un joueur en <strong>pleine progression</strong>, dont le plafond n'est pas encore atteint. "
    "Chaque compétition lui permet d'accumuler de l'expérience.</p>"
    "<p>Les Worlds 2026 constituent une étape <strong>décisive</strong> dans la construction de sa carrière internationale.</p>"
)

body = d["body"]
if "Un profil encore en construction" not in body:
    anchor = "Cette <strong>comparaison</strong> stimule Caliste, qui aspire à marcher dans les pas de son aîné tout en écrivant sa propre histoire.</p>"
    body = body.replace(anchor, anchor + add, 1)
    d["body"] = body
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("✓ ajouté")
else:
    print("· déjà présent")
