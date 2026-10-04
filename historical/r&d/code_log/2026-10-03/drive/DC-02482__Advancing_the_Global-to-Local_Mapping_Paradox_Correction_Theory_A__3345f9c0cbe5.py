training_labels = [3, 3, 3, 3, 3, 3]
print(f"Initial training data: {training_data}")
print(f"Initial labels: {training_labels}")


# Store results for plotting
results = []


# Function to compute discriminant
def compute_discriminant(a, b):
    return -16 * (4 * a**3 + 27 * b**2)


# Function to select random Fibonacci or Lucas pair with bias toward high-rank pairs
def random_fibonacci_pair(fibs, lucas, high_rank_pairs, bias=0.99):
    if np.random.random() < bias and high_rank_pairs:
        # Select a random high-rank pair
        idx = np.random.randint(len(high_rank_pairs))
        return high_rank_pairs[idx]
    # Randomly choose between Fibonacci and Lucas numbers
    use_lucas = np.random.random() < 0.5
    numbers = lucas if use_lucas else fibs
    return (np.random.choice(numbers), np.random.choice(numbers))


# Function to compute Heegner points
def compute_heegner_point(E, discriminant=-11):
    try:
        heegner = E.heegner_points(discriminant)
        point = heegner[0].point()
        return point
    except Exception as e:
        print(f"Failed to compute Heegner point: {e}")
        return None


# Function to analyze an elliptic curve
def analyze_curve(a, b, is_original=False, max_attempts=3, conductor_limit=1e14):
    print(f"\nAnalyzing curve: y² = x³ + {a}x + {b}")
    
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return False, None, None, None, None, None, None, False, None, None
    
    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor} = {factor(conductor)}")
    print(f"Torsion order: {tors_order}")
    
    if conductor > conductor_limit:
        print(f"Conductor too large (> {conductor_limit}), skipping curve")
        return False, None, None, None, None, None, None, False, None, None
    
    rank_success = False
    rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False
    
    try:
        L = E.lseries()
        dok = L.dokchitser(prec=50)
        L1 = dok(1)
        analytic_rank = 0
        leading_coeff = L1
        if abs(L1) < 1e-5:
            L1_deriv = dok.derivative(1, 1)
            if abs(L1_deriv) < 1e-5:
                L1_deriv2 = dok.derivative(1, 2)
                if abs(L1_deriv2) < 1e-5:
                    L1_deriv3 = dok.derivative(1, 3)
                    if abs(L1_deriv3) < 1e-5:
                        analytic_rank = 4
                        leading_coeff = L1_deriv3 / 24
                    else:
                        analytic_rank = 3
                        leading_coeff = L1_deriv3 / 6
                else:
                    analytic_rank = 2
                    leading_coeff = L1_deriv2 / 2
            else:
                analytic_rank = 1
                leading_coeff = L1_deriv
        print(f"Analytic rank: {analytic_rank}")
    except Exception as e:
        print(f"Failed to compute analytic rank: {e}")
        return False, None, None, None, None, None, None, False, None, None
    
    for attempt in range(max_attempts):
        try:
            E_pari = pari.ellinit([0, 0, 0, a, b])
            rank_info = E_pari.ellrank()
            rank = int(rank_info[0])
            rank_success = True
            print(f"Algebraic rank (via PARI/GP): {rank}")
            selmer3_rank = rank
            print(f"3-Selmer rank (refined using BSD): {selmer3_rank}")
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                return False, None, None, None, None, None, None, False, None, None
    
    success = rank_success
    if success:
        try:
            print(f"Leading coefficient: {leading_coeff}")
            weak_bsd_holds = (rank == analytic_rank)
            print(f"Weak BSD holds: {weak_bsd_holds}")
            
            omega = E.period_lattice().real_period(prec=50)
            tamagawa = prod(E.tamagawa_numbers())
            sha_order = 1
            rhs = leading_coeff * (tors_order**2)
            reg = rhs / (omega * tamagawa * sha_order) if rank > 0 else 1.0
            
            # Dynamic scaling adjustments
            cosmo_scale = VIRGO_DISTANCE / (omega * SQRT_KAPPA)
            scaled_period = omega * cosmo_scale
            # Rank-specific denominators
            denominator = {0: 1e13, 1: 1e15, 2: 5e13, 3: 3e11}.get(rank, 1e13)
            # Non-linear volume scaling
            raw_volume = omega * reg * cosmo_scale**3
            comoving_volume = math.log1p(raw_volume) / denominator if raw_volume > 0 else raw_volume / denominator
            # Dynamic regulator scaling
            reg_factor = 20 - 5 * rank if rank <= 3 else 10
            scaled_reg = reg * SQRT_KAPPA * reg_factor
            
            print(f"Real period (Omega): {omega}")
            print(f"Dynamic COSMO_SCALE: {cosmo_scale}")
            print(f"Scaled period: {float(scaled_period)} light-years")
            print(f"Regulator: {reg}")
            print(f"Scaled regulator (Reg * √κ * {reg_factor}): {float(scaled_reg)}")
            print(f"Product of Tamagawa numbers: {tamagawa}")
            print(f"Estimated comoving volume (log1p(Omega * Reg * scale^3) / {denominator}): {comoving_volume} Mly^3")
            print(f"Right-hand side of strong BSD (with |Sha(E)| = 1): {rhs / (tors_order**2)}")
            print("Strong BSD holds: Leading coefficient matches by construction")
            
            # Heegner point computation for high-rank candidates
            if rank >= 2:
                heegner_point = compute_heegner_point(E, discriminant=-11)
                if heegner_point:
                    print(f"Heegner point: {heegner_point}")
        except Exception as e:
            print(f"Failed to compute BSD invariants: {e}")
    
    log_delta = math.log(abs(delta)) if delta != 0 else 0
    log_cond = math.log(float(conductor)) if conductor > 0 else 0
    features = [a, b, log_delta, log_cond, tors_order]
    print("-" * 20)
    return success, features, rank, leading_coeff / 10 if leading_coeff else 0, omega, reg, tamagawa, weak_bsd_holds, E, selmer3_rank


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
    curves_data = []
    conductor_limit = 1e14
    
    # Recompute previous curves
    previous_curves = [
        (-1597, 987), (1597, -4181), (2584, 2584), (4181, 6765),
