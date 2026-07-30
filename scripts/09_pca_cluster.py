#!/usr/bin/env python3
# Standardisation, principal component analysis and k-means clustering in scikit-learn, with the number of classes selected by the mean silhouette coefficient.
"""Standardisation, principal component analysis and classification."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score

PARAMS = ["z_a", "W", "theta_l", "theta_s", "A", "S", "h_f", "d_f"]
VAR_KEPT = 0.90            # cumulative variance retained, fixed in advance
K_RANGE = range(2, 11)     # candidate numbers of classes
SEED = 0                   # fixed, so the partition is reproducible

df = pd.read_csv("morphometry.csv").dropna(subset=PARAMS)

Z = StandardScaler().fit_transform(df[PARAMS].to_numpy())        # Eq. 4
pca = PCA(n_components=VAR_KEPT, svd_solver="full", random_state=SEED)
Y = pca.fit_transform(Z)                                         # Eq. 5

# the number of classes is selected, not imposed
silhouette = {}
for k in K_RANGE:                                                # Eqs. 6, 7
    labels = KMeans(n_clusters=k, n_init=50, random_state=SEED).fit_predict(Y)
    silhouette[k] = silhouette_score(Y, labels)
K = max(silhouette, key=silhouette.get)

kmeans = KMeans(n_clusters=K, n_init=50, random_state=SEED).fit(Y)
ward = AgglomerativeClustering(n_clusters=K, linkage="ward").fit(Y)
ari = adjusted_rand_score(kmeans.labels_, ward.labels_)          # cross-check

df["class"] = kmeans.labels_
df.to_csv("morphometry_classified.csv", index=False)

print("components retained :", pca.n_components_,
      "(%.1f %% of variance)" % (100 * pca.explained_variance_ratio_.sum()))
print("classes retained    :", K, "silhouette %.3f" % silhouette[K])
print("k-means vs Ward ARI : %.3f" % ari)
