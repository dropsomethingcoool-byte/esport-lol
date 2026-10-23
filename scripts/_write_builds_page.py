#!/usr/bin/env python3
"""Génère content/builds-lol.json (page evergreen : builds League of Legends)."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "content", "builds-lol.json")

KW = "build league of legends"

page = {
    "slug": "builds-lol",
    "type": "article",
    "title": "Build League of Legends : guide des builds LoL",
    "meta_title": "Build League of Legends : le guide des builds LoL",
    "meta_description": "Comment construire un build League of Legends : objets de base, bottes, objets mythiques, ordre d'achat et adaptation du build LoL à l'adversaire.",
    "h1": "Build League of Legends",
    "intro": (
        '<p class="lead">Un <strong>build league of legends</strong> désigne la liste d\'objets, '
        'de bottes et de composants qu\'un champion achète au fil d\'une partie. Ce guide explique '
        'comment le construire et l\'adapter à la situation.</p>'
    ),
    "silo": "blog",
    "body": "",
    "related": [
        {"slug": "runes-league-of-legends", "anchor": "Guide des runes LoL"},
        {"slug": "tier-list-lol", "anchor": "Tier List LoL"},
        {"slug": "blog", "anchor": "Blog League of Legends"},
    ],
    "date_modified": "2026-10-21",
    "date_published": "2026-10-21",
}

B = []

def h2(t): B.append(f"<h2>{t}</h2>")
def h3(t): B.append(f"<h3>{t}</h3>")
def p(t): B.append(f"<p>{t}</p>")

# ---------------------------------------------------------------- H2 1
h2("Qu'est-ce qu'un build dans League of Legends")
h3("La définition d'un build LoL")
p("<strong>Six emplacements</strong> attendent un objet terminé à la fin d'une partie : "
  "les trois objets de la rangée du haut, puis la rangée du bas. Un build complet "
  "correspond donc à six achats définitifs, plus des consommables.")
p("Le terme build englobe aussi l'ordre d'achat. Deux joueurs peuvent finir avec "
  "exactement les mêmes <strong>six objets</strong> et gagner la partie de façon très "
  "différente selon qu'ils ont pris une composante défensive tôt ou tard.")

h3("Build et page de runes, deux réglages distincts")
p("Le build ne remplace pas la page de runes : les deux se répondent. Une page axée "
  "sur les dégâts soutenus demande des objets qui prolongent les échanges, tandis qu'une "
  "page de burst appelle de la pénétration et de la <strong>puissance</strong>.")
p("Pour aller plus loin sur ce réglage parallèle, le <a href=\"/runes-league-of-legends/\">"
  "guide des runes League of Legends</a> détaille les <strong>branches</strong> et les éclats "
  "de statistiques.")

# ---------------------------------------------------------------- H2 2
h2("Les grandes familles d'objets dans League of Legends")
h3("Objets de dégâts et de puissance")
p("Les objets de puissance brute augmentent les sorts et les attaques. Ils conviennent aux "
  "mages, aux <strong>assassins</strong> et aux porteurs de dégâts à distance qui restent "
  "à l'arrière du combat d'équipe.")
p("Les objets de vitesse d'attaque, de dégâts critiques et de pénétration armorale forment "
  "une famille distincte. Ils ciblent les champions qui frappent <strong>souvent</strong> "
  "plutôt que fort.")

h3("Objets défensifs et objets de soutien")
p("La défense se décline en armure contre les dégâts physiques, en résistance magique contre "
  "les sorts, et en points de vie qui protègent des <strong>deux types</strong>. Un tank en "
  "achète trois ou quatre, un porteur de dégâts un seul en fin de partie.")
p("Les objets de soutien et de vision apportent boucliers, soins, accélérations ou contrôle. "
  "Ils reviennent principalement aux <strong>support</strong> et à certains junglers "
  "utilitaires, alors que les <a href=\"/tier-list-lol/\">tier lists LoL</a> classent les "
  "champions selon ces familles.")

# ---------------------------------------------------------------- H2 3
h2("Construire un build étape par étape")
h3("L'objet de départ et le premier retour")
p("La première vague d'or sert à acheter un objet de départ et souvent une ou deux potions. "
  "Un retour réussi achète une <strong>composante complète</strong> plutôt que plusieurs "
  "petits achats dispersés.")
p("Sur une lane dominée, l'objectif est de convertir l'avance en objet terminé. Sur une lane "
  "subie, mieux vaut une <strong>composante défensive</strong> bon marché qu'un objet cher "
  "impossible à finir.")

h3("Le premier objet terminé")
p("Le premier objet terminé fixe l'identité du build. Il doit correspondre au pic de puissance "
  "du champion et au <strong>moment</strong> où le joueur espère peser sur la partie.")
p("Choisir un premier objet trop défensif prive le champion de son impact naturel. Choisir un "
  "objet offensif face à un adversaire dominant expose à des <strong>morts</strong> "
  "répétées.")

h3("Les bottes et leur enchantement")
p("Les bottes arrivent généralement juste après ou juste avant le premier objet terminé. Le "
  "choix dépend de l'ennemi principal : bottes anti-sorts face à plusieurs <strong>menaces "
  "magiques</strong>, bottes d'armure face à l'adversaire physique en duel.")

# ---------------------------------------------------------------- H2 4
h2("Adapter son build à la partie en cours")
h3("Lire la composition adverse")
p("Avant le premier achat cher, il faut compter les menaces de chaque type. Une équipe avec "
  "trois <strong>dégâts magiques</strong> impose une résistance magique, même sur un champion "
  "qui n'en achèterait pas d'habitude.")
p("La présence d'un soigneur ou d'un régénérateur impose un objet anti-soin. Sans cet achat, "
  "les dégâts du joueur sont <strong>annulés</strong> à chaque échange.")

h3("Gérer l'avance et le retard d'or")
p("Un joueur en avance peut accélérer son build avec des objets offensifs, chaque achat "
  "creusant l'<strong>écart</strong> avec son adversaire direct. En retard, il vise les objets "
  "au meilleur rapport efficacité-prix.")
p("Les composantes bon marché et les objets défensifs permettent alors de "
  "<strong>rester utile</strong> même sans or, plutôt que d'attendre un objet inatteignable.")

h3("Ne pas copier un build sans le lire")
p("Les builds publiés dans le client ou sur les sites de statistiques sont des "
  "<strong>moyennes</strong>, calculées sur des milliers de parties.")
p("Ils restent un point de départ utile. La décision finale revient toujours au joueur qui voit "
  "sa propre partie, son or et ses <strong>matchups</strong>.")

# ---------------------------------------------------------------- H2 5
h2("Les erreurs fréquentes sur les builds LoL")
h3("Acheter sans regarder son or")
p("Un build n'est pas un plan rigide : il se rejoue à chaque retour en base. Attendre une "
  "somme ronde pour compléter un objet coûte souvent une <strong>vague</strong> d'or perdue.")
p("Il vaut mieux acheter une composante utile tout de suite qu'un objet parfait dans trois "
  "minutes. Chaque minute passée sans dépenser est une <strong>perte</strong> sèche.")

h3("Ignorer la vitesse de déplacement")
p("Les bottes sont parfois traitées comme un achat mineur. Elles déterminent pourtant le "
  "rythme de rotation et la capacité à <strong>survivre</strong> aux ganks.")
p("Dans une partie où le joueur est régulièrement rattrapé, l'achat d'une paire de bottes "
  "supplémentaire ou d'un objet de mobilité vaut mieux qu'un <strong>énième</strong> objet "
  "de dégâts.")

# ---------------------------------------------------------------- H2 6
h2("Suivre l'évolution des builds au fil des patchs")
h3("Pourquoi les builds changent à chaque patch")
p("Chaque mise à jour modifie le prix ou les statistiques d'une partie des objets. Un build "
  "qui dominait une saison peut devenir <strong>inefficace</strong> après un simple ajustement.")
p("Les joueurs qui suivent les <a href=\"/patch-notes-lol/\">patch notes League of Legends</a> "
  "comprennent pourquoi un objet revient soudain dans <strong>toutes</strong> les parties.")

h3("Le lien entre build et drafting professionnel")
p("En compétition, le build dépend du plan d'équipe et des choix de draft. Une équipe qui "
  "joue autour de son <strong>porteur de dégâts</strong> lui donne plus d'or qu'il n'en "
  "recevrait en partie classique.")
p("Pour observer ces adaptations en situation réelle, les matchs des Worlds restent la "
  "meilleure école : le <a href=\"/planning/\">calendrier des Worlds LoL</a> donne toutes "
  "les dates, le <a href=\"/classement/\">classement des Worlds</a> suit la progression "
  "des <strong>équipes</strong>.")

page["body"] = "\n".join(B)

# ---- contrôle qualité interne (avant validate_seo.py) ---------------------
plain = re.sub(r"<[^>]+>", " ", page["body"])
words = len(plain.split())
paras = re.findall(r"<p>(.*?)</p>", page["body"], re.S)
long_paras = [len(re.sub(r"<[^>]+>", " ", x).split()) for x in paras
              if len(re.sub(r"<[^>]+>", " ", x).split()) >= 60]
print(f"body={words} mots, {len(paras)} paragraphes, paras>=60mots={long_paras}")
print(f"meta_title={len(page['meta_title'])} meta_desc={len(page['meta_description'])}")

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(page, f, ensure_ascii=False, indent=2)
print("écrit", PATH)
