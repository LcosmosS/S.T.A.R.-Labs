# quick verify
import json
p = "derived/tda_ptd_batches/summary_per_chunk.json"
s = json.loads(open(p).read())
print("Chunks in summary:", len(s))
print("Example entry:", s[0])
