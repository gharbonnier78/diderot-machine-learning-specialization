# Von Neumann & CFL Lab — pourquoi une simulation numérique peut-elle exploser ?

[🇫🇷 Français](#fr) · [🇬🇧 English](#en) · [🇪🇸 Español](#es) · [🇵🇹 Português](#pt)

> **Question de départ** : dans le premier Wave Equation Toy Lab, nous avons volontairement choisi un pas de temps trop grand et vu `max(|u|)` exploser. Pourquoi ? Ici, nous ne mémorisons pas la condition CFL. Nous essayons de la **retrouver nous-mêmes**.

<a id="fr"></a>

# 🇫🇷 Français — reconstruction pas à pas

## 0. Le chemin que nous allons reconstruire

```text
une petite erreur numérique existe toujours
        ↓
on veut savoir si elle va mourir, rester bornée ou grandir
        ↓
on décompose une erreur compliquée en oscillations simples
        ↓
mode de Fourier exp(i j θ)
        ↓
le stencil de différences finies agit très simplement sur ce mode
        ↓
le mode est un vecteur/fonction propre de l'opérateur discret
        ↓
on mesure ce qu'un pas de temps fait à son amplitude : facteur G
        ↓
stabilité : aucune composante ne doit croître sans borne
        ↓
|G| ≤ 1 pour tous les nombres d'onde résolus
        ↓
condition CFL
        ↓
puis : même stable, le schéma peut déformer la vitesse des différentes ondes
        ↓
dispersion numérique
```

Le point important est que **Fourier, nombres complexes, valeurs propres et stabilité numérique apparaissent ici pour répondre à une seule question d'ingénierie : peut-on faire confiance à la simulation après beaucoup d'itérations ?**

---

## 1. Repartons du schéma que nous connaissons

Pour l'équation d'onde 1D

\[
\frac{\partial^2u}{\partial t^2}
=
c^2\frac{\partial^2u}{\partial x^2},
\]

le schéma centré explicite utilisé dans le premier laboratoire est

\[
u_j^{n+1}-2u_j^n+u_j^{n-1}
=
r^2\left(u_{j+1}^n-2u_j^n+u_{j-1}^n\right),
\]

avec

\[
r=\frac{c\Delta t}{\Delta x}.
\]

### Lecture en français

- `j` indique **où** nous sommes sur la grille spatiale ;
- `n` indique **quand** nous sommes ;
- `u_j^n` est donc « la valeur de `u` au point `j`, au pas de temps `n` » ;
- `r` compare la distance physique `c Δt` parcourue pendant un pas de temps à la taille `Δx` d'une maille.

Le schéma dit en substance :

> « La valeur future dépend des deux niveaux temporels précédents et de la courbure spatiale actuelle estimée avec le voisin gauche, le point courant et le voisin droit. »

Dans le premier laboratoire, nous avons constaté expérimentalement :

- `r = 0.65` : comportement stable ;
- `r > 1` en 1D : comportement instable ;
- en 2D carrée, la limite arrive déjà vers `1/sqrt(2)`.

Mais constater n'est pas encore comprendre.

---

## 2. Pourquoi analyser une **erreur** plutôt que la solution ?

Un calcul numérique contient toujours de petites perturbations :

- arrondis flottants ;
- erreur de discrétisation ;
- données initiales imparfaites ;
- interpolation ;
- approximation des frontières ;
- bruit introduit par d'autres composants d'un système.

Supposons que la solution calculée soit

\[
u = u_{\mathrm{exact}} + e,
\]

où `e` est une petite erreur.

Pour une équation et un schéma **linéaires**, l'erreur obéit au même schéma homogène que la solution.

### Lecture

> « Au lieu de demander directement si toute la solution est correcte, nous pouvons demander ce que l'algorithme fait à une petite erreur. »

Si une erreur de taille `10^-12` devient `10^-11`, puis `10^-10`, puis `10^-9`, etc., le problème finit par être dominé par l'algorithme numérique lui-même.

La stabilité demande donc essentiellement :

> **Est-ce que le schéma amplifie certaines petites perturbations à chaque itération ?**

---

## 3. Une erreur compliquée peut être vue comme une somme d'oscillations simples

Une idée fondamentale de Fourier est qu'un signal suffisamment raisonnable peut être décomposé en composantes oscillantes.

Nous allons donc étudier une seule composante :

\[
e_j^n = G^n e^{i j\theta}.
\]

Cette formule semble abstraite. Relisons-la morceau par morceau.

### `e^{i jθ}` : la forme dans l'espace

Grâce à la formule d'Euler,

\[
e^{i\alpha}=\cos\alpha+i\sin\alpha.
\]

Donc `exp(i j θ)` contient simplement une oscillation sinusoïdale/cosinusoïdale.

Le paramètre

\[
\theta=k\Delta x
\]

est un **nombre d'onde discret sans dimension**.

- petit `θ` : onde longue par rapport à la maille ;
- `θ` proche de `π` : onde très courte, alternant presque `+ - + -` d'une cellule à l'autre.

### `G^n` : ce que le temps fait à l'amplitude

`G` est le **facteur d'amplification**.

Après un pas : amplitude multipliée par `G`.

Après deux pas : par `G²`.

Après `n` pas : par `G^n`.

Donc :

- `|G| < 1` : la composante décroît ;
- `|G| = 1` : elle reste de même amplitude ;
- `|G| > 1` : elle grandit exponentiellement avec le nombre de pas.

### Lecture globale

\[
e_j^n = G^n e^{i j\theta}
\]

se lit :

> « Je choisis une erreur ayant une forme oscillante simple dans l'espace et je demande de quel facteur le schéma multiplie son amplitude à chaque pas de temps. »

---

## 4. Pourquoi les modes de Fourier rendent-ils le calcul si simple ?

Regardons le stencil spatial

\[
e_{j+1}-2e_j+e_{j-1}.
\]

Pour

\[
e_j=e^{ij\theta},
\]

nous avons

\[
e_{j+1}=e^{i(j+1)\theta}=e^{ij\theta}e^{i\theta},
\]

et

\[
e_{j-1}=e^{ij\theta}e^{-i\theta}.
\]

On peut donc factoriser `e^{ijθ}` :

\[
e_{j+1}-2e_j+e_{j-1}
=
e^{ij\theta}
\left(e^{i\theta}-2+e^{-i\theta}\right).
\]

Avec

\[
e^{i\theta}+e^{-i\theta}=2\cos\theta,
\]

cela devient

\[
2\cos\theta-2.
\]

Puis l'identité

\[
\cos\theta-1=-2\sin^2\left(\frac\theta2\right)
\]

donne

\[
\boxed{
e^{i\theta}-2+e^{-i\theta}
=-4\sin^2\left(\frac\theta2\right)
}.
\]

### Lecture en français

> « Le stencil ne transforme pas un mode de Fourier en une forme compliquée différente. Il conserve la même forme et la multiplie seulement par un nombre. »

C'est exactement l'idée d'un **vecteur propre / d'une fonction propre** :

\[
L\phi=\lambda\phi.
\]

Ici :

- `φ = exp(i j θ)` ;
- `L` = opérateur de seconde différence ;
- `λ(θ) = -4 sin²(θ/2)`.

Voilà pourquoi les valeurs propres et Fourier apparaissent naturellement dans l'analyse numérique.

---

## 5. Injectons maintenant ce mode dans le schéma temporel

Nous posons

\[
u_j^n = G^n e^{ij\theta}.
\]

Le niveau suivant vaut

\[
u_j^{n+1}=G^{n+1}e^{ij\theta},
\]

et le précédent

\[
u_j^{n-1}=G^{n-1}e^{ij\theta}.
\]

En injectant tout cela dans

\[
u_j^{n+1}-2u_j^n+u_j^{n-1}
=
r^2(u_{j+1}^n-2u_j^n+u_{j-1}^n),
\]

et en utilisant le résultat spatial précédent, on obtient

\[
G^{n+1}-2G^n+G^{n-1}
=
-4r^2G^n\sin^2\left(\frac\theta2\right).
\]

Nous pouvons diviser par `G^{n-1}` :

\[
G^2-2G+1
=
-4r^2G\sin^2\left(\frac\theta2\right).
\]

Donc

\[
\boxed{
G^2
-2\left[1-2r^2\sin^2\left(\frac\theta2\right)\right]G
+1=0
}.
\]

Pour alléger l'écriture, définissons

\[
a=1-2r^2\sin^2\left(\frac\theta2\right).
\]

Alors

\[
\boxed{G^2-2aG+1=0}.
\]

### Lecture

> « Pour chaque fréquence spatiale `θ`, le schéma possède deux facteurs d'amplification possibles, déterminés par cette équation du second degré. »

Le produit des deux racines vaut `1`, car le terme constant est `1`.

C'est déjà instructif : si une racine a un module strictement supérieur à `1`, l'autre doit avoir un module inférieur à `1`. Une composante instable suffit à condamner le calcul à long terme.

---

## 6. Quand les racines restent-elles sur le cercle unité ?

L'équation

\[
G^2-2aG+1=0
\]

peut être réécrite, après division par `G`, sous la forme

\[
G+\frac1G=2a.
\]

Si `|G|=1`, nous pouvons écrire

\[
G=e^{i\Omega}.
\]

Alors

\[
G+G^{-1}=e^{i\Omega}+e^{-i\Omega}=2\cos\Omega.
\]

Donc

\[
a=\cos\Omega.
\]

Or un cosinus réel reste entre `-1` et `1`. La condition pour que les racines restent oscillatoires de module `1` est donc

\[
\boxed{|a|\le1}.
\]

En remplaçant `a` :

\[
-1
\le
1-2r^2\sin^2(\theta/2)
\le
1.
\]

La borne de droite est automatiquement satisfaite. La borne de gauche donne

\[
r^2\sin^2\left(\frac\theta2\right)\le1.
\]

Mais nous voulons être stables **pour toutes les fréquences que la grille peut contenir**.

Le pire cas est

\[
\sin^2(\theta/2)=1,
\]

atteint pour

\[
\theta=\pi.
\]

Il reste donc

\[
r^2\le1,
\]

c'est-à-dire

\[
\boxed{|r|\le1}.
\]

Comme

\[
r=\frac{c\Delta t}{\Delta x},
\]

nous retrouvons

\[
\boxed{
\frac{c\Delta t}{\Delta x}\le1
}.
\]

### Lecture en français

> « Pour ce schéma 1D, le pas de temps doit être assez petit pour que le nombre de Courant ne dépasse pas un. Sinon, au moins une oscillation spatiale que la grille sait représenter possède un facteur d'amplification supérieur à un et finit par exploser. »

Nous n'avons pas appris CFL par cœur : **nous l'avons reconstruite à partir du comportement des erreurs.**

---

## 7. Pourquoi le mode `θ = π` est-il le plus dangereux ?

Pour `θ = π`,

\[
e^{ij\pi}=(-1)^j.
\]

La grille ressemble donc à

```text
+1  -1  +1  -1  +1  -1 ...
```

C'est l'oscillation spatiale la plus rapide qu'une grille puisse distinguer : deux points voisins prennent des signes opposés.

### Lecture

> « Le premier mode à révéler l'instabilité est le mode le plus proche de la résolution limite de la grille. »

Cela explique pourquoi une simulation instable commence souvent par faire apparaître des motifs très oscillants ou un bruit de maille avant que toute la solution diverge visuellement.

---

## 8. Passage en 2D : d'où vient `1/sqrt(2)` ?

En 2D, définissons

\[
r_x=\frac{c\Delta t}{\Delta x},
\qquad
r_y=\frac{c\Delta t}{\Delta y}.
\]

Le mode devient

\[
u_{j,k}^n
=
G^n e^{i(j\theta_x+k\theta_y)}.
\]

Chaque direction apporte son propre terme de seconde différence. On obtient

\[
a
=
1
-2r_x^2\sin^2\left(\frac{\theta_x}{2}\right)
-2r_y^2\sin^2\left(\frac{\theta_y}{2}\right).
\]

Pour être stable pour toutes les fréquences, il faut considérer simultanément les pires fréquences dans `x` et `y` :

\[
\theta_x=\theta_y=\pi.
\]

La condition devient

\[
\boxed{r_x^2+r_y^2\le1}.
\]

En remplaçant `r_x` et `r_y` :

\[
\boxed{
c^2\Delta t^2
\left(
\frac1{\Delta x^2}
+
\frac1{\Delta y^2}
\right)
\le1
}.
\]

Sur une grille carrée,

\[
\Delta x=\Delta y=h,
\]

donc

\[
2\left(\frac{c\Delta t}{h}\right)^2\le1.
\]

Ainsi

\[
\boxed{
\frac{c\Delta t}{h}
\le
\frac1{\sqrt2}
}.
\]

### Lecture

> « En 2D, l'opérateur spatial peut produire de la courbure dans deux directions en même temps. Le budget de stabilité est donc partagé entre `x` et `y`, ce qui rend le pas de temps admissible plus petit. »

Le fameux `1/sqrt(2)` n'est donc plus mystérieux.

---

## 9. L'intuition “l'information ne doit pas sauter trop loin” : utile, mais pas toute la preuve

On raconte souvent CFL ainsi : pendant un pas de temps, une onde parcourt environ

\[
c\Delta t.
\]

Si cette distance devient trop grande par rapport à la maille, le stencil local ne peut plus représenter correctement la propagation de l'information.

Cette intuition est précieuse. Mais elle ne remplace pas l'analyse mathématique : la constante exacte dépend du schéma et de la dimension.

### À retenir

- l'intuition géométrique explique **pourquoi** une contrainte reliant vitesse, temps et maille est plausible ;
- l'analyse de Von Neumann explique **quelle contrainte exacte** possède ce schéma linéaire particulier.

---

## 10. Stable ne signifie pas exact : apparition de la dispersion numérique

Lorsque le schéma est stable, nous pouvons écrire

\[
G=e^{\pm i\omega_{num}\Delta t}.
\]

La relation précédente donne

\[
\cos(\omega_{num}\Delta t)
=
1-2r^2\sin^2\left(\frac{k\Delta x}{2}\right).
\]

Une forme très utile est

\[
\boxed{
\sin\left(\frac{\omega_{num}\Delta t}{2}\right)
=
r\sin\left(\frac{k\Delta x}{2}\right)
}.
\]

Dans le monde continu, l'équation d'onde idéale vérifie

\[
\omega=ck.
\]

Le schéma discret ne reproduit cette relation qu'approximativement.

Pour les grandes longueurs d'onde,

\[
k\Delta x\ll1,
\]

nous pouvons utiliser `sin(z) ≈ z`, et la relation discrète redevient approximativement

\[
\omega_{num}\approx ck.
\]

Mais près de la résolution de la grille, les sinus ne sont plus linéaires et la vitesse de phase numérique change avec `k`.

### Lecture

> « Deux ondes de fréquences spatiales différentes peuvent voyager à des vitesses numériques légèrement différentes alors que le modèle physique idéal leur donnait la même vitesse `c`. »

C'est la **dispersion numérique**.

Elle produit une leçon fondamentale :

\[
\boxed{\text{stable} \neq \text{précis}}
\]

Une simulation peut rester parfaitement bornée et pourtant transporter les phases au mauvais rythme.

---

## 11. Un cas étonnant : `r = 1` en 1D

Pour le schéma 1D et `r = 1`,

\[
\sin(\omega_{num}\Delta t/2)
=
\sin(k\Delta x/2).
\]

Sur la branche résolue `0 ≤ kΔx ≤ π`, cela conduit à

\[
\omega_{num}\Delta t=k\Delta x.
\]

Puisque

\[
\Delta t=\frac{\Delta x}{c},
\]

nous obtenons

\[
\omega_{num}=ck.
\]

Pour ce cas très particulier, le schéma 1D est donc sans dispersion de phase sur la branche résolue idéale.

Ce résultat ne doit pas être généralisé naïvement à d'autres dimensions, d'autres PDE ou d'autres schémas.

---

## 12. Les micro-expériences du notebook

Le notebook compagnon suit cette progression :

1. **Voir l'erreur grandir ou rester bornée** : reprendre une perturbation minuscule et comparer `r < 1` et `r > 1`.
2. **Voir un mode de Fourier** : visualiser `cos(jθ)` pour plusieurs `θ`, jusqu'au mode `π` alterné `+ - + -`.
3. **Vérifier numériquement la propriété de valeur propre** du stencil : appliquer la seconde différence à un mode et observer qu'on retrouve la même forme multipliée par `-4 sin²(θ/2)`.
4. **Tracer `|G(θ)|`** pour plusieurs valeurs de `r` et voir apparaître une zone au-dessus de `1` dès que CFL est violée.
5. **Cartographier la stabilité 2D** dans le plan `(r_x,r_y)` et retrouver le disque `r_x²+r_y² ≤ 1`.
6. **Tracer la vitesse de phase numérique** et observer la dispersion.
7. **Comparer théorie et simulation directe** : le mode prédit instable par `|G|>1` doit effectivement croître dans le solveur temporel.

À chaque fois : **prédire avant d'exécuter**.

---

## 13. Ce que Von Neumann suppose ici

Il faut aussi savoir ce que nous venons de démontrer — et ce que nous n'avons pas démontré.

L'analyse précédente est particulièrement naturelle pour :

- un problème linéaire ;
- coefficients constants ;
- grille régulière ;
- analyse locale sur un domaine infini ou périodique, de façon à utiliser directement les modes de Fourier.

Les frontières, coefficients variables, non-linéarités et maillages complexes peuvent demander d'autres outils de stabilité.

Pour notre schéma d'onde simple, l'analyse donne exactement la condition CFL classique utilisée dans le premier laboratoire. Mais il faut retenir le principe méthodologique : **ne pas exporter mécaniquement une condition de stabilité hors du modèle et du schéma qui l'ont produite.**

---

## 14. L'arbre de connaissances obtenu

```text
ERREUR NUMÉRIQUE
      ↓
LINÉARITÉ
  étudier l'erreur séparément
      ↓
FOURIER
  décomposer en oscillations
      ↓
NOMBRES COMPLEXES
  exp(iθ) = cosθ + i sinθ
      ↓
OPÉRATEUR DISCRET
  stencil de seconde différence
      ↓
VALEUR PROPRE / SYMBOLE
  λ(θ) = -4 sin²(θ/2)
      ↓
DYNAMIQUE TEMPORELLE
  facteur d'amplification G
      ↓
SPECTRE
  max |G|
      ↓
STABILITÉ
  |G| ≤ 1
      ↓
CFL
  r≤1 en 1D ; rx²+ry²≤1 en 2D
      ↓
DISPERSION
  stable mais phase imparfaite
      ↓
VALIDATION NUMÉRIQUE
  convergence · résolution · erreurs · confiance
```

Ce chemin relie donc directement l'analyse numérique à des notions déjà rencontrées ailleurs : Fourier, algèbre linéaire, valeurs propres, systèmes dynamiques et traitement du signal.

---

## 15. Fiche ultra-courte

Pour le schéma centré 1D :

\[
u_j^{n+1}-2u_j^n+u_j^{n-1}
=r^2(u_{j+1}^n-2u_j^n+u_{j-1}^n).
\]

Mode test :

\[
u_j^n=G^n e^{ij\theta}.
\]

Symbole du stencil :

\[
-4\sin^2(\theta/2).
\]

Équation d'amplification :

\[
G^2-2aG+1=0,
\qquad
a=1-2r^2\sin^2(\theta/2).
\]

Stabilité pour tous les modes :

\[
|r|\le1.
\]

En 2D :

\[
r_x^2+r_y^2\le1.
\]

Grille carrée :

\[
\frac{c\Delta t}{h}\le\frac1{\sqrt2}.
\]

Et surtout :

\[
\boxed{\text{stabilité n'implique pas exactitude}}
\]

car il reste notamment la dispersion numérique.

---

<a id="en"></a>

# 🇬🇧 English — compact map

The purpose is to derive CFL rather than memorise it. A numerical error is decomposed into Fourier modes

\[
e_j^n=G^n e^{ij\theta}.
\]

The centred second-difference stencil has Fourier symbol

\[
-4\sin^2(\theta/2).
\]

Substitution into the 1D centred wave scheme gives

\[
G^2-2aG+1=0,
\qquad a=1-2r^2\sin^2(\theta/2).
\]

Requiring all resolvable modes to keep amplification modulus at most one gives `|r|≤1`. In 2D the condition becomes `r_x²+r_y²≤1`, hence `c Δt/h≤1/√2` on a square grid. The same derivation yields the numerical dispersion relation and shows why **stable does not mean accurate**.

---

<a id="es"></a>

# 🇪🇸 Español — mapa compacto

El objetivo es reconstruir CFL, no memorizarla. Descomponemos un error numérico en modos de Fourier

\[
e_j^n=G^n e^{ij\theta}.
\]

El operador de segunda diferencia multiplica cada modo por

\[
-4\sin^2(\theta/2).
\]

Al introducir el modo en el esquema de ondas aparece una ecuación para el factor de amplificación `G`. Exigir que ningún modo resoluble crezca sin límite produce `|r|≤1` en 1D y `r_x²+r_y²≤1` en 2D. En una malla cuadrada aparece así `1/√2`. Después estudiamos la dispersión numérica: **una simulación puede ser estable y aun así propagar la fase con un error sistemático**.

---

<a id="pt"></a>

# 🇵🇹 Português — mapa compacto

O objetivo é reconstruir a condição CFL em vez de apenas memorizá-la. Decompomos um erro numérico em modos de Fourier

\[
e_j^n=G^n e^{ij\theta}.
\]

O operador de segunda diferença multiplica cada modo por

\[
-4\sin^2(\theta/2).
\]

Ao inserir esse modo no esquema de ondas obtemos uma equação para o fator de amplificação `G`. Exigir que nenhum modo representável cresça sem limite produz `|r|≤1` em 1D e `r_x²+r_y²≤1` em 2D; numa malha quadrada surge `1/√2`. Em seguida aparece a dispersão numérica, lembrando que **estabilidade não significa exatidão**.
