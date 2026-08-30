# Puissance statistique a priori — vérifier qu'une étude a une chance raisonnable de conclure

> **Question de départ :** même si notre méthode statistique est correctement calibrée, avons-nous assez d'information pour qu'elle puisse réellement démontrer l'effet qui nous intéresse ?

Cette entrée complète la note sur la [couverture statistique à vérité connue](statistical-coverage-known-truth.md).

La couverture demande : **« mon intervalle se comporte-t-il correctement ? »**

La puissance demande : **« si l'effet intéressant existe vraiment, ma procédure a-t-elle une probabilité suffisante de le détecter ou de satisfaire la règle de décision ? »**

Dans Study 1B, il s'agit d'une simulation **a priori**, avant d'ouvrir les résultats biométriques SCREEN/TEST.

---

## 1. Pourquoi la couverture ne suffit pas

Une procédure peut être parfaitement calibrée et pourtant être trop imprécise pour conclure.

Exemple caricatural : un intervalle extrêmement large peut contenir très souvent la vraie valeur. Sa couverture peut être excellente, mais il sera peu utile pour distinguer deux hypothèses proches.

Nous avons donc deux questions distinctes :

```text
Couverture : l'incertitude annoncée est-elle crédible ?
Puissance   : cette incertitude est-elle assez petite pour décider ?
```

Les deux sont nécessaires avant une étude coûteuse ou une décision scientifique importante.

---

## 2. Définition classique

Dans un test d'hypothèse simple, la puissance pour une valeur réelle donnée du paramètre est :

\[
\mathrm{Power}(\theta)
=
P_\theta(\text{rejeter }H_0).
\]

Autrement dit : si le monde est réellement dans une situation `θ`, quelle est la probabilité que notre expérience produise la conclusion recherchée ?

L'erreur de type II correspond alors à ne pas détecter cet effet malgré sa présence :

\[
\beta(\theta)=1-\mathrm{Power}(\theta).
\]

Study 1B utilise une règle de non-infériorité plus structurée qu'un test simple, mais l'idée reste la même : **simuler des mondes où nous savons ce qui est vrai et compter la fréquence à laquelle la règle scientifique complète réussit.**

---

## 3. La question Study 1B

La future étude comparera une représentation compressée à `raw512` via :

\[
\Delta_{FNMR}
=
FNMR_{compressé}-FNMR_{raw512}.
\]

La marge de non-infériorité préenregistrée est :

\[
\delta = 0.03.
\]

Pour un seed donné, la règle exige que la borne supérieure unilatérale à 97,5 % sur Δ reste sous cette marge :

\[
UCB_{97.5\%}(\Delta_{FNMR}) < 0.03.
\]

Mais Study 1B ne demande pas qu'un seul seed chanceux réussisse. La règle gelée exige que **les cinq seeds** `[11, 29, 47, 71, 101]` satisfassent le critère.

La décision simulée pour un dataset devient donc :

\[
\bigcap_{s\in\{11,29,47,71,101\}}
\left\{UCB_s<0.03\right\}.
\]

C'est cette règle complète — pas une approximation plus facile — dont la puissance doit être évaluée.

---

## 4. Les deux alternatives planifiées

Le contrat de puissance a gelé deux scénarios non inférieurs :

\[
\Delta_{vrai}=0
\qquad\text{et}\qquad
\Delta_{vrai}=0.01.
\]

Pourquoi les deux ?

- `Δ=0` représente un monde où la compression ne dégrade pas le FNMR par rapport à raw512 ;
- `Δ=0.01` représente une petite dégradation réelle, mais encore nettement à l'intérieur de la marge de non-infériorité `0.03`.

La frontière `Δ=0.03` n'est pas la cible de puissance. À la frontière même, il serait incohérent d'exiger que la procédure conclue très souvent strictement en dessous de cette frontière.

Le gate préenregistré exige :

\[
Power(\Delta=0)\ge0.90
\quad\text{et}\quad
Power(\Delta=0.01)\ge0.90.
\]

---

## 5. Comment la puissance est estimée par simulation

Pour chaque effet vrai (`0` ou `0.01`) :

