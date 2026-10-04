from pathlib import Path
import sys
root=Path.cwd()
while root != root.parent and not (root/'registry').is_dir(): root=root.parent
assert (root/'registry').is_dir(), 'repository root with registry/ not found'
sys.path.insert(0,str(root))
sys.path.insert(0,str(root/'src'))
import numpy as np
from acsc.projection import ArithmeticProjector
records=[{'delta':-11,'conductor':11,'rank':1},{'delta':-37,'conductor':37,'rank':2}]
a=ArithmeticProjector(Amax=1.0,Nmax=1.0,V0=1.0).project(records)
b=ArithmeticProjector(Amax=2.0,Nmax=2.0,V0=1.0).project(records)
assert a.shape==b.shape==(2,3) and np.isfinite(a).all() and np.isfinite(b).all()
assert not np.array_equal(a,b)
print('robustness parameter sensitivity smoke test passed')
