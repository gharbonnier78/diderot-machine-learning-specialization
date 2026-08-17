# Wave Equation Toy Lab — du phénomène observé au schéma numérique

[🇫🇷 Français](#fr) · [🇬🇧 English](#en) · [🇪🇸 Español](#es) · [🇵🇹 Português](#pt)

> **But du laboratoire** : ne pas seulement « faire tourner une animation ». Nous voulons reconstruire le chemin de pensée qui relie une observation physique à une équation, puis à une approximation numérique, puis à une expérience contrôlée.
>
> Ce laboratoire utilise l'équation d'onde **scalaire**. C'est un excellent modèle pédagogique de propagation, réflexion et interférence. Ce n'est pas encore un modèle complet de fluide comme Saint-Venant, Boussinesq ou Navier–Stokes.

<a id="fr"></a>

# 🇫🇷 Français — version pédagogique détaillée

## 0. La carte mentale avant les équations

Le fil directeur est :

```text
observation d'une perturbation
        ↓
une grandeur varie dans l'espace et le temps : u(x,t) ou u(x,y,t)
        ↓
la perturbation se propage
        ↓
équation d'onde
        ↓
source + conditions initiales + conditions aux limites
        ↓
l'ordinateur ne connaît pas les dérivées
        ↓
discrétisation de l'espace et du temps
        ↓
schéma aux différences finies
        ↓
question de stabilité
        ↓
condition CFL / analyse de Von Neumann
        ↓
simulation, visualisation, validation et expériences
```

Chaque expérience ajoute **une seule idée principale**. Le code doit rester lisible comme une traduction de la formule.

---

## 1. Expérience 1 — une impulsion 1D se sépare et se propage

### Question physique

Si je déforme localement une corde puis je la relâche, que se passe-t-il ?

On décrit la déformation par une fonction

\[
u(x,t).
\]

**Lecture en français :** « `u` est la valeur de la déformation au point `x` et à l'instant `t`. »

Le modèle le plus simple est

\[
\frac{\partial^2 u}{\partial t^2}=c^2\frac{\partial^2 u}{\partial x^2}.
\]

**Lecture en français :** « l'accélération temporelle de la déformation est proportionnelle à la courbure spatiale de la corde ; la constante `c` règle la vitesse de propagation. »

Une bosse locale peut être choisie sous forme gaussienne :

\[
u(x,0)=A\exp\!\left[-\frac{(x-x_0)^2}{2\sigma^2}\right].
\]

**Lecture :** « au départ, on crée une bosse centrée en `x0`, d'amplitude `A` et de largeur contrôlée par `sigma`. »

Si la vitesse initiale est nulle, cette bosse se décompose naturellement en deux contributions qui partent en sens opposés. C'est une première manifestation du fait que l'équation d'onde est une équation de **propagation**, pas de simple lissage.

### À observer

- deux fronts partent à gauche et à droite ;
- leur vitesse dépend de `c` ;
- tant qu'ils n'atteignent pas les bords, la forme reste reconnaissable ;
- en changeant `sigma`, on change le contenu fréquentiel de l'impulsion.

### Intuition importante

Comparer avec l'équation de diffusion

\[
\frac{\partial u}{\partial t}=D\frac{\partial^2u}{\partial x^2}.
\]

**Lecture :** « la vitesse de variation de `u` dépend de la courbure spatiale. »

La diffusion a tendance à **étaler** la bosse ; l'équation d'onde a tendance à la **transporter**.

---

## 2. Expérience 2 — une source sinusoïdale 1D crée un train d'ondes

Au lieu de seulement définir une forme au temps initial, on force continuellement un point :

\[
\frac{\partial^2u}{\partial t^2}=c^2\frac{\partial^2u}{\partial x^2}+S(x,t).
\]

On prend par exemple

\[
S(x,t)=A\sin(\omega t)\,\delta(x-x_0).
\]

**Lecture :** « une source située en `x0` pousse périodiquement le système avec une amplitude `A` et une pulsation `omega`. »

La fréquence ordinaire vaut

\[
f=\frac{\omega}{2\pi}.
\]

Et pour une onde simple,

\[
c=f\lambda.
\]

**Lecture :** « la vitesse de l'onde est égale à la fréquence multipliée par la longueur d'onde. »

Donc, si `c` reste fixe et si on augmente `f`, la longueur d'onde `lambda` diminue.

### À manipuler

- doubler `f` ;
- diviser `c` par deux ;
- augmenter `A` ;
- regarder séparément ce qui change : vitesse, espacement des crêtes, amplitude.

---

## 3. Expérience 3 — deux sources 1D : la phase fabrique l'interférence

On additionne deux sources :

\[
S=S_1+S_2.
\]

Par exemple :

\[
S_1=A\sin(\omega t)\delta(x-x_1),
\]

\[
S_2=A\sin(\omega t+\phi)\delta(x-x_2).
\]

La nouvelle grandeur est `phi`, le **déphasage**.

- `phi = 0` : les sources oscillent ensemble ;
- `phi = pi` : quand l'une monte, l'autre descend ;
- entre les deux : interférence partielle.

L'identité

\[
\sin(\omega t)+\sin(\omega t+\phi)
=2\cos\left(\frac{\phi}{2}\right)
\sin\left(\omega t+\frac{\phi}{2}\right)
\]

montre directement que l'amplitude résultante dépend du déphasage.

**Lecture :** « deux oscillations de même fréquence s'additionnent en une nouvelle oscillation dont l'amplitude est multipliée par `2 cos(phi/2)`. »

### Idée centrale

L'interférence n'est pas une nouvelle force mystérieuse. Dans un modèle linéaire, elle vient de la règle extrêmement simple

\[
u=u_1+u_2.
\]

**Lecture :** « l'onde totale est la somme locale des ondes présentes. »

---

## 4. Expérience 4 — passer en 2D : une source ponctuelle crée des fronts circulaires

En deux dimensions :

\[
\frac{\partial^2u}{\partial t^2}
=c^2\left(
\frac{\partial^2u}{\partial x^2}
+
\frac{\partial^2u}{\partial y^2}
\right)+S(x,y,t).
\]

Le terme entre parenthèses est le **Laplacien** :

\[
\Delta u=u_{xx}+u_{yy}.
\]

**Lecture :** « le Laplacien mesure comment la valeur en un point se compare, via sa courbure, à son voisinage spatial. »

Dans un milieu homogène et isotrope, aucune direction n'est privilégiée : une source ponctuelle produit donc des fronts approximativement circulaires.

### À observer

- isotropie du phénomène physique ;
- petites anisotropies numériques possibles liées au maillage carré ;
- rôle de la résolution spatiale.

C'est déjà une première leçon d'ingénierie numérique : **le modèle physique peut être isotrope alors que la grille de calcul ne l'est pas parfaitement.**

---

## 5. Expérience 5 — deux sources 2D : apparition des franges d'interférence

On place maintenant deux vibreurs de même fréquence. En chaque point du domaine, la valeur observée résulte de la somme des contributions des deux sources.

Pour des sources cohérentes, une manière simple de raisonner consiste à regarder la différence de trajet

\[
\Delta r=r_2-r_1.
\]

Interférence constructive approximative lorsque

\[
\Delta r=k\lambda,
\]

où `k` est entier.

**Lecture :** « les deux ondes arrivent en phase si la différence de distance parcourue vaut un nombre entier de longueurs d'onde. »

Interférence destructive approximative lorsque

\[
\Delta r=\left(k+\frac12\right)\lambda.
\]

**Lecture :** « elles arrivent en opposition de phase si la différence de trajet vaut un demi-multiple impair de la longueur d'onde. »

L'animation montre alors des zones qui oscillent fortement et d'autres qui restent presque calmes : les **franges**.

### Expérience contrôlée

Faire varier une seule chose à la fois :

1. distance entre les deux sources ;
2. fréquence ;
3. phase relative ;
4. amplitude relative.

Puis prédire qualitativement le résultat **avant** de lancer le code.

---

## 6. Expérience 6 — un mur réfléchissant : l'onde rencontre sa propre histoire

Une simulation n'est pas définie seulement par une équation. Il faut aussi dire ce qui se passe aux frontières.

Une condition de Neumann homogène est

\[
\frac{\partial u}{\partial n}=0.
\]

**Lecture :** « lorsqu'on se déplace dans la direction normale au bord, la valeur de `u` n'a localement pas de pente. »

Dans ce toy model, cette condition donne un bord réfléchissant. L'onde incidente revient et s'additionne à l'onde encore présente.

Le motif peut donc devenir complexe même avec **une seule source**, car on obtient

\[
\text{onde directe}+\text{onde réfléchie}+\text{réflexions suivantes}.
\]

C'est un point essentiel pour interpréter les images du post LinkedIn ayant inspiré ce laboratoire : un motif d'interférence complexe ne prouve pas qu'il y avait deux sources physiques.

### Comparaison utile

- Neumann : pente normale nulle ;
- Dirichlet : `u = 0` au bord ;
- bord absorbant : cherche à laisser sortir l'énergie avec un minimum de réflexion ;
- périodique : ce qui sort d'un côté revient de l'autre.

Le choix de frontière fait partie du **modèle physique**.

---

## 7. Expérience 7 — cavité fermée : des motifs privilégiés, les modes propres

Dans une boîte rectangulaire réfléchissante, toutes les formes spatiales ne se comportent pas de la même manière. Certaines formes sont reproduites par la dynamique, à un facteur temporel près : ce sont les **modes propres**.

Pour des conditions de Neumann dans un rectangle de dimensions `Lx` et `Ly`, une famille de formes est

\[
\phi_{mn}(x,y)=
\cos\left(\frac{m\pi x}{L_x}\right)
\cos\left(\frac{n\pi y}{L_y}\right).
\]

**Lecture :** « le mode `(m,n)` contient `m` variations structurées selon `x` et `n` selon `y`, compatibles avec une pente normale nulle aux murs. »

Sa pulsation propre est

\[
\omega_{mn}=c\pi
\sqrt{
\left(\frac{m}{L_x}\right)^2+
\left(\frac{n}{L_y}\right)^2
}.
\]

**Lecture :** « la fréquence naturelle augmente lorsque le mode varie plus rapidement dans l'espace, ou lorsque la cavité devient plus petite. »

### Pourquoi c'est important au-delà des vagues

Ici apparaît le pont vers :

```text
équation différentielle
   ↓
opérateur spatial
   ↓
valeurs propres / vecteurs propres
   ↓
modes propres
   ↓
décomposition spectrale
   ↓
Fourier, vibrations, acoustique, mécanique, électromagnétisme
```

C'est la même idée mathématique générale que l'on retrouve derrière de nombreux problèmes de systèmes dynamiques et d'algèbre linéaire.

---

## 8. Expérience 8 — violer volontairement CFL et regarder le calcul devenir instable

L'ordinateur ne manipule ni temps continu ni espace continu. On remplace les dérivées par des différences.

En 1D :

\[
\frac{\partial^2u}{\partial x^2}
\approx
\frac{u_{i+1}^n-2u_i^n+u_{i-1}^n}{\Delta x^2}.
\]

**Lecture :** « la courbure spatiale au point `i` est estimée à partir de la valeur du point, de son voisin gauche et de son voisin droit. »

Dans le temps :

\[
\frac{\partial^2u}{\partial t^2}
\approx
\frac{u_i^{n+1}-2u_i^n+u_i^{n-1}}{\Delta t^2}.
\]

**Lecture :** « l'accélération temporelle est estimée à partir de trois instants : précédent, courant et suivant. »

Après réarrangement, en 1D :

\[
u_i^{n+1}
=2u_i^n-u_i^{n-1}
+r^2\left(u_{i+1}^n-2u_i^n+u_{i-1}^n\right)
+\Delta t^2 S_i^n,
\]

avec

\[
r=\frac{c\Delta t}{\Delta x}.
\]

**Lecture :** « la valeur future est calculée avec les deux états temporels précédents et la courbure spatiale actuelle. Le nombre `r` compare la distance physique parcourue pendant un pas de temps à la taille d'une maille. »

En 1D, pour ce schéma explicite classique, la condition est

\[
\frac{c\Delta t}{\Delta x}\le 1.
\]

En 2D :

\[
c^2\Delta t^2
\left(
\frac{1}{\Delta x^2}+\frac{1}{\Delta y^2}
\right)
\le 1.
\]

Sur une grille carrée `dx = dy = h` :

\[
\frac{c\Delta t}{h}\le\frac{1}{\sqrt2}.
\]

**Lecture :** « en deux dimensions, le pas de temps doit être encore plus petit relativement à la maille ; sinon les erreurs numériques peuvent être amplifiées à chaque itération. »

### Pourquoi faire exprès de casser le modèle ?

Parce qu'une expérience scientifique ne consiste pas seulement à montrer le cas qui marche. On compare :

- un cas juste sous la limite CFL ;
- un cas juste au-dessus ;
- la croissance de `max(abs(u))` au cours du temps.

On voit alors qu'une animation peut devenir physiquement absurde **non parce que l'équation d'onde est fausse, mais parce que son approximation numérique est instable**.

C'est le point d'entrée naturel vers l'analyse de Von Neumann : on étudie comment le schéma amplifie ou atténue des composantes de Fourier d'un pas de temps au suivant.

---

## 9. Pourquoi les différences finies ressemblent à la physique locale

Le schéma 2D fait quelque chose de remarquablement simple. Chaque cellule regarde essentiellement :

```text
                voisin haut
                    |
voisin gauche -- cellule -- voisin droit
                    |
                voisin bas
```

Elle utilise aussi son propre état au pas de temps précédent.

Une règle locale répétée des milliers de fois produit :

- propagation ;
- réflexion ;
- interférence ;
- modes stationnaires ;
- motifs globaux complexes.

Cette relation « règle locale simple → organisation globale complexe » est un motif intellectuel que l'on retrouvera dans beaucoup d'autres domaines.

---

## 10. Ce que ce toy model ne prétend pas représenter

Une vague d'eau réelle peut demander davantage de physique : profondeur, gravité, non-linéarité, dispersion, viscosité, turbulence, surface libre, interaction avec un fond variable, etc.

Une hiérarchie utile est :

```text
équation d'onde scalaire
        ↓
modèles d'ondes en eau peu profonde / Saint-Venant
        ↓
modèles dispersifs de type Boussinesq
        ↓
Navier–Stokes + surface libre selon le niveau de fidélité recherché
```

Le bon modèle n'est pas « l'équation la plus compliquée ». C'est **le modèle le plus simple qui conserve les phénomènes nécessaires à la question posée**.

---

## 11. Arbre de connaissances à conserver dans Diderot ML

```text
OBSERVATION
  perturbation, vibration, vague, son
        │
        ▼
VARIABLE D'ÉTAT
  u(x,t), u(x,y,t)
        │
        ▼
DYNAMIQUE CONTINUE
  équation d'onde / PDE
        │
        ├── source S
        ├── conditions initiales
        └── conditions aux limites
        │
        ▼
DISCRÉTISATION
  grille spatiale + pas de temps
        │
        ▼
DIFFÉRENCES FINIES
  dérivées → différences de voisins
        │
        ▼
STABILITÉ NUMÉRIQUE
  Von Neumann → CFL
        │
        ▼
EXPÉRIENCE
  impulsion → oscillateur → 2 sources → 2D → réflexion → modes → rupture CFL
        │
        ▼
PONTS
  Fourier · algèbre linéaire · valeurs propres · signal · systèmes dynamiques
  automatique · simulation · estimation · optimisation · ML scientifique
```

### Réflexe Diderot

Pour chaque nouvelle formule, se poser cinq questions :

1. **Que représente chaque symbole physiquement ?**
2. **Comment relire la formule en français courant ?**
3. **Quelle hypothèse permet d'écrire cette formule ?**
4. **Comment l'ordinateur l'approxime-t-il ?**
5. **Quelle expérience pourrait la réfuter ou montrer sa limite ?**

---

## 12. Ordre d'exécution recommandé

Le notebook compagnon implémente les huit expériences dans cet ordre :

1. impulsion 1D ;
2. source sinusoïdale 1D ;
3. deux sources 1D et phase ;
4. source ponctuelle 2D ;
5. deux sources 2D et franges ;
6. réflexion sur les bords ;
7. mode propre d'une cavité ;
8. test volontaire de la limite CFL.

Ne pas seulement exécuter : **prédire avant chaque cellule**, puis confronter la prédiction à l'animation.

---

<a id="en"></a>

# 🇬🇧 English — compact guide

The lab follows one chain of reasoning: observed disturbance → state variable `u` → wave PDE → sources and boundaries → spatial/time discretization → finite differences → stability → CFL → controlled experiment.

The governing scalar model is

\[
u_{tt}=c^2\Delta u+S.
\]

Read it as: **the local acceleration of the field is driven by its spatial curvature plus an external source**. The eight experiments are: 1D pulse, 1D harmonic source, two 1D sources and phase, 2D circular propagation, two-source interference, reflecting boundaries, cavity eigenmodes, and intentional CFL violation.

The 2D stability condition used in the notebook is

\[
c^2\Delta t^2\left(\frac1{\Delta x^2}+\frac1{\Delta y^2}\right)\le1.
\]

On a square grid this becomes `c dt / h <= 1/sqrt(2)`.

The central learning habit is: for every equation, identify the physical meaning of every symbol, say the equation in ordinary language, state its assumptions, show how the computer approximates it, and design an experiment that exposes its limits.

---

<a id="es"></a>

# 🇪🇸 Español — guía compacta

El laboratorio reconstruye el camino completo: observación de una perturbación → variable de estado `u` → ecuación de ondas → fuentes y condiciones de frontera → discretización → diferencias finitas → estabilidad → condición CFL → experimento controlado.

El modelo escalar es

\[
u_{tt}=c^2\Delta u+S.
\]

Se puede leer así: **la aceleración local del campo depende de su curvatura espacial y de una fuente externa**.

Los ocho experimentos son: pulso 1D, fuente sinusoidal 1D, dos fuentes 1D y fase, propagación circular 2D, interferencia de dos fuentes, reflexión en los bordes, modos propios de una cavidad y violación voluntaria de CFL.

La idea pedagógica principal es no memorizar fórmulas aisladas: para cada ecuación hay que explicar los símbolos, traducirla a lenguaje común, identificar las hipótesis, entender su aproximación numérica y buscar un caso que muestre sus límites.

---

<a id="pt"></a>

# 🇵🇹 Português — guia compacto

O laboratório reconstrói o percurso completo: observação de uma perturbação → variável de estado `u` → equação de onda → fontes e condições de contorno → discretização → diferenças finitas → estabilidade → condição CFL → experiência controlada.

O modelo escalar é

\[
u_{tt}=c^2\Delta u+S.
\]

Leitura intuitiva: **a aceleração local do campo depende da sua curvatura espacial e de uma fonte externa**.

As oito experiências são: pulso 1D, fonte harmónica 1D, duas fontes 1D e fase, propagação circular 2D, interferência entre duas fontes, reflexão nas fronteiras, modos próprios de uma cavidade e violação intencional da condição CFL.

O hábito pedagógico central é sempre perguntar: o que significam os símbolos, como dizer a fórmula em linguagem comum, quais hipóteses foram feitas, como o computador aproxima a equação e que experiência pode mostrar os limites do modelo.
