# Tester une exigence comme une hypothèse — vers une lecture statistique de la qualification

**Date :** 2026-09-04  
**Statut :** draft pédagogique, à relire humainement avant promotion.  
**Contexte d'apparition :** aparté dérivé de Study 1B, après l'introduction de la puissance statistique et des erreurs de type I / II, appliqué à la question plus générale du Test / IVVQ / qualification.  
**Autorité scientifique de cette note :** aucune. Cette note propose une synthèse pédagogique et une grille d'ingénierie ; elle ne remplace ni les exigences du projet, ni les standards applicables, ni les sources statistiques.

## 1. L'idée centrale

Une activité de Test / IVVQ peut souvent être vue comme une **décision sous incertitude portant sur une affirmation**.

Un cahier des charges contient des exigences, mais beaucoup d'entre elles peuvent être reformulées comme des affirmations à démontrer :

- « le temps de réponse reste sous une limite donnée » ;
- « le système soutient un débit minimal » ;
- « le taux d'erreur biométrique reste sous un seuil » ;
- « la nouvelle version n'est pas moins bonne que l'ancienne de plus d'une marge acceptable » ;
- « le système récupère d'une panne sans perte de transaction » ;
- « la disponibilité reste au-dessus d'une cible donnée ».

La statistique n'est pas nécessaire pour toutes les exigences. En revanche, dès que les observations sont variables, bruitées, rares, dépendantes ou coûteuses, elle peut aider à distinguer :

1. ce que les mesures montrent réellement ;
2. ce que l'on peut conclure ;
3. le risque de prendre la mauvaise décision ;
4. la quantité d'évidence nécessaire avant de décider.

---

## 2. Du requirement au claim testable

Exemple d'exigence :

> Au moins 95 % des transactions doivent terminer en moins de 300 ms dans les conditions définies.

Une formulation mathématique possible est :

`P(T <= 300 ms) >= 0.95`.

Pour en faire un test statistique, il faut ensuite choisir explicitement ce que l'on considère par défaut et ce que l'on veut démontrer.

Par exemple :

`H0 : P(T <= 300 ms) < 0.95`  
`H1 : P(T <= 300 ms) >= 0.95`

Cette formulation n'est pas automatique : elle dépend de l'objet à qualifier, de la métrique, de la marge acceptable et du type de risque que l'on veut contrôler.

Le point pédagogique important est :

> **Écrire H0 et H1 force à expliciter ce que signifie PASS et ce que signifie FAIL.**

---

## 3. Erreur de type I et erreur de type II comme erreurs de décision de qualification

Dans une lecture d'ingénierie :

| Réalité | Décision de qualification | Risque |
|---|---|---|
| système non conforme | PASS | erreur de type I dans une formulation où le PASS exige de rejeter H0 |
| système conforme | FAIL / NOT DEMONSTRATED | erreur de type II |
| système non conforme | FAIL | décision correcte |
| système conforme | PASS | décision correcte |

### Type I — faux PASS

La probabilité d'erreur de type I est notée `alpha`.

Dans la formulation précédente, elle correspond à :

> **déclarer conforme un système qui ne satisfait pas réellement le claim testé.**

Selon le domaine, le coût peut être majeur :

- défaut mis en production ;
- performance insuffisante ;
- perte de disponibilité ;
- sécurité insuffisante ;
- non-conformité contractuelle ;
- décision de release erronée.

### Type II — faux FAIL / qualification manquée

La probabilité d'erreur de type II est notée `beta`.

Elle correspond à :

> **ne pas réussir à démontrer un claim qui est pourtant vrai dans la réalité.**

Conséquences possibles :

- rejet d'une solution correcte ;
- rework inutile ;
- retard de release ;
- surdimensionnement du système ;
- campagne d'essais répétée inutilement.

Le sens métier exact dépend toujours de la formulation de `H0` et `H1`. Il faut donc éviter de mémoriser `type I = faux positif` sans contexte.

---

## 4. La puissance statistique comme qualification du moyen de preuve

La puissance vaut :

`Power = 1 - beta`.

En langage Test Authority :

> **Si le système mérite réellement le PASS pour une situation donnée, quelle est la capacité de notre dispositif d'essai à le démontrer ?**

