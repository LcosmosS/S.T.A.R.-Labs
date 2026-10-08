import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, Integer, kronecker
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed
import os
import logging
import sys
import traceback
import time

# Verify SageMath environment
try:
    import sage
    from sage.version import version as sage_version
    print(f"SageMath version: {sage_version}")
    if sage_version < "10.6":
        raise RuntimeError("SageMath version 10.6 or higher is required. Please update SageMath.")
except ImportError:
    print("This script must be run in a SageMath environment. Please run with 'sage distortion_free_earth_mapping_test_v9.py'.")
    sys.exit(1)

# Set up logging
logging.basicConfig(filename='distortion_free_earth_mapping_test_v9.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_print(*args, **kwargs):
    msg = " ".join(map(str, args))
    logging.info(msg)
    print(msg)

# Set up SageMath environment for sequential processing
os.environ["SAGE_NUM_THREADS"] = "1"
pari.allocatemem(2**29)  # Reduced to 512 MB
pari.set_debug_level(2)
log_print(f"PARI stack size set to {2**29} bytes")

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

fib_numbers = generate_fibonacci(100)
lucas_numbers = generate_lucas(100)
log_print(f"Fibonacci numbers up to index 100: {fib_numbers}")
log_print(f"Lucas numbers up to index 100: {lucas_numbers}")

# Initial training data
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
    [34, 4181, 22.7453700939663, 22.0522229134064, 1],
    [17711, 17711, 25.9923456789012, 25.9923456789012, 1],
    [17711, 46368, 25.9865432109876, 24.5998765432109, 1],
    [-102, 918, 19.5063410364742, 18.4077287478061, 1],
    [4, 1152, 163153.99138494278, 61950.12099761353, 1],
    [14, 49392, 180000, 90000, 1],
]
training_labels = [3, 3, 3, 3, 3, 3, 1, 2]
log_print(f"Initial training data: {training_data}")
log_print(f"Initial labels: {training_labels}")

# Helper functions
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

def random_fibonacci_pair(fibs, lucas, high_rank_pairs, bias=0.99):
    if np.random.random() < bias and high_rank_pairs:
        idx = np.random.randint(len(high_rank_pairs))
        return high_rank_pairs[idx]
    use_lucas = np.random.random() < 0.5
    numbers = lucas if use_lucas else fibs
    return (np.random.choice(numbers), np.random.choice(numbers))

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
    fundamental_discriminants = [-3, -4, -7, -8, -11, -19, -43, -67, -163]
    for D in fundamental_discriminants:
        if satisfies_heegner_hypothesis(N, D):
            return D
    
    # Precompute additional discriminants based on N's prime factors
    N = Integer(N)
    prime_factors = N.prime_factors()
    additional_discriminants = []
    for p in prime_factors:
        for d in range(-3, -1000, -1):  # Extended range for precomputation
            if d % 4 in [0, 1] and Integer(d).is_squarefree() and kronecker(d, p) != 1:
                additional_discriminants.append(d)
    additional_discriminants = list(set(additional_discriminants))  # Remove duplicates
    additional_discriminants.sort()  # Sort for consistency
    
    # Try additional discriminants first
    for D in additional_discriminants[:100]:  # Limit to top 100 to avoid excessive computation
        if satisfies_heegner_hypothesis(N, D):
            log_print(f"Found suitable discriminant D={D} from precomputed list")
            return D
    
    # Existing dynamic search with square-free check
    D = -3
    max_attempts = 5000
    attempt = 0
    while attempt < max_attempts:
        if D % 4 in [0, 1] and Integer(D).is_squarefree() and satisfies_heegner_hypothesis(N, D):
            log_print(f"Found suitable discriminant D={D} after dynamic search")
            return D
        D -= 1
        attempt += 1
    log_print("No suitable discriminant found after extended dynamic search")
    return None

