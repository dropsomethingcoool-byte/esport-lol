#!/usr/bin/env python3
"""
Générateur de site statique — ariege-malin.fr
==============================================
Construit le dossier `site/` (déployable tel quel sur cPanel) à partir de :
  - content/*.json   : contenu de chaque page
  - data/nav.json    : structure du menu (silos)
  - templates/base.html : squelette HTML partagé

URLs propres (sans .html) via structure en dossiers :
  index.json        -> site/index.html      -> https://ariege-malin.fr/
  serrurier-ariege.json -> site/serrurier-ariege/index.html -> https://ariege-malin.fr/serrurier-ariege/

Usage :  python3 scripts/generate.py
Dépendances : aucune (stdlib uniquement).
"""
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content")
TEMPLATE_PATH = os.path.join(ROOT, "templates", "base.html")
NAV_PATH = os.path.join(ROOT, "data", "nav.json")
ASSETS_DIR = os.path.join(ROOT, "assets")
SITE_DIR = os.path.join(ROOT, "site")
PHP_DIR = os.path.join(ROOT, "php")

BASE_URL = "https://esport-lol.com"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def slug_to_file(slug):
    """Chemin du fichier généré (structure en dossiers pour URL propres)."""
    return "index.html" if slug == "index" else f"{slug}/index.html"


def url_for(slug):
    """URL relative du site (propre, sans .html)."""
    return "/" if slug == "index" else f"/{slug}/"


def abs_url(slug):
    return f"{BASE_URL}{url_for(slug)}"


def cover_image_url(page):
    """URL JPG de la couverture d'article (og:image / JSON-LD), ou None.
    Les réseaux sociaux ne lisent pas le webp -> on renvoie la version .jpg."""
    m = re.search(r'<img[^>]*class="article-cover"[^>]*src="([^"]+)"', page.get("body", ""))
    if not m:
        return None
    src = m.group(1)
    url = src if src.startswith("http") else BASE_URL + src
    return url.rsplit(".webp", 1)[0] + ".jpg"


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
def build_nav(nav):
    parts = []
    # « Accueil » retiré du menu (le logo du header pointe déjà vers l'accueil)

    for silo in nav.get("silos", []):
        if silo.get("pages"):
            children = "".join(
                f'<a href="{url_for(p["slug"])}">{p["label"]}</a>'
                for p in silo["pages"]
            )
            hub_label = silo.get("hub_label") or f"Tout {silo['label'].lower()}"
            parts.append(
                f'<div class="nav-item has-children">{silo["label"]}'
                f'<div class="nav-dropdown"><a href="{url_for(silo["slug"])}">{hub_label}</a>'
                f"{children}</div></div>"
            )
        else:
            parts.append(f'<a class="nav-item" href="{url_for(silo["slug"])}">{silo["label"]}</a>')

    for s in nav.get("static", []):
        parts.append(f'<a class="nav-item" href="{url_for(s["slug"])}">{s["label"]}</a>')

    return "".join(parts)


def build_footer(nav):
    cols = []
    for silo in nav.get("silos", []):
        links = [f'<a href="{url_for(silo["slug"])}">{silo["label"]}</a>']
        links += [
            f'<a href="{url_for(p["slug"])}">{p["label"]}</a>'
            for p in silo.get("pages", [])
        ]
        cols.append(f'<div><h3>{silo["label"]}</h3><ul><li>' + "</li><li>".join(links) + "</li></ul></div>")

    static_links = "".join(
        f'<li><a href="{url_for(s["slug"])}">{s["label"]}</a></li>'
        for s in nav.get("static", [])
    )
    static_links += '<li><a href="/confidentialite/">Confidentialité</a></li>'
    cols.append(f'<div><h3>Le site</h3><ul>{static_links}</ul></div>')

    return "".join(cols)


