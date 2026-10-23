#!/usr/bin/env python3
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(ROOT, "content", "patch-notes-lol.json")
p = json.load(open(path, encoding="utf-8"))
body = p["body"]
old = "Le réflexe utile : retester une <strong>partie normale</strong> avant de repartir en classée avec un build modifié."
new = "Le réflexe utile : retester une partie normale avant de repartir en classée avec un build modifié."
assert old in body
body = body.replace(old, new, 1)
p["body"] = body
json.dump(p, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("mots:", len(re.sub(r"<[^>]+>", " ", body).split()))
