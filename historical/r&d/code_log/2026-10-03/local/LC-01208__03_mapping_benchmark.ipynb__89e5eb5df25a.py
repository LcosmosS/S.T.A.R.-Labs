from pathlib import Path
import sys
root=Path.cwd()
while root != root.parent and not (root/'registry').is_dir(): root=root.parent
assert (root/'registry').is_dir(), 'repository root with registry/ not found'
sys.path.insert(0,str(root))
sys.path.insert(0,str(root/'src'))
import numpy as np
from acsc.projection import project
from acsc.alt_mappings import map_ptd, map_mcj
records=[{'delta':-11,'conductor':11,'rank':0,'regulator':1.0,'real_period':2.0,'torsion_order':1,'j_invariant':1728},{'delta':-19,'conductor':19,'rank':1,'regulator':1.5,'real_period':1.8,'torsion_order':1,'j_invariant':800}]
primary=project(records); ptd=map_ptd(records); mcj=map_mcj(records)
assert all(x.shape==(2,3) and np.isfinite(x).all() for x in [primary,ptd,mcj])
print('primary/PTD/MCJ mapping smoke tests passed')
