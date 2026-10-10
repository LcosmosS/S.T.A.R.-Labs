"""Scientific-control regression checks: valid archival bytes cannot promote bad inputs."""
import json
import pytest
from scripts.validate_audit_registries import (
    assert_controlled_input, assert_namespace_identity,
    assert_no_support_promotion, controlled_input_eligible,
    assert_crosswalk_snapshot, assert_original_control_snapshot,
    assert_dataset_lifecycle, assert_operational_dataset_coverage,
    has_recorded_sha256,
)

def test_quarantined_valid_hash_is_ineligible_even_when_planned_protocol_references_it():
    dataset={'Dataset_ID':'AUDIT-QUARANTINE-v0.3:QDATA-001','Status':'quarantined','Controlled_Execution_Eligible':'true'}
    provenance={'Dataset_ID':dataset['Dataset_ID'],'Provenance_Status':'quarantined','Evidence_Status':'negative_null','Integrity_Check':'SHA256='+'a'*64}
    protocol={'Experiment_ID':'REPO-CSV-v0.2:EXP-CTRL-A01','Status':'planned','Mode':'controlled','Dataset_ID':dataset['Dataset_ID'],'Controlled_Execution_Eligible':'true'}
    assert not controlled_input_eligible(dataset,provenance)
    with pytest.raises(AssertionError,match='quarantined or unverified input'):
        assert_controlled_input(protocol,dataset,provenance)

def test_unknown_source_does_not_become_eligible_from_declared_controlled_use():
    dataset={'Status':'planned','Controlled_Execution_Eligible':'true'}
    provenance={'Provenance_Status':'unknown','Evidence_Status':'controlled','Integrity_Check':'SHA256='+'a'*64}
    assert not controlled_input_eligible(dataset,provenance)

def test_equal_literal_experiment_string_cannot_cross_namespace_silently():
    row={'Experiment_ID':'EXP-CTRL-A01','Qualified_Experiment_ID':'STAR-PDF-v0.2:EXP-CTRL-A01'}
    with pytest.raises(AssertionError,match='namespace identity mismatch'):
        assert_namespace_identity(row,'REPO-CSV-v0.2','Experiment_ID','Qualified_Experiment_ID')

@pytest.mark.parametrize('field',['controlled_support_eligible','physical_support_eligible'])
def test_quarantine_promotion_is_rejected(field):
    with pytest.raises(AssertionError,match='support promotion'):
        assert_no_support_promotion([{field:'True'}],'valid-hash quarantined artifact')

@pytest.mark.parametrize('field',['Current_Assessment','Evidence_State'])
def test_crosswalk_assessment_mutation_is_rejected_while_links_remain_valid(field):
    source={
        'claim_id':'CORE-001','title':'Arithmetic/Cosmic Hypothesis',
        'baseline_crosswalk_text':None,'current_assessment':'PROPOSED / NOT VERIFIED',
        'evidence_state':'N','provenance':'EXPLORATORY / UNVERIFIED',
        'link_semantics':'Relevance only; not execution evidence',
        'unresolved_references':[],'next_actions':['Reconstruct before promotion'],
        'finding_ids':['E-LCL-014'],'original_experiment_references':['EXP-CTRL-A01'],
        'registered_experiment_links':['EXP-CTRL-A03'],
    }
    row={
        'Audit_Record_JSON':json.dumps(source),'Original_Claim_ID':source['claim_id'],
        'Title':source['title'],'Baseline_Crosswalk_Text':'',
        'Current_Assessment':source['current_assessment'],'Evidence_State':source['evidence_state'],
        'Link_Semantics':source['link_semantics'],'Evidence_Provenance':source['provenance'],
        'Unresolved_References':json.dumps(source['unresolved_references']),
        'Next_Actions':json.dumps(source['next_actions']),
        'Finding_IDs':'E-LCL-014','Qualified_Finding_IDs':'STAR-AUDIT-2026-10-03:E-LCL-014',
        'Qualified_Original_Experiment_References':'STAR-PDF-v0.2:EXP-CTRL-A01',
        'Qualified_Registered_Experiment_Links':'STAR-PDF-v0.2:EXP-CTRL-A03',
    }
    assert_crosswalk_snapshot(row,source)
    row[field]='SUPPORTED' if field=='Current_Assessment' else 'I'
    with pytest.raises(AssertionError,match='crosswalk mapped assessment changed'):
        assert_crosswalk_snapshot(row,source)


