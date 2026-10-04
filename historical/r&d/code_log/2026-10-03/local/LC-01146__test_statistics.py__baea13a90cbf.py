"""Tests for acsc.statistics module"""
import numpy as np
import pytest
from acsc import w2_between_diagrams, empirical_p_value


def test_w2_basic():
    """Test W2 distance computation"""
    dgmA = np.array([[0.1, 0.5], [0.2, 0.8]])
    dgmB = np.array([[0.15, 0.45], [0.25, 0.75]])
    
    dist = w2_between_diagrams(dgmA, dgmB)
    assert isinstance(dist, float)
    assert dist >= 0


def test_w2_empty():
    """Test W2 with empty diagrams"""
    dgmA = np.empty((0, 2))
    dgmB = np.empty((0, 2))
    
    dist = w2_between_diagrams(dgmA, dgmB)
    assert dist == 0.0


def test_empirical_p_value_basic():
    """Test empirical p-value computation"""
    observed = 0.5
    null_samples = np.random.randn(100)
    
    pval = empirical_p_value(observed, null_samples)
    assert 0 < pval <= 1


def test_empirical_p_value_all_below():
    """Test p-value when all nulls are below observed"""
    observed = 10.0
    null_samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    pval = empirical_p_value(observed, null_samples)
    assert pval == 1.0 / 6.0  # (1 + 5) / (1 + 5)


def test_empirical_p_value_all_above():
    """Test p-value when all nulls are above observed"""
    observed = 0.0
    null_samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    pval = empirical_p_value(observed, null_samples)
    assert pval == 1.0 / 6.0  # (1 + 0) / (1 + 5)