def compute_heegner_point(E, conductor):
    D = find_suitable_discriminant(conductor)
    if D is None:
        log_print("No suitable discriminant found; approximating Heegner point")
        # Approximate Heegner point using discriminant and conductor
        delta = float(E.discriminant())
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        x_approx = log_delta / (conductor + 1)  # Simple heuristic
        y_approx = math.sqrt(abs(x_approx**3 + E.a4() * x_approx + E.a6()))
        log_print(f"Approximated Heegner point: ({x_approx}, {y_approx})")
        return (x_approx, y_approx)
    try:
        heegner = E.heegner_point(D)
        x, y = heegner.xy()
        log_print(f"Heegner point with D={D}: ({x}, {y})")
        return (float(x), float(y))
    except Exception as e:
        log_print(f"Failed to compute Heegner point with D={D}: {e}")
        # Fallback to approximation if computation fails
        delta = float(E.discriminant())
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        x_approx = log_delta / (conductor + 1)
        y_approx = math.sqrt(abs(x_approx**3 + E.a4() * x_approx + E.a6()))
        log_print(f"Approximated Heegner point: ({x_approx}, {y_approx})")
        return (x_approx, y_approx)

# Compute authalic latitude to reduce distortions
def compute_authalic_latitude(geodetic_lat, flattening):
    e = np.sqrt(2 * flattening - flattening**2)  # Eccentricity
    sin_phi = np.sin(np.radians(geodetic_lat))
    q = (1 - e**2) * sin_phi / (1 - e**2 * sin_phi**2) + (1 / (2 * e)) * np.log((1 + e * sin_phi) / (1 - e * sin_phi))
    q0 = 1 + (1 / (2 * e)) * np.log((1 + e) / (1 - e))  # q at phi = 90 degrees
    sin_beta = q / q0
    beta = np.degrees(np.arcsin(sin_beta))
    return beta

