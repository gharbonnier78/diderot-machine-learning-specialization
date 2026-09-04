# Progression editoriale

Derniere mise a jour : 2026-09-04.

| Element | Etat | Prochaine action |
|---|---|---|
| Architecture Git/LaTeX/Python | Termine | Stabiliser apres plusieurs chapitres |
| M3-W1-11 Gaussienne | Termine v0.1 | Ajouter TP interactif ulterieur |
| Wave Equation Toy Lab | Fusionne et valide : guide + 8 experiences + solveur + tests + execution notebook CI | Utiliser comme base pour les laboratoires de stabilite et de fidelite |
| Von Neumann & CFL Lab | Fusionne et valide : derivation + notebook + helpers spectraux + tests + execution CI | Reutiliser pour phase, dispersion et limites de stabilite |
| Wave Lab 3 — convergence / verification | Candidat PR : solution exacte + raffinement + ordre observe + PPW + phase + energie + budget d'erreurs | Executer notebook en CI, relire les resultats de convergence et fusionner si coherents |
| Espace `studies/` | Candidat PR : cycle de vie des etudes a venir, gates et regles source / Diderot / experiment / evidence ; review independante PR #11 favorable avec commentaires non bloquants | Reconciliation avec `main`, CI fraiche, puis merge si aucune regression |
| Lecture Smets — Mathematics of Neural Networks | Source publique tracee + analyse pedagogique revue et mergee (PR #9) ; dossier `studies/smets-equivariance-to-gcnn-lab.md` en `STUDY_DESIGN`, review independante favorable | Apres merge de PR #11, preciser avant `LAB_CANDIDATE` H5, budget de fairness et contre-regime de mauvaise symetrie |
| Puissance statistique / erreurs type I-II / non-inferiorite | Draft pedagogique source-tracee, apparue dans Study 1B ; distinction mesures descriptives vs force de decision, analogie ingenierie, misconceptions et gate de comprehension ajoutes | Relecture humaine ; proposer `H0`, `H1`, `alpha`, `beta`, `1-beta` a l'atlas canonique de notation ; integrer plus tard au chapitre transverse statistiques/evidence |
| Tests d'hypotheses comme cadre de qualification IVVQ | Draft pedagogique transverse source-tracee ; pont requirement/claim -> evidence -> incertitude -> decision, Type I/II, power, non-inferiorite/equivalence et risque de decision | Relecture humaine ; ouvrir une etude transverse Test/IVVQ pour cas concrets performance, fiabilite, biometrie, failover et multiplicite ; distinguer prescriptions normatives et grille Diderot |
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

Pour une lecture transverse de source, distinguer explicitement : provenance et
empreinte, contenu soutenu par la source, interpretation Diderot, limites de la
source et experience falsifiable proposee. Une lecture capitalisee n'est pas
consideree comme un chapitre termine tant que les criteres ci-dessus ne sont pas
satisfaits.

Pour une etude a venir, utiliser le cycle de vie de [`studies/README.md`](../studies/README.md) :
la source, l'interpretation, le protocole experimental et les preuves observees
doivent rester des couches distinctes jusqu'a l'integration finale dans le livre.
