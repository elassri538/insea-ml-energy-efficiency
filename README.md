# Mini-projet 03 — Prédiction de la charge de chauffage

Ce projet compare cinq modèles de régression sur le jeu public **Energy Efficiency** de l’UCI. La cible est la charge de chauffage `Y1` ; `Y2` (refroidissement) n’est jamais utilisé comme prédicteur. Les données représentent 768 configurations de bâtiments simulées.

## Contenu

- `data/ENB2012_data.xlsx` : données UCI, avec l’archive téléchargée dans le même dossier.
- `src/train.py` : chargement, visualisations, séparation 80/20, validation croisée, entraînement et évaluation.
- `Projet_03_Efficacite_Energetique.ipynb` : notebook exécuté avec explications et résultats.
- `figures/` : exploration, comparaison, valeurs observées/prédites et résidus.
- `results/` : métriques, paramètres, prédictions du test et erreurs par sous-groupe.

## Reproduire

Depuis la racine du projet :

```bash
python -m venv .venv
# Sous Windows : .venv\Scripts\activate
# Sous Linux ou macOS : source .venv/bin/activate
pip install -r requirements.txt
python src/train.py
python make_notebook.py
```

Le notebook est déjà exécuté : son contenu peut être lu sans relancer ces commandes. La régression linéaire sert de référence. Ridge, KNN, arbre de décision et Random Forest font chacun l’objet d’une recherche d’hyperparamètres par validation croisée à cinq plis sur les 614 observations d’entraînement. La configuration est choisie par le RMSE moyen de validation ; les métriques finales sont calculées sur les 154 observations de test.

Les variables `X6` (orientation) et `X8` (distribution des vitrages) sont traitées comme catégories par encodage indicateur. Les autres variables sont standardisées pour les modèles sensibles à l’échelle, dans des pipelines qui évitent les fuites entre plis.

**Source des données :** UCI Machine Learning Repository, *Energy Efficiency*, dataset 242, https://archive.ics.uci.edu/dataset/242/energy+efficiency. Données simulées ; les résultats ne démontrent pas une performance sur des bâtiments réels.

## Rapport LaTeX

`report/rapport.tex` est le document principal ; `report/page_de_garde.tex` contient la couverture adaptée au mini-projet 03. Les images du rapport sont dans `figures/` et le logo INSEA dans `report/figures/logos/`. Le PDF compilé est `report/rapport.pdf` (quatre pages, couverture comprise).

Pour recompiler depuis `report/` :

```bash
pdflatex -interaction=nonstopmode -halt-on-error rapport.tex
pdflatex -interaction=nonstopmode -halt-on-error rapport.tex
```

La couverture reprend les éléments graphiques verts du modèle fourni, avec le titre de ce mini-projet et les trois membres du groupe. Le nom d'encadrant et le logo OCP ont été retirés conformément aux indications du groupe.

## Présentation

`Presentation_Projet_03.pptx` contient huit diapositives et des notes orales. Elle reprend le style général de la présentation fournie (ouverture et conclusion bleu nuit, pages claires, accents verts, cartes et numérotation) avec uniquement le contenu du projet énergétique. Les figures sont intégrées directement dans le PowerPoint. Le générateur éditable est `create_presentation.py`.
