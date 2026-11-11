# L’Houcine — comprendre ta partie depuis zéro

**Tu présentes les diapositives 4 et 5.** Ton texte oral est dans [ton PDF](../scripts_oraux/02_EL_ASSRI.pdf). Commence par lire les sections 1 à 4 ci-dessous, puis regarde les deux diapositives. Tu n’as aucun code à exécuter pour réviser.

## 1. L’idée du projet en une minute

Imagine un tableau de bâtiments. Pour chaque bâtiment, nous connaissons sa forme, sa surface, sa hauteur, son orientation et ses vitrages. Nous connaissons aussi la **charge de chauffage**, appelée **Y1**. Le but est d’apprendre, à partir des bâtiments connus, à estimer Y1 pour un autre bâtiment.

Un **modèle de machine learning** est simplement une méthode qui repère des relations dans les exemples connus et les réutilise pour faire une prédiction. Ici, la réponse est un nombre : c’est un problème de **régression**. Les données représentent des bâtiments **simulés**.

Exemple inventé pour comprendre :

| Bâtiment | Surface | Hauteur | Charge de chauffage connue |
|---|---:|---:|---:|
| A | 500 | 3,5 | 15 |
| B | 520 | 3,5 | 17 |
| C | 700 | 7 | 32 |

Si un nouveau bâtiment ressemble à A et B, une méthode pourrait prédire une charge proche de 16. **Ces trois lignes sont un exemple pédagogique ; elles ne sont pas les résultats du projet.** Dans le vrai projet, chaque bâtiment possède huit caractéristiques X1 à X8 et le tableau compte 768 lignes.

## 2. Ta diapositive 4 : comment vérifier que le modèle sait prédire ?

Pense à un contrôle à l’école. Tu révises sur des exercices, puis tu passes un examen avec d’autres exercices. Si tu connais déjà les réponses de l’examen, ta note ne mesure plus ce que tu as appris.

Nous appliquons la même règle :

- **614 bâtiments pour l’entraînement** : les modèles apprennent sur ces exemples. On y choisit aussi leurs réglages.
- **154 bâtiments pour le test** : on garde ces exemples à part jusqu’à la fin pour voir si les prédictions fonctionnent sur des cas non utilisés pour apprendre.

Le nombre `42` dans `random_state=42` fixe le tirage aléatoire. Il permet de retrouver les mêmes deux groupes lors d’une nouvelle exécution. **42 n’est pas un score et n’améliore pas la qualité des prédictions.**

### Que signifie « validation croisée à cinq plis » ?

Nous devons comparer plusieurs réglages d’un modèle. Pour cela, nous partageons les **614 bâtiments d’entraînement** en **cinq parties**, appelées *plis*. Le modèle apprend sur quatre parties et nous contrôlons ses prédictions sur la cinquième. Nous répétons cinq fois, en changeant la partie de contrôle. Le score moyen indique quel réglage fonctionne le mieux dans l’entraînement.

Cette validation se déroule **avant** le test final. Elle sert à choisir les réglages ; les 154 bâtiments de test ne participent pas au choix.

### Que mesure le RMSE ?

Si la vraie charge vaut 20 et que le modèle prédit 18, il se trompe de 2. Si la vraie charge vaut 30 et qu’il prédit 34, il se trompe de 4. Le **RMSE** résume les écarts sur tous les bâtiments en donnant davantage de poids aux grosses erreurs. **Plus le RMSE est faible, mieux les prédictions sont proches des valeurs connues.**

La validation croisée choisit les réglages avec le **plus petit RMSE moyen**. Le RMSE du test est calculé ensuite pour évaluer le résultat final.

### Que sont « scaler », « encodage » et « pipeline » ?

Tu peux comprendre la diapositive sans réciter ces mots. Voici leur sens :

- **Standardiser** ou utiliser un *scaler* : mettre des variables numériques sur des échelles comparables. La surface peut être de plusieurs centaines, tandis qu’une proportion de vitrage est entre 0 et 1. Sans précaution, une méthode basée sur les distances peut donner trop de poids à la surface.
- **Encoder une catégorie** : traduire une étiquette telle que l’orientation en colonnes utilisables par le modèle, sans prétendre qu’une orientation numérotée 4 est « deux fois » une orientation numérotée 2.
- **Pipeline** : ranger les étapes dans le bon ordre : préparer les données, puis entraîner le modèle. Pendant la validation, la préparation est apprise seulement sur les exemples utilisés pour l’entraînement du pli. Cela évite une **fuite de données**, c’est-à-dire l’utilisation indirecte d’informations venant des exemples à évaluer.

