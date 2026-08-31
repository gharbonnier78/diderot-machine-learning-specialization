# Index des notions Diderot ML

Ce dossier complete la progression par cours avec une progression par **concepts reutilisables**.
L'objectif n'est pas de transformer Diderot ML en glossaire, mais de reconstruire chaque notion selon
le chemin pedagogique suivant :

`question -> intuition -> definition -> mathematiques -> exemple minimal -> confusions -> liens -> limites`.

Une notion peut apparaitre dans plusieurs domaines. Par exemple, le produit scalaire intervient en
regression, en geometrie, dans les embeddings et dans l'attention. L'index permet donc de retrouver
la meme brique sans l'enfermer dans un seul cours ou une seule architecture.

## Niveau A — Fondations a revoir transversalement

Voir [`ml-foundations-revisited.md`](ml-foundations-revisited.md).

- vecteur : liste de nombres, point, direction ou representation selon le contexte ;
- matrice : tableau de nombres mais surtout transformation lineaire parametree ;
- produit scalaire : projection, alignement et score de compatibilite ;
- feature / representation / embedding / latent state : termes proches mais non synonymes ;
- parametre / activation / representation : ce qui est appris versus ce qui est calcule pour une entree ;
- softmax : transformation de scores en poids positifs normalises ;
- probabilite / densite / vraisemblance : trois objets a ne pas confondre ;
- objectif d'apprentissage / representation apprise : la loss supervise la tache, pas necessairement chaque structure interne ;
- PCA sur donnees ou representations versus analyse des poids du modele ;
- observation / etat / historique / belief state en apprentissage par renforcement.

## Niveau B — Representations et Transformer

Voir [`representations-transformers.md`](representations-transformers.md).

Chaine conceptuelle principale :

`signal brut -> tokenisation -> tokens -> embeddings -> positions -> Q/K/V -> attention -> representation contextualisee -> bloc Transformer -> representation latente -> tete de sortie`.

Entrees couvertes :

1. token et tokenisation ;
2. embedding ;
3. representation positionnelle ;
4. Query / Key / Value ;
5. scaled dot-product attention ;
6. self-attention ;
7. multi-head attention ;
8. residual connection et normalisation ;
9. feed-forward network dans un bloc Transformer ;
10. encoder / decoder / encoder-decoder ;
11. contextual representation ;
12. patch token ;
13. token `[CLS]` ;
14. latent representation ;
15. geometrie des representations et PCA ;
16. Transformer versus LLM ;
17. representation d'etat versus hidden state ;
18. pont vers POMDP, JEPA et world models.

## Niveau C — Ponts a construire

Ces fiches sont a developper lorsque les sources et experiences correspondantes seront integrees :

- RNN, hidden state, LSTM et motivation historique de l'attention ;
- attention cross-modal et representations multimodales ;
- Vision Transformer et tokenisation par patches ;
- predictive representation learning et JEPA ;
- etat latent suffisant, predictive state et belief state ;
- modele dynamique latent et world model ;
- geometrie des espaces latents, invariance et equivariance ;
- representations continues versus symboliques ;
- attention comme mecanisme de routage d'information versus memoire explicite.

## Convention pedagogique d'une fiche

Une fiche Diderot devrait autant que possible contenir :

1. **Question de depart** — quel probleme la notion resout-elle ?
2. **Intuition** — interpretation sans jargon.
3. **Definition precise** — objet mathematique ou algorithmique.
4. **Dimensions** — tailles des vecteurs, matrices ou tenseurs lorsqu'elles comptent.
5. **Exemple minimal** — nombres suffisamment petits pour etre calcules a la main.
6. **Ce qui est appris** — parametres ajustes par optimisation.
7. **Ce qui est calcule** — activations dependantes de l'entree.
8. **Confusions frequentes** — termes proches ou raccourcis trompeurs.
9. **Liens entrants et sortants** — prerequis et concepts prepares.
10. **Limites** — ce que la notion ne garantit pas.
11. **Sources** — papier primaire, cours, puis ressource pedagogique secondaire.

Cette structure est volontairement compatible avec le principe Diderot deja utilise dans les
laboratoires : reconstruire l'intuition, rendre les mathematiques lisibles, produire une experience,
puis expliciter les limites.
