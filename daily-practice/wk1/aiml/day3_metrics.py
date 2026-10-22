# import libraries
import numpy as np
import json
import os
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def compute_metrics(y_true, y_pred):
    """
    Calculate Precision, Recall, F1 from scratch.
    Assume positive class is 1 and negative class is 0.
    """
    tp = np.sum((y_true==1) & (y_pred==1))  # True Positives
    fp = np.sum((y_true==0) & (y_pred==1))  # False Positives
    fn = np.sum((y_true==1) & (y_pred==0))  # False Negatives   
    tn = np.sum((y_true==0) & (y_pred==0))  # True Negatives

    # Handle division by zero
    precision = tp/(tp + fp) if (tp +fp) > 0 else 0.0
    recall = tp/(tp +fn) if (tp+ fn) > 0 else 0.0
    f1 = 2 * (precision * recall)/(precision+recall) if (precision + recall) > 0 else 0.0
    accuracy = (tp+tn)/(tp+tn+fp+fn) if (tp+tn+fp+fn) > 0 else 0.0
    return precision, recall, f1, accuracy

# Test on generated imbalanced data (simulating 10% positive class)
X,y = make_classification(n_samples=1000, n_classes=2, weights=[0.9,0.1], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train,y_train)
y_pred = model.predict(X_test)

# Scratch
p,r,f1,acc = compute_metrics(y_test, y_pred)

# Sklearn
p_sk = precision_score(y_test, y_pred)
r_sk = recall_score(y_test, y_pred)
f1_sk = f1_score(y_test, y_pred)
acc_sk = accuracy_score(y_test, y_pred)

print("Results on imbalanced data (90/10 split):")
print(f"Scratch: Precision={p:.4f}, Recall={r:.4f}, F1={f1:.4f}, Accuracy={acc:.4f}")
print(f"Sklearn: Precision={p_sk:.4f}, Recall={r_sk:.4f}, F1={f1_sk:.4f}, Accuracy={acc_sk:.4f}")

# Save to metrics
os.makedirs("metrics", exist_ok=True)
metrics = {
    "day3_metrics": {
        "accuracy": round(acc, 4),
        "precision": round(p, 4),
        "recall": round(r, 4),
        "f1": round(f1, 4)
    }
}

try:
    with open("metrics/wk1.json", "r") as f:
        existing = json.load(f)
    existing.update(metrics)
except FileNotFoundError:
    existing = metrics

with open("metrics/wk1.json", "w") as f:
    json.dump(existing, f, indent=4)
    f.write("\n")

print("\nSaved to metrics/wk1.json")

# WHY-NOTE (Oct 21):
# Why can 95% accuracy be useless on imbalanced data?
# If the dataset has 95% negative class and 5% positive class, a model 
# that simply predicts "negative" for everything achieves 95% accuracy. 
# However, the Recall for the positive class is 0, meaning it detects 
# none of the actual positive cases. In fields like fraud or medicine, 
# missing a positive is far more costly than a false alarm.