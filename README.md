# Diderot ML - Machine Learning Specialization

Livre d'apprentissage personnel, reproductible et evolutif autour de la
Machine Learning Specialization. Le depot transforme les notes de cours, les
questions, les demonstrations mathematiques et les travaux pratiques en un
ouvrage original en francais.

## Etat actuel

Version `0.1.0` : architecture complete du depot et premier chapitre finalise :

- `M3-W1-11` - distribution gaussienne et fondements de la detection
  d'anomalies ;
- demonstration du facteur `pi`, maximum de vraisemblance et passage annonce
  aux caracteristiques multiples ;
- script reproductible produisant les courbes gaussiennes ;
- journal pedagogique condense de la discussion ;
- manifeste des sources privees, sans redistribution des videos ou
  transcriptions tierces.

Le plan global du livre se trouve dans [`docs/course-map.md`](docs/course-map.md)
et l'avancement dans [`docs/progress.md`](docs/progress.md).

## Harness et atlas des notations

Le depot adopte le `scientific-research-harness` par une reference immuable
declaree dans [`harness-adoption.yaml`](harness-adoption.yaml). Les agents de
depot disposent de points d'entree courts (`AGENTS.md` et `CLAUDE.md`) qui
chargent ce contrat sans qu'il soit necessaire de le repeter dans chaque
prompt. La meta-documentation se trouve dans
[`docs/harness-meta.md`](docs/harness-meta.md).

La table LaTeX du livre dans `book/chapters/appendix-notation.tex` reste une vue
specifique a cette publication. L'atlas pedagogique transverse et indexe des
notations est maintenu dans le depot canonique Diderot `mmals-ml-wiki`, sous
`mathematics/notation/registry.json`, avec une page interactive et une planche
A2 imprimable. Le livre ne doit pas creer un registre concurrent : une nouvelle
notation durable doit etre capitalisee ou remise au registre Diderot commun.

## Laboratoires transverses Diderot

Ces laboratoires partent d'une question concrete et reconstruisent le chemin
`intuition -> mathematiques -> discretisation -> code -> experience -> limites`.

### Wave Equation Toy Lab

[🇫🇷 FR](docs/waves-toy-lab.md#fr) · [🇬🇧 EN](docs/waves-toy-lab.md#en) · [🇪🇸 ES](docs/waves-toy-lab.md#es) · [🇵🇹 PT](docs/waves-toy-lab.md#pt)

Huit experiences progressives : impulsion 1D, source harmonique, deux sources
et phase, propagation 2D, interferences, reflexions, modes propres et rupture
volontaire de la condition CFL. Le guide relit explicitement les formules en
langage courant et le notebook compagnon est executable :

[`notebooks/waves/00_wave_equation_toy_lab.ipynb`](notebooks/waves/00_wave_equation_toy_lab.ipynb)

Les approximations numeriques importantes sont rendues explicites dans
[`docs/waves-numerical-caveats.md`](docs/waves-numerical-caveats.md) : source
ponctuelle de cellule versus Dirac normalisee, points fantomes de Neumann,
frequence continue versus frequence discrete et portee exacte de la condition
CFL.

### Von Neumann & CFL Lab

[🇫🇷 FR](docs/von-neumann-cfl-lab.md#fr) · [🇬🇧 EN](docs/von-neumann-cfl-lab.md#en) · [🇪🇸 ES](docs/von-neumann-cfl-lab.md#es) · [🇵🇹 PT](docs/von-neumann-cfl-lab.md#pt)

Ce second laboratoire part de l'explosion observee dans l'experience CFL et
reconstruit la condition de stabilite au lieu de la memoriser : erreur
numerique, modes de Fourier, nombres complexes, symbole du stencil, facteur
d'amplification, rayon spectral, condition CFL 1D/2D puis dispersion numerique.
Le notebook verifie chaque etape par de petites experiences :

[`notebooks/waves/01_von_neumann_cfl_lab.ipynb`](notebooks/waves/01_von_neumann_cfl_lab.ipynb)

Une note de precision traite le cas limite souvent masque par le raccourci
`|G| <= 1` : aux racines doubles situees sur le cercle unite, la multiplicite
compte et un terme seculaire peut apparaitre. Elle distingue donc la frontiere
CFL theorique d'une marge pratique de calcul :

[`docs/von-neumann-stability-caveats.md`](docs/von-neumann-stability-caveats.md)

### Wave Lab 3 — convergence, verification et credibilite numerique

[🇫🇷 FR](docs/wave-convergence-verification-lab.md#fr) · [🇬🇧 EN](docs/wave-convergence-verification-lab.md#en) · [🇪🇸 ES](docs/wave-convergence-verification-lab.md#es) · [🇵🇹 PT](docs/wave-convergence-verification-lab.md#pt)

Ce troisieme laboratoire separe explicitement stabilite, convergence,
verification numerique et validation physique. Il utilise un mode de Neumann
ayant une solution analytique connue pour mesurer l'erreur, raffiner la grille,
reconstruire l'ordre observe, etudier les points par longueur d'onde, l'erreur
de phase et un diagnostic d'energie. Une derniere experience montre que le
raffinement numerique ne corrige pas un mauvais parametre physique :

[`notebooks/waves/02_convergence_verification_lab.ipynb`](notebooks/waves/02_convergence_verification_lab.ipynb)

## Construire le livre

Prerequis : pdfLaTeX, Python 3, NumPy et Matplotlib.

```bash
make setup
make figures
make book
make test
```

Le PDF est genere dans :

```text
output/pdf/diderot-ml-specialization-v0.1.0.pdf
```

## Organisation

```text
book/          Sources LaTeX et figures originales
chat-notes/    Syntheses pedagogiques des discussions
docs/          Carte du cursus, progression et conventions
notebooks/     Laboratoires interactifs reproductibles
sources/       Manifeste de tracabilite des sources privees
src/           Code Python reproductible
tests/         Tests automatiques
output/pdf/    Livre compile
```

## Politique relative aux sources de cours

Les videos, captures d'ecran et transcriptions tierces ne sont pas publiees
dans ce depot. Elles restent des sources privees et sont seulement referencees
par leurs metadonnees et empreintes cryptographiques. Le texte du livre est une
reformulation pedagogique originale, enrichie d'explications, de derivations et
d'exercices propres.

## Auteur

Guillaume Harbonnier - Diderot ML, 2026.