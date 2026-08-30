# Couverture statistique à vérité connue — vérifier l'instrument avant le résultat

> **Question de départ :** avant de croire un intervalle de confiance ou une règle de décision appliquée à des données réelles, comment vérifier que cette procédure statistique se comporte comme prévu lorsque nous connaissons déjà la vraie réponse ?

Cette entrée est issue du préflight statistique de Study 1B dans `siamese-embedding-compression-lab`. Elle explique un concept général : **la couverture statistique d'une procédure d'intervalle**, testée par simulation à vérité connue.

Elle ne mesure ni la couverture de code, ni la couverture de tests, ni la qualité biométrique de la compression 512D → 128D.

---

## 1. Le problème : un intervalle peut être calculable sans être bien calibré

Dans Study 1B, la quantité scientifique qui nous intéressera plus tard est une différence de FNMR entre une représentation compressée et la référence `raw512` :

\[
\Delta_{FNMR}(m,\alpha)
=
FNMR_m(\alpha)-FNMR_{raw512}(\alpha).
\]

Le protocole utilise un rééchantillonnage bootstrap par identité pour produire une distribution d'incertitude et notamment une borne supérieure unilatérale.

Mais avant d'appliquer cette procédure aux vrais résultats de compression, une question plus fondamentale apparaît :

> **si la vraie valeur de Δ était connue, notre procédure statistique construirait-elle des intervalles qui contiennent cette vraie valeur aussi souvent qu'elle le devrait ?**

C'est une question de **calibration de l'instrument statistique**.

---

## 2. Construire un monde où la vérité est connue

Sur les vraies données, nous ne connaissons pas la « vraie » valeur de Δ dans la population sous-jacente. C'est précisément pour cela que nous estimons et construisons des intervalles.

Pour tester la procédure, nous créons donc beaucoup de jeux de données synthétiques où la valeur génératrice est imposée, par exemple :

\[
\Delta_{vrai}=0,
\qquad
0.01,
\qquad
0.03,
\qquad
0.05.
\]

Pour chaque jeu synthétique :

```text
vérité choisie Δ_vrai
        ↓
génération d'un dataset synthétique
        ↓
application de la même procédure statistique
        ↓
intervalle bootstrap obtenu
        ↓
question : contient-il Δ_vrai ?
```

Comme la vérité a été fixée avant la simulation, nous pouvons compter les succès et les échecs sans ambiguïté.

---

## 3. Définition de la couverture empirique

Si nous simulons `N` datasets indépendants et si `K` intervalles contiennent la vraie valeur, la couverture empirique est :

\[
\widehat C=\frac{K}{N}.
\]

Exemple simple :

```text
1000 datasets simulés
983 intervalles contiennent la vraie valeur
17 ne la contiennent pas

couverture empirique = 983 / 1000 = 98,3 %
```

Cette valeur ne dit pas que « le modèle est correct à 98,3 % ». Elle dit uniquement :

> **dans ce scénario synthétique à vérité connue, la procédure d'intervalle a contenu la vraie valeur dans 98,3 % des répétitions.**

---

## 4. Pourquoi ne pas regarder seulement 98,3 % ?

La couverture empirique elle-même est aléatoire. Avec un autre lot de 1000 simulations, on pourrait obtenir 97,9 %, 98,6 %, etc.

Il faut donc quantifier l'incertitude sur la couverture observée.

Study 1B utilise pour cela une borne inférieure exacte de **Clopper–Pearson** à 95 % appliquée au nombre de succès `K` parmi `N` essais.

L'idée est :

> « Je n'affirme pas seulement que j'ai observé 98,3 %. Je demande quelle couverture minimale reste compatible avec ces données à un niveau de confiance fixé. »

Le gate préenregistré exige :

\[
\text{borne basse CP 95 %} \ge 0.93.
\]

Attention à une confusion possible : **0,93 n'est pas le niveau nominal de l'intervalle principal**. C'est une règle conservatrice sur la borne basse de la couverture empirique mesurée par simulation.

---

## 5. Pourquoi plusieurs scénarios ?

Une procédure peut sembler bien calibrée dans un cas facile et échouer lorsque les observations sont dépendantes ou lorsque l'effet approche la frontière de décision.

Le préflight Study 1B a donc gelé cinq scénarios avant d'en lire les résultats :

| Scénario | Δ vrai | Rôle |
|---|---:|---|
| `independent_pair_null` | 0.00 | cas simple sans effet sujet |
| `subject_dependence_null` | 0.00 | dépendances par sujet, effet nul |
| `subject_dependence_noninferior` | 0.01 | effet non inférieur planifié |
| `subject_dependence_boundary` | 0.03 | exactement sur la marge de non-infériorité |
| `subject_dependence_inferior` | 0.05 | cas réellement inférieur |

Le point important est que la procédure est challengée dans plusieurs régimes, y compris autour de la frontière qui compte pour la décision.

---

## 6. Pourquoi le bootstrap est par identité et non par paire indépendante

Les paires biométriques ne sont pas toutes indépendantes : une même identité peut apparaître dans plusieurs comparaisons.

Le bootstrap Study 1B rééchantillonne donc des **slots d'identité**. Si une identité est tirée `m_i` fois :

- une arête genuine reçoit un poids `m_i` ;
- une arête impostor entre `i` et `j` reçoit un poids `m_i m_j`.

Les routes candidate et référence utilisent **le même tirage d'identités** pour conserver le caractère apparié de la comparaison.

