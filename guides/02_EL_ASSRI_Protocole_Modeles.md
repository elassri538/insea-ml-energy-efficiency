# El Assri L’Houcine — le protocole et les cinq modèles

**Tes diapositives : 4 et 5. Durée prévue : 2 min 05.** Ton PDF `scripts_oraux/02_EL_ASSRI.pdf` contient ton texte oral. Ce guide t’aide à comprendre pourquoi les résultats peuvent être considérés comme une comparaison loyale. Aucun calcul n’est à relancer pour apprendre cette partie.

## 1. Apprendre puis vérifier

Le jeu contient 768 configurations. On en garde **614 pour l’entraînement** et **154 pour le test**. Les 614 servent à apprendre et à choisir les réglages ; les 154 servent à vérifier le résultat final sur des exemples mis de côté. La séparation est aléatoire, avec `random_state=42`, ce qui permet de la reproduire.

Pense à un étudiant : il révise sur des exercices, puis passe un examen composé d’autres exercices. Regarder les réponses de l’examen pendant les révisions fausserait l’évaluation. Pour un modèle, ce serait une **fuite de données**.

## 2. Qu’est-ce que la validation croisée ?

Dans les 614 observations d’entraînement, on forme **cinq parties** appelées *plis*. Pour un réglage donné, le modèle apprend sur quatre plis et est contrôlé sur le cinquième. On recommence jusqu’à ce que chaque pli ait servi au contrôle. Le résultat moyen aide à choisir les paramètres.

Le critère retenu est le **RMSE** moyen. C’est une mesure de l’écart entre les charges prédites et réelles : **plus le RMSE est petit, mieux c’est**. Les scores des 154 observations de test ne servent pas au choix des paramètres.

Un **hyperparamètre** est un réglage choisi pour construire le modèle, par exemple le nombre de voisins de KNN. `GridSearchCV` essaie les valeurs prévues et choisit celles qui obtiennent le meilleur score moyen sur les cinq plis.

## 3. Pourquoi transformer certaines variables ?

Les entrées numériques n’ont pas toutes la même échelle. La **standardisation** retire la moyenne d’une variable et divise par son écart-type. Elle évite qu’une grande unité numérique domine une méthode sensible aux distances. Nous l’utilisons pour la régression linéaire, Ridge et KNN, à l’intérieur des pipelines.

X6, l’orientation, et X8, la répartition des vitrages, sont des **catégories** : les chiffres qui les codent ne représentent pas forcément des distances. Un encodage crée une colonne indicatrice pour chaque catégorie. Les arbres utilisent cet encodage mais n’ont pas besoin du scaler pour les autres variables.

Un **pipeline** relie transformation et modèle. À chaque pli, la transformation est calculée seulement sur la partie utilisée pour apprendre. Cela protège la comparaison contre une fuite depuis la partie de validation.

## 4. Les cinq modèles en langage courant

| Modèle | Idée simple | Réglage retenu |
|---|---|---|
| Régression linéaire | Cherche une combinaison des caractéristiques qui forme une droite ou un plan de prédiction | Référence sans réglage |
| Ridge | Régression linéaire avec une pénalité qui freine les coefficients trop grands | `alpha=0,1` |
| KNN | Regarde les configurations les plus proches, puis combine leurs Y1 | 5 voisins, distance Manhattan, poids égaux |
| Arbre de décision | Pose des questions successives sur les caractéristiques | Profondeur 8, au moins 2 cas par feuille |
| Random Forest | Combine les prédictions de nombreux arbres différents | 200 arbres, profondeur 10, au moins 1 cas par feuille |

Une **droite** est une image facile à comprendre pour la régression linéaire ; en réalité, le modèle combine plusieurs variables. KNN n’emploie pas cinq variables : il utilise les huit caractéristiques, puis retient cinq **observations voisines**. Random Forest ne signifie pas que les arbres sont choisis n’importe comment : leur construction introduit de l’aléatoire contrôlé afin de diversifier leurs prédictions.

## 5. Que dire sur les diapositives ?

**Diapositive 4 :** explique le parcours « séparer → valider → évaluer ». Souligne que le test reste à part jusqu’à la fin. Les chiffres à mémoriser sont **614**, **154** et **5 plis**.

**Diapositive 5 :** présente les cinq modèles en partant de la référence linéaire. Ridge, KNN, arbre et Random Forest ont été réglés par validation croisée. Dis une phrase simple pour chacun, puis passe la parole à Said pour les résultats.

## 6. Où lire les preuves dans le projet ?

Dans `src/train.py`, `train_test_split` réalise la séparation, `make_preprocessor` prépare les variables, `make_searches` définit les cinq modèles et `GridSearchCV` effectue les recherches. `results/parameters.json` contient les réglages effectivement choisis. Le notebook présente les étapes dans le même ordre.

## 7. Questions possibles du jury

**Pourquoi ne pas entraîner sur les 768 cas ?** Parce qu’il faut conserver des exemples non utilisés dans l’apprentissage pour estimer les performances finales.

**Pourquoi 42 ?** C’est une graine aléatoire pour reproduire le découpage. Le nombre 42 n’améliore pas le modèle.

**Pourquoi standardiser KNN ?** Il compare des distances entre observations ; des variables ayant de grandes unités pourraient dominer ces distances.

**Pourquoi les arbres n’ont-ils pas de scaler ?** Ils comparent chaque variable à des seuils et n’utilisent pas une distance globale comme KNN.

Entraîne-toi à dessiner sur papier les trois étapes « 614 train → 5 plis → 154 test » et à les expliquer sans lire.
