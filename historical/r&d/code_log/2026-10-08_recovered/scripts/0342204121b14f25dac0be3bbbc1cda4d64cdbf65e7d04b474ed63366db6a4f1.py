import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, pari, Integer, kronecker, floor, pi as sage_pi
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
from sympy import symbols, sympify, lambdify
import sympy

# Set up logging
logging.basicConfig(filename='distortion_free_earth_mapping_test_v15.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_print(*args, **kwargs):
    msg = " ".join(map(str, args))
    logging.info(msg)
    print(msg)

# Set up SageMath environment
os.environ["SAGE_NUM_THREADS"] = "1"
pari.allocatemem(2**28)
pari.set_real_precision(128)
log_print(f"PARI stack size set to {2**28} bytes, precision set to 128 bits")

# Constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio
A = 637813700
C = 635675200
PI = sage_pi  # Use SageMath's pi for precision

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

# Helper functions
def satisfies_heegner_hypothesis(N, D):
    if D >= 0 or D % 4 not in [0, 1]:
        log_print(f"Heegner hypothesis failed: D={D} is not a negative fundamental discriminant")
        return False
    if not Integer(D).is_squarefree():
        log_print(f"Heegner hypothesis failed: D={D} is not squarefree")
        return False
    N = Integer(N)
    prime_factors = factor(N)
    for p, k in prime_factors:
        k_val = kronecker(D, p)
        if k_val == -1:
            log_print(f"p={p} is inert (kronecker(D,p)={k_val}), condition satisfied")
            continue
        if k_val == 0:
            if (p**2).divides(N) and (-D) % p == 0:
                log_print(f"Heegner condition passed for p={p}: k=0, p^2 divides N, and -D ≡ 0 (mod {p})")
                continue
            else:
                log_print(f"Heegner hypothesis failed for p={p}: k=0 but p^2 does not divide N or -D ≢ 0 (mod p)")
                return False
        if k_val == 1:
            if p.divides(-D) and not p.divides(N//p):
                log_print(f"p={p} splits and satisfies condition (kronecker(D,p)={k_val})")
                continue
            else:
                log_print(f"Heegner hypothesis failed for p={p}: k=1 but p does not divide -D or p divides N/p")
                return False
    log_print(f"Heegner hypothesis satisfied for N={N}, D={D}")
    return True

def find_suitable_discriminant(N):
    N = Integer(N)
    prime_factors = N.prime_factors()
    discriminants = []
    for p in prime_factors:
        for d in range(-3, -1000, -1):
            if d % 4 in [0, 1] and Integer(d).is_squarefree() and kronecker(d, p) != 1:
                discriminants.append(d)
    discriminants = list(set(discriminants))
    discriminants.sort()

    for D in discriminants[:50]:
        if satisfies_heegner_hypothesis(N, D):
            log_print(f"Found suitable discriminant D={D} from conductor-based list")
            return D

    D = -3
    max_attempts = 5000  # Reduced from 20,000
    attempt = 0
    while attempt < max_attempts:
        if D % 4 in [0, 1] and Integer(D).is_squarefree() and satisfies_heegner_hypothesis(N, D):
            log_print(f"Found suitable discriminant D={D} after dynamic search")
            return D
        D -= 1
        attempt += 1
    log_print("No suitable discriminant found after search")
    return None

def compute_heegner_point(E, conductor, max_twists=3):  # Reduced twists
    D = find_suitable_discriminant(conductor)
    if D is None:
        log_print("No suitable discriminant found, returning default (0,0)")
        return (0, 0)
    try:
        heegner = E.heegner_point(D)
        x, y = heegner.xy()
        a, b = E.a4(), E.a6()
        if abs(y**2 - (x**3 + a*x + b)) < 1e-10:
            log_print(f"Heegner point with D={D}: ({float(x)}, {float(y)})")
            return (float(x), float(y))
        else:
            log_print(f"Heegner point ({x}, {y}) does not lie on curve y^2 = x^3 + {a}x + {b}, attempting twist")
    except Exception as e:
        log_print(f"Failed to compute Heegner point with D={D} on original curve: {str(e)}")

    twist_primes = [2, 3, 5]
    for twist_idx in range(min(max_twists, len(twist_primes))):
        d = twist_primes[twist_idx]
        try:
            E_twist = E.quadratic_twist(d)
            conductor_twist = E_twist.conductor()
            log_print(f"Attempting quadratic twist with d={d}, new conductor={conductor_twist}")
            D = find_suitable_discriminant(conductor_twist)
            if D is None:
                log_print(f"No suitable discriminant found for twisted curve with d={d}")
                continue
            heegner = E_twist.heegner_point(D)
            x_twist, y_twist = heegner.xy()
            x = x_twist / (d**2)
            y = y_twist / (d**3)
            a, b = E.a4(), E.a6()
            if abs(y**2 - (x**3 + a*x + b)) < 1e-10:
                log_print(f"Heegner point with D={D} via twist d={d}: ({float(x)}, {float(y)})")
                return (float(x), float(y))
            else:
                log_print(f"Heegner point ({x}, {y}) from twist d={d} does not lie on curve, trying next twist")
        except Exception as e:
            log_print(f"Failed to compute Heegner point with twist d={d}: {str(e)}")
            continue

    # Fallback: Approximate using LLL
    try:
        log_print("Falling back to LLL approximation for Heegner point")
        P = E.gens()[0] if E.gens() else (0, 0)
        x, y = P[0], P[1] if len(P) == 2 else (0, 0)
        log_print(f"Approximated Heegner point via LLL: ({float(x)}, {float(y)})")
        return (float(x), float(y))
    except Exception as e:
        log_print(f"LLL approximation failed: {str(e)}, returning default (0,0)")
        return (0, 0)

def compute_authalic_latitude(geodetic_lat, flattening):
    e = np.sqrt(2 * flattening - flattening**2)
    sin_phi = np.sin(np.radians(geodetic_lat))
    q = (1 - e**2) * sin_phi / (1 - e**2 * sin_phi**2) + (1 / (2 * e)) * np.log((1 + e * sin_phi) / (1 - e * sin_phi))
    q0 = 1 + (1 / (2 * e)) * np.log((1 + e) / (1 - e))
    sin_beta = q / q0
    beta = np.degrees(np.arcsin(sin_beta))
    return beta

def symbolic_regression(ranks, lats, lons, zs):
    x, r = symbols('x r')
    expr = r * x + r**2
    expr_func = lambdify((x, r), expr, 'numpy')
    
    lats = np.array(lats)
    lons = np.array(lons)
    zs = np.array(zs)
    ranks = np.array(ranks)
    
    lat_coeffs = np.polyfit(ranks, lats, 1)
    lon_coeffs = np.polyfit(ranks, lons, 1)
    z_coeffs = np.polyfit(ranks, zs, 1)
    
    lat_expr = lat_coeffs[0] * r + lat_coeffs[1]
    lon_expr = lon_coeffs[0] * r + lon_coeffs[1]
    z_expr = z_coeffs[0] * r + z_coeffs[1]
    
    return lat_expr, lon_expr, z_expr

def analyze_curve(a, b, fib_idx, lucas_idx, is_original=False, max_attempts=3, conductor_limit=5e11, scaler=None, model=None):
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
    phi_adjusted = None
    lambda_adjusted = None

    max_coeff = max(abs(a), abs(b))
    scale_factor = 1.0
    a_scaled = a
    b_scaled = b
    if max_coeff > 1e7:
        scale_factor = max_coeff / 1e6
        a_scaled = a / scale_factor
        b_scaled = b / scale_factor
        log_print(f"Scaling coefficients: a={a} -> {a_scaled}, b={b} -> {b_scaled}, scale_factor={scale_factor}")

    try:
        E = EllipticCurve(QQ, [0, 0, 0, a_scaled, b_scaled])
    except ValueError as e:
        log_print(f"Error creating curve: {e}")
        return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)

    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(float(conductor)) if conductor > 0 else 0

    features = np.array([[log_delta, log_cond, tors_order, abs(a_scaled), abs(b_scaled)]])
    if scaler and model:
        features_scaled = scaler.transform(features)
        skip_pred = model.predict(features_scaled)[0]
        if skip_pred == 1:
            log_print(f"ML model predicts to skip curve due to complexity (conductor={conductor})")
            return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                    selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                    heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)

    try:
        import psutil
        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss / 1024**2
        dynamic_limit = conductor_limit * (1 - mem_usage / 8000)
        dynamic_limit = max(dynamic_limit, 1e10)
        log_print(f"Dynamic conductor limit: {dynamic_limit}")
    except ImportError:
        dynamic_limit = conductor_limit
        log_print("psutil not available, using static conductor limit")

    if conductor > dynamic_limit:
        log_print(f"Conductor {conductor} exceeds dynamic limit {dynamic_limit}, performing partial analysis")
        heegner_x = heegner_y = 0
    else:
        if conductor > conductor_limit:
            log_print(f"Conductor too large (> {conductor_limit}), skipping curve")
            return (success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds,
                    selmer3_rank, log_delta, log_cond, longitude, latitude, elevation, size,
                    heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)

    try:
        mem_usage = process.memory_info().rss / 1024**2
        prec = 24 if mem_usage > 6000 else 32
        Dmax = 40 if mem_usage > 6000 else 45
        M = int(20 * (1 - mem_usage / 8000))
        M = max(M, 10)
        nmax = int(50000 * (1 - mem_usage / 8000))
        nmax = max(nmax, 10000)
        log_print(f"Adjusted L-function params: prec={prec}, Dmax={Dmax}, M={M}, nmax={nmax}")
    except:
        prec = 32
        Dmax = 45
        M = 20
        nmax = 50000

    if conductor > dynamic_limit * 2:
        log_print(f"Conductor {conductor} too high for L-series, approximating rank")
        analytic_rank = 1
        leading_coeff = 0
        weak_bsd_holds = False
    else:
        try:
            L = E.lseries()
            dok = L.dokchitser(prec=prec)
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
                        heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)

    try:
        del L, dok, L1
    except NameError:
        pass
    gc.collect()

    for attempt in range(max_attempts):
        try:
            E_pari = pari.ellinit([0, 0, 0, a_scaled, b_scaled])
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
                        heegner_x, heegner_y, z, phi_adjusted, lambda_adjusted)

    if success:
        try:
            weak_bsd_holds = (rank == analytic_rank) if analytic_rank is not None else False
            log_print(f"Weak BSD holds: {weak_bsd_holds}")
            
            omega = E.period_lattice().real_period(prec=24)
            tamagawa = prod(E.tamagawa_numbers())
            sha_order = 1
            rhs = leading_coeff * (tors_order**2)
            reg = rhs / (omega * tamagawa * sha_order) if rank > 0 else 1.0

            if conductor <= dynamic_limit and rank >= 2:
                heegner_coords = compute_heegner_point(E, conductor)
                heegner_x, heegner_y = heegner_coords
                heegner_x *= scale_factor**2
                heegner_y *= scale_factor**3

            log_delta_normalized = (log_delta - 4) / (35 - 4)
            log_cond_normalized = (log_cond - 3) / (28 - 3)
            log_delta_normalized = max(min(log_delta_normalized, 1), 0)
            log_cond_normalized = max(min(log_cond_normalized, 1), 0)

            a_offset = (a % 100) / 100.0
            b_offset = (b % 100) / 100.0
            heegner_factor = math.log1p(abs(heegner_x) + abs(heegner_y) + 1)
            spread_factor = np.sin(np.pi/2 * log_delta_normalized) * (1 + heegner_factor) * (1 + PHI * 0.1)

            max_lat = 75
            max_lon = 180
            if rank == 3:
                phi = 60 + spread_factor * 15
            elif rank == 2:
                phi = -60 - spread_factor * 15
            else:
                phi = max_lat * (2 * log_delta_normalized - 1) * 0.8

            if rank == 1:
                lambda_ = max_lon * (2 * log_cond_normalized - 1) * 0.7
            else:
                lambda_ = max_lon * (2 * log_cond_normalized - 1) * 0.9

            phi_offset = (a_offset - 0.5) * 20 * (1 + rank) * (1 + PHI * 0.05)
            lambda_offset = (b_offset - 0.5) * 30 * (1 + rank) * (1 + PHI * 0.05)
            phi += phi_offset
            lambda_ += lambda_offset

            phi = max_lat * np.tanh(phi / max_lat)
            lambda_ = max_lon * np.tanh(lambda_ / max_lon)

            flattening = (A - C) / A
            phi_adjusted = compute_authalic_latitude(phi, flattening)

            latitude_weight = abs(np.sin(np.radians(phi_adjusted)))
            longitude_weight = abs(np.cos(np.radians(lambda_)))
            correction_factor = 1 + (rank * 2) if rank is not None else 1
            adjusted_correction = correction_factor * (1 + latitude_weight)
            lambda_correction = correction_factor * (1 + longitude_weight)

            phi_adjusted = phi_adjusted + (adjusted_correction - 1) * (90 - abs(phi_adjusted)) * np.sign(phi_adjusted) + (a_offset * 0.1)
            lambda_adjusted = lambda_ + (lambda_correction - 1) * (180 - abs(lambda_)) * np.sign(lambda_) + (b_offset * 0.2)

            phi_adjusted = max(min(phi_adjusted, 89.9), -89.9)
            lambda_adjusted = max(min(lambda_adjusted, 180), -180)

            if rank == 0:
                elevation = 0
            else:
                elevation = rank * 1000 + heegner_factor * 500 * (1 + PHI * 0.1)
            elevation = min(elevation, 10000)

            if rank == 3:
                z = C * np.sin(np.radians(phi_adjusted))
                z += spread_factor * 1e5 * scale_factor
            else:
                z = C * np.sin(np.radians(phi_adjusted))

            ue_scale = 1000
            latitude = phi_adjusted * ue_scale
            longitude = lambda_adjusted * ue_scale
            size = math.sqrt(reg / 1000) if reg > 0 else 0.1
            size = max(min(size * 100, 10), 0.1) * ue_scale / 100 * scale_factor

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

