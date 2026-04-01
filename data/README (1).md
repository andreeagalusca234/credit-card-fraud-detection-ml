# Dataset

The dataset used in this project is the **Credit Card Fraud Detection** dataset from Kaggle, published by the ULB Machine Learning Group.

## Download Instructions

The CSV file (`creditcard.csv`) is not included in this repository due to its size (~150MB).

### Option 1 — Kaggle Web

1. Go to https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
2. Click **Download**
3. Place `creditcard.csv` in this `data/` folder

### Option 2 — Kaggle API

```bash
pip install kaggle
kaggle datasets download -d mlg-ulb/creditcardfraud -p data/
unzip data/creditcardfraud.zip -d data/
```

## Dataset Description

| Property | Value |
|---|---|
| Rows | 284,807 |
| Columns | 31 |
| Target column | `Class` (0 = Legitimate, 1 = Fraud) |
| Fraud rate | 0.172% |
| Missing values | None |
| Source | Real transactions from European cardholders, September 2013 |

Features `V1`–`V28` are the result of PCA transformation applied to protect user confidentiality. `Time` and `Amount` are the only untransformed features.
