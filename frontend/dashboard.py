
"""
dashboard.py — Analytics Dashboard
Reads predictions.db (read-only), renders all charts and data table.
No model loading, no prediction logic.
Predictor app: streamlit run app.py
"""

import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ── Constants ──────────────────────────────────────────────────────────────────
DB_PATH = "predictions.db"

ACCENT  = "#2563eb"   # blue-mid — Random Forest
ACCENT2 = "#1e3a5f"   # blue-deep — XGBoost
ACCENT3 = "#3b82f6"   # blue-bright — Neural Network
ACCENT4 = "#93c5fd"   # blue-light — Weekday
ACCENT5 = "#1d4ed8"   # blue-strong — Weekend

MODEL_COLORS = {
    "Random Forest":  ACCENT,
    "XGBoost":        ACCENT2,
    "Neural Network": ACCENT3,
}

MONTH_SHORT = {
    1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr",  5:"May",  6:"Jun",
    7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec",
}

# 'legend' is intentionally excluded from CHART_BASE.
# apply_layout() accepts it as an explicit param to avoid duplicate-key errors.
CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#f8faff",
    font=dict(family="Inter, sans-serif", color="#64748b", size=11),
    title_font=dict(family="Inter, sans-serif", color="#1e3a5f", size=13),
    xaxis=dict(gridcolor="#dbeafe", linecolor="#bfdbfe", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#dbeafe", linecolor="#bfdbfe", tickfont=dict(size=10)),
    margin=dict(l=45, r=20, t=50, b=40),
)

LEGEND_DEFAULT = dict(
    bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=10, color="#64748b"),
)

LEGEND_BOTTOM = dict(**LEGEND_DEFAULT, orientation="h", y=-0.22)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #ffffff; color: #0f172a; }
.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }

/* ── Hero ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size:2.76rem; font-weight: 700; letter-spacing: -0.02em; line-height: 1.12;
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 55%, #3b82f6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.hero-sub {
    font-size:0.94rem; color: #64748b; letter-spacing: 0.1em;
    text-transform: uppercase; font-weight: 500; margin-bottom: 2rem;
    encoding: utf-8;       
}

/* ── KPI cards — uniform fixed height so all 5 look identical ── */
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
    border-left: 3px solid #2563eb; padding-left: 0.75rem; margin: 1.6rem 0 1rem;
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
/* Collapse button — inside the blue sidebar, white is clearly visible */
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
/* Expand button — on the white main canvas, solid blue is clearly visible */
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
section[data-testid="stSidebar"] label {
    font-family: 'Inter', sans-serif !important;
    font-size:0.9rem !important; color: #ffffff !important;
}

/* ── Sidebar brand block ── */
.sb-brand {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 1.4rem;
    encoding: utf-8;
}

/* ── Misc ── */
.stDataFrame  { border: 1px solid #dbeafe !important; border-radius: 10px !important; }
.stAlert      { border-radius: 10px !important; font-family: 'Inter', sans-serif !important; font-size:0.92rem !important; }
.divider      { height: 1px; border: none; margin: 1.1rem 0; background: linear-gradient(90deg, rgba(255,255,255,.3), transparent); }
.no-data {
    text-align: center; padding: 4rem 2rem;
    font-family: 'Inter', sans-serif; color: #94a3b8; font-size:0.98rem;
}
</style>
""", unsafe_allow_html=True)


# ── DB — read-only ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=10)
def load_all_predictions() -> pd.DataFrame:
    """Opens DB in read-only mode; all rows used for charting only."""
    try:
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        df   = pd.read_sql("SELECT * FROM predictions ORDER BY id ASC", conn)
        conn.close()
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except Exception:
        return pd.DataFrame()


# ── Chart helpers ──────────────────────────────────────────────────────────────
def apply_layout(fig, title: str, height: int = 300, legend: dict = None, **extra):
    """Applies shared chart theme. legend is an explicit param to avoid key collision."""
    kwargs = dict(**CHART_BASE, title=title, height=height, **extra)
    kwargs["legend"] = legend if legend is not None else LEGEND_DEFAULT
    fig.update_layout(**kwargs)
    return fig

def show_chart(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ── Sidebar — filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div style='font-family:Inter,sans-serif;font-size:1.21rem;
                    font-weight:700;letter-spacing:.04em;
                    background:linear-gradient(90deg,#93c5fd,#ffffff);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
             \u2B21 SUPPLY CHAIN AI
        </div>
        <div style='font-size:0.78rem;color:#93c5fd;margin-top:.3rem;
                    font-family:Inter,sans-serif;letter-spacing:.08em;'>
            ANALYTICS DASHBOARD \u2022 v1.2
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 4rem;'></div>", unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown('<div class="sec-hdr">Filters</div>', unsafe_allow_html=True)

    _df_raw = load_all_predictions()

    if not _df_raw.empty:
        model_opts = ["All"] + sorted(_df_raw["model_used"].unique().tolist())
        sel_model  = st.selectbox("Model", model_opts)

        month_opts = ["All"] + sorted(_df_raw["order_month"].unique().tolist())
        sel_month  = st.selectbox(
            "Month", month_opts,
            format_func=lambda x: "All" if x == "All"
                else f"{x:02d} · {MONTH_SHORT.get(x, '?')}",
        )

        sel_weekend = st.selectbox(
            "Day Type",
            options=["All", 0, 1],
            format_func=lambda x: {"All":"All", 0:"0 · Weekday", 1:"1 · Weekend"}[x],
        )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        if st.button("\u21BB  Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    else:
        sel_model = sel_month = sel_weekend = "All"

    st.markdown("""
    <div style='font-family:Inter,sans-serif;font-size:0.75rem;
                color:#93c5fd;line-height:2.1;margin-top:1rem;'>
        <span style='color:#bfdbfe'>PREDICTOR APP</span><br>
        \u21E2 Go to Predictor
    </div>
    """, unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">Analytics Dashboard</div>
<div class="hero-sub">Prediction History | DataCo Supply Chain | SQLite \u2192 Plotly</div>
""", unsafe_allow_html=True)

