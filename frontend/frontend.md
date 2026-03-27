# Sales Demand Predictor — Frontend Guide

A two-screen Streamlit application for ML-powered sales demand prediction and analytics, built on the DataCo Supply Chain dataset.

---

## Project Structure

```
your_project/
│
├── app.py                  # Prediction interface
├── dashboard.py            # Analytics dashboard
├── requirements.txt        # Python dependencies
├── predictions.db          # SQLite database (auto-created on first run)
│
└── models/
    ├── random_forest.pkl
    ├── xgboost.pkl
    └── neural_network.h5
```

> The `models/` folder and its three files must be present before launching the app. `predictions.db` is created automatically on first run.

---

## Prerequisites

- Python 3.9 or higher
- pip (latest)
- Internet access on first run (for Google Fonts)

---

## Setup

**1. Create a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Place model files**

Copy your trained model files into the `models/` folder before starting.

---

## Running the App

The two screens run as separate processes. Open two terminals.

**Terminal 1 — Prediction Interface**

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

**Terminal 2 — Analytics Dashboard**

```bash
streamlit run dashboard.py
```

Opens at `http://localhost:8502`

Both can run simultaneously. Predictions made in `app.py` appear in `dashboard.py` within 10 seconds, or instantly after clicking **↺ Refresh Data** in the sidebar.

---

## What Each Screen Does

| Screen | File | Purpose |
|---|---|---|
| Prediction Interface | `app.py` | Select a model, fill in the 5 input fields, run a prediction, and save the result |
| Analytics Dashboard | `dashboard.py` | View charts, filter by model/month/day type, and browse the full prediction history |

### Input Fields (app.py)

All five fields must be filled before a prediction can be submitted.

| Field | Description |
|---|---|
| Order Item Quantity | Number of items in the order |
| Shipping Delay | Days between order placement and delivery |
| Profit Margin | Profit margin as a decimal (e.g. 0.25 = 25%) |
| Order Month | Month the order was placed (1–12) |
| Order Day Type | Weekday or Weekend |

### Available Models (app.py)

| Model | Type |
|---|---|
| Random Forest | Ensemble / Bagging |
| XGBoost | Gradient Boosting |
| Neural Network | Feedforward Dense NN |

### Dashboard Charts (dashboard.py)

- Predicted Sales Over Time
- Model Usage Split
- Prediction Distribution
- Order Quantity vs Predicted Sales
- Avg Predicted Sales by Month
- Shipping Delay vs Predicted Sales
- Profit Margin vs Predicted Sales
- Weekend vs Weekday Sales Distribution
- Cumulative Predictions Over Time
- Avg Predicted Sales by Model

---

## Dependencies

| Package | Purpose |
|---|---|
| streamlit | UI framework |
| pandas / numpy | Data handling |
| scikit-learn | Random Forest model |
| xgboost | XGBoost model |
| tensorflow | Neural Network model |
| joblib | Model file loading |
| plotly | Interactive charts |

---

## Notes

- `predictions.db` stores every prediction with its inputs, model used, timestamp, and result.
- The dashboard opens the database in read-only mode — it cannot modify any data.
- The prediction screen only shows summary statistics (totals, averages) — no individual records are displayed there.
- To use a custom port: `streamlit run app.py --server.port 8080`
