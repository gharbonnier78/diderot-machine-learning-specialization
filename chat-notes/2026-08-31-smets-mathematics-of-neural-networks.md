# Lecture Diderot — *Mathematics of Neural Networks* (Bart M. N. Smets)

## Statut de cette note

Cette entrée capitalise une **source publique académique/pédagogique** dans Diderot ML. Elle ne transforme pas encore la source en chapitre final du livre : elle sert de pont documenté entre les fondations de la Machine Learning Specialization et le fil transverse `géométrie -> symétries -> inductive bias -> architectures équivariantes`.

La synthèse ci-dessous est une reformulation originale. Les affirmations attribuées au document sont distinguées des interprétations Diderot.

---

## 1. Source et traçabilité

- **Titre** : *Mathematics of Neural Networks (Lecture Notes Graduate Course)*
- **Auteur** : Bart M. N. Smets
- **Date indiquée dans le document** : 12 novembre 2022
- **Dépôt arXiv** : 6 mars 2024, `arXiv:2403.04807v1 [cs.LG]`
- **Source canonique** : https://arxiv.org/abs/2403.04807
- **PDF canonique** : https://arxiv.org/pdf/2403.04807
- **Code / notebooks compagnons** : https://gitlab.com/bsmetsjr/mathematics_of_neural_networks
- **Copie locale analysée** : `1786122202337.pdf`
- **Taille de la copie locale** : `2,025,085` octets
- **SHA-256 de la copie locale** : `4f4900e1c7dfe4036cb01b459ecee2e6fcac042fd79bb4cf54304fc7ae652a75`

> Important : l'empreinte ci-dessus porte sur **les octets exacts de la copie locale fournie**. L'identité `arXiv:2403.04807v1` est présente dans le document et correspond à la notice arXiv, mais cette note ne prétend pas que le SHA-256 ci-dessus est un hash canonique publié par arXiv.

---

## 2. Pourquoi cette source est importante pour Diderot ML

Le document a une forme particulièrement utile pour notre parcours : il commence avec le langage standard du machine learning — apprentissage supervisé, neurones, fonctions d'activation, SGD, entraînement, réseaux profonds, initialisation, CNN, backpropagation et Adam — puis change progressivement de point de vue.

La question n'est plus seulement :

> « quelle architecture peut approximer la fonction que je cherche ? »

mais :

> « quelles transformations du problème sont déjà connues, et comment les imposer à l'architecture plutôt que demander aux données de les réapprendre ? »

C'est précisément le passage d'un modèle générique à un modèle muni d'un **inductive bias structurel**.

Le document formule d'ailleurs l'inductive bias dès le chapitre 1 comme l'ensemble des hypothèses nécessaires pour choisir le modèle, la loss et la manière d'optimiser alors que ces choix ne sont pas eux-mêmes déterminés par les données. Le chapitre 3 donne ensuite une incarnation mathématique très concrète de cette idée : **encoder une symétrie de groupe dans l'opérateur lui-même**.

Pour Diderot, c'est un pivot pédagogique majeur :

```text
apprendre une fonction
        ↓
choisir une architecture
        ↓
identifier les régularités connues du problème
        ↓
exprimer ces régularités comme transformations
        ↓
reconnaître une structure de groupe
        ↓
construire des opérateurs compatibles avec cette action
        ↓
réduire l'espace de fonctions que le réseau doit explorer
```

---

## 3. Carte du document

### Partie A — Fondations ML

Le chapitre 1 reconstruit l'apprentissage supervisé comme approximation d'une fonction inconnue

\[
f : X \to Y
\]

à partir d'un jeu fini de couples \((x_i,y_i)\). Le modèle est paramétré par des poids \(w\), la loss mesure l'écart entre prédiction et cible, puis l'entraînement cherche un paramètre minimisant la loss empirique.

Le texte relie ensuite ce point de vue à la théorie statistique de l'apprentissage : risque de population, risque empirique, régularisation et différence entre performance observée sur l'échantillon et objectif réel de généralisation.

### Partie B — Deep learning comme calcul différentiable

