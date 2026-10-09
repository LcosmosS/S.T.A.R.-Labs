"""Validate qualified audit records and prevent quarantine-to-evidence promotion."""
from pathlib import Path
import argparse, csv, hashlib, json, re

PDF_NS='STAR-PDF-v0.2'
REPO_NS='REPO-CSV-v0.2'
FIND_NS='STAR-AUDIT-2026-10-03'
A03_LOCKED_ASSESSMENT="EXP-MAP-A03-prereg-v1 is scientifically preregistered as the repository-qualified BSD-independent MCJ arithmetic null test; source bytes, the deterministic 37,936-row analysis cohort, exact j mapping, k=10 endpoint, conductor-decile null, seed=4103, B=999, alpha=0.005, and output contract are locked. Controlled execution and all support promotion remain disabled pending a separate activation-only PR and successful activation preflight."

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

SHA256_RECEIPT = re.compile(r'\bsha[-_ ]?256\s*[:=]\s*([0-9a-f]{64})\b', re.IGNORECASE)


def has_recorded_sha256(provenance):
    """Require a syntactically valid, non-placeholder hash in source lineage.

    This check is necessary, not proof that publisher bytes were independently
    hydrated. Dataset-specific source CI verifies the actual object contents.
    """
    checks = provenance.get('Integrity_Check', '')
    return any(
        match.group(1).lower() != '0' * 64
        for match in SHA256_RECEIPT.finditer(checks)
    )


def controlled_input_eligible(dataset, provenance):
    """Execution needs verified source identity, scientific evidence, and SHA.

    Source-only publisher verification with Evidence_Status=unknown is NOT
    sufficient. An execution flag is a separate authorization, not inferred
    from these prerequisites.
    """
    if dataset.get('Status', '').lower() == 'quarantined':
        return False
    if provenance.get('Provenance_Status', '').lower() != 'verified':
        return False
    if provenance.get('Evidence_Status', '').lower() not in {'controlled', 'derived'}:
        return False
    if not has_recorded_sha256(provenance):
        return False
    return truth(dataset.get('Controlled_Execution_Eligible', 'false'))


def assert_dataset_lifecycle(dataset, provenance):
    """Check a canonical operational row without naming any preferred dataset."""
    did = dataset['Dataset_ID']
    assert provenance['Dataset_ID'] == did, f'missing/mismatched provenance: {did}'
    assert dataset['Provenance_Status'] == provenance['Provenance_Status'], (
        f'dataset/provenance source-status drift: {did}'
    )
    assert dataset['Achieved_Evidence_Status'] == provenance['Evidence_Status'], (
        f'dataset/provenance evidence-status drift: {did}'
    )
    if provenance['Provenance_Status'] == 'verified':
        assert has_recorded_sha256(provenance), (
            f'verified dataset requires recorded SHA-256 integrity evidence: {did}'
        )
    if truth(dataset['Controlled_Execution_Eligible']):
        assert controlled_input_eligible(dataset, provenance), (
            f'controlled execution requires verified source, controlled/derived '
            f'evidence and real SHA-256: {did}'
        )
    for flag in ('Controlled_Support_Eligible', 'Physical_Support_Eligible'):
        if truth(dataset[flag]):
            assert controlled_input_eligible(dataset, provenance), (
                f'{flag} requires executable verified dataset evidence: {did}'
            )
    # An input passing this check is not by itself an authorized experiment,
    # approved display release or scientifically reviewed support claim.


def assert_operational_dataset_coverage(datasets, provenance, assets):
    """Separate immutable audit quarantine from extensible canonical inventory.

    Every operational dataset must have exactly one provenance record. The
    frozen quarantine inventory is checked against exactly its registered
    assets, rather than assuming the historical canonical row count is fixed.
    """
    ds_map = {r['Dataset_ID']: r for r in datasets}
    prov_map = {r['Dataset_ID']: r for r in provenance}
    assert len(ds_map) == len(datasets), 'duplicate Dataset_ID'
    assert len(prov_map) == len(provenance), 'duplicate provenance Dataset_ID'
    assert set(ds_map) == set(prov_map), 'missing/orphan provenance Dataset_ID'
    quarantined = {r['qualified_dataset_id'] for r in assets}
    assert len(quarantined) == len(assets), 'duplicate frozen quarantine asset'
    operational_quarantine = {
        did for did, row in ds_map.items()
        if row['Status'] == 'quarantined'
    }
    assert operational_quarantine == quarantined, (
        'quarantine registry/asset mismatch or unauthorized new quarantine'
    )
    non_quarantined = {
        did for did, row in ds_map.items()
        if row['Status'] != 'quarantined'
    }
    for did in non_quarantined:
        assert_dataset_lifecycle(ds_map[did], prov_map[did])
    return ds_map, prov_map, non_quarantined


