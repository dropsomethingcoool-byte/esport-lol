#!/usr/bin/env python3
"""Validation SEO des 2 nouvelles pages Worlds (format + meilleurs champions)."""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def text(html):
    return re.sub(r"<[^>]+>", " ", html)

for slug in ["format-worlds-lol", "meilleurs-champions-worlds"]:
    p = json.load(open(os.path.join(ROOT, "content", slug + ".json"), encoding="utf-8"))
    errs, warns = [], []
    if len(p["meta_title"]) > 60:
        errs.append(f"meta_title > 60 ({len(p['meta_title'])})")
    if len(p["meta_description"]) > 160:
        errs.append(f"meta_description > 160 ({len(p['meta_description'])})")
    iw = len(text(p["intro"]).split())
    if iw > 50:
        errs.append(f"intro > 50 mots ({iw})")
    # H2 -> >= 2 H3
    parts = re.split(r"<h2>", p["body"])[1:]
    for i, part in enumerate(parts):
        n3 = len(re.findall(r"<h3>", part))
        if n3 < 2:
            errs.append(f"H2 #{i+1} a {n3} H3 (< 2)")
    # paragraphes < 60 mots, 1 <strong> chacun
    paras = re.findall(r"<p>(.*?)</p>", p["body"])
    long_paras = [len(text(x).split()) for x in paras if len(text(x).split()) >= 60]
    if long_paras:
        errs.append(f"paragraphes >= 60 mots : {long_paras}")
    bad_bold = [len(re.findall(r"<strong>", x)) for x in paras if len(re.findall(r"<strong>", x)) != 1]
    if bad_bold:
        errs.append(f"paragraphes sans exactement 1 <strong> : {bad_bold}")
    # liens internes
    links = re.findall(r'href="(/[^"]*)"', p["body"])
    total_words = len(text(p["body"]).split()) + iw
    print(f"{slug}: {total_words} mots totaux | {len(paras)} paragraphes | liens internes: {links}")
    print(f"  meta_title {len(p['meta_title'])}ch, meta_desc {len(p['meta_description'])}ch, intro {iw} mots")
    if errs:
        print("  ❌ ERREURS:", errs)
    else:
        print("  ✅ OK (règles respectées)")
