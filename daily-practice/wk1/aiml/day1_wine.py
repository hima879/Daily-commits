# import libraries
import json
import os
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score,adjusted_rand_score
from sklearn.preprocessing import StandardScaler

# Load data
wine = load_wine()
X,y = wine.data, wine.target

# split data
X_train,X_test,y_train,y_test =  train_test_split(
    X,y,test_size=0.2,random_state=42,stratify=y)

# scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Supervised: k-NN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)   # <-- Make sure this says X_test_scaled!
knn_acc = accuracy_score(y_test, y_pred)

# Unsupervised: K-Means
# Note: we scale the FULL X for clustering (no train/test split needed for k-means here,
# since we're evaluating if it can recover the structure of the whole dataset)
scaler_full = StandardScaler()
X_scaled_full = scaler_full.fit_transform(X) 
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
cluster_labels = kmeans.fit_predict(X_scaled_full)
kmeans_ari = adjusted_rand_score(y, cluster_labels)

metrics = {
    "dataset": "wine",
    "knn_accuracy": round(knn_acc, 4),
    "kmeans_ari": round(kmeans_ari, 4)
}
os.makedirs("metrics", exist_ok=True) 
# Run this from aiml-prep root: python daily-practice/wk1/day1_wine.py

print(json.dumps(metrics, indent=4))

with open("metrics/wk1.json", "w") as f:
    json.dump(metrics, f, indent=4)

# WHY-NOTE (Oct 19):
# Q: Why can k-means partially recover wine variety structure without seeing a label, 
#    and where does it fail?
# A: K-means groups by Euclidean distance in 13-dimensional feature space. 
#    It partially recovers the varieties because different wines have distinct 
#    chemical profiles (e.g., alcohol content, flavanoids, proline). 
#    HOWEVER, it fails to achieve a perfect ARI (adj_rand ~0.4) because:
#    1. Two of the wine classes (Class 1 & 2) overlap heavily in chemical space.
#    2. K-means assumes spherical, equal-sized clusters, but wine chemical 
#       distributions are elongated and unequal (Class 0 has 59 samples, Class 1 has 71).
#    3. It ignores the actual labels entirely—it's finding "mathematical" groups, 
#       not "biological" ones.