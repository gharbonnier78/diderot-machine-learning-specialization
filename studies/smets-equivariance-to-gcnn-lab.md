# Étude à venir — Smets : de la source à un chapitre et un laboratoire G-CNN

## Statut

`STUDY_DESIGN`

Cette étude ne contient encore **aucun résultat expérimental propre à Diderot** sur la supériorité éventuelle d'un G-CNN. Elle documente le chemin déjà parcouru depuis la source primaire et prépare deux sorties distinctes :

1. un **chapitre pédagogique candidat** sur inductive bias, symétries et équivariance ;
2. un **laboratoire expérimental candidat** comparant CNN standard, CNN + augmentation de rotations et G-CNN.

Le dossier doit rester vivant jusqu'à la review des résultats expérimentaux et l'intégration éventuelle dans le livre.

---

## 1. Point de départ : source primaire

### Source

Bart M. N. Smets, *Mathematics of Neural Networks (Lecture Notes Graduate Course)*.

- arXiv : https://arxiv.org/abs/2403.04807
- version analysée : `arXiv:2403.04807v1 [cs.LG]`
- code/notebooks compagnons : https://gitlab.com/bsmetsjr/mathematics_of_neural_networks
- copie locale utilisée : `1786122202337.pdf`
- taille locale : `2,025,085` octets
- SHA-256 local : `4f4900e1c7dfe4036cb01b459ecee2e6fcac042fd79bb4cf54304fc7ae652a75`

La provenance complète est enregistrée dans [`sources/source_manifest.yaml`](../sources/source_manifest.yaml).

Le hash ci-dessus identifie uniquement les octets de la copie locale utilisée ; il n'est pas présenté comme un checksum canonique publié par arXiv.

### Ce que la source apporte effectivement

Smets construit une progression depuis les fondations ML et deep learning vers :

- invariance et équivariance ;
- variétés ;
- groupes de Lie ;
- actions de groupe ;
- espaces homogènes et stabilisateurs ;
- opérateurs linéaires équivariants ;
- Théorème 3.32 ;
- convolution de groupe ;
- lifting de `R^2` vers `SE(2)` ;
- group convolutions ;
- projection de `SE(2)` vers `R^2` ;
- discrétisation des orientations et interpolation ;
- opérateurs tropicaux équivariants ;
- ReLU et max pooling comme cas tropicaux ou tropicalement affines dans le cadre présenté.

### Ce que la source ne suffit pas à établir

Cette source est principalement théorique et pédagogique. Elle ne constitue pas, à elle seule, une étude expérimentale exhaustive démontrant que :

- un G-CNN est toujours meilleur qu'un CNN standard ;
- l'équivariance améliore toujours la généralisation ;
- l'augmentation de données est toujours inférieure à une contrainte architecturale ;
- le coût mémoire/calcul du G-CNN est toujours compensé par un gain prédictif ;
- une symétrie correcte au niveau théorique reste exactement satisfaite après discrétisation numérique.

Ces points doivent rester des **questions expérimentales**.

---

## 2. Première capitalisation : lecture Diderot

La synthèse originale est disponible dans :

[`chat-notes/2026-08-31-smets-mathematics-of-neural-networks.md`](../chat-notes/2026-08-31-smets-mathematics-of-neural-networks.md)

Cette note transforme la lecture en fil pédagogique :

```text
réseau générique
    ↓
inductive bias
    ↓
symétrie connue
    ↓
groupe de transformations
    ↓
action sur les données/représentations
    ↓
opérateur équivariant
    ↓
G-CNN
    ↓
discrétisation
    ↓
équivariance numérique à mesurer
```

La note distingue les affirmations soutenues par Smets des interprétations Diderot et contient des ancres vers les sections, définitions, équations, exemples et théorèmes pertinents de la source.

### Principe Diderot extrait de la lecture

> Ne pas demander au modèle de redécouvrir ce que nous savons déjà avec suffisamment de certitude.

Ce principe est **une interprétation Diderot**, pas un théorème de Smets. Il doit rester accompagné de sa clause inverse :

> Une mauvaise symétrie ou un mauvais inductive bias peut réduire l'espace d'hypothèses de façon incorrecte et dégrader la solution.

---

## 3. Review indépendante déjà réalisée sur la lecture

