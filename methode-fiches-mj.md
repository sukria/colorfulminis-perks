# Méthode « fiches MJ » — cahier des charges réutilisable

Ce fichier est un **mode d'emploi pour Claude Code**. Ouvre-le dans une session Claude
Code, puis écris :

> **`redaction scenario`**

Claude entre alors en **plan mode**, te pose les questions du protocole ci-dessous, te
soumet le plan des fiches, et — une fois le plan validé — produit le paquet **une fiche
à la fois**, chacune validée avant la suivante.

Rien ici ne dépend d'un scénario, d'un système ou d'une table en particulier. Tout ce
qui est propre à ta partie se remplit à l'entretien.

---

## 🤖 Instructions destinées à Claude

**Déclencheur.** Quand l'utilisateur écrit `redaction scenario` (ou « on écrit les
fiches », « prépare mon scénario »), applique ce fichier **intégralement** et dans
l'ordre : entretien → plan → production une par une.

**Trois interdits qui priment sur tout le reste :**

1. 🚨 **Jamais de production en lot.** Une fiche, une validation, puis la suivante. Un
   paquet produit d'un bloc est un paquet que personne ne relit.
2. 🚨 **Jamais de fiche sans son bloc ⑥.** La sortie et la phrase de relance sont
   obligatoires, y compris sur les fiches de PNJ et de lieu.
3. 🚨 **Jamais de spoiler sur une fiche joueur.** Elle ne dit que ce que le personnage
   sait *avant* la partie.

---

## Étape 1 — L'entretien (en plan mode)

Pose ces questions par lots courts, pas toutes d'un coup. Propose un défaut chaque fois
que tu peux : l'utilisateur doit pouvoir répondre « oui, comme ça » huit fois sur dix.
**N'invente rien sur la fiction** — si une réponse manque, redemande.

### Lot A · La table

- Le **système** et son édition. Comment se nomme un test (caractéristique, attribut,
  seuil) et quelle notation courte utiliser dans le bloc ③ ?
- **Durée visée** de la partie, **nombre de joueurs**.
- L'expérience du MJ : débutant, rouillé, chevronné. *(Ça décide du niveau de
  pré-résolution du bloc ③ et du volume des répliques du bloc ⑤.)*
- **Langue** de rédaction.

### Lot B · La fiction

- **Pitch en trois phrases** : la situation d'ouverture, ce qui cloche, ce qui est
  réellement en jeu.