La puissance devient donc une propriété du **moyen de preuve** :

- taille et structure de l'échantillon ;
- variabilité des observations ;
- dépendances entre observations ;
- marge entre la réalité et la limite ;
- règle de décision ;
- niveau de confiance ;
- qualité du banc et de la mesure.

Une campagne peut donc être parfaitement exécutée et malgré tout être **trop peu discriminante pour répondre à la question**.

C'est exactement ce que Study 1B a montré : avant d'ouvrir les performances réelles, le préflight a révélé que la règle de décision pouvait produire trop de `NOT DEMONSTRATED` dans une situation pourtant réellement acceptable.

---

## 5. Une reformulation utile pour le Test / IVVQ

Au lieu de demander uniquement :

> Combien de tests faut-il exécuter ?

on peut demander :

> **Combien d'évidence faut-il pour pouvoir distinguer, avec un risque connu, une situation acceptable d'une situation inacceptable ?**

Cela peut aider à dimensionner :

- durée d'un soak test ;
- nombre de transactions ;
- nombre d'utilisateurs ;
- nombre d'identités ou de comparaisons biométriques ;
- nombre de cycles de failover ;
- nombre de devices ;
- nombre de répétitions ;
- nombre d'environnements ou de configurations.

La réponse ne vient pas d'une règle universelle « 100 tests suffisent ». Elle dépend de l'effet que l'on veut pouvoir détecter et du risque de décision acceptable.

---

## 6. Toutes les exigences ne demandent pas un test statistique

Il faut distinguer les exigences essentiellement **déterministes** des exigences **stochastiques / variables**.

### Exigence plutôt déterministe

> Un utilisateur non autorisé reçoit une réponse HTTP 403 pour cette opération.

Si les préconditions et le comportement sont déterministes, un test fonctionnel représentatif peut suffire à établir la conformité de cette règle.

### Exigence naturellement statistique ou probabiliste

Exemples :

- latence ;
- débit ;
- disponibilité ;
- taux d'erreur ;
- fiabilité ;
- performance ML ;
- consommation variable ;
- robustesse au bruit ;
- performance sous charge ;
- comportement rare ou extrême.

Dans ces cas, une observation unique ou un simple PASS/FAIL ne décrit souvent pas suffisamment l'incertitude.

---

## 7. Choisir la bonne question statistique

Une difficulté majeure en qualification consiste à poser **la bonne question**.

### Différence / supériorité

> La nouvelle version est-elle meilleure que l'ancienne ?

### Non-infériorité

> La nouvelle version n'est-elle pas dégradée de plus d'une marge acceptable `delta` ?

Très utile pour :

- migration ;
- optimisation ;
- compression ;
- changement d'infrastructure ;
- remplacement de composant ;
- changement de fournisseur.

### Équivalence

> Les deux solutions sont-elles suffisamment proches dans une bande acceptable ?

### Erreur fréquente

> « Je n'ai pas détecté de différence significative, donc les deux systèmes sont équivalents. »

C'est faux.

**Absence de preuve de différence n'est pas preuve d'équivalence.**

Une étude d'équivalence ou de non-infériorité doit être construite pour cette question précise.

---

## 8. De l'intervalle de confiance à la décision

Une bonne campagne ne devrait pas seulement produire une valeur centrale.

Exemple :

`p95 latency = 284 ms`

Cette valeur seule ne dit pas à quel point elle est stable ou incertaine.

Une décision plus robuste peut utiliser une borne :

> même la borne supérieure plausible reste sous la limite de 300 ms.

La logique devient alors :

```text
mesures
  -> estimateur
  -> incertitude
  -> règle de décision
  -> PASS / FAIL / NOT DEMONSTRATED
```

Cette séparation est importante : `NOT DEMONSTRATED` n'est pas nécessairement synonyme de non-conformité réelle ; cela peut aussi signifier que l'évidence collectée est insuffisante.

---

## 9. Risque statistique et risque métier

Les erreurs de type I et II n'ont généralement pas le même coût.

On peut écrire une représentation simplifiée :

`Expected loss = C_I * P(Type I) + C_II * P(Type II)`

où :

- `C_I` = coût d'un faux PASS ;
- `C_II` = coût d'un faux FAIL.