Le chapitre 2 traite notamment :

- réseaux feed-forward ;
- vanishing/exploding gradients ;
- initialisations de type Xavier ;
- CNN ;
- différentiation automatique et graphe de calcul ;
- Adagrad, RMSProp et Adam.

Un détail pédagogiquement intéressant est que Smets ne cache pas la fragilité de certaines justifications heuristiques. Après avoir dérivé des règles d'initialisation sous plusieurs hypothèses simplificatrices, il souligne que certaines sont fausses dans les réseaux réels, tout en observant que ces règles restent utiles en pratique. C'est une bonne illustration de la différence entre **preuve**, **approximation**, **heuristique** et **validation empirique**.

### Partie C — Géométrie et équivariance

Le chapitre 3 constitue la contribution la plus distinctive du cours :

1. variétés ;
2. groupes de Lie ;
3. actions de groupes ;
4. applications/opérateurs équivariants ;
5. espaces homogènes ;
6. opérateurs linéaires équivariants ;
7. construction d'un CNN équivariant rotation-translation ;
8. discrétisation ;
9. opérateurs tropicaux et semi-anneaux.

---

## 4. Invariance et équivariance : le concept à retenir

Le document distingue utilement deux idées.

### Invariance

Une transformation de l'entrée ne change pas la sortie :

\[
F(g\cdot x)=F(x).
\]

Exemple intuitif : pour une tâche de classification, tourner un objet peut ne pas changer sa classe.

### Équivariance

La sortie se transforme de manière cohérente avec l'entrée :

\[
F(g\cdot x)=g\cdot F(x).
\]

Exemple intuitif : si une image d'entrée est tournée, une carte de segmentation doit tourner de la même manière.

L'équation centrale est donc la commutation :

\[
F\circ \rho_X(g)=\rho_Y(g)\circ F.
\]

Autrement dit, deux chemins conduisent au même résultat :

```text
x --transformation g--> g·x
|                       |
F                       F
|                       |
v                       v
F(x) --transformation--> g·F(x)
```

Ce diagramme est plus important que la notation : il dit que le réseau **respecte une loi de transformation connue**.

---

## 5. Pourquoi ne pas simplement faire de la data augmentation ?

Smets donne l'intuition dès l'ouverture du chapitre 3 : on pourrait ajouter de nombreuses versions translatées, tournées ou redimensionnées des exemples et espérer que le réseau apprenne la symétrie. Mais cela augmente fortement le volume d'entraînement et ne garantit pas que la propriété soit réellement encodée.

L'alternative est architecturale : construire une famille d'opérateurs pour laquelle la propriété est vraie par construction.

### Lecture Diderot

C'est une forme très pure de ce principe :

> **ne pas demander au modèle de redécouvrir ce que nous savons déjà avec suffisamment de certitude.**

Mais il faut ajouter immédiatement la clause inverse :

> **n'imposer une symétrie que si elle est réellement pertinente pour le phénomène et la décision.**

Un mauvais inductive bias ne réduit pas seulement l'espace de recherche : il peut exclure la solution correcte.

---

## 6. Le chemin mathématique : variété -> groupe de Lie -> action -> espace homogène

### 6.1 Variété

Une variété permet de travailler sur un espace qui peut être globalement non euclidien mais localement décrit par des coordonnées euclidiennes. Le cours introduit ce langage parce que les transformations continues intéressantes vivent naturellement sur de tels objets.

L'idée à retenir n'est pas « une variété est une surface courbe » mais plutôt :

> un espace dont la structure locale permet le calcul différentiel, même si sa structure globale n'est pas celle de \(\mathbb{R}^n\).

### 6.2 Groupe de Lie

Un groupe de Lie combine :

- une structure de groupe — composer et inverser des transformations ;
- une structure différentielle — les transformations varient continûment.

Pour les images planes, le groupe central du chapitre est

\[
SE(2)=\mathbb{R}^2\rtimes SO(2),
\]

qui représente translations et rotations du plan.

### 6.3 Action de groupe

