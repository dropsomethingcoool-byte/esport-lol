#!/usr/bin/env python3
"""Cron réactif — publie les récaps des matchs terminés, toutes équipes confondues.

Flux (100 % déterministe, stdlib + Pillow non requis) :
  1. scrape le live frais (scrape_live.py -> data/live.json) puis déploie live.json
  2. détecte les matchs `completed` sans article (idempotent via match_id)
  3. rédige l'article (score + stage adaptés), ajoute la VOD (API lolesports)
  4. publie via publish_recap.py --no-deploy
  5. déploie le site

Sortie : les slugs publiés. RIEN si aucun nouveau match (silencieux -> cron no_agent).
"""
import json
import os
import subprocess
import sys

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)
import cloud_recap  # noqa: E402  (réutilise fetch_vods_html, published_match_ids, completed_matches)

CTA = ('<div class="cta-affiliate"><div class="cta-box">\n'
       '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
       '<div class="cta-box-title">Parier sur les Worlds LoL</div>\n'
       'Suivez les cotes des prochains matchs des Worlds 2026 et placez vos paris esport sur BetNinja.</p>\n'
       '<a class="cta-btn" href="/parier-worlds-lol/" data-go="L2dvL2xvbA==" rel="nofollow sponsored noopener" target="_blank">Parier sur les Worlds <span class="cta-arrow">→</span></a>\n'
       '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire.</p>\n'
       '</div></div>')

SOURCE = ('<p class="source-line">Source : <a href="https://lolesports.com" rel="nofollow noopener" target="_blank">Lolesports</a> — données officielles du match.</p>')


def norm_name(name):
    return name.title() if name.isupper() else name


def run(cmd, timeout=300):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)


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


def write_article(match_id, win, lose, stage_slug):
    w = win["gameWins"]
    l = lose["gameWins"]
    score_txt = f"{w}-{l}"
    score_val = f"{w} – {l}"

    if w == 1 and l == 0:
        deroule = (f'{win["name"]} a pris le dessus sur {lose["name"]} dans ce Bo1. '
                   f'Une victoire nette sur le score de 1-0.')
    elif w == 2 and l == 0:
        deroule = f'{win["name"]} s\'impose 2-0 face à {lose["name"]}, sans concéder la moindre manche.'
    elif w == 2 and l == 1:
        deroule = f'{win["name"]} s\'impose 2-1 face à {lose["name"]} au terme d\'une série disputée.'
    elif w == 3 and l == 0:
        deroule = f'{win["name"]} écrase {lose["name"]} 3-0, sans laisser la moindre manche.'
    elif w == 3 and l == 1:
        deroule = f'{win["name"]} s\'impose 3-1 face à {lose["name"]}.'
    elif w == 3 and l == 2:
        deroule = f'{win["name"]} s\'impose 3-2 face à {lose["name"]} au terme d\'une série accrochée.'
    else:
        deroule = f'{win["name"]} s\'impose {score_txt} face à {lose["name"]}.'

    if stage_slug == "play_ins":
        suite = (f'Grâce à cette victoire, {win["name"]} poursuit sa route vers le swiss stage. '
                 f'{lose["name"]} bascule dans le bas du tableau et devra gagner pour rester en vie.')
    elif stage_slug == "knockouts":
        suite = (f'En phase finale, chaque série est éliminatoire. {win["name"]} poursuit son parcours, '
                 f'tandis que {lose["name"]} est éliminé de la compétition.')
    else:  # swiss
        suite = (f'Au swiss stage, il faut 3 victoires pour se qualifier et 3 défaites pour être éliminé. '
                 f'{win["name"]} progresse dans le tableau, tandis que {lose["name"]} devra réagir dès le prochain tour.')

    h2_deroule = "Le déroulé du match" if w == 1 else "Le déroulé de la série"

    title = f'{win["name"]} vs {lose["name"]} : résumé du match'
    meta_desc = f'{win["name"]} s\'impose {score_txt} face à {lose["name"]} lors des Worlds 2026.'
    intro = f'<p class="lead">{win["name"]} a battu {lose["name"]} {score_txt} aux Worlds 2026.</p>'

    body = (CTA + "\n\n" + matchup(win, lose, score_val) +
            f'<h2>{h2_deroule}</h2><p>{deroule}</p>\n'
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
    # 1. scrape frais + live.json serveur à jour (bandeau live)
    run([sys.executable, os.path.join(SCRIPTS, "scrape_live.py")])
    run([sys.executable, os.path.join(SCRIPTS, "deploy_live.py")])

    # 2. détecter les matchs terminés sans article
    live = json.load(open(os.path.join(ROOT, "data", "live.json"), encoding="utf-8"))
    done = cloud_recap.published_match_ids()
    new = [(s, m) for (s, _, m) in cloud_recap.completed_matches(live) if m["id"] not in done]

    if not new:
        return 0  # silencieux (cron no_agent)

    # 3. rédiger + publier chaque récap
    slugs = []
    for stage_slug, m in new:
        a, b = m["teams"][0], m["teams"][1]
        for team in (a, b):
            team["name"] = norm_name(team.get("name", ""))
            team["image"] = (team.get("image") or "").replace("http://", "https://")
        win, lose = (a, b) if a.get("outcome") == "win" else (b, a)
        spec = write_article(m["id"], win, lose, stage_slug)
        p = f'/tmp/spec_{m["id"]}.json'
        with open(p, "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False)
        r = run([sys.executable, os.path.join(SCRIPTS, "publish_recap.py"), p, "--no-deploy"])
        if r.returncode == 0:
            slugs.append(spec["slug"])

    # 4. déploiement unique du site
    if slugs:
        run([sys.executable, os.path.join(SCRIPTS, "deploy.py")])

    print("Récaps publiés : " + ", ".join(slugs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
