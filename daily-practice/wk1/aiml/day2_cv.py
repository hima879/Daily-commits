# import libraries
import os
import json
import time
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer

# Load data
X,y = load_breast_cancer(return_X_y=True)

# Hold-out split (80-20) for comparison
X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter = 1000)
model.fit(X_train_scaled,y_train)
holdout_acc = accuracy_score(y_test,model.predict(X_test_scaled))

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_accuracies = []
start_time = time.time()

for fold,(train_idx, test_idx) in enumerate(skf.split(X,y)):
    # Fold 1 is done 
    # Grab the actual rows for this fold
    X_train_fold,X_test_fold = X[train_idx],X[test_idx]
    y_train_fold,y_test_fold = y[train_idx],y[test_idx]

    # Critical: fit scaler only on train fold
    fold_scaler = StandardScaler()
    X_train_fold_scaled = fold_scaler.fit_transform(X_train_fold)
    X_test_fold_scaled = fold_scaler.transform(X_test_fold)

    # Train 
    fold_model = LogisticRegression(max_iter=1000)
    fold_model.fit(X_train_fold_scaled,y_train_fold)

    # Evaluate
    fold_preps = fold_model.predict(X_test_fold_scaled)
    fold_acc = accuracy_score(y_test_fold,fold_preps)
    fold_accuracies.append(fold_acc)

    print(f"Fold {fold+1} accuracy: {fold_acc:.4f}")

cv_mean = np.mean(fold_accuracies)
cv_std = np.std(fold_accuracies)
end_time = time.time()-start_time

print(f"Hold-out accuracy: {holdout_acc:.4f}")
print(f"Cross-validation accuracy: {cv_mean:.4f} (+/- {cv_std * 2:.4f})")
print(f"Time taken: {end_time:.4f} seconds")

os.makedirs("metrics",exist_ok=True)
metrics = {
    "day2_cv": {
        "holdout_accuracy": holdout_acc,
        "cv_mean_accuracy": cv_mean,
        "cv_std_accuracy": cv_std,
        "time_taken_seconds": end_time
    }
}

# read existing JSON, update it, write it back
try:
    with open("metrics/wk1.json","r") as f:
        existing_metrics = json.load(f)        
    existing_metrics.update(metrics)
except FileNotFoundError:
    existing_metrics = metrics

with open("metrics/wk1.json","w") as f:
    json.dump(existing_metrics,f)

print("\nSaved to metrics/wk1.json")

# Why Note
"""Why does a single hold-out split give a noisier estimate than 5-fold CV?
A single hold-out evaluates the model on only one random subset (e.g., 20% of the data).
Depending on which samples land in that split, the score can be artificially high or low.
5-fold CV evaluates the model 5 times, each time on a different 20% slice. Averaging these 5 scores reduces the variance,
giving a more stable and reliable estimate of true generalization performance."""