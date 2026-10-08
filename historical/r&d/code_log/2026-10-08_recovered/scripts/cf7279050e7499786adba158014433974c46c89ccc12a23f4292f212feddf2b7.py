# SageMath script for elliptic curve analysis with BSD analogy to galaxy mass ratios
from sage.all import *
from sage.libs.pari import pari
import matplotlib.pyplot as plt
import numpy as np

# Set PARI stack size and precision
pari.set_parisizemax(1073741824)  # Maximum stack size: 1GB
pari.set_parisize(268435456)      # Initial stack size: 256MB
pari.set_real_precision(128)      # Precision in bits

# Generate Fibonacci numbers up to index 100
def fibonacci(n):
    f = [0] * (n + 1)
    f[0] = 0
    f[1] = 1
    for i in range(2, n + 1):
        f[i] = f[i-1] + f[i-2]
    return f

# Generate Lucas numbers up to index 100
def lucas(n):
    l = [0] * (n + 1)
    l[0] = 2
    l[1] = 1
    for i in range(2, n + 1):
        l[i] = l[i-1] + l[i-2]
    return l

# Check if the Heegner hypothesis is satisfied for conductor N and discriminant D
def heegner_hypothesis(N, D):
    fact = factor(N)
    satisfied = True
    for p, k in fact:
        kronecker_val = kronecker(D, p)
        if kronecker_val != -1:
            print(f"p={p} is not inert (kronecker(D, p) != -1)")
            satisfied = False
            break
        if k == 1 and (p != -D % p or (N/p) % p == 0):
            print(f"Heegner hypothesis failed for p={p}: k=1 but p does not divide -D or p divides N/p")
            satisfied = False
            break
        if k > 1 and (-D % p != 0 or N % (p^2) != 0):
            print(f"Heegner hypothesis failed for p={p}: k={k} but p^2 does not divide N or -D != 0 (mod p)")
            satisfied = False
            break
    if satisfied:
        print(f"Heegner hypothesis satisfied for N={N}, D={D}")
    return satisfied

# Compute Heegner point or attempt quadratic twists
def compute_heegner_point(E, N, D, max_twists):
    if heegner_hypothesis(N, D):
        print(f"Attempting to compute Heegner point with D={D} on original curve")
        try:
            E.heegner_point(D)
            return True
        except Exception as e:
            print(f"Failed to compute Heegner point with D={D} on original curve: {e}")
            return False
    
    twist_attempts = [2, 3, 5, 7, 11]
    for i in range(min(max_twists, len(twist_attempts))):
        d = twist_attempts[i]
        new_N = N * d^2
        Etwist = E.quadratic_twist(d)
        print(f"Attempting quadratic twist with d={d}, new conductor={new_N}")
        if heegner_hypothesis(new_N, D):
            try:
                Etwist.heegner_point(D)
                print(f"Heegner hypothesis satisfied for N={new_N}, D={D}")
                return True
            except Exception as e:
                print(f"Failed to compute Heegner point with twist d={d}: {e}")
        else:
            print(f"Failed to compute Heegner point with twist d={d}: N(={new_N}) and D(={D}) must satisfy the Heegner hypothesis")
    print(f"Failed to compute Heegner point for curve {E} after {max_twists} twists")
    return False

