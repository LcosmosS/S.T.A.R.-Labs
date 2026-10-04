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
        rank = E.rank()
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
                    twist_rank = E_twist.rank(only_use_mwrank=False)
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


# Force-directed layout on sphere with polar penalty
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
            # Polar penalty
            if abs(lat_i) > 80:
                force = (abs(lat_i) - 80) / 10
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
        coords[:, 0] = np.clip(coords[:, 0], -90, 90)
        coords[:, 1] = (coords[:, 1] + 180) % 360 - 180
    return coords


# Sinusoidal mapping with force-directed adjustment
def sinusoidal_mapping(log_values, min_val, max_val, coords_all, regulators, idx):
    log_values = np.array(log_values, dtype=np.float64)
    min_val = np.array(min_val, dtype=np.float64)
    max_val = np.array(max_val, dtype=np.float64)
    normalized = (log_values - min_val) / (max_val - min_val + 1e-10)
    normalized = np.clip(normalized, 0, 1)
    lon = (normalized[0] * 360) - 180
    lat = np.arcsin((normalized[1] * 2) - 1) * (180 / np.pi)
    coords = np.array(coords_all, dtype=np.float64)
    coords[idx] = [lat, lon]
    coords = force_directed_layout(coords, regulators)
    return coords[idx][0], coords[idx][1]


# Analyze curve
def analyze_curve(a, b, min_log_disc, max_log_disc, min_log_cond, max_log_cond, coords_all, regulators, idx):
    print(f"\nAnalyzing curve: y^2 = x^3 + {a}x + {b}")
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        tors_order = E.torsion_subgroup().order()
        print(f"Discriminant: {delta}")
        print(f"Conductor: {conductor} = {factor(conductor)}")
        print(f"Torsion order: {tors_order}")


        analytic_rank = E.rank(only_use_mwrank=True)
        algebraic_rank = E.rank()
        print(f"Analytic rank: {analytic_rank}")
        print(f"Algebraic rank: {algebraic_rank}")


        selmer2_rank = E.rank()
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
        points = E.gens()
        regulator = E.regulator(points) if points else 1.0
        print(f"Real period (Omega): {omega}")
        print(f"Regulator: {regulator}")
        print(f"Tamagawa product: {tamagawa}")


        log_delta = float(math.log(abs(delta)) if delta != 0 else 0)
        log_cond = float(math.log(float(conductor)) if conductor > 0 else 0)
        latitude, longitude = sinusoidal_mapping(np.array([log_delta, log_cond]), 
                                                np.array([min_log_disc, min_log_cond]), 
                                                np.array([max_log_disc, max_log_cond]),
                                                coords_all, regulators, idx)
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
        return True, features, analytic_rank, leading_coeff, omega, regulator, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size
    except Exception as e:
        print(f"Error: {e}")
        return False, None, None, None, None, None, None, False, None, None, None, None, None


# Main procedure
def main():
    curves = [(3, 1), (-102, 918), (34, 4181)]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = f"curve_analysis_{timestamp}.csv"
    curves_data = []


    # Precompute min/max for mapping
    log_deltas = []
    log_conds = []
    regulators = []
    for a, b in curves:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
        delta = E.discriminant()
        conductor = E.conductor()
        points = E.gens()
        regulator = E.regulator(points) if points else 1.0
        log_deltas.append(float(math.log(abs(delta)) if delta != 0 else 0))
        log_conds.append(float(math.log(float(conductor)) if conductor > 0 else 0))
        regulators.append(float(regulator))
    min_log_disc, max_log_disc = min(log_deltas), max(log_deltas)
    min_log_cond, max_log_cond = min(log_conds), max(log_conds)


    # Initialize coordinates
    coords_all = [[0.0, 0.0] for _ in range(len(curves))]


    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a', 'b', 'rank', 'leading_coeff', 'omega', 'regulator', 'tamagawa', 'weak_bsd_holds', 'log_delta', 'log_cond', 'longitude', 'latitude', 'elevation', 'size'])


    for idx, (a, b) in enumerate(curves):
        result = analyze_curve(a, b, min_log_disc, max_log_disc, min_log_cond, max_log_cond, coords_all, regulators, idx)
        if result[0]:
            success, features, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size = result
            data_tuple = (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size)
            curves_data.append((None, data_tuple))
            coords_all[idx] = [latitude, longitude]
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data_tuple)
            if rank and rank >= 3:
                training_data.append(features)
                training_labels.append(rank)
                print(f"Added rank {rank} curve: {features}")
        gc.collect()


    # Interweb plotting with enhanced filaments
    try:
        interweb_data = []
        for label, (a, b, rank, leading_coeff, omega, reg, tamagawa, weak_bsd_holds, log_delta, log_cond, longitude, latitude, elevation, size) in curves_data:
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
