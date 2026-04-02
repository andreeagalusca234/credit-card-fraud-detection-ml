# 💳 Credit Card Fraud Detection - Machine Learning

> 📎 [View 1-page project summary](./report/credit-fraud-detection-summary.pdf)

## 📌 Overview

This project builds an end-to-end machine learning pipeline to detect fraudulent credit card transactions in real time. The dataset contains **284,807 transactions** with only **0.17% fraud cases**, a realistic and challenging class imbalance scenario mirroring production systems at companies like Revolut, Monzo, and Visa.

The output is not just a model - it is a **risk decision engine** that translates fraud probability scores into business actions: Approve, Review, or Decline.

---

## 🎯 Business Problem

Credit card fraud costs the global financial industry over **$30 billion annually**. Traditional rule-based systems flag too many false positives, frustrating customers. ML-powered solutions can:

- Detect complex, evolving fraud patterns that rules miss
- Assign continuous risk scores rather than binary decisions
- Reduce false positives while maintaining high fraud recall
- Scale to millions of transactions per day

This project demonstrates how data science can directly protect revenue and improve customer experience.

---

## 📊 Dataset

**Source:** [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) (ULB Machine Learning Group)

| Feature | Description |
|---|---|
| `V1–V28` | PCA-transformed features (anonymised for confidentiality) |
| `Amount` | Transaction value in EUR |
| `Time` | Seconds elapsed since first transaction |
| `Class` | Target — 0: Legitimate, 1: Fraud |

- **284,807** transactions over 2 days
- **492** fraud cases (0.17%)
- No missing values

---

## 🔍 Approach

### 1. Exploratory Data Analysis (EDA)

- Analysed class imbalance and fraud rate
- Compared transaction amount and time patterns between classes
- Identified correlations between PCA features and fraud label

### 2. Class Imbalance Handling — SMOTE

Standard accuracy metrics are misleading when 99.83% of transactions are legitimate. **SMOTE** (Synthetic Minority Over-sampling Technique) generates synthetic fraud samples during training to balance the learning signal — applied only to the training set to prevent data leakage.

### 3. Feature Engineering

- `Amount_log` — log-transformed transaction amount to reduce skew
- `Hour` — extracted from `Time` to capture within-day patterns
- `Is_night` — binary flag for transactions between 22:00–06:00

### 4. Model Development

Three models were trained and compared:

| Model | Role |
|---|---|
| Logistic Regression | Interpretable baseline |
| Random Forest | Non-linear ensemble, robust to outliers |
| XGBoost | Best-in-class for tabular fraud detection |

### 5. Evaluation Strategy

Given class imbalance, standard accuracy is meaningless. Evaluation uses:

- **ROC-AUC** — overall discrimination ability
- **Average Precision (PR-AUC)** — more informative on imbalanced data
- **Recall on fraud class** — business-critical: how much fraud did we catch?
- **Precision on fraud class** — false alarm rate for operations teams

---

## 📈 Results

| Model | ROC-AUC | Avg Precision | Recall (Fraud) | F1 |
|---|---|---|---|---|
| Logistic Regression | ~0.97 | ~0.73 | ~0.81 | ~0.77 |
| Random Forest | ~0.98 | ~0.84 | ~0.83 | ~0.86 |
| **XGBoost** | **~0.98** | **~0.87** | **~0.86** | **~0.88** |

**XGBoost** was selected as the production model.

---

## ⚙️ Risk Decision Engine

The model's probability output feeds a tiered decision engine:

| Risk Score | Decision | Business Action |
|---|---|---|
| < 0.20 | ✅ **Approve** | Transaction proceeds automatically |
| 0.20 – 0.60 | 🔍 **Review** | Flagged for analyst review or step-up auth |
| ≥ 0.60 | ❌ **Decline** | Transaction blocked, customer notified |

This mirrors real-world systems where fraud probability is a continuous signal, not a hard binary — allowing business teams to tune thresholds based on risk tolerance and operational capacity.

---

## 💼 Business Impact

Applied to a hypothetical platform processing **1 million transactions/day** at £50 average:

- ~1,700 fraudulent transactions daily
- XGBoost catches ~1,460 (86% recall)
- Protects an estimated **~£73,000/day** in fraud value
- Precision >90% minimises unnecessary customer friction

---

## 🧠 Key Learnings

- **Class imbalance is the core challenge** — SMOTE and PR-AUC are essential, not optional
- **ROC-AUC alone is insufficient** on imbalanced data; Precision-Recall AUC is more meaningful
- **Threshold tuning is a business decision**, not a data science one
- **Feature engineering amplified signal** — time-of-day and log-amount improved both models
- **XGBoost dominates on tabular fraud data** due to its regularisation and handling of feature interactions

---

## 🛠️ Tech Stack

- **Python 3.10**
- `pandas`, `numpy` — data manipulation
- `scikit-learn` — modelling, preprocessing, evaluation
- `imbalanced-learn` — SMOTE
- `xgboost` — gradient boosted trees
- `matplotlib`, `seaborn` — visualisation

---

## 📁 Repository Structure

```
credit-card-fraud-detection-ml/
│
├── notebook/
│   └── credit_fraud_detection_ml.ipynb   # Full ML pipeline
│
├── data/
│   └── README.md                          # Dataset download instructions
│
├── report/
│   ├── class_distribution.png
│   ├── amount_distribution.png
│   ├── time_distribution.png
│   ├── correlation_heatmap.png
│   ├── roc_pr_curves.png
│   ├── confusion_matrices.png
│   ├── feature_importance.png
│   ├── risk_score_distribution.png
│   └── credit-fraud-detection-summary.pdf
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/andreeagalusca234/credit-card-fraud-detection-ml.git
cd credit-card-fraud-detection-ml

# Install dependencies
pip install -r requirements.txt

# Download dataset
# See data/README.md for instructions (Kaggle API or manual download)

# Run the notebook
jupyter notebook notebook/credit_fraud_detection_ml.ipynb
```

---

## 🔮 Future Improvements

- Deploy the model as a REST API (FastAPI)
- Add real-time inference pipeline with streaming data (Kafka)
- Implement model monitoring and drift detection
- Explore neural network approaches (Autoencoder for anomaly detection)
- Add SHAP explainability for individual transaction decisions

---

## About

No description, website, or topics provided.
