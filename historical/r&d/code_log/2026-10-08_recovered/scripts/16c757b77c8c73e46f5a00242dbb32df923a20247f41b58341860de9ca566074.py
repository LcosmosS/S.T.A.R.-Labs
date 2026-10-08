"""
sr_pipeline.py
--------------
High-level orchestration pipeline for symbolic regression in the
S.T.A.R. Model.

This module:
- prepares data
- runs constrained GP
- evaluates candidate laws
- performs null-scramble tests
- outputs best symbolic expression
"""

import numpy as np
from .constrained_gp import ConstrainedGP
from .law_discovery_manifold import LawDiscoveryManifold
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0

class SRPipeline:
    """
    Orchestrates symbolic regression under S.T.A.R. constraints.
    """

    def __init__(self, max_depth=6, population=50, generations=20):
        self.gp = ConstrainedGP(max_depth=max_depth,
                                population=population)
        self.manifold = LawDiscoveryManifold(max_depth=max_depth)
        self.generations = generations

    def prepare_data(self, X):
        """
        Normalize and prepare data for symbolic regression.
        """
        X = np.array(X, dtype=float)
        X = X / (np.max(np.abs(X), axis=0) + 1e-12)
        return X

    def scramble(self, X):
        """
        Null-scramble the dataset.
        """
        X_scrambled = X.copy()
        np.random.shuffle(X_scrambled)
        return X_scrambled

    def run(self, X, isogeny_pairs):
        """
        Run full symbolic regression pipeline.
        """
        X = self.prepare_data(X)
        scrambled = self.scramble(X)

        best_tree = self.gp.evolve(
            data=X,
            isogeny_pairs=isogeny_pairs,
            scrambled=scrambled,
            generations=self.generations
        )

        return best_tree
