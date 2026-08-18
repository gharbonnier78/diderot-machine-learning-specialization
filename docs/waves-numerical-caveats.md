# Wave Equation Toy Lab — notes de fidélité numérique

Ce complément garde le laboratoire pédagogiquement simple sans transformer ses approximations en vérités plus générales qu'elles ne le sont.

## 1. La source ponctuelle du notebook n'est pas encore une Dirac normalisée

Dans l'équation continue, on peut écrire

\[
S(x,t)=A\sin(\omega t)\,\delta(x-x_0).
\]

La distribution de Dirac est définie de façon à conserver une intensité intégrée quand on change de résolution spatiale. Dans le notebook, la fonction `point_source_1d` ou `point_source_2d` fait volontairement quelque chose de plus simple : elle applique une force à **une cellule** du maillage.

**Lecture en français :** l'amplitude choisie dans le toy est une amplitude de forçage de cellule, pas encore une amplitude physique indépendante de la taille de la maille.

Conséquence : si l'on change fortement `dx` ou `dy`, il ne faut pas comparer directement l'amplitude obtenue comme si la même source physique avait été conservée. Une version ultérieure pourra proposer une source normalisée par la taille de cellule.

## 2. Neumann : pourquoi utiliser des points fantômes réfléchis ?

La condition continue est

\[
\frac{\partial u}{\partial n}=0.
\]

À gauche en 1D, une dérivée centrée s'écrit approximativement

\[
\frac{u_1-u_{-1}}{2\Delta x}=0.
\]

Le symbole `u_{-1}` représente ici un **point fantôme** situé juste à l'extérieur du domaine. L'équation précédente donne

\[
u_{-1}=u_1.
\]

**Lecture :** pour obtenir une pente normale nulle au mur, on imagine à l'extérieur une valeur miroir égale à celle du premier point intérieur.

Le solveur utilise cette construction miroir. C'est préférable, pour ce laboratoire, à la règle plus grossière consistant à écraser après chaque pas la valeur du bord par celle de son voisin. Avec les points fantômes, le bord continue à participer à l'équation différentielle discrète et les modes cosinus attendus sont préservés par l'opérateur discret.

## 3. Mode propre continu et mode propre discret

Pour la PDE continue sur un rectangle réfléchissant,

\[
\phi_{mn}(x,y)=\cos\left(\frac{m\pi x}{L_x}\right)
\cos\left(\frac{n\pi y}{L_y}\right)
\]

et

\[
\omega_{mn}=c\pi\sqrt{(m/L_x)^2+(n/L_y)^2}.
\]

Le notebook affiche cette **pulsation continue**. Mais une grille et un schéma temporel possèdent leur propre relation de dispersion : la fréquence observée numériquement n'est donc pas exactement la fréquence continue, surtout quand la longueur d'onde approche la taille des mailles.

**Lecture :** le motif spatial peut être parfaitement reconnu par le schéma alors que son rythme d'oscillation présente encore une petite erreur numérique.

Cette différence sera un excellent pont vers le laboratoire suivant sur Fourier, Von Neumann, facteur d'amplification et dispersion numérique.

## 4. CFL n'est pas une règle universelle détachée du schéma

Les limites

\[
\frac{c\Delta t}{\Delta x}\le 1
\]

en 1D et

\[
c^2\Delta t^2\left(\frac1{\Delta x^2}+\frac1{\Delta y^2}\right)\le1
\]

en 2D concernent ici le schéma explicite centré utilisé dans le laboratoire.

Changer l'équation, le schéma spatial, l'intégrateur temporel ou la grille peut changer la condition de stabilité.

**Lecture :** « CFL » n'est pas un nombre magique attaché à toutes les simulations ; c'est une contrainte qui naît de la rencontre entre une dynamique physique, une discrétisation et un algorithme temporel précis.

## 5. Ce que nous voulons apprendre de ces limites

Le but n'est pas de rendre le toy inutilement sophistiqué. Le but est de savoir à chaque étage ce qui relève :

- du phénomène physique ;
- du modèle mathématique ;
- de la discrétisation ;
- de l'implémentation ;
- de la visualisation.

Cette séparation évite une erreur fréquente : attribuer à la physique un artefact créé par le calcul numérique.
