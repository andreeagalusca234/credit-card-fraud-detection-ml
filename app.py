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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FBFBFA;
        color: #37352F;
        -webkit-font-smoothing: antialiased;
    }
    .stApp { background: #FBFBFA; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0.75rem 0.5rem !important; max-width: 1100px !important; margin: 0 auto !important; }

    .page-wrapper {
        max-width: 900px;
        margin: 0 auto;
        padding: 56px 60px 80px 60px;
    }
    .page-icon { font-size: 38px; margin-bottom: 10px; }
    .page-title {
        font-family: 'Inter', sans-serif;
        font-size: 34px; font-weight: 700;
        color: #37352F; line-height: 1.15;
        letter-spacing: -0.02em; margin-bottom: 8px;
    }
    .page-subtitle {
        font-size: 14px; font-weight: 400;
        color: #787774; margin-bottom: 32px;
        line-height: 1.65; max-width: 620px;
    }
    .notion-divider {
        border: none; border-top: 1px solid #E9E9E7; margin: 24px 0;
    }
    .section-label {
        font-size: 11px; font-weight: 600;
        letter-spacing: 0.06em; text-transform: uppercase;
        color: #9B9A97; margin-bottom: 12px;
    }
    .callout {
        background: #F1F1EF; border-radius: 3px;
        padding: 12px 14px; font-size: 13.5px; color: #37352F;
        line-height: 1.6; margin-bottom: 22px;
        display: flex; gap: 10px; align-items: flex-start;
    }
    .callout-icon { font-size: 16px; margin-top: 1px; flex-shrink: 0; }
    .metrics-row {
        display: grid; grid-template-columns: repeat(4, 1fr);
        gap: 10px; margin-bottom: 18px;
    }
    .metric-card {
        border: 1px solid #E9E9E7; border-radius: 3px;
        padding: 14px 16px; background: #FFFFFF;
        transition: background 0.12s;
    }
    .metric-card:hover { background: #F7F7F5; }
    .metric-label {
        font-size: 11px; font-weight: 500;
        color: #9B9A97; margin-bottom: 6px;
        letter-spacing: 0.04em; text-transform: uppercase;
    }
    .metric-value {
        font-size: 28px; font-weight: 600;
        color: #37352F; line-height: 1;
        margin-bottom: 5px; letter-spacing: -0.02em;
    }
    .metric-sub { font-size: 11px; color: #B0AEAB; font-weight: 400; }
    .metric-green .metric-value { color: #0F7B6C; }
    .metric-amber .metric-value { color: #AD6B00; }
    .metric-red   .metric-value { color: #C0392B; }
    .metric-blue  .metric-value { color: #0B5EA8; }

    .insight-line {
        font-size: 13px; color: #787774; line-height: 1.7;
        padding: 10px 14px; border-left: 2px solid #D3D1CB;
        margin-top: 14px; background: #F7F7F5;
        border-radius: 0 3px 3px 0;
    }
    .insight-line b { color: #37352F; font-weight: 600; }

    .threshold-row {
        display: flex; gap: 10px; align-items: center;
        font-size: 13px; color: #787774; margin-bottom: 6px;
    }
    .threshold-dot {
        width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
    }

    .badge {
        display: inline-block; font-size: 11.5px; font-weight: 500;
        padding: 2px 8px; border-radius: 3px; letter-spacing: 0.02em;
    }
    .badge-approve { background: #DDEDEA; color: #0F7B6C; }
    .badge-review  { background: #FDECC8; color: #AD6B00; }
    .badge-decline { background: #FFE2DD; color: #C0392B; }

    .score-result {
        border: 1px solid #E9E9E7; border-radius: 3px;
        padding: 18px 20px; margin-top: 14px; background: #F7F7F5;
    }
    .score-number {
        font-size: 34px; font-weight: 600;
        color: #37352F; letter-spacing: -0.02em; margin-bottom: 4px;
    }
    .score-decision-label { font-size: 13px; color: #787774; margin-bottom: 10px; }
    .score-description {
        font-size: 13px; color: #37352F; line-height: 1.6;
        padding-top: 10px; border-top: 1px solid #E9E9E7;
    }

    .stSlider > div > div > div > div { background: #37352F !important; }
    .stNumberInput input {
        border: 1px solid #E9E9E7 !important;
        border-radius: 3px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        background: #FFFFFF !important;
        color: #37352F !important;
    }
    label[data-testid="stWidgetLabel"] {
        font-size: 12px !important; font-weight: 500 !important;
        color: #787774 !important; letter-spacing: 0.02em !important;
    }
    .github-btn {
        position: fixed;
        top: 16px; right: 24px;
        z-index: 9999;
        background: #37352F;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        font-size: 12px; font-weight: 500;
        padding: 7px 14px;
        border-radius: 3px;
        text-decoration: none !important;
        letter-spacing: 0.02em;
        display: flex; align-items: center; gap: 6px;
        transition: background 0.15s;
    }
    .github-btn:hover { background: #555450; }

    /* ── Project summary ── */
    .summary-grid {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 10px; margin-bottom: 10px;
    }
    .summary-card {
        border: 1px solid #E9E9E7; border-radius: 3px;
        padding: 16px 18px; background: #FFFFFF;
    }
    .summary-card h4 {
        font-size: 11px; font-weight: 600;
        letter-spacing: 0.06em; text-transform: uppercase;
        color: #9B9A97; margin: 0 0 10px 0;
    }
    .summary-card p {
        font-size: 13px; color: #787774; line-height: 1.7; margin: 0;
    }
    .summary-card p b { color: #37352F; }
    .summary-card-full {
        border: 1px solid #E9E9E7; border-radius: 3px;
        padding: 16px 18px; background: #FFFFFF; margin-bottom: 10px;
    }
    .summary-card-full h4 {
        font-size: 11px; font-weight: 600;
        letter-spacing: 0.06em; text-transform: uppercase;
        color: #9B9A97; margin: 0 0 10px 0;
    }
    .summary-card-full p {
        font-size: 13px; color: #787774; line-height: 1.7; margin: 0;
    }
    .summary-card-full p b { color: #37352F; }
    .results-table {
        width: 100%; border-collapse: collapse; font-size: 12.5px;
    }
    .results-table th {
        font-size: 11px; font-weight: 600; color: #9B9A97;
        letter-spacing: 0.05em; text-transform: uppercase;
        padding: 5px 10px; text-align: left;
        border-bottom: 1px solid #E9E9E7;
    }
    .results-table td {
        padding: 7px 10px; color: #37352F;
        border-bottom: 1px solid #F1F1EF;
    }
    .results-table tr:last-child td { border-bottom: none; }
    .results-table .winner td { font-weight: 600; color: #0F7B6C; }
    .pill-row { display: flex; flex-wrap: wrap; gap: 6px; }
    .pill {
        font-size: 11.5px; font-weight: 500;
        padding: 3px 10px; border-radius: 20px;
        background: #F1F1EF; color: #37352F;
    }
    .learning-row {
        font-size: 13px; color: #787774; line-height: 1.65;
        padding: 7px 0; border-bottom: 1px solid #F1F1EF;
        display: flex; gap: 10px; align-items: baseline;
    }
    .learning-row:last-child { border-bottom: none; padding-bottom: 0; }
    .learning-row b { color: #37352F; }
    .learning-dot {
        width: 4px; height: 4px; border-radius: 50%;
        background: #C8C6C2; flex-shrink: 0; margin-top: 8px;
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
st.markdown('''
<a class="github-btn" href="https://github.com/andreeagalusca234/credit-card-fraud-detection-ml" target="_blank">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
    </svg>
    GitHub ↗
</a>
''', unsafe_allow_html=True)

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
        legend=dict(orientation="h", y=-0.2, x=0, font=dict(size=11)),
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

# ── Project Summary ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">About this Project</div>', unsafe_allow_html=True)

with st.expander("Overview, methodology & results", expanded=False):
    st.markdown("""
    <div class="summary-card-full">
        <h4>Problem & Motivation</h4>
        <p>
            Credit card fraud costs the global financial industry over <b>$30 billion annually</b>.
            Traditional rule-based systems generate excessive false positives, frustrating legitimate customers.
            This project builds an end-to-end ML pipeline that assigns a continuous risk score to each
            transaction — mirroring how production systems at companies like Revolut, Monzo, and Visa operate.
            The dataset contains <b>284,807 transactions</b> with only <b>0.17% fraud cases</b>, a realistic
            and challenging class imbalance scenario.
        </p>
    </div>

    <div class="summary-grid">
        <div class="summary-card">
            <h4>Dataset</h4>
            <p>
                Source: Kaggle / ULB Machine Learning Group.<br><br>
                Features <b>V1–V28</b> are PCA-transformed (anonymised for confidentiality).
                <b>Amount</b> is the transaction value in EUR; <b>Time</b> is seconds elapsed
                since the first transaction. No missing values. 492 fraud cases across two days.
            </p>
        </div>
        <div class="summary-card">
            <h4>Class Imbalance — SMOTE</h4>
            <p>
                Standard accuracy is misleading when 99.83% of transactions are legitimate.
                <b>SMOTE</b> (Synthetic Minority Over-sampling Technique) generates synthetic fraud
                samples during training only — applied carefully to prevent data leakage into
                the validation set.
            </p>
        </div>
        <div class="summary-card">
            <h4>Feature Engineering</h4>
            <p>
                Three engineered features boosted signal beyond the raw PCA components:
                <b>Amount_log</b> (log-transform to reduce skew), <b>Hour</b> (extracted from
                Time for within-day patterns), and <b>Is_night</b> (binary flag for the
                22:00–06:00 window, which correlates strongly with fraud).
            </p>
        </div>
        <div class="summary-card">
            <h4>Evaluation Strategy</h4>
            <p>
                ROC-AUC alone is insufficient on imbalanced data. Primary metrics:
                <b>PR-AUC</b> (Precision-Recall AUC), <b>Recall on fraud class</b>
                (how much fraud did we catch?), and <b>Precision on fraud class</b>
                (false alarm rate for operations teams).
            </p>
        </div>
    </div>

    <div class="summary-card-full">
        <h4>Model Comparison</h4>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Model</th>
                    <th>ROC-AUC</th>
                    <th>PR-AUC</th>
                    <th>Recall (Fraud)</th>
                    <th>F1</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Logistic Regression</td>
                    <td>~0.97</td><td>~0.73</td><td>~0.81</td><td>~0.77</td>
                </tr>
                <tr>
                    <td>Random Forest</td>
                    <td>~0.98</td><td>~0.84</td><td>~0.83</td><td>~0.86</td>
                </tr>
                <tr class="winner">
                    <td>✦ XGBoost (selected)</td>
                    <td>~0.98</td><td>~0.87</td><td>~0.86</td><td>~0.88</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="summary-card-full">
        <h4>Estimated Business Impact</h4>
        <p>
            Applied to a hypothetical platform processing <b>1 million transactions/day</b> at £50 average value:
            ~1,700 fraudulent transactions occur daily. XGBoost catches ~1,460 of them (<b>86% recall</b>),
            protecting an estimated <b>~£73,000/day</b> in fraud value. Precision above 90% keeps
            unnecessary customer friction low.
        </p>
    </div>

    <div class="summary-card-full">
        <h4>Key Learnings</h4>
        <div class="learning-row">
            <div class="learning-dot"></div>
            <span><b>Class imbalance is the core challenge.</b> SMOTE and PR-AUC are essential, not optional — standard accuracy is a misleading metric on this data.</span>
        </div>
        <div class="learning-row">
            <div class="learning-dot"></div>
            <span><b>Threshold tuning is a business decision.</b> The right cutoff depends on operational capacity and risk appetite — which is exactly what this dashboard lets you explore interactively.</span>
        </div>
        <div class="learning-row">
            <div class="learning-dot"></div>
            <span><b>Feature engineering amplified signal.</b> Time-of-day and log-amount meaningfully improved recall across all three models, even alongside 28 PCA components.</span>
        </div>
        <div class="learning-row">
            <div class="learning-dot"></div>
            <span><b>XGBoost dominates on tabular fraud data</b> due to its regularisation and handling of feature interactions. It outperformed both the baseline and Random Forest on every metric.</span>
        </div>
    </div>

    <div class="summary-card-full" style="margin-bottom:0;">
        <h4>Tech Stack</h4>
        <div class="pill-row">
            <span class="pill">Python 3.10</span>
            <span class="pill">XGBoost</span>
            <span class="pill">scikit-learn</span>
            <span class="pill">imbalanced-learn / SMOTE</span>
            <span class="pill">pandas</span>
            <span class="pill">numpy</span>
            <span class="pill">Streamlit</span>
            <span class="pill">Plotly</span>
            <span class="pill">matplotlib</span>
            <span class="pill">seaborn</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