La lecture a fait l'objet d'une review indépendante, conservée dans :

[`reviews/pr9-smets-independent-review.md`](../reviews/pr9-smets-independent-review.md)

Le verdict était :

`APPROVE WITH NON-BLOCKING COMMENTS`

avec recommandation :

`MERGE AFTER MINOR FIXES`.

Les corrections principales ont été intégrées avant le merge de la PR #9 :

- amélioration des ancres vers la source primaire ;
- clarification de l'attribution concernant weight sharing et équivariance translationnelle ;
- vérification directe de la section tropicale ;
- vérification du hash et de la taille locale ;
- conservation explicite de la distinction continu théorique / discret numérique.

La PR #9 a ensuite été mergée dans `main` avec CI réussie.

### Ce que cette review valide

Elle valide la **qualité de la lecture et de sa traçabilité**.

Elle ne valide pas encore :

- le futur chapitre final ;
- le protocole expérimental détaillé ;
- l'implémentation ;
- les résultats ;
- une conclusion scientifique sur les G-CNN.

Chaque étape doit disposer de son propre niveau de preuve.

---

## 4. Question pédagogique à transformer en chapitre

### Question centrale

Pourquoi un ingénieur ML devrait-il parfois préférer une architecture qui encode explicitement une symétrie à une architecture générique qui apprend depuis les données ?

### Objectif humain du chapitre

À la fin du chapitre, un lecteur connaissant les CNN ordinaires doit pouvoir expliquer, sans mémorisation mécanique :

1. ce qu'est un inductive bias ;
2. la différence entre invariance et équivariance ;
3. pourquoi une symétrie peut être représentée par un groupe agissant sur un espace ;
4. pourquoi les groupes de Lie apparaissent quand les transformations sont continues ;
5. le rôle des espaces homogènes et des stabilisateurs ;
6. comment la convolution ordinaire se relie à la translation ;
7. ce que généralise la convolution de groupe ;
8. pourquoi le lifting vers `SE(2)` ajoute une coordonnée d'orientation ;
9. comment la projection revient vers un espace de sortie plus simple ;
10. pourquoi l'équivariance théorique et l'équivariance numérique ne sont pas identiques ;
11. pourquoi le choix d'une mauvaise symétrie peut nuire au modèle ;
12. quelles affirmations doivent être testées plutôt que supposées.

---

## 5. Plan de chapitre candidat

Titre de travail :

**Des CNN aux réseaux équivariants — encoder les symétries que l'on connaît déjà**

### 5.1 Point de départ : le CNN que le lecteur connaît

- convolution ;
- noyau ;
- weight sharing ;
- structure spatiale ;
- translation ;
- rappel des limites des réseaux fully connected sur image.

Objectif : ne pas commencer par la géométrie abstraite.

### 5.2 Inductive bias

- données seules insuffisantes pour déterminer toute la structure du modèle ;
- choix de loss, architecture et optimisation ;
- inductive bias comme réduction/priorisation de l'espace des fonctions.

### 5.3 Invariance vs équivariance

Inclure les relations :

`F(g·x) = F(x)`

et

`F(g·x) = g·F(x)`.

Donner au moins :

- exemple classification ;
- exemple segmentation ou détection spatiale.

### 5.4 De la transformation au groupe

- composition ;
- identité ;
- inverse ;
- action ;
- pourquoi la structure de groupe est utile pour raisonner sur des familles de transformations.

### 5.5 Pourquoi un groupe de Lie ?

- continuité des rotations/translations ;
- structure différentiable ;
- exemple `SO(2)` puis `SE(2)`.

### 5.6 Espaces homogènes et stabilisateurs

- action transitive ;
- point de référence ;
- stabilisateur ;
- lien avec les contraintes sur les noyaux équivariants.

### 5.7 Théorème 3.32 comme pivot, sans surcharger la preuve

Le chapitre doit expliquer :

- ce que le théorème caractérise ;
- pourquoi un noyau réduit suffit sous les contraintes adéquates ;
- comment la convolution de groupe apparaît comme cas particulier.

Une dérivation détaillée peut aller en annexe ou encadré mathématique.

### 5.8 Architecture `R^2 -> SE(2) -> R^2`

