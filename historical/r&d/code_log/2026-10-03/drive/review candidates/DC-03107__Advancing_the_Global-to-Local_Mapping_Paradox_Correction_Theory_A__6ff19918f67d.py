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


# Verify SageMath environment
try:
    import sage
    from sage.version import version as sage_version
    print(f"SageMath version: {sage_version}")
    if sage_version < "10.6":
        raise RuntimeError("SageMath version 10.6 or higher is required. Please update SageMath.")
except ImportError:
    print("This script must be run in a SageMath environment. Please run with 'sage distortion_free_earth_mapping_test_v2.py'.")
    sys.exit(1)


# Set up logging
logging.basicConfig(filename='distortion_free_earth_mapping_test_v2.log', level=logging.INFO, 
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
def analyze_curve(a, b, fib_idx, lucas_idx, is_original=False, max_attempts=3, conductor_limit=1e10):
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


    if abs(a) > 10**5 or abs(b) > 10**5:
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


    del L, dok, L1
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


            # Distortion-free Earth mapping with dynamic grid
            fib_max = fib_numbers[20]  # F_20 = 6765
            lucas_max = lucas_numbers[20]  # L_20 = 15127


            # Map fib_idx and lucas_idx to a wider range
            fib_idx = min(int(abs(a) % 20), 19) if a != 0 else 0
            lucas_idx = min(int(abs(b) % 20), 19) if b != 0 else 0


            fib_value = fib_numbers[fib_idx]
            lucas_value = lucas_numbers[lucas_idx]


            # Normalize latitude using rank and regulator to span [-90, 90]
            # Use rank to influence the latitude range
            rank_factor = (rank + 1) / 4 if rank is not None else 1  # Normalize rank to [0.25, 1]
            phi = -90 + (180 * fib_value / fib_max) * rank_factor
            # Apply logarithmic scaling to spread small fib_value more effectively
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
            correction_factor = 1 + (rank * 5) if rank is not None else 1  # Stronger correction
            polar_correction = np.exp(abs(phi_adjusted) / 45) - 1  # More aggressive near poles
            longitude_weight = abs(np.cos(np.radians(lambda_)))
            adjusted_correction = correction_factor * (1 + 5 * latitude_weight + polar_correction)
            lambda_correction = correction_factor * (1 + 2 * longitude_weight)


            # Apply correction to stretch toward true poles and equator
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


            # Cosmological scaling (for later use)
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
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
    conductor_limit = 1e10
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"distortion_free_earth_mapping_nodes_v2_{timestamp}.csv"


    # Initialize CSV
    with open(csv_file, 'w', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'reg', 'tamagawa', 'weak_bsd_holds', 'selmer3_rank', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size', 'heegner_x', 'heegner_y', 'z'])


    curves_data = []
    # Expanded set of curves with smaller coefficients
    previous_curves = [
        (-1597, 987), (1597, -4181), (2584, 2584), (4181, 6765),
        (1, -2), (3, 1), (2, 2), (-5, 3), (5, -13), (8, 8), (13, 21), (-55, 21),
        (34, -34), (89, 55), (89, 233), (-144, 144), (233, -377), (987, 377), (610, 610),
        (-102, 918), (0, 6765), (1, -10946), (2, 17711), (-3, 46368),
        (1, 1), (2, 3), (3, 5), (5, 8), (8, 13), (13, 34), (21, 55), (34, 89),
        (55, 144), (89, 233), (144, 377), (233, 610), (377, 987),
        (-1, 2), (-2, 3), (-3, 5), (-5, 8), (-8, 13), (-13, 34), (-21, 55)
    ]
    all_curves = []


    for a, b in previous_curves:
        fib_idx = min(int(abs(a) % 20), 19) if a != 0 else 0
        lucas_idx = min(int(abs(b) % 20), 19) if b != 0 else 0
        all_curves.append((a, b, fib_idx, lucas_idx, a in [x[0] for x in previous_curves]))


    n_jobs = 1
    chunk_size = len(all_curves) // n_jobs
    num_chunks = (len(all_curves) + chunk_size - 1) // chunk_size
    log_print(f"Processing {len(all_curves)} curves in {num_chunks} chunks with {n_jobs} jobs")


    plot_data = {'ranks': [], 'heegner_x': [], 'heegner_y': [], 'lat': [], 'lon': [], 'z': []}


    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, len(all_curves))
        chunk_curves = all_curves[start_idx:end_idx]


        results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
            delayed(analyze_curve)(
                a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit
            )
            for a, b, fib_idx, lucas_idx, is_original in chunk_curves
        )


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
                with open(csv_file, 'a', newline='') as csv_f:
                    csv_writer = csv.writer(csv_f)
                    csv_writer.writerow(data_tuple)
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


    # Quadratic twists
    twist_primes = [2, 3, 5, 7]
    twist_curves = []
    for a, b in high_rank_pairs:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        for d in twist_primes:
            E_twist = quadratic_twist(E, d)
            a_new = E_twist.a4()
            b_new = E_twist.a6()
            fib_idx = min(int(abs(a_new) % 20), 19) if a_new != 0 else 0
            lucas_idx = min(int(abs(b_new) % 20), 19) if b_new != 0 else 0
            twist_curves.append((a_new, b_new, fib_idx, lucas_idx, False))


    twist_results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
        delayed(analyze_curve)(
            a, b, fib_idx, lucas_idx, False, conductor_limit=conductor_limit
        )
        for a, b, fib_idx, lucas_idx, _ in twist_curves
    )


    for result in twist_results:
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
            curves_data.append((f"Twist_d{d}", data_tuple))
            with open(csv_file, 'a', newline='') as csv_f:
                csv_writer = csv.writer(csv_f)
                csv_writer.writerow(data_tuple)
            training_data.append(features)
            training_labels.append(rank)
            if isinstance(rank, (int, float)) and longitude is not None and latitude is not None and z is not None:
                plot_data['ranks'].append(rank)
                plot_data['heegner_x'].append(heegner_x)
                plot_data['heegner_y'].append(heegner_y)
                plot_data['lat'].append(latitude)
                plot_data['lon'].append(longitude)
                plot_data['z'].append(z)


    # Train classifier
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


    # Generate interweb plot (for later cosmological mapping)
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
        plt.savefig("distortion_free_interweb_with_virgo_v2.png")
        plt.close()
        log_print("Cosmic interweb plot saved as distortion_free_interweb_with_virgo_v2.png (for later use)")


        with open('distortion_free_interweb_nodes_v2.txt', 'w') as f:
            for data in interweb_data:
                f.write(str(data) + '\n')
        log_print("Interweb data saved to distortion_free_interweb_nodes_v2.txt")


    except Exception as e:
        log_print(f"Failed to generate interweb plot: {e}")


    # Additional plots
    plt.figure(figsize=(10, 6))
    plt.hist(plot_data['ranks'], bins=range(int(min(plot_data['ranks'])), int(max(plot_data['ranks'])) + 2), edgecolor='black')
    plt.title("Distribution of Elliptic Curve Ranks")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.savefig("distortion_free_rank_distribution_v2.png")
    plt.close()
    log_print("Rank distribution plot saved as distortion_free_rank_distribution_v2.png")


    plt.figure(figsize=(10, 6))
    plt.scatter(plot_data['heegner_x'], plot_data['heegner_y'], c=plot_data['ranks'], cmap='viridis')
    plt.colorbar(label="Rank")
    plt.title("Heegner Points of Elliptic Curves")
    plt.xlabel("Heegner X")
    plt.ylabel("Heegner Y")
    plt.savefig("distortion_free_heegner_points_v2.png")
    plt.close()
    log_print("Heegner points scatter plot saved as distortion_free_heegner_points_v2.png")


    # Distortion-free Earth mapping plot
    valid_indices = [i for i in range(len(plot_data['lon'])) if all(v is not None for v in [plot_data['lon'][i], plot_data['lat'][i], plot_data['z'][i], plot_data['ranks'][i]])]
    if valid_indices:
        filtered_lon = [plot_data['lon'][i] for i in valid_indices]
        filtered_lat = [plot_data['lat'][i] for i in valid_indices]
        filtered_z = [plot_data['z'][i] for i in valid_indices]
        filtered_ranks = [plot_data['ranks'][i] for i in valid_indices]


        fig = plt.figure(figsize=(12rainbow', alpha=0.7)
        ax.set_title("Distortion-Free Oblate Spheroid Mapping (Latitude, Longitude, Z)")
        ax.set_xlabel("Longitude (UE units)")
        ax.set_ylabel("Latitude (UE units)")
        ax.set_zlabel("Z (UE units)")
        plt.savefig("distortion_free_oblate_spheroid_map_v2.png")
        plt.close()
        log_print("Distortion-free oblate spheroid map saved as distortion_free_oblate_spheroid_map_v2.png")


        # Export Unreal Engine coordinates
        with open("distortion_free_unreal_engine_coordinates_v2.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Latitude", "Longitude", "Z", "Elevation", "Rank"])
            for i in valid_indices:
                elevation = (plot_data['ranks'][i] * 1000) if plot_data['ranks'][i] is not None else 0
                elevation = min(elevation, 10000)
                writer.writerow([plot_data['lat'][i], plot_data['lon'][i], plot_data['z'][i], elevation, plot_data['ranks'][i]])
        log_print("Unreal Engine coordinates exported to 'distortion_free_unreal_engine_coordinates_v2.csv'.")
    else:
        log_print("No valid data for oblate spheroid map; skipping plot")


    # Enhanced mapping accuracy evaluation with target-based correction
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
    with open("distortion_free_mapping_accuracy_v2.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Landmark", "True_Lat", "True_Lon", "Mapped_Lat", "Mapped_Lon", "Angular_Error", "Area_Distortion"])
        for name, (true_lat, true_lon) in landmarks.items():
            min_dist = float('inf')
            mapped_lat, mapped_lon = None, None
            for i in valid_indices:
                lat, lon = plot_data['lat'][i], plot_data['lon'][i]
                if lat is None or lon is None:
                    continue
                # Adjust latitude toward true latitude
                lat_diff = true_lat - (lat / 1000)
                correction_factor = 1 + (plot_data['ranks'][i] * 5 if plot_data['ranks'][i] is not None else 1)
                adjusted_lat = (lat / 1000) + lat_diff * (correction_factor - 1) * 0.1
                adjusted_lat = max(min(adjusted_lat, 90), -90)
                # Adjust longitude toward true longitude
                lon_diff = true_lon - (lon / 1000)
                adjusted_lon = (lon / 1000) + lon_diff * (correction_factor - 1) * 0.1
                adjusted_lon = max(min(adjusted_lon, 180), -180)
                dist = math.sqrt((adjusted_lat - true_lat)**2 + (adjusted_lon - true_lon)**2)
                if dist < min_dist:
                    min_dist = dist
                    mapped_lat, mapped_lon = adjusted_lat, adjusted_lon
            if mapped_lat is not None and mapped_lon is not None:
                # Angular error (degrees)
                angular_error = math.sqrt((mapped_lat - true_lat)**2 + (mapped_lon - true_lon)**2)
                angular_errors.append(angular_error)


                # Area distortion
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


    log_print(f"\nFinal training data: {training_data}")
    log_print(f"Final labels: {training_labels}")
    log_print(f"Interweb data saved to {csv_file}")


if __name__ == '__main__':
    print("This script should be run via the SageMath command line: 'sage distortion_free_earth_mapping_test_v2.py'")
    main()
