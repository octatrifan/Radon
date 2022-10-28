from SVM import *
from sklearn.model_selection import GridSearchCV

import pandas as pd


def grid_search():
    params = [{'scaler': (StandardScaler(), MaxAbsScaler(), MinMaxScaler()),
               'svr__C': [0.001, 0.01, 0.1, 0.3, 0.5, 1, 10, 100, 300, 1000],
               'svr__gamma': ['auto', 'scale'],
               'svr__kernel': ['rbf', ],
               },
              {'scaler': (StandardScaler(), MaxAbsScaler(), MinMaxScaler()),
               'svr__C': [0.001, 0.01, 0.1, 0.3, 0.5, 1, 10, 100, 200],
               'svr__gamma': ['auto', 'scale'],
               'svr__kernel': ['sigmoid', ],
               'svr__coef0': [0.001, 0.1, 0.5, 1, 2],
               },
              {'scaler': (StandardScaler(), MaxAbsScaler(), MinMaxScaler()),
               'svr__C': [0.001, 0.01, 0.1, 0.3, 0.5, 1],
               'svr__gamma': ['auto', 'scale'],
               'svr__kernel': ['poly', ],
               'svr__degree': [4, 5],
               'svr__coef0': [0.001, 0.1, 0.5],
               },
              {'scaler': (StandardScaler(), MaxAbsScaler(), MinMaxScaler()),
               'svr__C': [100, 10],
               'svr__tol': [0.1, ],
               'svr__gamma': ['auto', 'scale'],
               'svr__kernel': ['poly', ],
               'svr__degree': [4],
               'svr__coef0': [0.001, 0.1],
               },
              ]

    pipe = Pipeline([('scaler', StandardScaler()), ('svr', SVR())])
    return GridSearchCV(pipe, params, n_jobs=-1, refit=True, verbose=verbose, scoring='r2')


def get_top_results(results_map, count):
    zipped_values = list(zip(*results_map.values()))
    models_map = [dict(zip(results_map.keys(), line)) for line in zipped_values]
    return sorted(models_map, key=lambda x: x['rank_test_score'])[:count]


if __name__ == "__main__":
    grid = grid_search()
    grid.fit(X_train, y_train)
    print(grid.best_params_)

    top = get_top_results(grid.cv_results_, 40)
    dataframe = pd.DataFrame([line.values() for line in top], columns=top[0].keys())
    print(dataframe.to_string())

    print("Final best score:", grid.score(X_test, y_test))

    """
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=dataframe.values, colLabels=dataframe.columns, loc='center')
    fig.tight_layout()
    plt.savefig('table.png', dpi=1200)
    """
