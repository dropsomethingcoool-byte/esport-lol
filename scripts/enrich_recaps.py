#!/usr/bin/env python3
"""Enrichit les récaps de match : bloc « matchup hero » (logos + score),
ligne source, logos téléchargés en local (recolorés si trop sombres).
Idempotent : ne ré-injecte pas si déjà présent."""
import json
import os
import re

from PIL import Image

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")
TEAMS_DIR = os.path.join(ROOT, "assets", "img", "teams")

# code -> (nom complet, fichier logo local)
TEAMS = {
    "KC": ("Karmine Corp", "kc.png"),
    "C9": ("Cloud9 Kia", "c9.png"),
    "MVK": ("MVK Esports", "mvk.png"),
    "FUR": ("FURIA", "fur.png"),
}

# slug -> (code A, code B, score A, score B)
RECAPS = {
    "fur-vs-c9-resume": ("FUR", "C9", 3, 1),
    "kc-vs-cloud9-resume": ("KC", "C9", 3, 2),
    "kc-vs-mvk-resume": ("KC", "MVK", 3, 0),
    "mvk-vs-fur-resume": ("MVK", "FUR", 3, 1),
    "mvk-vs-furia-resume": ("MVK", "FUR", 3, 0),
    "karmine-corp-remporte-play-in": ("KC", "MVK", 3, 0),
}

WHITE = (236, 236, 233)  # #ecece9, cohérent avec --text


def recolor_if_dark(path, threshold=110):
    """Si le logo est majoritairement sombre (noir), le recolorie en blanc.
    Garde la transparence. Retourne True si recoloré."""
    im = Image.open(path).convert("RGBA")
    px = list(im.getdata())
    op = [p for p in px if p[3] > 40]
    if not op:
        return False
    lum = sum((p[0] + p[1] + p[2]) / 3 for p in op) / len(op)
    if lum >= threshold:
        return False
    out = [(WHITE[0], WHITE[1], WHITE[2], p[3]) if p[3] > 0 else (0, 0, 0, 0) for p in px]
    im.putdata(out)
    im.save(path)
    return True


def ensure_logos():
    os.makedirs(TEAMS_DIR, exist_ok=True)
    for code, (name, fn) in TEAMS.items():
        p = os.path.join(TEAMS_DIR, fn)
        if os.path.exists(p):
            if recolor_if_dark(p):
                print(f"  ♻ {code} recoloré en blanc ({name})")
            else:
                print(f"  ✓ {code} ({name})")
        else:
            print(f"  ✗ {code} manquant : {fn}")


def matchup_html(ca, na, cb, nb, sa, sb):
    return (
        '<div class="matchup-hero">'
        f'<div class="matchup-team"><img class="matchup-logo" src="/assets/img/teams/{na}" '
        f'alt="Logo {ca}" loading="lazy"><span class="matchup-name">{ca}</span></div>'
        f'<div class="matchup-score"><span class="matchup-score-val">{sa} – {sb}</span>'
        '<span class="matchup-score-label">Score final</span></div>'
        f'<div class="matchup-team"><img class="matchup-logo" src="/assets/img/teams/{nb}" '
        f'alt="Logo {cb}" loading="lazy"><span class="matchup-name">{cb}</span></div>'
        '</div>'
    )


SOURCE_LINE = ('<p class="source-line">Source : <a href="https://lolesports.com" '
               'rel="nofollow noopener" target="_blank">Lolesports</a> — '
               'données officielles du match.</p>')


def inject(body, block, anchor_regex):
    """Injecte `block` juste avant la première occurrence de `anchor_regex`, sinon en tête."""
    m = re.search(anchor_regex, body)
    if m:
        return body[:m.start()] + block + body[m.start():]
    return block + body


def main():
    ensure_logos()
    for slug, (ca, cb, sa, sb) in RECAPS.items():
        p = os.path.join(CONTENT, f"{slug}.json")
        if not os.path.exists(p):
            print(f"  ✗ {slug}.json introuvable")
            continue
        d = json.load(open(p, encoding="utf-8"))
        body = d.get("body", "")
        na = TEAMS[ca][1]
        nb = TEAMS[cb][1]
        hero = matchup_html(TEAMS[ca][0], na, TEAMS[cb][0], nb, sa, sb)
        changed = []
        if 'class="matchup-hero"' not in body:
            # injecter avant le premier <h2> (juste après le bloc CTA)
            body = inject(body, hero, r'<h2')
            changed.append("matchup")
        if 'class="source-line"' not in body:
            body = body.rstrip() + "\n" + SOURCE_LINE
            changed.append("source")
        if changed:
            d["body"] = body
            json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"  ✓ {slug}: {' + '.join(changed)}")
        else:
            print(f"  = {slug}: déjà enrichi")


if __name__ == "__main__":
    main()
