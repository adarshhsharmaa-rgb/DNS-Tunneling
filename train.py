import pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from features import FEATURE_NAMES

df = pd.read_csv("data/dataset.csv")
X, y = df[FEATURE_NAMES], df["label"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

models = {
    "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
    "DecisionTree": DecisionTreeClassifier(max_depth=8, random_state=42),
    "LogReg": LogisticRegression(max_iter=2000),
}

for name, m in models.items():
    m.fit(Xtr, ytr)
    pred = m.predict(Xte)
    print("\n==", name, "==")
    print(classification_report(yte, pred, digits=4))
    print(confusion_matrix(yte, pred))
    print("AUC:", roc_auc_score(yte, m.predict_proba(Xte)[:, 1]))

rf = models["RandomForest"]
print("CV F1:", cross_val_score(rf, X, y, cv=5, scoring="f1").mean())
print(sorted(zip(rf.feature_importances_, FEATURE_NAMES), reverse=True))
joblib.dump(rf, "models/rf_model.joblib")
