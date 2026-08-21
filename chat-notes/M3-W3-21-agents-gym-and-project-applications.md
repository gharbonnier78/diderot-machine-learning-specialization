# M3-W3-21 — Agents, Gym/Gymnasium et applications à nos projets

> **Statut :** note pédagogique de travail  
> **Date :** 2026-08-16  
> **Contexte :** Machine Learning Specialization, cours 3, semaine 3, devoir *Deep Q-Learning — Lunar Lander*  
> **Portée :** synthèse originale reliant le formalisme agent–environnement, l’API Gym/Gymnasium, l’automatique et les projets Diderot ML, MMALS, biométrie, gouvernance d’ingénierie et simulation drone/EO-IR.

## 1. Question directrice

Le devoir Lunar Lander introduit une boucle :

```text
observation → décision → action → transition → récompense
```

Cette boucle soulève quatre questions : qu’est-ce qu’un agent, en quoi ressemble-t-il aux systèmes déjà construits, Gym/Gymnasium peut-il être utile à nos projets, et pourquoi ne l’avons-nous pas utilisé jusqu’ici ?

> Un système peut être agentique sans être un agent de reinforcement learning. Gymnasium devient utile lorsqu’il faut standardiser une interaction séquentielle entre un décideur et un environnement réel ou simulé. Il n’est pas nécessaire pour un apprentissage sur dataset fixe, un workflow déterministe, un classifieur siamois ou une simple aide documentaire à la décision.

## 2. Définition opérationnelle d’un agent

Au sens général, un agent est un système qui :

1. reçoit une représentation partielle ou complète d’une situation ;
2. poursuit un objectif ;
3. choisit une action ;
4. agit sur un environnement ;
5. observe les conséquences ;
6. éventuellement, adapte ses décisions futures.

À l’instant t, une observation o(t) est transformée par une politique π en action a(t). L’environnement applique ensuite cette action et produit une nouvelle observation, ainsi qu’une récompense éventuelle.

Le mot « agent » ne préjuge toutefois ni de l’algorithme ni de la présence d’apprentissage.

| Type | Mécanisme de décision | Apprentissage par interaction |
|---|---|---:|
| Agent à règles | règles, automate, DMN | non |
| Agent logiciel/LLM | raisonnement, outils, workflow | pas nécessairement |
| Modèle supervisé | fonction apprise sur exemples étiquetés | non pendant l’action |
| Contrôleur classique | PID, LQR, MPC, logique de commande | pas nécessairement |
| Agent RL | politique optimisée par récompenses cumulées | oui |

### 2.1 Agent logiciel/LLM et agent RL

Un agent LLM peut lire un dossier, appeler des outils, chercher des informations, produire une recommandation, demander une validation humaine et conserver un journal d’activité. Cela ne suffit pas à en faire un agent RL.

Pour parler de RL, il faut au minimum :

- une suite de décisions interdépendantes ;
- un environnement qui change après les actions ;
- un signal de récompense ou de coût ;
- une politique ajustée pour améliorer le retour cumulé.

### 2.2 Modèle, politique et agent

Dans Lunar Lander, le réseau neuronal n’est pas à lui seul l’agent complet. Le Q-network calcule quatre valeurs :

```text
Q(s,·) = [Q(s,0), Q(s,1), Q(s,2), Q(s,3)]
```

La politique epsilon-greedy décide ensuite d’explorer avec une probabilité epsilon ou de choisir l’action de valeur Q maximale.

L’agent comprend donc :

- le Q-network ;
- la politique epsilon-greedy ;
- le replay buffer ;
- le mécanisme d’apprentissage ;
- le réseau cible ;
- les hyperparamètres ;
- la logique de gestion des épisodes.

## 3. Le rôle de Gym/Gymnasium

Gym/Gymnasium n’est pas un algorithme de RL. C’est une **API standardisée d’environnement**. Elle sépare l’agent, qui choisit, de l’environnement, qui applique l’action et fait évoluer le monde.