La régression linéaire, Ridge et KNN utilisent la standardisation. Les deux méthodes à base d’arbres n’en ont pas besoin dans ce projet. L’orientation X6 et la répartition des vitrages X8 sont traitées comme des catégories.

## 3. Ta diapositive 5 : comprendre les cinq modèles

Ne cherche pas à apprendre leurs formules. Comprends l’image mentale de chacun :

| Modèle | Image facile à retenir | Ce qu’il fait ici |
|---|---|---|
| **Régression linéaire** | Une règle simple qui combine les mesures | Sert de référence pour comparer les autres |
| **Ridge** | La même règle, avec un frein sur les coefficients trop grands | Essaie d’éviter une règle trop sensible aux données apprises |
| **KNN** | « Quels bâtiments connus ressemblent le plus à celui-ci ? » | Regarde les cinq voisins retenus, puis combine leurs charges |
| **Arbre de décision** | Un jeu de questions « si… alors… » | Suit des questions sur les mesures jusqu’à une prédiction |
| **Random Forest** | Plusieurs arbres dont les résultats sont combinés | Utilise 200 arbres dans le réglage retenu |

**Attention à la confusion fréquente :** « KNN utilise cinq voisins » ne veut pas dire « cinq caractéristiques ». Il compare les bâtiments avec les **huit caractéristiques**, puis retient **cinq bâtiments voisins**.

La régression linéaire sert de point de départ. Pour Ridge, KNN, l’arbre et Random Forest, la validation croisée compare plusieurs réglages possibles. Par exemple, pour KNN, elle compare plusieurs nombres de voisins. Le code conserve les réglages gagnants dans `results/parameters.json`.

## 4. Les trois phrases essentielles à savoir dire

1. « Nous avons utilisé 614 bâtiments pour apprendre et 154 pour vérifier les prédictions à la fin. »
2. « Sur les 614 bâtiments, la validation croisée à cinq plis sert à choisir les réglages avec l’erreur RMSE la plus faible. »
3. « Nous comparons cinq modèles : régression linéaire, Ridge, KNN, arbre de décision et Random Forest. »

Si tu comprends ces trois phrases, tu peux déjà expliquer le cœur de tes diapositives. Tu peux ensuite ajouter que la préparation des variables se fait à l’intérieur de la validation pour éviter une fuite de données.

## 5. Où regarder dans les fichiers ?

- `Presentation_Projet_03.pptx` : tes diapositives 4 et 5.
- `scripts_oraux/02_EL_ASSRI.pdf` : le texte à dire, simplifié pour l’oral.
- `results/parameters.json` : les réglages retenus pour les modèles.
- `src/train.py` : `train_test_split` coupe les données ; `make_searches` définit les cinq modèles. Tu n’as pas besoin de savoir écrire ces fonctions pour expliquer leur rôle.

## 6. Questions possibles du jury

**Pourquoi ne pas donner les 768 lignes au modèle pour apprendre ?** Il faut garder 154 exemples de côté pour vérifier le résultat final.

**Pourquoi cinq plis ?** Pour comparer les réglages sur plusieurs parties de l’entraînement au lieu de dépendre d’une seule petite partie. Cinq est le choix utilisé dans cette expérience.

**Pourquoi un petit RMSE est-il bon ?** Parce qu’il signifie que les charges prédites sont, globalement, proches des charges connues.

**Quelle différence entre KNN et Random Forest ?** KNN cherche des bâtiments similaires ; Random Forest combine les prédictions de nombreux arbres de questions.

**Est-ce que vous avez utilisé Y2 ?** Non. Le sujet porte uniquement sur la charge de chauffage Y1 ; Y2 correspond au refroidissement.

**Si tu bloques à l’oral :** reviens au dessin « 614 pour apprendre → cinq plis pour choisir → 154 pour tester ». Il résume ta partie.