Le groupe abstrait devient utile lorsqu'il **agit** sur les données. Une action dit comment une transformation \(g\in G\) déplace un point, une image ou une représentation.

Cette étape est conceptuellement essentielle : connaître un groupe ne suffit pas. Il faut préciser **sur quoi et comment il agit**.

### 6.4 Espace homogène et stabilisateur

Un espace homogène est un espace sur lequel le groupe agit transitivement : deux points quelconques peuvent être reliés par une transformation du groupe.

Le stabilisateur d'un point \(x\) est le sous-groupe des transformations qui le laissent inchangé.

Ces deux objets deviennent ensuite un mécanisme de conception : les contraintes imposées au noyau d'un opérateur équivariant sont reliées au stabilisateur.

---

## 7. Le résultat structurel : caractériser les opérateurs linéaires équivariants

Le théorème 3.32 est le cœur mathématique du passage vers les G-CNN. Il donne une représentation d'opérateurs linéaires équivariants à partir d'un noyau dont la forme est contrainte par l'action du groupe et le stabilisateur.

Dans le cas où domaine et codomaine sont le groupe lui-même, on retrouve la convolution de groupe.

Cette lecture généralise une idée déjà cachée dans les CNN ordinaires :

- un CNN standard partage les mêmes poids à travers les translations ;
- cette structure lui donne une équivariance naturelle à la translation ;
- un G-CNN remplace la translation seule par une action de groupe plus générale.

Le poids partagé n'est donc pas seulement une astuce de compression de paramètres. Il est l'expression algorithmique d'une symétrie.

---

## 8. L'architecture SE(2) : lifting -> group convolution -> projection

Le cours propose une construction concrète d'un CNN équivariant aux rotations et translations.

### Étape 1 — Lifting

On part d'une image sur \(\mathbb{R}^2\) et on la transforme en une représentation définie sur \(SE(2)\).

Intuitivement, au lieu de mémoriser seulement :

```text
position (x,y)
```

la représentation porte aussi une orientation :

```text
position (x,y) + orientation θ
```

Le coût est une représentation de dimension supérieure, mais le gain est que l'orientation devient une coordonnée explicite sur laquelle le groupe agit naturellement.

### Étape 2 — Group convolutions

Une fois dans l'espace du groupe, on empile des convolutions de groupe. Elles transportent l'information tout en préservant l'équivariance.

### Étape 3 — Projection

La sortie finale n'a pas nécessairement besoin de vivre sur \(SE(2)\). Pour revenir vers \(\mathbb{R}^2\), le cours décrit notamment l'intégration sur l'axe des orientations :

\[
(Pf)(x)=\int_0^{2\pi}f(x,\theta)\,d\theta.
\]

Le maximum sur l'orientation constitue une autre opération équivariante, cette fois non linéaire.

### Résumé mental

```text
image 2D
  ↓ lifting
carte position × orientation
  ↓ group convolution
représentation équivariante sur SE(2)
  ↓ projection
sortie 2D cohérente avec rotation + translation
```

---

## 9. Discrétisation : là où la théorie rencontre la machine

Le chapitre développe d'abord le cadre dans un espace continu, puis ne discrétise qu'au moment de l'implémentation.

Pour le cas SE(2), Smets indique comme ordre de grandeur pratique :

- kernels de lifting typiquement `5x5` à `7x7` ;
- environ `8` orientations discrètes ;
- group convolutions typiquement `5x5x5` ;
- interpolation linéaire pour échantillonner les kernels tournés hors grille.

Il insiste sur un compromis : augmenter le nombre d'orientations ou la taille des kernels coûte vite en mémoire et en calcul, pour un gain de performance qui n'est pas proportionnel.

### Point critique Diderot

L'équivariance exacte appartient au modèle mathématique continu. Une implémentation numérique introduit :

- échantillonnage ;
- grille finie ;
- interpolation ;
- nombre fini d'orientations ;
- erreurs numériques.

Il faut donc distinguer :

```text
équivariance théorique
        ≠
équivariance numérique mesurée
```

Cela suggère immédiatement une métrique expérimentale :

