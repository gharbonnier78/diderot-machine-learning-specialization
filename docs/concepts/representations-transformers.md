# Representations, attention et Transformer

## 1. Question de depart

Un reseau de neurones classique peut recevoir un vecteur fixe et calculer une sortie. Mais de nombreux
problemes ont une structure interne : une phrase contient plusieurs mots, une image contient plusieurs
regions, une trajectoire contient plusieurs observations et actions.

La question devient alors :

> Comment construire une representation de chaque element en tenant compte des autres elements pertinents ?

Le Transformer apporte une reponse generale fondee sur l'attention. Il est aujourd'hui associe aux
LLM, mais le mecanisme est plus general : les elements manipules peuvent etre des tokens de texte,
des patches d'image, des segments audio ou d'autres representations vectorielles.

La chaine conceptuelle etudiee ici est :

`signal brut -> tokenisation -> token -> embedding -> position -> Q/K/V -> attention -> representation contextualisee -> bloc Transformer -> representation latente -> sortie`.

---

## 2. Token : une unite de calcul, pas necessairement un objet du monde

### Intuition

Un modele ne manipule pas directement une phrase, une image ou un objet physique. Il faut d'abord
choisir des unites elementaires.

Pour le texte, une tokenisation peut produire des mots, sous-mots ou caracteres. Pour une image de
Vision Transformer, on decoupe generalement l'image en patches. Dans les deux cas, le token est une
**unite manipulee par le modele**.

### Confusion importante

`objet semantique != token`.

Un token d'image peut ne contenir qu'un morceau de chaise. Un mot rare peut etre decompose en
plusieurs sous-tokens. La semantique n'est donc pas necessairement presente dans le decoupage initial ;
elle peut emerger progressivement dans les representations apprises.

---

## 3. Embedding : passer d'une unite discrete a un vecteur

Un token indexe `t_i` est transforme en vecteur :

\[
t_i \longrightarrow x_i \in \mathbb{R}^{d_{model}}.
\]

Pour un vocabulaire textuel, cette operation peut etre vue comme la selection d'une ligne dans une
matrice d'embedding apprise. Pour un patch d'image, le patch aplati peut etre projete par une
transformation lineaire dans le meme espace vectoriel.

### Token versus embedding

- **token** : unite ou indice ;
- **embedding** : vecteur numerique associe a cette unite ;
- **representation contextualisee** : vecteur obtenu apres interaction avec le contexte.

Ces trois niveaux ne doivent pas etre confondus.

---

## 4. Position : l'ordre doit etre represente

Une self-attention pure compare des vecteurs sans connaitre naturellement leur ordre dans la sequence.
Le modele doit donc recevoir une information de position, ajoutee ou integree aux representations.

Schema conceptuel :

\[
\tilde{x}_i = x_i + p_i,
\]

où `p_i` represente la position. Les architectures modernes utilisent plusieurs familles de methodes
(position absolue, relative, embeddings rotatifs, etc.). Le point pedagogique essentiel est plus simple :
**la relation entre elements ne suffit pas a elle seule a coder l'ordre**.

---

## 5. Query, Key, Value : trois roles pour un meme element

A partir d'une representation `x_i`, le modele calcule trois projections :

\[
q_i = x_i W_Q, \qquad k_i = x_i W_K, \qquad v_i = x_i W_V.
\]

En forme matricielle :

\[
Q = XW_Q, \qquad K = XW_K, \qquad V = XW_V.
\]

Les matrices `W_Q`, `W_K` et `W_V` sont des **parametres appris**. Les matrices `Q`, `K` et `V`
sont des **activations calculees pour l'entree courante**.

### Intuition fonctionnelle

- **Query** : quel type d'information cet element cherche-t-il ?
- **Key** : dans quelle mesure cet element correspond-il a une requete ?
- **Value** : quelle information cet element transmet-il lorsqu'il est retenu ?

Il ne faut pas prendre cette metaphore comme une definition semantique rigide. `Q`, `K` et `V` sont
d'abord des projections vectorielles apprises permettant de calculer un routage differentiable de
l'information.

---

## 6. Produit scalaire : mesurer une compatibilite

Pour l'element `i`, on compare sa query a la key de chaque element `j` :

\[
s_{ij} = q_i^\top k_j.
\]