1. générer 4000 datasets synthétiques ;
2. pour chacun, appliquer le même estimateur et le même bootstrap par identité que dans l'étude ;
3. produire les cinq réalisations candidate correspondant aux cinq seeds ;
4. calculer les cinq UCB ;
5. compter un succès uniquement si **les cinq** UCB sont `< 0.03`.

Si `R` datasets parmi 4000 satisfont cette intersection :

\[
\widehat{Power}=\frac{R}{4000}.
\]

Le nombre `4000` n'est pas réduit parce que le calcul est long : il fait partie du contrat préenregistré.

---

## 6. Pourquoi les cinq seeds réduisent naturellement la puissance

Supposons, uniquement pour l'intuition, que chaque seed ait individuellement 97 % de chances de passer et qu'ils soient indépendants. La probabilité que les cinq passent serait :

\[
0.97^5 \approx 0.859.
\]

La vraie dépendance n'est pas celle de cinq événements indépendants, mais cet exemple montre le principe : **une règle d'intersection est plus exigeante qu'une règle sur un seul seed**.

Cette exigence est volontaire. Elle répond à une question plus robuste :

> la conclusion de non-infériorité résiste-t-elle à la variabilité de l'entraînement/projection, plutôt que de dépendre d'un seed favorable ?

La simulation de puissance doit donc porter sur l'intersection réelle des cinq seeds.

---

## 7. Le point méthodologique crucial : un même monde raw512

Une première inspection du simulateur a révélé un détail important avant le lancement des lots complets.

Pour un dataset simulé donné, les cinq seeds sont cinq variantes candidates comparées **au même dataset raw512 de référence**.

Il faut donc :

```text
                 ┌─ candidate seed 11
un monde raw512 ─┼─ candidate seed 29
commun           ├─ candidate seed 47
                 ├─ candidate seed 71
                 └─ candidate seed 101
```

et non :

```text
raw monde A → seed 11
raw monde B → seed 29
raw monde C → seed 47
...
```

Sinon, la simulation ajouterait artificiellement cinq réalisations différentes du bruit de référence et ne représenterait plus la comparaison appariée réellement prévue.

Le contrat Study 1B impose désormais explicitement :

- **une réalisation raw/reference commune par dataset simulé** ;
- commune aux cinq method seeds ;
- un résiduel candidate propre à chaque seed.

Un test automatique protège cet invariant.

---

## 8. Variabilité entre seeds

Le préflight représente une variation modeste entre seeds par une perturbation additive sur Δ :

```text
distribution : normale centrée
écart-type   : 0,005
troncature   : [-0,02 ; 0,02]
```

C'est une **hypothèse de planification a priori**, pas un résultat appris sur Study 1B.

Elle doit donc être lue comme :

> « sous ce modèle explicite et gelé de variabilité entre seeds, notre design atteint-il la puissance requise ? »

Si cette hypothèse devait être changée de manière scientifiquement matérielle, cela demanderait un amendement pré-outcome documenté plutôt qu'un ajustement après lecture des résultats.

---

## 9. Ce que signifie un résultat de puissance ≥ 90 %

Si la simulation produit par exemple 92 % pour `Δ=0.01`, cela signifie :

> **dans le monde synthétique spécifié où la vraie dégradation vaut 0,01 et sous les hypothèses du simulateur, environ 92 % des expériences produisent cinq UCB simultanément sous la marge 0,03.**

Cela ne signifie pas :

- que la compression réelle aura 92 % de précision ;
- qu'il y a 92 % de probabilité que Siamese128 soit non inférieur ;
- que `Δ` réel vaut 0,01 ;
- que le résultat futur est connu à l'avance.

La puissance est une propriété du **design sous une hypothèse de monde**, pas une probabilité postérieure sur l'hypothèse scientifique.

---

## 10. Couverture et puissance ensemble

Les deux préflights forment une chaîne logique :

```text
1. La procédure d'incertitude est-elle calibrée ?
   → couverture statistique à vérité connue

2. Avec cette procédure, le design est-il assez informatif ?
   → puissance statistique a priori

3. Seulement si ces instruments sont crédibles :
   → exécuter l'étude scientifique réelle
```

On peut avoir :

