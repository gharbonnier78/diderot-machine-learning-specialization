# Progression editoriale

Derniere mise a jour : 2026-08-19.

| Element | Etat | Prochaine action |
|---|---|---|
| Architecture Git/LaTeX/Python | Termine | Stabiliser apres plusieurs chapitres |
| M3-W1-11 Gaussienne | Termine v0.1 | Ajouter TP interactif ulterieur |
| Wave Equation Toy Lab | Fusionne et valide : guide + 8 experiences + solveur + tests + execution notebook CI | Utiliser comme base pour les laboratoires de stabilite et de fidelite |
| Von Neumann & CFL Lab | Fusionne et valide : derivation + notebook + helpers spectraux + tests + execution CI | Reutiliser pour phase, dispersion et limites de stabilite |
| Wave Lab 3 — convergence / verification | Candidat PR : solution exacte + raffinement + ordre observe + PPW + phase + energie + budget d'erreurs | Executer notebook en CI, relire les resultats de convergence et fusionner si coherents |
| M3-W1 K-means | Notes disponibles | Reconstruire les chapitres 1 a 3 |
| M2-W4 arbres et ensembles | Notes disponibles | Consolider en partie II |
| Parties I a III | Planifie | Integrer progressivement les conversations |
| Videos et sous-titres | Sources privees indexees | Ne jamais publier sans autorisation |
| PDF | Compile et verifie | Publier a chaque version stable |

## Definition de « termine »

Un chapitre est termine lorsqu'il possede : texte original, formules relues,
exemple numerique, exercice, application d'ingenierie, limites, fiche de
revision, tests du code associe et verification visuelle du PDF.

Pour un laboratoire interactif, ajouter : execution complete du notebook,
verification visuelle des figures/animations, controle des conditions numeriques
et au moins une experience volontaire montrant une limite ou un echec.

Pour une etude de convergence, ajouter en plus : une reference exacte ou
independante, une norme d'erreur explicite, au moins trois niveaux de
raffinement, un ordre observe et une distinction claire entre erreur numerique,
erreur de modele et erreur de donnees.
