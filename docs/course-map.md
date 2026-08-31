# Carte editoriale du livre

Ce plan couvre la specialisation complete tout en distinguant le contenu deja
redige du contenu restant a reconstruire depuis les notes personnelles. Il est
complete par une couche de notions transverses afin qu'un concept puisse etre
retrouve independamment du cours dans lequel il a ete rencontre.

## Partie I - Apprentissage supervise : regression et classification

1. Introduction au machine learning
2. Regression lineaire et fonction de cout
3. Descente de gradient
4. Regression multiple et mise a l'echelle
5. Regression logistique
6. Frontieres de decision
7. Surapprentissage, regularisation et evaluation

## Partie II - Algorithmes avances

1. Reseaux de neurones et propagation avant
2. TensorFlow et implementation
3. Entrainement, biais, variance et diagnostic
4. Boucle de developpement ML
5. Arbres de decision et choix de coupure
6. Entropie, gain d'information et variance
7. Bagging, Random Forest et XGBoost

## Partie III - Apprentissage non supervise, recommandation et RL

1. Clustering et intuition de K-means
2. Affectation, deplacement des centroides et fonction de cout
3. Initialisation, minima locaux et choix de K
4. Detection d'anomalies
   - M3-W1-11 : distribution gaussienne et estimation des parametres
   - algorithme a plusieurs caracteristiques
   - choix des variables et evaluation
   - modele multivarie et correlations
5. Systemes de recommandation
6. Filtrage collaboratif et recommandations par contenu
7. Apprentissage par renforcement
8. Etats, actions, recompenses et equation de Bellman
9. Deep Q-learning

## Partie IV - Au-dela de la MLS : representations, attention et modeles d'etat

Cette partie ne pretend pas appartenir a la Machine Learning Specialization initiale. Elle documente
les notions devenues necessaires pour poursuivre vers la Deep Learning Specialization, les
Transformers, la vision, JEPA et les world models.

1. Representations vectorielles
   - feature, representation, embedding, hidden representation ;
   - parametres versus activations ;
   - geometrie des representations et PCA.
2. Sequences et contexte
   - tokenisation et tokens ;
   - position ;
   - hidden state et memoire de sequence.
3. Attention
   - Query / Key / Value ;
   - produit scalaire comme compatibilite ;
   - scaled dot-product attention ;
   - self-attention et multi-head attention.
4. Transformer
   - bloc attention + residual + normalisation + MLP ;
   - encoder, decoder, encoder-decoder ;
   - Transformer versus LLM.
5. Vision et representations spatiales
   - patch tokens ;
   - token `[CLS]` ;
   - structure semantique emergente des representations.
6. Etat latent et dynamique
   - observation, historique, hidden state, state representation ;
   - belief state en POMDP ;
   - suffisance predictive ;
   - predictive representation learning / JEPA ;
   - modele dynamique latent et world model.

Le point d'entree est [`concepts/README.md`](concepts/README.md), avec un premier guide detaille
[`concepts/representations-transformers.md`](concepts/representations-transformers.md) et une relecture
des fondations dans [`concepts/ml-foundations-revisited.md`](concepts/ml-foundations-revisited.md).

## Fils transverses Diderot ML

- lecture mathematique des formules ;
- geometrie, probabilites et theorie de l'information ;
- biometrie, identite et detection de fraude ;
- assurance qualite, risque residuel et observabilite ;
- MMALS et apprentissage continu ;
- simulation scientifique : observation -> EDP -> discretisation -> stabilite -> experience ;
- representations : signal -> token -> embedding -> contexte -> representation latente ;
- decision sous observation partielle : observation -> historique -> belief/state representation -> prediction/action ;
- ponts vers Fourier, valeurs propres, traitement du signal, automatique et systemes dynamiques ;
- fiches de revision et travaux pratiques reproductibles.

### Colonne vertebrale de notions

Diderot ML distingue desormais la progression par cours de la progression par notions. Une chaine
pedagogique utile pour les architectures modernes est :

`vecteur -> matrice/transformation -> produit scalaire -> reseau de neurones -> embedding -> softmax -> attention -> representation contextualisee -> etat latent -> dynamique latente`.

Cette chaine sert de carte, pas de preuve qu'un concept implique automatiquement le suivant. Chaque
maillon doit conserver ses hypotheses, limites et exemples propres.

### Laboratoire transverse : equation d'onde

Le [`Wave Equation Toy Lab`](waves-toy-lab.md) reconstruit huit experiences
progressives : impulsion 1D, source harmonique, interference, passage en 2D,
reflexion, modes propres et limite CFL. Il sert de premier laboratoire explicite
pour le chemin Diderot `intuition -> mathematiques -> numerique -> experience`.

### Laboratoire transverse : Von Neumann, CFL et dispersion numerique

Le [`Von Neumann & CFL Lab`](von-neumann-cfl-lab.md) repart de l'instabilite
observee dans le premier laboratoire et reconstruit le chemin
`erreur -> Fourier -> nombre complexe -> valeur propre discrete -> facteur
d'amplification -> spectre -> CFL -> dispersion`. Il relie ainsi l'analyse
numerique a l'algebre lineaire, aux systemes dynamiques et au traitement du
signal, avec un notebook de micro-experiences reproductibles.

### Laboratoire transverse : convergence, verification et validation

Le [`Wave Lab 3`](wave-convergence-verification-lab.md) ajoute le maillon
`solution exacte -> mesure d'erreur -> raffinement -> ordre de convergence ->
resolution par longueur d'onde -> phase -> energie -> budget d'erreurs`.
Il distingue explicitement la verification numerique (resout-on correctement
les equations choisies ?) de la validation physique (les equations sont-elles
adequates pour le systeme reel ?), afin de preparer proprement le futur passage
a Saint-Venant.

### Lecture transverse : geometrie, groupes de Lie et equivariance

La note [`Mathematics of Neural Networks — Smets`](../chat-notes/2026-08-31-smets-mathematics-of-neural-networks.md)
capitalise une source graduate-level qui part des fondations familieres des
reseaux de neurones puis reconstruit le chemin
`inductive bias -> varietes -> groupes de Lie -> actions -> espaces homogenes ->
operateurs equivariants -> G-CNN -> discretisation -> operateurs tropicaux`.
Elle sert de pont pedagogique entre la Machine Learning Specialization et le fil
Diderot `structure-preserving ML`. Le futur laboratoire associe devra mesurer
l'erreur d'equivariance et comparer CNN, augmentation de donnees et G-CNN.

### Lecture transverse : representations, attention et Transformer

Le guide [`Representations, attention et Transformer`](concepts/representations-transformers.md)
reconstruit le chemin
`signal -> token -> embedding -> Q/K/V -> attention -> representation contextualisee -> representation latente`.
Il relie les notions deja apprises (matrices, produit scalaire, softmax, reseaux de neurones) aux
architectures modernes, puis distingue explicitement representation latente, state representation et
belief state. Il prepare des experiences ulterieures sur attention minimale, Vision Transformer,
JEPA et world models.
