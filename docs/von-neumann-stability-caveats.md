# Von Neumann — précision sur `|G| = 1` et les racines doubles

Cette note complète le laboratoire principal. Elle ne change pas la condition CFL classique obtenue pour le schéma centré de l'équation d'onde ; elle précise un détail mathématique important à la frontière exacte de stabilité.

## 1. Pourquoi `|G| ≤ 1` n'est pas, à lui seul, toute l'histoire

Pour un mode de Fourier, nous obtenons la récurrence caractéristique

\[
G^2-2aG+1=0.
\]

Lorsque

\[
-1<a<1,
\]

les deux racines sont distinctes et se trouvent sur le cercle unité :

\[
G_{1,2}=e^{\pm i\Omega}.
\]

Dans ce cas, une combinaison des deux solutions reste bornée : chaque composante est une oscillation d'amplitude constante.

Mais aux valeurs limites

\[
a=1 \quad\text{ou}\quad a=-1,
\]

les deux racines se confondent :

\[
G=1 \quad\text{ou}\quad G=-1.
\]

Pour une équation de récurrence d'ordre deux ayant une racine double `G`, la solution générale peut contenir

\[
(C_1+C_2 n)G^n.
\]

Le facteur `n` peut donc produire une croissance linéaire, même si

\[
|G|=1.
\]

### Lecture en français

> « Voir toutes les racines sur le cercle unité empêche une croissance exponentielle, mais une racine répétée sur ce cercle peut encore autoriser une croissance lente, proportionnelle au nombre de pas. »

C'est la **condition des racines** qui est plus précise : les racines doivent avoir un module inférieur ou égal à un, et les racines situées exactement sur le cercle unité doivent être simples pour garantir le bornage de toute donnée initiale arbitraire.

## 2. Deux cas limites différents dans notre schéma

### Le mode constant `θ = 0`

Pour `θ=0`, le stencil spatial vaut zéro et l'équation discrète devient

\[
u^{n+1}-2u^n+u^{n-1}=0.
\]

La solution générale est

\[
u^n=A+Bn.
\]

Cela ressemble à une croissance, mais elle a ici une interprétation physique simple : un déplacement spatialement constant avec une vitesse initiale moyenne non nulle évolue linéairement dans le temps. Ce n'est pas nécessairement une instabilité numérique parasite.

### Le couple `r=1`, `θ=π`

Au bord CFL 1D,

\[
r=1,
\]

et pour le mode de Nyquist

\[
\theta=\pi,
\]

nous obtenons

\[
a=-1
\]

et donc la racine double

\[
G=-1.
\]

Pour des données à deux niveaux parfaitement compatibles avec la branche d'onde propagative, le cas `r=1` possède la remarquable relation de phase exacte décrite dans le laboratoire. Mais pour des données arbitraires au mode de Nyquist, la racine double permet aussi un terme

\[
n(-1)^n.
\]

Il faut donc distinguer :

- la **relation de dispersion** particulière et très favorable du schéma 1D à `r=1` ;
- le **bornage uniforme pour toute paire de niveaux temporels arbitraire**, qui demande de traiter la racine double avec précaution.

## 3. Que faut-il retenir opérationnellement ?

La condition CFL usuelle du schéma reste

\[
|r|\le1
\]

en 1D, et

\[
r_x^2+r_y^2\le1
\]

en 2D.

Elle identifie correctement la frontière séparant le régime où apparaissent des racines de module strictement supérieur à un du régime sans croissance exponentielle de Fourier.

Mais, dans une simulation d'ingénierie, on évite généralement de travailler exactement sur la frontière théorique :

\[
\text{on choisit une marge CFL}.
\]

Cette marge couvre à la fois les subtilités de frontière, les autres approximations du modèle, les coefficients variables éventuels et les erreurs de calcul.

### Lecture en français

> « `CFL ≤ limite` donne la frontière théorique du schéma idéal ; `CFL suffisamment sous la limite` est souvent la décision pratique plus robuste. »

## 4. Pourquoi conserver cette nuance dans Diderot ML ?

Parce qu'elle illustre exactement la méthode recherchée : une formule simple comme

\[
|G|\le1
\]

est utile, mais il faut toujours demander :

1. quelles hypothèses rendent cette phrase vraie ?
2. que se passe-t-il aux cas limites ?
3. parle-t-on d'absence de croissance exponentielle ou de bornage uniforme ?
4. quelle marge prendrait-on dans une vraie simulation ?

Cette petite nuance relie l'analyse de Von Neumann à une idée plus générale d'algèbre linéaire et de systèmes dynamiques : **les valeurs propres ne suffisent pas toujours ; leur multiplicité et la structure des modes associés peuvent compter.**
