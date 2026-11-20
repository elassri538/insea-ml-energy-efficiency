# Modèle réutilisable de rapport INSEA / HCP

Ce dossier contient uniquement les éléments de mise en forme nécessaires pour donner à un futur agent IA le contexte visuel d'une page de garde de rapport INSEA. Il ne contient aucun contenu, résultat ou auteur d'un projet précédent.

## Fichiers

- `pages/page_de_garde.tex` : page de garde LaTeX à inclure avec `\input{pages/page_de_garde}`.
- `figures/logos/hcp.jpg` : visuel du Haut-Commissariat au Plan.
- `figures/logos/INSEA_logo.png` : logo INSEA.
- `main.tex` : exemple minimal compilable, avec les champs à personnaliser.
- `apercu.pdf` : aperçu du modèle avec des textes de remplacement.

## Pour l'utiliser

1. Copiez ce dossier dans un nouveau projet, ou reprenez `pages/` et `figures/logos/` à sa racine.
2. Modifiez dans le préambule de `main.tex` le type de rapport, le titre, les auteurs, la filière, l'année et, si nécessaire, l'encadrant. Laissez `\ReportSupervisor` vide si le projet n'en a pas.
3. Remplacez le texte d'exemple après la page de garde par le contenu du nouveau rapport.
4. Compilez depuis la racine : `pdflatex -interaction=nonstopmode -halt-on-error main.tex`.

Les packages LaTeX requis figurent dans `main.tex`. Les chemins des images sont relatifs à la racine du document principal. Le modèle suppose une page A4. Pour l'intégrer à un rapport déjà existant, conservez les quatre couleurs et les packages du préambule, puis incluez seulement `pages/page_de_garde.tex`.

## Consigne à transmettre à un agent IA

« Utilise ce dossier uniquement comme référence de mise en page pour le nouveau rapport. Remplace tous les champs d'exemple par les informations de mon nouveau projet. Ne reprends aucun titre, nom, résultat ou contenu d'un autre projet. »

## Provenance des visuels

- HCP : visuel institutionnel publié par [OEC Maroc](https://oec.ma/actualite/ychi92u22dhjkcectv8egdq3).
- INSEA : logo affiché par le [compte INSEA_Rabat](https://x.com/INSEA_Rabat).

Pour une diffusion officielle, vérifiez que les visuels correspondent aux versions institutionnelles exigées par votre établissement.