def _claim_row(claim_id="CLAIM-BASE"):
    return {
        "Claim_ID": claim_id,
        "Claim_Type": "theory",
        "Statement": "baseline statement",
        "Status": "hypothesis",
        "Evidence_Requirement": "baseline evidence",
        "Registry_Namespace": "REPO-CSV-v0.2",
        "Qualified_Claim_ID": f"REPO-CSV-v0.2:{claim_id}",
        "Related_Audit_Claim_IDs": "",
        "Relation_Status": "related_scope_only_not_alias",
        "Current_Audit_Assessment": "baseline",
        "Audit_Finding_IDs": "",
        "Controlled_Support_Eligible": "false",
        "Physical_Support_Eligible": "false",
    }


def test_audit_baseline_allows_explicit_post_audit_nonalias_claim():
    baseline = _claim_row()
    snapshot = {
        "fields": [
            "Claim_ID",
            "Claim_Type",
            "Statement",
            "Status",
            "Evidence_Requirement",
        ],
        "rows": [baseline],
    }
    added = _claim_row("CLAIM-NEW")
    added["Relation_Status"] = "new_control_claim_no_historical_alias"
    added["Current_Audit_Assessment"] = "post-audit claim; unsupported"

    assert_original_control_snapshot(
        "claim_evidence_v0.2.csv",
        snapshot,
        [baseline, added],
    )


def test_audit_baseline_rejects_new_claim_that_inherits_historical_audit_identity():
    baseline = _claim_row()
    snapshot = {
        "fields": [
            "Claim_ID",
            "Claim_Type",
            "Statement",
            "Status",
            "Evidence_Requirement",
        ],
        "rows": [baseline],
    }
    added = _claim_row("CLAIM-NEW")
    added["Relation_Status"] = "new_control_claim_no_historical_alias"
    added["Related_Audit_Claim_IDs"] = "STAR-PDF-v0.2:CORE-001"

    with pytest.raises(AssertionError, match="cannot inherit audit claim IDs"):
        assert_original_control_snapshot(
            "claim_evidence_v0.2.csv",
            snapshot,
            [baseline, added],
        )


def test_audit_baseline_rejects_mutation_of_original_claim_when_new_claim_exists():
    baseline = _claim_row()
    snapshot = {
        "fields": [
            "Claim_ID",
            "Claim_Type",
            "Statement",
            "Status",
            "Evidence_Requirement",
        ],
        "rows": [baseline],
    }
    mutated = dict(baseline)
    mutated["Statement"] = "changed historical statement"
    added = _claim_row("CLAIM-NEW")
    added["Relation_Status"] = "new_control_claim_no_historical_alias"

    with pytest.raises(AssertionError, match="original controlled ID/definition changed"):
        assert_original_control_snapshot(
            "claim_evidence_v0.2.csv",
            snapshot,
            [mutated, added],
        )


def _candidate_rows(dataset_id="DATA-NEW", *, source="verified",
                    evidence="unknown", execution="false", integrity=None):
    """Build matching dataset/provenance fixtures with configurable gate states."""
    dataset = {
        "Dataset_ID": dataset_id, "Status": "planned",
        "Provenance_Status": source, "Achieved_Evidence_Status": evidence,
        "Controlled_Execution_Eligible": execution,
        "Controlled_Support_Eligible": "false",
        "Physical_Support_Eligible": "false",
    }
    provenance = {
        "Dataset_ID": dataset_id, "Provenance_Status": source,
        "Evidence_Status": evidence,
        "Integrity_Check": integrity if integrity is not None else (
            "SHA256=" + "a" * 64 if source == "verified" else ""
        ),
    }
    return dataset, provenance


