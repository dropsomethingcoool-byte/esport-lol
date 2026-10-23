#!/usr/bin/env python3
"""Nettoie et normalise la fin des récaps : retire les fragments cassés
(<p>, source-line, vod) puis reconstruit proprement : VOD puis source."""
import json
import os
import re

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

VODS = {
    "fur-vs-c9-resume": "BU5pD9sdKYY",
    "kc-vs-cloud9-resume": "P43KhERU89A",
    "kc-vs-mvk-resume": "V_4YZBC-VhY",
    "mvk-vs-fur-resume": "B8rN-jsBP14",
    "mvk-vs-furia-resume": "F8ev1IEAulw",
    "karmine-corp-remporte-play-in": "IFd4x-jubAw",
}

SOURCE = ('<p class="source-line">Source : <a href="https://lolesports.com" '
          'rel="nofollow noopener" target="_blank">Lolesports</a> — '
          'données officielles du match.</p>')


def vod_section(vid):
    return (
        '<h2>Revivre le match</h2>'
        f'<div class="vod-embed"><iframe src="https://www.youtube.com/embed/{vid}" '
        'title="Revivre le match (VOD)" loading="lazy" allowfullscreen '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>'
    )


def clean_tail(body):
    # retire les blocs VOD (quel que soit leur contenu)
    body = re.sub(r'<h2>Revivre le match</h2><div class="vod-embed">.*?</div>', '', body, flags=re.S)
    # retire les source-line (même cassées)
    body = re.sub(r'<p\s*\n?\s*class="source-line">.*?</p>', '', body, flags=re.S)
    # retire les <p> orphelins laissés par les réparations précédentes
    body = re.sub(r'<p\s*>', '', body)
    return body.rstrip()


for slug, vid in VODS.items():
    p = os.path.join(CONTENT, f"{slug}.json")
    d = json.load(open(p, encoding="utf-8"))
    body = clean_tail(d["body"])
    d["body"] = body + "\n" + vod_section(vid) + "\n" + SOURCE
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # vérif
    ok_src = d["body"].endswith('données officielles du match.</p>')
    ok_no_break = '<p \nclass' not in d["body"] and '<p\nclass' not in d["body"]
    print(f"  {'✓' if (ok_src and ok_no_break) else '✗'} {slug}")
