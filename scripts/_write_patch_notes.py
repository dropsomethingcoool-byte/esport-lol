#!/usr/bin/env python3
"""Rédige content/patch-notes-lol.json (patch 26.20) — sourcing Riot, aucun chiffre inventé."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

intro = (
    '<p class="lead">Les <strong>patch notes league of legends</strong> 26.20 '
    "sont en ligne depuis le 6 octobre 2026 : c'est le patch de référence des Worlds, "
    "avec des nerfs sur Ambessa et K'Santé, des buffs pour Kennen et Kindred, "
    "et une Ceinture-roquette rééquilibrée.</p>"
)

body = f"""<h2>Patch notes League of Legends 26.20 : ce qui change</h2>
<h3>Un patch calibré pour les Worlds</h3>
<p>Riot présente la mise à jour <strong>26.20</strong> comme le cadre d'équilibrage de la scène compétitive majeure de l'année. Les changements visent les champions les plus fiables en jeu coordonné.</p>
<p>Le calendrier du tournoi est détaillé dans notre <a href="/planning/">planning des Worlds</a>, et les bilans d'équipes se lisent dans le <a href="/classement/">classement des Worlds</a>.</p>
<h3>La date de déploiement</h3>
<p>Les notes officielles sont datées du <strong>6 octobre 2026</strong>. Les skins HEARTSTEEL Live My Life et le prestige Sett sont annoncés pour le 7 octobre.</p>
<p>Un patch remplace le précédent sur les serveurs live : les valeurs ci-dessous sont celles en vigueur sur la Faille depuis cette date.</p>
<h3>Les quatre axes du patch</h3>
<p>Le patch se répartit entre équilibrage des champions, ajustements d'objets, ajouts au mode Classic et retouches ARAM. Chaque famille de changement répond à un <strong>problème de méta</strong> identifié par Riot.</p>
<p>Les champions forts en compétition sont bridés, les profils trop faibles reçoivent des buffs ciblés, et les objets polyvalents sont réorientés vers un usage plus risqué.</p>
<h3>Où trouver le détail chiffré</h3>
<p>Chaque valeur modifiée est listée dans les notes officielles publiées par Riot. Ce récapitulatif se concentre sur les <strong>changements à impact</strong> pour la file classée et la scène pro.</p>
<p>Les guides d'analyse comme notre <a href="/tier-list-lol/">tier list LoL</a> se réévaluent à chaque patch, car la position d'un champion dépend directement de ces valeurs.</p>

