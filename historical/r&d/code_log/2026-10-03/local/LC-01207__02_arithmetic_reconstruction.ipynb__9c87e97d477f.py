from pathlib import Path
import sys
root=Path.cwd()
while root != root.parent and not (root/'registry').is_dir(): root=root.parent
assert (root/'registry').is_dir(), 'repository root with registry/ not found'
sys.path.insert(0,str(root))
sys.path.insert(0,str(root/'src'))
import numpy as np
from acsc.projection import project
records=[{'delta':-11,'conductor':11,'rank':0},{'delta':-19,'conductor':19,'rank':1},{'delta':-37,'conductor':37,'rank':2}]
coords=project(records)
assert coords.shape==(3,3) and np.isfinite(coords).all()
print(coords)
