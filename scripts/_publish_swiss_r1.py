#!/usr/bin/env python3
"""Publie les récaps des matchs Swiss R1 terminés (Bo1) sans article.
Rédaction factuelle locale (pas de DeepSeek), VOD via API lolesports,
publication via publish_recap.py, puis déploiement unique."""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import cloud_recap  # noqa: E402  (réutilise fetch_vods_html)

NAME_MAP = {"TOP ESPORTS": "Top Esports", "BILIBILI GAMING": "Bilibili Gaming"}

CTA = ('<div class="cta-affiliate"><div class="cta-box">\n'
       '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
       '<div class="cta-box-title">Parier sur les Worlds LoL</div>\n'
       'Suivez les cotes des prochains matchs des Worlds 2026 et placez vos paris esport sur BetNinja.</p>\n'
       '<a class="cta-btn" href="/parier-worlds-lol/" data-go="L2dvL2xvbA==" rel="nofollow sponsored noopener" target="_blank">Parier sur les Worlds <span class="cta-arrow">→</span></a>\n'
       '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire.</p>\n'
       '</div></div>')

SOURCE = ('<p class="source-line">Source : <a href="https://lolesports.com" rel="nofollow noopener" target="_blank">Lolesports</a> — données officielles du match.</p>')


def matchup(win, lose, score):
    return (
        '<div class="matchup-hero"><div class="matchup-team">'
        f'<img class="matchup-logo" src="{win["image"]}" alt="Logo {win["name"]} — Worlds 2026" loading="lazy">'
        f'<span class="matchup-name">{win["name"]}</span></div>'
        f'<div class="matchup-score"><span class="matchup-score-val">{score}</span>'
        '<span class="matchup-score-label">Score final</span></div>'
        '<div class="matchup-team">'
        f'<img class="matchup-logo" src="{lose["image"]}" alt="Logo {lose["name"]} — Worlds 2026" loading="lazy">'
        f'<span class="matchup-name">{lose["name"]}</span></div></div>'
    )


def build_spec(match_id, win, lose):
    score_val = f'{win["gameWins"]} – {lose["gameWins"]}'
    score_txt = f'{win["gameWins"]}-{lose["gameWins"]}'
    title = f'{win["name"]} vs {lose["name"]} : résumé du match'
    meta_desc = (f'{win["name"]} s\'impose {score_txt} face à {lose["name"]} '
                 f'lors du premier tour du système suisse des Worlds 2026.')
    intro = (f'<p class="lead">{win["name"]} a battu {lose["name"]} {score_txt} '
             f'lors du premier tour du système suisse des Worlds 2026.</p>')
    deroule = (f'{win["name"]} a pris le dessus sur {lose["name"]} dans ce Bo1 d\'ouverture '
               f'du système suisse. Une victoire nette sur le score de {score_txt}, qui lance '
               f'idéalement son parcours dans la compétition.')
    suite = (f'Au système suisse, il faut 3 victoires pour se qualifier et 3 défaites pour être '
             f'éliminé. {win["name"]} démarre donc avec un bilan de 1-0, tandis que {lose["name"]} '
             f'se retrouve à 0-1 et devra réagir dès le prochain tour.')
    body = (CTA + "\n\n" + matchup(win, lose, score_val) +
            f'<h2>Le déroulé du match</h2><p>{deroule}</p>\n'
            f'<h2>La suite pour les deux équipes</h2><p>{suite}</p>\n' + SOURCE)

    vod = cloud_recap.fetch_vods_html(match_id)
    if vod:
        body = body.replace(SOURCE, f'<h2>Revivre le match</h2>{vod}\n{SOURCE}')

    slug = f'{win["code"].lower()}-vs-{lose["code"].lower()}-resume'
    return {
        "match_id": match_id, "slug": slug, "title": title, "meta_title": title,
        "meta_description": meta_desc, "h1": title, "intro": intro, "body": body,
        "related": [
            {"slug": "planning", "anchor": "planning des Worlds"},
            {"slug": "classement", "anchor": "classement des Worlds"},
            {"slug": "resultats", "anchor": "résultats en direct"},
            {"slug": "blog", "anchor": "tous les résumés"},
        ],
    }


def main():
    live = json.load(open(os.path.join(ROOT, "data", "live.json"), encoding="utf-8"))
    published = set()
    for fn in os.listdir(os.path.join(ROOT, "content")):
        if fn.endswith(".json"):
            try:
                d = json.load(open(os.path.join(ROOT, "content", fn), encoding="utf-8"))
                if d.get("match_id"):
                    published.add(d["match_id"])
            except Exception:
                pass

    specs = []
    for st in live.get("stages", []):
        for m in st.get("matches", []):
            if m.get("state") != "completed" or m["id"] in published:
                continue
            t = m["teams"]
            a, b = t[0], t[1]
            for team in (a, b):
                team["name"] = NAME_MAP.get(team.get("name", ""), team.get("name", ""))
                img = team.get("image") or ""
                team["image"] = img.replace("http://", "https://")
            win, lose = (a, b) if a.get("outcome") == "win" else (b, a)
            specs.append(build_spec(m["id"], win, lose))

    if not specs:
        print("Rien à publier.")
        return 0

    slugs = []
    for spec in specs:
        p = f'/tmp/spec_{spec["match_id"]}.json'
        with open(p, "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False)
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "publish_recap.py"), p, "--no-deploy"],
                           cwd=ROOT, capture_output=True, text=True)
        print((r.stdout or "").strip())
        if r.stderr:
            print("STDERR:", r.stderr.strip())
        if r.returncode == 0:
            slugs.append(spec["slug"])

    # déploiement unique
    print("\nDéploiement...")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "deploy.py")],
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    print((r.stdout or r.stderr or "").strip())
    print("\nPUBLIÉ:", ", ".join(slugs))
    return 0 if r.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
