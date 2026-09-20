"""Tests for acsc.tda_pipeline module"""
import numpy as np
import pytest
from acsc import compute_persistence


def test_compute_persistence_basic():
    """Test basic persistence computation"""
    coords = np.random.randn(20, 3)
    result = compute_persistence(coords, maxdim=2)
    
    assert isinstance(result, dict)
    assert 'dgms' in result
    assert len(result['dgms']) >= 1


def test_compute_persistence_empty():
    """Test persistence with empty input"""
    coords = np.empty((0, 3))
    result = compute_persistence(coords, maxdim=2)
    
    assert isinstance(result, dict)
    assert 'dgms' in result


def test_compute_persistence_single_point():
    """Test persistence with single point"""
    coords = np.array([[0.0, 0.0, 0.0]])
    result = compute_persistence(coords, maxdim=1)
    
    assert isinstance(result, dict)
    assert 'dgms' in result
