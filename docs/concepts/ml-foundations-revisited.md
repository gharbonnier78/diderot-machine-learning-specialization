# Fondations ML revisitees — notions a reconnecter

Ce document ne remplace pas les chapitres de la Machine Learning Specialization. Il revient sur des
notions deja rencontrees et les relit avec les questions apparues ensuite : representations, attention,
etats latents, geometrie, POMDP et world models.

L'objectif pedagogique est double : consolider les bases et montrer qu'une notion simple change de
signification lorsqu'elle est reutilisee dans une architecture plus riche.

---

## 1. Vecteur : plus qu'une liste de nombres

Dans un premier cours de ML, un vecteur apparait souvent comme un ensemble de features :

\[
x=(x_1,\ldots,x_d).
\]

Mais le meme objet mathematique peut etre lu de plusieurs manieres :

- un point dans un espace ;
- une direction ;
- un ensemble de mesures ;
- une representation apprise ;
- un etat interne ;
- un embedding.

Le sens ne vient donc pas du fait qu'il s'agit d'un vecteur, mais de **ce que ses coordonnees
representent, comment il est construit et comment il est utilise**.

### Question a toujours poser

> Ce vecteur est-il une donnee brute, une feature engineeriee, une activation, un embedding, un etat
> latent ou un parametre ?

---

## 2. Matrice : stockage ou transformation ?

Une matrice peut etre un tableau de donnees, mais dans un reseau de neurones elle represente souvent
une transformation lineaire :

\[
y = Wx.
\]

Cette lecture est essentielle pour comprendre l'attention. Les matrices `W_Q`, `W_K` et `W_V` ne
sont pas trois bases de donnees ; elles apprennent trois projections :

\[
x \mapsto q, \qquad x \mapsto k, \qquad x \mapsto v.
\]

### Lecture geometrique

Multiplier par une matrice peut :

- tourner ;
- etirer ;
- comprimer ;
- projeter ;
- recombiner les directions d'un espace.

Dans un modele appris, ces transformations sont optimisees pour rendre certaines relations utiles a
la loss.

---

## 3. Produit scalaire : de la formule a la compatibilite

Le produit scalaire :

\[
x^\top y = \sum_i x_i y_i
\]

apparait dans la regression, la geometrie, les similarites cosinus et l'attention.

Geometriquement :

\[
x^\top y = \|x\|\,\|y\|\cos\theta.
\]

Il combine donc norme et alignement. Dans une attention `QK^T`, le produit scalaire est utilise comme
**score de compatibilite appris** entre une query et une key.

### Confusion a eviter

Un grand produit scalaire ne signifie pas universellement « meme sens semantique ». Cette
interpretation depend de l'espace appris, des normes et de la tache.

---

## 4. Feature, representation, embedding, latent variable

Ces mots sont souvent utilises comme s'ils etaient interchangeables.

### Feature

Variable fournie ou construite pour le modele : age, latence, score, pixel, etc.

### Representation

Terme general pour la facon dont une information est encodee dans un espace exploitable.

### Embedding

Representation vectorielle dense d'une unite, souvent discrete ou structuree : token, utilisateur,
produit, patch, graphe, etc.

### Latent representation

Representation interne non directement observee dans les donnees brutes.

### State representation

Representation destinee a resumer ce qui est pertinent de l'etat d'un processus pour predire ou
decider.

Une bonne discipline est donc : ne jamais appeler automatiquement tout vecteur interne « etat ».

---

## 5. Parametre versus activation

Dans un reseau :

\[
h = \sigma(Wx+b),
\]

`W` et `b` sont des **parametres appris**. `h` est une **activation calculee** pour une entree donnee.

Cette distinction devient fondamentale dans un Transformer :

- `W_Q`, `W_K`, `W_V` : poids appris ;
- `Q`, `K`, `V` : valeurs calculees pour la sequence courante ;
- matrices d'attention : dependent de l'entree ;
- representations finales : dependent egalement de l'entree.

Ainsi, analyser les representations n'est pas la meme chose qu'analyser les poids du modele.

---

## 6. Softmax : pas uniquement la derniere couche d'un classifieur

Pour des scores `s_1,...,s_n` :

\[
\operatorname{softmax}(s_i)
= \frac{e^{s_i}}{\sum_j e^{s_j}}.
\]

Le resultat est positif et somme a 1. Dans une classification, on l'interprete souvent comme une
distribution sur les classes. Dans l'attention, les memes mathematiques servent a obtenir des
**coefficients de melange** entre Value vectors.

### Lecon generale

Une operation mathematique n'a pas une interpretation unique. Son role depend de l'endroit ou elle est
placee dans le modele.

---

## 7. Probabilite, densite et vraisemblance

Ces trois notions sont deja importantes dans le chapitre gaussien et deviennent encore plus utiles
dans les modeles probabilistes d'etat.

### Probabilite

Mesure associee a un evenement :

\[
P(X \in A).
\]

### Densite

Pour une variable continue :

\[
p(x)
\]

est une hauteur telle que la probabilite d'un intervalle est une integrale.

### Vraisemblance

Lorsque les donnees sont fixees et que l'on fait varier les parametres :

\[
L(\theta;x)=p(x\mid\theta).
\]

La meme expression numerique peut donc etre lue differemment selon ce qui est considere variable.

### Pont vers POMDP

Le belief state :

\[
b_t(s)=P(S_t=s\mid h_t)
\]

est une distribution conditionnelle sur un etat cache, pas une simple activation neuronale.

---

## 8. Loss, supervision et structure interne

Une loss specifie ce qui est directement optimise :

