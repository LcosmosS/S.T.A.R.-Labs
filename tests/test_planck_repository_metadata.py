"""Integration checks for the tracked Planck chain metadata."""

from pathlib import Path

import numpy as np

from src.likelihoods.data.planck_compressed import load_planck_chain


ROOT = Path(__file__).resolve().parents[1]
PLANCK = ROOT / "data" / "planck"


def test_tracked_base_chain_matches_named_metada():
    frame = load_planck_chain(
        PLANCK / "base_plikHM_TTTEEE_lowl_lowE_1.txt"
    )

    assert frame.shape == (6125, 95)
    assert frame.columns[2] == "omegabh2"
    assert frame.columns[29] == "H0"
    assert frame.columns[-1] == "chi2_CMB"
    assert frame.attrs["schema_source"] == "direct-paramnames"
    assert frame.attrs["properties"] == {
        "plik_foregrounds": True,
        "burn_removed": True,
    }


def test_tracked_post_bao_chain_uses_validated_extended_schema():
    frame = load_planck_chain(
        PLANCK / "base_plikHM_TTTEEE_lowl_lowE_post_BAO_1.txt"
    )

    assert frame.shape == (1380, 99)
    assert frame.attrs["schema_source"] == (
        "base-paramnames-plus-post-BAO-ranges"
    )
    assert list(frame.columns[-6:]) == [
        "chi2_6DF",
        "chi2_MGS",
        "chi2_DR12BAO",
        "chi2_prior",
        "chi2_BAO",
        "chi2_CMB",
    ]
    assert np.allclose(
        frame["chi2_BAO"],
        frame["chi2_6DF"] + frame["chi2_MGS"] + frame["chi2_DR12BAO"],
        rtol=1e-6,
        atol=1e-5,
    )
    assert frame.attrs["properties"] == {
        "burn_removed": True,
        "plik_foregrounds": True,
    }