- lifting ;
- position + orientation ;
- group convolution ;
- projection intégrale ;
- projection par maximum ;
- coût de la représentation plus riche.

### 5.9 Discrétisation

- orientations finies ;
- kernels tournés ;
- interpolation ;
- frontières ;
- erreurs numériques ;
- distinction entre propriété prouvée et propriété mesurée.

### 5.10 Métrique d'équivariance

Introduire la quantité expérimentale Diderot :

`epsilon_eq(x,g) = ||F(g·x) - g·F(x)||`.

Préciser que cette métrique est une proposition expérimentale Diderot et non une équation reprise comme telle de Smets.

### 5.11 Data augmentation vs architecture

Ne pas présenter une opposition dogmatique.

Comparer conceptuellement :

- coût des exemples augmentés ;
- propriété apprise vs propriété architecturale ;
- robustesse possible ;
- coût calcul/mémoire ;
- risque de mauvais prior ;
- possibilité de combinaison augmentation + équivariance.

### 5.12 Opérateurs tropicaux

Présenter le message pédagogique central : structure-preserving ne signifie pas nécessairement « linéaire au sens classique ».

### 5.13 Limites

Le chapitre doit contenir explicitement :

- mauvaise symétrie ;
- symétrie seulement approximative ;
- violation aux frontières ;
- interpolation ;
- coût ;
- tâche où l'orientation absolue contient du signal ;
- différence entre géométrie imposée et géométrie émergente.

### 5.14 Transition vers le laboratoire

Terminer par la question :

> L'architecture équivariante produit-elle réellement, dans une expérience contrôlée, une équivariance plus précise, une meilleure efficacité en données ou une meilleure robustesse aux rotations non vues, et à quel coût ?

---

## 6. Critères de passage en `CHAPTER_CANDIDATE`

Le chapitre pourra être créé lorsqu'il existe :

- un plan stable ;
- des notations vérifiées ;
- des ancres vers la source ;
- au moins un exemple numérique ou visuel ;
- une distinction explicite source / Diderot ;
- une section limites ;
- une fiche de révision ;
- un exercice ;
- un lien direct vers le protocole expérimental ;
- une review indépendante de la version chapitre.

Le chapitre ne sera `READY_FOR_BOOK` qu'après satisfaction des critères de `docs/progress.md`.

---

## 7. Question scientifique du laboratoire

### Question principale

Pour une tâche dont la classe cible possède une symétrie rotation-translation réellement pertinente, comment se comparent :

1. un CNN standard ;
2. le même type de CNN avec augmentation de rotations ;
3. un G-CNN explicitement équivariant ?

### Question secondaire essentielle

Quelle part de l'erreur d'équivariance observée vient :

- du réseau ;
- de la discrétisation des orientations ;
- de l'interpolation ;
- des frontières/padding ;
- du sous-échantillonnage/pooling ?

---

## 8. Hypothèses falsifiables

### H1 — Équivariance mesurée

Si l'architecture encode correctement la symétrie et que la discrétisation est suffisamment fine, alors le G-CNN devrait produire une erreur `epsilon_eq` plus faible qu'un CNN standard.

**Réfutation possible :** aucune différence robuste ou G-CNN pire à budget comparable.

### H2 — Efficacité en données

Si la symétrie imposée correspond réellement au problème, le G-CNN peut atteindre une performance comparable avec moins de données d'entraînement.

**Réfutation possible :** avantage nul, instable ou inférieur à une augmentation simple.

### H3 — Robustesse aux rotations non vues

Le G-CNN devrait être moins sensible aux rotations absentes de l'entraînement qu'un CNN standard non augmenté.

**Réfutation possible :** robustesse équivalente ou meilleure pour la baseline.

### H4 — Augmentation vs équivariance

Une augmentation de données suffisamment riche peut réduire ou annuler l'avantage pratique d'un G-CNN, mais potentiellement avec un autre coût en données/calcul.

Cette hypothèse est volontairement non orientée : l'expérience peut montrer que l'augmentation est le meilleur compromis.

### H5 — Coût de discrétisation

Une augmentation du nombre d'orientations devrait réduire une partie de l'erreur d'équivariance jusqu'à un plateau, avec coût mémoire/calcul croissant.

**Réfutation possible :** pas de relation monotone, effet dominé par interpolation/architecture ou coût sans bénéfice.

