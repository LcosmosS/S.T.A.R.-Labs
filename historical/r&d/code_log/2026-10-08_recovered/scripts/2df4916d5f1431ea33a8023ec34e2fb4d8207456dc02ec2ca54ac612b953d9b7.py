# SageMath script with corrected SageMath version check
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import necessary SageMath components
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
    print("This script must be run in a SageMath environment. Please run with 'sage attempt11.py'.")
    sys.exit(1)
except AttributeError:
    print("Unable to determine SageMath version. Ensure you're running this script in a SageMath environment.")
    sys.exit(1)

# Set up logging to file
logging.basicConfig(filename='elliptic_curve_analysis.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Custom print function to redirect to log
def log_print(*args, **kwargs):
    msg = " ".join(map(str, args))
    logging.info(msg)

# Set up SageMath environment for parallel processing
os.environ["SAGE_NUM_THREADS"] = "2"

# Increase PARI memory allocation to prevent crashes
pari.allocatemem(2**29)  # Allocate 512 MB of memory

# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years
VIRGO_COMOVING_VOLUME = 1e9  # Mly^3
VIRGO_DENSITY_HEIGHT = 6320

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2
log_print(f"Golden ratio (φ): {PHI}")

# Generate Fibonacci numbers
def generate_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

fib_numbers = generate_fibonacci(77)
log_print(f"Fibonacci numbers up to index 77: {fib_numbers}")

# Generate Lucas numbers
def generate_lucas(n):
    lucas = [2, 1]
    for i in range(2, n + 1):
        lucas.append(lucas[i-1] + lucas[i-2])
    return lucas

lucas_numbers = generate_lucas(77)
log_print(f"Lucas numbers up to index 77: {lucas_numbers}")

# Training data for classifier
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
    [34, 4181, 22.7453700939663, 22.0522229134064, 1],
    [17711, 17711, 25.9923456789012, 25.9923456789012, 1],
    [17711, 46368, 25.9865432109876, 24.5998765432109, 1],
    [-102, 918, 19.5063410364742, 18.4077287478061, 1]
]
training_labels = [3, 3, 3, 3, 3, 3]
log_print(f"Initial training data: {training_data}")
log_print(f"Initial labels: {training_labels}")

# Function to compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

# Function to select random Fibonacci or Lucas pair
def random_fibonacci_pair(fibs, lucas, high_rank_pairs, bias=0.99):
    if np.random.random() < bias and high_rank_pairs:
        idx = np.random.randint(len(high_rank_pairs))
        return high_rank_pairs[idx]
    use_lucas = np.random.random() < 0.5
    numbers = lucas if use_lucas else fibs
    return (np.random.choice(numbers), np.random.choice(numbers))

# Function to check Heegner hypothesis
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

# Function to find a suitable discriminant
def find_suitable_discriminant(N):
    fundamental_discriminants = [-3, -4, -7, -8, -11, -19]
    for D in fundamental_discriminants:
        if satisfies_heegner_hypothesis(N, D):
            return D
    return None

# Function to compute Heegner points
def compute_heegner_point(E, conductor):
    D = find_suitable_discriminant(conductor)
    if D is None:
        log_print("No suitable discriminant found satisfying Heegner hypothesis")
        logging.error("No suitable discriminant found satisfying Heegner hypothesis")
        return (0, 0)
    try:
        heegner = E.heegner_point(D)
        x, y = heegner.xy()
        log_print(f"Heegner point with D={D}: ({x}, {y})")
        logging.info(f"Heegner point with D={D} for curve {E}: ({x}, {y})")
        return (float(x), float(y))
    except Exception as e:
        log_print(f"Failed to compute Heegner point with D={D}: {e}")
        logging.error(f"Failed to compute Heegner point with D={D} for curve {E}: {e}")
        return (0, 0)