def test_source_sha256_receipt_from_vizier_is_recognized():
    """Accept VizieR source_SHA256 receipts as recorded integrity evidence."""
    dataset, provenance = _candidate_rows(
        integrity="source_SHA256=" + "6" * 64 + "; size_bytes=10981088"
    )
    assert has_recorded_sha256(provenance)
    assert_dataset_lifecycle(dataset, provenance)


def test_nonquarantined_dataset_addition_has_no_historical_row_ceiling():
    """Allow canonical inventory growth when each dataset has provenance."""
    old, old_prov = _candidate_rows("DATA-OLD", source="unknown")
    new, new_prov = _candidate_rows("DATA-NEW")
    d, p, nonquarantined = assert_operational_dataset_coverage(
        [old, new], [old_prov, new_prov], []
    )
    assert set(d) == set(p) == nonquarantined == {"DATA-OLD", "DATA-NEW"}


def test_new_publisher_verified_dataset_is_not_automatically_executable():
    """Keep a publisher-verified source ineligible without execution approval."""
    dataset, provenance = _candidate_rows()
    assert_dataset_lifecycle(dataset, provenance)
    assert not controlled_input_eligible(dataset, provenance)


@pytest.mark.parametrize("evidence", ["unknown", "historical", "negative_null"])
def test_verified_source_without_controlled_evidence_rejects_execution(evidence):
    """Reject execution when verified bytes lack controlled or derived evidence."""
    dataset, provenance = _candidate_rows(
        evidence=evidence, execution="true"
    )
    with pytest.raises(AssertionError, match="controlled execution requires"):
        assert_dataset_lifecycle(dataset, provenance)


@pytest.mark.parametrize("integrity", ["", "SHA256=" + "0" * 64, "not-a-digest"])
def test_verified_source_requires_nonplaceholder_sha256(integrity):
    """Reject verified provenance with missing, zero-filled, or malformed hashes."""
    dataset, provenance = _candidate_rows(integrity=integrity)
    assert not has_recorded_sha256(provenance)
    with pytest.raises(AssertionError, match="requires recorded SHA-256"):
        assert_dataset_lifecycle(dataset, provenance)


@pytest.mark.parametrize("evidence", ["controlled", "derived"])
def test_execution_flag_is_eligible_only_with_verified_evidence_and_sha(evidence):
    """Accept explicit execution eligibility with verified scientific evidence."""
    dataset, provenance = _candidate_rows(evidence=evidence, execution="true")
    assert controlled_input_eligible(dataset, provenance)
    assert_dataset_lifecycle(dataset, provenance)


@pytest.mark.parametrize("flag", ["Controlled_Support_Eligible", "Physical_Support_Eligible"])
def test_unverified_dataset_cannot_promote_support(flag):
    """Reject either support flag when the dataset's source is unverified."""
    dataset, provenance = _candidate_rows(source="unknown")
    dataset[flag] = "true"
    with pytest.raises(AssertionError, match="requires executable verified"):
        assert_dataset_lifecycle(dataset, provenance)


def test_reject_unmatched_or_duplicate_provenance_and_quarantine():
    """Reject incomplete provenance, duplicate IDs, and quarantine mismatches."""
    dataset, provenance = _candidate_rows()
    with pytest.raises(AssertionError, match="missing/orphan provenance"):
        assert_operational_dataset_coverage([dataset], [], [])
    with pytest.raises(AssertionError, match="duplicate provenance"):
        assert_operational_dataset_coverage([dataset], [provenance, provenance], [])
    with pytest.raises(AssertionError, match="quarantine registry/asset mismatch"):
        assert_operational_dataset_coverage(
            [dataset], [provenance],
            [{"qualified_dataset_id": "AUDIT-QUARANTINE-v0.3:QDATA-001"}],
        )


def test_historical_quarantine_status_never_grants_execution():
    """Keep quarantined data ineligible even when its execution flag is true."""
    dataset, provenance = _candidate_rows(
        "AUDIT-QUARANTINE-v0.3:QDATA-001",
        source="quarantined", evidence="negative_null", execution="true",
    )
    dataset["Status"] = "quarantined"
    assert not controlled_input_eligible(dataset, provenance)
