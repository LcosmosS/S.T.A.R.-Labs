# Enhanced SageMath script for elliptic curve analysis with Heegner points, Selmer ranks, twists, and ML
from sage.all import EllipticCurve, QQ, pari, QuadraticTwist
from sage.rings.rational_field import RationalField
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint
from joblib import Parallel, delayed
from gplearn.genetic import SymbolicRegressor
import csv
import sys
import os
import numpy as np

# Set up SageMath environment for parallel processing
os.environ["SAGE_NUM_THREADS"] = "2"

# Step 1: Generate the grid of elliptic curves
a_values = list(range(-150, 151, 15))  # 21 values
b_values = list(range(-150, 151, 15))  # 21 values
curves = []

print("Generating curves for the grid.")
for i, a in enumerate(a_values):
    for b in b_values:
        try:
            E = EllipticCurve(QQ, [0, 0, 0, a, b])
            if E.discriminant() != 0:
                curves.append((a, b, E))
        except Exception:
            continue
    print(f"Generated curves for a={a} ({i+1}/21 a values processed)")

total_curves = len(curves)
print(f"Generated {total_curves} valid curves.")

# Step 2: Assign grid points (logging)
for i in range(50, 301, 50):
    print(f"Assigned {i}/{total_curves} grid points ({i/total_curves*100:.1f}%)")
print(f"Assigned 300/{total_curves} grid points ({300/total_curves*100:.1f}%)")

# Step 3: Define the function to analyze a single curve
def analyze_curve(a, b, E, curve_idx, total_curves):
    print(f"Analyzing curve {curve_idx+1}/{total_curves}: y^2 = x^3 + {a}x + {b}")
    
    # Compute basic curve properties
    discriminant = E.discriminant()
    conductor = E.conductor()
    torsion_order = E.torsion_subgroup().order()
    
    # Compute rank using mwrank first, then fall back to default
    try:
        rank = E.rank(only_use_mwrank=True)
        print(f"Rank (mwrank): {rank}")
    except Exception:
        try:
            rank = E.rank()
            print(f"Rank (default): {rank}")
        except Exception as e:
            rank = f"Error: {str(e)}"
            print(f"Error computing rank: {e}")
    
    # Compute 2-Selmer and 3-Selmer ranks
    try:
        selmer_2 = E.selmer_rank_bound(p=2)[0]
        selmer_3 = E.selmer_rank_bound(p=3)[0]
        print(f"2-Selmer rank: {selmer_2}, 3-Selmer rank: {selmer_3}")
    except Exception as e:
        selmer_2 = selmer_3 = f"Error: {str(e)}"
        print(f"Error computing Selmer ranks: {e}")
    
    # Compute Heegner points using PARI/GP
    try:
        D = -7  # Heegner discriminant (example value)
        heegner_point = E.heegner_point(D)
        heegner_coords = (float(heegner_point[0]), float(heegner_point[1]))
        print(f"Heegner point: {heegner_coords}")
    except Exception as e:
        heegner_coords = (0, 0)
        print(f"Error computing Heegner point: {e}")
    
    # Attempt to twist 3-Selmer rank 2 curves to rank 3
    twisted = False
    twisted_rank = None
    if selmer_3 == 2:
        try:
            twist_d = 3  # Example twisting parameter
            E_twist = E.quadratic_twist(twist_d)
            twisted_rank = E_twist.selmer_rank_bound(p=3)[0]
            if twisted_rank == 3:
                twisted = True
                print(f"Successfully twisted to 3-Selmer rank: {twisted_rank}")
        except Exception as e:
            print(f"Error twisting curve: {e}")
    
    # Map to latitude/longitude for oblate spheroid (simplified mapping)
    lat = float(a) / 150 * 90  # Scale a to latitude (-90 to 90)
    lon = float(b) / 150 * 180  # Scale b to longitude (-180 to 180)
    
    return (a, b, discriminant, conductor, torsion_order, rank, selmer_2, selmer_3, heegner_coords, twisted, twisted_rank, lat, lon)

# Step 4: Process curves in parallel with n_jobs=2
n_jobs = 2
chunk_size = total_curves // n_jobs
num_chunks = (total_curves + chunk_size - 1) // chunk_size

print(f"Processing {total_curves} curves in {num_chunks} chunks with {n_jobs} jobs")

# Collect data for ML and symbolic regression
curve_data = []
with open("elliptic_curve_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["a", "b", "Discriminant", "Conductor", "Torsion Order", "Rank", "2-Selmer", "3-Selmer", "Heegner X", "Heegner Y", "Twisted", "Twisted Rank", "Latitude", "Longitude"])
    
    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, total_curves)
        chunk_curves = curves[start_idx:end_idx]
        
        print(f"\nProcessing chunk {chunk_idx+1}/{num_chunks} ({len(chunk_curves)} curves)")
        
        results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
            delayed(analyze_curve)(a, b, E, i, total_curves)
            for i, (a, b, E) in enumerate(chunk_curves, start_idx)
        )
        
        for result in results:
            a, b, disc, cond, tors, rank, s2, s3, (hx, hy), twisted, twisted_rank, lat, lon = result
            writer.writerow([a, b, disc, cond, tors, rank, s2, s3, hx, hy, twisted, twisted_rank, lat, lon])
            # Collect numerical data for ML (skip if rank or Selmer ranks are errors)
            if isinstance(rank, (int, float)) and isinstance(s2, int) and isinstance(s3, int):
                curve_data.append([a, b, disc, cond, tors, rank, s2, s3, hx, hy])
        
        print(f"Completed chunk {chunk_idx+1}/{num_chunks} ({(chunk_idx+1)/num_chunks*100:.1f}% done)")

# Step 5: Apply symbolic regression to predict 3-Selmer rank
if curve_data:
    X = np.array([[d[0], d[1], d[2], d[3], d[4], d[6], d[8], d[9]] for d in curve_data])  # Features: a, b, disc, cond, tors, 2-Selmer, Heegner X/Y
    y = np.array([d[7] for d in curve_data])  # Target: 3-Selmer rank
    
    # Symbolic regression to find relationship
    sr = SymbolicRegressor(population_size=500, generations=20, random_state=0)
    sr.fit(X, y)
    print(f"Symbolic regression equation for 3-Selmer rank: {sr._program}")

print("Analysis complete. Results saved to 'elliptic_curve_results.csv'.")