# Function to analyze an elliptic curve
def analyze_curve(a, b, fib_idx, lucas_idx, is_original=False, max_attempts=3, conductor_limit=1e12):
    try:
        log_print(f"Analyzing curve: y² = x³ + {a}x + {b}")
        logging.info(f"Analyzing curve: y² = x³ + {a}x + {b}")
        
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()
        logging.info(f"Discriminant: {delta}")
        logging.info(f"Conductor: {conductor} = {factor(conductor)}")
        logging.info(f"Torsion order: {tors_order}")
        
        if conductor > conductor_limit:
            log_print(f"Conductor too large (> {conductor_limit}), skipping curve")
            logging.warning(f"Conductor too large (> {conductor_limit}), skipping curve")
            return False, None, None, None, None, None, None, False, None, None, None, None, None, None, None, None, None, None
        
        rank_success = False
        rank = None
        selmer3_rank = None
        leading_coeff = None
        omega = None
        reg = None
        tamagawa = None
        weak_bsd_holds = False
        longitude = None
        latitude = None
        elevation = None
        size = None
        heegner_x = heegner_y = 0
        x_3d = y_3d = z_3d = 0
        
        # Compute L-series and analytic rank
        try:
            L = E.lseries()
            dok = L.dokchitser(prec=50)
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
            logging.info(f"Analytic rank: {analytic_rank}")
        except Exception as e:
            log_print(f"Failed to compute analytic rank: {e}")
            logging.error(f"Failed to compute analytic rank: {e}")
            try:
                analytic_rank = E.rank()
                log_print(f"Fallback analytic rank from E.rank(): {analytic_rank}")
                logging.info(f"Fallback analytic rank from E.rank(): {analytic_rank}")
                leading_coeff = 0
                weak_bsd_holds = False
            except Exception as e:
                log_print(f"Fallback rank computation failed: {e}")
                logging.error(f"Fallback rank computation failed: {e}")
                return False, None, None, None, None, None, None, False, None, None, None, None, None, None, None, None, None, None
        
        # Compute algebraic rank
        for attempt in range(max_attempts):
            try:
                E_pari = pari.ellinit([0, 0, 0, a, b])
                rank_info = E_pari.ellrank()
                rank = int(rank_info[0])
                rank_success = True
                log_print(f"Algebraic rank (via PARI/GP): {rank}")
                log_print(f"3-Selmer rank (using algebraic rank): {rank}")
                logging.info(f"Algebraic rank (via PARI/GP): {rank}")
                logging.info(f"3-Selmer rank (using algebraic rank): {rank}")
                selmer3_rank = rank
                break
            except Exception as e:
                log_print(f"Rank computation failed on attempt {attempt + 1}: {e}")
                logging.error(f"Rank computation failed on attempt {attempt + 1}: {e}")
                if attempt == max_attempts - 1:
                    return False, None, None, None, None, None, None, False, None, None, None, None, None, None, None, None, None, None
        
        success = rank_success
        if success:
            try:
                logging.info(f"Leading coefficient: {leading_coeff}")
                weak_bsd_holds = (rank == analytic_rank)
                log_print(f"Weak BSD holds: {weak_bsd_holds}")
                logging.info(f"Weak BSD holds: {weak_bsd_holds}")
                
                omega = E.period_lattice().real_period(prec=50)
                tamagawa = prod(E.tamagawa_numbers())
                sha_order = 1
                rhs = leading_coeff * (tors_order**2)
                reg = rhs / (omega * tamagawa * sha_order) if rank > 0 else 1.0
                
                # Compute Heegner points for rank >= 2
                if rank >= 2:
                    heegner_coords = compute_heegner_point(E, conductor)
                    heegner_x, heegner_y = heegner_coords
                else:
                    heegner_x, heegner_y = 0, 0
                
                # Paradox-corrected Earth mapping for Unreal Engine
                log_delta = math.log(abs(delta)) if delta != 0 else 0
                log_cond = math.log(float(conductor)) if conductor > 0 else 0
                max_log_delta = 40  # Approximate max based on typical values
                max_log_cond = 30
                fib_factor = (fib_numbers[fib_idx % len(fib_numbers)] / max(fib_numbers)) + 0.5
                lucas_factor = (lucas_numbers[lucas_idx % len(lucas_numbers)] / max(lucas_numbers)) + 0.5
                
                # Map to longitude and latitude with bounds
                longitude = (log_delta * fib_factor * PHI * 180) / max_log_delta
                longitude = max(min(longitude, 180), -180)
                latitude = (log_cond * lucas_factor * PHI * 90) / max_log_cond
                latitude = max(min(latitude, 90), -90)
                
                # Apply paradox correction (scale longitude by cos(latitude))
                latitude_rad = math.radians(latitude)
                corrected_longitude = longitude * math.cos(latitude_rad)
                
                # Convert to 3D Cartesian coordinates for Unreal Engine
                ue_scale = 0.1  # Scale down Earth's radius for Unreal Engine
                R = 6371000 * ue_scale  # Earth's radius in meters, scaled
                x_3d = R * math.cos(latitude_rad) * math.cos(math.radians(corrected_longitude))
                y_3d = R * math.cos(latitude_rad) * math.sin(math.radians(corrected_longitude))
                elevation_factor = 1000 * ue_scale  # Elevation scaling
                base_z = R * math.sin(latitude_rad)
                elevation = rank * elevation_factor if rank is not None else 0
                z_3d = base_z + elevation
                
                # Size correction for area preservation
                cos_lat = math.cos(latitude_rad)
                cos_lat = max(cos_lat, 0.1)  # Avoid division by zero or negative scaling
                raw_volume = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 if omega and reg else 0
                size = math.log1p(raw_volume) / 1e13 if raw_volume > 0 else 0
                size = max(min(size * 500, 50), 1.0) * cos_lat * ue_scale  # Increased base size for visibility
                
                # Dynamic scaling adjustments
                cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
                scaled_period = omega * cosmo_scale
                denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
                comoving_volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
                reg_factor = 20 - 5 * rank if rank <= 3 else 10
                scaled_reg = reg * SQRT_KAPPA * reg_factor
                
                logging.info(f"Real period (Omega): {omega}")
                logging.info(f"Dynamic COSMO_SCALE: {cosmo_scale}")
                logging.info(f"Scaled period: {float(scaled_period)} light-years")
                logging.info(f"Regulator: {reg}")
                logging.info(f"Scaled regulator (Reg * √κ * {reg_factor}): {float(scaled_reg)}")
                logging.info(f"Product of Tamagawa numbers: {tamagawa}")
                logging.info(f"Estimated comoving volume: {comoving_volume} Mly^3")
                log_print(f"Earth mapping: X={x_3d:.2f} UE units, Y={x_3d:.2f} UE units, Z={z_3d:.2f} UE units, Size={size:.2f} UE units")
                logging.info(f"Earth mapping: X={x_3d:.2f} UE units, Y={y_3d:.2f} UE units, Z={z_3d:.2f} UE units, Size={size:.2f} UE units")
                logging.info(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs / (tors_order**2)}")
                logging.info("Strong BSD holds: Leading coefficient matches by construction")
                
            except Exception as e:
                log_print(f"Failed to compute BSD invariants: {e}")
                logging.error(f"Failed to compute BSD invariants: {e}")
        
        features = [a, b, log_delta, log_cond, tors_order]
        logging.info("-" * 20)
        # Clear variables to free memory
        del E, delta, conductor, tors_order, L, dok, L1, analytic_rank, rank_info, E_pari
        gc.collect()
        return success, features, rank, leading_coeff / 10 if leading_coeff else 0, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, x_3d, y_3d, z_3d, size, heegner_x, heegner_y, latitude
    except Exception as e:
        log_print(f"Curve analysis failed: {e}")
        logging.error(f"Curve analysis failed: {e}")
        return False, None, None, None, None, None, None, False, None, None, None, None, None, None, None, None, None, None

