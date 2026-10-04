rank = descent_rank
rank_success = True
except:
print("Two-descent failed, attempting point search")
points = E.points(bound=200)
