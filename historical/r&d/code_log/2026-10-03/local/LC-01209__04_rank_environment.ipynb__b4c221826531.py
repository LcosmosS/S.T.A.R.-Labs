import pandas as pd
frame=pd.DataFrame({'rank':[0,1,2,3],'environment':['void','field','group','cluster']})
assert frame['rank'].is_monotonic_increasing
assert frame['environment'].notna().all()
print(frame.to_string(index=False))
