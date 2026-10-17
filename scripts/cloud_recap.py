#!/usr/bin/env python3
"""Runner cloud (GitHub Actions) du blog esport-lol.

Fait, de façon 100 % déterministe (stdlib uniquement) :
  1. récupère live.json (https://esport-lol.com/live.json)
  2. détecte les matchs `completed` pas encore publiés (champ `match_id` dans content/*.json)
  3. pour chacun : rédige l'article via l'API DeepSeek (JSON structuré), ajoute la VOD
  4. publie via scripts/publish_recap.py --no-deploy (crée le JSON + met à jour le blog + régénère)
  5. déploie via scripts/deploy.py (FTP, creds en variables d'env)

Variables d'environnement requises :
  DEEPSEEK_API_KEY, DEEPSEEK_MODEL (défaut deepseek-v4-pro)
  FTP_HOST, FTP_USER, FTP_PASSWORD, FTP_PATH
"""
import json
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
LIVE_URL = "https://esport-lol.com/live.json"
DS_URL = "https://api.deepseek.com/chat/completions"
DS_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
LOL_API = "https://esports-api.lolesports.com/persisted/gw"
LOL_KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"

STAGE_CONTEXT = {
    "play_ins": ("le play-in", "Le vainqueur poursuit vers la qualification pour le système suisse ; "
                 "le perdant bascule dans le bas du tableau et devra gagner pour rester en vie."),
    "swiss": ("le système suisse", "Au système suisse, il faut 3 victoires pour se qualifier et 3 défaites pour être éliminé."),
    "knockouts": ("la phase finale", "En phase finale, chaque série est éliminatoire."),
}


def http_json(url, headers=None, data=None, timeout=40):
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def fetch_live():
    with urllib.request.urlopen(LIVE_URL, timeout=40) as r:
        return json.loads(r.read().decode())


def published_match_ids():
    ids = set()
    for fn in os.listdir(CONTENT):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(CONTENT, fn), encoding="utf-8") as f:
                d = json.load(f)
            if d.get("match_id"):
                ids.add(d["match_id"])
        except Exception:
            pass
    return ids


def completed_matches(live):
    out = []
    for st in live.get("stages", []):
        for m in st.get("matches", []):
            if m.get("state") == "completed":
                out.append((st.get("slug"), st.get("name"), m))
    return out


def fetch_vods_html(match_id):
    try:
        d = http_json(f"{LOL_API}/getEventDetails?hl=fr-FR&id={match_id}",
                      headers={"x-api-key": LOL_KEY})
        games = ((d.get("data", {}).get("event", {}) or {}).get("match") or {}).get("games") or []
        urls = []
        loc = None
        for g in games:
            if g.get("state") != "completed":
                continue
            for v in (g.get("vods") or []):
                if v.get("provider") == "youtube":
                    if v.get("locale") == "fr-FR":
                        urls.append(f"https://www.youtube.com/watch?v={v.get('parameter')}")
                        loc = "fr-FR"
                    elif v.get("locale") == "en-US" and loc != "fr-FR":
                        urls.append(f"https://www.youtube.com/watch?v={v.get('parameter')}")
                        loc = loc or "en-US"
                    break
        uniq = sorted(set(urls))
        if not uniq:
            return ""
        e = uniq[0].replace("/watch?v=", "/embed/")
        return (f'<div class="vod-embed"><iframe src="{e}" title="Revivre le match (VOD)" loading="lazy" '
                f'allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
                f'gyroscope; picture-in-picture"></iframe></div>')
    except Exception:
        return ""