\[
\varepsilon_{eq}(x,g)
=
\|F(g\cdot x)-g\cdot F(x)\|.
\]

Un futur lab Diderot devrait mesurer cette erreur en fonction du nombre d'orientations et de la méthode d'interpolation.

---

## 10. Le détour tropical est loin d'être anecdotique

La dernière section élargit encore le cadre. Au lieu de considérer « linéaire » et « non linéaire » comme une opposition absolue, le cours demande : peut-on remplacer l'algèbre usuelle \((+,\times)\) par une autre structure ?

Il introduit les semi-anneaux puis le semi-anneau tropical, où des opérations de type `max` et `+` jouent le rôle d'addition et de multiplication.

Le résultat pédagogique remarquable est que des opérations très familières des réseaux — notamment **ReLU** et **max pooling** — peuvent être replacées dans un cadre d'opérateurs tropicaux ou tropiquement affines.

Le chapitre construit ensuite des opérateurs tropicaux équivariants, analogues non classiques des opérateurs intégrals linéaires.

### Pourquoi c'est important

Le message profond n'est pas seulement « il existe une jolie interprétation algébrique de max pooling ».

Il est plutôt :

> **la préservation de structure ne s'arrête pas aux couches linéaires.**

Cela ouvre la porte à un design où l'on raisonne sur l'algèbre de l'opérateur lui-même, pas seulement sur la topologie du réseau.

---

## 11. Ce que cette source change dans notre modèle mental du deep learning

### Avant

On peut voir un réseau comme une grande famille paramétrique capable d'approximer une fonction, puis compter sur les données et l'optimisation pour trouver une solution utile.

### Après

On peut séparer explicitement trois niveaux :

1. **ce que nous savons avant les données** : symétries, conservation, causalité, géométrie, contraintes ;
2. **ce que nous laissons apprendre** : paramètres, résidus, inconnues structurelles ;
3. **ce que nous devons vérifier expérimentalement** : que l'inductive bias choisi améliore réellement généralisation, efficacité et robustesse dans le régime visé.

Cette séparation rejoint un principe général Diderot :

```text
structure connue
      +
incertitude restante
      +
données
      +
expérience falsifiable
      =
modèle d'ingénierie plus crédible
```

---

## 12. Connexions transverses Diderot

### Traitement du signal et filtrage

Le passage `signal -> opérateur -> symétrie -> convolution` relie directement cette source au traitement du signal. Un filtre n'est plus seulement vu comme un calcul local : sa forme peut être dérivée de propriétés d'invariance/équivariance.

### Géométrie de Lie et estimation

Cette source traite surtout l'action de groupes pour construire des réseaux. Elle est complémentaire — mais non identique — aux travaux sur le filtrage d'états vivant directement sur des groupes de Lie ou des variétés riemanniennes. Dans un cas, la géométrie contraint **l'architecture d'apprentissage** ; dans l'autre, elle contraint **l'espace de l'état estimé et sa dynamique**.

Il faudra préserver cette distinction dans Diderot.

### Représentations et embeddings

Un embedding appris peut présenter une géométrie émergente sans qu'elle ait été imposée. Ici, au contraire, la symétrie est spécifiée a priori au niveau de l'architecture. Ces deux situations ne doivent pas être confondues :

```text
géométrie observée a posteriori
vs
géométrie imposée a priori
```

Leur comparaison est une piste expérimentale intéressante.

### Physics-informed / structure-preserving ML

Le cadre des G-CNN illustre une famille plus générale de stratégies : incorporer dans le modèle les propriétés déjà connues du système plutôt que laisser un modèle universel les apprendre de zéro.

Ce principe peut prendre différentes formes : symétries, lois de conservation, structure hamiltonienne, contraintes de positivité, topologie, causalité, etc. La présente source documente solidement **le cas des symétries de groupe**, pas l'ensemble de ces extensions.

---

## 13. Limites et prudences

### 13.1 Ce sont des notes de cours

Le document est un support de cours de niveau graduate, pas une étude expérimentale comparative exhaustive. Sa valeur première est pédagogique et théorique.

### 13.2 Le chapitre 3 est centré sur les CNN et les symétries géométriques

