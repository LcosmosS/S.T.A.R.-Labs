"""Validate qualified audit records and prevent quarantine-to-evidence promotion."""
from pathlib import Path
import argparse, csv, hashlib, json

PDF_NS='STAR-PDF-v0.2'
REPO_NS='REPO-CSV-v0.2'
FIND_NS='STAR-AUDIT-2026-10-03'

def read_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader=csv.DictReader(stream); rows=list(reader)
        assert reader.fieldnames and len(reader.fieldnames)==len(set(reader.fieldnames)), f'duplicate/empty CSV header: {path}'
        assert all(None not in row and all(v is not None for v in row.values()) for row in rows), f'malformed CSV record: {path}'
    return rows

def ids(value):
    return json.loads(value) if value.lstrip().startswith('[') else [x for x in value.split(';') if x]

def truth(value): return str(value).strip().lower()=='true'

def assert_namespace_identity(row, namespace, original_key, qualified_key):
    assert row[qualified_key]==f'{namespace}:{row[original_key]}', f'namespace identity mismatch: {row[original_key]}'

def controlled_input_eligible(dataset, provenance):
    """A valid archival hash never overrides quarantine or unknown source status."""
    if dataset.get('Status','').lower()=='quarantined' or provenance.get('Provenance_Status','').lower()=='quarantined': return False
    if provenance.get('Provenance_Status')!='verified': return False
    if provenance.get('Evidence_Status') in {'negative_null','historical','unknown'}: return False
    return truth(dataset.get('Controlled_Execution_Eligible','false'))

def assert_controlled_input(experiment, dataset, provenance):
    if truth(experiment.get('Controlled_Execution_Eligible','false')):
        assert controlled_input_eligible(dataset,provenance), f'quarantined or unverified input cannot become controlled eligible: {experiment["Experiment_ID"]}'

def assert_no_support_promotion(rows, label):
    for row in rows:
        for key in ['controlled_support_eligible','physical_support_eligible','Controlled_Support_Eligible','Physical_Support_Eligible']:
            if key in row: assert not truth(row[key]), f'audit/quarantine support promotion: {label} {key}'

def snapshot_matches(value, cell):
    if isinstance(value,(list,dict)): return json.loads(cell)==value
    if isinstance(value,bool): return cell.strip().lower()==str(value).lower()
    return cell==('' if value is None else str(value))

def assert_crosswalk_snapshot(row, source):
    """Protect the complete source assessment as well as its displayed columns."""
    assert json.loads(row['Audit_Record_JSON'])==source, f'crosswalk source snapshot changed: {source["claim_id"]}'
    mapped={
        'Original_Claim_ID':source['claim_id'],
        'Title':source['title'],
        'Baseline_Crosswalk_Text':source['baseline_crosswalk_text'],
        'Current_Assessment':source['current_assessment'],
        'Evidence_State':source['evidence_state'],
        'Link_Semantics':source['link_semantics'],
        'Evidence_Provenance':source['provenance'],
        'Unresolved_References':source['unresolved_references'],
        'Next_Actions':source['next_actions'],
    }
    for field,value in mapped.items():
        assert snapshot_matches(value,row[field]), f'crosswalk mapped assessment changed: {source["claim_id"]} {field}'
    assert ids(row['Finding_IDs'])==source['finding_ids'], f'crosswalk finding IDs changed: {source["claim_id"]}'
    assert ids(row['Qualified_Finding_IDs'])==[f'{FIND_NS}:{fid}' for fid in source['finding_ids']]
    assert ids(row['Qualified_Original_Experiment_References'])==[f'{PDF_NS}:{eid}' for eid in source['original_experiment_references']]
    assert ids(row['Qualified_Registered_Experiment_Links'])==[f'{PDF_NS}:{eid}' for eid in source['registered_experiment_links']]

