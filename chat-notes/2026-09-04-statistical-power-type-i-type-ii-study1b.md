# Puissance statistique, erreurs de type I et II — une lecture de non-statisticien

**Date :** 2026-09-04  
**Statut :** draft pédagogique, à relire humainement avant promotion.  
**Contexte d'apparition :** Study 1B du dépôt `siamese-embedding-compression-lab`, pendant le préflight de puissance puis les analyses S2/S3 de la comparaison biométrique `raw512` vs `random128` / `PCA128` / `Siamese128`.  
**Autorité scientifique de cette note :** aucune. Cette note explique des sources et des artefacts de recherche ; elle ne les remplace pas.

## 1. L'idée avant le vocabulaire

Un test statistique ressemble à un **dispositif de décision imparfait**.

On lui donne des mesures et on lui demande de prendre une décision. Mais deux choses peuvent mal se passer :

1. il peut déclencher une alarme alors qu'il n'y avait pas de problème ;
2. il peut ne pas déclencher alors qu'un problème — ou un effet que l'on voulait détecter — était réellement présent.

Les statisticiens appellent ces deux erreurs **type I** et **type II**.

La **puissance** (*statistical power*) répond ensuite à une autre question :

> Si l'effet que je veux détecter existe réellement, mon expérience et ma règle de décision ont-elles de bonnes chances de le détecter ?

C'est une propriété du **test + plan expérimental + quantité d'information + effet réel supposé**, pas une note de qualité du modèle ML.

---

## 2. Une analogie d'ingénierie : le détecteur de fumée

Imaginons un détecteur de fumée.

| Réalité | Décision du détecteur | Lecture |
|---|---|---|
| Pas d'incendie | Alarme | **Erreur de type I** : fausse alarme |
| Incendie | Pas d'alarme | **Erreur de type II** : événement manqué |
| Pas d'incendie | Pas d'alarme | décision correcte |
| Incendie | Alarme | décision correcte |

La puissance correspondrait à :

> Parmi les vrais incendies d'une intensité donnée, quelle proportion sera effectivement détectée par ce détecteur dans ces conditions ?

Un détecteur peut être extrêmement prudent pour éviter les fausses alarmes et devenir, en contrepartie, moins capable de détecter des signaux faibles. C'est l'un des compromis fondamentaux que l'on retrouve dans les tests statistiques.

---

## 3. Erreur de type I — alpha

La probabilité d'erreur de type I est traditionnellement notée **α (alpha)**.

Dans le cadre classique où l'hypothèse nulle `H0` dit « pas d'effet », l'erreur de type I revient à dire :

> **Je déclare un effet alors qu'il n'y en a pas.**

C'est le cousin statistique du **faux positif** ou de la **fausse alarme**.

Le NIST Engineering Statistics Handbook décrit `α` comme le risque de rejeter l'hypothèse nulle alors qu'elle est vraie, et `1-β` comme la puissance du test.

### Attention : le sens métier dépend de la formulation de H0

Il ne faut pas mémoriser « type I = faux positif » sans regarder ce que dit réellement `H0`.

Dans notre test de **non-infériorité**, nous formulons essentiellement :

`H0 : la compression est inférieure d'au moins la marge autorisée`  
`H1 : la compression est non inférieure dans la marge autorisée`

avec une marge de `0,03` sur la différence de FNMR.

Dans ce cadre, une erreur de type I devient :

> **déclarer à tort la compression non inférieure alors qu'elle est en réalité trop dégradée.**

C'est donc ici un **faux PASS potentiellement dangereux**.

---

## 4. Erreur de type II — beta

La probabilité d'erreur de type II est traditionnellement notée **β (beta)**.

C'est le cas où le test ne parvient pas à détecter une situation réelle qu'il était censé pouvoir distinguer.

Dans le cadre classique :

> **Un effet existe, mais notre expérience ne réussit pas à le mettre en évidence.**

C'est proche d'un **faux négatif** ou d'une **détection manquée**.

Dans notre test de non-infériorité, cela devient :

> **la compression est réellement dans la marge acceptable, mais l'expérience ne parvient pas à démontrer sa non-infériorité.**

C'est donc plutôt un **faux FAIL** ou, plus rigoureusement, une conclusion `NOT DEMONSTRATED` alors que la situation réelle était acceptable.

Cela peut arriver parce que :

- l'échantillon contient trop peu d'information réellement indépendante ;
- les mesures sont trop variables ;
- l'effet recherché est petit ;
- la règle de décision est très conservatrice ;
- plusieurs sources d'incertitude s'additionnent.

---

## 5. Puissance : `Power = 1 - β`