Un produit scalaire eleve indique ici une forte compatibilite dans l'espace appris. Ce mecanisme
reutilise donc une notion d'algebre lineaire tres generale : le produit scalaire n'est pas seulement
une formule ; il mesure un alignement relatif entre vecteurs.

---

## 7. Scaled dot-product attention

Les scores sont divises par `\sqrt{d_k}` puis normalises :

\[
\alpha_{ij}
= \operatorname{softmax}_j\left(\frac{q_i^\top k_j}{\sqrt{d_k}}\right).
\]

La sortie associee a la position `i` devient :

\[
z_i = \sum_j \alpha_{ij} v_j.
\]

En forme matricielle :

\[
\operatorname{Attention}(Q,K,V)
= \operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V.
\]

### Pourquoi diviser par `\sqrt{d_k}` ?

Quand la dimension augmente, le produit scalaire peut naturellement atteindre des valeurs de plus
grande amplitude. Sans mise a l'echelle, le softmax peut devenir tres sature, produisant des gradients
peu favorables a l'optimisation. La division controle cette echelle.

### Ce que fait le softmax ici

Le softmax ne sert pas uniquement a produire des probabilites de classe. Ici, il transforme une ligne
de scores de compatibilite en poids positifs dont la somme vaut 1. Il construit donc une combinaison
ponderee des `Value`.

---

## 8. Exemple minimal calculable a la main

Prenons deux elements avec :

\[
q_1 = (1,0),\qquad k_1=(1,0),\qquad k_2=(0,1).
\]

Alors :

\[
q_1^\top k_1 = 1, \qquad q_1^\top k_2 = 0.
\]

Si `d_k=2`, les scores mis a l'echelle sont :

\[
(1/\sqrt{2},\;0).
\]

Apres softmax, le premier poids est superieur au second. Si :

\[
v_1=(10,0),\qquad v_2=(0,10),
\]

alors la sortie `z_1` sera une combinaison des deux vecteurs, mais davantage orientee vers `v_1`.

Le mecanisme complet peut donc etre lu ainsi :

`comparaison Q-K -> poids -> melange des V`.

---

## 9. Self-attention : les elements d'une meme sequence se contextualisent

On parle de **self-attention** lorsque `Q`, `K` et `V` proviennent de la meme collection de
representations `X`.

Avant attention, `x_i` represente principalement l'element local et son encodage initial. Apres
attention :

\[
z_i = \sum_j \alpha_{ij}v_j,
\]

la representation de `i` contient une information choisie dynamiquement parmi les autres positions.

C'est le passage conceptuel :

`representation locale -> representation relationnelle/contextualisee`.

---

## 10. Multi-head attention : plusieurs espaces relationnels

Au lieu d'une seule projection `Q,K,V`, le modele utilise plusieurs tetes :

\[
\text{head}_h = \operatorname{Attention}(XW_Q^{(h)}, XW_K^{(h)}, XW_V^{(h)}).
\]

Les sorties sont concatenees puis reprojetees. Chaque tete dispose de ses propres parametres et peut
apprendre des relations differentes.

Attention a une interpretation trop litterale : on ne peut pas supposer qu'une tete correspondra
necessairement a une relation humaine simple comme « sujet-verbe » ou « contour d'objet ». Certaines
tetes peuvent etre specialisees, redondantes, distribuees ou difficiles a interpreter.

---

## 11. Le bloc Transformer ne se reduit pas a l'attention

Un bloc comporte typiquement :

1. attention ;
2. connexion residuelle ;
3. normalisation ;
4. reseau feed-forward positionnel ;
5. nouvelle connexion residuelle et normalisation.

Une ecriture abstraite est :

\[
X' = \operatorname{Norm}(X + \operatorname{Attention}(X)),
\]

puis :

\[
X'' = \operatorname{Norm}(X' + \operatorname{MLP}(X')).
\]

Les details exacts de placement de la normalisation varient selon les architectures.

### Pourquoi l'MLP reste important

L'attention melange l'information entre positions. L'MLP applique ensuite une transformation non
lineaire a chaque position. On peut donc retenir :

- attention : **interaction entre elements** ;
- MLP : **transformation locale de la representation**.

---

## 12. Empiler les blocs : de l'embedding a la representation latente

Soit :

\[
X^{(0)} = \text{embeddings + positions}.
\]

Apres plusieurs blocs :

\[
X^{(0)} \to X^{(1)} \to \cdots \to X^{(L)}.
\]

