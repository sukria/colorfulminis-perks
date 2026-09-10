# Colorfulminis — perks

- 📹 [La chaîne YouTube](https://www.youtube.com/@Colorfulminis)
- 🎲 [Call of Dungeons](https://callofdungeons.com)

## Ce qu'il y a dedans

Un plugin Claude Code, `cfm-gamedesign`, et deux skills  :


|                                                                            |                                                                                                                                                    |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`/cfm-fichejdr`](plugins/cfm-gamedesign/skills/cfm-fichejdr/SKILL.md)     | Produire un paquet de fiches de MJ jouables en direct → [https://www.youtube.com/watch?v=sO6PI1Ax474](https://www.youtube.com/watch?v=sO6PI1Ax474) |
| [`/cfm-montecarlo`](plugins/cfm-gamedesign/skills/cfm-montecarlo/SKILL.md) | Équilibrer une règle de jeu par simulation Monte Carlo                                                                                             |


## Installation

Dans Claude Code :

```
/plugin marketplace add sukria/colorfulminis-perks
/plugin install cfm-gamedesign@colorfulminis-perks
```

**Tout se passe ensuite dans Claude** **Code**.

---

# `/cfm-fichejdr` — les fiches de MJ

**Un scénario doit être maîtrisable sans huit heures de lecture préliminaire.**

Cette skill transforme un scénario (le vôtre, ou un du commerce que vous résumez), en un paquet de fiches A4 imprimables, une par scène, par lieu et par PNJ. 

```
/cfm-fichejdr
```

La skill vous pose des questions pour préciser le cadre et affiner la structure du scénario, ensuite elle vous soumet un plan, puis produit les fiches **une par une, au format PDF**, chacune validée avant la suivante. 

Chaque fiche contient les mêmes  blocs, toujours à la même place : ce qu'on lit à voix haute, ce qui se passe, les tests possibles, les indices à trouver et la condition de sortie.

---

# `/cfm-montecarlo` — équilibrer une règle par simulation

**Un jeu qui repose sur des dés est un objet mesurable.** La plupart des barèmes se règlent au ressenti, parce que la probabilité exacte devient indécidable dès qu'on empile de multiples conditions (un malus, une opposition, une armure, des stats d'armes variables, etc).

Une simulation de Monte Carlo est une méthode "brute force" qui contourne le calcul de complexité exponentielle à mesure que les variables entre en jeu. **Au lieu de calculer la probabilité, on joue 200 000 fois et on observe les résultats. La théorie des Grands Nombres fait le reste (les résultats convergent vers la probabilité).**

Vous écrivez vos règles en français, dans un fichier. La skill les lit, vous pose quatre questions, les traduit en simulateur, l'exécute, et vous rend un résumé lisible plus le détail de tous les tirages en CSV.

```
/cfm-montecarlo mes-regles.md
```

## Essayer sur le jeu de démonstration

Le dépôt fournit un jeu d'entraînement : [`exemples/dummy-arena.md`](exemples/dummy-arena.md). **Un seul fichier, et aucune réponse à côté** — vous refaites toute la démarche vous-même.

Il tient en une page :

- Une figurine a un **Combat** de 2 à 6, c'est son nombre de dés, et **10 points de vie**.
- Chaque **5** inflige 1 blessure, chaque **6** en inflige 2.
- On lance 1 dé par point de Combat, **plus ou moins 1 dé par point d'écart** avec l'adversaire. Jamais moins de 1 dé, jamais plus de 6.

Ces règles paraissent saines. La question est simple : **combien de tours pour abattre une figurine à 10 points de vie ?**

Copiez le fichier dans un dossier vide, ouvrez Claude Code dedans, et lancez :

```
/cfm-montecarlo dummy-arena.md
```

Répondez aux questions, et voyez si vous trouver le défaut majeur de ces règles (spoiler: ce jeu n'a aucun intérêt en l'état !).

## Licence

MIT. C'est libre les amis.