---

## 9. Choix du problème expérimental

Le problème doit être assez simple pour que la symétrie soit contrôlable et assez riche pour distinguer les architectures.

### Option recommandée pour le premier lab

Classification ou segmentation d'objets 2D avec transformations rotationnelles synthétiques contrôlées.

Le dataset devra permettre de construire explicitement :

- rotations vues à l'entraînement ;
- rotations non vues ;
- éventuellement translations ;
- un régime où la symétrie est vraie ;
- un **contre-régime** où l'orientation absolue devient informative.

Ce dernier point est important : il permet de démontrer expérimentalement qu'un inductive bias peut devenir mauvais.

### Dataset final à choisir

Le choix exact n'est **pas encore figé**. Il doit faire l'objet d'une mini-review avant implémentation selon :

- licence ;
- taille ;
- reproductibilité ;
- contrôle des rotations ;
- temps d'entraînement ;
- simplicité pédagogique ;
- capacité à créer un test négatif.

---

## 10. Baselines et fairness

### Modèle A — CNN standard

Baseline sans augmentation rotationnelle spécifique.

### Modèle B — CNN + augmentation

Même famille de CNN, avec rotations ajoutées pendant l'entraînement.

### Modèle C — G-CNN

Architecture équivariante conçue pour la symétrie choisie.

### Contraintes de comparaison

La comparaison doit contrôler autant que possible :

- même split train/validation/test ;
- même prétraitement hors augmentation étudiée ;
- mêmes critères d'arrêt ;
- budget d'optimisation comparable ;
- recherche d'hyperparamètres comparable ;
- nombre de paramètres reporté ;
- FLOPs ou approximation de coût reportée si faisable ;
- mémoire maximale reportée ;
- temps d'entraînement ;
- temps d'inférence ;
- mêmes seeds pour les répétitions quand applicable.

Une égalité parfaite du nombre de paramètres n'est pas toujours possible ; les différences doivent être documentées plutôt que cachées.

---

## 11. Plan de données et splits

Le protocole devra figer avant entraînement :

- dataset/version ;
- source et licence ;
- seed de split ;
- train/validation/test ;
- rotations présentes dans train ;
- rotations réservées au test ;
- transformations de validation ;
- politique de normalisation ;
- politique de padding/crop.

Le test principal ne doit jamais être utilisé pour choisir les hyperparamètres.

---

## 12. Répétitions et incertitude

Minimum recommandé : plusieurs seeds indépendantes par configuration.

Pour chaque métrique principale, rapporter :

- moyenne ;
- dispersion ;
- intervalle de confiance ou bootstrap si pertinent ;
- points individuels par seed quand lisible.

Un seul run « meilleur » ne doit pas constituer la conclusion.

---

## 13. Métriques

### 13.1 Performance tâche

Selon la tâche :

- accuracy ;
- balanced accuracy ;
- F1 ;
- IoU/Dice si segmentation ;
- calibration si utile.

### 13.2 Erreur d'équivariance

Mesure principale :

`epsilon_eq(x,g) = ||F(g·x) - g·F(x)||`.

La norme et la normalisation doivent être spécifiées.

À mesurer :

- en sortie ;
- éventuellement à plusieurs couches pour comprendre où l'équivariance se dégrade.

### 13.3 Robustesse transformationnelle

Performance par angle ou famille de transformations, pas seulement moyenne globale.

### 13.4 Efficacité en données

Courbe performance vs fraction du dataset : par exemple 10 %, 25 %, 50 %, 100 % si le coût le permet.

### 13.5 Coût

- paramètres ;
- temps entraînement ;
- temps inférence ;
- mémoire ;
- éventuellement FLOPs.

---

## 14. Mesurer l'erreur introduite par l'interpolation

Le reviewer de la lecture a correctement identifié un risque : `epsilon_eq` peut mélanger l'erreur du réseau et l'erreur du mécanisme qui transforme les tenseurs.

Le lab doit donc inclure un contrôle sans réseau complexe :

1. prendre une entrée connue ;
2. appliquer une rotation ;
3. appliquer l'opération inverse ou une transformation analytique connue ;
4. mesurer l'erreur induite par l'interpolation et la grille seules.

