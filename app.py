import streamlit as st
import pandas as pd
import numpy as np
import pickle

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Fraud Detection App",
    page_icon="💳",
    layout="wide"
)

# -----------------------
# LOAD MODEL
# -----------------------
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# -----------------------
# SIDEBAR NAVIGATION
# -----------------------
page = st.sidebar.radio("Navigation", [
    "🏠 Overview",
    "📊 Data Exploration",
    "🤖 Model",
    "🔮 Prediction",
    "📈 Results & Insights"
])

# -----------------------
# OVERVIEW PAGE
# -----------------------
if page == "🏠 Overview":
    st.title("💳 Credit Card Fraud Detection")

    st.markdown("""
    ### 🚀 Project Overview
    This application uses Machine Learning to detect fraudulent credit card transactions.

    Fraud detection is a critical challenge because fraudulent transactions are **rare but costly**.
    The dataset is highly imbalanced, making detection more complex.

    ### 🎯 Objective
    - Detect fraudulent transactions
    - Minimize false positives (blocking real users)
    - Provide real-time predictions

    ### 🧠 Approach
    - Machine Learning models tested: Logistic Regression, Random Forest
    - Final model: Random Forest Classifier
    - Focus on handling class imbalance

    ### 💡 Business Impact
    Fraud detection systems help:
    - Reduce financial losses
    - Improve customer trust
    - Enable safer digital payments
    """)

    st.info("👉 Use the sidebar to explore the data, model, and make predictions.")

    st.markdown("[🔗 View GitHub Repository](https://github.com/andreeagalusca234/credit-card-fraud-detection-ml)")

# -----------------------
# DATA PAGE
# -----------------------
elif page == "📊 Data Exploration":
    st.title("📊 Data Exploration")

    df = pd.read_csv("creditcard.csv")

    if st.checkbox("Show dataset"):
        st.dataframe(df.head())

    st.subheader("Class Distribution")
    st.bar_chart(df["Class"].value_counts())

    st.markdown("""
    ### 🔍 Key Observations
    - Fraud cases are extremely rare
    - Dataset is highly imbalanced
    - Special handling is required for model training
    """)

# -----------------------
# MODEL PAGE
# -----------------------
elif page == "🤖 Model":
    st.title("🤖 Model Overview")

    st.markdown("""
    ### Model Used
    **Random Forest Classifier**

    ### Why this model?
    - Handles non-linear patterns well
    - Robust to noise
    - Performs well on imbalanced datasets

    ### Evaluation Metrics
    - Accuracy
    - Precision
    - Recall
    - F1-score

    ### Key Challenge
    Detecting rare fraud cases without flagging too many normal transactions.
    """)

# -----------------------
# PREDICTION PAGE
# -----------------------
elif page == "🔮 Prediction":
    st.title("🔮 Fraud Prediction")

    st.markdown("Enter transaction details below:")

    # Example inputs (adjust based on your model)
    amount = st.number_input("Transaction Amount", min_value=0.0)
    time = st.number_input("Transaction Time", min_value=0.0)

    if st.button("Predict"):
        input_data = np.array([[time, amount]])

        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.error("🚨 Fraudulent Transaction Detected")
        else:
            st.success("✅ Legitimate Transaction")

        st.write("Prediction is based on learned transaction patterns.")

# -----------------------
# RESULTS PAGE
# -----------------------
elif page == "📈 Results & Insights":
    st.title("📈 Results & Insights")

    st.markdown("""
    ### Model Performance
    - Accuracy: ~99%
    - Precision: High
    - Recall: Strong detection of fraud cases
    - F1-score: Balanced performance

    ### 🔍 Key Insights
    - Fraud transactions are rare but impactful
    - Certain transaction patterns increase fraud probability
    - Model successfully identifies anomalies

    ### ⚠️ Limitations
    - Model depends on historical data
    - May struggle with new fraud patterns
    - Requires continuous retraining

    ### 🚀 Future Improvements
    - Add real-time data pipeline
    - Improve feature engineering
    - Use deep learning models
    """)
