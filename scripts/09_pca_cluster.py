#!/usr/bin/env python3

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score

PARAMS = ["z_a", "W", "theta_l", "theta_s", "A", "S", "h_f", "d_f"]
VAR_KEPT = 0.90
K_RANGE = range(2, 11)
SEED = 0

df = pd.read_csv("morphometry.csv").dropna(subset=PARAMS)

Z = StandardScaler().fit_transform(df[PARAMS].to_numpy())
pca = PCA(n_components=VAR_KEPT, svd_solver="full", random_state=SEED)
Y = pca.fit_transform(Z)

silhouette = {}
for k in K_RANGE:
    labels = KMeans(n_clusters=k, n_init=50, random_state=SEED).fit_predict(Y)
    silhouette[k] = silhouette_score(Y, labels)
K = max(silhouette, key=silhouette.get)

kmeans = KMeans(n_clusters=K, n_init=50, random_state=SEED).fit(Y)
ward = AgglomerativeClustering(n_clusters=K, linkage="ward").fit(Y)
ari = adjusted_rand_score(kmeans.labels_, ward.labels_)

df["class"] = kmeans.labels_
df.to_csv("morphometry_classified.csv", index=False)

print("components retained :", pca.n_components_,
      "(%.1f %% of variance)" % (100 * pca.explained_variance_ratio_.sum()))
print("classes retained    :", K, "silhouette %.3f" % silhouette[K])
print("k-means vs Ward ARI : %.3f" % ari)
