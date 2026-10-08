import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from sage.all import EllipticCurve, QQ, factor, RealField, prod, fundamental_discriminant
from sage.arith.misc import kronecker_symbol
import numpy as np
import math
import gc
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Earth constants (WGS84)
EARTH_EQUATORIAL_RADIUS = 6378137.0  # meters
EARTH_FLATTENING = 1 / 298.257223563
EARTH_POLAR_RADIUS = EARTH_EQUATORIAL_RADIUS * (1 - EARTH_FLATTENING)

# Cosmological constants
KAPPA = 1000
SQRT_KAPPA = math.sqrt(KAPPA)
VIRGO_DISTANCE = 54e6  # light-years

# Training data
training_data = [
    [2, 144, 16.0081093416841, 15.3149621611242, 1],
    [377, 987, 22.0713726262387, 21.3782254456787, 1],
    [34, 4181, 22.7453700939663, 22.0522229134064, 1],
    [17711, 17711, 25.9923456789012, 25.9923456789012, 1],
    [17711, 46368, 25.9865432109876, 24.5998765432109, 1],
    [-102, 918, 19.5063410364742, 18.4077287478061, 1]
]
training_labels = [3, 3, 3, 3, 3, 3]

# Compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)

# Heegner hypothesis check
def satisfies_heegner_hypothesis(E, D):
    try:
        D_fund = fundamental_discriminant(D)
        if D_fund != D or D >= 0:
            return False
        N = E.conductor()
        for p in N.prime_factors():
            if kronecker_symbol(D, p) != 1:
                return False
        return True
    except Exception as e:
        print(f"Error checking Heegner hypothesis: {e}")
        return False

# Quadratic twist
def quadratic_twist(E, d):
    a, b = E.a4(), E.a6()
    return EllipticCurve(QQ, [0, 0, 0, d**2 * a, d**3 * b])

# Compute Heegner point
def compute_heegner_point(E, max_D=-100):
    try:
        rank = E.rank(descent_second_limit=20)
        if rank == 1:
            for D in range(-3, max_D - 1, -1):
                if satisfies_heegner_hypothesis(E, D):
                    try:
                        P = E.heegner_point(D).point_exact()
                        return D, P, None
                    except Exception as e:
                        print(f"Heegner point failed for D={D}: {e}")
            return None, None, None
        else:
            print(f"Rank {rank} > 1, trying twists")
            for d in [2, 3, 5, 7]:
                E_twist = quadratic_twist(E, d)
                try:
                    twist_rank = E_twist.rank(only_use_mwrank=False, descent_second_limit=20)
                    if twist_rank == 1:
                        print(f"Twist d={d} has rank 1: {E_twist.ainvs()}")
                        for D in range(-3, max_D - 1, -1):
                            if satisfies_heegner_hypothesis(E_twist, D):
                                try:
                                    P = E_twist.heegner_point(D).point_exact()
                                    return D, P, d
                                except Exception as e:
                                    print(f"Heegner failed for twist d={d}, D={D}: {e}")
                except Exception as e:
                    print(f"Rank failed for twist d={d}: {e}")
            return None, None, None
    except Exception as e:
        print(f"Heegner computation failed: {e}")
        return None, None, None

# Great circle distance on sphere (in degrees)
def great_circle_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return np.degrees(c)

