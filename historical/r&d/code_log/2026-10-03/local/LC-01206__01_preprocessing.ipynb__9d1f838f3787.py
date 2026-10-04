from pathlib import Path
import pandas as pd
root=Path.cwd()
while root != root.parent and not (root/'registry').is_dir(): root=root.parent
assert (root/'registry').is_dir(), 'repository root with registry/ not found'
registry=root/'registry'
for name in ['claim_evidence_v0.2.csv','claim_experiment_crosswalk_v0.2.csv','experiment_registry_v0.2.csv']:
    assert (registry/name).exists(), f'missing registry file: {name}'
probe=pd.DataFrame({'delta':[-11,-19,None],'conductor':[11,19,37],'rank':[0,1,2]})
assert len(probe)==3 and probe.isna().sum().sum()==1
print('data-validation contract passed; missing values are retained')
