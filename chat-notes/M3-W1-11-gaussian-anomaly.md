# M3-W1-11 - Gaussienne et detection d'anomalies

## Objet

Synthese editoriale originale de la discussion pedagogique autour de la video.
Ce fichier ne reproduit pas le transcript du cours.

## Questions qui ont structure la discussion

1. Que signifie reellement `p(x)` pour une variable continue ?
2. Comment un histogramme fini se relie-t-il a une densite theorique ?
3. Quelle difference entre variance `sigma^2` et ecart-type `sigma` ?
4. Pourquoi une gaussienne plus etroite devient-elle plus haute ?
5. Pourquoi `pi` apparait-il alors qu'aucun cercle n'est visible ?
6. Que signifient loi centree et loi centree reduite ?
7. Pourquoi la moyenne et la variance empiriques sont-elles les estimateurs du
   maximum de vraisemblance ?
8. Pourquoi voit-on parfois `1/(m-1)` a la place de `1/m` ?
9. Pourquoi une faible densite signale-t-elle une anomalie sans prouver une
   fraude ou une panne ?
10. Comment passer d'une seule caracteristique a un vecteur de signaux ?

## Resultats conceptuels

- Une densite est une hauteur; une probabilite continue est une aire.
- Dans une classe de largeur `Delta x`, la probabilite vaut environ
  `p(x) Delta x`.
- `mu` deplace la gaussienne; `sigma` change sa largeur.
- L'aire reste egale a un, ce qui impose une compensation largeur/hauteur.
- Le facteur `pi` vient de la mise au carre de l'integrale gaussienne et du
  passage aux coordonnees polaires dans le plan.
- Sous une contrainte de variance, la gaussienne est la distribution continue
  d'entropie maximale.
- La moyenne minimise la somme des distances carrees, ce qui relie estimation
  gaussienne et centroide de K-means.
- Une anomalie est une incompatibilite statistique avec le modele, pas une cause.

## Application a l'identite

Le detecteur devra combiner plusieurs familles de signaux : activite, scores
biometriques, qualite, terminal, reseau, historique du credential et contexte.
La conception devra egalement chercher les anomalies d'exclusion : parcours
trop long, repetition de capture, difficulte associee a un capteur ou a une
population. La qualification humaine et l'audit restent distincts du calcul de
densite.

## Point de reprise

Le prochain chapitre construit le detecteur a plusieurs caracteristiques : une
gaussienne par variable, produit des densites, choix du seuil et limites de
l'hypothese d'independance.

