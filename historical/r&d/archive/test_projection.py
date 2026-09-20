"""Tests for acsc.projection module"""
import numpy as np
import pytest
from acsc import project


def test_project_basic():
    """Test basic projection with simple input"""
    records = [
        {"delta": 1728, "conductor": 11, "rank": 0},
        {"delta": -432, "conductor": 37, "rank": 1},
    ]
    coords = project(records)
    assert coords.shape == (2, 3)
    assert np.all(np.isfinite(coords))


def test_project_empty():
    """Test projection with empty input"""
    coords = project([])
    assert coords.shape == (0, 3)


def test_project_none():
    """Test projection with None"""
    coords = project(None)
    assert coords.shape == (0, 3)


def test_project_single():
    """Test projection with single record"""
    record = [{"delta": 1728, "conductor": 11, "rank": 2}]
    coords = project(record)
    assert coords.shape == (1, 3)
    assert np.all(np.isfinite(coords))
