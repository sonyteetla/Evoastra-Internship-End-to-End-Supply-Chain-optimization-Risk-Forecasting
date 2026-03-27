"""
app.py — Sales Demand Predictor
Frontend UI for FastAPI backend
Sends prediction requests to backend API and logs results locally.
"""

import sqlite3
from datetime import datetime
import streamlit as st
import requests

# Streamlit page config must be the first Streamlit command on the page.
st.set_page_config(
    page_title="Sales Demand Predictor",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navigate between main app and analytics dashboard (dashboard.py is a separate Streamlit app that reads from the same DB)


# ── credentials (simple) ─────────────────────────────
USERNAME = "admin"
PASSWORD = "1234"

# ── session state ────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page_nav" not in st.session_state:
    st.session_state.page_nav = "Prediction App"

if st.session_state.pop("redirect_to_prediction", False):
    st.session_state.page_nav = "Prediction App"


# ── navigation ───────────────────────────────────────
page = st.sidebar.selectbox(
    "Navigation",
    ["Prediction App", "Analytics Dashboard"],
    key="page_nav",
)


# ── dashboard protection ─────────────────────────────
if page == "Analytics Dashboard":

    if not st.session_state.authenticated:
        

        # CSS only for login page
        st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
/* Hide sidebar */
[data-testid="stSidebar"] {
    display: none;
}

/* Hide sidebar toggle button */
button[kind="header"] {
    display: none;
}

/* Remove extra space */
[data-testid="collapsedControl"] {
    display: none;
}


.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 28%),
                radial-gradient(circle at bottom right, rgba(14,165,233,0.14), transparent 24%),
                linear-gradient(145deg, #06101c 0%, #0f1c33 45%, #13294b 100%);
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 3rem;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e3a5f 0%, #1e40af 60%, #1d4ed8 100%) !important;
            border-right: none !important;
            box-shadow: 4px 0 20px rgba(30,58,95,.2) !important;
        }

        section[data-testid="stSidebar"]::before {
            content: '';
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #93c5fd, #3b82f6, #2563eb);
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] label p,
        section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] span {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif !important;
        }

        .login-shell {
            max-width: 520px;
            margin: 72px auto;
            position: relative;
        }

        .login-shell::before {
            content: "";
            position: absolute;
            inset: -18px;
            background: linear-gradient(135deg, rgba(147,197,253,0.22), rgba(37,99,235,0.12));
            filter: blur(18px);
            border-radius: 28px;
            z-index: 0;
        }

        .login-container {
            position: relative;
            z-index: 1;
            background: rgba(248, 250, 255, 0.92);
            border: 1px solid rgba(191,219,254,0.55);
            border-radius: 24px;
            padding: 2.6rem 2.35rem 2.2rem;
            text-align: center;
            box-shadow: 0 24px 60px rgba(3, 12, 28, 0.28);
            backdrop-filter: blur(10px);
        }

        .login-chip {
            display: inline-block;
            padding: 0.38rem 0.8rem;
            margin-bottom: 1rem;
            border-radius: 999px;
            background: #e0ecff;
            border: 1px solid #bfdbfe;
            color: #1d4ed8;
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .login-title {
            font-family: 'Playfair Display', serif;
            font-size: 2.25rem;
            font-weight: 700;
            background: linear-gradient(135deg,#1e3a5f,#2563eb,#3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: .45rem;
        }

        .login-sub {
            font-size: .84rem;
            color: #64748b;
            letter-spacing: .1em;
            text-transform: uppercase;
            margin-bottom: .9rem;
        }

        .login-copy {
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.7;
            margin: 0 auto 1.4rem;
            max-width: 390px;
        }

        .login-divider {
            height: 1px;
            margin: 0 0 1.2rem;
            border: none;
            background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
        }

        .stTextInput > div > div > input {
            background: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            color: #0f172a !important;
            padding-top: 0.8rem !important;
            padding-bottom: 0.8rem !important;
            font-size: 1.08rem !important;
            font-weight: 500 !important;
            box-shadow: inset 0 1px 2px rgba(15,23,42,0.04);
        }

        .stTextInput > div > div > input:focus {
            border-color: #60a5fa !important;
            box-shadow: 0 0 0 4px rgba(96,165,250,0.18) !important;
        }

        label {
            color: #334155 !important;
            font-weight: 600 !important;
            font-size: 1.02rem !important;
        }

        .stTextInput label,
        .stTextInput label p,
        .stTextInput div[data-testid="stMarkdownContainer"] p {
            font-size: 1.22rem !important;
            font-weight: 700 !important;
            color: #1d4ed8 !important;
            letter-spacing: 0.01em;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 12px;
            background: linear-gradient(135deg, #1e3a5f, #2563eb);
            border: none;
            color: white;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding: .8rem 1rem;
            box-shadow: 0 14px 30px rgba(37,99,235,0.24);
        }

        div.stButton > button:hover {
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            transform: translateY(-1px);
        }

        </style>
        """, unsafe_allow_html=True)

        # Login card
        st.markdown("""
        <div class="login-shell">
        <div class="login-container">
            <div class="login-chip">Protected Analytics</div>
            <div class="login-title">Dashboard Access</div>
            <div class="login-copy">
                Sign in to view analytics, model activity, and prediction history in one place.
            </div>
            <hr class="login-divider">
            <div class="login-sub">Supply Chain AI · Admin Login</div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        login_col, back_col = st.columns(2)

        with login_col:
            login_clicked = st.button("Login", use_container_width=True)

        with back_col:
            back_clicked = st.button("Back", use_container_width=True)

        if back_clicked:
            st.session_state.redirect_to_prediction = True
            st.rerun()

        if login_clicked:

            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password")

        st.markdown("</div></div>", unsafe_allow_html=True)

        st.stop()

    # If authenticated → run dashboard
    exec(open("dashboard.py").read())
    st.stop()

# Backend API
API_URL = "http://localhost:8000/predict"

DB_PATH = "predictions.db"

MONTH_LABELS = {
    1:"January", 2:"February", 3:"March", 4:"April",
    5:"May", 6:"June", 7:"July", 8:"August",
    9:"September",10:"October",11:"November",12:"December",
}

MODEL_META = {
    "Random Forest":  {"type": "Ensemble / Bagging",   "n_estimators": 200, "r2": "0.144"},
    "XGBoost":        {"type": "Gradient Boosting",    "n_estimators": 200, "r2": "0.124"},
    "Neural Network": {"type": "Feedforward Dense NN", "n_estimators": "—", "r2": "—"},
}

# ── CSS ────────────────────────────────────────────────────────────────────────
# Blue palette:
#   --blue-deep   #1e3a5f   headings, sidebar bg
#   --blue-mid    #2563eb   primary actions, KPI values, section headers
#   --blue-bright #3b82f6   hover states, accents
#   --blue-light  #93c5fd   secondary accents, dividers
#   --blue-pale   #dbeafe   card borders, subtle fills
#   --bg          #ffffff   page background
#   --surface     #f8faff   card backgrounds
#   --text        #0f172a   primary text
#   --muted       #64748b   secondary text, labels
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #ffffff; color: #0f172a; }
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }

/* ── Hero ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size:3.22rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1.12;
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 55%, #3b82f6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.hero-sub {
    font-size:0.94rem; color: #64748b; letter-spacing: 0.1em;
    text-transform: uppercase; font-weight: 500; margin-bottom: 2rem;
}

/* ── KPI cards — uniform fixed height so all 4 look identical ── */
.kpi-card {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 12px;
    padding: 0;
    text-align: center;
    height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: border-color .2s, box-shadow .2s;
    overflow: hidden;
}
.kpi-card:hover {
    border-color: #93c5fd;
    box-shadow: 0 4px 16px rgba(37,99,235,.08);
}
.kpi-label {
    font-family: 'Inter', sans-serif; font-weight: 600;
    font-size:0.67rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.13em;
    margin-bottom: 0.3rem; line-height: 1;
}
/* Fixed font size — every card value renders at the same size */
.kpi-value {
    font-family: 'Inter', sans-serif;
    font-size:1.67rem;
    font-weight: 700;
    color: #2563eb;
    line-height: 1.15;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 90%;
}

/* ── Section headers ── */
.sec-hdr {
    font-family: 'Inter', sans-serif; font-weight: 700; font-size:0.8rem; color: #2563eb;
    text-transform: uppercase; letter-spacing: 0.16em;
    border-left: 3px solid #2563eb; padding-left: 0.75rem; margin: 1.5rem 0 1rem;
}

/* ── Prediction result box ── */

.pred-box {
    background: linear-gradient(135deg, #eff6ff, #f8faff);
    border: 2px solid #2563eb; border-radius: 16px;
    padding: 2.2rem 1.5rem; text-align: center;
    box-shadow: 0 4px 24px rgba(37,99,235,.1);
}
.pred-box-empty {
    background: #f8faff;
    border: 2px dashed #dbeafe;
    border-radius: 16px;
    padding: 2.2rem 1.5rem;
    text-align: center;
    color: #334155;
}
.error-box {
    background: linear-gradient(135deg, #fff1f2, #ffe4e6);
    border: 1px solid #fda4af;
    border-left: 5px solid #e11d48;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    color: #881337;
    box-shadow: 0 6px 18px rgba(225, 29, 72, 0.08);
}
.error-box-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    margin-bottom: 0.55rem;
    color: #9f1239;
}
.error-box-list {
    margin: 0;
    padding-left: 1.15rem;
    color: #881337;
    line-height: 1.6;
}
.error-box-list li {
    margin: 0.1rem 0;
}
.pred-lbl {
    font-family: 'Inter', sans-serif; font-weight: 600; font-size:0.78rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.14em;
}
.pred-val {
    font-family: 'Inter', sans-serif; font-size:3.91rem; font-weight: 700;
    background: linear-gradient(135deg, #1e3a5f, #2563eb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.pred-meta { font-family:'Inter',sans-serif; font-size:0.8rem; color:#94a3b8; margin-top:0.6rem; }

/* ── Model badge next to section header ── */
.model-badge {
    display: inline-block; background: #eff6ff; border: 1px solid #93c5fd;
    color: #2563eb; font-family: 'Inter', sans-serif; font-weight: 600; font-size:0.71rem;
    padding: 0.18rem 0.6rem; border-radius: 20px; margin-left: 0.5rem;
    letter-spacing: 0.08em; text-transform: uppercase; vertical-align: middle;
}

/* ── Field completion tracker ── */
.field-status {
    background: #f8faff; border: 1px solid #dbeafe;
    border-radius: 10px; padding: 0.9rem 1rem; margin-top: 1.2rem;
}
.field-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.22rem 0; font-family: 'Inter', sans-serif; font-size:0.78rem;
    border-bottom: 1px solid #eff6ff;
}
.field-row:last-child { border-bottom: none; }
.field-name { color: #64748b; }
.field-ok   { color: #16a34a; }
.field-no   { color: #cbd5e1; }

/* ── Model info panel in sidebar ── */
.model-info {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 10px; padding: 0.85rem 1rem; margin-top: 0.5rem;
}
.mi-row {
    display: flex; justify-content: space-between;
    font-family: 'Inter', sans-serif; font-size:0.78rem;
    padding: 0.28rem 0; border-bottom: 1px solid #dbeafe;
}
.mi-row:last-child { border-bottom: none; }
.mi-key { color: #64748b; }
.mi-val { color: #1e3a5f; }

/* ── Inputs ── */
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background-color: #f8faff !important; border: 1px solid #bfdbfe !important;
    color: #0f172a !important; border-radius: 8px !important;
}
.stNumberInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
}
label { color: #334155 !important; font-size:0.95rem !important; font-family: 'Inter', sans-serif !important; }

/* ── Predict button ── */
.stButton > button {
    font-family: 'Inter', sans-serif; font-size:0.98rem; font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase;
    background: linear-gradient(135deg, #1e3a5f, #2563eb);
    color: #ffffff; border: none; border-radius: 8px;
    padding: 0.75rem 2rem; width: 100%; transition: all .2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(37,99,235,.3);
    background: linear-gradient(135deg, #2563eb, #3b82f6);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a5f 0%, #1e40af 60%, #1d4ed8 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 20px rgba(30,58,95,.2) !important;
}
section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #93c5fd, #3b82f6, #2563eb);
}
/* Sidebar toggle buttons — white fill reads on the blue sidebar AND on the white main canvas */
button[data-testid="stSidebarCollapseButton"] {
    background: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    transition: background .15s ease, transform .15s ease !important;
}
button[data-testid="stSidebarCollapseButton"]:hover {
    background: #dbeafe !important;
    transform: scale(1.1) !important;
}
button[data-testid="stSidebarCollapseButton"] svg {
    color: #1e3a5f !important;
    fill: #1e3a5f !important;
    stroke: #1e3a5f !important;
}
/* Expand button sits on white main canvas — use solid blue so it's visible */
button[data-testid="stExpandSidebarButton"] {
    background: #2563eb !important;
    border: none !important;
    border-radius: 6px !important;
    transition: background .15s ease, transform .15s ease !important;
}
button[data-testid="stExpandSidebarButton"]:hover {
    background: #1d4ed8 !important;
    transform: scale(1.1) !important;
}
button[data-testid="stExpandSidebarButton"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
    stroke: #ffffff !important;
}
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stRadio label p,
section[data-testid="stSidebar"] .stRadio div[data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] .stRadio span {
    font-family: 'Inter', sans-serif !important;
    font-size:0.98rem !important;
    color: #ffffff !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Sidebar brand block ── */
.sb-brand {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 1.4rem;
}

/* ── Misc ── */
.stAlert { border-radius: 10px !important; font-family: 'Inter', sans-serif !important; font-size:0.92rem !important; }
.stAlert[data-baseweb="notification"],
div[data-baseweb="notification"][kind="error"] {
    background: #fff1f2 !important;
    border: 1px solid #fda4af !important;
    color: #881337 !important;
}
.stAlert[data-baseweb="notification"] p,
.stAlert[data-baseweb="notification"] div,
div[data-baseweb="notification"][kind="error"] p,
div[data-baseweb="notification"][kind="error"] div {
    color: #881337 !important;
}
.divider { height: 1px; border: none; margin: 1.1rem 0; background: linear-gradient(90deg, rgba(255,255,255,.25), transparent); }
.saved-pill {
    display: inline-block; background: #f0fdf4; border: 1px solid #86efac;
    color: #16a34a; font-family: 'Inter', sans-serif; font-size:0.75rem;
    padding: 0.2rem 0.7rem; border-radius: 20px; margin-top: 0.5rem; letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)


# ── DB helpers ─────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp           TEXT    NOT NULL,
            model_used          TEXT    NOT NULL,
            order_item_quantity INTEGER NOT NULL,
            shipping_delay      INTEGER NOT NULL,
            profit_margin       REAL    NOT NULL,
            order_month         INTEGER NOT NULL,
            is_weekend          INTEGER NOT NULL,
            predicted_sales     REAL    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(model_name, qty, delay, margin, month, weekend, pred):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO predictions
            (timestamp, model_used, order_item_quantity, shipping_delay,
             profit_margin, order_month, is_weekend, predicted_sales)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        model_name, int(qty), int(delay),
        float(margin), int(month), int(weekend), float(pred),
    ))
    conn.commit()
    conn.close()


def get_kpis() -> dict:
    """Returns scalar aggregates only — raw rows never leave the DB layer."""
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("""
        SELECT COUNT(*),
               ROUND(AVG(predicted_sales), 2),
               ROUND(MAX(predicted_sales), 2),
               ROUND(MIN(predicted_sales), 2)
        FROM predictions
    """)
    row = cur.fetchone()
    cur.execute("""
        SELECT model_used, COUNT(*) AS c
        FROM predictions GROUP BY model_used ORDER BY c DESC LIMIT 1
    """)
    top = cur.fetchone()
    conn.close()
    return {
        "total":     row[0] or 0,
        "avg":       row[1] or 0.0,
        "max":       row[2] or 0.0,
        "top_model": top[0] if top else "—",
    }




# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div style='font-family:Inter,sans-serif;font-size:1.21rem;
                    font-weight:700;letter-spacing:.04em;
                    background:linear-gradient(90deg,#93c5fd,#ffffff);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
            ⬡ SUPPLY CHAIN AI
        </div>
        <div style='font-size:0.78rem;color:#93c5fd;margin-top:.3rem;
                    font-family:Inter,sans-serif;letter-spacing:.08em;'>
            DEMAND PREDICTOR · v1.2
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-hdr">Select Model</div>', unsafe_allow_html=True)
    model_choice = st.radio("model", list(MODEL_META.keys()), label_visibility="collapsed")

    info = MODEL_META[model_choice]
    st.markdown(f"""
    <div class="model-info">
        <div class="mi-row"><span class="mi-key">Type</span>
            <span class="mi-val">{info['type']}</span></div>
        <div class="mi-row"><span class="mi-key">Estimators</span>
            <span class="mi-val">{info['n_estimators']}</span></div>
        <div class="mi-row"><span class="mi-key">Train R²</span>
            <span class="mi-val">{info['r2']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:Inter,sans-serif;font-size:0.75rem;
                color:#93c5fd;line-height:2.1;'>
        <span style='color:#bfdbfe'>FEATURES</span><br>
        → order_item_quantity<br>
        → shipping_delay<br>
        → profit_margin<br>
        → order_month<br>
        → is_weekend<br><br>
        <span style='color:#bfdbfe'>TARGET</span><br>
        → predicted_sales ($)<br><br>
        <span style='color:#bfdbfe'>ANALYTICS</span><br>
        → streamlit run dashboard.py
    </div>
    """, unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">Sales Demand<br>Predictor</div>
<div class="hero-sub">Supply Chain Intelligence · DataCo Dataset · Three ML Models</div>
""", unsafe_allow_html=True)

# ── KPI strip — uniform card height, uniform font size ────────────────────────
kpis = get_kpis()

def _kpi(label, value):
    """All cards use the same fixed font size — no per-card size overrides."""
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'</div>'
    )

k1, k2, k3, k4 = st.columns(4)
with k1: st.markdown(_kpi("Total Predictions",   str(kpis["total"])),                               unsafe_allow_html=True)
with k2: st.markdown(_kpi("Avg Predicted Sales",  f"${kpis['avg']:,.0f}" if kpis["total"] else "—"), unsafe_allow_html=True)
with k3: st.markdown(_kpi("Most Used Model",      kpis["top_model"]),                               unsafe_allow_html=True)
with k4: st.markdown(_kpi("Peak Predicted Sales", f"${kpis['max']:,.0f}" if kpis["total"] else "—"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Input panel ────────────────────────────────────────────────────────────────
left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown(
        f'<div class="sec-hdr">Input Features'
        f'<span class="model-badge">{model_choice}</span></div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        order_qty = st.number_input(
            "📦 Order Item Quantity",
            min_value=0, max_value=500,
            value=None, placeholder="e.g. 10",
            help="Number of items in the order (0 – 500)",
        )

        shipping_delay = st.number_input(
            "🚚 Shipping Delay (days)",
            min_value=0, max_value=365,
            value=None, placeholder="e.g. 3",
        )

        profit_margin_pct = st.number_input(
            "💰 Profit Margin (%)",
            
            value=None,
            max_value=500,
            min_value=-500,
            placeholder="e.g. 25",
            help="Enter profit margin as percentage (25 = 25%)",
        )
        profit_margin = profit_margin_pct / 100 if profit_margin_pct is not None else None

    with col_b:
        order_month = st.selectbox(
            "📅 Order Month",
            options=[None] + list(range(1, 13)),
            format_func=lambda x: "Select month…" if x is None
                else f"{x:02d} · {MONTH_LABELS[x]}",
            index=0,
        )

        is_weekend = st.selectbox(
            "📆 Order Day Type",
            options=[None, 0, 1],
            format_func=lambda x: "Select…" if x is None
                else ("1 · Weekend" if x == 1 else "0 · Weekday"),
            index=0,
        )

        fields = {
            "order_item_quantity": order_qty,
            "shipping_delay": shipping_delay,
            "profit_margin": profit_margin_pct,
            "order_month": order_month,
            "is_weekend": is_weekend,
        }

        rows_html = "".join(
            f'<div class="field-row"><span class="field-name">{name}</span>'
            f'<span class="{"field-ok" if v is not None else "field-no"}">'
            f'{"✔" if v is not None else "○"}</span></div>'
            for name, v in fields.items()
        )

        filled = sum(v is not None for v in fields.values())

        st.markdown(
            f'<div class="field-status">'
            f'<div style="font-size:0.71rem;color:#5a5d6a;letter-spacing:.1em;margin-bottom:.4rem;">'
            f'FIELDS COMPLETE · {filled} / 5</div>{rows_html}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("⚡ Run Prediction", use_container_width=True)


# ───────────────── RESULT PANEL ─────────────────
with right:

    st.markdown('<div class="sec-hdr">Prediction Result</div>', unsafe_allow_html=True)

    if predict_btn:

        missing = [name for name, val in fields.items() if val is None]

        if missing:
            missing_items = "".join(f"<li>{f}</li>" for f in missing)
            st.markdown(
            f"""
            <div class="error-box">
                <div class="error-box-title">⚠ All 5 fields are required. Please fill:</div>
                <ul class="error-box-list">
                    {missing_items}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
            )

        else:

            try:

                payload = {
                    "model_name": model_choice.lower().replace(" ", "_"),
                    "features": [
                        order_qty,
                        shipping_delay,
                        profit_margin/100,  # convert back to decimal for API
                        order_month,
                        is_weekend
                    ]
                }

                response = requests.post(API_URL, json=payload)

                if response.status_code != 200:
                    st.error("Backend API error")
                    st.stop()

                result = response.json()

                prediction = result["prediction"]

                if isinstance(prediction[0], list):
                    pred = float(prediction[0][0])
                else:
                    pred = float(prediction[0])

                save_prediction(
                    model_choice,
                    order_qty,
                    shipping_delay,
                    profit_margin,
                    order_month,
                    is_weekend,
                    pred,
                )

                st.session_state["last_pred"] = pred
                st.session_state["last_model"] = model_choice

                st.markdown(f"""
                <div class="pred-box">
                    <div class="pred-lbl">Predicted Sales</div>
                    <div class="pred-val">${pred:,.2f}</div>
                    <div class="pred-meta">
                        model · {model_choice}<br>
                        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    </div>
                    <div class="saved-pill">✔ saved to predictions.db</div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as exc:
                st.error(f"Backend connection failed: {exc}")


    elif "last_pred" in st.session_state:

        pred = st.session_state["last_pred"]
        mname = st.session_state.get("last_model", "")

        st.markdown(f"""
        <div class="pred-box">
            <div class="pred-lbl">Last Predicted Sales</div>
            <div class="pred-val">${pred:,.2f}</div>
            <div class="pred-meta">model · {mname}</div>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="pred-box-empty">
            <div style="font-size:2.8rem;margin-bottom:.6rem;">📦</div>
            <div class="pred-lbl" style="font-size:0.86rem;color:#94a3b8;">
                Fill all 5 fields and click Run Prediction
            </div>
        </div>
        """, unsafe_allow_html=True)
        

