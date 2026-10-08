"""
Tests for the sky survey dataset loader.

This test ensures:
- the loader runs without error
- the datasets exist in data/raw/
- schema validation passes
- downsampling works (for CI speed)
"""

from src.data.load_sky_surveys import load_sky_surveys


def test_load_sky_surveys_basic():
    """Loader should return two non-empty DataFrames."""
    df1, df2 = load_sky_surveys(downsample=50)
    assert len(df1) > 0
    assert len(df2) > 0


def test_load_sky_surveys_schema():
    """Schema validation should pass for required columns."""
    df1, df2 = load_sky_surveys(downsample=50, validate_schema=True)

    # Required columns for both datasets
    for df in (df1, df2):
        assert "RAdeg" in df.columns
        assert "DEdeg" in df.columns


def test_load_sky_surveys_downsample():
    """Downsampling should reduce dataset size deterministically."""
    df1_full, df2_full = load_sky_surveys()
    df1_small, df2_small = load_sky_surveys(downsample=10)

    assert len(df1_small) == 10
    assert len(df2_small) == 10
    assert len(df1_full) >= len(df1_small)
    assert len(df2_full) >= len(df2_small)
