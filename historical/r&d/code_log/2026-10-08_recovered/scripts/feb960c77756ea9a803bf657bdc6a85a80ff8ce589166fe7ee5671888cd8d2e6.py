import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, Integer
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging
import sys

# Verify SageMath environment
try:
    import sage
    from sage.version import version as sage_version
    print(f"SageMath version: {sage_version}")
    if sage_version < "10.6":
        raise RuntimeError("SageMath version 10.6 or higher is required. Please update SageMath.")
except ImportError:
    print("This script must be run in a SageMath environment. Please run with 'sage refined_mapping_test.py'.")
    sys.exit(1)

# Set up logging
logging.basicConfig(filename='refined_mapping_test.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_print(*args, **kwargs):
    msg = " ".join(map(str, args))
    logging.info(msg)
    print(msg)

# Set up PARI memory allocation
pari.allocatemem(2**31)
pari.set_debug_level(2)
log_print(f"PARI stack size set to {2**31} bytes")

# Constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
log_print(f"Golden ratio (φ): {PHI}")

# Earth's oblate spheroid parameters (in cm for Unreal Engine units)
A = 637813700  # Semi-major axis (equatorial radius, 6378.137 km)
C = 635675200  # Semi-minor axis (polar radius, 6356.752 km)

# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

fib_numbers = generate_fibonacci(50)
log_print(f"Fibonacci numbers up to index 50: {fib_numbers}")

# Generate Lucas numbers
def generate_lucas(n):
    lucas = [2, 1]
    for i in range(2, n + 1):
        lucas.append(lucas[i-1] + lucas[i-2])
    return lucas

lucas_numbers = generate_lucas(50)
log_print(f"Lucas numbers up to index 50: {lucas_numbers}")

# Function to compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

# Function to analyze an elliptic curve
def analyze_curve(a, b, max_attempts=3, conductor_limit=1e12):
    log_print(f"Analyzing curve: y² = x³ + {a}x + {b}")
    success = False
    rank = None
    log_delta = None
    log_cond = None
    longitude = None
    latitude = None
    z = None

    # Skip curves with large coefficients
    if abs(a) > 10**6 or abs(b) > 10**6:
        log_print(f"Coefficients too large (|a|={abs(a)}, |b|={abs(b)}), skipping curve")
        return (success, rank, log_delta, log_cond, longitude, latitude, z)

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        log_print(f"Error creating curve: {e}")
        return (success, rank, log_delta, log_cond, longitude, latitude, z)

    delta = E.discriminant()
    conductor = E.conductor()
    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(float(conductor)) if conductor > 0 else 0

    if conductor > conductor_limit:
        log_print(f"Conductor too large (> {conductor_limit}), skipping curve")
        return (success, rank, log_delta, log_cond, longitude, latitude, z)

    # Compute rank
    for attempt in range(max_attempts):
        try:
            E_pari = pari.ellinit([0, 0, 0, a, b])
            rank_info = E_pari.ellrank()
            rank = int(rank_info[0])
            log_print(f"Algebraic rank (via PARI/GP): {rank}")
            success = True
            break
        except Exception as e:
            log_print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                return (success, rank, log_delta, log_cond, longitude, latitude, z)

    if success:
        # Map to oblate spheroid with Fibonacci/Lucas grid and distortion correction
        fib_max = fib_numbers[10]  # Use F_10 = 55 for scaling
        lucas_max = lucas_numbers[10]  # Use L_10 = 123 for scaling
        idx = (a % len(fib_numbers)) if a > 0 else (-a % len(fib_numbers))
        fib_value = fib_numbers[idx % 10]
        lucas_value = lucas_numbers[idx % 10]

        # Base latitude and longitude using Fibonacci and Lucas spacing
        phi = -90 + (180 * fib_value / fib_max)  # Latitude in [-90, 90] degrees
        lambda_ = (360 * lucas_value / lucas_max)  # Longitude in [0, 360] degrees

        # Apply golden ratio adjustment
        phi *= PHI
        lambda_ *= PHI
        lambda_ = lambda_ % 360
        if lambda_ > 180:
            lambda_ -= 360  # Convert to [-180, 180]

        # Oblate spheroid adjustments
        flattening = (A - C) / A
        phi_rad = np.radians(phi)
        phi_adjusted = np.degrees(np.arctan(np.tan(phi_rad) / ((1 - flattening)**2)))

        # Distortion correction using rank
        correction_factor = 1 + (rank / 10) if rank is not None else 1
        phi_adjusted = phi_adjusted + (correction_factor - 1) * (90 - phi_adjusted)
        lambda_adjusted = lambda_ + (correction_factor - 1) * (180 - lambda_)

        # Convert to Unreal Engine units
        ue_scale = 1000
        latitude = phi_adjusted * ue_scale
        longitude = lambda_adjusted * ue_scale
        z = C * np.sin(np.radians(phi_adjusted))

        log_print(f"Mapping: Longitude={longitude} UE units, Latitude={latitude} UE units, Z={z} UE units")

    # Clean up
    try:
        del E, delta, conductor, E_pari
    except NameError:
        pass
    gc.collect()
    return (success, rank, log_delta, log_cond, longitude, latitude, z)

# Main test procedure
def main():
    # Define new set of elliptic curves
    a_values = [5000, 10000, 15000, 20000]
    b_values = [100000, 200000, 300000, 400000]
    conductor = 637813700
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"refined_mapping_nodes_{timestamp}.csv"

    # Initialize CSV
    with open(csv_file, 'w', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerow(['a', 'b', 'rank', 'log_delta', 'log_cond', 'longitude', 'latitude', 'z'])

    plot_data = {'ranks': [], 'log_delta': [], 'log_cond': [], 'lon': [], 'lat': [], 'z': []}
    mapping_data = []

    # Analyze curves
    for a in a_values:
        for b in b_values:
            result = analyze_curve(a, b)
            if len(result) != 7:
                continue
            success, rank, log_delta, log_cond, longitude, latitude, z = result
            if success:
                data_tuple = (a, b, rank, log_delta, log_cond, longitude, latitude, z)
                mapping_data.append(data_tuple)
                with open(csv_file, 'a', newline='') as csv_f:
                    csv_writer = csv.writer(csv_f)
                    csv_writer.writerow(data_tuple)
                if all(v is not None for v in [rank, log_delta, log_cond, longitude, latitude, z]):
                    plot_data['ranks'].append(rank)
                    plot_data['log_delta'].append(log_delta)
                    plot_data['log_cond'].append(log_cond)
                    plot_data['lon'].append(longitude)
                    plot_data['lat'].append(latitude)
                    plot_data['z'].append(z)
            gc.collect()

    # Evaluate mapping accuracy using known landmarks
    landmarks = {
        "Equator": (0, 0),  # (latitude, longitude)
        "North Pole": (90, 0),
        "South Pole": (-90, 0),
        "London": (51.5074, -0.1278),
        "Sydney": (-33.8688, 151.2093)
    }
    errors = []
    with open("mapping_accuracy.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Landmark", "True_Lat", "True_Lon", "Mapped_Lat", "Mapped_Lon", "Error"])
        for name, (true_lat, true_lon) in landmarks.items():
            # Find closest mapped point
            min_dist = float('inf')
            mapped_lat, mapped_lon = None, None
            for _, _, _, _, _, lat, lon, _ in mapping_data:
                if lat is None or lon is None:
                    continue
                dist = math.sqrt((lat/1000 - true_lat)**2 + (lon/1000 - true_lon)**2)
                if dist < min_dist:
                    min_dist = dist
                    mapped_lat, mapped_lon = lat/1000, lon/1000
            if mapped_lat is not None and mapped_lon is not None:
                error = math.sqrt((mapped_lat - true_lat)**2 + (mapped_lon - true_lon)**2)
                errors.append(error)
                writer.writerow([name, true_lat, true_lon, mapped_lat, mapped_lon, error])
                log_print(f"Landmark {name}: True ({true_lat}, {true_lon}), Mapped ({mapped_lat}, {mapped_lon}), Error: {error}")

    avg_error = sum(errors) / len(errors) if errors else 0
    log_print(f"Average mapping error: {avg_error} degrees")

    # Generate 3D plot for oblate spheroid
    valid_indices = [i for i in range(len(plot_data['lon'])) if all(v is not None for v in [plot_data['lon'][i], plot_data['lat'][i], plot_data['z'][i], plot_data['ranks'][i]])]
    if valid_indices:
        filtered_lon = [plot_data['lon'][i] for i in valid_indices]
        filtered_lat = [plot_data['lat'][i] for i in valid_indices]
        filtered_z = [plot_data['z'][i] for i in valid_indices]
        filtered_ranks = [plot_data['ranks'][i] for i in valid_indices]

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(filtered_lon, filtered_lat, filtered_z, c=filtered_ranks, cmap='plasma')
        ax.set_title("Refined Oblate Spheroid Mapping (Latitude, Longitude, Z)")
        ax.set_xlabel("Longitude (UE units)")
        ax.set_ylabel("Latitude (UE units)")
        ax.set_zlabel("Z (UE units)")
        plt.savefig("refined_oblate_spheroid_map.png")
        plt.close()
        log_print("Refined oblate spheroid map saved as refined_oblate_spheroid_map.png")
    else:
        log_print("No valid data for oblate spheroid map; skipping plot")

    # Export Unreal Engine coordinates
    with open("refined_unreal_engine_coordinates.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Latitude", "Longitude", "Z", "Rank"])
        for i in valid_indices:
            writer.writerow([plot_data['lat'][i], plot_data['lon'][i], plot_data['z'][i], plot_data['ranks'][i]])
    log_print("Unreal Engine coordinates exported to 'refined_unreal_engine_coordinates.csv'.")

    log_print(f"Mapping data saved to {csv_file}")

if __name__ == '__main__':
    print("This script should be run via the SageMath command line: 'sage refined_mapping_test.py'")
    main()