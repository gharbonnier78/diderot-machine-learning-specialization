# Carte editoriale du livre

Ce plan couvre la specialisation complete tout en distinguant le contenu deja
redige du contenu restant a reconstruire depuis les notes personnelles.

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

## Fils transverses Diderot ML

- lecture mathematique des formules ;
- geometrie, probabilites et theorie de l'information ;
- biometrie, identite et detection de fraude ;
- assurance qualite, risque residuel et observabilite ;
- MMALS et apprentissage continu ;
- simulation scientifique : observation -> EDP -> discretisation -> stabilite -> experience ;
- ponts vers Fourier, valeurs propres, traitement du signal, automatique et systemes dynamiques ;
- fiches de revision et travaux pratiques reproductibles.

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

