# Comprehensive SageMath script for elliptic curve analysis with plotting and Unreal Engine export
from sage.all import EllipticCurve, QQ, pari
from sage.rings.rational_field import RationalField
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint
from joblib import Parallel, delayed
from gplearn.genetic import SymbolicRegressor
import csv
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.mixture import GaussianMixture

# Set up SageMath environment for parallel processing
os.environ["SAGE_NUM_THREADS"] = "2"

# Define Fibonacci and Lucas number generators
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def lucas(n):
    if n <= 0:
        return 2
    elif n == 1:
        return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Golden ratio
golden_ratio = (1 + np.sqrt(5)) / 2

# Generate Fibonacci and Lucas sequences (21 values for a and b ranges)
fib_sequence = [fibonacci(i) for i in range(21)]
lucas_sequence = [lucas(i) for i in range(21)]

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
def analyze_curve(a, b, E, curve_idx, total_curves, a_idx, b_idx):
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
    
    # Compute the regulator (for BSD conjecture)
    try:
        regulator = E.regulator() if isinstance(rank, int) and rank > 0 else 0
        print(f"Regulator: {regulator}")
    except Exception as e:
        regulator = f"Error: {str(e)}"
        print(f"Error computing regulator: {e}")
    
    # Compute the L-function value at s=1 (approximation for BSD)
    try:
        L_value = E.L_function().value(1)
        print(f"L-function at s=1: {L_value}")
    except Exception as e:
        L_value = f"Error: {str(e)}"
        print(f"Error computing L-function: {e}")
    
    # Compute Heegner points using PARI/GP
    try:
        D = -7  # Heegner discriminant
        heegner_point = E.heegner_point(D)
        heegner_coords = (float(heegner_point[0]), float(heegner_point[1]))
        print(f"Heegner point: {heegner_coords}")
    except Exception as e:
        heegner_coords = (0, 0)
        print(f"Error computing Heegner point: {e}")
    
    # Attempt to twist 3-Selmer rank 2 curves to rank 3, using Lucas numbers
    twisted = False
    twisted_rank = None
    if selmer_3 == 2:
        try:
            twist_d = lucas_sequence[a_idx % len(lucas_sequence)]
            E_twist = E.quadratic_twist(twist_d)
            twisted_rank = E_twist.selmer_rank_bound(p=3)[0]
            if twisted_rank == 3:
                twisted = True
                print(f"Successfully twisted to 3-Selmer rank: {twisted_rank} with twist_d={twist_d}")
        except Exception as e:
            print(f"Error twisting curve: {e}")
    
    # Map to latitude/longitude for oblate spheroid using Fibonacci and Golden Ratio
    fib_a = fib_sequence[a_idx % len(fib_sequence)]
    fib_b = fib_sequence[b_idx % len(fib_sequence)]
    lat = (float(a) / 150 * 90) * (fib_a / max(fib_sequence)) * golden_ratio
    lon = (float(b) / 150 * 180) * (fib_b / max(fib_sequence)) * golden_ratio
    lat = min(max(lat, -90), 90)  # Clamp latitude
    lon = min(max(lon, -180), 180)  # Clamp longitude
    
    # Compute z-coordinate for oblate spheroid (simplified flattening factor)
    flattening = 0.1  # Oblate spheroid flattening factor
    z = (1 - flattening) * np.sin(np.radians(lat))
    
    return (a, b, discriminant, conductor, torsion_order, rank, selmer_2, selmer_3, regulator, L_value, heegner_coords, twisted, twisted_rank, lat, lon, z)

# Step 4: Process curves in parallel with n_jobs=2
n_jobs = 2
chunk_size = total_curves // n_jobs
num_chunks = (total_curves + chunk_size - 1) // chunk_size

print(f"Processing {total_curves} curves in {num_chunks} chunks with {n_jobs} jobs")