On pourra alors distinguer approximativement :

```text
erreur mesurée totale
    = composante transformation/interpolation
    + composante réseau/discrétisation architecturale
    + erreurs numériques résiduelles
```

Cette décomposition n'est pas forcément additive au sens strict ; elle sert d'abord de contrôle expérimental.

---

## 15. Ablations prévues

### A1 — Nombre d'orientations

Comparer plusieurs discrétisations, par exemple 4 / 8 / 16 orientations si l'implémentation le permet.

### A2 — Interpolation

Comparer au moins les choix disponibles pertinents dans la librairie retenue.

### A3 — Augmentation

Comparer plusieurs intensités ou distributions d'augmentation.

### A4 — Volume de données

Sous-échantillons contrôlés du train.

### A5 — Symétrie correcte vs mauvaise symétrie

Créer un régime où l'orientation absolue est informative pour vérifier qu'imposer une invariance/équivariance inappropriée peut nuire.

### A6 — Padding/frontières

Comparer ou au minimum documenter l'effet du padding sur l'équivalence translationnelle/rotationnelle observée.

---

## 16. Résultats négatifs explicitement acceptables

Le lab est scientifiquement utile même si :

- le G-CNN n'améliore pas la performance ;
- l'augmentation suffit ;
- le gain n'apparaît qu'en faible-data ;
- le coût du G-CNN est trop élevé ;
- l'équivariance mesurée reste limitée par l'interpolation ;
- l'avantage disparaît avec certaines rotations ;
- un CNN standard apprend une robustesse similaire ;
- une mauvaise symétrie détériore fortement les résultats.

Ces résultats seraient pédagogiquement précieux car ils empêchent la transformation de l'équivariance en dogme.

---

## 17. Menaces à la validité

À documenter avant conclusion :

- architecture des baselines non comparable ;
- tuning plus poussé d'un modèle ;
- dataset trop simple ;
- dataset trop petit ;
- leakage entre rotations train/test ;
- choix d'angles favorable au G-CNN ;
- erreur d'interpolation confondue avec erreur du réseau ;
- padding ;
- pooling/stride brisant une propriété attendue ;
- seed chanceuse ;
- métrique d'équivariance mal normalisée ;
- symétrie seulement approximative dans la vraie tâche ;
- conclusion généralisée au-delà du régime étudié.

---

## 18. Implémentation envisagée

Arborescence candidate :

```text
notebooks/equivariance/
    00_equivariance_intuition.ipynb
    01_cnn_vs_aug_vs_gcnn.ipynb
    02_equivariance_discretization_ablations.ipynb

src/diderot_ml/equivariance/
    data.py
    transforms.py
    models.py
    metrics.py
    experiments.py

experiments/equivariance/
    configs/
    runs/
    summaries/

tests/
    test_equivariance_metrics.py
    test_rotation_transforms.py
    test_experiment_reproducibility.py
```

L'arborescence exacte pourra évoluer, mais les responsabilités doivent rester séparées entre : données, transformations, modèles, métriques et orchestration expérimentale.

---

## 19. Artefacts attendus du laboratoire

Le lab final doit produire au minimum :

- configuration versionnée ;
- seeds ;
- versions librairies ;
- résultats bruts ou résumés reproductibles ;
- courbe performance vs rotation ;
- courbe `epsilon_eq` vs rotation ;
- courbe performance vs quantité de données ;
- ablation nombre d'orientations ;
- coût temps/mémoire ;
- tableau synthèse multi-seeds ;
- section échecs/limites ;
- conclusion strictement limitée aux conditions testées.

---

## 20. Gates de progression

### Gate G0 — Source tracée — PASS

Preuves : manifeste source + hash local + URLs.

### Gate G1 — Lecture originale — PASS

Preuve : note Diderot Smets.

### Gate G2 — Review de lecture — PASS

Preuve : review indépendante PR #9 + corrections.

### Gate G3 — Dossier d'étude — EN COURS

Ce document constitue le candidat à G3.

Critère de sortie : review indépendante du design, notamment falsifiabilité et fairness.

### Gate G4 — Chapitre candidat — À VENIR

Critère : plan transformé en chapitre avec exemple, exercice, limites, fiche de révision et source anchors.

### Gate G5 — Lab candidat — À VENIR

