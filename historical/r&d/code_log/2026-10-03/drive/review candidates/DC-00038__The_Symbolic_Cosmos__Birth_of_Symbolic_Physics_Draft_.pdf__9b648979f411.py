rank = descent_rank
rank_success = True
except:
print("Two-descent failed, attempting point search")
try:
points = E.points(bound=100)