# Collect data for ML, plotting, and Unreal Engine export
curve_data = []
plot_data = {'ranks': [], 'heegner_x': [], 'heegner_y': [], 'lat': [], 'lon': [], 'z': []}
with open("elliptic_curve_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["a", "b", "Discriminant", "Conductor", "Torsion Order", "Rank", "2-Selmer", "3-Selmer", "Regulator", "L-function", "Heegner X", "Heegner Y", "Twisted", "Twisted Rank", "Latitude", "Longitude", "Z"])
    
    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, total_curves)
        chunk_curves = curves[start_idx:end_idx]
        
        print(f"\nProcessing chunk {chunk_idx+1}/{num_chunks} ({len(chunk_curves)} curves)")
        
        results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
            delayed(analyze_curve)(
                a, b, E, i, total_curves, 
                a_values.index(a), b_values.index(b)
            )
            for i, (a, b, E) in enumerate(chunk_curves, start_idx)
        )
        
        for result in results:
            a, b, disc, cond, tors, rank, s2, s3, reg, L_val, (hx, hy), twisted, twisted_rank, lat, lon, z = result
            writer.writerow([a, b, disc, cond, tors, rank, s2, s3, reg, L_val, hx, hy, twisted, twisted_rank, lat, lon, z])
            # Collect data for ML and plotting
            if isinstance(rank, (int, float)) and isinstance(s2, int) and isinstance(s3, int):
                curve_data.append([a, b, disc, cond, tors, rank, s2, s3, hx, hy])
                plot_data['ranks'].append(rank)
                plot_data['heegner_x'].append(hx)
                plot_data['heegner_y'].append(hy)
                plot_data['lat'].append(lat)
                plot_data['lon'].append(lon)
                plot_data['z'].append(z)
        
        print(f"Completed chunk {chunk_idx+1}/{num_chunks} ({(chunk_idx+1)/num_chunks*100:.1f}% done)")

# Step 5: Apply Gaussian Mixture Model for subpopulation identification
if curve_data:
    X_gmm = np.array([[d[5], d[6], d[7]] for d in curve_data])  # Rank, 2-Selmer, 3-Selmer
    gmm = GaussianMixture(n_components=3, random_state=0)
    gmm.fit(X_gmm)
    labels = gmm.predict(X_gmm)
    print("Gaussian Mixture Model clustering completed. Subpopulation labels assigned.")

# Step 6: Symbolic regression to predict 3-Selmer rank
if curve_data:
    X = np.array([[d[0], d[1], d[2], d[3], d[4], d[6], d[8], d[9]] for d in curve_data])  # Features: a, b, disc, cond, tors, 2-Selmer, Heegner X/Y
    y = np.array([d[7] for d in curve_data])  # Target: 3-Selmer rank
    sr = SymbolicRegressor(population_size=500, generations=20, random_state=0)
    sr.fit(X, y)
    print(f"Symbolic regression equation for 3-Selmer rank: {sr._program}")

# Step 7: Plotting
# Plot 1: Histogram of ranks
plt.figure(figsize=(10, 6))
plt.hist(plot_data['ranks'], bins=range(int(min(plot_data['ranks'])), int(max(plot_data['ranks'])) + 2), edgecolor='black')
plt.title("Distribution of Elliptic Curve Ranks")
plt.xlabel("Rank")
plt.ylabel("Frequency")
plt.savefig("rank_distribution.png")
plt.close()

# Plot 2: Scatter plot of Heegner points
plt.figure(figsize=(10, 6))
plt.scatter(plot_data['heegner_x'], plot_data['heegner_y'], c=plot_data['ranks'], cmap='viridis')
plt.colorbar(label="Rank")
plt.title("Heegner Points of Elliptic Curves")
plt.xlabel("Heegner X")
plt.ylabel("Heegner Y")
plt.savefig("heegner_points.png")
plt.close()

# Plot 3: 3D scatter plot of latitude/longitude/z for oblate spheroid
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(plot_data['lon'], plot_data['lat'], plot_data['z'], c=plot_data['ranks'], cmap='plasma')
ax.set_title("Oblate Spheroid Mapping (Latitude, Longitude, Z)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Z (Flattened)")
plt.savefig("oblate_spheroid_map.png")
plt.close()

# Step 8: Export latitude/longitude/z data for Unreal Engine
with open("unreal_engine_coordinates.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Latitude", "Longitude", "Z", "Rank"])
    for lat, lon, z, rank in zip(plot_data['lat'], plot_data['lon'], plot_data['z'], plot_data['ranks']):
        writer.writerow([lat, lon, z, rank])
print("Unreal Engine coordinates exported to 'unreal_engine_coordinates.csv'.")

print("Analysis complete. Results saved to 'elliptic_curve_results.csv'. Plots saved as PNG files.")te=0)
    sr.fit(X, y)
    print(f"Symbolic regression equation for 3-Selmer rank: {sr._program}")

print("Analysis complete. Results saved to 'elliptic_curve_results.csv'.")"Symbolic regression equation for 3-Selmer rank: {sr._program}")

print("Analysis complete. Results saved to 'elliptic_curve_results.csv'.")