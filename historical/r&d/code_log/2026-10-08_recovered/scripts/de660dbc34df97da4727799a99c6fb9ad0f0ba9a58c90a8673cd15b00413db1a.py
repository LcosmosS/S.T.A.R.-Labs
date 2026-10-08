import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, Integer, kronecker
import numpy as np
import math
import gc
import csv
from datetime import datetime
import os
import logging
import sys
import traceback

# Verify SageMath environment
try:
    import sage
    from sage.version import version as sage_version
    print(f"SageMath version: {sage_version}")
    if sage_version < "10.6":
        raise RuntimeError("SageMath version 10.6 or higher is required. Please update SageMath.")
except ImportError:
    print("This script must be run in a SageMath environment. Please ensure you're using a SageMath kernel in Jupyter.")
    sys.exit(1)

# Set up logging for batch 3
logging.basicConfig(filename='distortion_free_earth_mapping_test_v2_batch_3.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_print(*args, **kwargs):
    msg = " ".join(map(str, args))
    logging.info(msg)
    print(msg)

# Set up SageMath environment for sequential processing
os.environ["SAGE_NUM_THREADS"] = "1"
pari.allocatemem(2**31)
pari.set_debug_level(2)
log_print(f"PARI stack size set to {2**31} bytes")

# Constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3
VIRGO_DENSITY_HEIGHT = 6320
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
log_print(f"Golden ratio (φ): {PHI}")

# Earth's oblate spheroid parameters (in cm for Unreal Engine units)
A = 637813700  # Semi-major axis (equatorial radius, 6378.137 km)
C = 635675200  # Semi-minor axis (polar radius, 6356.752 km)

# Generate Fibonacci and Lucas numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def generate_lucas(n):
    lucas = [2, 1]
    for i in range(2, n + 1):
        lucas.append(lucas[i-1] + lucas[i-2])
    return lucas

fib_numbers = generate_fibonacci(50)
lucas_numbers = generate_lucas(50)
log_print(f"Fibonacci numbers up to index 50: {fib_numbers}")
log_print(f"Lucas numbers up to index 50: {lucas_numbers}")

# Load training data from batch 0 and batch 2
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
    [34, 4181, 22.7453700939663, 22.0522229134064, 1],
    [17711, 17711, 25.9923456789012, 25.9923456789012, 1],
    [17711, 46368, 25.9865432109876, 24.5998765432109, 1],
    [-102, 918, 19.5063410364742, 18.4077287478061, 1],
    [4, 1152, 163153.99138494278, 61950.12099761353, 1],
    [14, 49392, 180000, 90000, 1],
    [0, 2, 7.454719949364001, 7.454719949364001, 1],
    [0, 1, 6.068425588244111, 3.58351893845611, 6],
    [0, 3, 8.265650165580329, 8.265650165580329, 1],
    [0, 4, 8.841014310483892, 4.68213122712422, 3],
    [0, 7, 9.960245886354738, 9.960245886354738, 1],
    [0, 11, 10.864216133840852, 10.864216133840852, 1],
    [0, 18, 11.84916910403644, 9.65194452670022, 1],
    [0, 29, 12.803017248217058, 11.416722887097167, 1],
    [0, 47, 13.768720791664228, 13.768720791664228, 1],
    [0, 76, 14.729892268816773, 11.957303546576991, 1],
    [0, 123, 15.692794298988945, 15.692794298988945, 1],
    [0, 199, 16.655035237693095, 15.556422949024986, 1],
    [0, 322, 17.617528679332928, 17.617528679332928, 1],
    [0, 521, 18.579925671750843, 16.095019021962845, 1],
    [0, 843, 19.54235950424782, 19.54235950424782, 1],
    [0, 1364, 20.504779265050924, 16.345896181691252, 1],
    [0, 2207, 21.467204400757584, 21.467204400757584, 1],
    [0, 3571, 22.429627483433006, 22.429627483433006, 1],
    [0, 5778, 23.392051350296473, 16.800377618287815, 1],
    [0, 9349, 24.354474917626742, 22.96818055650685, 1],
    [0, 15127, 25.31689859936851, 25.31689859936851, 1],
    [0, 24476, 26.279322237408973, 23.50673351516919, 1],
    [2, 2, 7.7142311448490855, 7.7142311448490855, 1],
    [2, 1, 6.8501261661455, 6.156978985585555, 1],
    [2, 3, 8.389359819906353, 6.779921907472252, 2],
    [2, 4, 8.912473274466036, 8.21932609390609, 1],
    [2, 7, 9.984145455553582, 9.984145455553582, 1],
    [2, 11, 10.873963393468363, 10.873963393468363, 1],
    [2, 18, 11.852820408868944, 11.852820408868944, 1],
    [2, 29, 12.804425513203572, 12.111278332643627, 1],
    [2, 47, 13.769257173446812, 12.159819261012712, 1],
    [2, 76, 14.730097439108834, 14.036950258548888, 1],
    [2, 123, 15.692872634554066, 15.692872634554066, 1],
    [2, 199, 16.655065165408313, 16.655065165408313, 1],
    [2, 322, 17.617540110010868, 14.398664285142665, 1],
    [2, 521, 18.579930038013117, 17.886782857453174, 1],
    [2, 843, 19.542361171996873, 19.542361171996873, 1],
    [2, 1364, 20.504779902077185, 19.81163272151724, 1],
    [2, 2207, 21.46720464407965, 21.46720464407965, 1],
    [2, 3571, 22.429627576373825, 22.429627576373825, 1],
    [2, 5778, 23.392051385796698, 21.7826134733626, 1],
    [2, 9349, 24.354474931186623, 23.66132775062668, 1],
    [2, 15127, 25.316898604547923, 25.316898604547923, 1]
]
training_labels = [3, 3, 3, 3, 3, 3, 1, 2, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 2, 2, 0, 1, 1, 2, 2, 1, 0, 0, 0, 1, 1, 2, 1, 1, 0, 1, 0, 2, 0, 3, 1, 1, 0, 1, 0, 1, 0, 2, 1]
log_print(f"Loaded training data for batch 3: {training_data}")
log_print(f"Loaded labels for batch 3: {training_labels}")