La puissance est la probabilité de **réussir à détecter ce que l'on veut détecter lorsque la situation réelle correspond à l'alternative considérée**.

Formellement :

`Power = 1 - β`

Mais la lecture importante est opérationnelle :

> **Si je répétais énormément de fois la même expérience dans un monde où je connais la vraie situation, dans quelle proportion des expériences mon test donnerait-il la décision attendue ?**

La puissance doit donc toujours être associée à une **situation réelle précise**. Elle n'est pas un nombre absolu du test.

Détecter une très grosse différence est plus facile que détecter une toute petite différence. Un même protocole peut donc avoir une puissance élevée pour un gros effet et faible pour un petit effet.

---

## 6. Rencontre Study 1B : pourquoi la notion est devenue nécessaire

Study 1B cherche à comparer la performance biométrique 1:1 d'une représentation AdaFace `raw512` avec trois routes compressées en 128 dimensions.

L'estimand principal est la différence :

`Δ = FNMR_compressed - FNMR_raw`

au même point opératoire `FMR = 0,01`.

La marge de non-infériorité est `0,03` : une route compressée doit pouvoir être considérée comme non inférieure si sa dégradation est suffisamment petite par rapport à cette marge, selon la règle statistique pré-définie.

Le préflight n'ouvre pas les vraies performances. Il simule des mondes où la vraie différence est connue, par exemple :

- `Δ = 0` : aucune dégradation réelle ;
- `Δ = +0,01` : légère dégradation, mais encore nettement à l'intérieur de la marge `0,03`.

On demande alors :

> Dans combien de ces mondes simulés notre règle réussirait-elle à conclure correctement à la non-infériorité ?

C'est exactement une **mesure de puissance**.

---

## 7. Pourquoi S3 a échoué sans que les futures mesures soient « fausses »

Dans S3, même en doublant l'information de paires réellement distinctes (`x2`), la puissance simulée à `Δ = +0,01` n'a atteint que :

`0,6485`.

Lecture non-statisticien :

> Si la vraie compression ne dégradait le FNMR que de +0,01, notre règle actuelle ne réussirait à le démontrer que dans environ 65 expériences sur 100 sous le générateur synthétique retenu.

Donc, dans environ 35 expériences sur 100, elle pourrait répondre « non démontré » alors que la vraie différence reste dans la marge acceptable.

Cela révèle principalement un **risque d'erreur de type II** élevé pour cette situation.

Cela **ne signifie pas** que les valeurs futures de FNMR, ROC, EER ou les différences `raw512` vs `128D` seraient fausses. Cela signifie que la **force de la conclusion confirmatoire** attachée à ces valeurs serait insuffisamment fiable avec cette règle.

---

## 8. Pourquoi la règle `5 seeds sur 5` compte autant

Le protocole initial demandait que les cinq réalisations d'entraînement passent chacune la limite statistique.

En langage d'ingénieur, c'est proche d'un système série :

> cinq sous-conditions doivent toutes être vertes ; une seule rouge suffit à faire échouer le gate.

Cette règle protège fortement contre une réalisation d'entraînement défavorable, mais elle peut aussi augmenter beaucoup le nombre de faux FAIL.

Les travaux S2 et S3 ont précisément séparé plusieurs causes possibles :

- règle d'agrégation des seeds ;
- variabilité entre entraînements ;
- quantité d'information biométrique réellement distincte ;
- largeur des intervalles d'incertitude.

Le résultat S3 a montré qu'ajouter davantage de paires distinctes améliore la puissance mais ne suffit pas à atteindre le seuil pré-déclaré de `0,90` sous la règle `5/5`.

---

## 9. Pourquoi `Power = 0,90` ne veut pas dire « 90 % de chances que notre conclusion soit vraie »

C'est un contresens fréquent.

Une puissance de 90 % signifie :

> **si une situation réelle précise est vraie, le protocole produira la décision recherchée dans environ 90 % des répétitions théoriques compatibles avec le modèle de calcul.**

Cela ne signifie pas :

- 90 % de chances que `H1` soit vraie après avoir vu les données ;
- 90 % de chances que le matcher soit bon ;
- 90 % d'accuracy ;
- 90 % de confiance au sens d'un intervalle de confiance.

Ce sont des objets différents.

---

## 10. Et une erreur de type III ?

Il n'existe pas de **type III universel et canonique** comparable aux types I et II dans le cadre standard des tests d'hypothèses.

Certains domaines utilisent l'expression « erreur de type III » pour des idées différentes : mauvaise direction de l'effet, bonne réponse à la mauvaise question, mauvais modèle, etc.

