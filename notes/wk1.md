# Week 1 Notes: Supervised vs Unsupervised, CV, Metrics
**Dates:** Sun 18 Oct 2026 → Thu 22 Oct 2026
**Status:** Mostly Revision (Concepts already known, focused on implementation)

---

## 🎯 Weekly Progress Checklist
- [x] **Oct 18:** Orientation, venv setup, Git repo created & pushed.
- [x] **Oct 19:** AIML Build (Wine dataset: k-NN & k-Means). Java Heap Theory.
- [x] **Oct 20:** AIML Build (Manual 5-Fold CV on Breast Cancer).
- [x] **Oct 21:** AIML Build (Precision/Recall/F1 from scratch). 
- [x] **Math:** Eigenvalues derivation + NumPy verification.
- [ ] **DSA LeetCode:** Heaps (#215, #703, #1046, etc.) → *Deferred to Sunday*.

---

## 🧠 60-Second Interview Answers (Draft)

**1. What is supervised vs unsupervised learning, and when would you use each?**
- **Supervised:** The data has labels (targets). You use it for prediction tasks (classification, regression). Example: Predicting if a tumor is malignant based on labeled historical data.
- **Unsupervised:** The data has no labels. You use it to find hidden structures or patterns. Example: K-Means clustering to group customers into segments based on purchasing behavior without knowing the segments beforehand.

**2. Why does cross-validation matter, and when does it fail?**
- **Why it matters:** A single train/test split can give a noisy, unreliable score depending on which samples land in the test set. K-Fold CV evaluates the model K times on different splits, providing a more robust mean and standard deviation of performance.
- **When it fails:** It fails when there is a temporal component (like time-series data). If you randomly shuffle a time series, you leak future data into the past. For time series, you must use "Time-Series Split" (walk-forward validation).

**3. Precision vs recall: when would you optimize each?**
- **Precision** (True Positives / (True Positives + False Positives)): Optimize when the cost of a False Positive is high. Example: Spam detection (you don't want to mark a boss's email as spam).
- **Recall** (True Positives / (True Positives + False Negatives)): Optimize when the cost of a False Negative is high. Example: Medical diagnosis for a deadly disease (you don't want to miss a sick patient, even if it means some false alarms).

---

## 🧮 Math: Eigenvalues & PCA
The principal components in PCA are the eigenvectors of the covariance matrix, and the corresponding eigenvalues represent the amount of variance captured by each component. By sorting eigenvalues in descending order, we can select the top principal components that retain the most information in the data.

## 📊 Metrics Summary (saved in metrics/wk1.json)
- **Holdout Accuracy:** 98.25% (Breast Cancer)
- **5-Fold CV Mean:** 97.37% ± 3.33%
- **Imbalanced Data (Scratch vs Sklearn):** Precision=0.6154, Recall=0.3810, F1=0.4706, Acc=0.9100 (Both matched perfectly!)