# ── Load + filter ──────────────────────────────────────────────────────────────
df_raw = load_all_predictions()

if df_raw.empty:
    st.markdown("""
    <div class="no-data">
        <div style="font-size:3rem;margin-bottom:1rem;">📭</div>
        No predictions found in <code>predictions.db</code>.<br><br>
        Run <code>streamlit run app.py</code> and make at least one prediction first.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = df_raw.copy()
if sel_model   != "All": df = df[df["model_used"]  == sel_model]
if sel_month   != "All": df = df[df["order_month"] == sel_month]
if sel_weekend != "All": df = df[df["is_weekend"]  == sel_weekend]

if df.empty:
    st.warning("No records match the selected filters. Adjust the sidebar.")
    st.stop()

# ── KPI strip — uniform card height, uniform font size ────────────────────────
def _kpi(label, val):
    """All cards use the same fixed font size — no per-card size overrides."""
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{val}</div>'
        f'</div>'
    )

k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.markdown(_kpi("Records",    len(df)),                                          unsafe_allow_html=True)
with k2: st.markdown(_kpi("Avg Sales",  f"${df['predicted_sales'].mean():,.0f}"),         unsafe_allow_html=True)
with k3: st.markdown(_kpi("Peak Sales", f"${df['predicted_sales'].max():,.0f}"),          unsafe_allow_html=True)
with k4: st.markdown(_kpi("Min Sales",  f"${df['predicted_sales'].min():,.0f}"),          unsafe_allow_html=True)
with k5: st.markdown(_kpi("Std Dev",    f"${df['predicted_sales'].std():,.0f}"),          unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── ROW 1 — Time series + Model usage donut ────────────────────────────────────
st.markdown('<div class="sec-hdr">Temporal & Model Breakdown</div>', unsafe_allow_html=True)
r1a, r1b = st.columns([1.65, 1])

with r1a:
    df_ts = df.sort_values("timestamp")
    fig   = go.Figure()
    for mname, color in MODEL_COLORS.items():
        sub = df_ts[df_ts["model_used"] == mname]
        if sub.empty: continue
        fig.add_trace(go.Scatter(
            x=sub["timestamp"], y=sub["predicted_sales"],
            mode="lines+markers", name=mname,
            line=dict(color=color, width=2), marker=dict(size=5, color=color),
            hovertemplate="<b>$%{y:,.2f}</b><br>%{x}<extra>" + mname + "</extra>",
        ))
    apply_layout(fig, "Predicted Sales Over Time", 310,
                 xaxis_title="Timestamp", yaxis_title="Predicted Sales ($)")
    show_chart(fig)

with r1b:
    counts     = df["model_used"].value_counts().reset_index()
    counts.columns = ["model", "count"]
    pie_colors = [MODEL_COLORS.get(m, ACCENT) for m in counts["model"]]
    fig = go.Figure(go.Pie(
        labels=counts["model"], values=counts["count"], hole=0.58,
        marker=dict(colors=pie_colors, line=dict(color="#ffffff", width=2)),
        textfont=dict(family="Inter, sans-serif", size=10),
        hovertemplate="<b>%{label}</b><br>%{value} predictions (%{percent})<extra></extra>",
    ))
    apply_layout(fig, "Model Usage Split", 310, legend=LEGEND_BOTTOM)
    show_chart(fig)


# ── ROW 2 — Distribution + Quantity scatter ────────────────────────────────────
st.markdown('<div class="sec-hdr">Distribution & Feature Relationships</div>', unsafe_allow_html=True)
r2a, r2b = st.columns(2)

with r2a:
    fig = go.Figure()
    for mname, color in MODEL_COLORS.items():
        sub = df[df["model_used"] == mname]
        if sub.empty: continue
        fig.add_trace(go.Histogram(
            x=sub["predicted_sales"], name=mname,
            marker_color=color, opacity=0.72, nbinsx=22,
            hovertemplate="Range: %{x}<br>Count: %{y}<extra>" + mname + "</extra>",
        ))
    apply_layout(fig, "Prediction Distribution", 300, barmode="overlay",
                 xaxis_title="Predicted Sales ($)", yaxis_title="Count")
    show_chart(fig)

with r2b:
    fig = go.Figure()
    for mname, color in MODEL_COLORS.items():
        sub = df[df["model_used"] == mname]
        if sub.empty: continue
        fig.add_trace(go.Scatter(
            x=sub["order_item_quantity"], y=sub["predicted_sales"],
            mode="markers", name=mname,
            marker=dict(color=color, size=7, opacity=0.8,
                        line=dict(color="#ffffff", width=1)),
            hovertemplate="Qty: %{x}<br>$%{y:,.2f}<extra>" + mname + "</extra>",
        ))
    apply_layout(fig, "Order Quantity vs Predicted Sales", 300,
                 xaxis_title="Order Item Quantity", yaxis_title="Predicted Sales ($)")
    show_chart(fig)


# ── ROW 3 — Monthly avg + Shipping delay ──────────────────────────────────────
st.markdown('<div class="sec-hdr">Seasonality & Logistics Impact</div>', unsafe_allow_html=True)
r3a, r3b = st.columns(2)

with r3a:
    monthly = (df.groupby("order_month")["predicted_sales"]
               .mean().reset_index().sort_values("order_month"))
    monthly["month_name"] = monthly["order_month"].map(MONTH_SHORT)
    fig = go.Figure(go.Bar(
        x=monthly["month_name"], y=monthly["predicted_sales"],
        marker=dict(
            color=monthly["predicted_sales"],
            colorscale=[[0, "#dbeafe"], [0.5, "#3b82f6"], [1, "#1e3a5f"]],
            showscale=False,
        ),
        text=[f"${v:,.0f}" for v in monthly["predicted_sales"]],
        textposition="outside",
        textfont=dict(family="Inter, sans-serif", size=9, color="#64748b"),
        hovertemplate="%{x}<br>Avg: $%{y:,.2f}<extra></extra>",
    ))
    apply_layout(fig, "Avg Predicted Sales by Month", 300,
                 xaxis_title="Month", yaxis_title="Avg Predicted Sales ($)")
    show_chart(fig)

with r3b:
    fig = go.Figure()
    for mname, color in MODEL_COLORS.items():
        sub = df[df["model_used"] == mname]
        if sub.empty: continue
        fig.add_trace(go.Scatter(
            x=sub["shipping_delay"], y=sub["predicted_sales"],
            mode="markers", name=mname,
            marker=dict(color=color, size=7, opacity=0.8,
                        line=dict(color="#ffffff", width=1)),
            hovertemplate="Delay: %{x}d<br>$%{y:,.2f}<extra>" + mname + "</extra>",
        ))
    apply_layout(fig, "Shipping Delay vs Predicted Sales", 300,
                 xaxis_title="Shipping Delay (days)", yaxis_title="Predicted Sales ($)")
    show_chart(fig)


# ── ROW 4 — Profit margin + Weekend box ───────────────────────────────────────
st.markdown('<div class="sec-hdr">Margin & Day-Type Analysis</div>', unsafe_allow_html=True)
r4a, r4b = st.columns(2)

with r4a:
    fig = go.Figure()
    for mname, color in MODEL_COLORS.items():
        sub = df[df["model_used"] == mname]
        if sub.empty: continue
        fig.add_trace(go.Scatter(
            x=sub["profit_margin"], y=sub["predicted_sales"],
            mode="markers", name=mname,
            marker=dict(color=color, size=7, opacity=0.78,
                        line=dict(color="#ffffff", width=1)),
            hovertemplate="Margin: %{x:.3f}<br>$%{y:,.2f}<extra>" + mname + "</extra>",
        ))
    apply_layout(fig, "Profit Margin vs Predicted Sales", 300,
                 xaxis_title="Profit Margin", yaxis_title="Predicted Sales ($)")
    show_chart(fig)

with r4b:
    fig = go.Figure()
    for val, label, color in [(0, "Weekday", ACCENT4), (1, "Weekend", ACCENT5)]:
        sub = df[df["is_weekend"] == val]
        if sub.empty: continue
        fig.add_trace(go.Box(
            y=sub["predicted_sales"], name=label,
            marker_color=color, line_color=color, boxmean="sd",
            hovertemplate="<b>" + label + "</b><br>$%{y:,.2f}<extra></extra>",
        ))
    apply_layout(fig, "Weekend vs Weekday — Sales Distribution", 300,
                 yaxis_title="Predicted Sales ($)")
    show_chart(fig)


# ── ROW 5 — Cumulative + Model avg comparison ──────────────────────────────────
st.markdown('<div class="sec-hdr">Cumulative Trends & Model Comparison</div>', unsafe_allow_html=True)
r5a, r5b = st.columns(2)

with r5a:
    df_cum = df.sort_values("timestamp").copy()
    df_cum["cumulative"] = range(1, len(df_cum) + 1)
    fig = go.Figure(go.Scatter(
        x=df_cum["timestamp"], y=df_cum["cumulative"],
        mode="lines", fill="tozeroy",
        line=dict(color=ACCENT4, width=2),
        fillcolor="rgba(37,99,235,0.06)",
        hovertemplate="%{x}<br>Total: %{y}<extra></extra>",
    ))
    apply_layout(fig, "Cumulative Predictions Over Time", 300,
                 xaxis_title="Timestamp", yaxis_title="Total Predictions")
    show_chart(fig)

with r5b:
    model_avg = (df.groupby("model_used")["predicted_sales"]
                 .mean().reset_index()
                 .sort_values("predicted_sales", ascending=False))
    bar_colors = [MODEL_COLORS.get(m, ACCENT) for m in model_avg["model_used"]]
    fig = go.Figure(go.Bar(
        x=model_avg["model_used"], y=model_avg["predicted_sales"],
        marker_color=bar_colors,
        text=[f"${v:,.0f}" for v in model_avg["predicted_sales"]],
        textposition="outside",
        textfont=dict(family="Inter, sans-serif", size=10),
        hovertemplate="<b>%{x}</b><br>Avg: $%{y:,.2f}<extra></extra>",
    ))
    apply_layout(fig, "Avg Predicted Sales by Model", 300,
                 xaxis_title="Model", yaxis_title="Avg Predicted Sales ($)",
                 showlegend=False)
    show_chart(fig)


# ── Full data table ────────────────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Full Prediction History</div>', unsafe_allow_html=True)

display_df = df.copy().sort_values("id", ascending=False)
display_df["timestamp"]       = display_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
display_df["predicted_sales"] = display_df["predicted_sales"].map("${:,.2f}".format)
display_df["profit_margin"]   = display_df["profit_margin"].map("{:.3f}".format)
display_df["is_weekend"]      = display_df["is_weekend"].map({0: "Weekday", 1: "Weekend"})
display_df["order_month"]     = display_df["order_month"].map(MONTH_SHORT)

display_df = display_df.rename(columns={
    "id":                  "ID",
    "timestamp":           "Timestamp",
    "model_used":          "Model",
    "order_item_quantity": "Quantity",
    "shipping_delay":      "Delay (d)",
    "profit_margin":       "Profit Margin",
    "order_month":         "Month",
    "is_weekend":          "Day Type",
    "predicted_sales":     "Predicted Sales",
})

st.dataframe(display_df, width="stretch", hide_index=True)

st.markdown(f"""
<div style='margin-top:2rem;text-align:center;font-family:Inter,sans-serif;
            font-size:0.71rem;color:#cbd5e1;'>
    {len(df)} record{"s" if len(df) != 1 else ""} shown ·
    predictions.db (read-only) · no model access in this process
</div>
""", unsafe_allow_html=True)