Il ne constitue pas une théorie générale de tous les réseaux modernes. Il ne faut pas extrapoler directement ses conclusions à toutes les architectures, notamment aux grands Transformers ou aux modèles de monde.

### 13.3 Une symétrie imposée peut être fausse

L'équivariance est bénéfique seulement si la transformation choisie correspond réellement à une régularité de la tâche. Si l'orientation absolue contient de l'information, imposer une invariance complète à la rotation peut détruire un signal utile.

### 13.4 Continu et discret doivent être séparés

Le cadre continu facilite les preuves. L'implémentation discrète introduit une approximation. Une architecture dite « équivariante » doit donc être évaluée numériquement et pas seulement nommée ainsi.

### 13.5 Inductive bias n'est pas preuve de généralisation

Réduire l'espace d'hypothèses peut améliorer l'efficacité statistique, mais la source ne démontre pas que toute architecture équivariante sera meilleure dans toute situation. Cela reste une hypothèse à tester pour le problème considéré.

---

## 14. Expérience Diderot proposée

### Question

Une contrainte d'équivariante rotation-translation apporte-t-elle une propriété mesurable qu'un CNN standard ne possède pas intrinsèquement ?

### Protocole minimal

Comparer :

1. CNN standard ;
2. CNN standard + augmentation par rotations ;
3. G-CNN équivariant.

Mesurer séparément :

- performance prédictive ;
- quantité de données nécessaire ;
- nombre de paramètres ;
- coût calcul/mémoire ;
- erreur d'équivariante \(\varepsilon_{eq}\) ;
- robustesse sur rotations non vues à l'entraînement.

Puis faire une ablation sur :

- nombre d'orientations discrètes ;
- interpolation ;
- quantité de data augmentation.

### Hypothèse falsifiable

> Si la tâche possède réellement la symétrie choisie, alors une architecture qui l'encode devrait atteindre une erreur d'équivariante plus faible et potentiellement une meilleure efficacité en données qu'un CNN standard, à budget comparable.

Le mot **potentiellement** est volontaire : l'expérience doit pouvoir réfuter l'hypothèse.

---

## 15. Fiche de révision

**Inductive bias** — hypothèses structurelles introduites avant l'observation complète des données.

**Invariance** — \(F(gx)=F(x)\).

**Équivariance** — \(F(gx)=gF(x)\).

**Groupe de Lie** — groupe muni d'une structure différentielle compatible avec ses opérations.

**Action de groupe** — règle disant comment un groupe transforme les éléments d'un espace.

**Espace homogène** — espace sur lequel l'action du groupe est transitive.

**Stabilisateur** — sous-groupe laissant un point donné inchangé.

**G-CNN** — CNN dont les couches sont conçues pour respecter une action de groupe.

**Lifting** — passage d'une représentation sur l'espace d'entrée à une représentation sur le groupe ou un espace homogène plus riche.

**Projection** — réduction de cette représentation vers l'espace de sortie désiré tout en contrôlant la symétrie.

**Semi-anneau tropical** — structure algébrique dans laquelle les opérations usuelles sont remplacées, typiquement, par `max` et `+` ; elle permet de reformuler certains opérateurs non linéaires dans un cadre structurel.

---

## 16. Positionnement final dans Diderot ML

Cette source doit être conservée comme **pont pédagogique de référence** entre :

```text
Machine Learning Specialization
        ↓
réseaux / CNN / backprop / optimisation
        ↓
inductive bias
        ↓
variétés et groupes de Lie
        ↓
actions et symétries
        ↓
équivariance
        ↓
G-CNN
        ↓
structure-preserving ML
```

Elle est particulièrement précieuse parce qu'elle ne commence pas par la géométrie abstraite : elle part du réseau de neurones que l'étudiant connaît déjà et montre progressivement **pourquoi** les outils géométriques deviennent utiles.

C'est exactement le type de source que Diderot ML doit capitaliser : non pour accumuler des concepts, mais pour reconstruire le chemin qui fait passer d'un outil appris à une raison de l'utiliser.
