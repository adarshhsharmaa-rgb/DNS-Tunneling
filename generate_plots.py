import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics import RocCurveDisplay, ConfusionMatrixDisplay, roc_auc_score
from features import FEATURE_NAMES
import os

os.makedirs("results", exist_ok=True)

# Load dataset and model
df = pd.read_csv("data/dataset.csv")
X, y = df[FEATURE_NAMES], df["label"]
rf = joblib.load("models/rf_model.joblib")

# 1. Feature Importance Plot
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), [FEATURE_NAMES[i] for i in indices], rotation=45, ha='right')
plt.xlim([-1, X.shape[1]])
plt.tight_layout()
plt.savefig("results/feature_importances.png")
plt.close()

# 2. Confusion Matrix Plot
disp = ConfusionMatrixDisplay.from_estimator(rf, X, y, display_labels=["Normal", "Tunnel"], cmap=plt.cm.Blues)
disp.figure_.savefig("results/confusion_matrix.png")
plt.close()

# 3. ROC Curve Plot
disp = RocCurveDisplay.from_estimator(rf, X, y)
disp.figure_.savefig("results/roc_curve.png")
plt.close()

print("Plots saved to results/ directory.")
