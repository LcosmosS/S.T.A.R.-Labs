"""Fail-closed A01/A03 shared DATA-ARITHMETIC activation compatibility.

This is a *runtime metadata compatibility certificate*, not a scientific
re-preregistration. The A03 spec, null, protocol, source and computational
code remain frozen. No status is changed by this module.
"""
from __future__ import annotations

from src.control.registry import record_sha256

DATASET_INACTIVE_SHA256 = "2fe4ab7f5763f39c6cde8392c3f7d8ff1a565e4664ce6e192640b99f3fe146d7"
DATASET_A01_ACTIVE_SHA256 = "1b81e05ab90ce822c7dcbda88bdb206f191f6523fac03fea5ecdf55724de44c2"
A01_ACTIVE_EXPERIMENT_SHA256 = "97dac41c4d8a866d0abbcdf5515829328e92ea1fb3cf7b4d03e1d9b9c0b9c868"
A03_FROZEN_EXPERIMENT_SHA256 = "3b0bb9c77c80a19a0fca69103f084bb9368593d56d1e3bf037775fb74732794e"
DATASET_ID = "DATA-ARITHMETIC"
A01_ID = "EXP-MAP-A01"
A03_ID = "EXP-MAP-A03"


def a03_shared_dataset_transition_is_compatible(spec: dict, resolved, snapshot) -> bool:
    """Permit exactly the A01 execution-only dataset bit, *never* A03 execution.

    Require the original A03 spec binding, an exact new row SHA, and reverse
    the sole permitted bit to reproduce the originally frozen row SHA. Also
    require the exact A01 activated experiment record; every other A03 binding
    continues to be enforced by the caller. Does not waive input/file hashes.
    """
    if spec.get("experiment_id") != A03_ID:
        return False
    bindings = spec.get("registry_bindings", {})
    if (bindings.get("dataset") != DATASET_INACTIVE_SHA256
            or bindings.get("experiment") != A03_FROZEN_EXPERIMENT_SHA256):
        return False
    if (resolved.experiment.get("Experiment_ID") != A03_ID
            or resolved.experiment.get("Controlled_Execution_Eligible") != "false"
            or resolved.experiment.get("Status") != "preregistered"):
        return False
    if record_sha256(resolved.experiment) != A03_FROZEN_EXPERIMENT_SHA256:
        return False
    dataset = resolved.dataset
    if (dataset.get("Dataset_ID") != DATASET_ID
            or dataset.get("Controlled_Execution_Eligible") != "true"
            or any(dataset.get(k) != "false" for k in
                   ("Controlled_Support_Eligible", "Physical_Support_Eligible"))):
        return False
    if record_sha256(dataset) != DATASET_A01_ACTIVE_SHA256:
        return False
    original = dict(dataset)
    original["Controlled_Execution_Eligible"] = "false"
    if record_sha256(original) != DATASET_INACTIVE_SHA256:
        return False
    a01 = snapshot.experiments.get(A01_ID)
    if (not a01 or a01.get("Controlled_Execution_Eligible") != "true"
            or a01.get("Status") != "preregistered"
            or any(a01.get(k) != "false" for k in
                   ("Controlled_Support_Eligible", "Physical_Support_Eligible"))):
        return False
    if record_sha256(a01) != A01_ACTIVE_EXPERIMENT_SHA256:
        return False
    return True


def a03_bindings_compatible(spec: dict, resolved, snapshot) -> bool:
    """Accept the frozen exact bindings or the single certified dataset bit.

    Every non-dataset binding MUST match its originally frozen hash. The
    compatibility state is only for the still-inactive A03 experiment.
    """
    declared = spec.get("registry_bindings", {})
    current = resolved.record_hashes
    if declared == current:
        return True
    if (set(declared) != set(current)
            or any(declared[k] != current[k] for k in current if k != "dataset")):
        return False
    return a03_shared_dataset_transition_is_compatible(spec, resolved, snapshot)
