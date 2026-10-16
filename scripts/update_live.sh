#!/bin/bash
# Mise à jour live (scrape + upload de live.json) — silencieux en cas de succès.
set -e
cd /Users/charlesploteau/esport-lol || { echo "⚠️ esport-lol: dossier introuvable"; exit 1; }

python3 scripts/scrape_live.py >/dev/null 2>&1 \
  || { echo "⚠️ esport-lol: échec scrape_live.py"; exit 1; }

python3 scripts/deploy_live.py >/dev/null 2>&1 \
  || { echo "⚠️ esport-lol: échec deploy_live.py"; exit 1; }

# Succès : rien à afficher (silencieux pour ne pas spammer Discord)
exit 0
