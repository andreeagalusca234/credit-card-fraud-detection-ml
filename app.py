import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payment Risk Scoring",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Notion-style CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #FFFFFF;
        color: #191919;
    }
    .stApp { background: #FFFFFF; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    .page-wrapper {
        max-width: 900px;
        margin: 0 auto;
        padding: 56px 40px 80px 40px;
    }
    .page-icon { font-size: 40px; margin-bottom: 8px; }
    .page-title {
        font-family: 'Crimson Pro', Georgia, serif;
        font-size: 42px; font-weight: 600;
        color: #191919; line-height: 1.2; margin-bottom: 6px;
    }
    .page-subtitle {
        font-size: 15px; font-weight: 300;
        color: #6B6B6B; margin-bottom: 32px;
        line-height: 1.6; max-width: 640px;
    }
    .notion-divider {
        border: none; border-top: 1px solid #E9E9E7; margin: 28px 0;
    }
    .section-label {
        font-size: 11px; font-weight: 500;
        letter-spacing: 0.08em; text-transform: uppercase;
        color: #9B9B9B; margin-bottom: 14px;
    }
    .callout {
        background: #F7F7F5; border-radius: 4px;
        padding: 14px 16px; font-size: 14px; color: #444;
        line-height: 1.65; margin-bottom: 24px;
        display: flex; gap: 10px; align-items: flex-start;
    }
    .callout-icon { font-size: 17px; margin-top: 1px; flex-shrink: 0; }
    .metrics-row {
        display: grid; grid-template-columns: repeat(4, 1fr);
        gap: 12px; margin-bottom: 20px;
    }
    .metric-card {
        border: 1px solid #E9E9E7; border-radius: 6px;
        padding: 16px 18px; background: #FFFFFF;
        transition: background 0.15s;
    }
    .metric-card:hover { background: #F7F7F5; }
    .metric-label {
        font-size: 12px; color: #9B9B9B;
        font-weight: 400; margin-bottom: 6px; letter-spacing: 0.02em;
    }
    .metric-value {
        font-family: 'Crimson Pro', Georgia, serif;
        font-size: 30px; font-weight: 600;
        color: #191919; line-height: 1; margin-bottom: 4px;
    }
    .metric-sub { font-size: 11px; color: #B0B0B0; font-weight: 300; }
    .metric-green .metric-value  { color: #0D7A5F; }
    .metric-amber .metric-value  { color: #A35200; }
    .metric-red   .metric-value  { color: #C0392B; }
    .metric-blue  .metric-value  { color: #0B5EA8; }

    .insight-line {
        font-size: 13px; color: #6B6B6B; line-height: 1.7;
        padding: 12px 16px; border-left: 3px solid #E9E9E7;
        margin-top: 16px; background: #FAFAFA;
        border-radius: 0 4px 4px 0;
    }
    .insight-line b { color: #191919; }

    .threshold-row {
        display: flex; gap: 10px; align-items: center;
        font-size: 13px; color: #6B6B6B; margin-bottom: 6px;
    }
    .threshold-dot {
        width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
    }

    .badge {
        display: inline-block; font-size: 12px; font-weight: 500;
        padding: 3px 10px; border-radius: 3px; letter-spacing: 0.03em;
    }
    .badge-approve { background: #DFFAEF; color: #0D7A5F; }
    .badge-review  { background: #FFF3CD; color: #A35200; }
    .badge-decline { background: #FDECEA; color: #C0392B; }

    .score-result {
        border: 1px solid #E9E9E7; border-radius: 6px;
        padding: 20px 22px; margin-top: 16px; background: #FAFAFA;
    }
    .score-number {
        font-family: 'Crimson Pro', Georgia, serif;
        font-size: 38px; font-weight: 600; color: #191919; margin-bottom: 4px;
    }
    .score-decision-label { font-size: 13px; color: #6B6B6B; margin-bottom: 12px; }
    .score-description {
        font-size: 13px; color: #444; line-height: 1.6;
        padding-top: 12px; border-top: 1px solid #E9E9E7;
    }

    .stSlider > div > div > div > div { background: #191919 !important; }
    .streamlit-expanderHeader {
        font-size: 13px !important; font-weight: 500 !important;
        color: #444 !important; background: #F7F7F5 !important;
        border-radius: 4px !important;
    }
    .stNumberInput input {
        border: 1px solid #E9E9E7 !important;
        border-radius: 4px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "data", "transactions.csv")

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

# ── Open wrapper ──────────────────────────────────────────────────────────────
st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-icon">💳</div>
<div class="page-title">Payment Risk Scoring</div>
<div class="page-subtitle">
    An interactive fraud detection engine built on XGBoost, trained on 284,807 real credit card
    transactions. Adjust the thresholds below to explore the tradeoff between fraud capture
    and customer friction.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="notion-divider">', unsafe_allow_html=True)

# ── Thresholds ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Risk Thresholds</div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_a:
    approve_threshold = st.slider(
        "Approve / Review boundary",
        min_value=0.0, max_value=1.0, value=0.20, step=0.01)
with col_b:
    decline_threshold = st.slider(
        "Review / Decline boundary",
        min_value=0.0, max_value=1.0, value=0.60, step=0.01)
with col_c:
    st.markdown(f"""
    <div style="padding-top:28px;">
        <div class="threshold-row">
            <div class="threshold-dot" style="background:#0D7A5F;"></div>
            Score &lt; {approve_threshold:.2f} &nbsp;→&nbsp; <b>Approve</b>
        </div>
        <div class="threshold-row">
            <div class="threshold-dot" style="background:#A35200;"></div>
            {approve_threshold:.2f} – {decline_threshold:.2f} &nbsp;→&nbsp; <b>Review</b>
        </div>
        <div class="threshold-row">
            <div class="threshold-dot" style="background:#C0392B;"></div>
            Score ≥ {decline_threshold:.2f} &nbsp;→&nbsp; <b>Decline</b>
        </div>
    </div>""", unsafe_allow_html=True)

if approve_threshold >= decline_threshold:
    st.warning("Approve threshold must be lower than Decline threshold.")
    st.stop()

# ── Compute ───────────────────────────────────────────────────────────────────
def risk_decision(score):
    if score < approve_threshold:   return "Approve"
    elif score < decline_threshold: return "Review"
    else:                            return "Decline"

df["decision"] = df["risk_score"].apply(risk_decision)

total_fraud     = df[df["actual"] == 1].shape[0]
fraud_caught    = df[(df["actual"] == 1) & (df["decision"] == "Decline")].shape[0]
fraud_review    = df[(df["actual"] == 1) & (df["decision"] == "Review")].shape[0]
fraud_missed    = df[(df["actual"] == 1) & (df["decision"] == "Approve")].shape[0]
false_positives = df[(df["actual"] == 0) & (df["decision"] == "Decline")].shape[0]
legit_review    = df[(df["actual"] == 0) & (df["decision"] == "Review")].shape[0]
legit_approved  = df[(df["actual"] == 0) & (df["decision"] == "Approve")].shape[0]

recall    = fraud_caught / total_fraud if total_fraud > 0 else 0
precision = fraud_caught / (fraud_caught + false_positives) if (fraud_caught + false_positives) > 0 else 0
protected = fraud_caught * 50

st.markdown('<hr class="notion-divider">', unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Live Performance</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card metric-green">
        <div class="metric-label">Fraud Recall</div>
        <div class="metric-value">{recall:.1%}</div>
        <div class="metric-sub">{fraud_caught} of {total_fraud} caught</div>
    </div>
    <div class="metric-card metric-blue">
        <div class="metric-label">Precision</div>
        <div class="metric-value">{precision:.1%}</div>
        <div class="metric-sub">of declines are true fraud</div>
    </div>
    <div class="metric-card metric-amber">
        <div class="metric-label">Sent to Review</div>
        <div class="metric-value">{legit_review + fraud_review:,}</div>
        <div class="metric-sub">incl. {fraud_review} fraud cases</div>
    </div>
    <div class="metric-card metric-red">
        <div class="metric-label">False Positives</div>
        <div class="metric-value">{false_positives:,}</div>
        <div class="metric-sub">legitimate txns declined</div>
    </div>
</div>
<div class="insight-line">
    At these thresholds the model catches <b>{recall:.1%} of fraud</b> —
    protecting an estimated <b>£{protected:,.0f}</b> in transaction value —
    while sending <b>{legit_review:,} legitimate transactions</b> to review
    and declining <b>{false_positives:,}</b> outright.
    Lowering the boundaries catches more fraud but increases analyst workload and customer friction.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="notion-divider">', unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Decision Analysis</div>', unsafe_allow_html=True)

LAYOUT = dict(
    plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
    font=dict(family="DM Sans, sans-serif", size=12, color="#444"),
    margin=dict(t=36, b=36, l=12, r=12), height=300,
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig1 = go.Figure()
    cats = ["Approve", "Review", "Decline"]
    fig1.add_trace(go.Bar(name="Legitimate", x=cats,
        y=[legit_approved, legit_review, false_positives],
        marker_color="#CBD5E1", marker_line_width=0))
    fig1.add_trace(go.Bar(name="Fraud", x=cats,
        y=[fraud_missed, fraud_review, fraud_caught],
        marker_color="#191919", marker_line_width=0))
    fig1.update_layout(**LAYOUT,
        title=dict(text="Decisions by Class", font=dict(size=13, color="#191919"), x=0),
        barmode="stack",
        legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11)),
        xaxis=dict(showgrid=False, linecolor="#E9E9E7"),
        yaxis=dict(gridcolor="#F0F0EE", linecolor="#E9E9E7"))
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    cm = [[legit_approved, legit_review, false_positives],
          [fraud_missed,   fraud_review, fraud_caught]]
    fig2 = go.Figure(go.Heatmap(
        z=cm, x=["Approve", "Review", "Decline"], y=["Legitimate", "Fraud"],
        colorscale=[[0, "#F7F7F5"], [1, "#191919"]],
        text=[[f"{v:,}" for v in row] for row in cm],
        texttemplate="%{text}", textfont=dict(size=14),
        showscale=False, xgap=3, ygap=3))
    fig2.update_layout(**LAYOUT,
        title=dict(text="Confusion Matrix", font=dict(size=13, color="#191919"), x=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="section-label" style="margin-top:8px;">Score Distribution</div>',
            unsafe_allow_html=True)

fig3 = go.Figure()
for cls, label, color in [(0, "Legitimate", "#CBD5E1"), (1, "Fraud", "#191919")]:
    fig3.add_trace(go.Histogram(
        x=df[df["actual"] == cls]["risk_score"], name=label,
        nbinsx=60, marker_color=color, opacity=0.75, marker_line_width=0))
fig3.add_vline(x=approve_threshold, line_dash="dot", line_color="#0D7A5F", line_width=1.5,
    annotation=dict(text=f"Approve {approve_threshold:.2f}",
                    font_size=11, font_color="#0D7A5F", yref="paper", y=1.05))
fig3.add_vline(x=decline_threshold, line_dash="dot", line_color="#C0392B", line_width=1.5,
    annotation=dict(text=f"Decline {decline_threshold:.2f}",
                    font_size=11, font_color="#C0392B", yref="paper", y=1.05))
LAYOUT3 = {**LAYOUT, "height": 260}
fig3.update_layout(**LAYOUT3, barmode="overlay",
    xaxis=dict(title="Risk Score", showgrid=False, linecolor="#E9E9E7"),
    yaxis=dict(title="Count", gridcolor="#F0F0EE", linecolor="#E9E9E7"),
    legend=dict(orientation="h", y=1.12, x=0, font=dict(size=11)))
st.plotly_chart(fig3, use_container_width=True)

st.markdown('<hr class="notion-divider">', unsafe_allow_html=True)

# ── Sample scorer ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Score a Transaction</div>', unsafe_allow_html=True)
st.markdown("""
<div class="callout">
    <span class="callout-icon">🔍</span>
    <div>Enter transaction details to simulate a real-time risk score based on
    amount and time-of-day signals — the features the model weighs most
    heavily alongside the anonymised PCA components.</div>
</div>""", unsafe_allow_html=True)

t1, t2, t3 = st.columns([1, 1, 1])
with t1:
    amount = st.number_input("Amount (£)", min_value=0.0,
                              max_value=50000.0, value=120.0, step=10.0)
with t2:
    hour = st.slider("Hour of Day", 0, 23, 14, format="%d:00")
with t3:
    is_night = 1 if (hour < 6 or hour >= 22) else 0
    st.markdown(f"""
    <div style="padding-top:28px; font-size:13px;
                color:{'#A35200' if is_night else '#0D7A5F'}; font-weight:500;">
        {'Night transaction ⚠️' if is_night else 'Daytime transaction ✓'}
    </div>
    <div style="font-size:12px; color:#9B9B9B; margin-top:4px;">
        Night window: 22:00 – 06:00
    </div>""", unsafe_allow_html=True)

base = 0.04
if is_night:      base += 0.28
if amount > 2000: base += 0.22
elif amount > 500: base += 0.12
elif amount > 200: base += 0.06
base += min(np.log1p(amount) / 40, 0.08)
rng   = np.random.default_rng(int(amount * 100 + hour))
score = float(np.clip(base + rng.uniform(-0.02, 0.02), 0.01, 0.98))
score = round(score, 3)

decision = risk_decision(score)
d_badges = {"Approve": "badge-approve", "Review": "badge-review", "Decline": "badge-decline"}
d_desc   = {
    "Approve": "Score is below the review boundary. Transaction proceeds automatically — no friction for the customer.",
    "Review":  "Score falls in the review zone. Flagged for manual analyst review or step-up authentication (e.g. OTP).",
    "Decline": "Score exceeds the decline boundary. Transaction blocked and customer notified to contact their bank."
}

st.markdown(f"""
<div class="score-result">
    <div class="score-number">{score:.3f}</div>
    <div class="score-decision-label">
        Risk score &nbsp;·&nbsp;
        <span class="badge {d_badges[decision]}">{decision}</span>
    </div>
    <div class="score-description">{d_desc[decision]}</div>
</div>""", unsafe_allow_html=True)

st.markdown('<hr class="notion-divider">', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;
            font-size:12px; color:#B0B0B0; padding-top:4px;">
    <span>Andreea Galusca &nbsp;·&nbsp; MSc Analytics &amp; Management &nbsp;·&nbsp; London Business School</span>
    <a href="https://github.com/andreeagalusca234/credit-card-fraud-detection-ml"
       style="color:#B0B0B0; text-decoration:none;">GitHub ↗</a>
</div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