Cette expression n'est pas une prescription universelle. Elle sert à rappeler que choisir `alpha = 0.05` ou `power = 0.90` uniquement par habitude peut être insuffisant.

Le niveau de prudence devrait être cohérent avec :

- la criticité ;
- l'impact d'un défaut échappé ;
- le coût du retard ;
- la réversibilité de la décision ;
- l'existence de monitoring / rollback ;
- l'environnement opérationnel.

---

## 10. Une grille possible pour la Test Authority

Pour une exigence quantitative importante, la qualification pourrait rendre explicitement visibles :

```text
CLAIM
  Ce que l'on veut démontrer.

EVIDENCE
  Mesures, données, environnement, représentativité.

DECISION RULE
  Comment les mesures conduisent à PASS / FAIL / NOT DEMONSTRATED.

TYPE-I RISK
  Risque de faux PASS.

TYPE-II RISK
  Risque de faux FAIL.

POWER
  Capacité du plan expérimental à démontrer un claim réellement satisfait.

RESIDUAL UNCERTAINTY
  Ce que l'expérience ne permet toujours pas d'affirmer.
```

Exemple :

```text
Claim:
  p95 latency <= 300 ms

Evidence:
  50 000 transactions
  environnement représentatif
  distribution de charge définie

Decision rule:
  borne supérieure de l'estimation p95 < 300 ms

Type-I risk:
  accepter une solution réellement au-dessus de 300 ms

Type-II risk:
  rejeter une solution réellement sous 300 ms

Power target:
  >= 0.90 pour une dégradation d'intérêt pré-définie

Residual uncertainty:
  extrapolation vers d'autres profils de charge non démontrée
```

Les nombres de cet exemple sont illustratifs ; ils doivent être dimensionnés par le contexte réel.

---

## 11. Autres outils statistiques potentiellement utiles à l'IVVQ

Cette note ne les développe pas encore complètement, mais ils constituent des prolongements naturels à étudier séparément :

### Tests séquentiels

Accumuler de l'évidence jusqu'à un critère de décision pré-déclaré, au lieu de choisir arbitrairement un nombre fixe d'exécutions.

### Multiplicité

Quand une campagne examine des centaines de métriques, endpoints ou exigences, le risque global de fausses découvertes peut augmenter. Les corrections de tests multiples permettent de contrôler ce phénomène.

### Fiabilité / analyse de survie

Pour durée de vie, taux de panne, temps avant défaut, disponibilité ou événements rares.

### Statistical Process Control

Pour distinguer une dérive réelle du bruit normal d'un processus au fil du temps.

### Design of Experiments

Pour choisir les combinaisons de facteurs qui apportent le plus d'information plutôt que tester toutes les combinaisons de façon uniforme.

### Measurement System Analysis

Avant de qualifier le produit, vérifier que le moyen de mesure lui-même est suffisamment fiable pour distinguer les différences d'intérêt.

### Approches bayésiennes

Pour combiner explicitement connaissance antérieure et nouvelles observations lorsque le cadre scientifique et réglementaire le permet.

Ces extensions nécessitent chacune leur propre source, hypothèses et limites ; elles ne sont pas introduites ici comme des prescriptions automatiques.

---

## 12. Vérification / validation dans la perspective systèmes

Le NASA Systems Engineering Handbook rappelle que la vérification est reliée au jeu d'exigences approuvé, tandis que la validation se rapporte à l'usage attendu / ConOps et aux attentes de la mission ou du client.

Il recommande également de définir dès le développement des exigences comment celles-ci seront vérifiées, notamment via une matrice de vérification des exigences.

La synthèse proposée ici ajoute une lecture statistique à ce cadre :

> lorsqu'une exigence est quantitative et son observation incertaine, la méthode de vérification devrait aussi préciser **le risque de décision et la capacité du plan à discriminer les situations pertinentes**.

Cette phrase est une interprétation Diderot / ingénierie ; elle n'est pas présentée comme une citation ou une exigence NASA.

---

## 13. Connexion avec Evidence → Decision

Une activité de test n'est pas seulement une exécution de scénarios.

Elle construit une chaîne :

