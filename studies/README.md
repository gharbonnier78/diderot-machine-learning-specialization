# Études à venir — Diderot ML

Cet espace contient les sujets **capitalisés mais non encore transformés en chapitres ou laboratoires terminés**. Il sert à préserver le chemin scientifique entre une source, une intuition, une analyse pédagogique, une hypothèse, un protocole expérimental et, seulement après validation, une intégration dans le livre.

L'objectif est d'éviter deux pertes fréquentes :

1. une source intéressante est résumée puis oubliée sans suite expérimentale ;
2. une idée de laboratoire est implémentée trop vite sans conserver les hypothèses, les limites et la provenance qui l'ont motivée.

## Statuts possibles

Une étude passe progressivement par les états suivants :

`SOURCE_CAPTURED` — source identifiée, lien et provenance disponibles.

`SOURCE_TRACED` — métadonnées, version, hash local si applicable et politique de redistribution enregistrés.

`READING_NOTE` — synthèse pédagogique originale, avec séparation source / interprétation Diderot.

`REVIEWED_READING` — lecture relue indépendamment ; les ambiguïtés mathématiques, d'attribution et de provenance sont fermées ou enregistrées.

`STUDY_DESIGN` — questions, hypothèses, variables, métriques, menaces à la validité et critères de réfutation sont définis.

`CHAPTER_CANDIDATE` — le fil pédagogique est suffisamment stable pour devenir un chapitre Diderot, mais le chapitre n'est pas encore considéré comme terminé.

`LAB_CANDIDATE` — le protocole expérimental est suffisamment précis pour être implémenté de façon reproductible.

`LAB_IMPLEMENTED` — notebook/code/tests existent et s'exécutent.

`EVIDENCE_REVIEW` — résultats, figures, statistiques, limites, résultats négatifs et reproductibilité ont été relus.

`READY_FOR_BOOK` — le chapitre et/ou le laboratoire satisfont les critères de définition de terminé de `docs/progress.md`.

`MERGED` — contenu intégré dans le livre et/ou les laboratoires transverses.

## Chaîne de transformation attendue

```text
source primaire
    ↓
provenance + version + hash/local bytes si disponibles
    ↓
lecture originale Diderot
    ↓
claim audit : source / inférence / externe / non supporté
    ↓
review indépendante de la lecture
    ↓
question pédagogique et scientifique
    ↓
hypothèses falsifiables
    ↓
plan de chapitre
    ↓
protocole de laboratoire
    ↓
implémentation reproductible
    ↓
mesures + incertitude + ablations + résultats négatifs possibles
    ↓
review des preuves
    ↓
chapitre/lab finalisés
    ↓
intégration dans le livre
```

## Règles de gouvernance

Une étude à venir doit toujours conserver quatre couches distinctes :

- **SOURCE** — ce qui est effectivement soutenu par la source primaire ;
- **DIDEROT** — interprétations, connexions, reformulations ou hypothèses propres au projet ;
- **EXPERIMENT** — ce qui doit être testé et peut être réfuté ;
- **EVIDENCE** — ce qui a réellement été observé après expérimentation.

Une proposition ne devient pas un résultat parce qu'elle est mathématiquement élégante. Une architecture ne devient pas meilleure parce qu'elle respecte une symétrie. Une expérience doit pouvoir produire un résultat négatif.

## Critères minimaux avant implémentation d'un lab

Le dossier d'étude doit contenir :

- la question principale ;
- au moins une hypothèse falsifiable ;
- une baseline ;
- les facteurs manipulés ;
- les métriques principales et secondaires ;
- les contrôles nécessaires pour rendre la comparaison équitable ;
- les seeds/répétitions prévues ;
- la stratégie d'incertitude/statistique ;
- les ablations ;
- les coûts calcul/mémoire à suivre si pertinents ;
- les menaces à la validité ;
- le critère qui ferait conclure « hypothèse non soutenue ».

## Review indépendante

Une review indépendante peut être demandée à un autre modèle ou à un humain. Elle doit idéalement être faite sur la source primaire et les artefacts du dépôt, pas à partir d'un résumé de l'agent auteur.

Pour les études importantes, la review doit vérifier séparément :

- fidélité à la source ;
- exactitude mathématique ;
- séparation source / Diderot ;
- qualité pédagogique ;
- falsifiabilité du protocole ;
- fairness des baselines ;
- reproductibilité ;
- risques de surinterprétation ;
- conditions de passage au chapitre ou au lab.

Le reviewer doit pouvoir conclure `APPROVE`, `APPROVE WITH NON-BLOCKING COMMENTS` ou `REQUEST CHANGES`.

## Index actuel

| Étude | Origine | État actuel | Prochaine porte |
|---|---|---|---|
| [Smets — de l'équivariance au laboratoire CNN / augmentation / G-CNN](smets-equivariance-to-gcnn-lab.md) | *Mathematics of Neural Networks*, arXiv:2403.04807v1 | `STUDY_DESIGN` | Review indépendante du dossier d'étude, puis séparation `CHAPTER_CANDIDATE` / `LAB_CANDIDATE` |

## Convention de nommage

Les dossiers utilisent un nom stable orienté sujet, par exemple :

```text
studies/smets-equivariance-to-gcnn-lab.md
studies/transformers-attention-from-tokens-to-qkv.md
studies/scaling-laws-compute-data-model.md
```

Lorsqu'une étude devient un chapitre ou un laboratoire, le dossier n'est pas supprimé : il reste la trace du **raisonnement qui a conduit de la source à l'artefact final** et pointe vers les fichiers produits.