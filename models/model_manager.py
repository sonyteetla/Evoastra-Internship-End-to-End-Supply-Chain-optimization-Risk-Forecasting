import joblib
import os


MODEL_DIR = "models"


def save_model(model, model_name):
    """
    Save trained model into models folder
    """

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    model_path = os.path.join(MODEL_DIR, f"{model_name}.pkl")

    joblib.dump(model, model_path)

    print(f"Model saved successfully at {model_path}")


def load_model(model_name):
    """
    Load model from models folder
    """

    model_path = os.path.join(MODEL_DIR, f"{model_name}.pkl")

    model = joblib.load(model_path)

    print(f"Model loaded from {model_path}")

    return model