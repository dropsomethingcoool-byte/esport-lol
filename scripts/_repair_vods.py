#!/usr/bin/env python3
"""Répare les récaps : retire les VOD cassées puis ré-insère proprement avant la source-line."""
import json
import os
import re

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")

SLUGS = ["fur-vs-c9-resume", "kc-vs-mvk-resume", "mvk-vs-fur-resume",
          "karmine-corp-remporte-play-in"]

VODS = {
    "fur-vs-c9-resume": "BU5pD9sdKYY",
    "kc-vs-mvk-resume": "V_4YZBC-VhY",
    "mvk-vs-fur-resume": "B8rN-jsBP14",
    "karmine-corp-remporte-play-in": "IFd4x-jubAw",
}

VOD_BLOCK_RE = re.compile(r'<h2>Revivre le match</h2><div class="vod-embed">.*?</div>', re.S)


def vod_section(vid):
    return (
        f'<h2>Revivre le match</h2>'
        f'<div class="vod-embed"><iframe src="https://www.youtube.com/embed/{vid}" '
        'title="Revivre le match (VOD)" loading="lazy" allowfullscreen '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>'
    )


for slug in SLUGS:
    p = os.path.join(CONTENT, f"{slug}.json")
    d = json.load(open(p, encoding="utf-8"))
    body = d["body"]
    # retire tout bloc VOD existant (cassé ou non)
    body, n = VOD_BLOCK_RE.subn("", body)
    # insère avant la source-line
    vid = VODS[slug]
    src = '<p class="source-line">'
    k = body.find(src)
    if k != -1:
        body = body[:k] + vod_section(vid) + "\n" + body[k:]
    else:
        body = body.rstrip() + "\n" + vod_section(vid)
    d["body"] = body
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  ✓ {slug}: VOD réinsérée proprement ({n} retirée)")
