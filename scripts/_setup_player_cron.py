#!/usr/bin/env python3
"""Remplit data/backlog.json avec les 13 joueurs restants (pour le cron quotidien)."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
BACKLOG = os.path.join(ROOT, "data", "backlog.json")

with open(os.path.join(ROOT, "data", "player_photos.json"), encoding="utf-8") as f:
    photos = json.load(f)

def https(u):
    return u.replace("http://", "https://") if u else u

# slug -> (pseudo, role, pays, team, team_slug, clé photo, facts)
P = [
    ("joueur-hans-sama", "Hans Sama", "ADC", "France", "G2 Esports", "equipe-g2-esports", "hans sama",
     "ADC français de G2 Esports, l'un des tireurs les plus capés d'Europe, passé par la LEC et la LCS. Réputé pour sa mécanique et sa régularité en teamfight."),
    ("joueur-chovy", "Chovy", "Midlane", "Corée du Sud", "Gen.G", "equipe-gen-g", "chovy",
     "Midlaner vedette de Gen.G, considéré comme la meilleure midlane du monde grâce à sa mécanique exceptionnelle. Multiple champion de LCK."),
    ("joueur-ruler", "Ruler", "ADC", "Corée du Sud", "Gen.G", "equipe-gen-g", "ruler",
     "ADC de Gen.G, champion du monde 2017 avec Samsung Galaxy. L'un des tireurs les plus titrés de l'histoire de League of Legends."),
    ("joueur-zeus", "Zeus", "Toplane", "Corée du Sud", "Hanwha Life Esports", "equipe-hanwha-life-esports", "zeus",
     "Toplaner de Hanwha Life Esports, double champion du monde (2023, 2024) avec T1. Élu MVP de la finale 2023."),
    ("joueur-gumayusi", "Gumayusi", "ADC", "Corée du Sud", "Hanwha Life Esports", "equipe-hanwha-life-esports", "gumayusi",
     "ADC de Hanwha Life Esports, double champion du monde (2023, 2024) avec T1. Un tireur fiable en phase décisive."),
    ("joueur-showmaker", "ShowMaker", "Midlane", "Corée du Sud", "Dplus Kia", "equipe-dplus-kia", "showmaker",
     "Midlaner de Dplus Kia, champion du monde 2020 avec DAMWON Gaming. Finaliste des Worlds 2021."),
    ("joueur-theshy", "TheShy", "Toplane", "Corée du Sud", "Invictus Gaming", "equipe-invictus-gaming", "theshy",
     "Toplaner d'Invictus Gaming, champion du monde 2018 et élu MVP de la finale. Légende de la toplane."),
    ("joueur-jackeylove", "JackeyLove", "ADC", "Chine", "Top Esports", "equipe-top-esports", "jackeylove",
     "ADC de Top Esports, champion du monde 2018 avec Invictus Gaming. L'une des stars de la LPL chinoise."),
    ("joueur-knight", "Knight", "Midlane", "Chine", "Bilibili Gaming", "equipe-bilibili-gaming", "knight",
     "Midlaner de Bilibili Gaming, MVP de la LPL. L'un des meilleurs joueurs chinois de sa génération."),
    ("joueur-viper", "Viper", "ADC", "Corée du Sud", "Bilibili Gaming", "equipe-bilibili-gaming", "viper",
     "ADC de Bilibili Gaming, champion du monde 2021 avec Edward Gaming. Un facteur X dans chaque série."),
    ("joueur-bin", "Bin", "Toplane", "Chine", "Bilibili Gaming", "equipe-bilibili-gaming", "bin",
     "Toplaner de Bilibili Gaming, finaliste des Worlds 2023 et 2024. Réputé pour ses initiations décisives."),
    ("joueur-corejj", "CoreJJ", "Support", "Corée du Sud", "Team Liquid", "equipe-team-liquid", "corejj",
     "Support de Team Liquid, champion du monde 2017 avec Samsung Galaxy. L'un des cerveaux les plus respectés du circuit."),
    ("joueur-brokenblade", "BrokenBlade", "Toplane", "Allemagne", "G2 Esports", "equipe-g2-esports", "brokenblade",
     "Toplaner de G2 Esports, l'un des toplaners les plus polyvalents d'Europe. Réputé pour sa large gamme de champions."),
]

pages = []
for slug, pseudo, role, country, team, team_slug, pkey, facts in P:
    pages.append({
        "slug": slug,
        "label": pseudo,
        "keyword": pseudo,
        "role": role,
        "country": country,
        "team": team,
        "team_slug": team_slug,
        "photo": https(photos.get(pkey, {}).get("photo", "")),
        "facts": facts,
    })

with open(BACKLOG, "w", encoding="utf-8") as f:
    json.dump({"pages": pages}, f, ensure_ascii=False, indent=2)
print(f"✓ backlog.json : {len(pages)} joueurs en file")