def assert_controlled_input(experiment, dataset, provenance):
    if truth(experiment.get('Controlled_Execution_Eligible', 'false')):
        assert controlled_input_eligible(dataset, provenance), (
            f'quarantined or unverified input cannot become controlled eligible: {experiment["Experiment_ID"]}'
        )


def assert_no_support_promotion(rows, label):
    for row in rows:
        for key in ['controlled_support_eligible','physical_support_eligible','Controlled_Support_Eligible','Physical_Support_Eligible']:
            if key in row: assert not truth(row[key]), f'audit/quarantine support promotion: {label} {key}'

def assert_original_control_snapshot(name, snapshot, current):
    """Preserve audited baseline records while permitting explicit post-audit claims.

    The October 3 snapshot is immutable evidence about records that existed at
    audit time. It is not a permanent ban on adding new canonical claims after
    that audit. New experiment/crosswalk records remain disallowed here because
    they require their own reviewed lifecycle integration.
    """
    key_fields = {
        'claim_evidence_v0.2.csv': ('Claim_ID',),
        'experiment_registry_v0.2.csv': ('Experiment_ID',),
        'claim_experiment_crosswalk_v0.2.csv': ('Claim_ID', 'Experiment_ID'),
    }
    key_fields_for_name = key_fields[name]

    def key(row):
        return tuple(row[field] for field in key_fields_for_name)

    current_map = {key(row): row for row in current}
    assert len(current_map) == len(current), f'duplicate operational control key: {name}'

    original_keys = {key(row) for row in snapshot['rows']}
    assert original_keys.issubset(current_map), f'audited baseline record removed: {name}'

    for original in snapshot['rows']:
        row = current_map[key(original)]

        # Historical audit snapshots remain immutable. Operational lifecycle
        # transitions are narrow, experiment-specific exceptions.
        allowed_a01 = (
            name == 'experiment_registry_v0.2.csv'
            and original.get('Experiment_ID') == 'EXP-MAP-A01'
            and original.get('Status') == 'planned'
            and row.get('Status') == 'preregistered'
        )
        allowed_a03 = (
            name == 'experiment_registry_v0.2.csv'
            and original.get('Experiment_ID') == 'EXP-MAP-A03'
            and original.get('Status') == 'planned'
            and row.get('Status') == 'preregistered'
            and row.get('Current_Audit_Assessment') == A03_LOCKED_ASSESSMENT
            and row.get('Controlled_Execution_Eligible') == 'false'
            and row.get('Controlled_Support_Eligible') == 'false'
            and row.get('Physical_Support_Eligible') == 'false'
        )
        mutable = {'Status'} if allowed_a01 else (
            {'Status', 'Current_Audit_Assessment'} if allowed_a03 else set()
        )
        protected = [field for field in snapshot['fields'] if field not in mutable]
        assert all(row[field] == original[field] for field in protected), (
            f'original controlled ID/definition changed: {name}'
        )
        if name == 'experiment_registry_v0.2.csv' and original.get('Experiment_ID') == 'EXP-MAP-A01':
            assert allowed_a01, 'EXP-MAP-A01 audit transition must be explicit planned -> preregistered'
        if name == 'experiment_registry_v0.2.csv' and original.get('Experiment_ID') == 'EXP-MAP-A03':
            assert allowed_a03 or row == original, (
                'EXP-MAP-A03 may change only planned -> preregistered plus the exact locked assessment'
            )

    extra_keys = set(current_map) - original_keys
    if name != 'claim_evidence_v0.2.csv':
        assert not extra_keys, f'post-audit operational rows require separate reviewed integration: {name}'

    for extra_key in extra_keys:
        row = current_map[extra_key]
        assert row['Registry_Namespace'] == REPO_NS, f'post-audit claim namespace mismatch: {row["Claim_ID"]}'
        assert row['Qualified_Claim_ID'] == f'{REPO_NS}:{row["Claim_ID"]}', f'post-audit claim qualified ID mismatch: {row["Claim_ID"]}'
        assert row['Relation_Status'] == 'new_control_claim_no_historical_alias', f'post-audit claim must be explicit non-alias: {row["Claim_ID"]}'
        assert row['Related_Audit_Claim_IDs'] == '', f'post-audit claim cannot inherit audit claim IDs: {row["Claim_ID"]}'
        assert row['Audit_Finding_IDs'] == '', f'post-audit claim cannot inherit audit findings: {row["Claim_ID"]}'
        assert row['Current_Audit_Assessment'].strip(), f'post-audit claim lacks current assessment: {row["Claim_ID"]}'
        assert not truth(row['Controlled_Support_Eligible']), f'post-audit claim support promotion: {row["Claim_ID"]}'
        assert not truth(row['Physical_Support_Eligible']), f'post-audit claim physical promotion: {row["Claim_ID"]}'

    assert_no_support_promotion(current, name)

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
        assert_original_control_snapshot(name, snapshot, rows(name))
    datasets=rows('dataset_registry_v0.1.csv'); provenance=rows('data_provenance_registry_v0.1.csv'); assets=rows('audit_quarantine_dataset_status_v0.3.csv')
    ds_map, prov_map, non_quarantined = assert_operational_dataset_coverage(
        datasets, provenance, assets
    )
    assert provenance and len(provenance[0])==21
    assert_no_support_promotion(assets,'frozen quarantined asset')
    # The quarantined assets are an immutable October 3 audit snapshot;
    # their cardinality is historical, unlike the evolving canonical registry.
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
    # Deliberately no fixed number of non-quarantined canonical datasets.

    # The October 3 audit rows remain immutable historical snapshots, but a
    # later reviewed remediation may advance an operational DATA-* record.
    # EXP-MAP-A01-prereg-v1 is the first such remediation: it pins exact ecdata
    # source bytes while deliberately leaving execution/support eligibility off.
    prereg_manifest=load('preregistrations/EXP-MAP-A01/dataset_manifest.json')
    remediated_id='DATA-ARITHMETIC'
    assert remediated_id in non_quarantined
    remediated_dataset=ds_map[remediated_id]
    remediated_provenance=prov_map[remediated_id]
    assert remediated_dataset['Status']=='locked'
    assert remediated_dataset['Provenance_Status']=='verified'
    assert remediated_dataset['Achieved_Evidence_Status']=='controlled'
    # Future execution activation requires a separate preregistered experiment
    # and approval transaction, not another hard-coded validator exception.
    assert remediated_provenance['Provenance_Status']=='verified'
    assert remediated_provenance['Evidence_Status']=='controlled'
    assert prereg_manifest['artifact']['sha256'] in remediated_provenance['Integrity_Check']
    assert prereg_manifest['source']['git_commit'] in remediated_provenance['Version_or_Release']
    assert_dataset_lifecycle(remediated_dataset,remediated_provenance)

    # A later provenance-only review independently downloaded the SDSS DR17
    # H I-MaNGA DR3 publisher binary and reproduced the preserved LFS object's
    # SHA-256.  This advances source identity only: the dataset remains planned,
    # its achieved evidence remains unknown, and every eligibility gate remains
    # false until a prospective matching protocol is admitted separately.
    hi_id='DATA-MANGA-HI-ALL'
    hi_receipt=load('data/provenance/publisher_byte_verification_2026-10-08.json')
    hi_dataset=ds_map[hi_id]
    hi_provenance=prov_map[hi_id]
    hi_record=next(r for r in hi_receipt['datasets'] if r['dataset_id']==hi_id)
    assert hi_dataset['Status']=='planned'
    assert hi_dataset['Provenance_Status']=='verified'
    assert hi_dataset['Achieved_Evidence_Status']=='unknown'
    assert not truth(hi_dataset['Controlled_Execution_Eligible'])
    assert not truth(hi_dataset['Controlled_Support_Eligible'])
    assert not truth(hi_dataset['Physical_Support_Eligible'])
    assert hi_provenance['Provenance_Status']=='verified'
    assert hi_provenance['Evidence_Status']=='unknown'
    assert hi_record['publisher']['sha256'] in hi_provenance['Integrity_Check']
    assert hi_record['comparison']['publisher_equals_repository_lfs'] is True
    assert not controlled_input_eligible(hi_dataset,hi_provenance)

    # All other canonical datasets, whether newly registered or promoted
    # from placeholders, use the same evidence/eligibility predicate. Source
    # hashes alone never grant controlled execution or web admission.
    for did in non_quarantined:
        assert_dataset_lifecycle(ds_map[did], prov_map[did])

    controlled=rows('experiment_registry_v0.2.csv')
    for experiment in controlled:
        assert_namespace_identity(experiment,REPO_NS,'Experiment_ID','Qualified_Experiment_ID')
        assert_controlled_input(experiment,ds_map[experiment['Dataset_ID']],prov_map[experiment['Dataset_ID']])
    bindings=rows('dataset_audit_bindings_v0.3.csv')
    asset_ids={r['binding_id'] for r in assets}
    audited_ids={r['Dataset_ID'] for r in bindings}
    assert len(audited_ids)==len(bindings), 'duplicate frozen audit dataset binding'
    # Historical bindings are an immutable subset, not a complete enumeration
    # of future, independently reviewed canonical registrations.
    assert audited_ids.issubset(non_quarantined)
    for row in bindings:
        assert row['Relationship']=='diagnostic_context_only_not_dataset_identity'
        assert row['Accepted_Quarantine_Input_Bindings']=='' and not truth(row['Canonical_Source_Identity_Verified'])
        assert set(ids(row['Related_Quarantine_Bindings'])).issubset(asset_ids)
    print('Validated 51 claims, 25 definitions, 51 crosswalk records, audit-frozen planned scopes, 2 locked preregistered arithmetic scopes and 37 quarantined artifacts; no support promotion.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--overlay',type=Path)
    args=parser.parse_args(); validate(args.repo,args.overlay)
