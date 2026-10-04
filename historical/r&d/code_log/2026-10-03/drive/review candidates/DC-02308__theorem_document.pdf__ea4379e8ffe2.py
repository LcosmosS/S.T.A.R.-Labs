from persim import wasserstein
def compare_topologies(diag1, diag2):
return wasserstein(diag1[1], diag2[1])
# Example: diag1 from elliptic curve, diag2 from galaxy data
distance = compare_topologies(diagrams_curve, diagrams_galaxy)