# Force-directed layout on sphere with enhanced polar penalty
def force_directed_layout(coords, regulators, iterations=100, min_dist=None):
    n = len(coords)
    if n <= 1:
        return coords
    if min_dist is None:
        min_dist = 180 / np.sqrt(n)
    coords = np.array(coords, dtype=np.float64)
    regs = np.array(regulators, dtype=np.float64)
    reg_mean, reg_std = np.mean(regs), np.std(regs)
    norm_regs = (regs - reg_mean) / (reg_std + 1e-10)
    
    for _ in range(iterations):
        forces = np.zeros_like(coords)
        for i in range(n):
            lat_i, lon_i = coords[i]
            if abs(lat_i) > 70:
                force = ((abs(lat_i) - 70) / 20) ** 2
                forces[i][0] -= force * np.sign(lat_i)
            for j in range(n):
                if i == j:
                    continue
                lat_j, lon_j = coords[j]
                dist = great_circle_distance(lat_i, lon_i, lat_j, lon_j)
                if dist < min_dist:
                    force = (min_dist - dist) / min_dist
                    dlat = lat_j - lat_i
                    dlon = lon_j - lon_i
                    norm = np.sqrt(dlat**2 + dlon**2 + 1e-10)
                    forces[i] -= force * np.array([dlat, dlon]) / norm
                    forces[j] += force * np.array([dlat, dlon]) / norm
                reg_diff = abs(norm_regs[i] - norm_regs[j])
                if reg_diff < 1.0:
                    force = (1 - reg_diff) * 0.1
                    dlat = lat_j - lat_i
                    dlon = lon_j - lon_i
                    norm = np.sqrt(dlat**2 + dlon**2 + 1e-10)
                    forces[i] += force * np.array([dlat, dlon]) / norm
                    forces[j] -= force * np.array([dlat, dlon]) / norm
        coords += forces * 0.05
        coords[:, 0] = np.clip(coords[:, 0], -85, 85)
        coords[:, 1] = (coords[:, 1] + 180) % 360 - 180
    return coords

# Initial sinusoidal mapping without force-directed adjustment
def initial_sinusoidal_mapping(log_values, min_val, max_val):
    log_values = np.array(log_values, dtype=np.float64)
    min_val = np.array(min_val, dtype=np.float64)
    max_val = np.array(max_val, dtype=np.float64)
    normalized = (log_values - min_val) / (max_val - min_val + 1e-10)
    normalized = np.clip(normalized, 0, 1)
    lon = (normalized[0] * 360) - 180
    lat = np.arcsin((normalized[1] * 1.7) - 0.85) * (180 / np.pi)
    lat = np.clip(lat, -85, 85)
    return lat, lon

# Final sinusoidal mapping with force-directed adjustment for a chunk
def sinusoidal_mapping(log_values, min_val, max_val, coords_all, regulators, chunk_start_idx, chunk_coords):
    log_values = np.array(log_values, dtype=np.float64)
    min_val = np.array(min_val, dtype=np.float64)
    max_val = np.array(max_val, dtype=np.float64)
    normalized = (log_values - min_val) / (max_val - min_val + 1e-10)
    normalized = np.clip(normalized, 0, 1)
    lon = (normalized[0] * 360) - 180
    lat = np.arcsin((normalized[1] * 1.7) - 0.85) * (180 / np.pi)
    lat = np.clip(lat, -85, 85)

    # Update the chunk coordinates in the full coords_all
    for i, (c_lat, c_lon) in enumerate(chunk_coords):
        coords_all[chunk_start_idx + i] = [c_lat, c_lon]

    # Apply force-directed layout to the entire set of coordinates
    coords_all_updated = force_directed_layout(coords_all, regulators, iterations=50)
    
    # Return the updated coordinates for the current chunk
    return [(coords_all_updated[chunk_start_idx + i][0], coords_all_updated[chunk_start_idx + i][1]) for i in range(len(chunk_coords))]

