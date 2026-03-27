import pandas as pd
from sklearn.model_selection import train_test_split

from src.preprocessing import load_data, preprocess_data
from src.ml_models import train_random_forest, train_xgboost, train_neural_network
from src.evaluation import evaluate_model
from models.model_manager import save_model


def run_pipeline():

    print("Loading dataset...")

    df = load_data("data/processed/DataCoSupplyChain_clean.csv")

    print("Preprocessing data...")

    df = preprocess_data(df)

    X = df[['order_item_quantity',
            'shipping_delay',
            'profit_margin',
            'order_month',
            'is_weekend']]

    y = df['sales']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -------------------------
    # RANDOM FOREST
    # -------------------------

    print("Training Random Forest...")

    rf_model = train_random_forest(X_train, y_train)

    rmse, r2 = evaluate_model(rf_model, X_test, y_test)

    print("Random Forest RMSE:", rmse)
    print("Random Forest R2:", r2)

    save_model(rf_model, "random_forest")

    # -------------------------
    # XGBOOST
    # -------------------------

    print("Training XGBoost...")

    xgb_model = train_xgboost(X_train, y_train)

    rmse, r2 = evaluate_model(xgb_model, X_test, y_test)

    print("XGBoost RMSE:", rmse)
    print("XGBoost R2:", r2)

    save_model(xgb_model, "xgboost")

    # -------------------------
    # NEURAL NETWORK
    # -------------------------

    print("Training Neural Network...")

    nn_model = train_neural_network(X_train, y_train)

    nn_model.save("models/neural_network.h5")

    print("Neural Network saved at models/neural_network.h5")

    print("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()