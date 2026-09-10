# Arène — les règles du duel

*Règles d'exemple, écrites pour servir de bac à sable à `/cfm-montecarlo`.
Ce jeu n'existe pas. Il tient en une page, et il contient un défaut
d'équilibrage que la simulation trouve en une minute.*

## Les figurines

Une figurine a deux caractéristiques :

- **Combat**, de 2 à 6. C'est le nombre de dés qu'elle lance.
- **Points de vie**, 10 en standard.

## L'attaque

Une figurine attaque une fois par tour.

Le nombre de dés à six faces qu'elle lance dépend de l'écart de Combat entre
elle et son adversaire :

| Situation | Dés lancés |
|---|---|
| Autant de Combat que l'adversaire | 1 dé par point de Combat |
| **Moins** de Combat que l'adversaire | 1 dé par point de Combat, **moins** 1 dé par point d'écart |
| **Plus** de Combat que l'adversaire | 1 dé par point de Combat, **plus** 1 dé par point d'écart |

**Jamais moins de 1 dé, jamais plus de 6.**

Exemples :

- Combat 4 contre Combat 4 → 4 dés
- Combat 4 contre Combat 6 → 4 − 2 = **2 dés**
- Combat 6 contre Combat 4 → 6 + 2 = 8, ramené au plafond → **6 dés**

## Les dégâts

Chaque **5** obtenu inflige **1 blessure**.
Chaque **6** obtenu inflige **2 blessures**.

Les autres dés ne font rien.

Une figurine tombe quand ses points de vie atteignent 0.

## Ce qu'on veut savoir

- **Combien de tours faut-il pour abattre une figurine à 10 points de vie ?**
  Pour chaque couple de niveaux de Combat.
- Les cinq niveaux de Combat sont-ils réellement distincts, ou certains
  produisent-ils le même résultat ?
- Le plancher de 1 dé et le plafond de 6 dés coûtent-ils quelque chose ?
