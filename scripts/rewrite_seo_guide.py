#!/usr/bin/env python3
"""Réécrit parier-worlds-lol.json pour le mot-clé « parier sur lol »
(phrases courtes, données tangibles, 1 gras/paragraphe, H3 max, 2 § max/partie)."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
PATH = os.path.join(ROOT, "content", "parier-worlds-lol.json")

CTA = ('<div class="cta-affiliate"><div class="cta-box">\n'
       '<span class="cta-bonus">Bonus de dépôt 75 % jusqu\'à 500 €</span>\n'
       '<div class="cta-box-title">Parier sur LoL avec BetNinja</div>\n'
       '<p>BetNinja couvre League of Legends avec des cotes en direct et un '
       '<strong>bonus de 75 % jusqu\'à 500 €</strong> sur le premier dépôt.</p>\n'
       '<a class="cta-btn" href="/parier-worlds-lol/" data-go="L2dvL2xvbA==" '
       'rel="nofollow sponsored noopener" target="_blank">Parier sur LoL '
       '<span class="cta-arrow">→</span></a>\n'
       '<p class="cta-disclosure">18+ · Jouer comporte des risques · Lien partenaire '
       '(commission perçue sans surcoût).</p>\n'
       '</div></div>')

BODY = CTA + """

<h2>Pourquoi parier sur LoL ?</h2>
<h3>Les Worlds 2026 en chiffres</h3>
<p>Le système suisse des Worlds 2026 réunit <strong>16 équipes</strong> du 23 au 31 octobre à Allen (Texas).</p>
<p>Le tournoi complet compte <strong>46 matchs</strong>, du play-in à la grande finale.</p>
<h3>Les marchés disponibles</h3>
<p>Sur chaque match de LoL, un bookmaker propose <strong>15 à 30 marchés</strong> : vainqueur, nombre de kills, premier sang ou premier objectif.</p>
<p>Les cotes sont mises à jour <strong>en temps réel</strong> avant et pendant chaque partie.</p>

<h2>Le format des Worlds 2026</h2>
<h3>Le play-in</h3>
<p>Le play-in réunissait <strong>4 équipes</strong> : MVK Esports, FURIA, Karmine Corp et Cloud9 Kia.</p>
<p><strong>Karmine Corp</strong> a remporté le play-in et validé sa place au système suisse.</p>
<h3>Le système suisse</h3>
<p>Le système suisse oppose <strong>16 équipes</strong>. Une équipe se qualifie après 3 victoires et est éliminée après 3 défaites.</p>
<p>Les matchs de qualification et d'élimination se jouent en <strong>Bo3</strong>, les autres en Bo1.</p>
<h3>La phase finale</h3>
<p>Les <strong>8 équipes</strong> qualifiées s'affrontent en élimination directe : quarts, demi-finales puis finale.</p>
<p>Les quarts, les demi-finales et la finale se jouent en <strong>Bo5</strong>.</p>

<h2>Les types de paris sur LoL</h2>
<h3>Le vainqueur du match</h3>
<p>Vous choisissez l'équipe qui remporte la série. C'est le pari le plus <strong>simple</strong> pour débuter.</p>
<p>Exemple : miser 10 € sur Gen.G à une cote de <strong>1,50</strong> rapporte 15 € si Gen.G gagne.</p>
<h3>Le nombre total de kills</h3>
<p>Le bookmaker fixe un seuil de kills, par exemple <strong>25,5</strong>. Vous pariez sur un total supérieur ou inférieur.</p>
<p>Deux équipes agressives produisent souvent <strong>plus de 25 kills</strong> par partie.</p>
<h3>Le vainqueur du tournoi</h3>
<p>Vous désignez le futur champion du monde avant ou pendant le tournoi. Ce pari se place sur <strong>plusieurs semaines</strong>.</p>
<p>La cote change après chaque journée. Parier tôt peut offrir une cote <strong>plus élevée</strong>.</p>
<h3>Le premier sang</h3>
<p>Le « premier sang » désigne l'équipe qui réalise la <strong>première élimination</strong> de la partie.</p>
<p>Ce résultat tombe souvent dans les <strong>5 premières minutes</strong> de jeu.</p>

<h2>Comprendre les cotes</h2>
<h3>Lire une cote décimale</h3>
<p>En France, une cote s'affiche au format <strong>décimal</strong>. Une cote de 2,00 double la mise.</p>
<p>Une cote basse indique un favori. Une cote élevée indique un résultat <strong>moins probable</strong>.</p>
<h3>Convertir une cote en probabilité</h3>
<p>Divisez 100 par la cote pour obtenir la probabilité estimée. Une cote de 2,00 équivaut à <strong>50 %</strong>.</p>
<p>Cette méthode aide à repérer une cote supérieure à votre propre estimation du résultat.</p>
<h3>Cotes fixes et cotes en direct</h3>
<p>Une cote fixe est verrouillée au moment du pari. Une cote en direct change <strong>pendant le match</strong>.</p>
<p>Le pari en direct demande de décider vite, car la cote bouge à chaque objectif pris.</p>

<h2>Le vocabulaire de base</h2>
<h3>Mise, cote et gain</h3>
<p>La mise est la somme engagée. Le gain se calcule en multipliant la mise par la cote.</p>
<p>Une mise de 10 € à une cote de 1,80 rapporte <strong>18 €</strong>, soit 8 € de bénéfice.</p>
<h3>La bankroll</h3>
<p>La bankroll est le budget total réservé aux paris, séparé de vos dépenses courantes.</p>
<p>Une règle courante est de ne jamais miser plus de <strong>5 % de sa bankroll</strong> sur un seul pari.</p>
<h3>Le cash out</h3>
<p>Le cash out permet de clôturer un pari avant la fin et de récupérer une partie du gain.</p>
<p>Cette option réduit la perte, mais réduit aussi le <strong>gain maximal</strong>.</p>