L’environnement encapsule typiquement :

- la dynamique du système ;
- les conditions initiales ;
- les perturbations ;
- les capteurs ou observations ;
- les actionneurs ou actions possibles ;
- la fonction de récompense ;
- les conditions de terminaison ;
- les informations de diagnostic.

Cette séparation permet de comparer sur le même problème une politique aléatoire, des règles expertes, un PID/LQR/MPC, un planificateur, un agent RL ou un opérateur humain.

### 3.1 API ancienne du cours

Le notebook utilise Gym 0.24 :

```python
state = env.reset()
next_state, reward, done, info = env.step(action)
```

Le booléen `done` regroupe toutes les fins d’épisode.

### 3.2 API moderne Gymnasium

Gymnasium est le fork maintenu de Gym. L’API moderne distingue :

```python
observation, info = env.reset(seed=42)
next_observation, reward, terminated, truncated, info = env.step(action)
```

- `terminated=True` : état terminal intrinsèque au problème, par exemple crash ou succès ;
- `truncated=True` : arrêt externe, par exemple limite de temps ou budget d’étapes.

La boucle s’arrête dans les deux cas, mais la cible de Bellman ne doit généralement couper le bootstrap que lors d’une vraie terminaison :

```text
y = r + gamma × (1 − terminated) × max Q(s’,a’)
```

Une troncature ne signifie pas nécessairement qu’il n’existe plus de valeur future. Cette nuance corrige une ambiguïté importante de l’ancien `done`.

Références :

