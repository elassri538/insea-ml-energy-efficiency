# Said Charaf — lire les résultats, les erreurs et conclure

**Tes diapositives : 6, 7 et 8. Durée prévue : 2 min 05.** Ton texte oral est dans `scripts_oraux/03_SAID.pdf`. Cette partie répond à la question centrale du sujet avec les chiffres réellement calculés.

## 1. Les quatre mesures à connaître

Une **erreur** est la différence entre la charge observée Y1 et la charge prédite. Les mesures ci-dessous résument les erreurs sur les **154 observations de test**.

| Mesure | Signification pratique | Sens favorable |
|---|---|---|
| MAE | Moyenne des écarts absolus : taille moyenne des erreurs sans tenir compte de leur signe | Plus petit |
| MSE | Moyenne des erreurs mises au carré : les grosses erreurs pèsent davantage | Plus petit |
| RMSE | Racine du MSE : une erreur exprimée dans l’unité de Y1 | Plus petit |
| R² | Compare le modèle à une prédiction constante égale à la moyenne | Plus proche de 1 |

La **MAE** répond à « de combien se trompe-t-on en moyenne ? ». Le **RMSE** réagit plus fortement aux grandes erreurs. **R² = 0,997** indique une très bonne adéquation sur ce jeu de test ; ce n’est pas une garantie de 99,7 % d’exactitude sur tous les bâtiments.

Le préfixe **CV** dans « RMSE CV » signifie *validation croisée*. Ce score est obtenu sur les 614 observations d’entraînement et sert à choisir le modèle. Les autres chiffres sont calculés sur les 154 observations de test.

## 2. Le tableau des cinq modèles

| Modèle | RMSE CV | MAE test | MSE test | RMSE test | R² test |
|---|---:|---:|---:|---:|---:|
| Régression linéaire | 2,828 | 2,059 | 8,250 | 2,872 | 0,921 |
| Ridge | 2,828 | 2,061 | 8,257 | 2,874 | 0,921 |
| KNN | 1,559 | 1,118 | 2,793 | 1,671 | 0,973 |
| Arbre de décision | 0,579 | **0,353** | **0,282** | **0,531** | **0,997** |
| Random Forest | **0,535** | 0,371 | 0,287 | 0,536 | 0,997 |

Les méthodes non linéaires, en particulier l’arbre et Random Forest, réussissent mieux que les modèles linéaires sur cette expérience. **Random Forest est sélectionné par la validation croisée**, car son RMSE CV de 0,535 est le plus petit. Sur le test, l’arbre a un RMSE légèrement plus petit, 0,531 contre 0,536. Cet écart minime sur un seul test ne suffit pas à déclarer un gagnant universel.

## 3. Comment expliquer les graphiques ?

**Diapositive 6 :** les graphiques à barres comparent RMSE et R² pour les cinq modèles. L’axe RMSE doit descendre, tandis que R² doit monter. Les nombres exacts sont conservés dans `results/metrics.csv` et dans le rapport.

**Diapositive 7 :** à gauche, le graphique « observé / prédit » place la vraie valeur de Y1 sur l’axe horizontal et la prédiction sur l’axe vertical. Plus un point est près de la diagonale, plus sa prédiction est proche. La référence linéaire est montrée à côté de Random Forest pour visualiser la différence.

À droite, un **résidu** est `valeur observée − valeur prédite`. Un résidu positif veut dire que le modèle a sous-estimé la charge ; un résidu négatif veut dire qu’il l’a surestimée. Une répartition autour de zéro est souhaitable. L’histogramme montre combien de résidus tombent dans chaque intervalle.

## 4. Quelles caractéristiques influencent les erreurs ?

Le fichier `results/erreurs_par_groupe.csv` décrit l’erreur absolue moyenne de Random Forest pour certaines valeurs de X5, X6, X7 et X8. Pour **X5 = 3,5**, la MAE est **0,171** sur 72 cas ; pour **X5 = 7**, elle est **0,546** sur 82 cas.

On peut dire que les erreurs observées **diffèrent entre ces sous-groupes**. On ne peut pas conclure que la hauteur seule cause cette différence : d’autres caractéristiques peuvent changer en même temps. Certains sous-groupes sont petits, par exemple seulement huit cas pour X7 = 0.

## 5. Les limites et la conclusion

Ces bâtiments sont **simulés**. Le test est une seule sélection aléatoire de 154 cas provenant du même jeu. Les résultats ne prouvent pas une performance identique sur des bâtiments réels. Avant toute application pratique, il faudrait évaluer le modèle sur des données indépendantes de bâtiments réels.

La conclusion à dire est précise : « Dans notre expérience, Random Forest a obtenu le meilleur RMSE de validation croisée. L’arbre de décision et la forêt obtiennent les meilleurs résultats sur le test, avec des écarts très faibles. »

**Diapositive 8 :** rappelle ce résultat, la limite des simulations et remercie le jury. N’annonce pas que le projet a construit un logiciel utilisable directement dans un bâtiment.

## 6. Questions possibles du jury

**Pourquoi choisir Random Forest alors que l’arbre a un RMSE test légèrement inférieur ?** Parce que le choix a été défini avec la validation croisée sur l’entraînement. Utiliser le test pour changer ce choix fausserait son rôle d’évaluation finale.

**Que signifie un résidu négatif ?** La prédiction est plus grande que la valeur observée : le modèle surestime Y1.

**Est-ce que R² = 0,997 signifie « 99,7 % de prédictions correctes » ?** Non. R² est une mesure de la réduction de l’erreur quadratique par rapport à la moyenne sur ce test.

**Que manque-t-il pour une application réelle ?** Une validation sur des bâtiments réels et sur d’autres conditions que celles des 768 configurations simulées.

Pour t’entraîner, cache le tableau et explique de mémoire pourquoi les colonnes « RMSE CV » et « RMSE test » n’ont pas le même rôle.