# ---------------------------------------------------------------------------
# Breadcrumb
# ---------------------------------------------------------------------------
def build_breadcrumb(page, nav):
    silo_label = None
    silo_slug = None
    for silo in nav.get("silos", []):
        if silo.get("slug") == page.get("silo"):
            silo_label = silo["label"]
            silo_slug = silo["slug"]
            break

    items = ['<a href="/">Accueil</a>']
    if silo_label and page.get("type") not in ("home",):
        items.append(f'<a href="{url_for(silo_slug)}">{silo_label}</a>')
    items.append(f'<span class="current">{page.get("h1", page.get("title", ""))}</span>')

    return '<nav class="breadcrumb" aria-label="Fil d\u2019Ariane">' + ' <span class="sep">›</span> '.join(items) + "</nav>"


# ---------------------------------------------------------------------------
# Author line
# ---------------------------------------------------------------------------
def build_author_line(page):
    d = page.get("date_modified", "")
    return (
        '<div class="author-line">'
        f"<span class=\"trust\">✓ Mis à jour le <time datetime=\"{d}\">{d}</time></span>"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Related (maillage interne sortant)
# ---------------------------------------------------------------------------
def build_related(page):
    related = page.get("related", [])
    if not related:
        return ""
    links = []
    for r in related:
        if isinstance(r, dict):
            slug = r.get("slug")
            anchor = r.get("anchor") or slug.replace("-", " ").title()
        else:
            slug = r
            anchor = slug.replace("-", " ").title()
        links.append(f'<a href="{url_for(slug)}">{anchor}</a>')
    return (
        '<section class="related"><h2>À lire aussi</h2>'
        f'<div class="related-links">{"".join(links)}</div></section>'
    )


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
def build_jsonld(page):
    ptype = page.get("type", "page")
    date_mod = page.get("date_modified", "")
    date_pub = page.get("date_published", date_mod)

    if ptype == "home":
        data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "name": "esport-lol",
                    "url": f"{BASE_URL}/",
                    "inLanguage": "fr-FR",
                },
                {
                    "@type": "SportsEvent",
                    "name": "Worlds 2026 — League of Legends",
                    "description": "Championnat du monde de League of Legends 2026 : planning, résultats et classement.",
                    "startDate": "2026-10-15",
                    "endDate": "2026-11-05",
                    "eventStatus": "https://schema.org/EventScheduled",
                    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                    "location": {
                        "@type": "Place",
                        "name": "Allen (Texas)",
                        "address": {"@type": "PostalAddress", "addressLocality": "Allen", "addressRegion": "Texas", "addressCountry": "US"},
                    },
                    "organizer": {
                        "@type": "Organization",
                        "name": "Riot Games",
                        "url": "https://www.riotgames.com",
                    },
                    "url": f"{BASE_URL}/",
                    "inLanguage": "fr-FR",
                },
            ],
        }
    elif ptype in ("comparatif", "article"):
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": page.get("h1", page.get("title", "")),
            "description": page.get("meta_description", ""),
            "publisher": {
                "@type": "Organization",
                "name": "esport-lol",
                "url": BASE_URL,
            },
            "datePublished": date_pub,
            "dateModified": date_mod,
            "mainEntityOfPage": abs_url(page["slug"]),
            "inLanguage": "fr-FR",
        }
        cover = cover_image_url(page)
        if cover:
            data["image"] = cover
        faq = page.get("faq")
        if faq:
            data = {
                "@context": "https://schema.org",
                "@graph": [
                    data,
                    {
                        "@type": "FAQPage",
                        "mainEntity": [
                            {
                                "@type": "Question",
                                "name": q["question"],
                                "acceptedAnswer": {"@type": "Answer", "text": q["answer"]},
                            }
                            for q in faq
                        ],
                    },
                ],
            }
    elif ptype == "about":
        data = {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "name": page.get("h1", "À propos"),
            "url": abs_url(page["slug"]),
            "inLanguage": "fr-FR",
        }
    elif ptype == "contact":
        data = {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": page.get("h1", "Contact"),
            "url": abs_url(page["slug"]),
            "inLanguage": "fr-FR",
        }
    else:
        data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": page.get("h1", page.get("title", "")),
            "url": abs_url(page["slug"]),
            "inLanguage": "fr-FR",
        }

    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