<h2>Bien parier sur LoL</h2>
<h3>Analyser la forme des équipes</h3>
<p>Regardez les <strong>5 derniers résultats</strong> de chaque équipe avant de parier.</p>
<p>Consultez le <a href="/classement/">classement des Worlds</a> et les <a href="/resultats/">résultats</a> pour repérer les équipes en forme.</p>
<h3>Comparer les cotes</h3>
<p>Le même pari peut afficher une cote différente selon le bookmaker. Comparer augmente le gain.</p>
<p>Un écart de 0,10 sur une cote à 2,00 change le gain de <strong>1 €</strong> pour une mise de 10 €.</p>
<h3>Suivre le patch</h3>
<p>Chaque mise à jour du jeu change la <strong>puissance des champions</strong>.</p>
<p>Suivre les changements de patch aide à anticiper les compositions probables d'un match.</p>

<h2>Les erreurs à éviter</h2>
<h3>Parier par passion</h3>
<p>Miser sur son équipe favorite fausse le jugement. La passion ne remplace pas l'analyse.</p>
<p>Une équipe populaire n'est pas toujours favorite : sa cote reflète parfois le nombre de parieurs, pas la <strong>probabilité réelle</strong>.</p>
<h3>Chasser les pertes</h3>
<p>Augmenter la mise pour récupérer une perte est la <strong>principale cause</strong> de pertes importantes.</p>
<p>Après une défaite, gardez la même mise ou réduisez-la. Ne pariez pas pour compenser une perte.</p>

<h2>BetNinja pour parier sur LoL</h2>
<h3>Le bonus de dépôt</h3>
<p>BetNinja propose un bonus de dépôt hebdomadaire de <strong>75 % jusqu'à 500 €</strong> sur le sport.</p>
<p>Un dépôt de 100 € peut donc être abondé de <strong>75 € de bonus</strong>, selon les conditions en vigueur.</p>
<h3>Les autres promotions</h3>
<p>La plateforme ajoute un multiboost de <strong>30 %</strong> sur les combinés gagnants et des cotes boostées du jour.</p>
<p>Ces promotions sont soumises à des conditions générales. Lisez-les avant de vous inscrire.</p>
<h3>Notre avis honnête</h3>
<p>BetNinja couvre League of Legends et affiche des cotes sur les Worlds. Nous percevons une <strong>commission</strong> si vous vous inscrivez via nos liens.</p>
<p>Nous recommandons de comparer BetNinja avec d'autres bookmakers avant de choisir. Les cotes et les bonus changent.</p>

<h2>Parier de façon responsable</h2>
<h3>Fixer un budget</h3>
<p>Ne misez que de l'argent que vous pouvez <strong>perdre</strong>. Définissez un budget mensuel et respectez-le.</p>
<p>Ne pariez jamais pour récupérer une perte.</p>
<h3>Reconnaître les signes de dépendance</h3>
<p>Les jeux d'argent comportent des risques : endettement, isolement, dépendance. Ils sont interdits aux <strong>moins de 18 ans</strong>.</p>
<p>Contactez <strong>Joueurs Info Service au 09 74 75 13 13</strong> (appel non surtaxé) si vous ou un proche avez besoin d'aide.</p>

<h2>FAQ — parier sur LoL</h2>
<h3>Peut-on parier sur LoL en France ?</h3>
<p>Oui, sur les <strong>sites agréés</strong>. Vérifiez la licence de l'opérateur avant de vous inscrire.</p>
<h3>Quel est le meilleur site pour parier sur LoL ?</h3>
<p>Nous recommandons <strong>BetNinja</strong> pour ses cotes et son bonus de 75 % jusqu'à 500 €. Comparez toujours les cotes.</p>
<h3>À partir de quel âge peut-on parier ?</h3>
<p>À partir de <strong>18 ans</strong>. L'inscription des mineurs est interdite et vérifiée.</p>
<h3>Peut-on parier en direct ?</h3>
<p>Oui, les <strong>cotes en direct</strong> changent pendant le match.</p>
<h3>Comment commencer à parier sur LoL ?</h3>
<p>Créez un compte, déposez une petite somme et pariez sur un marché simple comme le <strong>vainqueur du match</strong>.</p>
<h3>Quels sont les risques ?</h3>
<p>Perdre de l'argent, s'endetter ou devenir dépendant. Fixez des <strong>limites</strong>.</p>
"""

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)

d["title"] = "Parier sur LoL : le guide complet 2026"
d["meta_title"] = "Parier sur LoL 2026 : guide, cotes et bonus | esport-lol"
d["meta_description"] = ("Comment parier sur LoL en 2026 : types de paris, lecture des cotes, "
                         "bonus BetNinja de 75 % jusqu'à 500 €. Guide simple et transparent.")
d["h1"] = "Parier sur LoL"
d["intro"] = ("<p class=\"lead\">Comment <strong>parier sur LoL</strong> en 2026 ? Ce guide explique "
              "les types de paris, la lecture des cotes et le bonus BetNinja de 75 % jusqu'à 500 €.</p>")
d["body"] = BODY
d["date_modified"] = "2026-10-19"

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("OK — page réécrite pour « parier sur LoL »")
print("occurrences 'parier sur LoL':", BODY.count("parier sur LoL") + d["intro"].count("parier sur LoL") + d["h1"].count("parier sur LoL"))
