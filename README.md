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