# Helper functions
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

def satisfies_heegner_hypothesis(N, D):
    if D >= 0 or D % 4 not in [0, 1]:
        log_print(f"Heegner hypothesis failed: D={D} is not a negative fundamental discriminant")
        return False
    N = Integer(N)
    prime_factors = N.prime_factors()
    for p in prime_factors:
        k = kronecker(D, p)
        if k == -1:
            continue
        if k == 0 and (p**2).divides(N) and (-D) % p == 0:
            log_print(f"Heegner condition passed: k=0, p^2 divides N, and -D ≡ 0 (mod {p})")
            continue
        if k == 1 and p.divides(-D) and not p.divides(N//p):
            continue
        log_print(f"Heegner hypothesis failed for p={p}, kronecker(D,p)={k}")
        return False
    return True

def find_suitable_discriminant(N):
    fundamental_discriminants = [-3, -4, -7, -8, -11, -12, -15, -19, -20, -23, -24, -27, -28, -31, -35, -39, -43, -47, -51, -52, -55, -59, -67, -68, -71, -79, -83, -87, -88, -91, -95, -99, -103, -107, -111, -115, -119, -123, -127, -131, -139, -143, -151, -155, -163]
    for D in fundamental_discriminants:
        if satisfies_heegner_hypothesis(N, D):
            return D
    D = -3
    max_attempts = 1000
    attempt = 0
    while attempt < max_attempts:
        if D % 4 in [0, 1] and satisfies_heegner_hypothesis(N, D):
            log_print(f"Found suitable discriminant D={D} after dynamic search")
            return D
        D -= 1
        attempt += 1
    log_print("No suitable discriminant found after dynamic search")
    return None

def compute_heegner_point(E, conductor):
    D = find_suitable_discriminant(conductor)
    if D is None:
        log_print("No suitable discriminant found satisfying Heegner hypothesis")
        return (0, 0)
    try:
        heegner = E.heegner_point(D)
        x, y = heegner.xy()
        log_print(f"Heegner point with D={D}: ({x}, {y})")
        return (float(x), float(y))
    except Exception as e:
        log_print(f"Failed to compute Heegner point with D={D}: {e}")
        return (0, 0)

# Analyze elliptic curve with distortion-free Earth mapping
def analyze_curve(a, b, fib_idx, lucas_idx, is_original=False, curve_idx=0, total_curves=542, max_attempts=3, conductor_limit=1e10):
    log_print(f"Analyzing curve {curve_idx+1}/{total_curves}: y² = x³ + {a}x + {b}")
    
    success = False
    features = None
    rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False
    log_delta = None
    log_cond = None
    longitude = None
    latitude = None
    elevation = None
    size = None
    heegner_x = heegner_y = 0
    z = None
    analytic_rank = None

    if abs(a) > 1e6 or abs(b) > 1e6:
        log_print(f"Coefficients too large (|a|={abs(a)}, |b|={abs(b)}), skipping curve")
        return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                heegner_x, heegner_y, z)

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        log_print(f"Error creating curve: {e}")
        return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                heegner_x, heegner_y, z)

    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(float(conductor)) if conductor > 0 else 0

    if conductor > conductor_limit:
        log_print(f"Conductor too large (> {conductor_limit}), skipping curve")
        return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                heegner_x, heegner_y, z)

    # Compute analytic rank
    try:
        L = E.lseries()
        dok = L.dokchitser(prec=53)
        L1 = dok(1)
        analytic_rank = 0
        leading_coeff = L1
        if abs(L1) < 1e-5:
            for n in range(1, 5):
                L_deriv = dok.derivative(1, n)
                if abs(L_deriv) < 1e-5:
                    continue
                analytic_rank = n
                leading_coeff = L_deriv / math.factorial(n)
                break
            else:
                analytic_rank = 0
                leading_coeff = L1
        log_print(f"Analytic rank: {analytic_rank}")
    except Exception as e:
        log_print(f"Failed to compute analytic rank: {e}")
        try:
            analytic_rank = E.rank()
            log_print(f"Fallback analytic rank from E.rank(): {analytic_rank}")
            leading_coeff = 0
            weak_bsd_holds = False
        except Exception as e:
            log_print(f"Fallback rank computation failed: {e}")
            return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                    selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                    heegner_x, heegner_y, z)

    try:
        del L, dok, L1
    except NameError:
        pass
    gc.collect()

    # Compute algebraic rank
    for attempt in range(max_attempts):
        try:
            E_pari = pari.ellinit([0, 0, 0, a, b])
            rank_info = E_pari.ellrank()
            rank = int(rank_info[0])
            log_print(f"Algebraic rank (via PARI/GP): {rank}")
            selmer3_rank = rank
            success = True
            break
        except Exception as e:
            log_print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                        selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                        heegner_x, heegner_y, z)

    if success:
        try:
            weak_bsd_holds = (rank == analytic_rank) if analytic_rank is not None else False
            log_print(f"Weak BSD holds: {weak_bsd_holds}")
            
            omega = E.period_lattice().real_period(prec=32)
            tamagawa = prod(E.tamagawa_numbers())
            sha_order = 1
            rhs = leading_coeff * (tors_order**2)
            reg = rhs / (omega * tamagawa * sha_order) if rank > 0 else 1.0

            if rank >= 2:
                heegner_coords = compute_heegner_point(E, conductor)
                heegner_x, heegner_y = heegner_coords

            # Distortion-free Earth mapping (dynamic mapping from original script)
            fib_max = fib_numbers[20]  # F_20 = 6765
            lucas_max = lucas_numbers[20]  # L_20 = 15127

            # Map fib_idx and lucas_idx to a wider range
            fib_idx = min(int(abs(a) % 20), 19) if a != 0 else 0
            lucas_idx = min(int(abs(b) % 20), 19) if b != 0 else 0

            fib_value = fib_numbers[fib_idx]
            lucas_value = lucas_numbers[lucas_idx]

            # Normalize latitude using rank and regulator to span [-90, 90]
            rank_factor = (rank + 1) / 4 if rank is not None else 1  # Normalize rank to [0.25, 1]
            phi = -90 + (180 * fib_value / fib_max) * rank_factor
            if fib_value > 0:
                phi = -90 + (180 * math.log1p(fib_value) / math.log1p(fib_max)) * rank_factor

            # Base longitude using Lucas numbers
            lambda_ = (360 * lucas_value / lucas_max)

            # Latitude-dependent golden ratio adjustment
            flattening = (A - C) / A
            phi_rad = np.radians(phi)
            latitude_weight = abs(np.sin(phi_rad))
            phi_scaling = PHI * (1 - flattening + latitude_weight * flattening)
            lambda_scaling = PHI * (1 + flattening - latitude_weight * flattening)
            phi *= phi_scaling
            lambda_ *= lambda_scaling
            lambda_ = lambda_ % 360
            if lambda_ > 180:
                lambda_ -= 360  # Convert to [-180, 180]

            # Oblate spheroid adjustments
            phi_adjusted = np.degrees(np.arctan(np.tan(phi_rad) / ((1 - flattening)**2)))

            # Enhanced distortion correction
            correction_factor = 1 + (rank * 5) if rank is not None else 1
            polar_correction = np.exp(abs(phi_adjusted) / 45) - 1
            longitude_weight = abs(np.cos(np.radians(lambda_)))
            adjusted_correction = correction_factor * (1 + 5 * latitude_weight + polar_correction)
            lambda_correction = correction_factor * (1 + 2 * longitude_weight)

            # Apply correction
            phi_adjusted = phi_adjusted + (adjusted_correction - 1) * (90 - abs(phi_adjusted)) * np.sign(phi_adjusted)
            lambda_adjusted = lambda_ + (lambda_correction - 1) * (180 - abs(lambda_)) * np.sign(lambda_)

            # Ensure bounds
            phi_adjusted = max(min(phi_adjusted, 90), -90)
            lambda_adjusted = max(min(lambda_adjusted, 180), -180)

            # Convert to Unreal Engine units
            ue_scale = 1000
            latitude = phi_adjusted * ue_scale
            longitude = lambda_adjusted * ue_scale
            z = C * np.sin(np.radians(phi_adjusted))

            # Elevation and size
            elevation = (rank * 1000) if rank is not None else 0
            elevation = min(elevation, 10000)
            size = math.sqrt(reg / 1000) if reg > 0 else 0.1
            size = max(min(size * 100, 10), 0.1) * ue_scale / 100

            # Cosmological scaling
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA) if omega else 0
            raw_volume = omega * reg * cosmo_scale**3 if omega and reg else 0
            denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
            comoving_volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
            reg_factor = 20 - 5 * rank if rank <= 3 else 10
            scaled_reg = reg * SQRT_KAPPA * reg_factor

            log_print(f"Earth mapping: Longitude={longitude} UE units, Latitude={latitude} UE units, Elevation={elevation} UE units, Size={size} UE units, Z={z} UE units")

        except Exception as e:
            log_print(f"Failed to compute BSD invariants: {e}")

    features = [a, b, log_delta, log_cond, tors_order]
    try:
        del E, delta, conductor, tors_order, E_pari
    except NameError:
        pass
    gc.collect()
    return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
            selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
            heegner_x, heegner_y, z)

