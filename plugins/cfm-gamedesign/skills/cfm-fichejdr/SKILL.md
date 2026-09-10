---
name: cfm-fichejdr
description: Produire un paquet de fiches de MJ jouables en direct pour une partie de jeu de rôle — une fiche par scène, par lieu, par PNJ, sur une page A4, en HTML et PDF. Invoquée par /cfm-fichejdr, ou par « rédaction scénario », « on écrit les fiches », « prépare mon scénario ». Indépendante du système et de la table : tout ce qui est propre à la partie se remplit par un entretien. À utiliser pour préparer une partie à maîtriser sans huit heures de relecture, pour convertir un scénario du commerce en paquet jouable, ou pour distribuer un scénario maison.
---

# Les fiches de MJ

**Un scénario doit être maîtrisable sans huit heures de lecture préliminaire.** C'est la contrainte qui décide de tout : ce qui la contredit est une régression, quelle que soit la qualité littéraire.

Une fiche est donc un **support d'exécution**, lu à table, une main dessus, pendant que six personnes attendent. Pas un document de lecture.

Le trajet est toujours le même : **entretien → plan validé → production une fiche à la fois.**

> 🚨 **Trois interdits, qui priment sur tout le reste.**
>
> 1. **Jamais de production en lot.** Une fiche, une validation, puis la suivante. Un paquet produit d'un bloc est un paquet que personne ne relit.
> 2. **Jamais de fiche sans son bloc ⑥.** La sortie et la phrase de relance sont obligatoires, y compris sur les fiches de PNJ et de lieu.
> 3. **Jamais de spoiler sur une fiche joueur.** Elle ne dit que ce que le personnage sait *avant* la partie.

## Étape 1 · L'entretien

Passe en **plan mode**. Les questions sont dans `references/entretien.md`, en six lots — la table, la fiction, les personnages, la structure, les verrous de continuité, le débouché.

- **Pose-les par lots courts**, jamais toutes d'un coup.
- **Propose un défaut à chaque fois que tu peux** : l'utilisateur doit pouvoir répondre « oui, comme ça » huit fois sur dix.
- 🚨 **N'invente rien sur la fiction.** Si une réponse manque, redemande. Une fiche inventée se découvre à table, au pire moment.

## Étape 2 · Le plan, à valider

Sors du plan mode avec un `plan-fiches-mj.md` :

1. **La table** — système, format, durée, joueurs.
2. **Le groupe** — un PJ par ligne, avec sa clé et sa porte de sortie.
3. **Les verrous de continuité**, chacun avec son *pourquoi*.
4. **Les tâches** — une ligne = une fiche, en case à cocher, groupées en lots.

Le découpage par défaut :

| Lot | Contenu |
|---|---|
| **0** | `CH` chronologie · `TB` tableau de bord · `B0` briefing · fiches de règle maison |
| **1** | `S1…Sn` les scènes linéaires, plus les fiches pivot `P*` |
| **1 bis** | `J*` une fiche joueur par PJ — **aucun spoiler** |
| **2** | `K0` plan du lieu central · `L1…Ln` les lieux |
| **3** | `N1…Nn` les PNJ |
| **4** | l'acte final : lieu du dénouement, antagoniste, fins |

⚠️ **`S*` et `L*` ne se mélangent jamais dans la pile** : les `S` se jouent dans l'ordre du numéro, les `L` se piochent quand les joueurs entrent dans le lieu.

**Le plan est verrouillé une fois validé.** Toute évolution se rediscute explicitement ; elle ne se glisse pas dans une fiche.

## Étape 3 · La production, une fiche à la fois

Pour chaque ligne cochable, dans l'ordre des lots :

1. **Annonce** la fiche et ce qu'elle accomplit, en une phrase.
2. **Écris le `.html`** dans `fiches/<CODE>-<slug>.html`, au gabarit `references/gabarit.html`, collé tel quel.
3. **Produis le `.pdf`** — impression A4 depuis le HTML, moteur au choix.
4. **Vérifie** : une seule page ? Les six blocs ? Le bloc ⑥ a-t-il sa phrase de relance ?
5. **Attends la validation**, coche la ligne du plan, passe à la suivante.

⚠️ **Si une fiche déborde, on coupe — on n'ajoute jamais de page.** Saute en premier : le décor, puis les nuances du bloc ②, puis les entrées rares du bloc ③. **Jamais les blocs ①, ④ et ⑥.**

## L'anatomie d'une fiche

Une page A4, autonome, imprimable, empilable. **Les mêmes six blocs, toujours à la même place — l'œil doit trouver sans lire.**

| | Bloc | Rôle |
|---|---|---|
| **En-tête** | N° · titre · lieu · PNJ présents | Repérage quand les fiches sont empilées |
| **①** | **À LIRE À VOIX HAUTE**, encadré, 5 lignes max | Le MJ lit, il n'improvise pas |
| **②** | **CE QUI SE PASSE**, 3 beats maximum | Le déroulé, pas le décor |
| **③** | **SI LES PJ FONT ÇA → JETTE ÇA** | Le jet, la réussite, l'échec. **Pré-résolu** |
| **④** | **INDICES À PLACER**, cases à cocher | Cochées en direct |
| **⑤** | **RÉPLIQUES**, prêtes à dire | Le MJ ne cherche pas ses mots |
| **⑥** | **SORTIE · SI ÇA BLOQUE** | L'enchaînement, et la phrase de relance |

> 🚨 **Le bloc ⑥ est le plus important du paquet.** La peur numéro un d'un MJ, c'est le silence après « bon… vous faites quoi ? ». Aucune fiche ne sort sans sa phrase de relance écrite noir sur blanc.

Le détail des règles de rédaction est dans `references/anatomie-fiche.md`. Les quatre fautes les plus fréquentes :

- **Le bloc ③ n'est pas une procédure, c'est un résultat.** Ce que le joueur obtient s'il réussit **et** s'il rate. Un échec ne rend jamais la main vide : il rend une information dégradée, ou un coût.
- **Un échec ne ferme jamais une porte d'indice.** Un indice à porte unique est un point de rupture : ouvre-en une deuxième, ou rends-le automatique.
- **Les répliques sont dites, pas décrites.** « Il est méfiant » ne s'utilise pas à table. « On prend l'eau à la source, plus haut » s'utilise.
- **Pas de décor sans usage.** Un détail qui n'est ni un indice, ni une réplique, ni un danger, saute.

## Le contrôle final

Avant de déclarer le paquet fini, passe la liste de `references/controle-final.md`. Elle vérifie ce qui casse une partie : une fiche à deux pages, un indice à porte unique, une dépendance de PJ sans porte de sortie, un spoiler sur une fiche joueur.