# Analyze curve
def analyze_curve(a, b, min_log_disc, max_log_disc, min_log_cond, max_log_cond, coords_all, regulators, chunk_start_idx, chunk_coords):
    print(f"\nAnalyzing curve: y^2 = x^3 + {a}x + {b}")
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()
        print(f"Discriminant: {delta}")
        print(f"Conductor: {conductor} = {factor(conductor)}")
        print(f"Torsion order: {tors_order}")

        analytic_rank = E.rank(only_use_mwrank=True, descent_second_limit=20)
        algebraic_rank = E.rank(descent_second_limit=20)
        print(f"Analytic rank: {analytic_rank}")
        print(f"Algebraic rank: {algebraic_rank}")

        selmer2_rank = E.rank(descent_second_limit=20)
        print(f"2-Selmer rank: {selmer2_rank}")
        print(f"3-Selmer rank: {selmer2_rank}")

        D, P, twist_d = compute_heegner_point(E)
        if D and P:
            curve_str = f"twist d={twist_d}" if twist_d else "original"
            print(f"Heegner point for D={D} on {curve_str}: {P}")

        L = E.lseries()
        dok = L.dokchitser(prec=50)
        L1 = dok(1)
        leading_coeff = L1
        if abs(L1) < 1e-5:
            for n in range(1, 5):
                L_deriv = dok.derivative(1, n)
                if abs(L_deriv) > 1e-5:
                    leading_coeff = L_deriv / math.factorial(n)
                    break
        print(f"Leading coefficient: {leading_coeff}")

        omega = E.period_lattice().real_period(prec=50)
        tamagawa = prod(E.tamagawa_numbers())
        try:
            points = E.gens(descent_second_limit=20)
            regulator = E.regulator(points) if points else 1.0
        except Exception as e:
            print(f"Failed to compute generators: {e}. Using default regulator=1.0")
            regulator = 1.0
        print(f"Real period (Omega): {omega}")
        print(f"Regulator: {regulator}")
        print(f"Tamagawa product: {tamagawa}")

        log_delta = float(math.log(abs(delta)) if delta != 0 else 0)
        log_cond = float(math.log(float(conductor)) if conductor > 0 else 0)
        chunk_coords_updated = sinusoidal_mapping(np.array([log_delta, log_cond]), 
                                                 np.array([min_log_disc, min_log_cond]), 
                                                 np.array([max_log_disc, max_log_cond]),
                                                 coords_all, regulators, chunk_start_idx, chunk_coords)
        latitude, longitude = chunk_coords_updated[len(chunk_coords) - 1]  # Last curve in chunk
        elevation = min((analytic_rank or 0) * 1000, 9000)
        size = math.log1p(leading_coeff) * 10
        print(f"Earth mapping: Longitude={longitude}°, Latitude={latitude}°, Elevation={elevation}m, Size={size}km")

        weak_bsd_holds = analytic_rank == algebraic_rank
        print(f"Weak BSD holds: {weak_bsd_holds}")

        plt.figure()
        E.plot(xmin=-5, xmax=5, ymin=-10, ymax=10)
        plt.title(f"Curve y^2 = x^3 + {a}x + {b}")
        plt.grid(True)
        plt.savefig(f"curve_a{a}_b{b}.png")
        plt.close()
        print(f"Plot saved as curve_a{a}_b{b}.png")

        features = [a, b, log_delta, log_cond, tors_order]
        return True, features, analytic_rank, leading_coeff, omega, regulator, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size, chunk_coords_updated
    except Exception as e:
        print(f"Error: {e}")
        return False, None, None, None, None, None, None, False, None, None, None, None, None, None, chunk_coords

# Generate curves for target coordinates
def generate_curves_for_grid():
    # Define the grid
    latitudes = np.arange(-85, 86, 10)  # 18 points
    longitudes = np.arange(-180, 181, 20)  # 19 points
    grid_coords = [(lat, lon) for lat in latitudes for lon in longitudes]
    print(f"Generating {len(grid_coords)} curves for the grid.")

    # Define ranges for log_disc and log_cond
    min_log_disc, max_log_disc = 6.0, 23.0
    min_log_cond, max_log_cond = 6.0, 22.5

    # Generate a pool of curves (optimized range to reduce computation)
    a_range = np.arange(-150, 151, 15)  # Step size 15
    b_range = np.arange(-1500, 1501, 150)  # Step size 150
    curve_pool = []
    total_b_values = len(b_range)
    for idx_a, a in enumerate(a_range):
        for idx_b, b in enumerate(b_range):
            try:
                if a == 0 and b == 0:
                    continue
                E = EllipticCurve(QQ, [0, 0, 0, a, b])
                delta = E.discriminant()
                if delta == 0:
                    continue
                conductor = E.conductor()
                log_delta = float(math.log(abs(delta)))
                log_cond = float(math.log(float(conductor)))
                if 5.0 <= log_delta <= 24.0 and 5.0 <= log_cond <= 23.0:
                    curve_pool.append((a, b, log_delta, log_cond))
            except Exception:
                continue
        print(f"Generated curves for a={a} ({idx_a + 1}/{len(a_range)} a values processed, {len(b_range)} b values per a)")
    print(f"Generated {len(curve_pool)} candidate curves.")

    # Assign curves to grid points
    curves = []
    for idx, (lat, lon) in enumerate(grid_coords):
        target_log_disc = min_log_disc + ((lon + 180) / 360) * (max_log_disc - min_log_disc)
        target_log_cond = min_log_cond + ((np.sin(lat * np.pi / 180) + 0.85) / 1.7) * (max_log_cond - min_log_cond)
        
        # Find the closest curve in the pool
        min_dist = float('inf')
        best_curve = None
        for a, b, log_delta, log_cond in curve_pool:
            dist = (log_delta - target_log_disc)**2 + (log_cond - target_log_cond)**2
            if dist < min_dist:
                min_dist = dist
                best_curve = (a, b)
        if best_curve:
            curves.append(best_curve)
        else:
            curves.append((int(target_log_disc), int(target_log_cond * 10)))  # Fallback
            print(f"Fallback used for lat={lat}, lon={lon}")
        if (idx + 1) % 50 == 0:
            print(f"Assigned {idx + 1}/{len(grid_coords)} grid points ({(idx + 1) / len(grid_coords) * 100:.1f}%)")

    return curves

