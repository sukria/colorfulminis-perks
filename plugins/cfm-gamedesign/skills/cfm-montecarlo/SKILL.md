---
name: cfm-montecarlo
description: Équilibrer une règle de jeu par simulation Monte-Carlo. Invoquée par /cfm-montecarlo <regles.md>, elle lit un fichier de règles écrit en français, pose les questions nécessaires (ce qu'on mesure, quelles dimensions balayer, combien de tirages), traduit les règles en simulateur Python, l'exécute et produit un résumé .md plus un CSV des tirages. À utiliser pour toute question du type « est-ce que ma règle est équilibrée », « quelle arme est la meilleure », « combien coûte ce malus », « cette option sert-elle à quelque chose », ou avant de figer un barème de jeu de plateau, de figurines ou de rôle.
---

# Équilibrer une règle par simulation

**Un jeu qui repose sur des dés est un objet mesurable.** La plupart des barèmes se règlent au ressenti parce que la probabilité exacte devient indécidable dès qu'on empile trois clauses. La simulation contourne le calcul : au lieu de calculer la probabilité, on joue 200 000 fois et on compte.

Cette compétence fait ce trajet en entier, depuis un fichier de règles en français jusqu'aux tableaux qui répondent.

> 🚨 **La règle de fer : le fichier de règles fait foi.**
> Le code ne décide rien, il traduit. Si le code et les règles divergent, c'est le code qui est faux. Ne « corrige » jamais une règle en la codant autrement — signale la divergence et demande.

## Ce qui existe déjà, à ne pas réécrire

- `scripts/montecarlo.py` — le moteur. Il ne connaît aucun jeu. Il répète une résolution, agrège, et écrit. **Il ne se modifie pas.**
- `exemple/regles.md` et `exemple/regles.py` — un jeu jouet complet, à lire avant d'écrire quoi que ce soit.
- `references/moteur.md` — le contrat exact du fichier de règles.

Le seul fichier à produire est un `regles.py`. Tout le reste est fourni.

## Le déroulé

### 1 · Lire les règles et les restituer

Lis le fichier passé en argument. **Restitue-le sous forme de liste courte, une ligne par mécanisme**, et fais-la valider avant d'écrire une ligne de code.

C'est l'étape qui décide de tout : une règle mal comprise produit des tableaux justes sur un jeu qui n'existe pas.

Signale explicitement :

- les points que les règles ne tranchent pas (« que se passe-t-il si les deux camps obtiennent un 6 ? ») ;
- les termes employés dans deux sens différents ;
- ce que tu as dû interpréter.

### 2 · Poser les questions

Quatre questions, avec leurs valeurs par défaut. **Propose les défauts et n'insiste pas** : si l'utilisateur répond « va‑y », prends-les.

| Question | Défaut |
|---|---|
| **Qu'est-ce qu'on mesure ?** Les valeurs de sortie de chaque résolution. | ce que les règles produisent : issue, dégâts |
| **Quelles dimensions balayer ?** Les axes qui font varier le résultat. | tous les axes cités par les règles, bornes comprises |
| **Combien de tirages par cas ?** | `20 000` pour explorer, `200 000` pour figer un barème |
| **Quelle graine ?** | `1` — fixée, donc reproductible |

⚠️ **Garde le nombre de scénarios sous ~200.** Le produit des dimensions explose vite. S'il dépasse, propose de réduire une dimension aux bornes plutôt que de tout balayer.

### 3 · Écrire `regles.py`

Copie `exemple/regles.py` et remplace son contenu. Le contrat complet est dans `references/moteur.md`. En résumé :

```python
NOM = "..."                # titre du rapport
NOTE = "..."               # ce que la simulation suppose (facultatif)
SCENARIOS = [ {...}, ... ] # un dict = une ligne de résultat
def resoudre(scenario, rng) -> dict: ...
```

**Trois exigences, non négociables :**

- **Le barème vit en haut du fichier**, en constantes nommées. Une valeur numérique enfouie dans `resoudre()` est un barème qu'on ne pourra plus modifier sans relire le code.
- **Chaque arme, option ou clause est décrite avec les mots de sa règle**, en commentaire. C'est ce qui permet de vérifier le code contre le texte, ligne à ligne.
- **`resoudre()` ne fait aucune moyenne et n'agrège rien.** Elle joue un coup, une fois, et retourne ce qui s'est passé. L'agrégation est le travail du moteur.

### 4 · Lancer

```bash
python3 <chemin>/scripts/montecarlo.py regles.py --tirages 20000 --sortie ./resultats
```

Produit `resultats/resume.md` et `resultats/tirages.csv`.

### 5 · Lire, et chercher ce qui cloche

**C'est l'étape utile, et c'est celle qu'on saute.** Sortir des tableaux ne sert à rien si personne ne les interroge. Passe la sortie au crible et rapporte, verdict d'abord :

- **Une option qui ne change rien.** Deux lignes aux chiffres identiques = une clause décorative. C'est le défaut le plus fréquent et le plus coûteux : le joueur choisit, et son choix n'existe pas.
- **Une monotonie cassée.** Une valeur qui devrait monter avec une caractéristique et qui descend, ou qui plafonne.
- **Un écart-type énorme devant la moyenne.** Une moyenne de 3 avec un écart-type de 3, c'est un jeu où la moyenne ne se joue jamais.
- **Un `max` observé absurde**, signe d'une clause qui se cumule sans borne.
- **Un cas jamais atteint** : une modalité à 0,0 % est une règle qui ne sert à rien.

Puis propose une correction, **une seule à la fois**, et relance. La boucle « je change le barème, je relance, je compare » est le cœur de la méthode.

### 6 · Ce qui reste

Le CSV contient un détail par tirage. Il sert aux questions que le résumé ne couvre pas : distributions, seuils, corrélations. N'y touche que si une question précise se pose.

## À éviter

- **Un simulateur qui réimplémente le moteur.** Boucle, moyennes, écriture CSV : tout est déjà là.
- **Une moyenne toute seule.** Elle cache la variance, qui est souvent le vrai sujet d'un jeu.
- **Faire dire à la simulation ce qu'on voulait entendre.** Elle mesure les règles telles qu'écrites, pas telles qu'on les imaginait — et c'est exactement ce pour quoi elle sert.
- **Générer 200 000 tirages avant d'avoir validé la lecture des règles à l'étape 1.**
