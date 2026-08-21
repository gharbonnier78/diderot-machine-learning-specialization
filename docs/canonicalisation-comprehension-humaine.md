# De la vérification à la connaissance canonique

## Idée centrale

Un résultat n'est pas encore une connaissance durable simplement parce qu'il a été généré, testé ou accepté par un vérificateur automatique.

Principe de fermeture :

> **C'est fermé quand je peux tout expliquer.**

Dans une production scientifique ou d'ingénierie assistée par LLM, cela impose de distinguer au moins trois questions :

1. **Est-ce suffisamment étayé ?** — question scientifique ou de vérification.
2. **Est-ce réellement compris par un humain responsable ?** — question de compréhension.
3. **Est-ce prêt à devenir une référence durable ?** — question de canonicalisation.

Ces trois états sont liés, mais aucun ne remplace les deux autres.

## Axiome repris par le Scientific Research Harness

Le `scientific-research-harness` formalise désormais l'axiome suivant :

> **A claim cannot reach canonical status solely because an automated verifier accepted it.**  
> **At least one accountable human must be capable of explaining the result, its evidence, limitations, provenance and significance.**

Un résultat peut donc être valide, reproductible et même formellement vérifié sans être encore canonique. Inversement, une bonne explication humaine ne rend pas valide une preuve ou une expérience qui échoue à ses critères scientifiques.

Référence d'implémentation : `gharbonnier78/scientific-research-harness`, fichier `design/HUMAN_COMPREHENSION_CANONICALIZATION.md`.

## Source conceptuelle : Terence Tao, 2026

Cette distinction est renforcée par l'essai de Terence Tao, *Mathematics in the Age of AI*, arXiv:2608.16753v1 (2026).

Le papier ne cherche pas principalement à déterminer jusqu'où l'IA peut faire des mathématiques. Il suppose conditionnellement qu'une capacité de niveau recherche deviendra suffisamment forte, puis examine ce que la communauté cherche réellement à préserver : compréhension, transmission, contribution cumulative, construction de théorie et valeur collective.

Tao montre qu'un objectif apparemment simple comme « résoudre des problèmes » se décompose progressivement en une chaîne :

```text
génération
  -> vérification
  -> exposition
  -> publication / acceptation
  -> digestion
  -> canonicalisation
```

Le point important pour Diderot est que **la vérification n'est qu'une étape**. Une connaissance devient durable lorsqu'elle peut être comprise, reliée à ce qui l'entoure, enseignée et incorporée dans un outillage intellectuel réutilisable.

Le papier souligne aussi un déplacement de rareté : si l'IA rend la génération abondante, les ressources rares deviennent l'attention experte, la vérification, l'explication, la digestion et la canonicalisation.

Il avertit enfin qu'une écriture trop polie peut effacer la « friction naturelle » qui révèle où se trouvait réellement la difficulté. Les erreurs corrigées, contre-exemples, hypothèses abandonnées et changements de raisonnement peuvent donc avoir une valeur pédagogique propre.

Une extraction sourcée et bornée du papier est conservée dans le harness : `sources/tao-2026-mathematics-in-the-age-of-ai.md`.

## Rôle de Diderot

Diderot n'est pas le lieu où une expérience acquiert sa validité scientifique. Cette validité doit venir des sources, expériences, vérifications, revues et critères propres au travail concerné.

Diderot joue plutôt le rôle de **couche de canonicalisation pédagogique locale** :

```text
travail de recherche / ingénierie
        |
        v
preuves + falsification + revue
        |
        v
compréhension humaine responsable
        |
        v
Diderot
        |
        v
connaissance expliquée, reliée, rejouable et réutilisable
```

Une entrée Diderot devrait donc être capable de reconstruire la chaîne intellectuelle et non seulement le résultat final :

- la question initiale ;
- les hypothèses et les sources ;
- le raisonnement ou la dérivation ;
- l'expérience ou la preuve ;
- ce qui a échoué ou corrigé le modèle mental ;
- les limites ;
- ce que le résultat change réellement ;
- les liens vers les concepts voisins et les expériences rejouables.

## Conséquence pour les agents et les LLM

Un agent peut générer un notebook, une preuve, un plan de test, une architecture, du code, une configuration, un rapport ou une recommandation. Un autre agent peut le relire, exécuter des tests et vérifier des contraintes.

Cela produit de l'**évidence automatisée**. Ce n'est pas encore une autorité canonique.

Pour un artefact conséquent, le passage au statut de référence doit laisser au moins un humain responsable capable d'expliquer :

```text
ce qui a été produit
-> pourquoi on y croit
-> quelles preuves ont été obtenues
-> quelles limites subsistent
-> d'où viennent les données, sources et transformations
-> quelle décision ou quel usage le résultat autorise réellement
```

La production assistée par IA peut donc accélérer fortement la partie amont. La gouvernance doit éviter que cette accélération transforme la canonicalisation en simple validation mécanique.

## Protection contre les faux objectifs

Le même raisonnement protège contre la loi de Goodhart. Les métriques faciles à optimiser restent utiles, mais ne doivent pas devenir l'objectif réel :

- nombre de notebooks ;
- nombre de dépôts ;
- nombre de tests ;
- couverture seule ;
- nombre de claims ;
- benchmark seul ;
- nombre de documents générés ;
- nombre de checks verts.

L'objectif utile est plus exigeant :

> **augmenter le débit de connaissances fiables, comprises et réutilisables — pas le débit d'artefacts.**

## Statut

Cette note est une entrée transversale de Diderot. Elle ne transforme pas l'essai de Tao en preuve expérimentale de l'efficacité du harness ; elle en conserve les idées pertinentes et explicite leur adaptation à une démarche de recherche, d'apprentissage et d'ingénierie assistée par IA.