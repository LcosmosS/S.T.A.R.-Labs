"""Tests for acsc.quantile module"""
import numpy as np
import pytest
from acsc import QuantileAligner


def test_quantile_fit_basic():
    """Test basic quantile fitting"""
    ref_coords = np.random.randn(100, 3)
    qa = QuantileAligner()
    qa.fit(ref_coords)
    assert qa._fitted
    assert len(qa._axis_maps) == 3


def test_quantile_transform_basic():
    """Test quantile transformation"""
    ref_coords = np.random.randn(50, 3)
    src_coords = np.random.randn(30, 3)
    
    qa = QuantileAligner()
    qa.fit(ref_coords)
    result = qa.transform(src_coords)
    
    assert result.shape == (30, 3)
    assert np.all(np.isfinite(result))


def test_quantile_fit_transform():
    """Test fit_transform method"""
    ref_coords = np.random.randn(100, 3)
    src_coords = np.random.randn(50, 3)
    
    qa = QuantileAligner()
    result = qa.fit_transform(ref_coords, src_coords)
    
    assert result.shape == (50, 3)
    assert np.all(np.isfinite(result))


def test_quantile_unfitted_transform():
    """Test that transform fails on unfitted aligner"""
    qa = QuantileAligner()
    src_coords = np.random.randn(10, 3)
    
    with pytest.raises(RuntimeError):
        qa.transform(src_coords)