\[
\min_\theta \mathcal{L}(f_\theta(x),y).
\]

Mais la loss ne dit pas exactement quelle organisation interne le reseau doit adopter. Plusieurs
representations internes peuvent mener a la meme performance de sortie.

C'est pourquoi une supervision appliquee seulement a une sortie globale peut tout de meme entrainer
des representations locales structurees. Le gradient traverse les couches intermediaires.

### Prudence

Une structure interne observee ne doit pas etre interpretee trop vite comme une variable causale ou un
concept humain explicite. Il faut verifier par experiences, interventions, ablations ou probes adaptees.

---

## 9. PCA : sur quoi applique-t-on la reduction de dimension ?

La PCA est une methode geometrique appliquee a un ensemble de vecteurs. Ces vecteurs peuvent etre :

- des observations brutes ;
- des features ;
- des embeddings ;
- des activations intermediaires ;
- parfois des poids, si cette question a un sens experimental.

Dire « faire une PCA du modele » est donc ambigu. Il faut toujours preciser l'objet :

\[
\{h_i\}_{i=1}^N \subset \mathbb{R}^d
\]

par exemple les patch-token representations produites par un encodeur pour une image ou un corpus.

### Ce que montre une PCA

Elle montre les directions lineaires de variance dominante. Elle ne prouve pas automatiquement que les
axes identifies correspondent aux facteurs fondamentaux du monde ou aux concepts utilises par le modele.

---

## 10. Etat, observation et historique

En apprentissage par renforcement, il est tentant de confondre ce que l'agent voit et l'etat reel.

### MDP

On suppose disposer d'un etat `S_t` suffisamment informatif :

\[
P(S_{t+1}\mid S_{0:t},A_{0:t})
= P(S_{t+1}\mid S_t,A_t).
\]

### POMDP

L'agent observe `O_t`, qui ne determine pas necessairement `S_t`. Il doit utiliser l'historique :

\[
h_t=(o_1,a_1,o_2,a_2,\ldots,o_t).
\]

Le belief ideal est :

\[
b_t(s)=P(S_t=s\mid h_t).
\]

### Representation neurale

Un reseau peut apprendre :

\[
z_t=f_\theta(h_t).
\]

Mais la question scientifique devient alors : **qu'est-ce qui garantit que `z_t` conserve ce qui est
necessaire ?**

Cette question ouvre vers les notions de sufficient statistic, predictive state, representation
d'etat et world model.

---

## 11. Markovien ne signifie pas deterministe

La propriete de Markov concerne la dependance conditionnelle, pas l'absence d'aleatoire.

Un systeme peut etre a la fois :

- markovien ;
- stochastique.

Par exemple :

\[
S_{t+1}\sim P(\cdot\mid S_t,A_t).
\]

Le prochain etat peut rester incertain meme lorsque l'etat actuel est parfaitement connu.

Cette distinction est importante lorsqu'on parle de world model : apprendre une dynamique peut
signifier apprendre une distribution conditionnelle, pas seulement une fonction deterministe.

---

## 12. Hidden state versus belief state

Un hidden state d'un RNN est un vecteur calcule :

\[
h_t=f_\theta(h_{t-1},x_t).
\]

Un belief state est une distribution probabiliste definie par le modele POMDP :

\[
b_t(s)=P(S_t=s\mid h_t^{obs}).
\]

Un hidden state peut etre entraine pour approximer l'information d'un belief state, mais les deux
objets ne sont pas identiques par definition.

---

## 13. Prediction correcte versus representation correcte

Un modele peut produire une prediction correcte pour de mauvaises raisons, ou grace a des correlations
fragiles. Reciproquement, une representation interpretable n'est pas automatiquement la plus utile pour
toutes les taches.

Pour analyser une representation, il faut donc distinguer :

1. performance de sortie ;
2. robustesse hors distribution ;
3. invariances/equivariances ;
4. information predictive conservee ;
5. sensibilite aux perturbations ;
6. structure geometrique ;
7. stabilite temporelle ;
8. cout de calcul et de memoire.

Cette grille sera utile pour les futures etudes JEPA, continual learning et world models.

---

## 14. Une nouvelle chaine de prerequis

Les notions apprises dans la Machine Learning Specialization peuvent maintenant etre reconnectees :

`algebre lineaire -> couches lineaires -> reseaux de neurones -> embeddings -> similarite/produit scalaire -> softmax -> attention -> representations contextualisees -> etat latent -> dynamique latente`.

Cette chaine ne signifie pas que chaque concept derive automatiquement du precedent. Elle indique
plutot une progression pedagogique permettant de comprendre les architectures modernes sans les
traiter comme des boites noires.

---

## 15. Questions Diderot a conserver ouvertes

Ces questions doivent devenir des fiches ou des experiences ulterieures :

- Quand une representation devient-elle suffisante pour predire le futur pertinent ?
- Peut-on mesurer la perte d'information entre historique et etat latent ?
- Comment distinguer structure semantique reelle et artefact de projection PCA ?
- Quel role la geometrie de l'espace latent joue-t-elle dans la generalisation ?
- Quelle difference experimentale entre embedding statique et representation contextualisee ?
- Comment verifier qu'un world model a appris une dynamique plutot qu'une correlation de trajectoire ?
- Quand un etat latent doit-il etre probabiliste plutot que deterministe ?
- Quels mecanismes permettent de conserver les competences acquises en continual learning sans figer le modele ?

Elles forment un pont naturel entre la specialisation ML initiale et les prochains blocs Diderot sur le
deep learning, la representation learning, les systemes dynamiques et l'apprentissage continu.
