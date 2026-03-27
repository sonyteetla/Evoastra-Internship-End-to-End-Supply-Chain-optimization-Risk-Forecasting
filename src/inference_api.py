from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(
    title="Evoastra Supply Chain ML API",
    version="1.0"
)

FEATURE_COLUMNS = [
    "order_item_quantity",
    "shipping_delay",
    "profit_margin",
    "order_month",
    "is_weekend"
]

# -----------------------------
# Load Models
# -----------------------------

MODEL_DIR = "models"

rf_model = joblib.load(os.path.join(MODEL_DIR, "random_forest.pkl"))
xgb_model = joblib.load(os.path.join(MODEL_DIR, "xgboost.pkl"))

models = {
    "random_forest": rf_model,
    "xgboost": xgb_model
}

# -----------------------------
# Request Schema
# -----------------------------

class PredictionInput(BaseModel):
    model_name: str
    features: list


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Evoastra ML Inference API Running",
        "available_models": list(models.keys())
    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {"status": "healthy"}


# -----------------------------
# Prediction Endpoint
# -----------------------------

@app.post("/predict")
def predict(data: PredictionInput):

    model = models[data.model_name]

    # Validate input size
    if len(data.features) != len(FEATURE_COLUMNS):
        return {
            "error": f"Expected {len(FEATURE_COLUMNS)} features"
        }

    # Convert input to DataFrame with correct feature names
    features_df = pd.DataFrame([data.features], columns=FEATURE_COLUMNS)

    prediction = model.predict(features_df)

    return {
        "model": data.model_name,
        "prediction": prediction.tolist()
    }