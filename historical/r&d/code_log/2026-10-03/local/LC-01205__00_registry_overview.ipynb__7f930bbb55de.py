from pathlib import Path
import csv
root=Path.cwd()
while root != root.parent and not (root/'registry').is_dir(): root=root.parent
assert (root/'registry').is_dir(), 'repository root with registry/ not found'
registry=root/'registry'
def rows(name):
    with (registry/name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
claims=rows('claim_evidence_v0.2.csv'); experiments=rows('experiment_registry_v0.2.csv'); crosswalk=rows('claim_experiment_crosswalk_v0.2.csv')
claim_ids={r['Claim_ID'] for r in claims}; exp_ids={r['Experiment_ID'] for r in experiments}
assert len(exp_ids)==len(experiments)
assert all(r['Claim_ID'] in claim_ids and r['Experiment_ID'] in exp_ids for r in crosswalk)
print(f'claims={len(claim_ids)}, experiments={len(exp_ids)}, crosswalk={len(crosswalk)}')
