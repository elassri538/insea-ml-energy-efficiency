"""Mini-projet 03 : prédiction reproductible de la charge de chauffage Y1."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

ROOT = Path(__file__).resolve().parents[1]
FEATURES = [f'X{i}' for i in range(1, 9)]
NUMERIC = [f'X{i}' for i in (1, 2, 3, 4, 5, 7)]
CATEGORICAL = ['X6', 'X8']  # orientation et distribution des vitrages
LABELS = {
    'X1': 'Compacité relative', 'X2': 'Surface', 'X3': 'Surface des murs',
    'X4': 'Surface du toit', 'X5': 'Hauteur totale', 'X6': 'Orientation',
    'X7': 'Surface vitrée', 'X8': 'Distribution des vitrages',
}


def load_data():
    data = pd.read_excel(ROOT / 'data' / 'ENB2012_data.xlsx')
    expected = FEATURES + ['Y1', 'Y2']
    if data.shape != (768, 10) or data.columns.tolist() != expected:
        raise ValueError(f'Structure inattendue : {data.shape}, {data.columns.tolist()}')
    if data[expected].isna().any().any():
        raise ValueError('Valeurs manquantes dans les données.')
    return data


def make_preprocessor(scale):
    return ColumnTransformer([
        ('numeric', StandardScaler() if scale else 'passthrough', NUMERIC),
        ('categorical', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL),
    ])


def make_searches():
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    specs = {
        'Régression linéaire': (LinearRegression(), {}, True),
        'Ridge': (Ridge(), {'model__alpha': [0.01, 0.1, 1, 10, 100]}, True),
        'KNN': (KNeighborsRegressor(), {
            'model__n_neighbors': [3, 5, 7, 11, 15],
            'model__weights': ['uniform', 'distance'],
            'model__p': [1, 2],
        }, True),
        'Arbre de décision': (DecisionTreeRegressor(random_state=42), {
            'model__max_depth': [3, 5, 8, 12, None],
            'model__min_samples_leaf': [1, 2, 5],
        }, False),
        'Random Forest': (RandomForestRegressor(random_state=42, n_jobs=1), {
            'model__n_estimators': [100, 200],
            'model__max_depth': [5, 10, None],
            'model__min_samples_leaf': [1, 2],
        }, False),
    }
    searches = {}
    for name, (model, params, scale) in specs.items():
        pipe = Pipeline([('preprocess', make_preprocessor(scale)), ('model', model)])
        searches[name] = (GridSearchCV(pipe, params, cv=cv, scoring='neg_root_mean_squared_error', n_jobs=1)
                          if params else pipe)
    return searches


def plot_eda(data):
    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    axes[0, 0].hist(data.Y1, bins=25, color='#236d83')
    axes[0, 0].set(xlabel='Y1 : charge de chauffage', ylabel='Nombre', title='Distribution de Y1')
    for ax, col in zip(axes.flat[1:], ['X1', 'X2', 'X4', 'X5', 'X7']):
        ax.scatter(data[col], data.Y1, s=14, alpha=.4)
        ax.set(xlabel=f'{col} : {LABELS[col]}', ylabel='Y1', title=f'Y1 selon {col}')
    fig.tight_layout()
    fig.savefig(ROOT / 'figures' / '01_exploration.png', dpi=160)
    plt.close(fig)


def plot_results(scores, predictions, y_test, selected_model):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].bar(scores.Model, scores.RMSE, color='#236d83')
    axes[0].set(ylabel='RMSE (plus faible = mieux)', title='Erreur quadratique moyenne')
    axes[1].bar(scores.Model, scores.R2, color='#369c75')
    axes[1].set(ylabel='R² (plus proche de 1 = mieux)', title='Variance expliquée')
    for ax in axes: ax.tick_params(axis='x', rotation=25)
    fig.tight_layout()
    fig.savefig(ROOT / 'figures' / '02_comparaison.png', dpi=160)
    plt.close(fig)

    selected = ['Régression linéaire', selected_model]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    for ax, name in zip(axes, selected):
        ax.scatter(y_test, predictions[name], s=22, alpha=.7)
        lo = min(y_test.min(), predictions[name].min())
        hi = max(y_test.max(), predictions[name].max())
        ax.plot([lo, hi], [lo, hi], '--', color='black')
        ax.set(xlabel='Y1 observée', ylabel='Y1 prédite', title=name)
    fig.tight_layout()
    fig.savefig(ROOT / 'figures' / '03_observe_predit.png', dpi=160)
    plt.close(fig)

    best = selected_model
    residuals = np.asarray(y_test) - predictions[best]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    axes[0].scatter(predictions[best], residuals, s=22, alpha=.7)
    axes[0].axhline(0, color='black', linestyle='--')
    axes[0].set(xlabel='Y1 prédite', ylabel='Observée − prédite', title='Résidus selon la prédiction')
    axes[1].hist(residuals, bins=20, color='#236d83')
    axes[1].set(xlabel='Observée − prédite', ylabel='Nombre', title='Distribution des résidus')
    fig.suptitle(f'Meilleur modèle selon RMSE CV : {best}')
    fig.tight_layout()
    fig.savefig(ROOT / 'figures' / '04_residus.png', dpi=160)
    plt.close(fig)


def main():
    (ROOT / 'results').mkdir(exist_ok=True)
    (ROOT / 'figures').mkdir(exist_ok=True)
    data = load_data()
    plot_eda(data)
    # Y2 est volontairement absent des prédicteurs.
    X_train, X_test, y_train, y_test = train_test_split(
        data[FEATURES], data['Y1'], test_size=.2, random_state=42)
    rows, predictions, parameters = [], {}, {}
    for name, estimator in make_searches().items():
        estimator.fit(X_train, y_train)
        fitted = estimator.best_estimator_ if isinstance(estimator, GridSearchCV) else estimator
        params = estimator.best_params_ if isinstance(estimator, GridSearchCV) else {}
        cv_rmse = (-estimator.best_score_ if isinstance(estimator, GridSearchCV)
                   else -cross_val_score(estimator, X_train, y_train, cv=KFold(5, shuffle=True, random_state=42),
                                         scoring='neg_root_mean_squared_error', n_jobs=1).mean())
        pred = fitted.predict(X_test)
        predictions[name] = pred
        parameters[name] = params
        rows.append({'Model': name, 'CV_RMSE': cv_rmse,
                     'MAE': mean_absolute_error(y_test, pred),
                     'MSE': mean_squared_error(y_test, pred),
                     'RMSE': np.sqrt(mean_squared_error(y_test, pred)),
                     'R2': r2_score(y_test, pred)})
        print(f'{name}: CV_RMSE={cv_rmse:.3f}, test_RMSE={rows[-1]["RMSE"]:.3f}, R2={rows[-1]["R2"]:.3f}; {params}', flush=True)
    scores = pd.DataFrame(rows).sort_values('CV_RMSE').reset_index(drop=True)
    selected_model = scores.iloc[0].Model
    scores.to_csv(ROOT / 'results' / 'metrics.csv', index=False)
    pd.DataFrame({'Y1_observee': y_test.to_numpy(), **{name: pred for name, pred in predictions.items()}}).to_csv(
        ROOT / 'results' / 'predictions_test.csv', index=False)
    with (ROOT / 'results' / 'parameters.json').open('w', encoding='utf-8') as f:
        json.dump(parameters, f, ensure_ascii=False, indent=2)
    plot_results(scores, predictions, y_test, selected_model)
    # Analyse descriptive des erreurs sur le test : ces groupes ne servent pas au réglage.
    absolute_error = np.abs(y_test.to_numpy() - predictions[selected_model])
    groups = []
    for feature in ['X5', 'X6', 'X7', 'X8']:
        for value, part in X_test.groupby(feature):
            loc = X_test.index.get_indexer(part.index)
            groups.append({'Caracteristique': feature, 'Valeur': value, 'Effectif': len(loc),
                           'MAE': float(absolute_error[loc].mean())})
    pd.DataFrame(groups).to_csv(ROOT / 'results' / 'erreurs_par_groupe.csv', index=False)
    print(f'Entraînement: {len(X_train)} ; test: {len(X_test)} ; modèle sélectionné par CV: {selected_model}', flush=True)
    return scores


if __name__ == '__main__':
    main()