```text
Requirement / Claim
        ↓
Test design
        ↓
Measurement system
        ↓
Observed evidence
        ↓
Uncertainty model
        ↓
Decision rule
        ↓
Decision
        ↓
Residual uncertainty
```

Une Test Authority peut donc poser une question supplémentaire :

> **Avons-nous qualifié le système, ou seulement exécuté un test ?**

Et une autre encore :

> **Avons-nous vérifié que notre moyen de preuve était capable de distinguer les situations que la décision doit séparer ?**

C'est le lien direct avec la puissance statistique.

---

## 14. Misconceptions

**Faux :** « Une exigence a passé 100 fois, donc elle est démontrée. »  
**Correction :** cela dépend de la structure de l'échantillon, de la variabilité, de la fréquence de l'événement et du claim exact.

**Faux :** « 0 défaut observé signifie risque nul. »  
**Correction :** zéro événement observé dans un échantillon fini n'implique pas une probabilité réelle nulle.

**Faux :** « Un test à 95 % de confiance est automatiquement bien dimensionné. »  
**Correction :** le contrôle du faux PASS ne garantit pas une puissance suffisante pour éviter les faux FAIL.

**Faux :** « Pas de différence significative = équivalence. »  
**Correction :** une étude d'équivalence ou de non-infériorité doit être conçue explicitement pour cette question.

**Faux :** « Plus de tests signifie toujours plus d'information indépendante. »  
**Correction :** répéter des observations fortement dépendantes ou dupliquer des scénarios peut ajouter peu d'information réelle.

---

## 15. Understanding gate

Avant de considérer cette note assimilée, être capable d'expliquer sans formule :

1. pourquoi une exigence quantitative peut être reformulée comme un claim ;
2. la différence métier entre faux PASS et faux FAIL ;
3. pourquoi la puissance qualifie aussi le plan d'essai, pas seulement le système ;
4. pourquoi `NOT DEMONSTRATED` et `NON CONFORME` ne sont pas toujours synonymes ;
5. pourquoi absence de différence ne prouve pas l'équivalence ;
6. pourquoi la quantité d'information indépendante compte plus que le simple nombre de tests.

Puis être capable de proposer pour une exigence réelle :

- `H0` ;
- `H1` ;
- le risque de type I ;
- le risque de type II ;
- la différence minimale d'intérêt ;
- la quantité d'évidence nécessaire ou la méthode pour la dimensionner.

---

## 16. Sources et provenance

### Statistique — source de référence

NIST/SEMATECH e-Handbook of Statistical Methods :

- https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm
- https://www.itl.nist.gov/div898/handbook/prc/section1/prc131.htm

Ces pages définissent notamment `H0`, `Ha`, le niveau de significativité `alpha`, l'erreur de type I, l'erreur de type II `beta`, la puissance `1-beta`, les régions critiques et les p-values.

### Systems Engineering / V&V

NASA Systems Engineering Handbook :

- https://www.nasa.gov/reference/system-engineering-handbook-appendix/
- https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf

Le handbook décrit notamment la matrice de vérification des exigences, les méthodes de vérification/validation, la qualification et la distinction entre verification testing et validation testing.

### Encounter de recherche ayant déclenché cet aparté

`gharbonnier78/siamese-embedding-compression-lab`, Study 1B :

- préflight de puissance ;
- analyses S1/S2 ;
- S3 information sensitivity ;
- reframe S4 / S4NEW.

La leçon transférée n'est pas « tout test doit devenir statistique », mais :

> **lorsqu'une décision de qualification dépend de mesures incertaines, il est utile de qualifier aussi le dispositif de décision : risque de faux PASS, risque de faux FAIL, puissance, représentativité et incertitude résiduelle.**

---

## 17. Statut pédagogique

Cette note est une **synthèse Diderot draft**.

Elle ne change aucun protocole Study 1B, aucun gate scientifique, aucune règle Test Authority et aucun standard d'entreprise.

Elle fournit un pont pédagogique entre :

- tests d'hypothèses ;
- puissance statistique ;
- non-infériorité / équivalence ;
- IVVQ ;
- qualification ;
- Evidence → Decision.

La suite naturelle est une étude transverse séparée :

`Hypothesis testing as an engineering qualification framework`.
