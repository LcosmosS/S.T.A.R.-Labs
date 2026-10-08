# Optimized SageMath script to analyze elliptic curves with reduced computational requirements
from sage.all import EllipticCurve, QQ, sage
from sage.rings.rational_field import RationalField
from joblib import Parallel, delayed
import csv
import sys
import os

# Ensure SageMath environment is properly set up for parallel processing
os.environ["SAGE_NUM_THREADS"] = "2"  # Limit SageMath internal threads to avoid conflicts

# Step 1: Generate the grid of elliptic curves
a_values = list(range(-150, 151, 15))  # 21 values
b_values = list(range(-150, 151, 15))  # 21 values
curves = []

print("Generating curves for the grid.")
for i, a in enumerate(a_values):
    for b in b_values:
        try:
            E = EllipticCurve(QQ, [0, 0, 0, a, b])
            if E.discriminant() != 0:  # Filter invalid curves early
                curves.append((a, b, E))
        except Exception:
            continue
    print(f"Generated curves for a={a} ({i+1}/21 a values processed, 21 b values per a)")

total_curves = len(curves)
print(f"Generated {total_curves} valid curves.")

# Step 2: Assign grid points (logging)
for i in range(50, 301, 50):
    print(f"Assigned {i}/{total_curves} grid points ({i/total_curves*100:.1f}%)")
print(f"Assigned 300/{total_curves} grid points ({300/total_curves*100:.1f}%)")

# Step 3: Define the function to analyze a single curve
def analyze_curve(a, b, E, curve_idx, total_curves):
    print(f"Analyzing curve {curve_idx+1}/{total_curves}: y^2 = x^3 + {a}x + {b}")
    
    # Compute curve properties
    discriminant = E.discriminant()
    conductor = E.conductor()
    torsion_order = E.torsion_subgroup().order()
    
    # Compute rank using mwrank first, then fall back to default if needed
    try:
        rank = E.rank(only_use_mwrank=True)
        print(f"Rank (mwrank): {rank}")
    except Exception as e:
        print(f"mwrank failed: {e}, falling back to default rank method")
        try:
            rank = E.rank()  # Default SageMath method
            print(f"Rank (default): {rank}")
        except Exception as e:
            rank = f"Error: {str(e)}"
            print(f"Error computing rank: {e}")
    
    return (a, b, discriminant, conductor, torsion_order, rank)

# Step 4: Process curves in parallel with n_jobs=2
n_jobs = 2
chunk_size = total_curves // n_jobs  # Roughly 220 curves per job
num_chunks = (total_curves + chunk_size - 1) // chunk_size

print(f"Processing {total_curves} curves in {num_chunks} chunks with {n_jobs} jobs")

# Open a CSV file to write results incrementally (reduces memory usage)
with open("elliptic_curve_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["a", "b", "Discriminant", "Conductor", "Torsion Order", "Rank"])
    
    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, total_curves)
        chunk_curves = curves[start_idx:end_idx]
        
        print(f"\nProcessing chunk {chunk_idx+1}/{num_chunks} ({len(chunk_curves)} curves, indices {start_idx} to {end_idx-1})")
        
        # Parallel processing of the chunk
        results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
            delayed(analyze_curve)(a, b, E, i, total_curves)
            for i, (a, b, E) in enumerate(chunk_curves, start_idx)
        )
        
        # Write results to CSV immediately to free memory
        for result in results:
            writer.writerow(result)
        
        print(f"Completed chunk {chunk_idx+1}/{num_chunks} ({(chunk_idx+1)/num_chunks*100:.1f}% of chunks done)")

print("Analysis complete. Results saved to 'elliptic_curve_results.csv'.")