Dans Diderot, il faut donc retenir :

> **Type I et Type II sont les catégories standards. « Type III » doit toujours être défini par la source qui l'utilise ; ne jamais lui supposer une signification universelle.**

---

## 11. Carte mentale pour un non-statisticien

```text
                        REALITE
                situation A     situation B
              +-------------+-------------+
DECISION       |             |             |
du test        | correcte    | Type I ou   |
              |             | Type II     |
              +-------------+-------------+
```

La bonne façon de remplir la table est toujours :

1. écrire exactement `H0` ;
2. écrire exactement `H1` ;
3. seulement ensuite traduire type I et type II en risque métier.

Pour Study 1B non-infériorité :

```text
Type I  -> faux PASS : déclarer non inférieur alors que trop dégradé
Type II -> faux FAIL / NOT DEMONSTRATED : ne pas démontrer une non-infériorité réelle
Power   -> capacité du protocole à éviter ce faux FAIL pour une vraie situation donnée
```

---

## 12. Prérequis et connexions

**Prérequis :** probabilité, hypothèse nulle `H0`, hypothèse alternative `H1`, intervalle de confiance, différence/effet `Δ`.

**Connexions :**

- seuil de significativité `α` ;
- erreur de type II `β` ;
- puissance `1-β` ;
- taille d'effet ;
- taille d'échantillon et quantité d'information indépendante ;
- non-infériorité ;
- bootstrap et dépendance entre observations ;
- calibration d'un protocole de décision.

---

## 13. Misconceptions à retenir

**Faux :** « Si la puissance est faible, les mesures sont fausses. »  
**Correction :** la puissance faible signifie surtout que la procédure de décision risque souvent de ne pas démontrer un effet réel d'une taille donnée.

**Faux :** « Type I = toujours faux positif métier. »  
**Correction :** le sens métier dépend de la définition de `H0`. En non-infériorité, type I correspond à déclarer à tort la non-infériorité.

**Faux :** « Power = confiance dans le résultat obtenu. »  
**Correction :** la puissance est une propriété fréquentiste du protocole sous une vérité spécifiée, pas une probabilité postérieure sur l'hypothèse.

**Faux :** « Ajouter des milliers de bootstrap augmente la quantité d'information réelle. »  
**Correction :** davantage de répétitions bootstrap peuvent réduire l'erreur Monte-Carlo du calcul, mais ne créent pas de nouvelles identités ou observations indépendantes.

---

## 14. Understanding gate

Avant de considérer cette notion assimilée, être capable de répondre sans formule à ces quatre questions :

1. Quelle différence entre une fausse alarme et une détection manquée ?
2. Pourquoi la signification métier du type I dépend-elle de la manière dont `H0` est formulée ?
3. Que signifie réellement « puissance = 90 % » ?
4. Pourquoi une faible puissance peut-elle produire un `NOT DEMONSTRATED` sans rendre les mesures descriptives fausses ?

Puis être capable de reconstruire :

`Power = 1 - β`.

---

## Sources et provenance

### Définition statistique de référence

NIST/SEMATECH Engineering Statistics Handbook, sections sur les tests statistiques et les techniques quantitatives :

- https://www.itl.nist.gov/div898/handbook/prc/section1/prc13.htm
- https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm

Le NIST y définit `α` comme le risque de rejeter `H0` lorsqu'elle est vraie, `β` comme le risque de ne pas rejeter `H0` lorsqu'elle est fausse, et la puissance comme `1-β` pour une alternative spécifiée.

### Contexte d'apparition dans notre recherche

`gharbonnier78/siamese-embedding-compression-lab`, Study 1B :

- contrat de sensibilité S1–S4 : `protocol/simulations/STUDY1B_POWER_DESIGN_SENSITIVITY_V0_1_2026-08-31.yaml` ;
- contrat S3 final : `protocol/simulations/STUDY1B_POWER_DESIGN_S3_POWER_CALIBRATION_V0_1_2026-09-03.yaml` ;
- clôture S3 et changement de perspective vers S4NEW : commit `cfb1bdb05c9cfab0da20d89ae251cdc17930e088`.

Ces artefacts sont des **encounters** du concept : ils expliquent pourquoi la puissance est devenue nécessaire dans notre recherche. Ils ne remplacent pas la définition statistique de référence.

## Notation — handoff vers l'atlas canonique

Les notations `H0`, `H1`, `α`, `β` et `1-β` sont candidates à une entrée ou à un enrichissement dans le registre canonique `gharbonnier78/mmals-ml-wiki/mathematics/notation/registry.json`. Elles ne sont pas dupliquées dans un registre local Diderot.
