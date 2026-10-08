"""Fail-closed tests for prospective preregistration reviews."""
import copy
import pytest

from tools.validate_preregistration_transition_candidates import (
    PreregistrationReviewError, validate, validate_a01_lifecycle, load_csv, load_json, ROOT, CONFIG, LEDGER
)

def _fixture():
    return load_json(ROOT, LEDGER), load_json(ROOT, CONFIG)

def test_prospective_reviews_preserve_canonical_gates():
    assert validate() == 3

def test_reject_candidate_support_promotion():
    ledger, cfg = _fixture()
    ledger["candidates"][1]["physical_support_eligible"] = True
    with pytest.raises(PreregistrationReviewError, match="eligibility promotion"):
        validate(ledger=ledger, config=cfg)

def test_reject_unreviewed_preregistration_status_in_incomplete_design():
    ledger, cfg = _fixture()
    ledger["candidates"][2]["design_status"] = "prospective_protocol_locked_pending_canonical_transition"
    with pytest.raises(PreregistrationReviewError, match="incorrectly marked locked"):
        validate(ledger=ledger, config=cfg)

def test_reject_null_seed_or_scientific_endpoint_change():
    ledger, cfg = _fixture()
    cfg["null"]["seed"] += 1
    with pytest.raises(PreregistrationReviewError, match="Unfrozen null"):
        validate(ledger=ledger, config=cfg)
    ledger, cfg = _fixture()
    cfg["inference"]["alpha"] = 0.05
    with pytest.raises(PreregistrationReviewError, match="Endpoint or threshold changed"):
        validate(ledger=ledger, config=cfg)

def test_reject_rank_leakage_and_j_zero_selection_after_rank_review():
    ledger, cfg = _fixture()
    cfg["mapping"]["rank_used_in_embedding"] = True
    with pytest.raises(PreregistrationReviewError, match="Rank contamination"):
        validate(ledger=ledger, config=cfg)
    ledger, cfg = _fixture()
    cfg["mapping"]["j_zero_policy"] = "exclude_after_rank_review"
    with pytest.raises(PreregistrationReviewError, match="Undefined j=0"):
        validate(ledger=ledger, config=cfg)

def test_reject_changed_source_digest():
    ledger, cfg = _fixture()
    cfg["input"]["source_sha256"] = "0"*64
    with pytest.raises(PreregistrationReviewError, match="Arithmetic source bytes"):
        validate(ledger=ledger, config=cfg)

def _a01_rows():
    exp = load_csv(ROOT, "registry/experiment_registry_v0.2.csv", "Experiment_ID")
    datasets = load_csv(ROOT, "registry/dataset_registry_v0.1.csv", "Dataset_ID")
    return dict(exp["EXP-MAP-A01"]), dict(datasets["DATA-ARITHMETIC"])

def test_a01_inactive_or_exact_separate_activation_is_accepted_not_support():
    experiment, dataset = _a01_rows()
    validate_a01_lifecycle(experiment, dataset)
    experiment["Controlled_Execution_Eligible"] = "true"
    dataset["Controlled_Execution_Eligible"] = "true"
    validate_a01_lifecycle(experiment, dataset)
    experiment["Current_Audit_Assessment"] += " illicit amendment"
    with pytest.raises(PreregistrationReviewError, match="exact reviewed bindings"):
        validate_a01_lifecycle(experiment, dataset)

def test_a01_partial_activation_and_support_promotion_are_rejected():
    experiment, dataset = _a01_rows()
    experiment["Controlled_Execution_Eligible"] = "true"
    with pytest.raises(PreregistrationReviewError, match="partial activation"):
        validate_a01_lifecycle(experiment, dataset)
    experiment["Controlled_Execution_Eligible"] = "false"
    dataset["Physical_Support_Eligible"] = "true"
    with pytest.raises(PreregistrationReviewError, match="physical support"):
        validate_a01_lifecycle(experiment, dataset)
