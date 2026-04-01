import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
 
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payment Risk Scoring Dashboard",
    page_icon="💳",
    layout="wide"
)
 
# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 4px solid #1A73E8;
        margin-bottom: 8px;
    }
    .metric-label { font-size: 13px; color: #666; margin-bottom: 4px; }
    .metric-value { font-size: 28px; font-weight: 700; color: #1A1A2E; }
    .metric-sub   { font-size: 12px; color: #888; margin-top: 2px; }
    .approve  { border-left-color: #34A853; }
    .review   { border-left-color: #FBBC04; }
    .decline  { border-left-color: #EA4335; }
    .section-header {
        font-size: 16px; font-weight: 700; color: #1A1A2E;
        border-bottom: 2px solid #1A73E8;
        padding-bottom: 6px; margin: 20px 0 12px 0;
    }
    .explainer {
        background: #EEF4FF; border-radius: 8px;
        padding: 14px 18px; font-size: 13px; color: #333;
        margin-bottom: 16px; line-height: 1.6;
    }
    .insight-box {
        background: #1A73E8; border-radius: 8px;
        padding: 14px 18px; color: white;
        font-size: 13px; margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)
 
# ── Load data ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "data", "transactions.csv")
 
@st.cache_data
def load_data():
    return pd.read_csv(file_path)
 
df = load_data()
 
# ── Header ────────────────────────────────────────────────────────────────────
st.title("💳 Payment Risk Scoring Dashboard")
st.markdown("""
<div class="explainer">
    This dashboard simulates a <b>real-time fraud detection engine</b> powered by an XGBoost model 
    trained on 284,807 credit card transactions. Each transaction receives a <b>risk score (0–1)</b>. 
    The threshold controls where the boundaries sit between <b>Approve</b>, <b>Review</b>, and <b>Decline</b> — 
    a business decision that trades off fraud capture rate against customer friction.
</div>
""", unsafe_allow_html=True)
 
# ── Threshold controls ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">⚙️ Risk Threshold Controls</div>', unsafe_allow_html=True)
 
col1, col2 = st.columns(2)
with col1:
    approve_threshold = st.slider(
        "Approve / Review boundary",
        min_value=0.0, max_value=1.0, value=0.20, step=0.01,
        help="Transactions below this score are automatically approved"
    )
with col2:
    decline_threshold = st.slider(
        "Review / Decline boundary",
        min_value=0.0, max_value=1.0, value=0.60, step=0.01,
        help="Transactions above this score are declined"
    )
 
if approve_threshold >= decline_threshold:
    st.warning("⚠️ Approve threshold must be lower than Decline threshold.")
    st.stop()
 
# ── Apply three-tier decision engine ─────────────────────────────────────────
def risk_decision(score):
    if score < approve_threshold:
        return "Approve"
    elif score < decline_threshold:
        return "Review"
    else:
        return "Decline"
 
df["decision"] = df["risk_score"].apply(risk_decision)
 
total_fraud     = df[df["actual"] == 1].shape[0]
total_legit     = df[df["actual"] == 0].shape[0]
 
fraud_caught    = df[(df["actual"] == 1) & (df["decision"] == "Decline")].shape[0]
fraud_review    = df[(df["actual"] == 1) & (df["decision"] == "Review")].shape[0]
fraud_approved  = df[(df["actual"] == 1) & (df["decision"] == "Approve")].shape[0]
 
false_positives = df[(df["actual"] == 0) & (df["decision"] == "Decline")].shape[0]
legit_review    = df[(df["actual"] == 0) & (df["decision"] == "Review")].shape[0]
legit_approved  = df[(df["actual"] == 0) & (df["decision"] == "Approve")].shape[0]
 
recall      = fraud_caught / total_fraud if total_fraud > 0 else 0
precision   = fraud_caught / (fraud_caught + false_positives) if (fraud_caught + false_positives) > 0 else 0
avg_tx      = 50
fraud_protected = fraud_caught * avg_tx
 
# ── Key metrics ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Live Performance Metrics</div>', unsafe_allow_html=True)
 
m1, m2, m3, m4, m5 = st.columns(5)
 
with m1:
    st.markdown(f"""
    <div class="metric-card decline">
        <div class="metric-label">Fraud Recall</div>
        <div class="metric-value">{recall:.1%}</div>
        <div class="metric-sub">of {total_fraud} fraud cases caught</div>
    </div>""", unsafe_allow_html=True)
 
with m2:
    st.markdown(f"""
    <div class="metric-card approve">
        <div class="metric-label">Precision</div>
        <div class="metric-value">{precision:.1%}</div>
        <div class="metric-sub">of declines are true fraud</div>
    </div>""", unsafe_allow_html=True)
 
with m3:
    st.markdown(f"""
    <div class="metric-card review">
        <div class="metric-label">False Positives</div>
        <div class="metric-value">{false_positives:,}</div>
        <div class="metric-sub">legit txns declined</div>
    </div>""", unsafe_allow_html=True)
 
with m4:
    st.markdown(f"""
    <div class="metric-card review">
        <div class="metric-label">Sent to Review</div>
        <div class="metric-value">{legit_review + fraud_review:,}</div>
        <div class="metric-sub">incl. {fraud_review} fraud cases</div>
    </div>""", unsafe_allow_html=True)
 
with m5:
    st.markdown(f"""
    <div class="metric-card approve">
        <div class="metric-label">Value Protected</div>
        <div class="metric-value">£{fraud_protected:,.0f}</div>
        <div class="metric-sub">at £{avg_tx} avg transaction</div>
    </div>""", unsafe_allow_html=True)
 
# ── Business insight callout ──────────────────────────────────────────────────
st.markdown(f"""
<div class="insight-box">
    💡 <b>Business interpretation:</b> At these thresholds, the model catches <b>{recall:.1%} of fraud</b> 
    while sending <b>{legit_review:,} legitimate transactions</b> to manual review and declining 
    <b>{false_positives:,} legitimate transactions</b> outright. 
    Lowering the Review/Decline boundary catches more fraud but increases analyst workload and customer friction.
</div>
""", unsafe_allow_html=True)
 
# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Decision Distribution & Confusion Matrix</div>', unsafe_allow_html=True)
 
chart_col1, chart_col2 = st.columns(2)
 
# Decision distribution by class
with chart_col1:
    decision_counts = df.groupby(["decision", "actual"]).size().reset_index(name="count")
    decision_counts["Class"] = decision_counts["actual"].map({0: "Legitimate", 1: "Fraud"})
 
    fig1 = go.Figure()
    colors = {"Legitimate": "#4C72B0", "Fraud": "#DD8452"}
    for cls in ["Legitimate", "Fraud"]:
        d = decision_counts[decision_counts["Class"] == cls]
        fig1.add_trace(go.Bar(
            x=d["decision"], y=d["count"],
            name=cls, marker_color=colors[cls], opacity=0.85
        ))
 
    fig1.update_layout(
        title="Transaction Decisions by Class",
        barmode="group",
        xaxis=dict(categoryorder="array", categoryarray=["Approve", "Review", "Decline"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=60, b=40),
        height=340
    )
    fig1.update_yaxes(gridcolor="#eeeeee")
    st.plotly_chart(fig1, use_container_width=True)
 
# Confusion matrix
with chart_col2:
    cm = np.array([
        [legit_approved, legit_review, false_positives],
        [fraud_approved, fraud_review, fraud_caught]
    ])
 
    fig2 = go.Figure(go.Heatmap(
        z=cm,
        x=["Approve", "Review", "Decline"],
        y=["Legitimate", "Fraud"],
        colorscale=[[0, "#EEF4FF"], [1, "#1A73E8"]],
        text=cm, texttemplate="%{text:,}",
        textfont={"size": 16, "color": "white"},
        showscale=False
    ))
    fig2.update_layout(
        title="Confusion Matrix",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=60, b=40),
        height=340
    )
    st.plotly_chart(fig2, use_container_width=True)
 
# ── Risk score distribution ───────────────────────────────────────────────────
st.markdown('<div class="section-header">🎯 Risk Score Distribution</div>', unsafe_allow_html=True)
 
fig3 = go.Figure()
for cls, label, color in [(0, "Legitimate", "#4C72B0"), (1, "Fraud", "#DD8452")]:
    fig3.add_trace(go.Histogram(
        x=df[df["actual"] == cls]["risk_score"],
        name=label, nbinsx=60,
        marker_color=color, opacity=0.6
    ))
 
fig3.add_vline(x=approve_threshold, line_dash="dash", line_color="#34A853", line_width=2,
               annotation_text=f"Approve/Review ({approve_threshold:.2f})",
               annotation_position="top right")
fig3.add_vline(x=decline_threshold, line_dash="dash", line_color="#EA4335", line_width=2,
               annotation_text=f"Review/Decline ({decline_threshold:.2f})",
               annotation_position="top left")
 
fig3.update_layout(
    barmode="overlay",
    xaxis_title="Risk Score", yaxis_title="Count",
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    plot_bgcolor="white", paper_bgcolor="white",
    height=300, margin=dict(t=40, b=40)
)
fig3.update_yaxes(gridcolor="#eeeeee")
st.plotly_chart(fig3, use_container_width=True)
 
# ── Sample transaction scorer ─────────────────────────────────────────────────
st.markdown('<div class="section-header">🔍 Score a Sample Transaction</div>', unsafe_allow_html=True)
st.markdown("Enter transaction details below to get an instant risk score and decision.")
 
with st.expander("Enter transaction details", expanded=True):
    t1, t2, t3 = st.columns(3)
    with t1:
        amount = st.number_input("Transaction Amount (£)", min_value=0.0, max_value=50000.0, value=120.0, step=10.0)
    with t2:
        hour = st.slider("Hour of Day", 0, 23, 14)
    with t3:
        is_night = 1 if (hour < 6 or hour >= 22) else 0
        st.metric("Night Transaction", "Yes ⚠️" if is_night else "No ✅")
 
    # Simulate a risk score based on inputs (since we don't have the model serialised)
    amount_log = np.log1p(amount)
    base_score = 0.05
    if is_night:
        base_score += 0.25
    if amount > 1000:
        base_score += 0.20
    elif amount > 500:
        base_score += 0.10
    if amount_log > 5:
        base_score += 0.10
    simulated_score = min(round(base_score + np.random.uniform(-0.03, 0.03), 3), 0.99)
 
    decision = risk_decision(simulated_score)
    decision_colors = {"Approve": "#34A853", "Review": "#FBBC04", "Decline": "#EA4335"}
    decision_icons  = {"Approve": "✅", "Review": "🔍", "Decline": "❌"}
 
    st.markdown(f"""
    <div style="margin-top:16px; padding:16px 20px; border-radius:10px;
                background:{decision_colors[decision]}22;
                border-left: 5px solid {decision_colors[decision]};">
        <b style="font-size:15px;">Risk Score: {simulated_score:.3f}</b><br>
        <span style="font-size:22px; font-weight:700; color:{decision_colors[decision]};">
            {decision_icons[decision]} {decision}
        </span><br>
        <span style="font-size:12px; color:#555;">
            {"Transaction approved automatically." if decision == "Approve"
             else "Flagged for manual review or step-up authentication." if decision == "Review"
             else "Transaction blocked. Customer will be notified."}
        </span>
    </div>
    """, unsafe_allow_html=True)
 
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:12px; color:#aaa;'>"
    "Built by Andreea Galusca · MSc Analytics & Management · London Business School · "
    "<a href='https://github.com/andreeagalusca234/credit-card-fraud-detection-ml' "
    "style='color:#1A73E8;'>GitHub Repo</a></div>",
    unsafe_allow_html=True
)