| Couverture | Puissance | Interprétation |
|---|---|---|
| mauvaise | peu importe | instrument statistique non crédible |
| bonne | faible | instrument crédible mais étude trop peu informative |
| bonne | suffisante | design statistiquement prêt, sous hypothèses |

Le troisième cas ne prouve toujours pas le résultat scientifique. Il indique que l'expérience a été préparée pour pouvoir fournir une réponse utile.

---

## 11. En français dans le texte

Avant de faire une vraie expérience coûteuse, on vérifie deux choses.

D'abord, est-ce que notre thermomètre mesure correctement ? C'est la **couverture**.

Ensuite, si la différence que nous cherchons existe vraiment, le thermomètre est-il assez précis pour la voir ? C'est la **puissance**.

Un thermomètre correct mais gradué seulement tous les 20 degrés ne permettra pas de distinguer 20 °C de 21 °C. Il est peut-être juste, mais pas assez précis pour la question.

---

## 12. Lecture ingénieur

La puissance est une **analyse de capacité du plan d'essai**, conditionnelle aux hypothèses de génération.

Elle lie :

- effet minimal/scénario d'intérêt ;
- variance des données ;
- structure de dépendance ;
- taille de l'échantillon ;
- estimateur ;
- niveau de confiance ;
- multiplicité des seeds ;
- règle de décision finale.

Changer l'un de ces éléments peut modifier la puissance. C'est pourquoi une analyse a priori doit réutiliser **la règle de décision complète** prévue pour l'expérience, et non un test simplifié fabriqué seulement pour produire un chiffre favorable.

Pour Study 1B, l'objet qualifié est donc le système :

```text
graphe de paires
+ dépendance par identité
+ bootstrap 10 000
+ UCB 97,5 %
+ marge 0,03
+ cinq seeds
+ intersection des cinq décisions
```

---

## 13. Lecture 12 ans

Imagine cinq joueurs qui doivent tous réussir un panier pour que l'équipe gagne.

Tu veux savoir si le jeu est raisonnable avant le vrai match. Tu construis alors 4000 matchs simulés où tu connais exactement la difficulté.

À chaque match, tu regardes si **les cinq joueurs réussissent**. Si l'équipe gagne au moins neuf fois sur dix dans les deux difficultés prévues, le plan est considéré comme assez puissant.

Cela ne dit pas que l'équipe gagnera le vrai match. Cela dit que **les règles du match lui donnent une chance raisonnable de montrer ce qu'elle vaut**.

---

## 14. Réflexe Diderot

Avant de lancer une étude, demander :

1. Quelle conclusion exacte devra être produite ?
2. Quelle taille d'effet est scientifiquement intéressante ?
3. Quelle est la règle complète de succès — multiplicité comprise ?
4. Quelle variabilité des données et des seeds est supposée ?
5. Les comparaisons appariées partagent-elles bien le même monde de référence ?
6. Combien de simulations sont nécessaires pour estimer la puissance ?
7. Quel seuil de puissance est exigé avant les outcomes ?
8. Les hypothèses de puissance ont-elles été gelées avant de lire les résultats réels ?
9. Une puissance suffisante est-elle correctement présentée comme une propriété du design, et non comme une preuve de l'hypothèse ?

---

## 15. Provenance et état Study 1B

Source d'expérience : `gharbonnier78/siamese-embedding-compression-lab`, Study 1B, préflight non-outcome.

Contrat : `protocol/simulations/STUDY1B_COVERAGE_POWER_PREFLIGHT_2026-08-27.yaml`.

Configuration gelée :

```text
4000 datasets pour Δ=0
4000 datasets pour Δ=0,01
5 seeds : 11, 29, 47, 71, 101
10 000 réplications bootstrap par dataset
1 raw/reference commun aux cinq seeds pour chaque dataset
succès = les cinq UCB < 0,03
puissance requise >= 0,90 dans les deux scénarios
```

Le workflow de puissance a été lancé. Cette note **ne préjuge pas de son résultat** et ne sera pas rétroactivement réécrite pour adapter les concepts au verdict obtenu.

Aucun outcome biométrique SCREEN/TEST de Study 1B n'est ouvert par cette simulation.