def write_article(team_a, team_b, winner, score_a, score_b, stage_slug, stage_name):
    stage_label, stage_hint = STAGE_CONTEXT.get(stage_slug, (stage_name, ""))
    prompt = (
        "Tu es rédacteur esport pour un site français. Écris un article récap d'un match des "
        "Worlds League of Legends 2026. Retourne UNIQUEMENT un objet JSON valide (sans texte autour), "
        "avec exactement ces clés : title, meta_title, meta_description, h1, intro, body.\n\n"
        f"DONNÉES : équipes {team_a['name']} ({team_a['code']}) contre {team_b['name']} ({team_b['code']}). "
        f"Score final : {team_a['code']} {score_a} - {score_b} {team_b['code']}. "
        f"Vainqueur : {winner}. Stage : {stage_label}.\n"
        f"Contexte du stage : {stage_hint}\n\n"
        "RÈGLES :\n"
        "- title et h1 au format « <Équipe A> vs <Équipe B> : résumé du match ».\n"
        "- intro = une balise <p class=\"lead\">…</p> annonçant le résultat.\n"
        "- body = HTML avec deux sections H2 : « Le déroulé de la série » (déduis du score : "
        "3-2 = série serrée jusqu'à la manche décisive, 3-0 = domination) et « La suite pour les "
        "deux équipes » (gagnant + perdant, d'après le contexte du stage).\n"
        "- N'invente AUCUN détail absent : pas de MVP, pas de score par manche, pas de statistiques.\n"
        "- meta_title court (≤ 60 caractères), meta_description 1-2 phrases (≤ 160 caractères).\n"
        "- Français correct, ton neutre et factuel."
    )
    payload = {
        "model": DS_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096,
        "temperature": 0.4,
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(payload).encode()
    r = http_json(DS_URL,
                  headers={"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
                           "Content-Type": "application/json"},
                  data=data)
    content = r["choices"][0]["message"]["content"]
    return json.loads(content)


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def main():
    live = fetch_live()
    # Sauvegarde le live.json frais (pour que generate.py le copie dans site/,
    # et ne PAS écraser la version fraîche du serveur au déploiement)
    with open(os.path.join(ROOT, "data", "live.json"), "w", encoding="utf-8") as f:
        json.dump(live, f, ensure_ascii=False)
    done = published_match_ids()
    matches = completed_matches(live)

    new = [(s, n, m) for (s, n, m) in matches if m["id"] not in done]
    if not new:
        print("Rien de nouveau : tous les matchs terminés sont déjà publiés.")
        return 0

    published = []
    for stage_slug, stage_name, m in new:
        t = m["teams"]
        a, b = t[0], t[1]
        winner = a["name"] if a.get("outcome") == "win" else b["name"]
        try:
            art = write_article(a, b, winner, a.get("gameWins", "?"), b.get("gameWins", "?"),
                                stage_slug, stage_name)
        except Exception as e:
            print(f"ERREUR rédaction {m['id']} : {e}", file=sys.stderr)
            continue

        vods = fetch_vods_html(m["id"])
        if vods and "Revivre le match" not in art.get("body", ""):
            art["body"] = art.get("body", "") + f"<h2>Revivre le match</h2>{vods}"

        spec = {
            "match_id": m["id"],
            "slug": art.get("slug") or f"{a['code'].lower()}-vs-{b['code'].lower()}-resume",
            "title": art["title"], "meta_title": art["meta_title"],
            "meta_description": art["meta_description"], "h1": art["h1"],
            "intro": art["intro"], "body": art["body"],
            "related": [{"slug": "planning", "anchor": "planning des Worlds"},
                        {"slug": "classement", "anchor": "classement des Worlds"},
                        {"slug": "resultats", "anchor": "résultats en direct"},
                        {"slug": "blog", "anchor": "tous les résumés"}],
        }
        spec_path = f"/tmp/spec_{m['id']}.json"
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False)
        r = run([sys.executable, os.path.join(ROOT, "scripts", "publish_recap.py"), spec_path, "--no-deploy"])
        if r.returncode != 0:
            print(f"ERREUR publication {m['id']} : {r.stderr}", file=sys.stderr)
            continue
        published.append(spec["slug"])
        print(f"✓ publié : {spec['slug']}")

    # déploiement unique
    if published:
        r = run([sys.executable, os.path.join(ROOT, "scripts", "deploy.py")], timeout=300)
        print(r.stdout or r.stderr)
        if r.returncode != 0:
            print("ERREUR déploiement", file=sys.stderr)
            return 1
    print("PUBLIÉ:", ", ".join(published))
    return 0


if __name__ == "__main__":
    sys.exit(main())
