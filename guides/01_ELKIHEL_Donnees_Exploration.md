# Elkihel Elmehdi — le problème, les données et les graphiques

**Tes diapositives : 1, 2 et 3. Durée prévue : 1 min 50.** Ce guide explique ce que tu présentes. Le fichier `scripts_oraux/01_ELKIHEL.pdf` contient uniquement ton texte à mémoriser. Les calculs et les graphiques ont déjà été exécutés ; tu n’as rien à lancer pour préparer l’oral.

## 1. De quoi parle ce projet ?

On cherche à prédire **la charge de chauffage d’un bâtiment** : la quantité de chaleur nécessaire pour maintenir une température intérieure dans les configurations simulées du jeu étudié. Le nombre à prédire s’appelle **Y1**. Comme il s’agit d’un nombre et non d’une catégorie, le problème est une **régression**. On compare cinq méthodes pour voir laquelle donne les prédictions les plus proches de Y1.

Ce projet est un exercice de machine learning sur des simulations. Il ne démontre pas que les modèles fonctionneraient aussi bien sur des bâtiments réels.

## 2. Qu’y a-t-il dans les données ?

Le jeu *Energy Efficiency* de l’UCI contient **768 lignes**. Chaque ligne est une configuration de bâtiment. Il n’y a **aucune valeur manquante**. Les **8 entrées X1 à X8** décrivent le bâtiment ; **Y1** est la réponse que l’on veut prédire. Une autre colonne, **Y2**, correspond à la charge de refroidissement : elle est exclue du projet et ne sert jamais d’entrée.

| Colonne | Signification simple |
|---|---|
| X1 | Compacité relative : une indication de la forme du bâtiment |
| X2 | Surface globale |
| X3 | Surface des murs |
| X4 | Surface du toit |
| X5 | Hauteur totale |
| X6 | Orientation |
| X7 | Surface vitrée |
| X8 | Répartition des vitrages |
| Y1 | Charge de chauffage à prédire |

**Entrée** veut dire information fournie au modèle. **Cible** veut dire réponse qu’il doit apprendre à prévoir. En Python, le tableau des entrées est souvent appelé `X`, et la cible `y`.

## 3. Comment expliquer les trois premières diapositives ?

**Diapositive 1 :** annoncer le sujet et les trois membres. Ne lis pas simplement le titre : dis que l’objectif est de comparer des méthodes de prédiction sur un même jeu de données.

**Diapositive 2 :** montrer la question centrale : « Quel modèle prédit le plus précisément Y1, et où apparaissent les erreurs ? » Explique les trois nombres : 768 configurations, huit caractéristiques et une seule cible. Précise que Y2 n’est pas utilisée.

**Diapositive 3 :** montrer le graphique `figures/01_exploration.png`. Le premier panneau est un **histogramme** : il compte combien de bâtiments ont une charge Y1 dans chaque intervalle. Les autres panneaux sont des **nuages de points** : un point représente une configuration ; sa position horizontale est une caractéristique et sa position verticale est Y1. Si les points forment une forme courbe ou plusieurs groupes, une relation linéaire simple peut être insuffisante. Ce dessin ne prouve pas qu’une variable cause directement une variation de Y1.

## 4. Mots à savoir expliquer sans lire

- **Observation** : une ligne du tableau, donc une configuration simulée.
- **Caractéristique** : une information X1 à X8 donnée au modèle.
- **Régression** : prédire une valeur numérique.
- **Modèle** : une méthode qui apprend des relations à partir d’exemples.
- **Valeur manquante** : case vide ou inconnue dans le tableau. Ici, il n’y en a pas.
- **Simulation** : données produites par un calcul ou un logiciel, plutôt que mesurées sur un bâtiment réel.

## 5. Où regarder pour vérifier ?

Ouvre `data/ENB2012_data.xlsx` pour voir les colonnes, `Projet_03_Efficacite_Energetique.ipynb` pour voir leur résumé, `figures/01_exploration.png` pour le graphique et `src/train.py` pour la fonction `load_data`. Tu n’as pas besoin de comprendre toute la syntaxe Python : vérifie d’abord que les noms des colonnes correspondent au tableau ci-dessus.

## 6. Questions possibles du jury

**Pourquoi Y2 est-elle écartée ?** Le sujet demande de prédire uniquement la charge de chauffage Y1. Y2 est une autre sortie du jeu, la charge de refroidissement.

**Pourquoi ce problème n’est-il pas une classification ?** La réponse est un nombre de charge de chauffage, et non une étiquette comme « oui » ou « non ».

**Les graphiques prouvent-ils qu’une variable cause la charge ?** Non. Ils montrent seulement des associations dans les configurations simulées.

Pour t’entraîner, explique la diapositive 2 sans employer le mot « modèle » plus d’une fois : l’objectif est que quelqu’un qui découvre le sujet comprenne les données.
