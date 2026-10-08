"""
Astro Embedding Pipeline
========================

Builds embeddings from sky coordinates and cosmological distances.
"""

from __future__ import annotations
import numpy as np
from sklearn.decomposition import PCA
import umap


class AstroEmbeddingPipeline:
    def __init__(self, projector, cosmology, n_components=3):
        self.projector = projector
        self.cosmology = cosmology
        self.n_components = n_components

    def build_features(self, df):
        coords = self.projector.project(df["RAdeg"], df["DEdeg"])
        z = df["redshift"].values
        dist = np.array([self.cosmology.comoving_distance(zi) for zi in z])
        return np.hstack([coords, dist[:, None]])

    def embed(self, df):
        X = self.build_features(df)
        X_pca = PCA(n_components=self.n_components).fit_transform(X)
        X_umap = umap.UMAP(n_components=2).fit_transform(X_pca)
        return X_umap
