from pathlib import Path
import sys
root=Path.cwd()
while root != root.parent and not (root/'registry').is_dir(): root=root.parent
assert (root/'registry').is_dir(), 'repository root with registry/ not found'
sys.path.insert(0,str(root))
sys.path.insert(0,str(root/'src'))
import numpy as np
from acsc.tda_pipeline import compute_persistence
points=np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
result=compute_persistence(points,maxdim=1,thresh=2.0)
assert set(result)=={'dgms'} and len(result['dgms'])==2
print([d.shape for d in result['dgms']])