- Le **point de départ exact** — la première image que le MJ décrit.
- La **vérité cachée**, en une phrase. *(Elle n'apparaît sur aucune fiche joueur.)*
- Les **fins possibles**, et ce qui les départage.

### Lot C · Les personnages

- Les PJ : nom, rôle, et surtout **sa clé dans le scénario** — la chose que ce
  personnage-là voit, ouvre ou déclenche et qu'aucun autre ne peut faire.
- Les PNJ qui parlent, et ce que chacun **cache**.
- Y a-t-il un **PNJ embarqué** avec le groupe ?
- 🚨 Pour chaque clé de PJ, demande **la porte de sortie** : que se passe-t-il si ce
  personnage n'est pas là, ou si son joueur rate ? Une dépendance sans porte de sortie
  est un blocage de table.

### Lot D · La structure

- Les **scènes linéaires** d'ouverture, dans l'ordre.
- Les **lieux** libres, sans ordre.
- Les éventuelles **fiches pivot** déclenchées par l'heure ou par un compteur, pas par
  un lieu.
- Les **indices** : combien, lequel doit tomber tôt, et par quelles portes il peut
  arriver. *(Un indice à porte unique est un point de rupture — signale-le.)*
- Les **accélérateurs** : ce que le MJ dégaine si la table s'enlise.

### Lot E · Les verrous de continuité

Demande explicitement s'il existe des contraintes qui doivent tenir sur tout le paquet :
horloge visible (lune, marée, délai), ordre d'événements irréversible, règle maison
(monnaie, blessures, ressources), géographie inventée à situer, tabous de ton.

**Écris-les dans le plan.** Un verrou non écrit se casse à la troisième fiche.

### Lot F · Le débouché

- **Usage privé** à ta table, ou **paquet public** distribué ?
- Si public : PJ anonymisés en rôles numérotés avec blancs à remplir, chaque dépendance
  dotée de sa porte de sortie écrite, zéro spoiler joueur, mention légale d'attribution
  de marque en pied de page de garde.

---

## Étape 2 — Le plan (à valider avant toute production)

Sors du plan mode avec un `plan-fiches-mj.md` contenant, dans cet ordre :

1. **La table** — système, format, durée, joueurs.
2. **Le groupe** — un PJ par ligne, avec sa clé et sa porte de sortie.
3. **Les verrous de continuité** — la liste du lot E, chacun avec son *pourquoi*.
4. **Les tâches** — une ligne = une fiche, en case à cocher, groupées en lots.

Le plan est **verrouillé** une fois validé : toute évolution ultérieure se rediscute
explicitement, elle ne se glisse pas dans une fiche.

### Le découpage en lots, par défaut

| Lot | Contenu |
|---|---|
| **Lot 0** | `CH` chronologie · `TB` tableau de bord · `B0` briefing d'intro · fiches de règle maison |
| **Lot 1** | `S1…Sn` les scènes linéaires d'ouverture, plus les fiches pivot `P*` |
| **Lot 1 bis** | `J*` une fiche joueur par PJ — **aucun spoiler** |
| **Lot 2** | `K0` plan du lieu central · `L1…Ln` les lieux |
| **Lot 3** | `N1…Nn` les PNJ |
| **Lot 4** | l'acte final : le lieu du dénouement, l'antagoniste, les fins |
| **Hors paquet** | kit de règles, fiche de personnage, documents de référence |

Deux numérotations qui **ne se mélangent jamais dans la pile** : `S*` se joue dans
l'ordre du numéro, `L*` se pioche quand les joueurs y entrent.

---

## Étape 3 — L'anatomie d'une fiche

Une fiche = **une page A4**, autonome, imprimable, empilable. Les mêmes six blocs,
toujours à la même place — **l'œil doit trouver sans lire**.

| | Bloc | Rôle |
|---|---|---|
| **En-tête** | N° · titre · lieu · PNJ présents | Repérage quand les fiches sont empilées |
| **①** | **À LIRE À VOIX HAUTE** — encadré, **5 lignes max** | Le MJ lit, il n'improvise pas |
| **②** | **CE QUI SE PASSE** — **3 beats maximum** | Le déroulé, pas le décor |
| **③** | **SI LES PJ FONT ÇA → JETTE ÇA** | Le jet, le modificateur, la réussite, l'échec. **Pré-résolu** |
| **④** | **INDICES À PLACER** — cases à cocher | Cochées en direct |
| **⑤** | **RÉPLIQUES** — prêtes à dire | Le MJ ne cherche pas ses mots |
| **⑥** | **SORTIE + SI ÇA BLOQUE** | L'enchaînement, et la phrase de relance |

> 🚨 **Le bloc ⑥ est le plus important du paquet.** La peur numéro un d'un MJ débutant,
> c'est le silence après « bon… vous faites quoi ? ». Aucune fiche ne sort sans sa
> phrase de relance écrite noir sur blanc.

### Les règles de rédaction, dans l'ordre de fréquence des fautes

- **Le bloc ③ est pré-résolu.** Écris le résultat, pas la procédure : ce que le joueur
  obtient s'il réussit **et** ce qu'il obtient s'il rate. Un échec ne rend jamais la
  main vide — il rend une information dégradée ou un coût.
- **Un échec ne ferme jamais une porte d'indice.** Si un indice n'a qu'une porte, ouvres-en
  une deuxième ou rends-le automatique.
- **Trois beats, pas quatre.** Ce qui ne tient pas en trois beats est deux scènes.
- **Les répliques sont dites, pas décrites.** « Il est méfiant » ne s'utilise pas à
  table ; « On prend l'eau à la source, plus haut » s'utilise.
- **Ce qui est vrai va sur la fiche MJ, ce qui est su va sur la fiche joueur.**
- **Pas de décor sans usage.** Un détail qui n'est ni un indice, ni une réplique, ni un
  danger, saute.
- Emojis avec parcimonie, comme repères (🚨 verrou, ⚠️ garde-fou, 📸 à montrer).

### Le tableau de bord — une page qui n'est pas une fiche de scène

En permanence sous les yeux du MJ : l'ordre des scènes, **les indices en cases à
cocher**, les **accélérateurs avec une case « brûlé »** (pour ne jamais lancer deux
fois le même ressort), les rappels de règle, l'état des PNJ.

---

## Étape 4 — La production, une fiche à la fois

Pour chaque ligne cochable du plan, dans l'ordre des lots :

1. **Annonce** la fiche que tu produis et ce qu'elle doit accomplir en une phrase.
2. **Écris le `.html`** au gabarit ci-dessous, une page A4, dans `fiches/<CODE>-<slug>.html`.
3. **Produis le `.pdf`** — impression A4 depuis le HTML (moteur au choix ; toute chaîne
   qui respecte `@page { size: A4 }` convient).
4. **Vérifie** : la fiche tient-elle sur **une seule page** ? Les six blocs y sont-ils ?
   Le bloc ⑥ a-t-il sa phrase de relance ? Si non, coupe — **on n'ajoute pas de page**.
5. **Attends la validation** de l'utilisateur, coche la ligne dans le plan, passe à la
   suivante.

Si une fiche déborde, ce qui saute en premier : le décor, puis les nuances du bloc ②,
puis les entrées rares du bloc ③. Jamais les blocs ①, ④ et ⑥.

---

## Le gabarit CSS — à coller tel quel dans chaque `.html`

```html
<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<title>CODE — Titre de la fiche</title>
<style>
@page { size: A4; margin: 9mm 10mm; }
* { box-sizing: border-box; }
body { margin:0; color:#111; background:#fff; font-size:7.9pt; line-height:1.28;
  font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif; }
.hdr { display:flex; justify-content:space-between; align-items:flex-end;
  border-bottom:3px double #000; padding-bottom:1.4mm; margin-bottom:2mm; }
h1 { font-size:15pt; letter-spacing:.05em; text-transform:uppercase; margin:0; }
h1 small { display:block; font-size:6.6pt; letter-spacing:.13em; font-weight:normal;
  text-transform:none; font-style:italic; margin-top:.9mm; }
.num { font-size:22pt; font-weight:700; line-height:1; }
h2 { font-size:6.8pt; letter-spacing:.14em; text-transform:uppercase; margin:0 0 1mm;
  padding-bottom:.5mm; border-bottom:1.5px solid #000; }
h2 .n { display:inline-block; background:#000; color:#fff; padding:0 1.1mm;
  margin-right:1.2mm; font-size:6.6pt; }
.cols { column-count:2; column-gap:5.5mm; }
.box { border:1px solid #000; padding:1.6mm 2mm; margin-bottom:2.2mm; break-inside:avoid; }
.box.hv { border-width:2px; }
.box.dk { background:#f2f2ef; }
.read { border:2px solid #000; background:#faf8f3; padding:2mm 2.4mm; margin-bottom:2.2mm;
  break-inside:avoid; font-style:italic; font-size:8.4pt; line-height:1.4; }
.read .lbl { font-style:normal; font-size:6.2pt; letter-spacing:.16em; text-transform:uppercase;
  display:block; margin-bottom:1.2mm; }
p { margin:0 0 1mm; }
ul, ol { margin:0 0 1mm; padding-left:3.8mm; }
li { margin:0 0 .7mm; }
.ck { list-style:none; padding-left:0; }
.ck li { display:flex; gap:1.3mm; align-items:baseline; }
.ck b.sq { display:inline-block; width:2.5mm; height:2.5mm; border:1px solid #000;
  flex:0 0 auto; margin-top:.4mm; }
table { width:100%; border-collapse:collapse; font-size:7.1pt; margin:0 0 1mm; }
th,td { border:1px solid #000; padding:.5mm .9mm; text-align:left; vertical-align:top; }
th { background:#e8e8e6; font-size:6.2pt; letter-spacing:.06em; text-transform:uppercase; }
.say { font-style:italic; border-left:2.2px solid #000; padding-left:1.8mm; margin:.8mm 0 1.2mm; }
.say b { font-style:normal; }
.hint { font-size:6.5pt; color:#444; }
.beat { font-size:6.4pt; letter-spacing:.12em; text-transform:uppercase;
  border-bottom:1px solid #999; padding-bottom:.4mm; margin:1.6mm 0 .8mm; }
.beat:first-child { margin-top:0; }
@media screen { body { padding:9mm; } }
</style></head><body>
```

### Le squelette de corps

```html
<div class="hdr">
  <h1>Titre de la fiche<small>Où · qui est présent · ce que la fiche accomplit</small></h1>
  <div class="num">CODE</div>
</div>

<div class="read">
  <span class="lbl">① À lire à voix haute</span>
  « Cinq lignes maximum, au présent, adressées aux joueurs. »
</div>

<div class="cols">
  <div class="box hv dk">
    <h2><span class="n">②</span> Ce qui se passe</h2>
    <div class="beat">1 · …</div><p>…</p>
    <div class="beat">2 · …</div><p>…</p>
    <div class="beat">3 · …</div><p>…</p>
  </div>

  <div class="box hv">
    <h2><span class="n">③</span> Si les PJ font ça → jette ça</h2>
    <table>
      <tr><th>Le joueur</th><th>Le jet</th><th>Ce qu'il obtient</th></tr>
      <tr><td>…</td><td>…</td><td>Réussi : … Raté : …</td></tr>
    </table>
  </div>

  <div class="box dk">
    <h2><span class="n">④</span> Indices à placer</h2>
    <ul class="ck"><li><b class="sq"></b><span><b>INDICE n</b> — …</span></li></ul>
  </div>

  <div class="box">
    <h2><span class="n">⑤</span> Répliques</h2>
    <p class="say"><b>Nom :</b> « … » <span class="hint">(ton, sous-texte)</span></p>
  </div>

  <div class="box hv">
    <h2><span class="n">⑥</span> Sortie · si ça bloque</h2>
    <p><b>Vers :</b> …</p>
    <p class="hint">🚨 <b>Si le silence tombe, dis :</b> « … »</p>
  </div>
</div>
</body></html>
```

---

## Le contrôle final — avant de déclarer le paquet fini

- [ ] Chaque fiche tient sur **une page**.
- [ ] Chaque fiche a ses six blocs, **⑥ compris**.
- [ ] Chaque indice a **au moins deux portes**.
- [ ] Chaque clé de PJ a **sa porte de sortie** si le personnage manque à table.
- [ ] Aucune fiche joueur ne contient d'information postérieure au début de la partie.
- [ ] Le tableau de bord liste tous les indices et tous les accélérateurs.
- [ ] Les verrous de continuité du plan tiennent sur **toutes** les fiches.
- [ ] Si le paquet est public : PJ anonymisés, dépendances neutralisées, mention légale.

> 🎯 **La contrainte qui décide de tout : un scénario doit être maîtrisable sans huit
> heures de lecture préliminaire.** Tout ce qui contredit ça est une régression, quelle
> que soit sa qualité littéraire.
