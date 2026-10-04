D = -43 # Satisfies Heegner hypothesis for all curves
try:
# Compute a Heegner point with conductor 1
P_K = E.heegner_point(D, 1) # Heegner point in E(K)
P = P_K.trace_to_rational() # Trace to E(Q)
print(f"Heegner point (traced to Q): {P.xy()}")
# Check if the point has infinite order
if P.order() == 0:
print("Heegner point has infinite order, suggesting rank