def validate(repo, overlay=None):
    repo=Path(repo)
    def path(relative):
        candidate=Path(overlay)/relative if overlay else None
        return candidate if candidate and candidate.is_file() else repo/relative
    def rows(name): return read_rows(path('registry/'+name))
    def load(relative): return json.loads(path(relative).read_text(encoding='utf-8-sig'))
    metadata=load('registry/audit_namespace_source_bindings_v0.3.json')
    package=metadata['audit_package']
    for name, expected in metadata['package_sources'].items():
        assert hashlib.sha256(path(package+'/'+name).read_bytes()).hexdigest()==expected, f'audit intake changed: {name}'
    updates=load(package+'/claim_updates.json'); experiments=load(package+'/experiment_updates.json'); crosswalk=load(package+'/crosswalk_updates.json')
    baseline_claims={r['claim_id']:r for r in load(package+'/baseline_claims.json')}
    baseline_experiments={r['experiment_id']:r for r in load(package+'/baseline_experiments.json')}
    audit_claims=rows('claim_evidence_audit_v0.3.csv'); audit_exps=rows('experiment_audit_v0.3.csv'); audit_cross=rows('claim_experiment_crosswalk_audit_v0.3.csv')
    assert len(audit_claims)==len(updates)==51 and len(audit_exps)==len(experiments)==25 and len(audit_cross)==len(crosswalk['records'])==51
    claim_map={r['claim_id']:r for r in audit_claims}; exp_map={r['experiment_id']:r for r in audit_exps}
    assert len(claim_map)==51 and len(exp_map)==25
    for source in updates:
        row=claim_map[source['claim_id']]
        assert all(snapshot_matches(value,row[key]) for key,value in source.items()), f'imported claim field changed: {source["claim_id"]}'
        assert row['Baseline_Record_Text']==baseline_claims[source['claim_id']]['baseline_record_text']
        assert_namespace_identity(row,PDF_NS,'claim_id','qualified_id')
    for source in experiments:
        row=exp_map[source['experiment_id']]
        assert all(snapshot_matches(value,row[key]) for key,value in source.items()), f'imported experiment field changed: {source["experiment_id"]}'
        assert row['Baseline_Record_Text']==baseline_experiments[source['experiment_id']]['baseline_record_text']
        assert_namespace_identity(row,PDF_NS,'experiment_id','qualified_id')
        assert not truth(row['canonical_protocol_completed']) and not truth(row['evidence_promotion'])
    qualified_claims={f'{PDF_NS}:{cid}' for cid in claim_map}; qualified_exps={f'{PDF_NS}:{eid}' for eid in exp_map}
    findings=load(package+'/local_findings.json')['findings']+load(package+'/drive_findings.json')['findings']
    finding_ids={f'{FIND_NS}:{row["finding_id"]}' for row in findings}
    unresolved=rows('audit_unresolved_references_v0.3.csv')
    unresolved_ids={r['Qualified_Original_Reference'] for r in unresolved}
    for row in unresolved:
        assert row['Qualified_Original_Reference'] not in qualified_exps
        assert not truth(row['Canonical_Definition_Present']) and not truth(row['Execution_Eligible'])
        assert row['Candidate_Qualified_Experiment_ID'] in qualified_exps|{''}
        assert row['Alias_Resolution']!='CONFIRMED'
    assert {r['Qualified_Claim_ID'] for r in audit_cross}==qualified_claims
    source_cross={r['claim_id']:r for r in crosswalk['records']}
    for row in audit_cross:
        source=source_cross[row['Original_Claim_ID']]
        assert_crosswalk_snapshot(row,source)
        assert snapshot_matches(source['baseline_crosswalk_text'],row['Baseline_Crosswalk_Text']), f"crosswalk baseline text changed: {row['Original_Claim_ID']}"
        assert ids(row['Qualified_Registered_Experiment_Links'])==[f'{PDF_NS}:{eid}' for eid in source['registered_experiment_links']]
        assert set(ids(row['Qualified_Registered_Experiment_Links'])).issubset(qualified_exps)
        assert set(ids(row['Qualified_Original_Experiment_References'])).issubset(qualified_exps|unresolved_ids)
        assert set(ids(row['Qualified_Finding_IDs'])).issubset(finding_ids)
    assert_no_support_promotion(audit_claims+audit_exps+audit_cross,'historical audit')
    assert metadata['confirmed_cross_namespace_aliases']==[]
    relationships=rows('namespace_relationships_v0.3.csv')
    for row in relationships:
        assert row['Source_Qualified_ID']==f'{row["Source_Namespace"]}:{row["Source_ID"]}'
        assert row['Relationship'] in {'related_scope_only_not_alias','unresolved_no_alias'}
        assert not truth(row['Evidence_Eligible'])
        if row['Target_ID']:
            assert row['Target_Qualified_ID']==f'{PDF_NS}:{row["Target_ID"]}'
            assert row['Target_Qualified_ID'] in qualified_claims|qualified_exps
    for name, snapshot in metadata['original_control_snapshots'].items():
        current=rows(name)
        assert len(current)==len(snapshot['rows'])
        for original, row in zip(snapshot['rows'],current):
            # Historical audit snapshots remain immutable. The operational
            # experiment registry may make one explicit reviewed lifecycle
            # transition for EXP-MAP-A01: Status planned -> preregistered.
            # IDs, claims, dataset/parameter/null bindings, mode, priority and
            # Historical_RandD must remain identical to the audit snapshot.
            allowed_transition = (
                name == 'experiment_registry_v0.2.csv'
                and original.get('Experiment_ID') == 'EXP-MAP-A01'
                and original.get('Status') == 'planned'
                and row.get('Status') == 'preregistered'
            )
            protected = [
                key for key in snapshot['fields']
                if not (allowed_transition and key == 'Status')
            ]
            assert all(row[key]==original[key] for key in protected), f'original controlled ID/definition changed: {name}'
            if name == 'experiment_registry_v0.2.csv' and original.get('Experiment_ID') == 'EXP-MAP-A01':
                assert allowed_transition, 'EXP-MAP-A01 audit transition must be explicit planned -> preregistered'
        assert_no_support_promotion(current,name)
    datasets=rows('dataset_registry_v0.1.csv'); provenance=rows('data_provenance_registry_v0.1.csv'); assets=rows('audit_quarantine_dataset_status_v0.3.csv')
    ds_map={r['Dataset_ID']:r for r in datasets}; prov_map={r['Dataset_ID']:r for r in provenance}
    assert len(ds_map)==len(datasets)==len(prov_map)==len(provenance)==45
    assert set(ds_map)==set(prov_map)
    assert len(provenance[0])==21
    assert_no_support_promotion(datasets+assets,'dataset or quarantined asset')
    assert len(assets)==37 and len({r['qualified_dataset_id'] for r in assets})==37
    for asset in assets:
        did=asset['qualified_dataset_id']; dataset=ds_map[did]; prov=prov_map[did]
        assert dataset['Qualified_Dataset_ID']==did and dataset['Registry_Namespace']==asset['qualified_namespace']
        assert dataset['Status']=='quarantined' and prov['Provenance_Status']=='quarantined'
        assert prov['Evidence_Status'] in {'negative_null','historical'}
        assert dataset['Source_or_Definition']==asset['quarantine_path']
        assert asset['quarantine_path'] in prov['Transformation_History']
        assert asset['quarantine_sha256'] in prov['Integrity_Check']
        quarantine=path(asset['quarantine_path'])
        assert quarantine.is_file() and hashlib.sha256(quarantine.read_bytes()).hexdigest()==asset['quarantine_sha256']
        assert not controlled_input_eligible(dataset,prov)
    original_ids=set(ds_map)-{r['qualified_dataset_id'] for r in assets}
    assert len(original_ids)==8

    # The October 3 audit rows remain immutable historical snapshots, but a
    # later reviewed remediation may advance an operational DATA-* record.
    # EXP-MAP-A01-prereg-v1 is the first such remediation: it pins exact ecdata
    # source bytes while deliberately leaving execution/support eligibility off.
    prereg_manifest=load('preregistrations/EXP-MAP-A01/dataset_manifest.json')
    remediated_id='DATA-ARITHMETIC'
    assert remediated_id in original_ids
    remediated_dataset=ds_map[remediated_id]
    remediated_provenance=prov_map[remediated_id]
    assert remediated_dataset['Status']=='locked'
    assert remediated_dataset['Provenance_Status']=='verified'
    assert remediated_dataset['Achieved_Evidence_Status']=='controlled'
    assert not truth(remediated_dataset['Controlled_Execution_Eligible'])
    assert not truth(remediated_dataset['Controlled_Support_Eligible'])
    assert not truth(remediated_dataset['Physical_Support_Eligible'])
    assert remediated_provenance['Provenance_Status']=='verified'
    assert remediated_provenance['Evidence_Status']=='controlled'
    assert prereg_manifest['artifact']['sha256'] in remediated_provenance['Integrity_Check']
    assert prereg_manifest['source']['git_commit'] in remediated_provenance['Version_or_Release']
    assert not controlled_input_eligible(remediated_dataset,remediated_provenance)

    for did in original_ids-{remediated_id}:
        assert ds_map[did]['Status']=='planned' and prov_map[did]['Provenance_Status']=='unknown' and prov_map[did]['Evidence_Status']=='unknown'
        assert not controlled_input_eligible(ds_map[did],prov_map[did])
    controlled=rows('experiment_registry_v0.2.csv')
    for experiment in controlled:
        assert_namespace_identity(experiment,REPO_NS,'Experiment_ID','Qualified_Experiment_ID')
        assert_controlled_input(experiment,ds_map[experiment['Dataset_ID']],prov_map[experiment['Dataset_ID']])
    bindings=rows('dataset_audit_bindings_v0.3.csv')
    asset_ids={r['binding_id'] for r in assets}
    assert {r['Dataset_ID'] for r in bindings}==original_ids
    for row in bindings:
        assert row['Relationship']=='diagnostic_context_only_not_dataset_identity'
        assert row['Accepted_Quarantine_Input_Bindings']=='' and not truth(row['Canonical_Source_Identity_Verified'])
        assert set(ids(row['Related_Quarantine_Bindings'])).issubset(asset_ids)
    print('Validated 51 claims, 25 definitions, 51 crosswalk records, 7 audit-frozen planned scopes, 1 locked preregistered arithmetic scope and 37 quarantined artifacts; no support promotion.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--overlay',type=Path)
    args=parser.parse_args(); validate(args.repo,args.overlay)
