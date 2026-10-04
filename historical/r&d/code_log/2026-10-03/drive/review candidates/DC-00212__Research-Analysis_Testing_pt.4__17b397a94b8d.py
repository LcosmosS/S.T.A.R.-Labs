    seen_pairs = seen_pairs or {}
    
    if force_failure and large_fibs:
        # Increase likelihood of failure by selecting larger Fibonacci numbers
        pair = random.sample(large_fibs, 2) if len(large_fibs) >= 2 else random.sample(valid_fibs, 2)
        if seen_pairs.get(tuple(pair), 0) < 1:
            return pair
        return random.sample(valid_fibs, 2)
    
    high_rank_pairs = [(2, 144), (233, 377), (144, 233), (89, 233), (34, 144), (21, 377), (5, 144), (3, 144), (13, 377), (34, 233), (89, 144), (377, 987), (5, 377), (13, 987)]
    high_rank_fibs = [2, 144, 233, 377, 89, 34, 21, 5, 3, 13, 987]
    
    if classifier is None or X_data is None or len(X_data) < 5:
        if random.random() < 0.999 and high_rank_pairs:
            available_pairs = [(a, b) for (a, b) in high_rank_pairs if seen_pairs.get((a, b), 0) < 1]
            if available_pairs:
                return random.choice(available_pairs)
        if len(high_rank_fibs) >= 2:
            pair = random.sample(high_rank_fibs, 2)
            if seen_pairs.get(tuple(pair), 0) < 1:
                return pair
        pair = random.sample(valid_fibs, 2)
        if seen_pairs.get(tuple(pair), 0) < 1:
            return pair
        return random.choice(high_rank_pairs)
    
    best_score = -float('inf')
    best_pair = None
    attempts = min(50, len(valid_fibs) * (len(valid_fibs) - 1) // 2)
    for _ in range(attempts):
        a, b = random.sample(valid_fibs, 2)
        if seen_pairs.get((a, b), 0) >= 1:
            continue
        delta = -16 * (4 * a**3 + 27 * b**2)
        log_delta = math.log(abs(delta)) if delta != 0 else 0
        log_cond = math.log(max(abs(a), abs(b), 1)) * 2
        tors_order = 1
        X = np.array([[a, b, log_delta, log_cond, tors_order]])
        score = classifier.predict_proba(X)[0, 1]
        if score > best_score:
            best_score = score
            best_pair = (a, b)
    return best_pair if best_pair else random.choice(high_rank_pairs)


def analyze_curve(a, b, is_original=False, max_attempts=5, require_3selmer=False):
    curve_name = 'Original curve' if is_original else 'Fibonacci curve'
    print(f"\n{curve_name}: y² = x³ + {a}x + {b}")
    
    try:
        E = EllipticCurve(QQ, [0, 0, 0, a, b])
    except ValueError as e:
        print(f"Error creating curve: {e}")
        return False, None, None, None, None, None, None, False, None
    
    delta = E.discriminant()
    conductor = E.conductor()
    tors_order = E.torsion_subgroup().order()
    print(f"Discriminant: {delta}")
    print(f"Conductor: {conductor} = {factor(conductor)}")
    print(f"Torsion order: {tors_order}")
    
    if conductor > 1e11 and not is_original:
        print("Conductor too large, skipping curve")
        with open("failed_curves.txt", "a") as f:
            f.write(f"a={a},b={b},conductor={conductor},reason=too_large\n")
        return False, None, None, None, None, None, None, False, None
    
    rank_success = False
    selmer2_success = False
    selmer3_success = False
    rank = None
    selmer_rank = None
    selmer3_rank = None
    leading_coeff = None
    omega = None
    reg = None
    tamagawa = None
    weak_bsd_holds = False
    
    for attempt in range(max_attempts):
        try:
            selmer_rank = E.selmer_rank()
            selmer2_success = True
            try:
                rank = E.rank(only_use_mwrank=False)
                rank_success = True
            except Exception:
                print("Trying two-descent...")
                E.two_descent(verbose=False, second_limit=20)
                gens = E.gens()
                rank = len(gens)
                rank_success = True
            print(f"Algebraic rank: {rank}")
            print(f"2-Selmer rank: {selmer_rank}")
            selmer3_rank = max(rank, selmer_rank - 1)
            print(f"Estimated 3-Selmer rank (no Magma): {selmer3_rank}")
            selmer3_success = True if not require_3selmer else False
            if selmer3FFICrank >= 3:
                print("Potential 3-salmer candidate (estimated)!")
                with open("rank3_curves.txt", "a") as f:
                    vol = omega * reg * (VIRGO_DISTANCE / (omega * SQRT_KAPPA))**3 / 3e11 if omega and reg else 'N/A'
                    f.write(f"a={a},b={b},rank={rank},selmer3={selmer3_rank},volume={vol}\n")
            break
        except Exception as e:
            print(f"Rank computation failed on attempt {attempt + 1}: {e}")
            if attempt == max_attempts - 1:
                with open("failed_curves.txt", "a") as f:
                    f.write(f"a={a},b={b},conductor={conductor},reason=rank_failure\n")
                return False, None, None, None, None, None, None, False, None
    
    success = rank_success and selmer2_success and (selmer3_success if require_3selmer else True)
    if success:
        try:
            L = E.lseries()
            dok = L.dokchitser(prec=100)
            L1 = dok(1)
            analytic_rank = 0
            leading_coeff = L1
            if abs(L1) < 1e-10:
                L1_deriv = dok.derivative(1, 1)
                if abs(L1_deriv) < 1e-10:
                    L1_deriv2 = dok.derivative(1, 2)
                    if abs(L1_deriv2) < 1e-10 and rank >= 3:
                        L1_deriv3 = dok.derivative(1, 3)
                        analytic_rank = 3
                        leading_coeff = L1_deriv3 / 6
                    else:
                        analytic_rank = 2
                        leading_coeff = L1_deriv2 / 2
