# Le contrat du fichier de règles

`montecarlo.py` ne connaît aucun jeu. Il importe un module Python, y cherche trois choses, et fait le reste.

## Ce que le module doit déclarer

```python
NOM = "…"          # titre du rapport                        (facultatif)
NOTE = "…"         # ce que la simulation suppose            (facultatif)

SCENARIOS = [      # obligatoire : un dict = une ligne de résultat
    {"attaquant": 4, "cible": 6},
    …
]

def resoudre(scenario, rng) -> dict:   # obligatoire
    ...
```

### `SCENARIOS`

Une liste de dictionnaires. **Toutes les clés doivent être les mêmes partout** — ce sont les colonnes de gauche des tableaux.

Elles se construisent presque toujours en compréhension :

```python
SCENARIOS = [
    {"attaquant": a, "cible": c}
    for a in COMBAT for c in COMBAT
]
```

⚠️ **Le produit explose vite.** 5 × 5 = 25, c'est confortable. 4 × 6 × 4 × 3 = 288, c'est déjà trop long à lire. Au-delà, réduis une dimension à ses bornes.

### `resoudre(scenario, rng)`

Joue **une** résolution, **une** fois, et retourne ce qui s'est passé.

Elle peut boucler à l'intérieur d'un tirage quand la mesure l'exige — enchaîner les tours d'un duel jusqu'à l'abattage, par exemple. Ce qu'elle ne fait jamais, c'est agréger entre tirages.

- `scenario` est un des dictionnaires de `SCENARIOS`.
- `rng` est un `random.Random` déjà initialisé avec la graine. **Utilise-le, et jamais `random` directement** : c'est lui qui rend la simulation reproductible.
- Le retour est un dict `{nom de la mesure: valeur}`. **Les mêmes clés à chaque appel**, quelle que soit l'issue.

```python
def resoudre(scenario, rng):
    des = [rng.randint(1, 6) for _ in range(nombre_de_des(scenario))]
    ...
    return {"issue": "touche", "tours pour abattre": 4}
```

## Comment les sorties sont lues

Le moteur regarde le **type** de chaque valeur retournée :

| Type retourné | Ce qui est produit |
|---|---|
| `int`, `float` | moyenne, médiane, écart-type, min, max |
| `str`, `bool` | le pourcentage de chaque modalité |

C'est le seul réglage, et il se fait en choisissant le type de retour.

> 💡 **Le piège des booléens.** `True` est un entier en Python, mais le moteur le traite en catégorie — sinon `touche : True` serait moyenné au lieu d'être compté. Si tu veux un taux, retourne une chaîne ou un booléen. Si tu veux une moyenne, retourne un nombre.

**Retourne les deux quand les deux ont un sens.** `{"issue": "touche", "tours pour abattre": 4}` donne un tableau de taux *et* un tableau de durées, pour le prix d'un.

## Les erreurs que le moteur refuse

Il s'arrête avec un message, sans trace Python :

- `SCENARIOS` ou `resoudre` absent
- `SCENARIOS` vide, ou contenant autre chose que des dictionnaires
- `resoudre` qui ne retourne pas un dictionnaire
- le fichier de règles qui plante à l'import

## La ligne de commande

```
python3 montecarlo.py regles.py [options]

  --tirages N    tirages par scénario     (défaut 20 000)
  --graine N     graine aléatoire         (défaut 1)
  --sortie DIR   dossier de sortie        (défaut .)
  --csv-max N    lignes max dans le CSV   (défaut 200 000)
```

`--csv-max` répartit un quota égal entre les scénarios. Le résumé porte toujours sur la **totalité** des tirages : seul le détail du CSV est échantillonné.

## Combien de tirages

| Usage | Tirages | Précision |
|---|---|---|
| Explorer, itérer | 20 000 | ~0,3 point de pourcentage |
| Figer un barème | 200 000 | ~0,1 point |

Au-delà, le temps de calcul double et la troisième décimale ne décide rien.
