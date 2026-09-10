# Colorfulminis — perks

Les outils que j'utilise vraiment, publiés pour que vous puissiez les reprendre.

- 📹 [La chaîne YouTube](https://www.youtube.com/@Colorfulminis)
- 🎲 [Call of Dungeons](https://callofdungeons.com)

## Ce qu'il y a dedans

Un plugin Claude Code, `cfm-gamedesign`, et deux compétences dedans :

| | |
|---|---|
| [`/cfm-fichejdr`](plugins/cfm-gamedesign/skills/cfm-fichejdr/SKILL.md) | Produire un paquet de fiches de MJ jouables en direct |
| [`/cfm-montecarlo`](plugins/cfm-gamedesign/skills/cfm-montecarlo/SKILL.md) | Équilibrer une règle de jeu par simulation |

## Installation

Dans Claude Code :

```
/plugin marketplace add sukria/colorfulminis-perks
/plugin install cfm-gamedesign@colorfulminis-perks
```

C'est tout. **Tout se passe ensuite dans Claude** : aucune commande à taper dans un terminal, rien à installer, aucune dépendance.

---

# `/cfm-fichejdr` — les fiches de MJ

**Un scénario doit être maîtrisable sans huit heures de lecture préliminaire.**

Cette compétence transforme un scénario — le vôtre, ou un du commerce — en un paquet de fiches A4 imprimables, une par scène, par lieu et par PNJ. Une fiche se lit à table, une main dessus, pendant que six personnes attendent.

```
/cfm-fichejdr
```

Elle vous fait passer un entretien, vous soumet un plan, puis produit les fiches **une par une**, chacune validée avant la suivante. Elle ne dépend d'aucun système : tout ce qui est propre à votre partie se remplit à l'entretien.

Chaque fiche porte les mêmes six blocs, toujours à la même place — ce qu'on lit à voix haute, ce qui se passe en trois beats, les jets déjà résolus, les indices en cases à cocher, les répliques prêtes à dire, et la sortie.

> 🚨 **Le dernier bloc est le plus important du paquet.** La peur numéro un d'un MJ, c'est le silence après « bon… vous faites quoi ? ». Aucune fiche ne sort sans sa phrase de relance écrite noir sur blanc.

La méthode complète reste lisible seule dans [`methode-fiches-mj.md`](methode-fiches-mj.md), pour qui préfère la charger à la main.

---

# `/cfm-montecarlo` — équilibrer une règle par simulation

**Un jeu qui repose sur des dés est un objet mesurable.** La plupart des barèmes se règlent au ressenti, parce que la probabilité exacte devient indécidable dès qu'on empile trois clauses : un malus, une opposition, une armure.

La simulation contourne le calcul. **Au lieu de calculer la probabilité, on joue 200 000 fois et on compte.**

Vous écrivez vos règles en français, dans un fichier. La compétence les lit, vous pose quatre questions, les traduit en simulateur, l'exécute, et vous rend un résumé lisible plus le détail de tous les tirages en CSV.

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

Répondez à l'entretien, demandez 200 000 tirages, puis ouvrez le tableau `tours pour abattre` :

| Attaquant \ Cible | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| **Combat 2** | 10,6 | 20,7 | 20,7 | 20,6 | 20,6 |
| **Combat 3** | 5,6 | 7,2 | 10,6 | 20,7 | 20,7 |
| **Combat 4** | **3,9** | 4,5 | 5,6 | 7,2 | 10,6 |
| **Combat 5** | **3,9** | **3,9** | **3,9** | 4,5 | 5,5 |
| **Combat 6** | **3,9** | **3,9** | **3,9** | **3,9** | **3,9** |

Trois constats, et ils sont graves :

- **Un Combat 6 abat tout le monde en 3,9 tours.** Un adversaire à 2 ou à 6, c'est identique. Le plafond de 6 dés mange toute sa supériorité — au sommet, l'écart de Combat ne veut plus rien dire.
- **Un Combat 2 met 20,6 tours contre 3, 4, 5 comme 6.** Le plancher de 1 dé fait la même chose en bas.
- **Un Combat 4 contre un Combat 2 vaut exactement un Combat 6** : 3,9 tours des deux côtés. Deux points de caractéristique pour rien.

Aucune relecture des règles ne trouve ça. 200 000 tirages, oui — et il devient évident que c'est l'écart qu'il faut borner, pas le nombre de dés.

## Comment c'est fait

Deux fichiers, et la séparation entre les deux est tout l'intérêt :

- **Le moteur** ne connaît aucun jeu. Il répète une résolution, agrège, écrit. Il ne se modifie jamais.
- **`regles.py`** — vos règles, et rien d'autre. C'est le seul fichier que l'IA écrit.

```python
SCENARIOS = [...]                      # les cas à balayer
def resoudre(scenario, rng) -> dict:   # une résolution, une fois
```

> 🚨 **La règle de fer : le fichier de règles fait foi.** Le code ne décide rien, il traduit. Si le code et les règles divergent, c'est le code qui est faux. L'IA n'a pas voix au chapitre sur votre jeu — elle traduit votre texte en quelque chose d'exécutable, et c'est déjà énorme.

Le contrat complet est dans [`references/moteur.md`](plugins/cfm-gamedesign/skills/cfm-montecarlo/references/moteur.md).

## Ça marche sur un vrai jeu ?

Oui. La compétence a été rejouée sur l'action de Tir de Call of Dungeons, contre un simulateur écrit à la main pour cette règle précise. **Elle retrouve ses chiffres à moins de 0,2 point**, arme par arme, et elle retrouve la même anomalie : à Agilité 7, on touche 7 points de plus pour 0,01 blessure de moins.

## Pour les curieux

Le moteur est vérifié par 24 tests sans dépendance, dans [`evals/test_moteur.py`](plugins/cfm-gamedesign/skills/cfm-montecarlo/evals/test_moteur.py) : convergence vers des valeurs connues à la main — la moyenne d'un dé à six faces tombe sur 3,5 —, reproductibilité à graine fixée, format du CSV, refus propre des règles invalides.

Les scénarios de comportement des deux compétences sont dans leurs `evals/evals.json` — [cfm-montecarlo](plugins/cfm-gamedesign/skills/cfm-montecarlo/evals/evals.json) (10 scénarios) et [cfm-fichejdr](plugins/cfm-gamedesign/skills/cfm-fichejdr/evals/evals.json) (12 scénarios).

## Licence

MIT. Prenez, modifiez, publiez vos jeux.