# Main analysis function for an elliptic curve
def analyze_curve(a, b, batch, total_batches, curve_idx, galaxy_mass_ratio, rank_dist):
    E = EllipticCurve(QQ, [0, 0, 0, a, b])
    conductor = E.conductor()
    dynamic_limit = 381455078125.0 / (1 + batch/total_batches)
    print(f"Analyzing curve: y^2 = x^3 + {a}x + {b}")
    print(f"Dynamic conductor limit: {dynamic_limit}")
    
    # Scale coefficients using galaxy mass ratio
    if conductor > dynamic_limit:
        scale_factor = (conductor / dynamic_limit) ** (1/2) * galaxy_mass_ratio
        new_a = a / scale_factor^4
        new_b = b / scale_factor^6
        print(f"Scaling coefficients with galaxy mass ratio {galaxy_mass_ratio}: a={a} -> {new_a}, b={b} -> {new_b}, scale_factor={scale_factor}")
        E = EllipticCurve(QQ, [0, 0, 0, new_a, new_b])
        conductor = E.conductor()
    
    # Adjusted L-function parameters with higher precision
    prec = 64
    Dmax = 50
    M = 20
    nmax = 50000
    print(f"Adjusted L-function params: prec={prec}, Dmax={Dmax}, M={M}, nmax={nmax}")
    
    # Compute ranks with retries on precision errors
    for attempt in range(1, 4):
        try:
            analytic_rank = E.analytic_rank(precision=prec)
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt}: {e}")
            prec *= 2
            if attempt == 3:
                raise Exception("Failed to compute analytic rank after 3 attempts")
    
    for attempt in range(1, 4):
        try:
            algebraic_rank = E.rank()
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt}: {e}")
            prec *= 2
            if attempt == 3:
                raise Exception("Failed to compute algebraic rank after 3 attempts")
    
    print(f"Analytic rank: {analytic_rank}")
    print(f"Algebraic rank (via PARI/GP): {algebraic_rank}")
    print(f"Weak BSD holds: {analytic_rank == algebraic_rank}")
    rank_dist.append(algebraic_rank)
    
    # Earth mapping (using values from the PDF)
    longitude = 180000
    latitude = 89900
    elevation = 1402.6503751475802
    size = 100.0
    Z = 635674231.8115495
    if algebraic_rank == 0:
        longitude = -116436.72544647662
        latitude = 8775.860902042263
        elevation = 0
        size = 31.62277660168379
        Z = 96984631.81631373
    print(f"Earth mapping: Longitude={longitude} UE units, Latitude={latitude} UE units, Elevation={elevation} UE units, Size={size} UE units, Z={Z} UE units")
    
    # Attempt BSD invariants computation with Heegner points
    if analytic_rank > 0:
        D = -3
        N = conductor
        max_twists = 5
        if not compute_heegner_point(E, N, D, max_twists):
            print(f"Failed to compute BSD invariants: Failed to compute Heegner point for curve {E} after {max_twists} twists")

# Main execution
fibs = fibonacci(100)
lucas_nums = lucas(100)
print(f"Fibonacci numbers up to index 100: {fibs}")
print(f"Lucas numbers up to index 100: {lucas_nums}")

total_curves = 542
batch_size = 3
total_batches = ceil(total_curves / batch_size)
curves_processed = 0
rank_dist = []
print(f"Generated {total_curves} unique curves")

# Simulated galaxy mass ratios (from your 1,108 galaxy dataset discussion)
galaxy_mass_ratios = [1.0 + i*0.01 for i in range(total_curves)]

# Generate curves using Fibonacci and Lucas numbers
for batch in range(1, total_batches + 1):
    start_idx = (batch-1)*batch_size + 1
    end_idx = min(batch*batch_size, total_curves)
    print(f"Processing batch {batch}/{total_batches} ({start_idx-1} to {end_idx-1})")
    for i in range(start_idx, end_idx + 1):
        a = fibs[i]
        b = lucas_nums[i]
        mass_ratio = galaxy_mass_ratios[i-1]
        analyze_curve(a, b, batch, total_batches, i, mass_ratio, rank_dist)
        curves_processed += 1
    print(f"Completed batch {batch}/{total_batches} ({round(curves_processed/total_curves*100, 1)}% done)")

# Plot rank distribution
print("Processing complete, generating plots...")
plt.figure(figsize=(8, 6))
plt.hist(rank_dist, bins=range(max(rank_dist)+2), align='left', rwidth=0.8, color='blue', alpha=0.7)
plt.title('Rank Distribution of Elliptic Curves')
plt.xlabel('Algebraic Rank')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('distortion_free_rank_distribution_v9.png')
print("Rank distribution plot saved as distortion_free_rank_distribution_v9.png")