from pathlib import Path
import sys
root=Path.cwd()
while root != root.parent and not (root/'registry').is_dir(): root=root.parent
assert (root/'registry').is_dir(), 'repository root with registry/ not found'
sys.path.insert(0,str(root))
sys.path.insert(0,str(root/'src'))
import numpy as np
from acsc.statistics import empirical_p_value, effect_size
null=np.array([0.1,0.2,0.3,0.4,0.5])
p=empirical_p_value(0.3,null); e=effect_size(0.3,null)
assert 0.0 < p <= 1.0 and np.isfinite(e)
print(f'empirical_p={p:.6f}, effect_size={e:.6f}')
