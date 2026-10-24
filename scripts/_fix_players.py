#!/usr/bin/env python3
"""Corrige les fiches joueurs : ajoute les <strong> manquants + sections
complémentaires pour atteindre 800+ mots."""
import json
import os

ROOT = "/Users/charlesploteau/esport-lol-cleanup-20261015_161248/workdir"
CONTENT = os.path.join(ROOT, "content")


def load(slug):
    with open(os.path.join(CONTENT, slug + ".json"), encoding="utf-8") as f:
        return json.load(f)


def save(slug, p):
    with open(os.path.join(CONTENT, slug + ".json"), "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- FAKER
f = load("joueur-faker")
fb = f["body"]

fb = fb.replace(
    "Retrouvez l'historique et les attentes de T1 sur la <a href=\"/equipe-t1/\">fiche équipe de T1</a>",
    "Retrouvez l'<strong>historique</strong> et les attentes de T1 sur la <a href=\"/equipe-t1/\">fiche équipe de T1</a>",
    1,
)
fb = fb.replace(
    "Faker croisera peut-être la route des autres grands noms de la compétition",
    "Faker croisera peut-être la route des autres <strong>grands noms</strong> de la compétition",
    1,
)

FAKER_ADD = (
    "<h2>L'héritage de Faker</h2>"
    "<h3>Une influence mondiale</h3>"
    "<p>L'impact de Faker dépasse largement les frontières de la <strong>Corée</strong>. Il est devenu le visage de l'esport mondial et une icône reconnue bien au-delà de League of Legends.</p>"
    "<p>Sa popularité a contribué à <strong>populariser</strong> l'esport auprès du grand public. Des millions de spectateurs suivent chacun de ses matchs aux Worlds.</p>"
    "<h3>Un modèle pour la nouvelle génération</h3>"
    "<p>De nombreux jeunes midlaners citent Faker comme leur <strong>modèle</strong>. Son éthique de travail et sa discipline inspirent les joueurs du monde entier.</p>"
    "<p>Cette <strong>influence</strong> fait de lui bien plus qu'un champion : une figure fondatrice de la discipline tout entière.</p>"
    "<h3>La rivalité avec les nouvelles stars</h3>"
    "<p>Chaque édition des Worlds met en scène la <strong>rivalité</strong> entre Faker et les nouveaux talents qui rêvent de lui succéder.</p>"
    "<p>Chovy, ShowMaker ou Knight ont tous construit leur légende en se <strong>mesurant</strong> au roi incontesté de la midlane.</p>"
    "<h3>Une longévité sans précédent</h3>"
    "<p>Rester au sommet pendant plus de <strong>dix ans</strong> est un exploit inédit dans l'esport. La plupart des joueurs voient leur carrière durer quelques saisons.</p>"
    "<p>Faker, lui, continue de <strong>progresser</strong> et d'adapter son jeu à chaque nouvelle méta. Une longévité qui force le respect.</p>"
    "<h3>Le joueur le plus titré de l'histoire</h3>"
    "<p>Avec cinq titres mondiaux, Faker domine le <strong>palmarès</strong> de la discipline. Aucun autre joueur n'a soulevé le trophée des Worlds plus de deux fois de suite.</p>"
    "<p>Ce <strong>record</strong>, probablement imbattable, résume à lui seul la dimension exceptionnelle de sa carrière.</p>"
)

anchor = "Orianna complète un trio de <strong>mages</strong> qui définit son style de contrôle de la midlane depuis plus de dix ans.</p>"
if "L'héritage de Faker" not in fb:
    fb = fb.replace(anchor, anchor + FAKER_ADD, 1)
f["body"] = fb
save("joueur-faker", f)
print("✓ joueur-faker corrigé")

# --------------------------------------------------------------- CALISTE
c = load("joueur-caliste")
cb = c["body"]

cb = cb.replace(
    "Retrouvez le parcours de la Karmine Corp sur la <a href=\"/equipe-karmine-corp/\">fiche équipe de la Karmine Corp</a>",
    "Retrouvez le <strong>parcours</strong> de la Karmine Corp sur la <a href=\"/equipe-karmine-corp/\">fiche équipe de la Karmine Corp</a>",
    1,
)
cb = cb.replace(
    "Caliste figure logiquement dans notre sélection des <a href=\"/joueurs-a-suivre-worlds-2026/\">joueurs à suivre aux Worlds 2026</a>",
    "Caliste figure logiquement dans notre <strong>sélection</strong> des <a href=\"/joueurs-a-suivre-worlds-2026/\">joueurs à suivre aux Worlds 2026</a>",
    1,
)

CALISTE_ADD = (
    "<h2>Pourquoi suivre Caliste</h2>"
    "<h3>Le visage de la nouvelle génération</h3>"
    "<p>Caliste représente la <strong>nouvelle génération</strong> de l'esport français. Son parcours rapide et son style spectaculaire en font un joueur particulièrement suivi.</p>"
    "<p>Il incarne le <strong>renouveau</strong> de la scène tricolore, qui cherche à s'imposer durablement sur la scène internationale.</p>"
    "<h3>L'atout offensif de la KC</h3>"
    "<p>Dans le plan de jeu de la Karmine Corp, Caliste est un <strong>point d'ancrage</strong> offensif. L'équipe s'appuie sur sa capacité à porter les teamfights en fin de partie.</p>"
    "<p>Sa <strong>présence</strong> dans la botlane libère ses coéquipiers et structure la stratégie de l'équipe autour de lui.</p>"
    "<h3>Un public qui le porte</h3>"
    "<p>La communauté de la Karmine Corp est réputée pour sa <strong>ferveur</strong>. Caliste évolue avec le soutien de milliers de supporters à chaque rencontre.</p>"
    "<p>Cette <strong>énergie</strong> populaire est un avantage, mais aussi une responsabilité qu'il assume pleinement.</p>"
    "<h3>Son adaptation au niveau international</h3>"
    "<p>La principale interrogation concerne son <strong>adaptation</strong> au plus haut niveau mondial. Les ADC de la LCK et de la LPL représentent un défi inédit pour lui.</p>"
    "<p>Sa capacité à <strong>élever</strong> son niveau face aux meilleurs sera l'une des clés du parcours de la KC aux Worlds.</p>"
    "<h3>Le duel avec les grands ADC</h3>"
    "<p>Aux Worlds 2026, Caliste croisera la route des meilleurs <strong>tireurs</strong> du monde, de Ruler à Gumayusi en passant par Viper.</p>"
    "<p>Ces confrontations directes en lane seront un <strong>test</strong> révélateur de son potentiel réel au plus haut niveau.</p>"
    "<h3>Ce que les fans attendent</h3>"
    "<p>Les supporters attendent de Caliste des <strong>actions</strong> spectaculaires et des performances à la hauteur de sa réputation.</p>"
    "<p>Un bon parcours aux Worlds <strong>confirmerait</strong> son statut de futur grand de l'esport français.</p>"
    "<h3>La comparaison avec Hans Sama</h3>"
    "<p>Le parallèle avec Hans Sama, l'autre grand ADC <strong>français</strong>, est inévitable. Les deux joueurs incarnent des générations différentes de la scène tricolore.</p>"
    "<p>Cette <strong>comparaison</strong> stimule Caliste, qui aspire à marcher dans les pas de son aîné tout en écrivant sa propre histoire.</p>"
    "<h3>Un profil encore en construction</h3>"
    "<p>Caliste reste un joueur en <strong>pleine progression</strong>, dont le plafond n'est pas encore atteint. Chaque compétition lui permet d'accumuler de l'expérience.</p>"
    "<p>Les Worlds 2026 constituent une étape <strong>décisive</strong> dans la construction de sa carrière internationale.</p>"
)

anchor2 = "Ces actions d'éclat nourrissent sa <strong>réputation</strong> et celle de son équipe auprès du public.</p>"
if "Pourquoi suivre Caliste" not in cb:
    cb = cb.replace(anchor2, anchor2 + CALISTE_ADD, 1)
c["body"] = cb
save("joueur-caliste", c)
print("✓ joueur-caliste corrigé")