Cette mécanique est justement l'objet que la simulation de couverture cherche à valider. Nous ne voulons pas seulement vérifier une formule abstraite ; nous voulons vérifier **notre estimateur réellement implémenté avec sa structure de dépendance**.

---

## 7. Résultat réel du checkpoint Study 1B à 1000 datasets

Le checkpoint préenregistré à 1000 datasets par scénario a produit :

| Scénario | Couverture empirique | Borne basse Clopper–Pearson 95 % | Dégénérescence |
|---|---:|---:|---:|
| independent pair null | 98,3 % | 97,29 % | 0 |
| subject dependence null | 99,9 % | 99,44 % | 0 |
| subject dependence noninferior, Δ=0,01 | 99,2 % | 98,43 % | 0 |
| boundary, Δ=0,03 | 99,4 % | 98,70 % | 0 |
| inferior, Δ=0,05 | 98,6 % | 97,66 % | 0 |

Le gate était :

```text
pour chaque cellule :
  borne basse CP 95 % >= 93 %
  ET
  fraction de réplications dégénérées <= 0,1 %
```

Les cinq cellules passent.

Le protocole avait aussi gelé les checkpoints `1000 → 2000 → 4000` avec la règle :

> **arrêter au premier checkpoint où toutes les cellules passent.**

La couverture est donc fermée au checkpoint 1000. Continuer à 2000 ou 4000 seulement parce que les résultats sont déjà connus serait contraire à la règle d'arrêt préenregistrée et consommerait du calcul sans modifier la décision prévue.

---

## 8. Ce que ce PASS autorise — et ce qu'il n'autorise pas

Le PASS de couverture autorise l'affirmation :

> **« Dans les scénarios synthétiques à vérité connue préenregistrés, notre procédure statistique présente une couverture suffisamment calibrée selon le gate défini avant les résultats. »**

Il n'autorise pas :

- « Siamese128 est aussi bon que raw512 » ;
- « PCA128 ne perd rien » ;
- « random128 passe » ;
- « la compression 512D → 128D est non inférieure » ;
- « TEST peut être ouvert ».

Ces affirmations nécessitent les **vrais résultats de Study 1B**, qui restent séparés du préflight.

La distinction est essentielle :

```text
validation de l'instrument statistique
                ≠
résultat scientifique sur le modèle
```

---

## 9. En français dans le texte

Imagine que tu possèdes une règle graduée compliquée et que tu veux mesurer une pièce inconnue. Avant de faire confiance à la règle, tu mesures beaucoup d'objets dont la longueur exacte est déjà connue.

Si la règle annonce presque toujours une zone qui contient la vraie longueur, elle est bien calibrée. Si elle donne souvent une zone qui rate la vraie longueur, le problème vient de l'instrument de mesure, même avant de parler de la pièce inconnue.

Ici :

- les objets connus = datasets synthétiques ;
- la longueur vraie = Δ imposé par le simulateur ;
- la règle = bootstrap + estimateur + intervalle ;
- « contient la vraie valeur » = succès de couverture.

---

## 10. Lecture ingénieur

La simulation de couverture joue le rôle d'une **qualification métrologique de la chaîne d'estimation**.

On ne qualifie pas le composant biométrique ; on qualifie la capacité du pipeline statistique à fournir une enveloppe d'incertitude ayant les propriétés attendues sous des régimes contrôlés.

Le chemin d'assurance est :

```text
estimand gelé
→ structure de dépendance explicitée
→ estimateur implémenté
→ vérité synthétique connue
→ Monte Carlo
→ couverture empirique
→ incertitude sur cette couverture
→ gate préenregistré
→ seulement ensuite données scientifiques réelles
```

Cette séparation évite de découvrir après coup qu'une décision « significative » reposait sur un intervalle mal calibré.

---

## 11. Lecture 12 ans

Tu inventes 1000 énigmes dont tu connais déjà la réponse, mais tu fais semblant de ne pas la connaître et tu utilises ta méthode pour proposer une zone où la réponse devrait être.

Si ta zone contient presque toujours la vraie réponse, ta méthode a réussi son examen.

Après seulement, tu peux utiliser la méthode sur une énigme où personne ne connaît la réponse exacte.

**Réussir l'examen de la méthode ne veut pas dire que la prochaine énigme aura une bonne réponse. Cela veut dire que l'outil utilisé pour l'estimer a été testé.**

---

## 12. Réflexe Diderot

Quand un résultat scientifique repose sur un intervalle ou une règle de décision complexe, demander :

1. Quelle est exactement la quantité estimée ?
2. Quelle dépendance existe dans les données ?
3. Quel rééchantillonnage reproduit cette dépendance ?
4. Peut-on construire un monde synthétique où la vérité est connue ?
5. La procédure couvre-t-elle cette vérité au niveau attendu ?
6. L'incertitude sur la couverture elle-même est-elle prise en compte ?
7. Les scénarios difficiles et les frontières de décision ont-ils été testés ?
8. Le gate a-t-il été défini avant de voir les résultats ?
9. Le PASS est-il correctement limité à ce qu'il démontre ?

---

## 13. Provenance Study 1B

Source d'expérience : `gharbonnier78/siamese-embedding-compression-lab`, Study 1B, préflight non-outcome.

Référence d'exécution du checkpoint de couverture : GitHub Actions run `33256396749`, artefact `study1b-coverage-checkpoint-1000-summary`, digest `sha256:b3acfcd530c38e0a63364a569d07a75b9e686dd65920ded488b7d51cc1dc4fb3`.

Cette entrée capitalise le concept et les résultats de qualification statistique. Elle ne contient aucun outcome biométrique SCREEN/TEST de Study 1B.
