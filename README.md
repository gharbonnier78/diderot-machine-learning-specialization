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

## Labs experimentaux

Le depot accueille aussi des bancs experimentaux qui relient les outils de ML
aux problematiques d'ingenierie systeme.

- [`Change Impact & Regression Evidence`](labs/change-impact-regression/README.md)
  — simulateur reproductible separant le graphe systeme reel cache
  `G_true` du graphe d'ingenierie imparfait `G_observed`, avec strategies
  R0-R5, couverture, probabilite de detection, cout et Monte Carlo.
- [Notebook Colab/Jupyter](labs/change-impact-regression/00_change_impact_regression_lab.ipynb)
  — experience guidee et visualisation post-hoc des impacts predits, reels et
  couverts.

Ces labs sont des outils de recherche et de pedagogie. Ils ne constituent pas
des modeles de production ni des seuils de decision operationnels.

## Construire le livre

Prerequis : pdfLaTeX, Python 3 et les dependances de `requirements.txt`.

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
labs/          Bancs experimentaux reproductibles et notebooks
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
