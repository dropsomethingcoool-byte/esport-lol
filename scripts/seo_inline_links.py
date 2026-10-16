#!/usr/bin/env python3
"""Injecte des liens internes contextualisés (dans le texte) dans les pages équipe.
Relançable sans risque (idempotent : n'ajoute un lien que s'il n'existe pas déjà).
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")


def inject(body):
    # 1. lien contextuel sur la 1re mention de "Worlds LoL 2026"/"Worlds LoL" dans un <p>
    if 'href="/planning/"' not in body:
        body = re.sub(
            r'(<p>)((?!<a).)*?(Worlds LoL 2026|Worlds LoL)',
            lambda m: m.group(0).replace(
                m.group(3),
                f'<a href="/planning/">{m.group(3)}</a>', 1),
            body, count=1)
    # 2. paragraphe de clôture avec 2 liens contextuels (si pas déjà présent)
    if 'classement des Worlds LoL' not in body:
        body += ('<p>Retrouvez le <a href="/classement/">classement des Worlds LoL</a> '
                 'et les <a href="/blog/">résumés de matchs des Worlds</a> pour suivre '
                 'toute la compétition.</p>')
    return body


def main():
    n = 0
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.startswith('equipe-') or not fn.endswith('.json'):
            continue
        path = os.path.join(CONTENT, fn)
        d = json.load(open(path, encoding='utf-8'))
        before = d.get('body', '')
        after = inject(before)
        if after != before:
            d['body'] = after
            json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            n += 1
    print(f"✓ {n} pages équipe : liens contextualisés injectés")


if __name__ == '__main__':
    main()