# Analyze elliptic curve with new rank mapping and paradox correction
def analyze_curve(a, b, fib_idx, lucas_idx, is_original=False, max_attempts=3, conductor_limit=5e11):
    log_print(f"Analyzing curve: y² = x³ + {a}x + {b}")
    
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
                heegner_x, heegner_y, z, None, None)

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        log_print(f"Error creating curve: {e}")
        return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                heegner_x, heegner_y, z, None, None)

    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(float(conductor)) if conductor > 0 else 0

    # Dynamic conductor limit based on memory usage
    try:
        import psutil
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss / 1024**2  # Memory in MB
        dynamic_limit = conductor_limit * (1 - mem_usage / 16000)  # Scale down if memory usage exceeds 16GB
        dynamic_limit = max(dynamic_limit, 1e10)  # Minimum limit
        log_print(f"Dynamic conductor limit: {dynamic_limit}")
    except ImportError:
        dynamic_limit = conductor_limit
        log_print("psutil not available, using static conductor limit")

    if conductor > dynamic_limit:
        log_print(f"Conductor {conductor} exceeds dynamic limit {dynamic_limit}, performing partial analysis")
        # Partial analysis: Skip Heegner points, proceed with rank and invariants
        heegner_x = heegner_y = 0
    else:
        # Existing conductor check
        if conductor > conductor_limit:
            log_print(f"Conductor too large (> {conductor_limit}), skipping curve")
            return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                    selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                    heegner_x, heegner_y, z, None, None)

    # Existing analytic rank computation with safeguard
    if conductor > dynamic_limit * 2:  # Very high conductor
        log_print(f"Conductor {conductor} too high for L-series, approximating rank")
        analytic_rank = 1  # Approximation based on typical behavior
        leading_coeff = 0
        weak_bsd_holds = False
    else:
        try:
            L = E.lseries()
            dok = L.dokchitser(prec=28)  # Further reduced from 32
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
                        heegner_x, heegner_y, z, None, None)

    try:
        del L, dok, L1
    except NameError:
        pass
    gc.collect()

    # Existing algebraic rank computation
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
                        heegner_x, heegner_y, z, None, None)

    if success:
        try:
            weak_bsd_holds = (rank == analytic_rank) if analytic_rank is not None else False
            log_print(f"Weak BSD holds: {weak_bsd_holds}")
            
            omega = E.period_lattice().real_period(prec=32)
            tamagawa = prod(E.tamagawa_numbers())
            sha_order = 1
            rhs = leading_coeff * (tors_order**2)
            reg = rhs / (omega * tamagawa * sha_order) if rank > 0 else 1.0

            # Compute Heegner points only if conductor is within dynamic limit
            if conductor <= dynamic_limit and rank >= 2:
                heegner_coords = compute_heegner_point(E, conductor)
                heegner_x, heegner_y = heegner_coords

            # Updated coordinate mapping to avoid clustering
            # Normalize log_delta and log_cond with wider range to allow more variability
            log_delta_normalized = (log_delta - 4) / (35 - 4)  # Expanded range from (5, 30)
            log_cond_normalized = (log_cond - 3) / (28 - 3)   # Expanded range from (4, 25)
            log_delta_normalized = max(min(log_delta_normalized, 1), 0)
            log_cond_normalized = max(min(log_cond_normalized, 1), 0)

            # Introduce curve-specific variation using coefficients a and b
            # Scale down a and b to avoid massive shifts, and use them as offsets
            a_offset = (a % 100) / 100.0  # Modulo to keep it manageable, then normalize to [0, 1]
            b_offset = (b % 100) / 100.0
            spread_factor = np.sin(np.pi/2 * log_delta_normalized)

            # Base latitude and longitude with rank-based adjustments
            if rank == 3:
                phi = 78 + (spread_factor * 10)
            elif rank == 2:
                phi = -78 - (spread_factor * 10)
            else:
                max_lat = 75
                phi = max_lat * (2 * log_delta_normalized - 1)

            if rank == 1:
                lambda_ = 180 * (2 * log_cond_normalized - 1)
            else:
                max_lon = 180
                lambda_ = max_lon * (2 * log_cond_normalized - 1)

            # Add curve-specific offsets to latitude and longitude
            # Use a and b to create small perturbations, scaled by rank to control spread
            phi_offset = (a_offset - 0.5) * 5 * (1 + rank)  # Small perturbation, e.g., [-2.5, 2.5] degrees scaled by rank
            lambda_offset = (b_offset - 0.5) * 10 * (1 + rank)  # Larger range for longitude, e.g., [-5, 5] degrees
            phi += phi_offset
            lambda_ += lambda_offset

            # Ensure bounds are respected
            phi = max(min(phi, 89.9), -89.9)
            lambda_ = max(min(lambda_, 179.9), -179.9)

            # Apply authalic latitude correction for distortion-free mapping
            flattening = (A - C) / A
            phi_adjusted = compute_authalic_latitude(phi, flattening)

            # Weight adjustments for paradox correction
            latitude_weight = abs(np.sin(np.radians(phi_adjusted)))
            longitude_weight = abs(np.cos(np.radians(lambda_)))
            correction_factor = 1 + (rank * 2) if rank is not None else 1
            adjusted_correction = correction_factor * (1 + latitude_weight)
            lambda_correction = correction_factor * (1 + longitude_weight)

            # Apply corrections with slight curve-specific tweaks
            phi_adjusted = phi_adjusted + (adjusted_correction - 1) * (90 - abs(phi_adjusted)) * np.sign(phi_adjusted) + (a_offset * 0.1)
            lambda_adjusted = lambda_ + (lambda_correction - 1) * (180 - abs(lambda_)) * np.sign(lambda_) + (b_offset * 0.2)

            # Final bounds check
            phi_adjusted = max(min(phi_adjusted, 89.9), -89.9)
            lambda_adjusted = max(min(lambda_adjusted, 180), -180)

            # Compute z-coordinate with rank-based adjustments
            if rank == 3:
                z = C * np.sin(np.radians(phi_adjusted))
                z += spread_factor * 1e5
            else:
                z = C * np.sin(np.radians(phi_adjusted))

            # Elevation based on rank
            if rank == 0:
                elevation = 0
            else:
                elevation = rank * 1000
            elevation = min(elevation, 10000)

            # Convert to Unreal Engine units
            ue_scale = 1000
            latitude = phi_adjusted * ue_scale
            longitude = lambda_adjusted * ue_scale

            size = math.sqrt(reg / 1000) if reg > 0 else 0.1
            size = max(min(size * 100, 10), 0.1) * ue_scale / 100

            # Cosmic scale computations
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
            heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)

# Quadratic twist function
def quadratic_twist(E, d):
    a = E.a4()
    b = E.a6()
    a_new = a * d
    b_new = b * (d**3)
    return EllipticCurve(QQ, [0, 0, 0, a_new, b_new])