- [Gymnasium — documentation officielle](https://gymnasium.farama.org/) ;
- [guide officiel de migration depuis Gym](https://gymnasium.farama.org/introduction/migration_guide/).

## 4. Lecture en termes d’automatique

| Gym/RL | Système automatique |
|---|---|
| environnement | procédé, plante ou simulateur |
| observation | mesure capteur |
| état | variables internes du système |
| estimateur | Kalman, observateur, fusion de données |
| action | commande des actionneurs |
| politique | contrôleur ou loi de commande |
| `step(action)` | appliquer la commande et avancer de Te |
| récompense | critère instantané |
| return | objectif cumulé |
| épisode | mission, essai ou trajectoire |
| terminaison | succès, panne, crash ou fin de mission |

Gym ne résout pas automatiquement :

- le choix de la fréquence d’échantillonnage ;
- la synchronisation des capteurs ;
- les retards et le jitter ;
- la perte de trames ;
- l’interpolation et l’extrapolation ;
- le filtrage et l’estimation d’état ;
- la calibration et l’identification du modèle ;
- la saturation des actionneurs ;
- la représentativité simulation–réalité ;
- les validations SIL/HIL ;
- la sûreté de fonctionnement.

Ces phénomènes doivent être explicitement intégrés à l’environnement, à ses wrappers ou à la chaîne d’estimation.

### 4.1 État et observation

Dans un exemple pédagogique, on assimile souvent état et observation. Dans un système réel, l’observation est plutôt une fonction partielle et bruitée de l’état. L’agent peut recevoir des mesures brutes, un état estimé par filtre de Kalman, une fenêtre temporelle, un belief state ou une représentation apprise.

Lorsque l’observation ne suffit pas à rendre le futur indépendant du passé, le problème relève plutôt d’un POMDP que d’un MDP pleinement observable.

## 5. Ce que nous avons déjà construit

### 5.1 Evidence-Guided Engineering Agents

Les personas tels que `bom-intelligence`, `funding-business`, `ip-legal-opportunity` et les futurs assistants d’innovation ou de nomenclature sont des agents logiciels bornés.

Ils peuvent recevoir un dossier, rechercher et structurer des éléments, construire une evidence card, recommander une action ou une escalade, tracer leur activité et laisser la décision engageante à l’humain.

Ils ne sont pas aujourd’hui des agents RL, car ils n’apprennent pas une politique par interaction répétée avec un environnement et une récompense. Ils combinent surtout schémas, règles, raisonnement LLM, recherche, gates déterministes et validation humaine.

### 5.2 STRAT-Q et Test Authority

La chaîne de gouvernance est :

```text
Claim → Hypothèses → Scénarios de risque → Obligations de preuve
→ Evidence → Confiance → Risque résiduel → Décision
```

Elle peut être mise en correspondance avec une boucle décisionnelle :

| Gouvernance | Formalisme séquentiel |
|---|---|
| état du projet et preuves | observation |
| sélectionner un test | action |
| obtenir son résultat | transition |
| information gagnée et risque réduit | récompense possible |
| coût, délai, exposition | pénalité possible |
| poursuivre, escalader ou arrêter | décision/terminaison |

Mais le système reste volontairement une aide à la décision gouvernée. Il ne doit pas apprendre seul à libérer ou bloquer un projet à partir d’un KPI approximatif.

Le principe **Evidence-Guided, Judgment-Accountable** implique que les contraintes restent explicites, les preuves auditables, les critères non réduits à un score unique, l’incertitude conservée et l’humain responsable des décisions engageantes.

### 5.3 MMALS

MMALS est le système existant le plus proche d’une extension RL. Les prototypes ont déjà introduit tâches successives, mémoire fonctionnelle, distillation, routage, mesure de l’oubli et changements de régime.

Cependant, apprentissage séquentiel ne signifie pas automatiquement reinforcement learning :

- les données d’apprentissage restent fournies ;
- le système ne choisit pas nécessairement les expériences ;
- aucune récompense environnementale n’entraîne une politique de décision ;
- le RL meta-router reste une extension optionnelle.

Gymnasium n’était donc pas nécessaire pour tester le continual learning actuel.

### 5.4 Recommandeur expérimental transparent et bayésien

Ce projet possède une structure naturellement séquentielle. À chaque étape, le système observe les hypothèses, les preuves, les contradictions, la confiance, le budget, le temps restant et les expériences déjà effectuées.

Il peut recommander réplication, collecte ciblée, exploration, falsification, exploitation, arrêt ou escalade humaine.

Une récompense candidate pourrait combiner :

```text
gain d’information
+ amélioration de calibration
+ détection d’une hypothèse fausse
− coût
− délai
− risque
```

Le danger est de confondre récompense mesurable et finalité réelle. Un agent pourrait maximiser le nombre de tests, le nombre de défauts ou le taux de fermeture sans améliorer la qualité de la décision. D’où la nécessité de contraintes, d’audit, de baselines et d’un removal test.

### 5.5 Recherche biométrique siamoise

Le réseau siamois actuel apprend une représentation ou une distance entre deux échantillons. Ce travail relève principalement de l’apprentissage métrique supervisé.

Gymnasium n’est pas nécessaire pour entraîner les embeddings, comparer baseline et projection, mesurer FMR/FNMR, effectuer le bootstrap ou tester la compression 512→128.

Un problème séquentiel apparaîtrait si le système devait choisir quel doigt demander ensuite, quelle modalité acquérir, si une acquisition supplémentaire vaut son coût, quand accepter ou demander une revue, et à quel instant arrêter.

On se rapprocherait alors de l’active sensing, du bandit contextuel ou du POMDP. Gymnasium pourrait standardiser ce simulateur décisionnel sans remplacer le modèle biométrique.

## 6. Où Gymnasium serait réellement utile

### 6.1 Simulateur drone et capteur EO/IR

C’est le cas d’usage le plus direct.

**Observation possible :**

- position, vitesse et attitude ;
- état estimé et covariance ;
- énergie restante ;
- météo, visibilité et vent ;
- état des capteurs EO/IR ;
- qualité et latence de la liaison ;
- couverture déjà réalisée ;
- incertitude des détections ;
- terrain, obstacles et zones interdites.

**Actions possibles :**

- changer de cap, vitesse ou altitude ;
- orienter la charge utile ;
- changer de mode capteur ;
- choisir une zone d’observation ;
- acquérir une nouvelle image ;
- modifier la trajectoire ;
- retourner à la base ;
- abandonner une tâche devenue dangereuse.

**Récompense possible :**

- information utile acquise ;
- couverture et qualité de classification ;
- réduction d’incertitude ;
- énergie consommée ;
- temps de mission ;
- risque de collision ;
- perte de communication ;
- violation de contraintes de sécurité.

Gymnasium ne remplacerait ni le simulateur 3D, ni le modèle de vol, ni le MNT/MNS, ni les modèles EO/IR, ni la chaîne de classification, ni la visualisation accélérée. Il fournirait le contrat entre l’agent et le simulateur.

```text
agent de décision
    ↕ action / observation
environnement Gymnasium
    ↕
simulateur physique + capteurs + monde 3D
```

Cette séparation permettrait d’évaluer sur le même monde une politique de référence, un contrôleur classique, un planificateur, un agent RL, un opérateur humain ou une combinaison hiérarchique.

### 6.2 Environnement de recommandation expérimentale

Un environnement personnalisé pourrait simuler des hypothèses vraies ou fausses cachées, des expériences de coûts différents, des observations bruitées, des puissances statistiques variables, des régimes stables ou émergents et des budgets limités.

```python
class ExperimentalGovernanceEnv(gym.Env):
    def reset(self, seed=None, options=None):
        return observation, info

    def step(self, action):
        return observation, reward, terminated, truncated, info
```

Le même banc permettrait de comparer règles expertes, choix bayésien, gain d’information, bandits contextuels, RL, recommandation LLM et choix humain.

Même si le meilleur système final n’est pas RL, l’interface Gymnasium resterait utile comme **harness d’évaluation commun**.

## 7. Pourquoi Gymnasium n’a pas été utilisé jusqu’ici

Ce n’est pas un oubli. Jusqu’ici, nos principaux problèmes avaient plutôt la forme :

```text
X → prédiction
```

ou :

```text
document → analyse → recommandation humaine
```

Gymnasium devient pertinent lorsque le problème prend la forme :

```text
s0 → a0 → r1,s1 → a1 → r2,s2 → …
```

Quatre conditions signalent sa pertinence :

1. il existe plusieurs décisions successives ;
2. chaque action modifie les décisions futures ;
3. la qualité se juge sur une trajectoire et non sur une seule prédiction ;
4. un environnement réel ou simulé peut répondre aux actions.

| Projet | Méthode actuelle | Gymnasium aujourd’hui |
|---|---|---:|
| Réseau siamois | apprentissage métrique | inutile |
| Projection 512→128 | compression apprise | inutile |
| MMALS actuel | continual learning/routage | non nécessaire |
| Evidence cards | règles, LLM, schémas | non nécessaire |
| Test Authority | décision gouvernée | utilité indirecte |
| Recommandeur expérimental | Bayésien/ranking | utile pour le futur banc d’essai |
| Simulateur drone/EO-IR | contrôle séquentiel | fortement pertinent |

## 8. Gymnasium n’implique pas automatiquement RL

Une interface Gymnasium peut héberger un contrôleur non apprenant :

```python
observation, info = env.reset()

while True:
    action = classical_controller(observation)
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break
```

Sa valeur architecturale est donc plus large : normaliser les entrées/sorties, enregistrer les trajectoires, comparer des politiques, rejouer des scénarios, fixer des seeds, tester les conditions terminales, instrumenter les performances, créer des wrappers pour bruit et délais, et vectoriser les simulations.

## 9. Limites et risques

### 9.1 Reward hacking

Une politique optimise ce qui est codé, pas nécessairement ce qui était voulu. Elle pourrait maximiser les défauts trouvés en évitant les composants robustes, réduire le délai en arrêtant trop tôt, augmenter la confiance déclarée sans accroître la crédibilité, ou économiser l’énergie d’un drone en sacrifiant la couverture.

Garde-fous :

- contraintes dures séparées de la récompense ;
- critères multiples ;
- métriques de sécurité ;
- scénarios adverses ;
- tests hors distribution ;
- audit de trajectoires ;
- comparaison à des baselines ;
- revue humaine ;
- arrêt d’urgence indépendant de la politique.

### 9.2 Exploration coûteuse ou dangereuse

L’exploration est acceptable dans un simulateur mais peut être inacceptable sur un équipement réel, en biométrie citoyenne, dans une décision de release ou sur une infrastructure critique.

Approches à considérer : offline RL, imitation learning, safe RL, constrained MDP, shadow mode, SIL/HIL, enveloppes de sécurité et contrôleur de secours déterministe.

### 9.3 Sim-to-real

Un agent peut exploiter une approximation erronée du simulateur. La transition nécessite identification du modèle, calibration, domain randomization, injection de retards et de bruits, variation des paramètres, tests de sensibilité, validation des scénarios rares, comparaison simulation/réalité, surveillance en exploitation et stratégie de repli.

## 10. Positionnement recommandé

Ne pas introduire Gymnasium artificiellement dans tous les dépôts.

### Expérience A — Experimental Governance Gym

Objectif : comparer de manière reproductible plusieurs stratégies de sélection d’expériences.

Ordre recommandé :

1. politique aléatoire ;
2. règles expertes ;
3. politique myope coût/bénéfice ;
4. sélection bayésienne par gain d’information ;
5. bandit contextuel ;
6. agent RL ;
7. comparaison à des décisions humaines.

Critères : hypothèses fausses détectées, calibration, coût total, délai, risque résiduel, robustesse au changement de régime, explicabilité et escalades humaines pertinentes.

### Expérience B — Drone/EO-IR Gymnasium Adapter

Objectif : découpler le simulateur du contrôleur.

Étapes :

1. formaliser observation, action, reward et termination ;
2. implémenter une politique de référence déterministe ;
3. introduire un modèle cinématique minimal ;
4. ajouter énergie, communications et capteurs ;
5. ajouter estimation d’état et incertitude ;
6. tester perturbations et défaillances ;
7. comparer contrôle classique, planification et RL ;
8. seulement ensuite envisager une politique apprise plus complexe.

## 11. Décision d’architecture

> Gymnasium doit être vu comme un contrat expérimental normalisé entre un décideur et un monde simulé ou réel.

Il n’est ni un substitut au modèle physique, ni un algorithme d’apprentissage, ni une garantie de sécurité, ni une obligation pour tout système agentique, ni une raison suffisante d’utiliser le RL.

> Si le problème consiste à prédire sur un dataset fixe, Gymnasium est probablement superflu. Si le problème consiste à choisir une suite d’actions dont les conséquences modifient le futur, Gymnasium mérite d’être envisagé.

## 12. Fiche de révision

- **Agent :** système qui observe, décide et agit vers un objectif.
- **Agent RL :** agent dont la politique est apprise à partir de récompenses cumulées.
- **Environnement :** système qui reçoit une action et produit transition, observation et récompense.
- **Gymnasium :** API standardisée pour implémenter cette interaction.
- **Q-network :** modèle estimant Q(s,a), pas l’agent complet.
- **Politique :** mécanisme de sélection de l’action.
- **`terminated` :** vraie fin du problème.
- **`truncated` :** arrêt externe, par exemple limite de temps.
- **Usage actuel recommandé :** harness pour recommandation expérimentale et adaptateur du simulateur drone/EO-IR.
- **Non-usage justifié :** apprentissage siamois, compression et workflows documentaires ne nécessitent pas d’environnement interactif.
