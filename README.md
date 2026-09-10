# Colorfulminis — perks

Les outils que j'utilise vraiment, publiés pour que vous puissiez les reprendre.

- 📹 [La chaîne YouTube](https://www.youtube.com/@Colorfulminis)
- 🎲 [Call of Dungeons](https://callofdungeons.com)

## Ce qu'il y a dedans

| | |
|---|---|
| [`methode-fiches-mj.md`](methode-fiches-mj.md) | La méthode pour générer des fiches de MJ jouables avec une IA |
| [`/cfm-montecarlo`](plugins/cfm-gamedesign/skills/cfm-montecarlo/SKILL.md) | Équilibrer une règle de jeu par simulation |

---

# `/cfm-montecarlo` — équilibrer une règle par simulation

**Un jeu qui repose sur des dés est un objet mesurable.** La plupart des barèmes se règlent au ressenti, parce que la probabilité exacte devient indécidable dès qu'on empile trois clauses : un malus, une opposition, une armure.

La simulation contourne le calcul. **Au lieu de calculer la probabilité, on joue 200 000 fois et on compte.**

Vous écrivez vos règles en français. La compétence les lit, vous pose quatre questions, les traduit en simulateur, l'exécute, et vous rend deux fichiers : un résumé lisible et le détail de tous les tirages en CSV.

## Installation

Dans Claude Code :

```
/plugin marketplace add sukria/colorfulminis-perks
/plugin install cfm-gamedesign@colorfulminis-perks
```

Puis, depuis le dossier de votre jeu :

```
/cfm-montecarlo mes-regles.md
```

Rien à installer d'autre : le moteur est du Python 3.9 sans aucune dépendance.

## Essayer en deux minutes

Le dépôt contient un jeu jouet complet, [Arène](plugins/cfm-gamedesign/skills/cfm-montecarlo/exemple/regles.md), qui tient en une page :

- Une figurine a un **Combat** de 2 à 6, c'est son nombre de dés, et **10 points de vie**.
- Chaque **5** inflige 1 blessure, chaque **6** en inflige 2.
- On lance 1 dé par point de Combat, **plus ou moins 1 dé par point d'écart** avec l'adversaire. Jamais moins de 1 dé, jamais plus de 6.

Ces règles paraissent saines. La question est simple : **combien de tours pour abattre une figurine à 10 points de vie ?**

```bash
cd plugins/cfm-gamedesign/skills/cfm-montecarlo/exemple
python3 ../scripts/montecarlo.py regles.py --tirages 200000 --sortie ./resultats
```

Ouvrez `resultats/resume.md`. Tours moyens pour abattre :

| Attaquant \ Cible | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| **Combat 2** | 10,6 | 20,7 | 20,7 | 20,6 | 20,6 |
| **Combat 3** | 5,6 | 7,2 | 10,6 | 20,7 | 20,7 |
| **Combat 4** | **3,9** | 4,5 | 5,6 | 7,2 | 10,6 |
| **Combat 5** | **3,9** | **3,9** | **3,9** | 4,5 | 5,5 |
| **Combat 6** | **3,9** | **3,9** | **3,9** | **3,9** | **3,9** |

Deux défauts, et ils sont graves :

- **Un Combat 6 abat tout le monde en 3,9 tours.** Un adversaire à 2 ou à 6, c'est identique. Le plafond de 6 dés mange toute sa supériorité — au sommet, l'écart de Combat ne veut plus rien dire.
- **Un Combat 2 met 20,6 tours contre 3, 4, 5 comme 6.** Le plancher de 1 dé fait la même chose en bas.
- Et **un Combat 4 contre un Combat 2 vaut exactement un Combat 6** : 3,9 tours des deux côtés. Deux points de caractéristique pour rien.

Aucune relecture des règles ne trouve ça. 200 000 tirages, oui — et il devient évident que c'est l'écart qu'il faut borner, pas le nombre de dés.

## Comment c'est fait

Deux fichiers, et la séparation entre les deux est tout l'intérêt :

- **`scripts/montecarlo.py`** — le moteur. Il ne connaît aucun jeu. Il répète une résolution, agrège, écrit. Il ne se modifie jamais.
- **`regles.py`** — vos règles, et rien d'autre. C'est le seul fichier que l'IA écrit.

```python
SCENARIOS = [...]                      # les cas à balayer
def resoudre(scenario, rng) -> dict:   # une résolution, une fois
```

Le contrat complet tient dans [`references/moteur.md`](plugins/cfm-gamedesign/skills/cfm-montecarlo/references/moteur.md).

> 🚨 **La règle de fer : le fichier de règles fait foi.** Le code ne décide rien, il traduit. Si le code et les règles divergent, c'est le code qui est faux. L'IA n'a pas voix au chapitre sur votre jeu — elle traduit votre texte en quelque chose d'exécutable, et c'est déjà énorme.

## Ça marche sur un vrai jeu ?

Oui. La compétence a été rejouée sur l'action de Tir de Call of Dungeons, contre un simulateur écrit à la main pour cette règle précise. **Elle retrouve ses chiffres à moins de 0,2 point**, arme par arme, et elle retrouve la même anomalie : à Agilité 7, on touche 7 points de plus pour 0,01 blessure de moins.

## Validation

```bash
python3 plugins/cfm-gamedesign/skills/cfm-montecarlo/evals/test_moteur.py
```

24 vérifications, sans pytest ni dépendance : convergence vers des valeurs connues à la main, reproductibilité à graine fixée, format du CSV, refus propre des règles invalides, et présence des deux zones plates dans l'exemple.

Les scénarios de comportement de la compétence sont dans [`evals/evals.json`](plugins/cfm-gamedesign/skills/cfm-montecarlo/evals/evals.json).

## Licence

MIT. Prenez, modifiez, publiez vos jeux.