Critère : dataset, modèles, budgets, métriques, seeds, ablations et critères d'arrêt gelés avant résultats.

### Gate G6 — Implémentation — À VENIR

Critère : code/notebooks/tests exécutables et CI verte.

### Gate G7 — Evidence review — À VENIR

Critère : résultats multi-seeds, incertitude, négatifs, menaces à la validité et reproductibilité relus indépendamment.

### Gate G8 — Ready for book — À VENIR

Critère : chapitre/lab alignés sur les preuves et sur la définition de terminé Diderot.

---

## 21. Review Claude proposée pour ce dossier

Une review indépendante dédiée au **study design** est souhaitable avant d'implémenter le lab.

Le reviewer devra recevoir au minimum :

- cette étude ;
- la note Smets ;
- la review PR #9 ;
- la source primaire ou son lien arXiv ;
- le manifeste source.

### Questions à poser au reviewer

1. Le chemin source -> lecture -> hypothèse -> chapitre -> lab conserve-t-il correctement les niveaux de preuve ?
2. Des affirmations sont-elles encore attribuées à Smets alors qu'elles relèvent de Diderot ou de connaissances externes ?
3. Le plan de chapitre est-il pédagogiquement complet sans devenir un cours de géométrie différentielle disproportionné ?
4. Les hypothèses H1-H5 sont-elles réellement falsifiables ?
5. Les trois modèles sont-ils comparés de façon suffisamment équitable ?
6. Quelles variables confondantes manquent ?
7. `epsilon_eq` est-elle définie assez précisément ?
8. Comment mieux isoler l'erreur d'interpolation ?
9. Le contre-régime « mauvaise symétrie » est-il suffisant pour tester le risque d'inductive bias incorrect ?
10. Quels éléments doivent être gelés avant de voir les résultats ?
11. Quelles conclusions seraient interdites même si le G-CNN gagne ?
12. Le dossier est-il prêt pour séparer un PR chapitre et un PR lab ?

### Verdict attendu

`APPROVE`

ou

`APPROVE WITH NON-BLOCKING COMMENTS`

ou

`REQUEST CHANGES`.

Si la review demande des changements sur le protocole, ceux-ci doivent être appliqués **avant** les runs de comparaison principaux afin d'éviter d'adapter le protocole aux résultats observés.

---

## 22. Séparation recommandée des futurs PR

### PR A — Chapitre pédagogique

Contenu :

- LaTeX du chapitre ;
- figures explicatives originales ;
- exercice ;
- fiche de révision ;
- liens source ;
- éventuellement micro-notebook d'intuition.

Pas de revendication expérimentale non encore mesurée.

### PR B — Infrastructure du lab

Contenu :

- dataset loader ;
- transformations ;
- trois modèles ;
- métriques ;
- configurations ;
- tests ;
- petit smoke run.

Le protocole doit être gelé avant les runs principaux.

### PR C — Résultats expérimentaux

Contenu :

- runs principaux ;
- statistiques ;
- figures ;
- ablations ;
- résultats négatifs ;
- limites ;
- evidence review.

### PR D — Intégration finale au livre

Mettre à jour le chapitre avec les résultats réellement observés et uniquement ceux-ci.

---

## 23. Chemin complet à conserver

```text
Smets arXiv v1
    ↓
source_manifest.yaml
    ↓
chat-notes/2026-08-31-smets-mathematics-of-neural-networks.md
    ↓
review indépendante PR #9
    ↓
corrections + merge PR #9
    ↓
CE DOSSIER : studies/smets-equivariance-to-gcnn-lab.md
    ↓
review Claude du study design
    ↓
PR A : chapitre pédagogique candidat
    ↓
review chapitre
    ↓
PR B : protocole + infrastructure lab
    ↓
freeze du protocole
    ↓
runs principaux multi-seeds
    ↓
PR C : résultats + ablations + evidence review
    ↓
conclusions limitées aux preuves
    ↓
PR D : intégration chapitre/lab dans le livre
    ↓
READY_FOR_BOOK / MERGED
```

Ce chemin est lui-même un artefact pédagogique : il montre comment Diderot passe d'une source intéressante à une connaissance expliquée, puis d'une hypothèse à une preuve expérimentale, sans confondre les étapes.