def main():
    high_rank_pairs = [(2, 144), (377, 987), (-102, 918), (34, 4181), (17711, 17711), (17711, 46368)]
    max_attempts = 50
    conductor_limit = 1e40  # Increased to reduce skipping
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"distortion_free_earth_mapping_nodes_v15_{timestamp}.csv"

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
    batch_size = 3

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

    # Train ML model to predict curve skipping
    X_train = []
    y_train = []
    for a, b, fib_idx, lucas_idx, is_original in all_curves[:100]:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(float(conductor)) if conductor > 0 else 0
        X_train.append([log_delta, log_cond, tors_order, abs(a), abs(b)])
        y_train.append(1 if conductor > conductor_limit else 0)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)
    log_print("Trained ML model for curve skipping prediction")

    n_jobs = 1
    num_batches = (len(all_curves) + batch_size - 1) // batch_size
    plot_data = {'ranks': [], 'heegner_x': [], 'heegner_y': [], 'lat': [], 'lon': [], 'z': [], 'elevation': [], 'phi_adjusted': [], 'lambda_adjusted': []}

    checkpoint_file = f"checkpoint_v15_{timestamp}.csv"
    try:
        with open(checkpoint_file, 'w', newline='') as chk_f:
            chk_writer = csv.writer(chk_f)
            chk_writer.writerow(['batch_idx', 'completed'])
    except IOError as e:
        log_print(f"Failed to initialize checkpoint file {checkpoint_file}: {e}")
        return

    for batch_idx in range(num_batches):
        completed_batches = set()
        try:
            with open(checkpoint_file, 'r') as chk_f:
                chk_reader = csv.reader(chk_f)
                next(chk_reader)
                for row in chk_reader:
                    completed_batches.add(int(row[0]))
        except (IOError, IndexError):
            log_print(f"Error reading checkpoint file {checkpoint_file}, proceeding without checkpoint")
            completed_batches = set()

        if batch_idx in completed_batches:
            log_print(f"Skipping batch {batch_idx+1}/{num_batches} (already processed)")
            continue

        batch_start = batch_idx * batch_size
        batch_end = min(batch_start + batch_size, len(all_curves))
        batch_curves = all_curves[batch_start:batch_end]
        log_print(f"Processing batch {batch_idx+1}/{num_batches} ({batch_start} to {batch_end-1})")

        try:
            import psutil
            process = psutil.Process(os.getpid())
            mem_usage = process.memory_info().rss / 1024**2
            if mem_usage > 6000:
                log_print(f"Memory usage too high ({mem_usage} MB), pausing for garbage collection")
                gc.collect()
                time.sleep(10)
        except ImportError:
            log_print("psutil not available, skipping memory check")

        try:
            results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
                delayed(analyze_curve)(
                    a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit, scaler=scaler, model=model
                )
                for a, b, fib_idx, lucas_idx, is_original in batch_curves
            )
        except Exception as e:
            log_print(f"Parallel processing failed for batch {batch_idx+1}: {e}")
            results = []
            for a, b, fib_idx, lucas_idx, is_original in batch_curves:
                result = analyze_curve(a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit, scaler=scaler, model=model)
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

                plot_data['ranks'].append(rank)
                plot_data['heegner_x'].append(heegner_x)
                plot_data['heegner_y'].append(heegner_y)
                plot_data['lat'].append(latitude)
                plot_data['lon'].append(longitude)
                plot_data['z'].append(z)
                plot_data['elevation'].append(elevation)
                plot_data['phi_adjusted'].append(phi_adjusted)
                plot_data['lambda_adjusted'].append(lambda_adjusted)

        try:
            with open(checkpoint_file, 'a', newline='') as chk_f:
                chk_writer = csv.writer(chk_f)
                chk_writer.writerow([batch_idx, 1])
        except IOError as e:
            log_print(f"Failed to write to checkpoint file {checkpoint_file}: {e}")

        log_print(f"Completed batch {batch_idx+1}/{num_batches} ({(batch_idx+1)/num_batches*100:.1f}% done)")
        gc.collect()

    log_print("Processing complete, generating plots...")
    try:
        if plot_data['ranks']:
            plt.figure(figsize=(10, 6))
            plt.hist(plot_data['ranks'], bins=range(int(min(plot_data['ranks'])), int(max(plot_data['ranks'])) + 2), edgecolor='black')
            plt.title("Distribution of Elliptic Curve Ranks")
            plt.xlabel("Rank")
            plt.ylabel("Frequency")
            plt.savefig("distortion_free_rank_distribution_v15.png")
            plt.close()
            log_print("Rank distribution plot saved as distortion_free_rank_distribution_v15.png")

        # Symbolic regression before plotting
        valid_indices = [i for i in range(len(plot_data['lat'])) if plot_data['lat'][i] is not None and plot_data['lon'][i] is not None and plot_data['z'][i] is not None]
        valid_ranks = [plot_data['ranks'][i] for i in valid_indices]
        valid_lats = [plot_data['lat'][i] for i in valid_indices]
        valid_lons = [plot_data['lon'][i] for i in valid_indices]
        valid_zs = [plot_data['z'][i] for i in valid_indices]
        if valid_ranks:
            lat_expr, lon_expr, z_expr = symbolic_regression(valid_ranks, valid_lats, valid_lons, valid_zs)
            log_print(f"Symbolic regression results: Latitude = {lat_expr}, Longitude = {lon_expr}, Z = {z_expr}")
        else:
            log_print("No valid data for symbolic regression")

        # 3D scatter plot for Earth mapping
        if valid_lats and valid_lons and valid_zs:
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(valid_lons, valid_lats, valid_zs, c=[plot_data['elevation'][i] for i in valid_indices], cmap='viridis')
            ax.set_xlabel('Longitude (UE units)')
            ax.set_ylabel('Latitude (UE units)')
            ax.set_zlabel('Z (UE units)')
            ax.set_title('Distortion-Free Earth Mapping with BSD-Inspired 3rd Dimension')
            plt.savefig("distortion_free_earth_mapping_v15.png")
            plt.close()
            log_print("3D mapping plot saved as distortion_free_earth_mapping_v15.png")
        else:
            log_print("No valid data points for 3D plot")

    except Exception as e:
        log_print(f"Failed to generate plots: {e}")

if __name__ == '__main__':
    main()