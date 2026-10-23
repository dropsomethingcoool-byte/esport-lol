#!/usr/bin/env python3
"""Ajoute la section « Revivre le match » (VOD) aux récaps qui n'en ont pas.
Idempotent : saute si un iframe est déjà présent."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

VODS = {
    "fur-vs-c9-resume": "BU5pD9sdKYY",
    "kc-vs-mvk-resume": "V_4YZBC-VhY",
    "mvk-vs-fur-resume": "B8rN-jsBP14",
    "karmine-corp-remporte-play-in": "IFd4x-jubAw",
}


def vod_section(vid, title="Revivre le match (VOD)"):
    return (
        f'<h2>Revivre le match</h2>'
        f'<div class="vod-embed"><iframe src="https://www.youtube.com/embed/{vid}" '
        f'title="{title}" loading="lazy" allowfullscreen '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>'
    )


for slug, vid in VODS.items():
    p = os.path.join(CONTENT, f"{slug}.json")
    d = json.load(open(p, encoding="utf-8"))
    body = d["body"]
    if "iframe" in body or "youtube" in body:
        print(f"  = {slug}: VOD déjà présente")
        continue
    # insérer la section VOD à la fin (après la source-line, c'est plus logique avant la source)
    # on la place juste avant la source-line si présente, sinon en fin
    if 'class="source-line"' in body:
        i = body.find('class="source-line"')
        # reculer jusqu'au début du <p class="source-line">
        j = body.rfind('<p class="source-line"', 0, i)
        if j == -1:
            j = i
        body = body[:j] + vod_section(vid) + "\n" + body[j:]
    else:
        body = body.rstrip() + "\n" + vod_section(vid)
    d["body"] = body
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  ✓ {slug}: VOD ajoutée ({vid})")
