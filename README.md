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

Le dépôt contient un jeu jouet complet, [Les Gardiens du Pont](plugins/cfm-gamedesign/skills/cfm-montecarlo/exemple/regles.md) — quatre armes, une armure, une maladresse. **Il contient un défaut d'équilibrage, et la simulation le trouve en une minute.**

```bash
cd plugins/cfm-gamedesign/skills/cfm-montecarlo/exemple
python3 ../scripts/montecarlo.py regles.py --tirages 200000 --sortie ./resultats
```

Ouvrez `resultats/resume.md` et comparez ces deux lignes, à Vigueur 3 sans armure :

| Arme | Réussite | Dégâts moyens |
|---|---|---|
| Bâton | 87,3 % | 1,49 |
| Arc long | **96,0 %** | **1,50** |

L'Arc long réussit 9 points de plus et ne fait pas plus de dégâts. Sa clause — « les 3 comptent comme des 4 » — crée des succès qui touchent sans blesser, puisque le barème ne paie que les 5 et les 6. **C'est une option décorative : le joueur choisit, et son choix n'existe pas.**

Aucune relecture ne trouve ça. 200 000 tirages, oui.

## Comment c'est fait

Deux fichiers, et la séparation entre les deux est tout l'intérêt :

- **`scripts/montecarlo.py`** — le moteur. Il ne connaît aucun jeu. Il répète une résolution, agrège, écrit. Il ne se modifie jamais.
- **`regles.py`** — vos règles, et rien d'autre. C'est le seul fichier que l'IA écrit.

```python
SCENARIOS = [...]                      # les cas à balayer
def resoudre(scenario, rng) -> dict:   # un coup, une fois
```

Le contrat complet tient dans [`references/moteur.md`](plugins/cfm-gamedesign/skills/cfm-montecarlo/references/moteur.md).

> 🚨 **La règle de fer : le fichier de règles fait foi.** Le code ne décide rien, il traduit. Si le code et les règles divergent, c'est le code qui est faux. L'IA n'a pas voix au chapitre sur votre jeu — elle traduit votre texte en quelque chose d'exécutable, et c'est déjà énorme.

## Ça marche sur un vrai jeu ?

Oui. La compétence a été rejouée sur l'action de Tir de Call of Dungeons, contre un simulateur écrit à la main pour cette règle précise. **Elle retrouve ses chiffres à moins de 0,2 point**, arme par arme, et elle retrouve la même anomalie : à Agilité 7, on touche 7 points de plus pour 0,01 blessure de moins.

## Validation

```bash
python3 plugins/cfm-gamedesign/skills/cfm-montecarlo/evals/test_moteur.py
```

22 vérifications, sans pytest ni dépendance : convergence vers des valeurs connues à la main, reproductibilité à graine fixée, format du CSV, refus propre des règles invalides, et présence de l'anomalie dans l'exemple.

Les scénarios de comportement de la compétence sont dans [`evals/evals.json`](plugins/cfm-gamedesign/skills/cfm-montecarlo/evals/evals.json).

## Licence

MIT. Prenez, modifiez, publiez vos jeux.
