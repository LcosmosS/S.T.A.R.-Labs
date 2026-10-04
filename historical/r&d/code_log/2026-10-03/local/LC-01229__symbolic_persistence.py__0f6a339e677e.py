"""
symbolic_persistence.py
-----------------------
Implements symbolic persistence analysis for the S.T.A.R. Model.

This module:
- computes persistent homology barcodes
- extracts Betti numbers
- computes symbolic persistence signatures
- integrates with entropy shells and cohomology classes
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
from ripser import ripser
from src.data.load_sky_surveys import load_sky_surveys

def test_sky_surveys_load():
    df1, df2 = load_sky_surveys(downsample=100, validate_schema=True)
    assert len(df1) > 0
    assert len(df2) > 0



class SymbolicPersistence:
    """
    Computes persistent homology for symbolic manifolds.
    """

    def __init__(self, maxdim=2):
        self.maxdim = maxdim

    def distance_matrix(self, X):
        """
        Compute pairwise distances.
        """
        return squareform(pdist(X))

    def barcodes(self, X):
        """
        Compute persistent homology barcodes using Ripser.
        """
        D = self.distance_matrix(X)
        result = ripser(D, maxdim=self.maxdim, distance_matrix=True)
        return result["dgms"]

    def betti_numbers(self, barcodes):
        """
        Extract Betti numbers from barcodes.
        """
        return [len(bc) for bc in barcodes]

    def persistence_signature(self, barcodes):
        """
        Compute a symbolic persistence signature:
        signature = Σ (death - birth)
        """
        signature = []
        for bc in barcodes:
            total = np.sum([d - b for b, d in bc])
            signature.append(total)
        return np.array(signature)