# ---------------------------------------------------------------------------
# Encart "Demander un devis / un tarif" dans les TOP 5/10 (pages comparatif)
# ---------------------------------------------------------------------------
def inject_pro_cta(body, page):
    """Ajoute un bouton de mise en relation sous chaque pro d'un TOP 5/10."""
    silo = page.get("silo", "artisans")
    label = "Demander un devis" if silo == "artisans" else "Demander un tarif"
    slug = html.escape(page.get("slug", ""), quote=True)

    def process_ol(m):
        inner = m.group(1)

        def process_li(lm):
            li = lm.group(0)
            if "pro-name" not in li:
                return li
            nm = re.search(r'<p class=["\']pro-name["\']>(.*?)</p>', li, re.S)
            name = ""
            if nm:
                name = re.sub(r"<[^>]+>", "", nm.group(1)).strip()
            btn = (
                '<p class="pro-cta-wrap">'
                f'<button type="button" class="pro-cta" '
                f'data-pro="{html.escape(name, quote=True)}" '
                f'data-page="{slug}" '
                f'data-intent="{html.escape(label, quote=True)}">{label}</button>'
                "</p>"
            )
            return re.sub(r"</li>\s*$", btn + "</li>", li)

        new_inner = re.sub(r"<li[^>]*>.*?</li>", process_li, inner, flags=re.S)
        return m.group(0).replace(inner, new_inner)

    return re.sub(r'<ol class="top(?:5|10)">(.*?)</ol>', process_ol, body, flags=re.S)


# ---------------------------------------------------------------------------
# Table des matières (auto) pour les articles longs
# ---------------------------------------------------------------------------
def build_toc(body):
    """Génère une TOC ancrée depuis les H2, si le body a au moins 3 H2."""
    hs = re.findall(r"<h2[^>]*>(.*?)</h2>", body, flags=re.S)
    if len(hs) < 3:
        return ""
    items = []
    for i, h in enumerate(hs):
        text = re.sub(r"<[^>]+>", "", h).strip()
        if not text:
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        items.append(f'<li><a href="#{slug}">{text}</a></li>')
    if not items:
        return ""
    return (
        '<nav class="toc" aria-label="Sommaire">'
        '<span class="toc-title">Sommaire</span>'
        f'<ol>{"".join(items)}</ol></nav>'
    )


def add_heading_ids(body):
    """Ajoute un id ancré aux H2 (pour la TOC)."""
    def repl(m):
        attrs = m.group(1)
        inner = m.group(2)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return f'<h2{attrs} id="{slug}">{inner}</h2>'
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body, flags=re.S)