Le vecteur `x_i^{(L)}` n'est plus simplement l'embedding du token initial. Il est une
**representation latente contextualisee**, construite par l'ensemble des transformations du modele.

C'est une distinction essentielle pour lire les travaux modernes :

`embedding initial != hidden representation != latent state garanti suffisant`.

---

## 13. Encoder, decoder et encoder-decoder

Le Transformer original utilise un encodeur et un decodeur.

- **encoder-only** : produit des representations contextualisees de l'entree ;
- **decoder-only** : construit autoregressivement une sortie, avec attention masquee pour ne pas voir
  les tokens futurs ;
- **encoder-decoder** : encode une entree puis genere une sortie conditionnee par cette representation.

BERT est un exemple classique d'architecture encoder-only ; GPT est decoder-only. Cette distinction
architecturale est plus fondamentale que l'etiquette « LLM ».

---

## 14. Transformer versus LLM

Un Transformer est une **famille d'architectures**. Un LLM est un **modele de langage de grande taille**,
souvent construit avec une architecture Transformer decoder-only.

Ainsi :

`Transformer != LLM`.

La meme idee architecturale peut traiter du texte, de la vision, de l'audio, des series temporelles ou
des trajectoires.

---

## 15. Patch token : appliquer la meme logique a l'image

Une image peut etre decoupee en patches :

\[
I \to (P_1, P_2, \ldots, P_N).
\]

Chaque patch est projete en vecteur :

\[
P_i \to x_i.
\]

Le Transformer peut alors traiter la collection de patches comme une sequence de tokens. Un patch
n'est pas necessairement un objet ; la representation semantique d'une region peut emerger apres les
interactions entre patches et les couches successives.

---

## 16. Token `[CLS]` : construire une representation globale

Certaines architectures ajoutent un token special `[CLS]` a la sequence. Apres plusieurs blocs, sa
representation finale peut etre utilisee comme resume global de l'entree pour une tache de
classification ou une autre supervision globale.

Point pedagogique important : si seule la representation `[CLS]` est directement supervisee, cela
n'implique pas que les autres tokens n'apprennent rien. Les gradients traversent le reseau et les
representations locales peuvent developper une structure utile a la tache globale.

---

## 17. Geometrie des representations et PCA

Supposons que le modele produise des representations finales :

\[
h_1, h_2, \ldots, h_N \in \mathbb{R}^d.
\]

On peut appliquer une PCA a ces vecteurs pour etudier leur geometrie dans un espace de dimension
reduite.

Ici, la PCA porte sur les **activations ou representations produites par le modele**, pas necessairement
sur ses poids. On peut alors rechercher :

- groupes ;
- directions dominantes ;
- separation entre categories ;
- structure spatiale ou semantique emergente.

Une visualisation PCA suggestive n'est toutefois pas une preuve suffisante qu'un concept humain precis
est « code » dans une dimension. Elle constitue une observation exploratoire a completer par des tests,
comparaisons et ablations.

---

## 18. Hidden state, latent representation et state representation

Ces mots se ressemblent mais ne garantissent pas la meme chose.

- **hidden representation** : activation interne non directement observee ;
- **latent representation** : variable ou vecteur interne representant certains facteurs de l'entree ;
- **state representation** : representation destinee a resumer l'etat pertinent d'un processus ;
- **sufficient state** : representation contenant toute l'information necessaire a la prediction ou a
  la decision consideree.

Un Transformer produit naturellement des hidden/latent representations. Il ne garantit pas, par son
architecture seule, qu'elles constituent un etat suffisant d'un systeme dynamique.

---

## 19. Pont vers MDP et POMDP

Dans un MDP, l'etat `S_t` satisfait une propriete de Markov : le futur pertinent depend de l'etat courant
et de l'action, pas de tout l'historique une fois l'etat connu.

Dans un POMDP, l'etat reel n'est pas directement observe. Un belief state ideal est une distribution :

\[
b_t(s) = P(S_t=s \mid h_t),
\]

où `h_t` represente l'historique d'observations et d'actions disponible.

Un encodeur neuronal peut apprendre une compression :

\[
z_t = f_\theta(h_t).
\]

Mais `z_t` n'est un bon etat que s'il conserve l'information necessaire pour la tache. Une exigence
predictive possible est :