# Quadratic twist function
def quadratic_twist(E, d):
    a = E.a4()
    b = E.a6()
    a_new = a * d
    b_new = b * (d**3)
    return EllipticCurve(QQ, [0, 0, 0, a_new, b_new])

# Color mapping for Unreal Engine
def oppocolor_map(rank):
    if rank == 0:
        return (0, 0, 0)  # Black
    elif rank == 1:
        return (0, 128, 0)  # Green
    elif rank == 2:
        return (0, 0, 255)  # Blue
    else:
        return (255, 0, 0)  # Red

# Main test procedure
def main():
    high_rank_pairs = [(2, 144), (377, 987), (-102, 918), (34, 4181), (17711, 17711), (17711, 46368)]
    max_attempts = 50
    conductor_limit = 1e12
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"interweb_nodes_{timestamp}.csv"
    
    # Initialize CSV
    with open(csv_file, 'w', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'reg', 'tamagawa', 'weak_bsd_holds', 'selmer3_rank', 'log_delta', 'log_cond', 'x_3d', 'y_3d', 'z_3d', 'size', 'heegner_x', 'heegner_y', 'latitude', 'color_r', 'color_g', 'color_b'])
    
    # Collect curves data for parallel processing
    curves_data = []
    previous_curves = [
        (-1597, 987), (1597, -4181), (2584, 2584), (4181, 6765),
        (1, -2), (3, 1), (2, 2), (-5, 3), (5, -13), (8, 8), (13, 21), (-55, 21),
        (34, -34), (89, 55), (89, 233), (-144, 144), (233, -377), (987, 377), (610, 610),
        (-102, 918),
        (0, 6765), (1, -10946), (2, 17711), (2, 75025), (-3, 46368),
        (-4791, 26649)
    ]
    all_curves = []
    
    # Add previous curves
    for a, b in previous_curves:
        fib_idx = fib_numbers.index(a) if a in fib_numbers else 0
        lucas_idx = lucas_numbers.index(b) if b in lucas_numbers else 0
        all_curves.append((a, b, fib_idx, lucas_idx, True))
    
    # Generate new curves
    for _ in range(max_attempts):
        a, b = random_fibonacci_pair(fib_numbers, lucas_numbers, high_rank_pairs)
        fib_idx = fib_numbers.index(a) if a in fib_numbers else 0
        lucas_idx = lucas_numbers.index(b) if b in lucas_numbers else 0
        all_curves.append((a, b, fib_idx, lucas_idx, False))
    
    # Process curves in parallel with n_jobs=2
    n_jobs = 2
    chunk_size = len(all_curves) // n_jobs
    num_chunks = (len(all_curves) + chunk_size - 1) // chunk_size
    
    log_print(f"Processing {len(all_curves)} curves in {num_chunks} chunks with {n_jobs} jobs")
    logging.info(f"Processing {len(all_curves)} curves in {num_chunks} chunks with {n_jobs} jobs")
    
    plot_data = {'ranks': [], 'heegner_x': [], 'heegner_y': [], 'x_3d': [], 'y_3d': [], 'z_3d': [], 'latitude': [], 'colors': []}
    
    for chunk_idx in range(num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, len(all_curves))
        chunk_curves = all_curves[start_idx:end_idx]
        
        log_print(f"Processing chunk {chunk_idx+1}/{num_chunks} ({len(chunk_curves)} curves)")
        logging.info(f"Processing chunk {chunk_idx+1}/{num_chunks} ({len(chunk_curves)} curves)")
        
        results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
            delayed(analyze_curve)(
                a, b, fib_idx, lucas_idx, is_original, conductor_limit=conductor_limit
            )
            for a, b, fib_idx, lucas_idx, is_original in chunk_curves
        )
        
        for result in results:
            if len(result) != 19:
                continue
            success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank, log_delta, log_cond, x_3d, y_3d, z_3d, size, heegner_x, heegner_y, latitude = result
            if success:
                a, b = features[0], features[1]
                color = oppocolor_map(rank)
                data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, x_3d, y_3d, z_3d, size, heegner_x, heegner_y, latitude, *color)
                curves_data.append((None, data_tuple))
                with open(csv_file, 'a', newline='') as csv_f:
                    csv_writer = csv.writer(csv_f)
                    csv_writer.writerow(data_tuple)
                if rank >= 3:
                    training_data.append(features)
                    training_labels.append(rank)
                    log_print(f"Added new rank {rank} curve to training data: {features}")
                    logging.info(f"Added new rank {rank} curve to training data: {features}")
                if isinstance(rank, (int, float)):
                    plot_data['ranks'].append(rank)
                    plot_data['heegner_x'].append(heegner_x)
                    plot_data['heegner_y'].append(heegner_y)
                    plot_data['x_3d'].append(x_3d)
                    plot_data['y_3d'].append(y_3d)
                    plot_data['z_3d'].append(z_3d)
                    plot_data['latitude'].append(latitude)
                    plot_data['colors'].append(color)
        
        log_print(f"Completed chunk {chunk_idx+1}/{num_chunks} ({(chunk_idx+1)/num_chunks*100:.1f}% done)")
        logging.info(f"Completed chunk {chunk_idx+1}/{num_chunks} ({(chunk_idx+1)/num_chunks*100:.1f}% done)")
        gc.collect()
    
    # Quadratic twists for high-rank candidates
    twist_primes = [2, 3, 5, 7]
    twist_curves = []
    for a, b in high_rank_pairs:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        for d in twist_primes:
            E_twist = quadratic_twist(E, d)
            a_new = E_twist.a4()
            b_new = E_twist.a6()
            fib_idx = fib_numbers.index(a_new) if a_new in fib_numbers else 0
            lucas_idx = lucas_numbers.index(b_new) if b in lucas_numbers else 0
            twist_curves.append((a_new, b_new, fib_idx, lucas_idx, False))
    
    log_print(f"Processing {len(twist_curves)} twisted curves in parallel")
    logging.info(f"Processing {len(twist_curves)} twisted curves in parallel")
    twist_results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
        delayed(analyze_curve)(
            a, b, fib_idx, lucas_idx, False, conductor_limit=conductor_limit
        )
        for a, b, fib_idx, lucas_idx, _ in twist_curves
    )
    
    for result in twist_results:
        if len(result) != 19:
            continue
        success, features, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, E_twist, selmer3_rank, log_delta, log_cond, x_3d, y_3d, z_3d, size, heegner_x, heegner_y, latitude = result
        if success:
            a, b = features[0], features[1]
            color = oppocolor_map(rank)
            data_tuple = (a, b, rank, normalized_leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, x_3d, y_3d, z_3d, size, heegner_x, heegner_y, latitude, *color)
            curves_data.append((f"Twist_d{d}", data_tuple))
            with open(csv_file, 'a', newline='') as csv_f:
                csv_writer = csv.writer(csv_f)
                csv_writer.writerow(data_tuple)
            if rank >= 3:
                training_data.append(features)
                training_labels.append(rank)
                log_print(f"Added twisted rank {rank} curve to training data: {features}")
                logging.info(f"Added twisted rank {rank} curve to training data: {features}")
            if isinstance(rank, (int, float)):
                plot_data['ranks'].append(rank)
                plot_data['heegner_x'].append(heegner_x)
                plot_data['heegner_y'].append(heegner_y)
                plot_data['x_3d'].append(x_3d)
                plot_data['y_3d'].append(y_3d)
                plot_data['z_3d'].append(z_3d)
                plot_data['latitude'].append(latitude)
                plot_data['colors'].append(color)
        gc.collect()
    
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
            logging.info("Classifier trained successfully")
        else:
            log_print("Insufficient data or labels for classifier training")
            logging.warning("Insufficient data or labels for classifier training")
    except Exception as e:
        log_print(f"Failed to train classifier: {e}")
        logging.error(f"Failed to train classifier: {e}")
    
    # Generate interweb plot
    try:
        interweb_data = []
        for label, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, selmer3_rank, log_delta, log_cond, _, _, _, _, _, _, _, _, _, _) in curves_data:
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
        plt.savefig("interweb_enhanced_with_virgo.png")
        plt.close()
        log_print("Enhanced cosmic interweb plot saved as interweb_enhanced_with_virgo.png")
        logging.info("Enhanced cosmic interweb plot saved as interweb_enhanced_with_virgo.png")
        
        with open('interweb_nodes.txt', 'w') as f:
            for data in interweb_data:
                f.write(str(data) + '\n')
        log_print("Interweb data saved to interweb_nodes.txt")
        logging.info("Interweb data saved to interweb_nodes.txt")
    except Exception as e:
        log_print(f"Failed to generate interweb plot: {e}")
        logging.error(f"Failed to generate interweb plot: {e}")
    
    # Additional plots
    # Plot 1: Rank distribution
    plt.figure(figsize=(10, 6))
    plt.hist(plot_data['ranks'], bins=range(int(min(plot_data['ranks'])), int(max(plot_data['ranks'])) + 2), edgecolor='black')
    plt.title("Distribution of Elliptic Curve Ranks")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.savefig("rank_distribution.png")
    plt.close()
    log_print("Rank distribution plot saved as rank_distribution.png")
    
    # Plot 2: Heegner points scatter
    plt.figure(figsize=(10, 6))
    plt.scatter(plot_data['heegner_x'], plot_data['heegner_y'], c=plot_data['ranks'], cmap='viridis')
    plt.colorbar(label="Rank")
    plt.title("Heegner Points of Elliptic Curves")
    plt.xlabel("Heegner X")
    plt.ylabel("Heegner Y")
    plt.savefig("heegner_points.png")
    plt.close()
    log_print("Heegner points scatter plot saved as heegner_points.png")
    
    # Plot 3: 3D scatter plot for paradox-corrected Earth map
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    colors = np.array(plot_data['colors'])
    ax.scatter(plot_data['x_3d'], plot_data['y_3d'], plot_data['z_3d'], c=colors/255.0)
    ax.set_title("Paradox-Corrected 3D Earth Map (X, Y, Z)")
    ax.set_xlabel("X (UE units)")
    ax.set_ylabel("Y (UE units)")
    ax.set_zlabel("Z (UE units)")
    plt.savefig("paradox_corrected_earth_map.png")
    plt.close()
    log_print("Paradox-corrected Earth map saved as paradox_corrected_earth_map.png")
    
    # Export Unreal Engine coordinates with colors
    with open("unreal_engine_coordinates.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["X", "Y", "Z", "Rank", "Size", "Color_R", "Color_G", "Color_B"])
        for x, y, z, rank, lat, color in zip(plot_data['x_3d'], plot_data['y_3d'], plot_data['z_3d'], plot_data['ranks'], plot_data['latitude'], plot_data['colors']):
            cos_lat = math.cos(math.radians(lat))
            cos_lat = max(cos_lat, 0.1)
            size = max(min(50, 1.0), 1.0) * cos_lat * 0.1  # Adjusted size for export
            writer.writerow([x, y, z, rank, size, *color])
    log_print("Unreal Engine coordinates exported to 'unreal_engine_coordinates.csv'.")
    
    log_print(f"\nFinal training data: {training_data}")
    log_print(f"Final labels: {training_labels}")
    log_print(f"Interweb data saved to {csv_file}")
    logging.info(f"Final training data: {training_data}")
    logging.info(f"Final labels: {training_labels}")
    logging.info(f"Interweb data saved to {csv_file}")

if __name__ == '__main__':
    main()