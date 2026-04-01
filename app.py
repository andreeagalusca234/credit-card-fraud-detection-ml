import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "data", "transactions.csv")

df = pd.read_csv(file_path)

st.title("💳 Payment Risk Scoring Dashboard")

threshold = st.slider("Risk Threshold", 0.0, 1.0, 0.5)

df["decision"] = df["risk_score"].apply(
    lambda x: "Decline" if x >= threshold else "Approve"
)

fraud_caught = df[(df["actual"] == 1) & (df["decision"] == "Decline")].shape[0]
total_fraud = df[df["actual"] == 1].shape[0]

false_positives = df[(df["actual"] == 0) & (df["decision"] == "Decline")].shape[0]

st.metric("Fraud Recall", f"{fraud_caught / total_fraud:.2%}")
st.metric("False Positives", false_positives)

st.bar_chart(df["decision"].value_counts())