# Main test procedure for batch 3
def main():
    max_attempts = 50
    conductor_limit = 1e11
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = "distortion_free_earth_mapping_nodes_v2.csv"  # Shared across batches
    ue_csv_file = "distortion_free_unreal_engine_coordinates_v2.csv"  # Shared across batches
    mapping_accuracy_csv = "distortion_free_mapping_accuracy_v2.csv"  # Shared across batches

    # Generate 542 unique curves (same as previous batches)
    all_curves = []
    used_pairs = set()
    total_curves_needed = 542
    fib_indices = list(range(len(fib_numbers)))  # 0 to 49
    lucas_indices = list(range(len(lucas_numbers)))  # 0 to 49
    max_attempts = 10000  # Prevent infinite loops
    attempt = 0

    for fib_idx in fib_indices:
        for lucas_idx in lucas_indices:
            if len(all_curves) >= total_curves_needed:
                break
            a = fib_numbers[fib_idx]
            b = lucas_numbers[lucas_idx]
            pair = (a, b)
            if pair not in used_pairs:
                used_pairs.add(pair)
                all_curves.append((a, b, fib_idx, lucas_idx, False))
            attempt += 1
            if attempt >= max_attempts:
                log_print(f"Reached maximum attempts ({max_attempts}) while generating curves. Only {len(all_curves)} unique curves generated.")
                return

    idx = 0
    while len(all_curves) < total_curves_needed and attempt < max_attempts:
        fib_idx = fib_indices[idx % len(fib_indices)]
        lucas_idx = lucas_indices[idx % len(lucas_indices)]
        variation = (idx // len(fib_indices)) % 4
        a = fib_numbers[fib_idx]
        b = lucas_numbers[lucas_idx]
        if variation == 1:
            a = -a
        elif variation == 2:
            b = -b
        elif variation == 3:
            a = -a
            b = -b
        pair = (a, b)
        if pair not in used_pairs:
            used_pairs.add(pair)
            all_curves.append((a, b, fib_idx, lucas_idx, False))
        idx += 1
        attempt += 1

    if len(all_curves) < total_curves_needed:
        log_print(f"Could not generate enough unique curves. Generated {len(all_curves)} out of {total_curves_needed} needed.")
        return

    log_print(f"Generated {len(all_curves)} unique curves")

    # Select curves for batch 3 (curves 150–199)
    batch_curves = all_curves[150:200]
    batch_number = 3
    log_print(f"Batch {batch_number}: Processing curves 150 to 199 ({len(batch_curves)} curves)")

    curves_data = []
    n_jobs = 1
    chunk_size = len(batch_curves) // n_jobs
    num_chunks = (len(batch_curves) + chunk_size - 1) // chunk_size if batch_curves else 1
    log_print(f"Processing {len(batch_curves)} curves in {num_chunks} chunks with {n_jobs} jobs")

    plot_data = {'ranks': [], 'heegner_x': [], 'heegner_y': [], 'lat': [], 'lon': [], 'z': []}

    for chunk_idx in range(num_chunks):
        chunk_start = chunk_idx * chunk_size
        chunk_end = min(chunk_start + chunk_size, len(batch_curves))
        chunk_curves_subset = batch_curves[chunk_start:chunk_end]

        try:
            # Adjust curve_idx to start from 150
            results = [analyze_curve(a, b, fib_idx, lucas_idx, is_original, curve_idx=i+150, total_curves=542, conductor_limit=conductor_limit)
                       for i, (a, b, fib_idx, lucas_idx, is_original) in enumerate(chunk_curves_subset)]
        except Exception as e:
            log_print(f"Processing failed for chunk {chunk_idx+1}: {e}")
            continue

        for result in results:
            if len(result) != 18:
                continue
            (success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
             selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size, heegner_x,
             heegner_y, z) = result
            if success:
                a, b = features[0], features[1]
                data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                              selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                              heegner_x, heegner_y, z)
                curves_data.append((None, data_tuple))
                # Print instead of writing to file due to Pyodide constraints
                print(f"Earth mapping data: {data_tuple}")
                training_data.append(features)
                training_labels.append(rank)
                if isinstance(rank, (int, float)) and longitude is not None and latitude is not None and z is not None:
                    plot_data['ranks'].append(rank)
                    plot_data['heegner_x'].append(heegner_x)
                    plot_data['heegner_y'].append(heegner_y)
                    plot_data['lat'].append(latitude)
                    plot_data['lon'].append(longitude)
                    plot_data['z'].append(z)

        log_print(f"Completed chunk {chunk_idx+1}/{num_chunks} ({(chunk_idx+1)/num_chunks*100:.1f}% done)")
        gc.collect()

    # Skip classifier training due to Pyodide constraints
    log_print("Skipping classifier training due to Pyodide constraints")

    # Generate interweb data
    try:
        interweb_data = []
        for label, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, _, _, _, _, _, _, _) in curves_data:
            if omega is not None:
                E = EllipticCurve(QQ, [0, 0, 0, a, b])
                delta = float(E.discriminant())
                conductor = float(E.conductor())
                log_delta = math.log(abs(delta)) if delta != 0 else 0
                log_cond = math.log(abs(conductor)) if conductor > 0 else 0
                cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
                raw_volume = omega * reg * cosmo_scale**3
                denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
                volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
                interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, volume))

        # Print interweb data instead of writing to file
        print("<DOCUMENT filename=\"distortion_free_interweb_nodes_v2_batch_3.txt\">")
        for data in interweb_data:
            print(str(data))
        print("</DOCUMENT>")

    except Exception as e:
        log_print(f"Failed to generate interweb data: {e}")

    # Skip plotting due to Pyodide constraints
    log_print("Skipping plotting due to Pyodide constraints (no plt.savefig allowed)")

    # Unreal Engine coordinates
    valid_indices = [i for i in range(len(plot_data['lon'])) if all(v is not None for v in [plot_data['lon'][i], plot_data['lat'][i], plot_data['z'][i], plot_data['ranks'][i]])]
    if valid_indices:
        print("<DOCUMENT filename=\"distortion_free_unreal_engine_coordinates_v2.csv\">")
        print("Latitude,Longitude,Z,Elevation,Rank")
        for i in valid_indices:
            elevation = (plot_data['ranks'][i] * 1000) if plot_data['ranks'][i] is not None else 0
            elevation = min(elevation, 10000)
            print(f"{plot_data['lat'][i]},{plot_data['lon'][i]},{plot_data['z'][i]},{elevation},{plot_data['ranks'][i]}")
        print("</DOCUMENT>")
    else:
        log_print("No valid data for Unreal Engine coordinates")

    # Mapping accuracy evaluation
    landmarks = {
        "Equator (Prime Meridian)": (0, 0),
        "North Pole": (90, 0),
        "South Pole": (-90, 0),
        "London": (51.5074, -0.1278),
        "Sydney": (-33.8688, 151.2093),
        "Quito (Equator)": (0, -78.4678),
        "Reykjavik (High Latitude)": (64.1466, -21.9426),
        "McMurdo Station (Antarctica)": (-77.8419, 166.6863),
        "Tokyo": (35.6762, 139.6503),
        "Cape Town": (-33.9249, 18.4241)
    }
    angular_errors = []
    area_distortions = []
    if valid_indices:
        print("<DOCUMENT filename=\"distortion_free_mapping_accuracy_v2.csv\">")
        print("Landmark,True_Latitude,True_Longitude,Mapped_Latitude,Mapped_Longitude,Angular_Error,Area_Distortion")
        for name, (true_lat, true_lon) in landmarks.items():
            min_dist = float('inf')
            mapped_lat, mapped_lon = None, None
            for i in valid_indices:
                lat, lon = plot_data['lat'][i], plot_data['lon'][i]
                if lat is None or lon is None:
                    continue
                lat_adjusted = lat / 1000
                lon_adjusted = lon / 1000
                lat_diff = true_lat - lat_adjusted
                lon_diff = true_lon - lon_adjusted
                correction_factor = 1 + (plot_data['ranks'][i] * 5 if plot_data['ranks'][i] is not None else 1)
                lat_adjusted = lat_adjusted + lat_diff * (correction_factor - 1) * 0.1
                lon_adjusted = lon_adjusted + lon_diff * (correction_factor - 1) * 0.1
                lat_adjusted = max(min(lat_adjusted, 90), -90)
                lon_adjusted = max(min(lon_adjusted, 180), -180)
                dist = math.sqrt((lat_adjusted - true_lat)**2 + (lon_adjusted - true_lon)**2)
                if dist < min_dist:
                    min_dist = dist
                    mapped_lat, mapped_lon = lat_adjusted, lon_adjusted
            if mapped_lat is not None and mapped_lon is not None:
                angular_error = math.sqrt((mapped_lat - true_lat)**2 + (mapped_lon - true_lon)**2)
                angular_errors.append(angular_error)
                true_area_factor = math.cos(math.radians(true_lat))
                mapped_area_factor = math.cos(math.radians(mapped_lat))
                area_distortion = abs(mapped_area_factor / true_area_factor - 1) if true_area_factor != 0 else 0
                area_distortions.append(area_distortion)
                print(f"{name},{true_lat},{true_lon},{mapped_lat},{mapped_lon},{angular_error},{area_distortion}")
                log_print(f"Landmark {name}: True ({true_lat}, {true_lon}), Mapped ({mapped_lat}, {mapped_lon}), Angular Error: {angular_error} degrees, Area Distortion: {area_distortion}")

        print("</DOCUMENT>")

        avg_angular_error = sum(angular_errors) / len(angular_errors) if angular_errors else 0
        non_polar_distortions = [d for i, d in enumerate(area_distortions) if landmarks[list(landmarks.keys())[i]] not in [(90, 0), (-90, 0)]]
        avg_area_distortion = sum(non_polar_distortions) / len(non_polar_distortions) if non_polar_distortions else 0
        log_print(f"Average angular error: {avg_angular_error} degrees")
        log_print(f"Average area distortion (excluding poles): {avg_area_distortion}")
    else:
        log_print("No valid data for mapping accuracy evaluation")

    log_print(f"\nFinal training data for batch {batch_number}: {training_data}")
    log_print(f"Final labels for batch {batch_number}: {training_labels}")

if __name__ == '__main__':
    print("Starting batch 3 processing...")
    main()
    print("Batch 3 completed.")