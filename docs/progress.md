# Progression editoriale

Derniere mise a jour : 2026-08-31.

| Element | Etat | Prochaine action |
|---|---|---|
| Architecture Git/LaTeX/Python | Termine | Stabiliser apres plusieurs chapitres |
| M3-W1-11 Gaussienne | Termine v0.1 | Ajouter TP interactif ulterieur |
| Wave Equation Toy Lab | Fusionne et valide : guide + 8 experiences + solveur + tests + execution notebook CI | Utiliser comme base pour les laboratoires de stabilite et de fidelite |
| Von Neumann & CFL Lab | Fusionne et valide : derivation + notebook + helpers spectraux + tests + execution CI | Reutiliser pour phase, dispersion et limites de stabilite |
| Wave Lab 3 — convergence / verification | Fusionne sur main : solution exacte + raffinement + ordre observe + PPW + phase + energie + budget d'erreurs | Etendre vers fidelite de modele et systemes plus complexes |
| Index de notions Diderot | Candidat PR : architecture `question -> intuition -> definition -> mathematiques -> exemple -> confusions -> liens -> limites` | Appliquer progressivement aux anciennes et nouvelles notions |
| Fondations ML revisitees | Candidat PR : vecteurs, matrices, produit scalaire, softmax, probabilite, PCA, etat/observation, hidden versus belief | Ajouter de petits exercices calculables et liens vers chapitres du livre |
| Representations / Transformer | Candidat PR : token, embedding, Q/K/V, attention, Transformer, patch token, CLS, latent state, POMDP/JEPA/world-model bridges | Ajouter notebook minimal d'attention et fiches Vision/JEPA separees |
| M3-W1 K-means | Notes disponibles | Reconstruire les chapitres 1 a 3 |
| M2-W4 arbres et ensembles | Notes disponibles | Consolider en partie II |
| Parties I a III | Planifie | Integrer progressivement les conversations |
| Partie IV — representations et modeles d'etat | Initiee | Poursuivre avec Deep Learning Specialization, ViT, JEPA et world models |
| Videos et sous-titres | Sources privees indexees | Ne jamais publier sans autorisation |
| Sources publiques Transformer | Indexees en reference_only | Ajouter les sources primaires au fur et a mesure des nouvelles fiches |
| PDF | Compile et verifie | Integrer les fiches conceptuelles au livre lorsqu'elles sont suffisamment stabilisees |

## Definition de « termine »

Un chapitre est termine lorsqu'il possede : texte original, formules relues,
exemple numerique, exercice, application d'ingenierie, limites, fiche de
revision, tests du code associe et verification visuelle du PDF.

Pour une fiche conceptuelle transverse, ajouter : question de depart, intuition,
definition precise, dimensions des objets mathematiques lorsque pertinentes,
exemple calculable, distinction entre parametres appris et activations calculees,
confusions frequentes, liens entrants/sortants, limites et sources de reference.

Pour un laboratoire interactif, ajouter : execution complete du notebook,
verification visuelle des figures/animations, controle des conditions numeriques
et au moins une experience volontaire montrant une limite ou un echec.

Pour une etude de convergence, ajouter en plus : une reference exacte ou
independante, une norme d'erreur explicite, au moins trois niveaux de
raffinement, un ordre observe et une distinction claire entre erreur numerique,
erreur de modele et erreur de donnees.