\[
P(o_{t+1}, r_{t+1} \mid h_t, a_t)
\approx
P(o_{t+1}, r_{t+1} \mid z_t, a_t).
\]

La distinction a retenir est donc :

`representation contextualisee != belief state`.

Le Transformer peut servir d'architecture a un estimateur d'etat ; il n'apporte pas a lui seul la
propriete de suffisance.

---

## 20. Pont vers JEPA et world models

Une representation latente devient particulierement interessante lorsqu'on ne veut plus seulement
classifier ou generer, mais **predire la dynamique du monde dans un espace de representation**.

Schema conceptuel :

\[
o_t \xrightarrow{encoder} z_t,
\]

puis :

\[
(z_t, a_t) \xrightarrow{modele\ dynamique} \hat{z}_{t+1}.
\]

Un world model complet peut combiner plusieurs composants :

- encodeur / representation d'etat ;
- dynamique latente ;
- modele d'observation ou decodeur selon l'architecture ;
- reward/value/policy selon l'objectif.

Les approches JEPA deplacent l'accent vers la prediction dans l'espace des representations plutot que
vers la reconstruction detaillee de toutes les observations. Cette idee doit etre etudiee separement :
un Transformer peut etre un composant d'un JEPA ou d'un world model, mais ces concepts ne sont pas
synonymes.

---

## 21. Ce qui est appris et ce qui depend de l'entree

Cette distinction est utile pour ne pas confondre « poids » et « representations ».

### Parametres appris pendant l'entrainement

Par exemple :

\[
W_Q, W_K, W_V, W_O, W_{MLP}, \text{embeddings appris}, \ldots
\]

### Valeurs calculees pour une entree donnee

Par exemple :

\[
X, Q, K, V, \alpha, Z, X^{(1)}, \ldots, X^{(L)}.
\]

Les secondes changent lorsque l'entree change, meme si les poids du modele restent fixes.

---

## 22. Confusions frequentes

| Confusion | Correction |
|---|---|
| token = mot | un token peut etre un sous-mot, caractere, patch ou autre unite |
| token = embedding | le token est l'unite ; l'embedding est son vecteur |
| embedding = representation finale | l'embedding initial est transforme par les couches |
| attention = explication fiable | les poids d'attention sont un mecanisme interne, pas automatiquement une explication causale |
| Q/K/V = trois copies du token | ce sont trois projections apprises ayant des roles differents dans le calcul |
| softmax = classification | softmax transforme generiquement des scores en poids normalises |
| Transformer = LLM | un LLM est une application/famille de modeles ; le Transformer est une architecture |
| patch = objet | un patch est une region d'image, pas necessairement une entite semantique |
| latent state = etat Markovien | une representation latente ne garantit pas la suffisance dynamique |
| PCA des tokens = PCA des poids | on peut appliquer la PCA aux activations produites pour analyser leur geometrie |

---

## 23. Parcours d'apprentissage conseille

Pour relier ces notions aux bases deja apprises :

1. revoir vecteurs, matrices et produit scalaire ;
2. revoir reseaux de neurones et couches lineaires ;
3. comprendre embeddings ;
4. comprendre sequence models et hidden state ;
5. comprendre attention ;
6. deriver `Q/K/V` et scaled dot-product attention ;
7. comprendre multi-head et bloc Transformer ;
8. passer a Vision Transformer / patch tokens ;
9. etudier representations latentes et leur geometrie ;
10. seulement ensuite relier a JEPA, POMDP et world models.

La Deep Learning Specialization de DeepLearning.AI fournit aujourd'hui un pont direct : son cours
`Sequence Models` traite les word embeddings, l'attention, puis une semaine consacree au Transformer,
a la self-attention et a la multi-head attention.

---

## 24. Sources principales

- Vaswani et al., *Attention Is All You Need*, 2017 — source primaire de l'architecture Transformer.
- Jay Alammar, *The Illustrated Transformer* — reconstruction visuelle et pedagogique des flux de
  representations, de la self-attention et de `Q/K/V`.
- DeepLearning.AI / Andrew Ng, *Sequence Models* — pont pedagogique RNN/embeddings -> attention ->
  Transformer dans la Deep Learning Specialization.

Ces sources servent de point de depart. Les extensions modernes (RoPE, GQA/MQA, FlashAttention,
architectures multimodales, ViT, JEPA et world models) devront etre traitees dans des fiches distinctes
avec sources primaires et limites explicites.