<h2>Les nerfs des champions dominants</h2>
<h3>Ambessa et K'Santé en compétition</h3>
<p>Ambessa perd de la puissance en fin de partie : son passif passe de 5-30 (+25% des dégâts d'attaque bonus) à <strong>5-25 (+20%)</strong>.</p>
<p>K'Santé voit le coût en mana de son Z grimper de 40-60 à 45-65, et la réduction de dégâts du Z descend de 30-75% à <strong>25-70%</strong>.</p>
<h3>Ashe, Cassiopeia et Fiora ajustés</h3>
<p>Ashe perd 0,5 point de dégâts d'attaque par niveau, une correction expliquée par son statut de <strong>tireur utilitaire</strong> le plus polyvalent du jeu.</p>
<p>Cassopeia recule à 610 PV et 450 mana de base, tandis que Fiora paie la Riposte : son bonus d'attaque passe de 15-35 à <strong>10-30</strong>.</p>
<h3>Graves et Fizz ciblés sur leurs dégâts</h3>
<p>Graves est le champion le plus fort du patch selon Riot : dégâts d'attaque de base de 54,1 à 50, et dégâts du cône de l'ultime de <strong>140-360 à 140-320</strong>.</p>
<p>Fizz conserve son style d'assassin, mais ses ratios de puissance baissent : 60% à 40% sur le A, 35% à <strong>20%</strong> sur le Z actif.</p>
<h3>Yunara et Smolder dans le viseur</h3>
<p>Yunara perd 2 dégâts par palier sur son A, et son Z cesse de cumuler les ralentissements avec ceux d'autres sources. Riot veut couper l'inaction <strong>hyperscalaire</strong> avant les Worlds.</p>
<p>Smolder reçoit l'inverse : ses dégâts bonus passent de 25-55% à 25-60%, pour rapprocher ses builds coup critique de ses builds bagarreur.</p>
<h3>Ce que ça change en partie classée</h3>
<p>Un champion nerfé reste jouable s'il possède un plan de jeu clair. Le repère utile est le <strong>taux de victoire</strong> observé quelques jours après le déploiement.</p>
<p>Avant de changer de main, consultez le <a href="/guide-champions-lol/">guide champion League of Legends</a> pour vérifier que la courbe de puissance correspond à votre style.</p>

<h2>Les buffs à connaître</h2>
<h3>Kennen, un buff pensé pour l'AD</h3>
<p>La vitesse d'attaque bonus du E de Kennen monte de 40-80% à <strong>50-90%</strong>. Son Z devient 25-85 plus 100% des dégâts d'attaque bonus.</p>
<p>Ces valeurs profitent surtout au Kennen AD, un profil qui manquait de puissance comparé aux autres ninjas de la Faille.</p>
<h3>Kindred et Lillia en jungle</h3>
<p>Kindred frappe les monstres à <strong>165%</strong> au lieu de 150% via son Z, et le ralentissement de son E dure 1,5 seconde au lieu d'une.</p>
<p>Lillia gagne jusqu'à 3 secondes de sommeil sur son ultime aux niveaux avancés, au lieu de 2,5 secondes fixes.</p>
<h3>Lucian, Mordekaiser et Vayne</h3>
<p>Lucian compense un nerf précédent avec <strong>2,9</strong> dégâts d'attaque par niveau au lieu de 2,5. Mordekaiser voit son A progresser de +7 par niveau au lieu de +5.</p>
<p>Vayne retrouve une régénération plus saine et un coût de Roulade fixé à <strong>30</strong> mana, au lieu d'une échelle dégressive.</p>
<h3>Swain, Neeko et Tahm Kench</h3>
<p>Swain gagne 3 points de résistance magique et 40 de dégâts au niveau 5 sur son Z, avec un délai réduit à <strong>16 secondes</strong>.</p>
<p>Neeko et Tahm Kench reçoivent des compensations liées aux objets modifiés : +10 dégâts de base sur le E pour l'une, soins de Coup de langue à <strong>10-50</strong> pour l'autre.</p>
<h3>Le cas Diana</h3>
<p>La version bagarreuse de Diana progresse : son bouclier passe de 11% à <strong>14%</strong> des PV bonus. Le style assassin reste inchangé.</p>
<p>C'est un buff de style de jeu plus que de puissance brute, utile pour les joueurs qui bâtissent Diana avec des PV.</p>

<h2>Les objets modifiés au patch 26.20</h2>
<h3>La Ceinture-roquette Hextech</h3>
<p>La Ceinture-roquette perd 10 points d'accélération de compétence mais gagne de la puissance active : <strong>135 (+15%)</strong> au lieu de 100 (+10%).</p>
<p>Riot veut décourager son usage comme outil de fuite et récompenser l'engagement volontaire des bagarreurs AP.</p>
<h3>Hexplaque expérimentale et Ouragan de Runaan</h3>
<p>L'Hexplaque expérimentale à distance tombe à <strong>50%</strong> de sa valeur, contre 70% auparavant, sur la vitesse d'attaque comme sur la vitesse de déplacement.</p>
<p>L'Ouragan de Runaan revient à 60% de dégâts par éclair, après un buff jugé excessif au patch précédent.</p>
<h3>La régénération des objets de tank</h3>
<p>Visage spirituel passe de 4 à <strong>20</strong> PV toutes les 5 secondes, Force de la nature de 20 à 40, et Armure de Warmog de 10 à 30.</p>
<p>Ces buffs corrigent une régénération trop faible sur des objets pensés pour tenir la durée.</p>
<h3>Le tableau des scores allégé</h3>
<p>Les compteurs de nombreux objets sont désormais masqués sur le tableau des scores, dont la <strong>Danse de la mort</strong> et le Tourment de Liandry.</p>
<p>Les objets à charge stratégique, comme la Larme de la déesse et le Voleur d'âmes de Mejai, conservent leur affichage.</p>

<h2>Classic, ARAM et corrections de bugs</h2>
<h3>Cinq anciens champions en Classic</h3>
<p>Aatrox, Caitlyn, Irelia, Karma et Quinn rejoignent les Champs de justice en version Classic : <strong>cinq kits</strong> tels qu'ils existaient avant leurs refontes.</p>
<p>Ces versions s'appuient sur les sorts d'origine, par exemple le Mantra de Karma disponible dès le niveau 1 avec deux charges.</p>
<h3>Le mode ARAM du chaos</h3>
<p>Bard, Garen, Lee Sin, Thresh, K'Santé et Swain reçoivent des buffs dédiés à l'ARAM du chaos. Le Z de K'Santé y dure <strong>10 secondes fixes</strong>.</p>
<p>Plusieurs optimisations sont retouchées, dont Gâchette infernale, dont le délai tombe de 15 à 5 secondes.</p>
<h3>Horaires de la file classée</h3>
<p>Les parties en Classé 5c5 restent disponibles de <strong>16h à 4h</strong> (heure du serveur), contre 16h à 2h auparavant.</p>
<p>Ceux qui jouent tard y gagnent deux heures de fenêtre, sans changement sur le reste du système.</p>
<h3>Les corrections notables</h3>
<p>Riot corrige notamment le A de Xin Zhao, qui repartait en délai complet si la première attaque était esquivée, ainsi que le <strong>Bouclier magique</strong> de Sivir face à la Lame du zénith de Leona.</p>
<p>Plusieurs bugs d'affichage sont aussi corrigés sur les pages de runes et les icônes Classic.</p>

<h2>Comment lire et appliquer un patch</h2>
<h3>Repérer les changements utiles</h3>
<p>Un patch contient des dizaines de lignes, mais peu concernent votre pool de champions. Filtrez par <strong>rôle</strong> et par champion joué pour ne retenir que l'essentiel.</p>
<p>Les chiffres bruts comptent moins que la tendance : une baisse de ratio répétée sur trois patchs signale un vrai recul.</p>
<h3>Mettre à jour runes et objets</h3>
<p>Un objet modifié entraîne souvent une page de runes à revoir, notamment quand l'accélération de compétence change. Notre guide des <a href="/runes-league-of-legends/">runes League of Legends</a> détaille la logique des arbres.</p>
<p>Le réflexe utile : retester une partie normale avant de repartir en classée avec un build modifié.</p>
<h3>Éviter les conclusions hâtives</h3>
<p>Les <strong>taux de victoire</strong> des premiers jours sont biaisés par les joueurs qui testent. Attendez une à deux semaines pour juger un changement.</p>
<p>Pendant cette période, les notes officielles restent la seule source fiable sur les valeurs réellement appliquées.</p>
<p>Pour suivre l'actualité du jeu et des Worlds, retrouvez nos analyses sur le <a href="/blog/">blog League of Legends</a>.</p>"""

page = {
    "slug": "patch-notes-lol",
    "type": "article",
    "title": "Patch notes League of Legends : le patch 26.20 en résumé",
    "meta_title": "Patch notes League of Legends : patch 26.20",
    "meta_description": "Patch notes League of Legends 26.20 : nerfs Ambessa, K'Santé et Graves, buffs Kennen et Kindred, objets revus et ajouts Classic. L'essentiel du patch.",
    "h1": "Patch notes League of Legends : le patch 26.20",
    "intro": intro,
    "body": body,
    "related": [
        {"slug": "tier-list-lol", "anchor": "Tier List LoL"},
        {"slug": "guide-champions-lol", "anchor": "Guide champion League of Legends"},
        {"slug": "runes-league-of-legends", "anchor": "Runes League of Legends"},
    ],
    "date_modified": "2026-10-20",
    "date_published": "2026-10-20",
}

path = os.path.join(ROOT, "content", "patch-notes-lol.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(page, f, ensure_ascii=False, indent=2)
print("écrit", path)