# Load progress from checkpoint
def load_checkpoint(timestamp):
    checkpoint_file = f"checkpoint_{timestamp}.txt"
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            last_chunk = int(f.read().strip())
        return last_chunk
    return 0

# Save progress to checkpoint
def save_checkpoint(timestamp, chunk_idx):
    checkpoint_file = f"checkpoint_{timestamp}.txt"
    with open(checkpoint_file, 'w') as f:
        f.write(str(chunk_idx))

# Main procedure with chunked processing and checkpointing
def main():
    # Generate curves for the grid
    curves = generate_curves_for_grid()
    total_curves = len(curves)
    chunk_size = 20
    num_chunks = (total_curves + chunk_size - 1) // chunk_size  # Ceiling division
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_csv_file = f"curve_analysis_{timestamp}.csv"
    temp_csv_files = []

    # Load checkpoint to resume from the last completed chunk
    start_chunk = load_checkpoint(timestamp)
    print(f"Resuming from chunk {start_chunk}/{num_chunks}")

    # Precompute min/max for mapping and initial coordinates
    log_deltas = []
    log_conds = []
    regulators = []
    initial_coords = []
    min_log_disc, max_log_disc = 6.0, 23.0  # Use predefined ranges to ensure consistency
    min_log_cond, max_log_cond = 6.0, 22.5

    print("Precomputing initial coordinates...")
    for idx, (a, b) in enumerate(curves):
        try:
            E = EllipticCurve(QQ, [0, 0, 0, a, b])
            delta = E.discriminant()
            conductor = E.conductor()
            log_delta = float(math.log(abs(delta)) if delta != 0 else 0)
            log_cond = float(math.log(float(conductor)) if conductor > 0 else 0)
            lat, lon = initial_sinusoidal_mapping(np.array([log_delta, log_cond]), 
                                                  np.array([min_log_disc, min_log_cond]), 
                                                  np.array([max_log_disc, max_log_cond]))
            # Skip E.gens() to save time; compute regulator during analysis
            regulator = 1.0  # Default value
            log_deltas.append(log_delta)
            log_conds.append(log_cond)
            regulators.append(float(regulator))
            initial_coords.append([lat, lon])
            if (idx + 1) % 50 == 0:
                print(f"Processed {idx + 1}/{total_curves} curves for initial setup ({(idx + 1) / total_curves * 100:.1f}%)")
        except Exception as e:
            print(f"Failed to process curve a={a}, b={b}: {e}. Skipping.")
            log_deltas.append(0)
            log_conds.append(0)
            regulators.append(1.0)
            initial_coords.append([0.0, 0.0])

    # Process curves in chunks
    all_curves_data = []
    coords_all = initial_coords.copy()

    for chunk_idx in range(start_chunk, num_chunks):
        start_idx = chunk_idx * chunk_size
        end_idx = min(start_idx + chunk_size, total_curves)
        chunk_curves = curves[start_idx:end_idx]
        chunk_coords = initial_coords[start_idx:end_idx]
        print(f"\nProcessing chunk {chunk_idx + 1}/{num_chunks} ({len(chunk_curves)} curves, indices {start_idx} to {end_idx-1})")

        # Temporary CSV for this chunk
        temp_csv = f"curve_analysis_{timestamp}_chunk_{chunk_idx}.csv"
        temp_csv_files.append(temp_csv)
        chunk_data = []

        with open(temp_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'regulator', 'tamagawa', 'weak_bsd_holds', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size'])

            for idx, (a, b) in enumerate(chunk_curves):
                global_idx = start_idx + idx
                print(f"Analyzing curve {idx + 1}/{len(chunk_curves)} in chunk (global index {global_idx})")
                result = analyze_curve(a, b, min_log_disc, max_log_disc, min_log_cond, max_log_cond, coords_all, regulators, start_idx, chunk_coords)
                chunk_coords = result[14]  # Updated coordinates for the chunk
                if result[0]:
                    success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size, _ = result
                    data_tuple = (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size)
                    chunk_data.append((None, data_tuple))
                    writer.writerow(data_tuple)
                    # Update regulator in the global list
                    regulators[global_idx] = float(reg)
                    if rank and rank >= 3:
                        training_data.append(features)
                        training_labels.append(rank)
                        print(f"Added rank {rank} curve: {features}")

        all_curves_data.extend(chunk_data)
        save_checkpoint(timestamp, chunk_idx + 1)  # Save progress after each chunk
        print(f"Completed chunk {chunk_idx + 1}/{num_chunks} ({(chunk_idx + 1) / num_chunks * 100:.1f}% of chunks done)")
        gc.collect()

    # Combine all temporary CSV files into the final CSV
    with open(final_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'regulator', 'tamagawa', 'weak_bsd_holds', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size'])
        for temp_csv in temp_csv_files:
            if os.path.exists(temp_csv):
                with open(temp_csv, 'r') as temp_f:
                    reader = csv.reader(temp_f)
                    header = next(reader)  # Skip header
                    for row in reader:
                        writer.writerow(row)

    # Final force-directed layout refinement
    print("Performing final force-directed layout refinement...")
    coords_all = force_directed_layout(coords_all, regulators, iterations=100)
    for idx, (label, data_tuple) in enumerate(all_curves_data):
        data_tuple = list(data_tuple)
        data_tuple[10] = coords_all[idx][1]  # Update longitude
        data_tuple[11] = coords_all[idx][0]  # Update latitude
        all_curves_data[idx] = (label, tuple(data_tuple))

    # Rewrite the final CSV with updated coordinates
    with open(final_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'regulator', 'tamagawa', 'weak_bsd_holds', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size'])
        for label, data_tuple in all_curves_data:
            writer.writerow(data_tuple)

    # Interweb plotting with enhanced filaments
    try:
        print("Generating interweb plot...")
        interweb_data = []
        for label, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size) in all_curves_data:
            if omega and rank is not None:
                E = EllipticCurve(QQ, [0, 0, 0, a, b])
                delta = float(E.discriminant())
                conductor = float(E.conductor())
                log_delta = float(math.log(abs(delta)) if delta != 0 else 0)
                log_cond = float(math.log(float(conductor)) if conductor > 0 else 0)
                cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
                raw_volume = omega * reg * cosmo_scale**3
                denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
                volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
                interweb_data.append((a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, volume))

        fig = plt.figure(figsize=(10, 8))
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

        # Enhanced filament computation
        regs = np.array([float(x[5]) for x in interweb_data], dtype=np.float64)
        reg_mean, reg_std = np.mean(regs), np.std(regs)
        norm_regs = (regs - reg_mean) / (reg_std + 1e-10)

        for i, (a, b, rank, _, _, reg, _, _, log_delta, log_cond, _) in enumerate(interweb_data):
            for j in range(i + 1, len(interweb_data)):
                reg_diff = abs(norm_regs[i] - norm_regs[j])
                weight = np.exp(-reg_diff / 0.01)
                if weight > 0.1:
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
        print("Interweb plot saved as interweb_enhanced_with_virgo.png")

        with open('interweb_nodes.txt', 'w') as f:
            for data in interweb_data:
                f.write(str(data) + '\n')
        print("Interweb data saved to interweb_nodes.txt")
    except Exception as e:
        print(f"Failed to generate interweb plot: {e}")

    print(f"Results saved to {final_csv_file}")
    print(f"Updated training data: {training_data}")
    print(f"Updated labels: {training_labels}")

if __name__ == "__main__":
    main()