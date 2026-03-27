from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor


def tune_random_forest(X_train, y_train):

    param_grid = {
        "n_estimators":[100,200],
        "max_depth":[5,10],
        "min_samples_split":[2,5]
    }

    grid_search = GridSearchCV(
        RandomForestRegressor(),
        param_grid,
        cv=3,
        scoring="r2"
    )

    grid_search.fit(X_train, y_train)

    return grid_search.best_estimator_