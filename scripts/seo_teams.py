#!/usr/bin/env python3
"""SEO : génère le contenu 500+ mots + mots-clés (H1/meta) + maillage interne des pages équipe.

Pour chaque équipe :
  - contenu HTML 500-600 mots via l'API DeepSeek (mot-clé « <Nom> Worlds LoL »)
  - h1 / meta_title / meta_description optimisés (mot-clé présent)
  - related = 3 liens internes SEO (hub + 2 équipes voisines, en cycle → chaque
    page reçoit aussi 3 liens entrants)

Réutilisable : écrase les pages équipe existantes.
"""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
DS_URL = "https://api.deepseek.com/chat/completions"
DS_MODEL = "deepseek-chat"
ENV = "/Users/charlesploteau/.hermes/profiles/esport-lol/.env"

sys.path.insert(0, os.path.join(ROOT, "scripts"))
from build_teams import TEAMS, slugify  # noqa: E402


def ds_key():
    for line in open(ENV, encoding="utf-8"):
        line = line.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")


def call_deepseek(prompt):
    payload = {"model": DS_MODEL, "messages": [{"role": "user", "content": prompt}],
               "max_tokens": 4096, "temperature": 0.5, "response_format": {"type": "json_object"}}
    req = urllib.request.Request(DS_URL, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {ds_key()}",
                                          "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read().decode())


def generate(name, region, seed, history, expect):
    prompt = (
        f"Rédige un contenu SEO français de 500 à 600 mots pour la page équipe de {name} sur un site "
        f"consacré aux Worlds League of Legends. Le mot-clé principal est « {name} Worlds LoL ».\n\n"
        f"FAITS (base-toi uniquement dessus, n'invente AUCUN fait précis supplémentaire) :\n"
        f"- Équipe : {name}\n- Région : {region}\n- Seed : {seed}\n"
        f"- Historique : {history}\n- Attentes : {expect}\n\n"
        f"Retourne UNIQUEMENT un objet JSON avec les clés h1, meta_title, meta_description, body.\n"
        f"- h1 : « {name} aux Worlds LoL 2026 »\n"
        f"- meta_title : contient « {name} » et « Worlds LoL » (≤ 60 caractères)\n"
        f"- meta_description : 1-2 phrases (≤ 160 caractères) contenant le mot-clé\n"
        f"- body : HTML (h2/h3 + p uniquement) d'au moins 500 mots, structuré :\n"
        f"  1) h2 « {name} aux Worlds LoL 2026 » : 2-3 paragraphes (présentation, région, seed, enjeu)\n"
        f"  2) h2 « Historique et parcours » : 2 paragraphes (à partir de l'historique fourni)\n"
        f"  3) h2 « Attentes pour les Worlds LoL » : 2 paragraphes (à partir des attentes fournies)\n"
        f"- Utilise le mot-clé « {name} Worlds LoL » (et variantes naturelles) 4 à 6 fois, dont dans un h2 et le premier paragraphe.\n"
        f"- N'invente PAS de palmarès chiffré, de roster, de statistiques ou de résultats précis. Reste général.\n"
        f"- Français correct, ton éditorial, phrases claires."
    )
    r = call_deepseek(prompt)
    return json.loads(r["choices"][0]["message"]["content"])


def word_count(html):
    # compte approximatif des mots (texte hors balises)
    import re
    text = re.sub(r"<[^>]+>", " ", html)
    return len(text.split())


def main():
    teams = [dict(name=n, region=reg, seed=sd, logo=lg, history=h, expect=e, code=c)
             for (c, n, reg, sd, lg, h, e) in TEAMS]
    n = len(teams)
    for i, t in enumerate(teams):
        slug = "equipe-" + slugify(t["name"])
        path = os.path.join(CONTENT, slug + ".json")
        if not os.path.exists(path):
            print(f"[SKIP] {slug} introuvable")
            continue
        try:
            art = generate(t["name"], t["region"], t["seed"], t["history"], t["expect"])
        except Exception as e:
            print(f"[ERREUR] {t['name']} : {e}")
            continue

        wc = word_count(art.get("body", ""))
        # 3 liens internes sortants (cycle) : hub + 2 équipes voisines
        nxt1 = teams[(i + 1) % n]
        nxt2 = teams[(i + 2) % n]
        related = [
            {"slug": "equipes", "anchor": "toutes les équipes des Worlds LoL 2026"},
            {"slug": "equipe-" + slugify(nxt1["name"]), "anchor": f"{nxt1['name']} aux Worlds LoL"},
            {"slug": "equipe-" + slugify(nxt2["name"]), "anchor": f"{nxt2['name']} aux Worlds LoL"},
        ]

        d = json.load(open(path, encoding="utf-8"))
        d["h1"] = art["h1"]
        d["meta_title"] = art["meta_title"]
        d["meta_description"] = art["meta_description"]
        d["title"] = art["h1"]
        d["intro"] = f'<p class="lead">{art["meta_description"]}</p>'
        d["body"] = f'<div class="team-hero"><img class="team-logo" src="{t["logo"]}" alt="{t["name"]}" loading="lazy"><div class="team-hero-meta"><span class="team-region">{t["region"]}</span><span class="team-seed">Seed : {t["seed"]}</span></div></div>' + art["body"]
        d["related"] = related
        json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"✓ {t['name']:24} {wc} mots")

    print("Terminé.")


if __name__ == "__main__":
    main()