# ---------------------------------------------------------------------------
# Main content assembly
# ---------------------------------------------------------------------------
def build_main(page, nav):
    ptype = page.get("type", "page")

    if ptype == "home":
        return '<main class="content">' + page.get("body", "") + "</main>"

    breadcrumb = build_breadcrumb(page, nav)
    author_line = build_author_line(page)
    related = build_related(page)
    lead = page.get("intro", "")
    body = page.get("body", "")
    if ptype == "comparatif":
        body = inject_pro_cta(body, page)

    # Table des matières pour les articles longs (seulement les articles blog)
    if ptype == "article" and len(re.findall(r"<h2[^>]*>", body)) >= 3:
        body = add_heading_ids(body)
        toc = build_toc(body)
        body = toc + body

    return (
        '<main class="content">'
        f"{breadcrumb}"
        '<article>'
        '<header class="page-header">'
        f'<h1>{page.get("h1", page.get("title", ""))}</h1>'
        f'{lead}'
        f"{author_line}"
        "</header>"
        f"{body}"
        f"{related}"
        "</article>"
        "</main>"
    )


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def render(page, nav):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()

    og_image = cover_image_url(page) or f"{BASE_URL}/assets/img/og-image.png"

    replacements = {
        "__META_TITLE__": page.get("meta_title", page.get("title", "")),
        "__META_DESC__": page.get("meta_description", ""),
        "__CANONICAL__": abs_url(page["slug"]),
        "__OG_IMAGE__": og_image,
        "__JSONLD__": build_jsonld(page),
        "__NAV__": build_nav(nav),
        "__MAIN__": build_main(page, nav),
        "__FOOTER__": build_footer(nav),
    }
    for k, v in replacements.items():
        tpl = tpl.replace(k, v)

    out = os.path.join(SITE_DIR, slug_to_file(page["slug"]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(tpl)
    return out


# ---------------------------------------------------------------------------
# Sitemap / robots
# ---------------------------------------------------------------------------
def build_sitemap(pages):
    entries = []
    for p in pages:
        entries.append(
            "  <url>\n"
            f"    <loc>{abs_url(p['slug'])}</loc>\n"
            f"    <lastmod>{p.get('date_modified', '')}</lastmod>\n"
            "  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    with open(os.path.join(SITE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def build_robots():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"\nSitemap: {BASE_URL}/sitemap.xml\n"
    )
    with open(os.path.join(SITE_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(content)


def build_htaccess():
    content = (
        "# Redirections permanentes (anciennes URLs)\n"
        "RedirectMatch 301 ^/paris(/.*)?$ /parier-worlds-lol/\n"
        "\n"
        "# Fichiers racine : slash final -> sans slash (évite les 404 des crawlers)\n"
        "RedirectMatch 301 ^/([^/]+\\.[A-Za-z0-9]+)/$ /$1\n"
        "\n"
        "# Lien affilié BetNinja (go/lol -> trackeur partenaire)\n"
        "RedirectMatch 302 ^/go/lol$ https://media.betninjapartners.com/redirect.aspx?pid=4008&bid=1497\n"
    )
    with open(os.path.join(SITE_DIR, ".htaccess"), "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    nav = load_json(NAV_PATH)

    # Rebuild propre : on repart d'un site/ vide (évite les fichiers obsolètes).
    if os.path.isdir(SITE_DIR):
        shutil.rmtree(SITE_DIR)
    os.makedirs(SITE_DIR)

    # Copie des assets
    shutil.copytree(ASSETS_DIR, os.path.join(SITE_DIR, "assets"))

    # Favicon à la racine (pour /favicon.ico, demandé par les navigateurs)
    ico = os.path.join(ASSETS_DIR, "img", "favicon.ico")
    if os.path.exists(ico):
        shutil.copy2(ico, os.path.join(SITE_DIR, "favicon.ico"))

    # Données live (rechargées par le front toutes les 60s)
    live = os.path.join(ROOT, "data", "live.json")
    if os.path.exists(live):
        shutil.copy2(live, os.path.join(SITE_DIR, "live.json"))

    # Fichiers PHP (endpoints) copiés à la racine du site
    if os.path.isdir(PHP_DIR):
        for fn in os.listdir(PHP_DIR):
            if fn.endswith(".php"):
                shutil.copy2(os.path.join(PHP_DIR, fn), os.path.join(SITE_DIR, fn))

    # Charger et trier les pages
    files = sorted(os.listdir(CONTENT_DIR)) if os.path.isdir(CONTENT_DIR) else []
    pages = []
    for fn in files:
        if fn.endswith(".json"):
            pages.append(load_json(os.path.join(CONTENT_DIR, fn)))

    order = {"home": 0, "about": 1, "contact": 2, "page": 3, "hub": 4, "comparatif": 5, "article": 5}
    pages.sort(key=lambda p: (order.get(p.get("type"), 9), p.get("slug", "")))

    for p in pages:
        out = render(p, nav)
        print(f"  ✓ {p['slug']} -> {os.path.relpath(out, ROOT)}")

    build_sitemap(pages)
    build_robots()
    build_htaccess()
    print(f"\nGénération terminée : {len(pages)} pages -> {os.path.relpath(SITE_DIR, ROOT)}")
    print("sitemap.xml + robots.txt générés.")


if __name__ == "__main__":
    main()
