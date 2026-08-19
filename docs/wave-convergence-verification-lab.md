# Wave Lab 3 — convergence, verification et crédibilité numérique

[🇫🇷 Français](#fr) · [🇬🇧 English](#en) · [🇪🇸 Español](#es) · [🇵🇹 Português](#pt)

> **Question de départ** : une simulation peut être stable et pourtant fausse. Comment vérifier que, lorsque l'on raffine la grille, la solution numérique se rapproche réellement de la solution de l'équation que nous prétendons résoudre ?

<a id="fr"></a>

# 🇫🇷 Français — version pédagogique détaillée

## 0. Le nouveau chemin de connaissance

Dans les deux premiers laboratoires, nous avons appris à faire apparaître une onde, puis à comprendre pourquoi un schéma peut exploser. Nous ajoutons maintenant une question plus exigeante : **si le calcul ne diverge pas, est-il pour autant digne de confiance ?**

```text
équation continue
      ↓
cas dont on connaît une solution exacte
      ↓
simulation sur une grille
      ↓
solution numérique ≠ solution exacte
      ↓
mesure d'erreur
      ↓
raffinement h, h/2, h/4, ...
      ↓
l'erreur diminue-t-elle ?
      ↓
à quelle vitesse ? ordre de convergence p
      ↓
stable mais encore trop grossier ?
      ↓
points par longueur d'onde + erreur de phase
      ↓
diagnostic d'énergie
      ↓
budget d'erreurs : modèle / numérique / données
      ↓
VERIFICATION : résout-on correctement les équations choisies ?
      ↓
VALIDATION : ces équations représentent-elles assez bien le monde réel ?
```

La phrase à conserver est :

> **Stabilité, convergence, précision et validité physique sont quatre questions différentes.**

---

## 1. Trois mots qu'il faut séparer : stabilité, vérification, validation

### Stabilité

La stabilité demande :

> « Une petite perturbation numérique reste-t-elle contrôlée lorsque l'on avance dans le temps ? »

Dans le Lab 2, nous avons relié cette question au facteur d'amplification `G`, puis à CFL.

Une simulation qui explose est inutilisable. Mais une simulation qui **n'explose pas** peut encore transporter une onde à la mauvaise vitesse, avec la mauvaise phase ou avec une résolution trop grossière.

### Vérification

La vérification demande :

> « Le code et le schéma résolvent-ils correctement les équations mathématiques que nous avons choisies ? »

Ici, nous allons utiliser une solution exacte connue. Si le maillage devient de plus en plus fin, la solution numérique doit s'en rapprocher selon un comportement prévisible.

### Validation

La validation demande autre chose :

> « Les équations choisies représentent-elles suffisamment bien le système physique réel pour la décision que nous voulons prendre ? »

Notre équation d'onde scalaire peut être parfaitement vérifiée numériquement et rester un modèle insuffisant d'une vague d'eau réelle. C'est précisément pour cela que Saint-Venant viendra **après** ce laboratoire.

---

## 2. Construire un cas où nous connaissons la réponse avant de lancer le code

Nous repartons de l'équation d'onde 1D :

\[
\frac{\partial^2 u}{\partial t^2}
=
c^2\frac{\partial^2u}{\partial x^2}.
\]

**Lecture en français :** « l'accélération temporelle de `u` est égale à `c²` fois sa courbure spatiale. »

Nous prenons un domaine

\[
0\le x\le L
\]

avec des murs de Neumann :

\[
\frac{\partial u}{\partial x}(0,t)=0,
\qquad
\frac{\partial u}{\partial x}(L,t)=0.
\]

**Lecture :** « la pente de `u` est nulle aux deux extrémités. »

Une famille de formes compatibles avec ces murs est

\[
\cos\left(\frac{m\pi x}{L}\right).
\]

Pourquoi ? Parce que la dérivée d'un cosinus est un sinus :

\[
\frac{d}{dx}
\cos\left(\frac{m\pi x}{L}\right)
=
-\frac{m\pi}{L}
\sin\left(\frac{m\pi x}{L}\right),
\]

et le sinus vaut zéro pour `x=0` et `x=L` lorsque `m` est entier.

Nous choisissons donc la solution exacte

\[
\boxed{
u(x,t)=
\cos(kx)\cos(ckt)
}
\]

avec

\[
k=\frac{m\pi}{L}.
\]

### Lecture en français

> « La forme spatiale est un cosinus fixé dans la cavité. Son amplitude monte et descend périodiquement dans le temps. »

C'est une onde stationnaire. Nous connaissons sa valeur **en tout point et à tout instant**. Elle devient donc notre règle de comparaison.

---

## 3. Pourquoi cette solution est-elle exacte ?

Calculons les deux dérivées secondes.

Dans le temps :

\[
u_{tt}
=
-(ck)^2\cos(kx)\cos(ckt).
\]

Dans l'espace :

\[
u_{xx}
=
-k^2\cos(kx)\cos(ckt).
\]

Donc

\[
c^2u_{xx}
=
-c^2k^2\cos(kx)\cos(ckt)
=
u_{tt}.
\]

L'équation est bien satisfaite.

### Lecture

> « Les deux côtés de l'équation produisent exactement la même fonction. Nous disposons donc d'une référence analytique indépendante du solveur numérique. »

C'est essentiel : nous ne comparons pas le code à lui-même.

---

## 4. Une erreur doit être mesurée, pas seulement regardée

À un instant final `T`, nous avons :

\[
u_{\text{exact}}(x,T)
\]

et

\[
u_{\text{num}}(x,T).
\]

L'erreur locale est

\[
e(x)=u_{\text{num}}(x,T)-u_{\text{exact}}(x,T).
\]

Mais une seule valeur maximale peut être sensible à un point particulier. Nous utiliserons aussi une norme de type `L2` :

\[
E
=
\left(
\frac1L
\int_0^L
|u_{\text{num}}-u_{\text{exact}}|^2dx
\right)^{1/2}.
\]

### Lecture en français

> « On calcule l'écart entre numérique et exact partout, on le met au carré pour empêcher les signes de s'annuler, on moyenne sur le domaine, puis on reprend une racine carrée pour revenir à l'échelle de `u`. »

Dans le code, l'intégrale est elle-même approximée par une somme pondérée sur les points de la grille.

---

## 5. Que veut dire « converger » ?

Notons

\[
h=\Delta x.
\]

Nous calculons plusieurs fois le même problème :

\[
h,
\qquad
\frac h2,
\qquad
\frac h4,
\qquad
\frac h8.
\]

Pour chaque grille, nous mesurons une erreur :

\[
E(h),
\quad
E(h/2),
\quad
E(h/4),
\ldots
\]

Un schéma convergent doit vérifier

\[
E(h)\to0
\qquad
\text{lorsque}
\qquad
h\to0.
\]

### Lecture

> « Si je rends la grille arbitrairement fine, la solution numérique doit se rapprocher de la solution de l'équation continue. »

Attention : cela ne dit toujours pas que l'équation continue décrit parfaitement la réalité. Cela vérifie le lien **numérique → mathématique**.

---

## 6. Pourquoi attendons-nous ici un ordre 2 ?

Notre seconde dérivée spatiale utilise

\[
\frac{u_{j+1}-2u_j+u_{j-1}}{\Delta x^2}.
\]

Son erreur locale dominante est proportionnelle à

\[
O(\Delta x^2).
\]

La seconde dérivée temporelle centrée est elle aussi d'ordre 2 :

\[
O(\Delta t^2).
\]

Nous choisissons un nombre de Courant à peu près constant, donc

\[
\Delta t\propto\Delta x.
\]

Ainsi les deux contributions décroissent quadratiquement avec la taille de maille. Nous nous attendons donc, dans le régime asymptotique, à

\[
\boxed{E(h)\approx C h^2.}
\]

### Lecture en français

> « Lorsque la maille devient deux fois plus petite, l'erreur devrait devenir environ quatre fois plus petite. »

Car

\[
\left(\frac h2\right)^2
=
\frac{h^2}{4}.
\]

---

## 7. Mesurer l'ordre au lieu de simplement croire qu'il vaut 2

Supposons plus généralement

\[
E(h)\approx C h^p.
\]

et

\[
E(h/2)\approx C(h/2)^p.
\]

En divisant :

\[
\frac{E(h)}{E(h/2)}
\approx
2^p.
\]

Donc

\[
\boxed{
p
\approx
\frac{\log(E(h)/E(h/2))}{\log 2}
}.
\]

### Lecture en français

> « J'observe combien l'erreur diminue quand je divise la maille par deux, et cette diminution me permet de reconstruire expérimentalement l'ordre du schéma. »

Si nous obtenons successivement quelque chose comme

```text
p = 1.7, 1.92, 1.98, 2.00
```

cela raconte une histoire très intéressante : les premières grilles n'étaient pas encore complètement dans le régime asymptotique, puis le comportement théorique d'ordre 2 apparaît progressivement.

C'est plus crédible qu'une seule valeur « p=2 » imprimée par le code.

---

## 8. Pourquoi faut-il raffiner l'espace ET le temps ?

Imaginez que nous divisons `dx` par 2 mais que nous gardons `dt` identique.

Deux choses peuvent alors arriver :

1. le nombre de Courant augmente et finit par violer CFL ;
2. même sans violation, l'erreur temporelle peut cesser de diminuer et masquer l'amélioration spatiale.

Dans ce laboratoire nous gardons approximativement

\[
r=\frac{c\Delta t}{\Delta x}
\]

constant.

### Lecture

> « Quand je raffine l'espace, je raffine aussi le temps proportionnellement. Ainsi je teste proprement le schéma espace-temps complet. »

Le code ajuste légèrement `dt` pour arriver **exactement** au même instant final `T` sur toutes les grilles. Cela évite de comparer des solutions évaluées à des instants différents.

---

## 9. Stable ne veut pas dire précis : les points par longueur d'onde

Une onde de nombre d'onde `k` possède une longueur d'onde

\[
\lambda=\frac{2\pi}{k}.
\]

Pour notre mode de Neumann

\[
k=\frac{m\pi}{L},
\]

on obtient

\[
\lambda=\frac{2L}{m}.
\]

Une mesure simple de résolution est

\[
\boxed{
N_\lambda=\frac{\lambda}{\Delta x}
}
\]

appelée ici **points par longueur d'onde**.

### Lecture

> « Combien de points de grille décrivent une oscillation spatiale complète ? »

Deux simulations peuvent toutes les deux respecter CFL, alors que :

- l'une possède 8 points par longueur d'onde ;
- l'autre en possède 80.

Elles sont toutes les deux stables, mais elles n'ont pas la même fidélité de phase.

Il n'existe pas un nombre universel de points par longueur d'onde valable pour tous les schémas et toutes les exigences. Ce laboratoire utilise `N_lambda` comme **diagnostic**, pas comme nouvelle formule magique.

---

## 10. Le lien direct avec le Lab 2 : dispersion numérique

Le Lab 2 a obtenu, pour ce schéma 1D,

\[
\sin\left(\frac{\omega_{\text{num}}\Delta t}{2}\right)
=
r
\sin\left(\frac{k\Delta x}{2}\right).
\]

La physique continue, elle, dit

\[
\omega=ck.
\]

Sauf cas particuliers, la fréquence numérique `omega_num` n'est donc pas exactement `ck`.

### Lecture en français

> « Le code peut faire osciller le bon motif spatial mais avec une fréquence légèrement fausse. À court terme la différence paraît minuscule ; après beaucoup de périodes, le déphasage peut devenir visible. »

C'est l'**erreur de phase**.

Voilà pourquoi une simulation peut :

- ne jamais exploser ;
- conserver une belle forme d'onde ;
- et pourtant être progressivement décalée par rapport à la solution exacte.

---

## 11. Une petite erreur de vitesse peut devenir une grande erreur de phase

Pour une onde progressive idéale :

\[
u(x,t)=A\cos(kx-\omega t).
\]

Si le code utilise en pratique

\[
\omega_{\text{num}}=\omega+\delta\omega,
\]

alors après un temps `t`, l'erreur de phase accumulée vaut environ

\[
\Delta\phi(t)
=
(\omega_{\text{num}}-\omega)t
=
\delta\omega\,t.
\]

### Lecture

> « Une petite erreur de fréquence est multipliée par le temps. Même un schéma stable et apparemment précis à court terme peut dériver en phase sur une simulation longue. »

C'est une idée extrêmement générale : en simulation dynamique, certaines petites erreurs **s'accumulent** au lieu de rester localisées.

---

## 12. L'énergie : une autre propriété à surveiller

Pour l'équation d'onde continue sans source, définissons

\[
E(t)
=
\frac12
\int_0^L
\left[
(u_t)^2+c^2(u_x)^2
\right]dx.
\]

Le premier terme ressemble à une énergie cinétique ; le second à une énergie de déformation.

### Lecture

> « L'énergie totale est la somme d'une partie liée à la vitesse du mouvement et d'une partie liée à la pente spatiale de la déformation. »

Pour voir pourquoi elle est conservée, multiplions l'équation

\[
u_{tt}=c^2u_{xx}
\]

par `u_t` et intégrons sur le domaine. Après intégration par parties, on obtient

\[
\frac{dE}{dt}
=
c^2[u_tu_x]_0^L.
\]

Avec des murs de Neumann,

\[
u_x=0
\]

aux extrémités, donc

\[
\boxed{\frac{dE}{dt}=0.}
\]

### Lecture

> « Aucune énergie ne traverse les murs dans ce modèle idéal ; l'énergie totale continue reste donc constante. »

### Attention numérique

Le notebook calcule une **approximation de l'énergie physique continue** avec des différences finies. Cette quantité peut légèrement osciller ou dériver. Ce n'est pas exactement l'invariant discret spécialisé du schéma leapfrog.

Nous l'utilisons donc comme **diagnostic de crédibilité**, pas comme preuve absolue de conservation.

---

## 13. Trois familles d'erreurs qu'il ne faut jamais confondre

### A. Erreur de modèle

Exemple : utiliser l'équation d'onde scalaire alors que le phénomène réel exige profondeur variable, gravité, non-linéarité ou dispersion physique.

```text
monde réel
   ↓ approximation physique
modèle PDE
```

Raffiner la grille ne corrige pas une mauvaise physique.

### B. Erreur numérique

Exemples :

- `dx` trop grand ;
- `dt` trop grand ;
- dispersion numérique ;
- approximation des frontières ;
- erreur d'arrondi ;
- solveur insuffisamment convergé.

```text
PDE
 ↓ discrétisation
solution numérique
```

Le raffinement et les études de convergence ciblent principalement cette famille.

### C. Erreur ou incertitude sur les données

Exemples :

- vitesse `c` mal connue ;
- position de source imprécise ;
- amplitude ou phase mesurée avec erreur ;
- condition initiale bruitée.

Même un solveur exact du bon modèle peut produire une mauvaise prédiction si ses données d'entrée sont fausses.

### La carte complète

```text
REALITE
  │
  │ erreur / hypothèse de modèle
  ▼
EQUATIONS
  │
  │ erreur numérique
  ▼
CALCUL
  ▲
  │
  │ incertitude / erreur de données
  │
MESURES / PARAMETRES
```

---

## 14. Une expérience particulièrement importante : raffiner ne corrige pas un mauvais paramètre

Nous allons volontairement simuler avec une vitesse

\[
c_{\text{num}}
\neq
c_{\text{référence}}.
\]

Puis nous raffinerons la grille.

Au début, l'erreur totale contient à la fois :

- une erreur de discrétisation ;
- une erreur de paramètre.

Quand `h` diminue, la première disparaît progressivement, mais la seconde reste.

### Lecture

> « Si l'erreur cesse de diminuer malgré le raffinement, cela peut signifier que le solveur n'est plus la principale source d'erreur. »

C'est une intuition capitale pour les systèmes réels : **plus de calcul n'améliore pas une hypothèse physique ou une donnée fausse.**

---

## 15. Richardson : utiliser le raffinement pour estimer ce que l'on ne connaît pas

Si

\[
u_h=u_*+Ch^p+\text{termes plus petits},
\]

et si nous connaissons `p`, deux grilles peuvent donner une meilleure estimation de la limite :

\[
\boxed{
u_{\text{ext}}
\approx
u_{h/2}
+
\frac{u_{h/2}-u_h}{2^p-1}
}
\]

pour un raffinement par facteur 2.

### Lecture

> « J'utilise la manière prévisible dont l'erreur décroît avec `h` pour extrapoler ce que donnerait une grille infiniment fine. »

Dans ce Lab 3, Richardson reste un **bonus avancé**. La priorité est d'abord de démontrer que nous sommes réellement dans un régime où `E≈Ch^p`.

---

## 16. Les 8 micro-expériences du notebook

### Expérience 1 — solution exacte connue

Tracer le mode analytique à plusieurs instants et vérifier visuellement la condition de Neumann.

**Question :** savons-nous ce que le code devrait produire avant de l'exécuter ?

### Expérience 2 — une grille unique : numérique contre exact

Superposer la solution numérique et la solution analytique à l'instant final.

**Question :** une courbe « jolie » suffit-elle ? Non : on calcule aussi l'erreur `L2`.

### Expérience 3 — raffinement `h, h/2, h/4, h/8`

Afficher l'erreur pour quatre grilles.

**Prédiction :** l'erreur doit décroître fortement.

### Expérience 4 — reconstruire l'ordre observé

Calculer

\[
p\approx\log(E_h/E_{h/2})/\log2.
\]

**Prédiction :** `p` doit tendre vers 2.

### Expérience 5 — stable mais grossier

Comparer plusieurs points par longueur d'onde à Courant stable.

**Prédiction :** aucune simulation n'explose, mais les plus grossières ont une erreur de phase beaucoup plus forte.

### Expérience 6 — laisser l'erreur de phase s'accumuler

Comparer court terme et long terme.

**Prédiction :** un petit écart de fréquence devient un déphasage visible après de nombreuses périodes.

### Expérience 7 — surveiller l'énergie

Tracer l'énergie physique approximée au cours du temps et son écart relatif.

**Prédiction :** pour un cas bien résolu et stable, elle reste proche de sa valeur initiale, avec de petites oscillations numériques.

### Expérience 8 — mauvais `c`, grille parfaite

Introduire une erreur volontaire sur la vitesse de propagation puis raffiner.

**Prédiction :** l'erreur finit par atteindre un plancher ; le raffinement numérique ne corrige pas le mauvais paramètre.

---

## 17. Le réflexe Diderot de vérification

Pour toute simulation numérique future, demander :

1. **Quelle équation suis-je réellement en train de résoudre ?**
2. **Ai-je un cas simple dont je connais la solution exacte ou une référence indépendante ?**
3. **Quelle norme d'erreur est pertinente ?**
4. **L'erreur tend-elle vers zéro quand je raffine ?**
5. **L'ordre mesuré correspond-il à l'ordre théorique attendu ?**
6. **Suis-je stable mais sous-résolu ?**
7. **Quelle propriété physique puis-je surveiller : énergie, masse, quantité de mouvement, positivité… ?**
8. **Si l'erreur ne diminue plus, est-ce encore une erreur numérique, ou ai-je atteint l'erreur de modèle / données ?**

---

## 18. Ce que nous saurons avant de passer à Saint-Venant

À la fin des trois laboratoires, notre arbre devient :

```text
PHENOMENE OBSERVE
      ↓
EQUATION D'ONDE
      ↓
DIFFERENCES FINIES
      ↓
CFL / STABILITE
      ↓
FOURIER / VALEURS PROPRES
      ↓
DISPERSION NUMERIQUE
      ↓
SOLUTION EXACTE DE REFERENCE
      ↓
ERREUR + RAFFINEMENT
      ↓
ORDRE DE CONVERGENCE
      ↓
ENERGIE / PROPRIETES
      ↓
VERIFICATION NUMERIQUE
      ↓
ERREUR MODELE vs NUMERIQUE vs DONNEES
      ↓
VALIDATION PHYSIQUE
      ↓
MODELE PLUS RICHE : SAINT-VENANT
```

Le passage à Saint-Venant ne sera donc pas « ajoutons une équation plus compliquée ». Il répondra à une question beaucoup plus propre :

> **Quelles propriétés des vagues d'eau notre modèle scalaire vérifié ne peut-il pas représenter, et quelle physique minimale faut-il ajouter ?**

---

<a id="en"></a>

# 🇬🇧 English — compact map

**Core distinction:** stable does not mean accurate; numerically verified does not mean physically validated.

```text
known exact PDE solution
→ numerical solution
→ error norm
→ grid refinement
→ observed order p
→ points per wavelength
→ phase error / dispersion
→ energy diagnostic
→ numerical verification
→ model/data/numerical error separation
→ physical validation
```

Main exact case:

\[
u(x,t)=\cos(kx)\cos(ckt),\qquad k=m\pi/L.
\]

Expected second-order convergence when `dt` scales with `dx`:

\[
E(h)\approx Ch^2,
\qquad
p\approx\frac{\log(E_h/E_{h/2})}{\log2}.
\]

Plain reading: **halve the mesh size; in the asymptotic regime the error should be roughly quartered.**

---

<a id="es"></a>

# 🇪🇸 Español — mapa compacto

**Distinción central:** estable no significa preciso; verificado numéricamente no significa validado físicamente.

```text
solución exacta conocida
→ solución numérica
→ norma de error
→ refinamiento de malla
→ orden observado p
→ puntos por longitud de onda
→ error de fase / dispersión
→ energía
→ verificación
→ separar error de modelo / numérico / datos
→ validación física
```

Caso exacto principal:

\[
u(x,t)=\cos(kx)\cos(ckt),\qquad k=m\pi/L.
\]

Si el método es de orden 2 y `dt` disminuye con `dx`:

\[
E(h)\approx Ch^2.
\]

Lectura: **si dividimos la malla por dos, esperamos aproximadamente cuatro veces menos error.**

---

<a id="pt"></a>

# 🇵🇹 Português — mapa compacto

**Distinção central:** estabilidade não é precisão; verificação numérica não é validação física.

```text
solução exata conhecida
→ solução numérica
→ norma do erro
→ refinamento da malha
→ ordem observada p
→ pontos por comprimento de onda
→ erro de fase / dispersão
→ energia
→ verificação
→ separar erro de modelo / numérico / dados
→ validação física
```

Caso exato principal:

\[
u(x,t)=\cos(kx)\cos(ckt),\qquad k=m\pi/L.
\]

Para um método de segunda ordem com `dt` proporcional a `dx`:

\[
E(h)\approx Ch^2.
\]

Leitura: **reduzir a malha pela metade deve, no regime assintótico, reduzir o erro aproximadamente por um fator quatro.**
