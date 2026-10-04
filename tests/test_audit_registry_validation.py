"""Scientific-control regression checks: valid archival bytes cannot promote bad inputs."""
import json
import pytest
from scripts.validate_audit_registries import (
    assert_controlled_input, assert_namespace_identity,
    assert_no_support_promotion, controlled_input_eligible,
    assert_crosswalk_snapshot,
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