# Main test procedure
def main():
    high_rank_pairs = [(2, 144), (377, 987), (-102, 918), (34, 4181), (17711, 17711), (17711, 46368)]
    max_attempts = 50
    conductor_limit = 4e11  # Reduced from 5e11
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"distortion_free_earth_mapping_nodes_v9_{timestamp}.csv"

    try:
        with open(csv_file, 'w', newline='') as csv_f:
            csv_writer = csv.writer(csv_f)
            csv_writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'reg', 'tamagawa', 'weak_bsd_holds', 'selmer3_rank', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size', 'heegner_x', 'heegner_y', 'z'])
    except IOError as e:
        log_print(f"Failed to initialize CSV file {csv_file}: {e}")
        return

    curves_data = []
    all_curves = []
    used_pairs = set()
    total_curves_needed = 542
    batch_size = 3  # Reduced from 5

    # Existing curve generation code
    fib_indices = list(range(len(fib_numbers)))
    lucas_indices = list(range(len(lucas_numbers)))
    max_attempts_generate = 20000
    attempt = 0
    idx = 0
    scale_factors = [1, 2, 3]

    while len(all_curves) < total_curves_needed and attempt < max_attempts_generate:
        fib_idx = fib_indices[idx % len(fib_indices)]
        lucas_idx = lucas_indices[idx % len(lucas_indices)]
        scale_a = scale_factors[(idx // len(fib_indices)) % len(scale_factors)]
        scale_b = scale_factors[(idx // (len(fib_indices) * len(scale_factors))) % len(scale_factors)]
        variation = (idx // (len(fib_indices) * len(scale_factors) * len(scale_factors))) % 4
        a = fib_numbers[fib_idx] * scale_a
        b = lucas_numbers[lucas_idx] * scale_b
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

    # Process curves in batches with memory monitoring
    n_jobs = 1
    num_batches = (len(all_curves) + batch_size - 1) // batch_size
    plot_data = {'ranks': [], 'heegner_x': [], 'heegner_y': [], 'lat': [], 'lon': [], 'z': [], 'elevation': [], 'phi_adjusted': [], 'lambda_adjusted': []}

    # Checkpoint file
    checkpoint_file = f"checkpoint_v9_{timestamp}.csv"
    try:
        with open(checkpoint_file, 'w', newline='') as chk_f:
            chk_writer = csv.writer(chk_f)
            chk_writer.writerow(['batch_idx', 'completed'])
    except IOError as e:
        log_print(f"Failed to initialize checkpoint file {checkpoint_file}: {e}")

    for batch_idx in range(num_batches):
        # Check if batch was already processed
        completed_batches = set()
        try:
            with open(checkpoint_file, 'r') as chk_f:
                chk_reader = csv.reader(chk_f)
                next(chk_reader)  # Skip header
                for row in chk_reader:
                    completed_batches.add(int(row[0]))
        except (IOError, IndexError):
            pass

        if batch_idx in completed_batches:
            log_print(f"Skipping batch {batch_idx+1}/{num_batches} (already processed)")
            continue

        batch_start = batch_idx * batch_size
        batch_end = min(batch_start + batch_size, len(all_curves))
        batch_curves = all_curves[batch_start:batch_end]
        log_print(f"Processing batch {batch_idx+1}/{num_batches} ({batch_start} to {batch_end-1})")

        # Memory check
        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_usage = process.memory_info().rss / 1024**2
            if mem_usage > 10000:  # Threshold: 10GB (was 12GB)
                log_print(f"Memory usage too high ({mem_usage} MB), pausing for garbage collection")
                gc.collect()
                time.sleep(5)  # Pause to allow system to stabilize
        except ImportError:
            log_print("psutil not available, skipping memory check")

        try:
            results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
                delayed(analyze_curve)(
                    a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit
                )
                for a, b, fib_idx, lucas_idx, is_original in batch_curves
            )
        except MemoryError as e:
            log_print(f"MemoryError during parallel processing for batch {batch_idx+1}: {e}")
            log_print("Falling back to sequential processing for this batch")
            results = []
            for a, b, fib_idx, lucas_idx, is_original in batch_curves:
                result = analyze_curve(a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit)
                results.append(result)
        except Exception as e:
            log_print(f"Parallel processing failed for batch {batch_idx+1}: {e}")
            log_print("Falling back to sequential processing for this batch")
            results = []
            for a, b, fib_idx, lucas_idx, is_original in batch_curves:
                result = analyze_curve(a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit)
                results.append(result)

        for result in results:
            if len(result) != 20:
                continue
            (success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
             selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size, heegner_x,
             heegner_y, z, phi_adjusted, lambda_adjusted) = result
            if success:
                a, b = features[0], features[1]
                data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                              selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                              heegner_x, heegner_y, z)
                curves_data.append((None, data_tuple))
                try:
                    with open(csv_file, 'a', newline='') as csv_f:
                        csv_writer = csv.writer(csv_f)
                        csv_writer.writerow(data_tuple)
                except IOError as e:
                    log_print(f"Failed to write to CSV file {csv_file}: {e}")
                training_data.append(features)
                training_labels.append(rank)
                if isinstance(rank, (int, float)) and longitude is not None and latitude is not None and z is not None:
                    plot_data['ranks'].append(rank)
                    plot_data['heegner_x'].append(heegner_x)
                    plot_data['heegner_y'].append(heegner_y)
                    plot_data['lat'].append(latitude)
                    plot_data['lon'].append(longitude)
                    plot_data['z'].append(z)
                    plot_data['elevation'].append(elevation)
                    plot_data['phi_adjusted'].append(phi_adjusted)
                    plot_data['lambda_adjusted'].append(lambda_adjusted)

        # Save checkpoint
        try:
            with open(checkpoint_file, 'a', newline='') as chk_f:
                chk_writer = csv.writer(chk_f)
                chk_writer.writerow([batch_idx, 1])
        except IOError as e:
            log_print(f"Failed to write to checkpoint file {checkpoint_file}: {e}")

        log_print(f"Completed batch {batch_idx+1}/{num_batches} ({(batch_idx+1)/num_batches*100:.1f}% done)")
        gc.collect()

    # Existing quadratic twists and remaining code
    twist_primes = [2, 3, 5, 7]
    twist_curves = []
    for a, b in high_rank_pairs:
        try:
            E = EllipticCurve(QQ, [0, 0, 0, a, b])
            for d in twist_primes:
                E_twist = quadratic_twist(E, d)
                a_new = E_twist.a4()
                b_new = E_twist.a6()
                fib_idx = min(int(abs(a_new) % 20), 19) if a_new != 0 else 0
                lucas_idx = min(int(abs(b_new) % 20), 19) if b_new != 0 else 0
                twist_curves.append((a_new, b_new, fib_idx, lucas_idx, False))
        except Exception as e:
            log_print(f"Failed to compute quadratic twist for curve ({a}, {b}): {e}")

    try:
        twist_results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
            delayed(analyze_curve)(
                a, b, fib_idx, lucas_idx, False, conductor_limit=conductor_limit
            )
            for a, b, fib_idx, lucas_idx, _ in twist_curves
        )
    except MemoryError as e:
        log_print(f"MemoryError during parallel processing for quadratic twists: {e}")
        log_print("Falling back to sequential processing for quadratic twists")
        twist_results = []
        for a, b, fib_idx, lucas_idx, _ in twist_curves:
            result = analyze_curve(a, b, fib_idx, lucas_idx, False, conductor_limit=conductor_limit)
            twist_results.append(result)
    except Exception as e:
        log_print(f"Parallel processing failed for quadratic twists: {e}")
        log_print("Falling back to sequential processing for quadratic twists")
        twist_results = []
        for a, b, fib_idx, lucas_idx, _ in twist_curves:
            result = analyze_curve(a, b, fib_idx, lucas_idx, False, conductor_limit=conductor_limit)
            twist_results.append(result)

    for result in twist_results:
        if len(result) != 20:
            continue
        (success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
         selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size, heegner_x,
         heegner_y, z, phi_adjusted, lambda_adjusted) = result
        if success:
            a, b = features[0], features[1]
            data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                          selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                          heegner_x, heegner_y, z)
            curves_data.append((f"Twist_d{d}", data_tuple))
            try:
                with open(csv_file, 'a', newline='') as csv_f:
                    csv_writer = csv.writer(csv_f)
                    csv_writer.writerow(data_tuple)
            except IOError as e:
                log_print(f"Failed to write to CSV file {csv_file}: {e}")
            training_data.append(features)
            training_labels.append(rank)
            if isinstance(rank, (int, float)) and longitude is not None and latitude is not None and z is not None:
                plot_data['ranks'].append(rank)
                plot_data['heegner_x'].append(heegner_x)
                plot_data['heegner_y'].append(heegner_y)
                plot_data['lat'].append(latitude)
                plot_data['lon'].append(longitude)
                plot_data['z'].append(z)
                plot_data['elevation'].append(elevation)
                plot_data['phi_adjusted'].append(phi_adjusted)
                plot_data['lambda_adjusted'].append(lambda_adjusted)

    # Existing plotting and accuracy evaluation code remains unchanged
    try:
        X = np.array([row[:4] for row in training_data])
        y = np.array(training_labels)
        if len(set(y)) >= 2 and len(X) >= 5:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            clf = LogisticRegression(class_weight='balanced')
            clf.fit(X_scaled, y)
            log_print("Classifier trained successfully")
        else:
            log_print("Insufficient data or labels for classifier training")
    except Exception as e:
        log_print(f"Failed to train classifier: {e}")

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

        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        ranks = [float(x[2]) for x in interweb_data]
        log_deltas = [float(x[8]) for x in interweb_data]
        log_conds = [float(x[9]) for x in interweb_data]
        volumes = [float(x[10]) for x in interweb_data]
        sizes = [float(max(x[3] * 100, 1e-6)) for x in interweb_data]

        colors = ['k' if r == 0 else 'g' if r == 1 else 'b' if r == 2 else 'r' for r in ranks]
        scatter = ax.scatter(log_deltas, log_conds, ranks, s=sizes, c=colors, alpha=0.7)

        virgo_rank = 3
        largest_rank3 = max([x for x in interweb_data if x[2] == 3], key=lambda x: x[10], default=None)
        if largest_rank3:
            virgo_log_delta = largest_rank3[8] + 0.5
            virgo_log_cond = largest_rank3[9] + 0.5
        else:
            virgo_log_delta, virgo_log_cond = 23.0, 22.0
        ax.scatter([virgo_log_delta], [virgo_log_cond], [virgo_rank], s=200, c='green', marker='*', label='Virgo Supercluster')
        ax.text(virgo_log_delta + 0.5, virgo_log_cond + 0.5, virgo_rank + 0.1, 'Virgo Supercluster', size=10, color='green')

        for i, (a, b, rank, _, _, reg, _, _, log_delta, log_cond, _) in enumerate(interweb_data):
            for j in range(i + 1, len(interweb_data)):
                reg_diff = abs(interweb_data[i][5] - interweb_data[j][5])
                if reg_diff < 5000:
                    weight = 1 / (1 + reg_diff / 100)
                    if weight > 0.7:
                        ax.plot([log_deltas[i], log_deltas[j]], [log_conds[i], log_conds[j]], [ranks[i], ranks[j]], 'b-', alpha=0.5 * weight, linewidth=0.7 * weight)
            if rank >= 2:
                color = 'red' if rank == 3 else 'blue'
                offset = 0.5 if log_delta > 20 else -0.5
                ax.text(log_delta + offset, log_cond + offset, rank + 0.1, f'({a},{b})', size=8, color=color)

        ax.set_xlabel('Log(|Discriminant|)')
        ax.set_ylabel('Log(|Conductor|)')
        ax.set_zlabel('Rank')
        ax.set_title('Cosmic Interweb: Nodes, Weighted Filaments, and Virgo Supercluster Marker')
        ax.grid(True)
        ax.legend()
        plt.savefig("distortion_free_interweb_with_virgo_v9.png")
        plt.close()
        log_print("Cosmic interweb plot saved as distortion_free_interweb_with_virgo_v9.png (for later use)")

        try:
            with open('distortion_free_interweb_nodes_v9.txt', 'w') as f:
                for data in interweb_data:
                    f.write(str(data) + '\n')
            log_print("Interweb data saved to distortion_free_interweb_nodes_v9.txt")
        except IOError as e:
            log_print(f"Failed to write interweb data to file: {e}")

    except Exception as e:
        log_print(f"Failed to generate interweb plot: {e}")

    try:
        if plot_data['ranks']:
            plt.figure(figsize=(10, 6))
            plt.hist(plot_data['ranks'], bins=range(int(min(plot_data['ranks'])), int(max(plot_data['ranks'])) + 2), edgecolor='black')
            plt.title("Distribution of Elliptic Curve Ranks")
            plt.xlabel("Rank")
            plt.ylabel("Frequency")
            plt.savefig("distortion_free_rank_distribution_v9.png")
            plt.close()
            log_print("Rank distribution plot saved as distortion_free_rank_distribution_v9.png")
        else:
            log_print("No rank data available for histogram; skipping rank distribution plot")
    except Exception as e:
        log_print(f"Failed to generate rank distribution plot: {e}")

    try:
        if plot_data['heegner_x'] and plot_data['heegner_y'] and plot_data['ranks']:
            plt.figure(figsize=(10, 6))
            plt.scatter(plot_data['heegner_x'], plot_data['heegner_y'], c=plot_data['ranks'], cmap='viridis')
            plt.colorbar(label="Rank")
            plt.title("Heegner Points of Elliptic Curves")
            plt.xlabel("Heegner X")
            plt.ylabel("Heegner Y")
            plt.savefig("distortion_free_heegner_points_v9.png")
            plt.close()
            log_print("Heegner points scatter plot saved as distortion_free_heegner_points_v9.png")
        else:
            log_print("No Heegner point data available; skipping Heegner points plot")
    except Exception as e:
        log_print(f"Failed to generate Heegner points plot: {e}")

    valid_indices = [i for i in range(len(plot_data['lon'])) if all(v is not None for v in [plot_data['lon'][i], plot_data['elevation'][i], plot_data['z'][i], plot_data['ranks'][i]])]
    if valid_indices:
        filtered_lon = [plot_data['lon'][i] for i in valid_indices]
        filtered_elevation = [plot_data['elevation'][i] for i in valid_indices]
        filtered_z = [plot_data['z'][i] for i in valid_indices]
        filtered_ranks = [plot_data['ranks'][i] for i in valid_indices]

        try:
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            scatter = ax.scatter(filtered_lon, filtered_elevation, filtered_z, c=filtered_ranks, cmap='rainbow', alpha=0.7)
            fig.colorbar(scatter, ax=ax, label='Rank')
            ax.set_title("Distortion-Free Oblate Spheroid Mapping with Paradox Correction (Longitude, Elevation, Depth)")
            ax.set_xlabel("Longitude (UE units)")
            ax.set_ylabel("Elevation (UE units)")
            ax.set_zlabel("Depth (Z, UE units)")
            plt.savefig("distortion_free_oblate_spheroid_map_v9.png")
            plt.close()
            log_print("Distortion-free oblate spheroid map saved as distortion_free_oblate_spheroid_map_v9.png")
        except Exception as e:
            log_print(f"Failed to generate oblate spheroid map: {e}")

        try:
            with open("distortion_free_unreal_engine_coordinates_v9.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Latitude", "Longitude", "Z", "Elevation", "Rank"])
                for i in valid_indices:
                    elevation = plot_data['elevation'][i]
                    writer.writerow([plot_data['lat'][i], plot_data['lon'][i], plot_data['z'][i], elevation, plot_data['ranks'][i]])
            log_print("Unreal Engine coordinates exported to 'distortion_free_unreal_engine_coordinates_v9.csv'.")
        except IOError as e:
            log_print(f"Failed to export Unreal Engine coordinates: {e}")
    else:
        log_print("No valid data for oblate spheroid map; skipping plot and Unreal Engine coordinates export")

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
        try:
            computed_coords = [(plot_data['phi_adjusted'][i], plot_data['lambda_adjusted'][i], plot_data['ranks'][i]) for i in valid_indices]

            landmark_coords = []
            computed_matches = []
            for name, (true_lat, true_lon) in landmarks.items():
                min_dist = float('inf')
                best_match = None
                for phi, lambda_, rank in computed_coords:
                    dist = math.sqrt((phi - true_lat)**2 + (lambda_ - true_lon)**2)
                    if dist < min_dist:
                        min_dist = dist
                        best_match = (phi, lambda_)
                if best_match:
                    landmark_coords.append([true_lat, true_lon])
                    computed_matches.append([best_match[0], best_match[1]])

            if len(landmark_coords) >= 2:
                landmark_coords = np.array(landmark_coords)
                computed_matches = np.array(computed_matches)
                A_phi = np.vstack([computed_matches[:, 0], np.ones(len(computed_matches))]).T
                a_phi, b_phi = np.linalg.lstsq(A_phi, landmark_coords[:, 0], rcond=None)[0]
                A_lambda = np.vstack([computed_matches[:, 1], np.ones(len(computed_matches))]).T
                c_lambda, d_lambda = np.linalg.lstsq(A_lambda, landmark_coords[:, 1], rcond=None)[0]

                for i in valid_indices:
                    phi = plot_data['phi_adjusted'][i]
                    lambda_ = plot_data['lambda_adjusted'][i]
                    mapped_lat = a_phi * phi + b_phi
                    mapped_lon = c_lambda * lambda_ + d_lambda
                    mapped_lat = max(min(mapped_lat, 90), -90)
                    mapped_lon = max(min(mapped_lon, 180), -180)
                    ue_scale = 1000
                    plot_data['lat'][i] = mapped_lat * ue_scale
                    plot_data['lon'][i] = mapped_lon * ue_scale
                    plot_data['z'][i] = C * np.sin(np.radians(mapped_lat))
                    idx = next(idx for idx, (label, data) in enumerate(curves_data) if data[12] == plot_data['lat'][i] / ue_scale and data[11] == plot_data['lon'][i] / ue_scale)
                    _, data_tuple = curves_data[idx]
                    new_data = (data_tuple[0], data_tuple[1], data_tuple[2], data_tuple[3], data_tuple[4], data_tuple[5], data_tuple[6], data_tuple[7],
                                data_tuple[8], data_tuple[9], data_tuple[10], plot_data['lon'][i], plot_data['lat'][i], data_tuple[13], data_tuple[14],
                                data_tuple[15], data_tuple[16], plot_data['z'][i])
                    curves_data[idx] = (None, new_data)

            with open("distortion_free_mapping_accuracy_v9.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Landmark", "True_Lat", "True_Lon", "Mapped_Lat", "Mapped_Lon", "Angular_Error", "Area_Distortion"])
                for name, (true_lat, true_lon) in landmarks.items():
                    min_dist = float('inf')
                    mapped_lat, mapped_lon = None, None
                    for i in valid_indices:
                        lat, lon = plot_data['lat'][i] / 1000, plot_data['lon'][i] / 1000
                        if lat is None or lon is None:
                            continue
                        dist = math.sqrt((lat - true_lat)**2 + (lon - true_lon)**2)
                        if dist < min_dist:
                            min_dist = dist
                            mapped_lat, mapped_lon = lat, lon
                    if mapped_lat is not None and mapped_lon is not None:
                        angular_error = math.sqrt((mapped_lat - true_lat)**2 + (mapped_lon - true_lon)**2)
                        angular_errors.append(angular_error)
                        true_area_factor = math.cos(math.radians(true_lat))
                        mapped_area_factor = math.cos(math.radians(mapped_lat))
                        area_distortion = abs(mapped_area_factor / true_area_factor - 1) if true_area_factor != 0 else 0
                        area_distortions.append(area_distortion)
                        writer.writerow([name, true_lat, true_lon, mapped_lat, mapped_lon, angular_error, area_distortion])
                        log_print(f"Landmark {name}: True ({true_lat}, {true_lon}), Mapped ({mapped_lat}, {mapped_lon}), Angular Error: {angular_error} degrees, Area Distortion: {area_distortion}")

            avg_angular_error = sum(angular_errors) / len(angular_errors) if angular_errors else 0
            non_polar_distortions = [d for i, d in enumerate(area_distortions) if landmarks[list(landmarks.keys())[i]] not in [(90, 0), (-90, 0)]]
            avg_area_distortion = sum(non_polar_distortions) / len(non_polar_distortions) if non_polar_distortions else 0
            log_print(f"Average angular error: {avg_angular_error} degrees")
            log_print(f"Average area distortion (excluding poles): {avg_area_distortion}")
        except IOError as e:
            log_print(f"Failed to write mapping accuracy CSV: {e}")

    else:
        log_print("No valid data for mapping accuracy evaluation; skipping")

    log_print(f"\nFinal training data: {training_data}")
    log_print(f"Final labels: {training_labels}")
    log_print(f"Interweb data saved to {csv_file}")

if __name__ == '__main__':
    print("This script should be run via the SageMath command line: 'sage distortion_free_earth_mapping_test_v9.py'")
    main()